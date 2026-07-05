# Guion del video — Semana 4 (duración objetivo: 6 minutos)

> Requisitos: exposición realizada directamente por el estudiante, mostrando de
> forma continua su participación; evidenciar comprensión del proceso MDD4CPS,
> las transformaciones realizadas y las decisiones de diseño incorporadas.
> Compartir pantalla con: diagrams.net (CIM y PIM), la herramienta web de
> transformación y el código en el editor.

## Escena 1 — Introducción y caso de estudio (0:00–0:45)

«Hola, soy [nombre]. En este video aplico el proceso MDD4CPS a **SVIF**, un sistema
ciberfísico de videovigilancia con identificación facial compuesto por dos nodos:
un **Face Monitor** con cámara ESP32-CAM que detecta e identifica rostros, y un
**Access Actuator** que desbloquea la cerradura o activa la alarma. Recorreré la
cadena completa: del modelo orientado a agentes al código Arduino.»

## Escena 2 — CIM: el modelo iStar de la semana anterior (0:45–1:45)

*(Mostrar `cim-istar-svif.drawio`, vista SD/SR.)*

«Este es el CIM en iStar 2.0. Cada nodo es un **agente** con su límite. El objetivo
"Monitorear presencia de personas" se refina en cuatro tareas; noten el
refinamiento **OR** en el actuador —desbloquear o alarmar— y los **softgoals**:
privacidad de datos personales, oportunidad e trazabilidad. La dependencia central
es el recurso **"Evento de identificación"**: el actuador depende del monitor para
obtenerlo.»

## Escena 3 — Transformación CIM → PIM (1:45–3:00)

*(Mostrar la herramienta web en modo CIM→PIM: cargar XML, Apply Rules, Transform;
luego el PIM en diagrams.net.)*

«La transformación identifica automáticamente las correspondencias: los agentes se
convierten en **CP Components**, los objetivos en **On Interval Actions**, las
tareas en **On Demand Actions**, y la dependencia en un par
**MessageSender/MessageReceiver**. La trazabilidad se preserva con
`id_cim_parent`.

Aquí incorporo la información que el CIM no contiene y que la herramienta me
solicita: el **período** de monitoreo —500 milisegundos— y de control de acceso
—250 milisegundos—, los **parámetros de entrada y salida** de cada acción, y la
**estructura del dependum**: timestamp, person_id, person_name, confidence y
authorized. Es una decisión deliberada de privacidad: se transmite la identidad,
nunca la imagen. Todo esto sigue siendo independiente de plataforma.»

## Escena 4 — Transformación PIM → PSM (3:00–4:30)

*(Mostrar modo PIM→PSM: elegir plataforma Arduino y tecnología MQTT; abrir el
código generado.)*

«Ahora sí elijo tecnología: **Arduino/ESP32** y **MQTT**. Observemos la
correspondencia en el código generado:

- Cada CP Component es una **unidad de despliegue**: un `.ino`, un `comm_utils.h`
  y un `secrets.h` manual.
- La On Interval Action se volvió un **hilo FreeRTOS** con
  `vTaskDelay(pdMS_TO_TICKS(500))` — el período viene del modelo.
- Cada On Demand Action es una **función** con su bloque de trazabilidad:
  Function ID, Parent ID, origen CIM, parámetros y los softgoals afectados.
- El sender y el receiver comparten la **struct del dependum** y la lógica MQTT.
- El refinamiento **OR** del CIM aparece como el condicional de
  `gestionarRespuestaAcceso`.
- Los recursos de software son **structs tipadas**, y los de hardware,
  **comentarios de integración** con sus pines.»

## Escena 5 — Fase Code y demostración (4:30–5:30)

*(Mostrar `secrets.h`, el umbral de confianza y, si es posible, una corrida en
modo simulación con el monitor MQTT.)*

«En la fase Code completé lo que ningún modelo puede deducir: credenciales,
umbral de confianza, política de autorización y la simulación de cámara. Con
`SIMULATION_MODE` el flujo completo corre sin hardware: el monitor publica un
evento y el actuador decide entre desbloquear o alarmar, registrándolo en la
bitácora.»

## Escena 6 — Análisis crítico y cierre (5:30–6:00)

«Del total de la implementación, aproximadamente un **78 % fue generado** y el
resto es personalización. Lo más valioso: la **trazabilidad** —puedo seguir el
softgoal de privacidad desde iStar hasta un comentario en la función de
comparación—. Las limitaciones: los softgoals llegan al código solo como
comentarios, el criterio del OR debe reintroducirse a mano y el DSL aún no expresa
restricciones temporales duras; además, la herramienta es una versión alfa, por lo
que algunos ajustes se hicieron editando el modelo en diagrams.net. Completé la
encuesta de la experiencia de modelado. Muchas gracias.»
