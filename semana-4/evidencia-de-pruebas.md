# Evidencia de verificación de SVIF (ejecución de punta a punta)

Este documento registra la verificación funcional del sistema desarrollado,
realizada sin hardware mediante el **gemelo de simulación**
(`recursos-comunes/herramientas/simular_sistema.py`), que replica en Python la lógica del PSM
(mismos períodos —monitoreo 500 ms, control 250 ms—, misma estructura del
*dependum* y misma lógica del refinamiento OR) contra un broker **Mosquitto**
local. Esta estrategia responde directamente al desafío de *verification
problem* identificado en la Semana 1.

## 1. Entorno de prueba

| Elemento | Valor |
|---|---|
| Broker MQTT | Eclipse Mosquitto 2.x, `localhost:1883` |
| Cliente | paho-mqtt (Python 3) |
| Tópico del *dependum* | `svif/eventos/identificacion` |
| Duración de la corrida | 12 s (semilla aleatoria fija: 7, reproducible) |

## 2. Escenarios cubiertos

| # | Escenario | Rama del OR (CIM: cim-t7) | Resultado |
|---|---|---|---|
| 1 | Rostro enrolado y **autorizado** (Ana Pérez) | cim-t8: Desbloquear cerradura | Relé ON 5 s y retorno al estado seguro ✔ |
| 2 | Rostro enrolado y **no autorizado** (Visita Roja) | cim-t9: Activar alarma | Buzzer ON 3 s ✔ |
| 3 | Registro en bitácora de **cada** evento | cim-t10 | 14/14 eventos registrados ✔ |
| 4 | Herramientas auxiliares (monitor e inyector) | — | Recepción y decodificación correctas ✔ |

## 3. Extracto de la salida real de la corrida

```text
=== SVIF: gemelo de simulacion (12 s) ===
[FaceMonitor ] deteccion -> publica {'timestamp': 1783268298056, 'person_id': 1,
               'person_name': 'Ana Perez', 'confidence': 0.98, 'authorized': True}
[AccessActuator] >>> RELE ON: cerradura DESBLOQUEADA 5 s (luego retorna a estado seguro)
[AccessActuator] bitacora #6: {'timestamp': 1783268298056, 'person_id': 1,
               'action_taken': 'desbloqueo', 'confidence': 0.98}
[FaceMonitor ] deteccion -> publica {'timestamp': 1783268299057, 'person_id': 3,
               'person_name': 'Visita Roja', 'confidence': 1.0, 'authorized': False}
[AccessActuator] >>> BUZZER ON: ALARMA activada 3 s
[AccessActuator] bitacora #7: {'timestamp': 1783268299057, 'person_id': 3,
               'action_taken': 'alarma', 'confidence': 1.0}
...
=== Resumen de la bitacora de accesos ===
Eventos registrados: 14 (desbloqueos: 10, alarmas: 4)
```

Verificación de las herramientas auxiliares:

```text
[monitor] Conectado a localhost:1883, suscrito a svif/eventos/identificacion
[svif/eventos/identificacion] AUTORIZADO :: person_id=1 (Ana Perez) conf=0.92
[svif/eventos/identificacion] NO AUTORIZADO :: person_id=-1 (desconocido) conf=0.92
```

## 4. Cómo reproducir

```bash
# 1) Broker local
mosquitto -p 1883 -d           # o: docker run -p 1883:1883 eclipse-mosquitto:2 ...

# 2) Dependencias
pip install paho-mqtt

# 3) Simulación completa (reproducible con la misma semilla)
python3 recursos-comunes/herramientas/simular_sistema.py --broker localhost --duracion 12 --semilla 7

# 4) (Opcional) observar el tópico y/o inyectar eventos manualmente
python3 recursos-comunes/herramientas/monitor_mqtt.py --broker localhost
python3 recursos-comunes/herramientas/publicar_evento_prueba.py --broker localhost --person-id 1 --authorized
```

## 5. Hallazgo de verificación (y corrección aplicada)

Durante la primera corrida se detectó que la regla sintética de detección
(`frame < 0.30`) solo generaba rostros próximos al enrolado autorizado, por lo
que la rama **cim-t9 (Activar alarma)** del refinamiento OR **nunca se
ejercitaba**. Se corrigió la regla (`frame < 0.30 || frame > 0.70`) tanto en el
gemelo de simulación como en `FaceMonitorComponent.ino`, de modo que la
población sintética incluya rostros no autorizados. Este hallazgo ilustra el
valor de ejecutar el sistema de punta a punta y no limitarse a la revisión
estática del código: la cobertura de las ramas del modelo (OR del CIM) es un
criterio de aceptación verificable.
