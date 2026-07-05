# Código SVIF — Fases PSM y Code del proceso MDD4CPS

Cada carpeta corresponde a la **unidad de despliegue** de un componente
ciberfísico (`CPComponent` del modelo PIM), siguiendo la convención de archivos
del proceso MDD4CPS:

| Archivo | Rol | ¿Generado? |
|---|---|---|
| `<CPC>.ino` | Punto de entrada: inicializa WiFi/MQTT/hardware, crea los hilos y mantiene `loop()` | PSM (estructura generada) |
| `comm_utils.h` | Publicación/suscripción MQTT, serialización del *dependum*, estructuras de mensaje | PSM (generado desde el PIM) |
| `secrets.h` | Credenciales y parámetros sensibles (SSID, broker) | **Manual** (fase Code; usar `secrets.h.example`) |

## Correspondencia PIM → PSM

| Constructo PIM | Elemento de código |
|---|---|
| `CPComponent` | Carpeta/sketch Arduino (unidad de despliegue) |
| `OnIntervalAction` | Hilo FreeRTOS periódico (`xTaskCreatePinnedToCore` + `vTaskDelay` con el `interval_in_milliseconds` del modelo) |
| `OnDemandAction` | Función C++ invocable, con trazabilidad en comentarios |
| `MessageSender` / `MessageReceiver` | Hilos/callbacks de comunicación MQTT que comparten la estructura del *dependum* |
| `SWResource` | `struct` tipada (p. ej., `EnrolledFace`, `AccessLogEntry`) |
| `HWResource` | Comentario estructurado + pin de integración (fase Code) |
| Softgoals (qualification/contribution) | Comentarios de trazabilidad en las funciones afectadas |
| Refinamiento OR del CIM | Estructura condicional en `gestionarRespuestaAcceso()` |

## Cómo probar sin hardware

1. **Broker MQTT local** (requiere Docker o Mosquitto instalado):

   ```bash
   docker run -it --rm -p 1883:1883 eclipse-mosquitto:2 mosquitto -c /mosquitto-no-auth.conf
   ```

2. **Observar el tópico** del *dependum*:

   ```bash
   python3 ../recursos-comunes/herramientas/monitor_mqtt.py --broker localhost
   ```

3. **Inyectar un evento de prueba** (sustituye al Face Monitor para probar el
   actuador de forma aislada):

   ```bash
   python3 ../recursos-comunes/herramientas/publicar_evento_prueba.py --broker localhost --person-id 1 --authorized
   ```

4. **Simulación completa del sistema** (gemelo en Python de ambos CPC, con los
   mismos períodos y estructura del *dependum* que el PSM; ejercita las dos
   ramas del OR — desbloqueo y alarma):

   ```bash
   python3 ../recursos-comunes/herramientas/simular_sistema.py --broker localhost --duracion 12 --semilla 7
   ```

   La evidencia de una corrida real está en
   [`../evidencia-de-pruebas.md`](../evidencia-de-pruebas.md).

5. **Nodos ESP32**: compilar con Arduino IDE (core ESP32 + librería
   `PubSubClient`), copiando antes `secrets.h.example` → `secrets.h`. El
   `FaceMonitorComponent` compila por defecto con `SIMULATION_MODE`, que genera
   detecciones sintéticas sin cámara; también puede simularse el circuito completo
   en [Wokwi](https://wokwi.com) (ESP32 + relé + buzzer).

## Flujo esperado (modo simulación)

```
FaceMonitor: capturarImagen -> detectarRostro -> identificarRostro
             -> publish svif/eventos/identificacion
AccessActuator: receiver -> evaluarAutorizacion
             -> desbloquearCerradura | activarAlarma -> registrarEventoAcceso
```
