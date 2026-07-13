# 🚀 SVIF Simulation Runner — Demo One-Shot

Scripts para ejecutar la simulación completa del sistema SVIF (Face Monitor + Access Actuator) en modo Python, con soporte automático de broker MQTT.

## Quick Start

### Script Python (recomendado)

```bash
cd /home/sebastian/mddCPStrabajo/semana-4
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

```bash
$ python3 run_simulation.py --duracion 8 --semilla 7
============================================================
🔬 SVIF Simulation Runner — MDD4CPS Semana 4
============================================================
🚀 Iniciando broker MQTT en localhost:1883...
✓ Broker MQTT iniciado

📊 Ejecutando simulación (8s, semilla=7)...

[FaceMonitor ] capturarImagen: frame=0.22
[FaceMonitor ] detectarRostro: frame=0.22 → TRUE (< 0.30)
[FaceMonitor ] identificarRostro: 0.22 → Ana Perez (person_id=1, authorized=true)
[FaceMonitor ] >>> Publicando evento a svif/eventos/identificacion

[AccessActuator] Recibió evento: {person_id: 1, person_name: 'Ana Perez', ...}
[AccessActuator] evaluar_autorizacion: authorized=true → GRANTED
[AccessActuator] >>> RELE ON: cerradura DESBLOQUEADA 5 s
[AccessActuator] >>> Registrando en bitacora

... (continúa con más detecciones)

[FaceMonitor ] capturarImagen: frame=0.85
[FaceMonitor ] detectarRostro: frame=0.85 → TRUE (> 0.70)
[FaceMonitor ] identificarRostro: 0.85 → Visita Roja (person_id=3, authorized=false)
[AccessActuator] evaluar_autorizacion: authorized=false → DENIED
[AccessActuator] >>> BUZZER ON: ALARMA activada 3 s

=== Resumen de la bitacora de accesos ===
Eventos registrados: 15 (desbloqueos: 8, alarmas: 7)

✅ Simulación completada exitosamente

🧹 Limpiando recursos...
```

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
