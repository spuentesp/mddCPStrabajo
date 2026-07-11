# Guion del video — Semana 4 (duración objetivo: 6–7 minutos)

> Requisitos: exposición realizada directamente por el estudiante, mostrando de
> forma continua su participación; evidenciar comprensión del proceso MDD4CPS,
> las transformaciones realizadas y las decisiones de diseño incorporadas.
> Compartir pantalla con: diagrams.net (CIM y PIM), el código en el editor y la
> herramienta oficial `aomdd4cps` corriendo en Docker (validación).
>
> **Enfoque honesto:** apliqué el proceso MDD4CPS **con un agente** (razonando las
> transformaciones y completando la fase Code con código ESP32 verificado) y luego
> lo **validé empíricamente ejecutando la herramienta oficial** sobre el mismo CIM.
> El video narra ambas cosas y no atribuye a la herramienta artefactos que produjo
> el agente.

## Escena 1 — Introducción y caso de estudio (0:00–0:45)

«Hola, soy [nombre]. En este video aplico el proceso MDD4CPS a **SVIF**, un sistema
ciberfísico de videovigilancia con identificación facial compuesto por dos nodos:
un **Face Monitor** con cámara ESP32-CAM que detecta e identifica rostros, y un
**Access Actuator** que desbloquea la cerradura o activa la alarma. Recorreré la
cadena completa —del modelo orientado a agentes al código— y, al final, **validaré
el proceso corriendo la herramienta oficial** para contrastar lo que genera.»

## Escena 2 — CIM: el modelo iStar de la semana anterior (0:45–1:45)

*(Mostrar `cim-istar-svif.drawio`, vista SD/SR.)*

«Este es el CIM en iStar 2.0. Cada nodo es un **agente** con su límite. El objetivo
"Monitorear presencia de personas" se refina en cuatro tareas; noten el
refinamiento **OR** en el actuador —desbloquear o alarmar— y los **softgoals**:
privacidad de datos personales, oportunidad y trazabilidad. La dependencia central
es el recurso **"Evento de identificación"**: el actuador depende del monitor para
obtenerlo.»

## Escena 3 — Transformación CIM → PIM (1:45–3:00)

*(Mostrar el PIM resultante en diagrams.net, `pim-dsl-svif.drawio`.)*

«Apliqué la transformación siguiendo las reglas del proceso: los agentes se
convierten en **CP Components**, los objetivos en **On Interval Actions**, las
tareas en **On Demand Actions**, y la dependencia en un par
**MessageSender/MessageReceiver**. La trazabilidad se preserva con `id_cim_parent`.

Aquí incorporo la información que el CIM no contiene: el **período** de monitoreo
—500 milisegundos— y de control de acceso —250 milisegundos—, los **parámetros de
entrada y salida** de cada acción, y la **estructura del dependum**: timestamp,
person_id, person_name, confidence y authorized. Es una decisión deliberada de
privacidad: se transmite la identidad, nunca la imagen. Todo esto sigue siendo
independiente de plataforma. Adelanto un punto que confirmaré al final: el
refinamiento **OR** lo preservé yo en el modelo, no es algo que la herramienta
materialice.»

## Escena 4 — Transformación PIM → PSM y fase Code (3:00–4:15)

*(Mostrar el código ESP32 generado en el editor: `.ino`, structs, hilos.)*

«Ahora fijo la tecnología: **ESP32** con Arduino core y **MQTT**. Esta es mi
realización de referencia del PSM:

- Cada CP Component es una **unidad de despliegue**: un `.ino`, un `comm_utils.h`
  y un `secrets.h`.
- La On Interval Action es un **hilo FreeRTOS** con
  `vTaskDelay(pdMS_TO_TICKS(500))` — el período viene del modelo.
- Cada On Demand Action es una **función** con su bloque de trazabilidad:
  origen CIM, parámetros y los softgoals afectados.
- El sender y el receiver comparten la **struct del dependum** y la lógica MQTT.
- El refinamiento **OR** aparece como el condicional de `gestionarRespuestaAcceso`.
- En la fase Code completé lo que ningún modelo deduce: credenciales, umbral de
  confianza, política de autorización y la simulación de cámara (`SIMULATION_MODE`).»

## Escena 5 — Verificación de punta a punta (4:15–5:00)

*(Mostrar, si es posible, una corrida en modo simulación con el monitor MQTT.)*

«Con `SIMULATION_MODE` el flujo completo corre sin hardware contra Mosquitto: el
monitor publica un evento y el actuador decide entre desbloquear o alarmar,
registrándolo en la bitácora. En la corrida hubo **14 eventos: 10 desbloqueos y 4
alarmas**. Un hallazgo importante: con la regla inicial la **rama de alarma no se
ejercitaba**, así que ajusté la política para cubrir **ambas ramas del OR** como
criterio de aceptación.»

## Escena 6 — Validación con la herramienta oficial (5:00–6:15)

*(Mostrar `aomdd4cps` corriendo en Docker y los artefactos en `comparativa-app/`.)*

«Para no quedarme en un recorrido narrado, **ejecuté la herramienta oficial
`aomdd4cps`** sobre el mismo CIM. Primero reproduje su caso de ejemplo, el
invernadero: la herramienta regenera su PIM y su PSM **idénticos** a los del
repositorio, así que el entorno es fiel. Sobre SVIF encontré tres cosas:

1. **CIM→PIM**: reproduce fielmente componentes, metas, acciones, recursos y
   comunicación… pero **descarta los operadores AND/OR**. Esto confirma que el OR
   lo tuve que preservar yo.
2. **PIM→PSM**: es la fase más sólida —genera un modelo completo con los dos
   componentes, las funciones, los hilos con su período y el buzón del dependum.
3. **PSM→Code**: genera 622 líneas, pero apunta a **Arduino MKR 1010, no ESP32**,
   emite sintaxis inválida como `char[32] person_id;` y deja la lógica en *stubs*:
   **no compila** tal cual.»

## Escena 7 — Análisis crítico y cierre (6:15–7:00)

«La conclusión es matizada. Ese **~78 % "generado"** mide el volumen de
**andamiaje** —hilos, structs, comunicación, trazabilidad—, que es justo lo más
propenso a error a mano; pero no es código funcional. La **herramienta** gana en
determinismo, reproducibilidad y homogeneidad; el **agente** gana en corrección,
plataforma correcta, semántica del OR y cobertura de la fase Code. No son
sustitutos: lo ideal es usar la herramienta para el andamiaje determinista y un
agente para completar lo que el DSL aún no expresa. Completé la encuesta de la
experiencia de modelado. Muchas gracias.»
