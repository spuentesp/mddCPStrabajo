#!/usr/bin/env python3
"""Monitor del topico del dependum "Evento de identificacion" (SVIF).

Uso:
    python3 monitor_mqtt.py --broker localhost [--topic svif/eventos/identificacion]

Requiere: pip install paho-mqtt
"""
import argparse
import json

import paho.mqtt.client as mqtt

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--broker", default="localhost")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--topic", default="svif/eventos/identificacion")
    args = parser.parse_args()

    def on_connect(client, userdata, flags, reason_code, properties=None):
        print(f"[monitor] Conectado a {args.broker}:{args.port}, suscrito a {args.topic}")
        client.subscribe(args.topic)

    def on_message(client, userdata, msg):
        try:
            event = json.loads(msg.payload.decode())
            estado = "AUTORIZADO" if event.get("authorized") else "NO AUTORIZADO"
            print(f"[{msg.topic}] {estado} :: person_id={event.get('person_id')} "
                  f"({event.get('person_name')}) conf={event.get('confidence')}")
        except json.JSONDecodeError:
            print(f"[{msg.topic}] payload no JSON: {msg.payload!r}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(args.broker, args.port)
    client.loop_forever()

if __name__ == "__main__":
    main()
