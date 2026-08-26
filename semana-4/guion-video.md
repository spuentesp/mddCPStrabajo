# Guion del video — Semana 4 (duración objetivo: 6–7 minutos)

> Requisitos: exposición realizada directamente por el estudiante, mostrando de
> forma continua su participación; evidenciar comprensión del proceso MDD4CPS,
> las transformaciones realizadas y las decisiones de diseño incorporadas.
> Compartir pantalla con: diagrams.net (CIM y PIM abiertos en la vista
> correspondiente), el código en el editor y la herramienta oficial
> `aomdd4cps` corriendo en Docker.
>
> **Enfoque del video:** apliqué el proceso MDD4CPS con un **agente** que
> razonó las transformaciones y completó la fase Code con código ESP32
> verificado. Después apliqué también la herramienta oficial sobre el mismo
> CIM para contrastar los artefactos. El video narra ambas cosas y no
> atribuye a la herramienta artefactos que produjo el agente.

## Escena 1 — Introducción y caso de estudio (0:00–0:45)

«Hola. En este video aplico el proceso MDD4CPS a **SVIF**, un sistema
ciberfísico de videovigilancia con identificación facial. SVIF tiene dos nodos:
un **Face Monitor** con cámara ESP32-CAM que detecta e identifica rostros, y
un **Access Actuator** que desbloquea una cerradura o activa una alarma.
Recorreré la cadena completa —del modelo orientado a agentes al código— y al
final contrastaré lo que produce una herramienta que implementa el mismo
proceso.»

## Escena 2 — SVIF y el CIM (0:45–1:45)

*(Mostrar `cim-istar-svif.drawio`, **página 2 — vista híbrida SD/SR**: ambos
agentes en un mismo diagrama.)*

«Este es el CIM en iStar 2.0. Cada nodo es un **agente** con su límite. El
objetivo *Monitorear presencia de personas* se refina en cuatro tareas; noten
el refinamiento **OR** en el actuador —desbloquear o alarmar— y los
**softgoals**: privacidad de datos personales, oportunidad y trazabilidad. La
dependencia central es el recurso *"Evento de identificación"*: el actuador
depende del monitor para obtenerlo.»

## Escena 3 — Transformación CIM → PIM (1:45–3:00)

*(Mostrar el PIM en diagrams.net, `pim-dsl-svif.drawio`.)*

«Apliqué la transformación siguiendo las reglas del proceso: los agentes se
convierten en **CP Components**, los objetivos en **On Interval Actions**, las
tareas en **On Demand Actions**, y la dependencia en un par
**MessageSender / MessageReceiver**. La trazabilidad se preserva con
`id_cim_parent`.

Aquí incorporo la información que el CIM no contiene: el **período** de
monitoreo —500 ms— y de control —250 ms—, los **parámetros de entrada y
salida** de cada acción, y la **estructura del dependum**: timestamp,
person_id, person_name, confidence y authorized. Una decisión deliberada:
**no guardamos imágenes, sino una firma a partir del rostro** — el dependum
transmite sólo identidad y metadatos. Todo esto sigue siendo independiente de
plataforma. Un punto que voy a confirmar al final: el refinamiento **OR** lo
preservé en el código, no es algo que la herramienta materialice.»

## Escena 4 — Materialización PIM → PSM (3:00–3:45)

*(Mostrar el código ESP32 generado en el editor: `.ino`, structs, hilos.)*

«Ahora fijo la tecnología: **ESP32** con Arduino core y **MQTT**. La
realización del PSM queda así:

- Cada CP Component es una **unidad de despliegue**: un `.ino`, un
  `comm_utils.h` y un `secrets.h`.
- La On Interval Action es un **hilo FreeRTOS** con
  `vTaskDelay(pdMS_TO_TICKS(500))` — el período viene del modelo.
- Cada On Demand Action es una **función** con su bloque de trazabilidad.
- El sender y el receiver comparten la struct del dependum.
- El refinamiento **OR** aparece como el condicional de
  `gestionarRespuestaAcceso`.»

## Escena 5 — Completado manual y verificación (3:45–4:30)

«En la fase Code completé lo que ningún modelo deduce: credenciales, umbral de
confianza, política de autorización y la simulación de cámara
(`SIMULATION_MODE`).

*(Mostrar, si es posible, una corrida en modo simulación con el monitor MQTT.)*

Con `SIMULATION_MODE` el flujo corre sin hardware contra Mosquitto: el monitor
publica un evento y el actuador decide entre desbloquear o alarmar,
registrándolo en la bitácora. En la corrida hubo **14 eventos: 10 desbloqueos y
4 alarmas**. Un hallazgo: con la regla inicial la **rama de alarma no se
ejercitaba**, así que ajusté la política para cubrir **ambas ramas del OR**
como criterio de aceptación.»

## Escena 6 — Aplicación de la herramienta aomdd4cps (4:30–5:45)

*(Mostrar `aomdd4cps` corriendo en Docker y los artefactos en
`comparativa-app/`.)*

«Para no quedarme sólo en el recorrido narrado, apliqué también la
**herramienta oficial `aomdd4cps`** sobre el mismo CIM. Primero reproduje su
caso de ejemplo, el invernadero: la herramienta regenera su PIM y su PSM
**idénticos** a los del repositorio, así que el entorno es fiel. Sobre SVIF
encontré tres cosas:

1. **CIM → PIM**: reproduce fielmente componentes, metas, acciones, recursos y
   comunicación… pero **descarta los operadores AND/OR**. Esto confirma que el
   OR lo preservé yo.
2. **PIM → PSM**: es la fase más sólida — genera un modelo completo con los
   dos componentes, las funciones, los hilos con su período y el buzón del
   dependum.
3. **PSM → Code**: genera 622 líneas, pero apunta a **Arduino MKR 1010, no
   ESP32**, emite sintaxis inválida como `char[32] person_id;` y deja la
   lógica en *stubs*: **no compila** tal cual.»

## Escena 7 — Análisis del código generado y cierre (5:45–6:45)

«Para estimar cuánto código generó la transformación, conté las líneas del
`.ino` y de `comm_utils.h`, y resté lo que completé a mano en la fase Code.
Sobre 627 líneas totales, ~135 son personalizadas — eso da el **~78 %** que
reporta el paper para el caso del invernadero. Pero esa cifra **mide el
volumen de andamiaje** —hilos, funciones, structs, comunicación y
trazabilidad—, no el código funcional: en la herramienta todo ese andamiaje
queda en *stubs*, y en el agente quedó implementado.

*(Mostrar la tabla de la comparativa al final.)*

La **herramienta** gana en rigor, reproducibilidad y homogeneidad del
andamiaje. El **agente** gana en corrección, plataforma correcta, semántica
del OR y cobertura de la fase Code. No son intercambiables: cada vía aporta
lo que la otra no entrega en su estado actual.

Eso es todo. La encuesta de la experiencia de modelado la dejo en la
descripción. Gracias.»

---

## Cronograma total

| Escena | Tema | Duración |
|---|---|---|
| 1 | Introducción y caso | 0:00–0:45 |
| 2 | SVIF y el CIM | 0:45–1:45 |
| 3 | CIM → PIM | 1:45–3:00 |
| 4 | Materialización PIM → PSM | 3:00–3:45 |
| 5 | Completado manual y verificación | 3:45–4:30 |
| 6 | Aplicación de la herramienta aomdd4cps | 4:30–5:45 |
| 7 | Análisis del código generado y cierre | 5:45–6:45 |
| **Total** | | **≈ 6:45** |