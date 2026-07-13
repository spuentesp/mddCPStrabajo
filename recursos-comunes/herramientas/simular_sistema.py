#!/usr/bin/env python3
"""Gemelo de simulacion de SVIF: ejecuta ambos componentes ciberfisicos en Python.

Replica la logica del PSM (codigo Arduino) para verificar el flujo completo del
sistema sin hardware: percepcion -> identificacion -> publicacion MQTT ->
evaluacion -> actuacion (cerradura/alarma) -> bitacora.

Cada hilo conserva la trazabilidad con el modelo PIM (mismos IDs, mismos
periodos: monitoreo 500 ms, control de acceso 250 ms) y el dependum comparte la
estructura definida en pim-fm-08 / pim-aa-10.

Uso:
    python3 simular_sistema.py --broker localhost --duracion 10

Requiere: pip install paho-mqtt  (y un broker MQTT, p. ej. mosquitto local)
"""
import argparse
import json
import random
import threading
import time

import paho.mqtt.client as mqtt

TOPIC = "svif/eventos/identificacion"

# Compatibilidad con paho-mqtt 1.x y 2.0+
try:
    CLIENT_API_VERSION = mqtt.CallbackAPIVersion.VERSION2
except AttributeError:
    CLIENT_API_VERSION = None

# SW Resource pim-fm-06 (CIM: cim-r2) — Base de rostros enrolados
ENROLLED_FACES = [
    {"person_id": 1, "person_name": "Ana Perez",   "face_embedding": 0.11, "authorized": True},
    {"person_id": 2, "person_name": "Juan Soto",   "face_embedding": 0.47, "authorized": True},
    {"person_id": 3, "person_name": "Visita Roja", "face_embedding": 0.83, "authorized": False},
]
CONFIDENCE_THRESHOLD = 0.75  # fase Code


# ============================ Face Monitor Component (pim-fm-00 / cim-a1)
class FaceMonitorComponent(threading.Thread):
    """OnIntervalAction pim-fm-01 (cim-g1): monitoreo cada 500 ms."""

    def __init__(self, broker: str, port: int, stop: threading.Event):
        super().__init__(name="FaceMonitor", daemon=True)
        self.stop = stop
        if CLIENT_API_VERSION:
            self.client = mqtt.Client(CLIENT_API_VERSION, client_id="svif-face-monitor-sim")
        else:
            self.client = mqtt.Client(client_id="svif-face-monitor-sim")
        self.client.connect(broker, port)
        self.client.loop_start()

    # pim-fm-02 (cim-t1): Capturar imagen
    def capturar_imagen(self) -> float:
        return random.random()

    # pim-fm-03 (cim-t2): Detectar rostro
    def detectar_rostro(self, frame: float) -> bool:
        # La region baja del "frame" corresponde a rostros cercanos a un
        # enrolado autorizado (Ana) y la region alta a uno no autorizado
        # (Visita Roja), lo que permite ejercitar ambas ramas del OR.
        return frame < 0.30 or frame > 0.70

    # pim-fm-05 (cim-t4): Comparar con rostros enrolados (local => help privacidad)
    def comparar_con_rostros_enrolados(self, face_embedding: float):
        best, best_distance = None, 1.0
        for face in ENROLLED_FACES:
            d = abs(face["face_embedding"] - face_embedding)
            if d < best_distance:
                best, best_distance = face, d
        return best, 1.0 - best_distance

    # pim-fm-04 (cim-t3): Identificar rostro
    def identificar_rostro(self, frame: float) -> dict:
        face, confidence = self.comparar_con_rostros_enrolados(frame)
        if face and confidence >= CONFIDENCE_THRESHOLD:
            return {"timestamp": int(time.time() * 1000),
                    "person_id": face["person_id"],
                    "person_name": face["person_name"],
                    "confidence": round(confidence, 2),
                    "authorized": face["authorized"]}
        return {"timestamp": int(time.time() * 1000), "person_id": -1,
                "person_name": "desconocido",
                "confidence": round(confidence, 2), "authorized": False}

    def run(self):
        while not self.stop.is_set():
            frame = self.capturar_imagen()
            if self.detectar_rostro(frame):
                event = self.identificar_rostro(frame)
                # pim-fm-08 (cim-d1/cim-t5): MessageSender (hurt privacidad: datos
                # personales minimizados por la red)
                self.client.publish(TOPIC, json.dumps(event))
                print(f"[FaceMonitor ] deteccion -> publica {event}")
            self.stop.wait(0.5)  # interval_in_milliseconds = 500
        self.client.loop_stop()


# ============================ Access Actuator Component (pim-aa-00 / cim-a2)
class AccessActuatorComponent(threading.Thread):
    """OnIntervalAction pim-aa-01 (cim-g2): control de acceso cada 250 ms."""

    def __init__(self, broker: str, port: int, stop: threading.Event):
        super().__init__(name="AccessActuator", daemon=True)
        self.stop = stop
        self.pending = None
        self.lock = threading.Lock()
        self.bitacora = []  # SW Resource pim-aa-09 (cim-r5)
        if CLIENT_API_VERSION:
            self.client = mqtt.Client(CLIENT_API_VERSION, client_id="svif-access-actuator-sim")
        else:
            self.client = mqtt.Client(client_id="svif-access-actuator-sim")
        self.client.on_message = self.receiver_callback
        self.client.connect(broker, port)
        self.client.subscribe(TOPIC)
        self.client.loop_start()

    # pim-aa-10 (cim-d1): MessageReceiver
    def receiver_callback(self, client, userdata, msg):
        with self.lock:
            self.pending = json.loads(msg.payload.decode())

    # pim-aa-02 (cim-t6): Evaluar autorizacion
    def evaluar_autorizacion(self, event: dict) -> bool:
        return bool(event.get("authorized")) and event.get("person_id", -1) >= 0

    # pim-aa-04 (cim-t8): Desbloquear cerradura  [HW: rele, pim-aa-07]
    def desbloquear_cerradura(self):
        print("[AccessActuator] >>> RELE ON: cerradura DESBLOQUEADA 5 s "
              "(luego retorna a estado seguro)")

    # pim-aa-05 (cim-t9): Activar alarma  [HW: buzzer, pim-aa-08]
    def activar_alarma(self):
        print("[AccessActuator] >>> BUZZER ON: ALARMA activada 3 s")

    # pim-aa-03 (cim-t7): Gestionar respuesta (refinamiento OR del CIM)
    def gestionar_respuesta_acceso(self, granted: bool) -> str:
        if granted:      # rama OR 1: cim-t8
            self.desbloquear_cerradura()
            return "desbloqueo"
        self.activar_alarma()  # rama OR 2: cim-t9
        return "alarma"

    # pim-aa-06 (cim-t10): Registrar evento (help trazabilidad, cim-q4)
    def registrar_evento_acceso(self, event: dict, action: str):
        entry = {"timestamp": event["timestamp"], "person_id": event["person_id"],
                 "action_taken": action, "confidence": event["confidence"]}
        self.bitacora.append(entry)
        print(f"[AccessActuator] bitacora #{len(self.bitacora)}: {entry}")

    def run(self):
        while not self.stop.is_set():
            event = None
            with self.lock:
                if self.pending is not None:
                    event, self.pending = self.pending, None
            if event:
                granted = self.evaluar_autorizacion(event)
                action = self.gestionar_respuesta_acceso(granted)
                self.registrar_evento_acceso(event, action)
            self.stop.wait(0.25)  # interval_in_milliseconds = 250
        self.client.loop_stop()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--broker", default="localhost")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--duracion", type=int, default=10,
                        help="Segundos de simulacion")
    parser.add_argument("--semilla", type=int, default=None)
    args = parser.parse_args()
    if args.semilla is not None:
        random.seed(args.semilla)

    print(f"=== SVIF: gemelo de simulacion ({args.duracion} s) ===")
    stop = threading.Event()
    actuator = AccessActuatorComponent(args.broker, args.port, stop)
    monitor = FaceMonitorComponent(args.broker, args.port, stop)
    actuator.start()
    monitor.start()
    time.sleep(args.duracion)
    stop.set()
    monitor.join(2)
    actuator.join(2)

    print("\n=== Resumen de la bitacora de accesos ===")
    desbloqueos = sum(1 for e in actuator.bitacora if e["action_taken"] == "desbloqueo")
    alarmas = sum(1 for e in actuator.bitacora if e["action_taken"] == "alarma")
    print(f"Eventos registrados: {len(actuator.bitacora)} "
          f"(desbloqueos: {desbloqueos}, alarmas: {alarmas})")


if __name__ == "__main__":
    main()
