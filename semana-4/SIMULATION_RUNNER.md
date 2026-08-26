# 🚀 SVIF Simulation Runner — Demo One-Shot

Scripts para ejecutar la simulación completa del sistema SVIF (Face Monitor + Access Actuator) en modo Python, con soporte automático de broker MQTT.

## Quick Start

### Script Python (recomendado)

```bash
cd mddCPStrabajo/semana-4
python3 run_simulation.py
```

**Opciones:**
```bash
# Duración personalizada (segundos)
python3 run_simulation.py --duracion 20

# Reproducible (misma semilla = mismos eventos)
python3 run_simulation.py --semilla 42

# Sin Docker (broker manual en localhost:1883)
python3 run_simulation.py --no-docker

# Combinado
python3 run_simulation.py --duracion 15 --semilla 99
```

## Requisitos

- **Python 3.8+**
- **Docker** (opcional; si no lo tienes, inicia broker manualmente)

### Si NO tienes Docker

Inicia el broker en otra terminal **antes** de ejecutar:

```bash
docker run -it --rm -p 1883:1883 eclipse-mosquitto:2 \
  mosquitto -c /mosquitto-no-auth.conf
```

Luego:
```bash
python3 run_simulation.py --no-docker
```

## ¿Qué hace?

1. **Inicia broker MQTT automáticamente** (con Docker si está disponible)
2. **Ejecuta ambos componentes** en Python:
   - `FaceMonitorComponent`: captura → detecta → identifica rostros
   - `AccessActuatorComponent`: evalúa autorización → actúa (desbloqueo/alarma)
3. **Intercambia eventos MQTT** entre componentes (como en el sistema real)
4. **Limpia recursos** al finalizar

## Ejemplo de ejecución

Salida real, capturada ejecutando `python3 run_simulation.py --duracion 8
--semilla 7 --no-docker` contra un broker Mosquitto local (reproducida dos
veces con resultado idéntico):

```text
============================================================
🔬 SVIF Simulation Runner — MDD4CPS Semana 4
============================================================
🔍 Verificando paho-mqtt...
✓  paho-mqtt está instalado
ℹ️  Modo manual: asumiendo broker en localhost:1883
✓  Broker disponible (intento 1, 0.0s)
🔍 Comando: python3 .../simular_sistema.py --broker localhost --port 1883 --duracion 8 --semilla 7

=== SVIF: gemelo de simulacion (8 s) ===
[FaceMonitor ] deteccion -> publica {'person_id': 1, 'person_name': 'Ana Perez', 'confidence': 0.96, 'authorized': True}
[AccessActuator] >>> RELE ON: cerradura DESBLOQUEADA 5 s (luego retorna a estado seguro)
[AccessActuator] bitacora #1: {'person_id': 1, 'action_taken': 'desbloqueo', 'confidence': 0.96}
... (continúa con más detecciones — 6 desbloqueos seguidos de Ana Perez)
[FaceMonitor ] deteccion -> publica {'person_id': 3, 'person_name': 'Visita Roja', 'confidence': 1.0, 'authorized': False}
[AccessActuator] >>> BUZZER ON: ALARMA activada 3 s
[AccessActuator] bitacora #7: {'person_id': 3, 'action_taken': 'alarma', 'confidence': 1.0}
[FaceMonitor ] deteccion -> publica {'person_id': 1, 'person_name': 'Ana Perez', 'confidence': 0.99, 'authorized': True}
[AccessActuator] >>> RELE ON: cerradura DESBLOQUEADA 5 s (luego retorna a estado seguro)
[AccessActuator] bitacora #8: {'person_id': 1, 'action_taken': 'desbloqueo', 'confidence': 0.99}
[FaceMonitor ] deteccion -> publica {'person_id': 1, 'person_name': 'Ana Perez', 'confidence': 0.89, 'authorized': True}
[AccessActuator] >>> RELE ON: cerradura DESBLOQUEADA 5 s (luego retorna a estado seguro)
[AccessActuator] bitacora #9: {'person_id': 1, 'action_taken': 'desbloqueo', 'confidence': 0.89}

=== Resumen de la bitacora de accesos ===
Eventos registrados: 9 (desbloqueos: 8, alarmas: 1)
✓  Simulación completada sin errores

✅ Simulación completada EXITOSAMENTE
```

> Con solo 8 segundos de duración la rama de alarma se ejercita una sola vez.
> `evidencia-de-pruebas.md` usa una corrida más larga (12 s, misma semilla 7)
> que ejercita ambas ramas con más margen: 14 eventos (10 desbloqueos, 4
> alarmas). Esa es la corrida de referencia para la actividad.

## Características

✅ **One-shot**: ejecuta y termina automáticamente  
✅ **Broker automático**: inicia Docker si lo tiene, o usa uno existente  
✅ **Reproducible**: usa `--semilla N` para repetir exactamente los mismos eventos  
✅ **Traza el flujo completo**: detección → identificación → publicación → evaluación → actuación  
✅ **Ejercita ambas ramas del OR**: desbloqueos (autorizados) y alarmas (no autorizados)

## Estructura

- `run_simulation.py` — Script principal con manejo de broker
- `codigo/` — Código Arduino (FaceMonitorComponent, AccessActuatorComponent)
- `../recursos-comunes/herramientas/simular_sistema.py` — Gemelo Python que replica el PSM
