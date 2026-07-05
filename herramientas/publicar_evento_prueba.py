#!/usr/bin/env python3
"""Inyecta un "Evento de identificacion" sintetico en el topico MQTT de SVIF.

Permite probar el Access Actuator Component sin el nodo de camara.

Uso:
    python3 publicar_evento_prueba.py --broker localhost --person-id 1 --authorized
    python3 publicar_evento_prueba.py --broker localhost --person-id -1   # intruso

Requiere: pip install paho-mqtt
"""
import argparse
import json
import time

import paho.mqtt.client as mqtt

NAMES = {1: "Ana Perez", 2: "Juan Soto", 3: "Visita Roja"}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--broker", default="localhost")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--topic", default="svif/eventos/identificacion")
    parser.add_argument("--person-id", type=int, default=1)
    parser.add_argument("--confidence", type=float, default=0.92)
    parser.add_argument("--authorized", action="store_true")
    args = parser.parse_args()

    event = {
        "timestamp": int(time.time() * 1000),
        "person_id": args.person_id,
        "person_name": NAMES.get(args.person_id, "desconocido"),
        "confidence": args.confidence,
        "authorized": bool(args.authorized),
    }
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(args.broker, args.port)
    client.publish(args.topic, json.dumps(event)).wait_for_publish()
    print(f"[test] Publicado en {args.topic}: {json.dumps(event)}")
    client.disconnect()

if __name__ == "__main__":
    main()
