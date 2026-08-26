# Actividad Semana 4 — Desarrollo de SVIF mediante el proceso MDD4CPS

**Objetivo:** aplicar el proceso MDD4CPS para transformar el modelo orientado a
agentes de SVIF (Semana 3) en una implementación específica de plataforma,
analizando cómo las decisiones de diseño se incorporan progresivamente.

**Entregables:**

| Entregable | Ubicación |
|---|---|
| Modelo CIM (`.drawio`) | `cim-istar-svif.drawio` (en esta carpeta) |
| Modelo PIM/DSL (`.drawio`) | `pim-dsl-svif.drawio` (en esta carpeta) |
| Código fuente generado | `codigo/` (en esta carpeta) |
| Presentación y video (5–7 min) | guion en `guion-video.md` |
| Encuesta de la experiencia | https://forms.gle/VPaL9qx7mhKttJgf8 (completar tras la actividad) |

---

## 1. Aplicación del proceso

### 1.1 Transformación CIM → PIM

A partir del modelo iStar 2.0, se derivó el modelo PIM en el DSL para CPS. Las
correspondencias identificadas automáticamente por las reglas de transformación
fueron:

| Constructo CIM (iStar) | Constructo PIM (DSL) | Instancias en SVIF |
|---|---|---|
| *Agent* | `CPComponent` | cim-a1 → pim-fm-00; cim-a2 → pim-aa-00 |
| *Goal* | `OnIntervalAction` | cim-g1 → pim-fm-01; cim-g2 → pim-aa-01 |
| *Task* | `OnDemandAction` | cim-t1..t4, t6..t10 → pim-fm-02..05, pim-aa-02..06 |
| *Resource* (SW) | `SWResource` | cim-r2 → pim-fm-06; cim-r5 → pim-aa-09 |
| *Resource* (HW) | `HWResource` | cim-r1 → pim-fm-07; cim-r3/r4 → pim-aa-07/08 |
| *Dependency* (dependum cim-d1) | `MessageSender` + `MessageReceiver` | pim-fm-08 y pim-aa-10 |
| Refinamientos AND/OR | Operadores `AND`/`OR` | pim-fm-a1, pim-aa-a1, pim-aa-o1 |
| *Quality* (softgoals) | `qualification_array` / `contribution_array` en los elementos afectados | cim-q1..q4 propagados |

**Información incorporada por el diseñador en esta etapa** (no deducible del CIM,
pero aún independiente de tecnología):

| Elemento | Decisión de diseño |
|---|---|
| `pim-fm-01` | `interval_in_milliseconds = 500` (percepción 2 veces por segundo) |
| `pim-aa-01` | `interval_in_milliseconds = 250` (la actuación debe ser más reactiva que la percepción) |
| `pim-fm-08` / `pim-aa-10` | Estructura del *dependum*: `timestamp`, `person_id`, `person_name`, `confidence`, `authorized` (minimización de datos: se transmite la identidad, nunca la imagen) |
| `OnDemandActions` | Parámetros de entrada/salida (p. ej., `identificarRostro`: entrada `frame`, salida `identification_event`) |
| `pim-fm-06` / `pim-aa-09` | Campos de las estructuras de datos (`data_structure`) de la base de enrolados y la bitácora |

### 1.2 Transformación PIM → PSM

Se materializó el PIM sobre la plataforma **ESP32 (Arduino core)** con
comunicación **MQTT**, decisión tomada durante esta transformación. Aunque adopta
la forma de código fuente, el PSM sigue siendo un modelo: quedan abiertos aspectos
que se completan en la fase Code.

| Constructo PIM | Elemento PSM generado | Evidencia en el código |
|---|---|---|
| `CPComponent` | Unidad de despliegue: `<CPC>.ino` + `comm_utils.h` + `secrets.h` | Carpetas `FaceMonitorComponent/`, `AccessActuatorComponent/` |
| `OnIntervalAction` | **Hilo periódico FreeRTOS** con el período del modelo | `monitorearPresenciaDePersonasTask` (500 ms), `controlarAccesoAlRecintoTask` (250 ms) |
| `OnDemandAction` | **Función ejecutable** con firma derivada de los parámetros del PIM | `capturarImagen()`, `identificarRostro()`, `evaluarAutorizacion()`, … |
| `MessageSender` | **Hilo de comunicación** que publica el *dependum* serializado | `eventoIdentificacionSenderTask` + `publishIdentificationEvent()` |
| `MessageReceiver` | **Callback/hilo receptor** que deserializa y deja disponible el *dependum* | `eventoIdentificacionReceiverCallback` + `deserializeIdentificationEvent()` |
| `SWResource` | **`struct` tipada** (tipos concretos asignados en esta etapa) | `EnrolledFace`, `AccessLogEntry`, `IdentificationEvent` |
| `HWResource` | **Comentario estructurado** + marca de integración | Bloques `HW Resource:` con `RELAY_PIN`, `BUZZER_PIN` |
| Refinamiento OR (cim-t8/t9) | **Estructura condicional** | `if/else` en `gestionarRespuestaAcceso()` |
| Softgoals | **Comentarios de trazabilidad** | `Qualification Array:` / `Contribution Array:` en cada función |

**Información incorporada por el diseñador en esta etapa:** plataforma objetivo
(ESP32/Arduino), tecnología de comunicación (MQTT), tipado concreto
(`unsigned long`, `char[32]`, `float`, `bool`), pines de integración y umbral de
confianza.

### 1.3 Fase Code

Se completaron manualmente: credenciales y broker (`secrets.h`), la política de
autorización (`evaluarAutorizacion`), la lógica de simulación de cámara
(`SIMULATION_MODE`), las duraciones de desbloqueo/alarma y el tópico MQTT.

## 2. Análisis: información automática vs. incorporada por el diseñador

| Etapa | Capturado automáticamente | Incorporado por el diseñador |
|---|---|---|
| CIM → PIM | `id`, `name`, `id_cim_parent`, propagación de `qualification_array` y `contribution_array`, correspondencias de constructos, relaciones AND/OR | Períodos de las acciones, estructura del *dependum*, parámetros E/S, campos de recursos SW |
| PIM → PSM | Esqueleto de hilos y funciones, nombres, structs del *dependum*, lógica de publicación/suscripción, comentarios de trazabilidad, condicionales del OR | Plataforma, tecnología de comunicación, tipos concretos, pines |
| Code | — | Credenciales, umbrales, política de autorización, lógica específica de simulación/cámara |

### Grado de automatización estimado

Considerando como "generado" el esqueleto estructural (hilos, funciones, structs,
comunicación, trazabilidad) y como "personalizado" las secciones manuales de la
fase Code:

| CPC | Líneas totales | Personalizadas (aprox.) | % generado |
|---|---|---|---|
| Face Monitor Component (`.ino` + `comm_utils.h`) | 312 | ~70 (simulación, umbral, credenciales) | ~78 % |
| Access Actuator Component (`.ino` + `comm_utils.h`) | 315 | ~65 (política, pines, duraciones) | ~79 % |
| **Total** | **627** | **~135** | **~78 %** |

El resultado es consistente con el grado de automatización reportado para el caso
de estudio del invernadero en MDD4CPS (≈78 %; Navarro et al., 2025).

## 3. Análisis crítico del proceso

**Fortalezas observadas.**
(i) La **trazabilidad** es el mayor aporte: cada función del código enlaza con su
tarea CIM mediante `id_cim_parent`, lo que permitió, por ejemplo, verificar que la
decisión de privacidad (comparar rostros localmente) sobrevive desde el softgoal
cim-q2 hasta un comentario de contribución en `compararConRostrosEnrolados()`.
(ii) La separación CIM/PIM/PSM obligó a **postergar decisiones** correctamente: el
período de muestreo no contaminó el modelo de objetivos, y la elección de MQTT no
apareció hasta el PSM.
(iii) El esqueleto generado impone una **arquitectura homogénea** (hilos + buzón
del *dependum*) que reduce errores de concurrencia típicos en Arduino.

**Limitaciones observadas.**
(i) El DSL no posee constructos para expresar **restricciones temporales duras**
(plazos, prioridades de hilos); el período es un atributo, pero nada verifica su
cumplimiento.
(ii) Los **softgoals se preservan solo como comentarios** en el PSM: la
trazabilidad es informativa, no verificable automáticamente.
(iii) **Limitación verificada empíricamente — de la herramienta `aomdd4cps`,
no del proceso MDD4CPS en sí.** Al ejecutar la herramienta oficial sobre el
mismo CIM ([`comparativa-agente-vs-app.md`](comparativa-agente-vs-app.md)),
ésta descartó los operadores de refinamiento AND/OR en la transformación
CIM→PIM: el PSM generado
([`comparativa-app/modelos/svif-04-PSM.xml`](comparativa-app/modelos/svif-04-PSM.xml))
tiene 0 `<and_ref_operator>` y 0 `<or_ref_operator>`, por lo que la rama OR
no se propaga al código emitido. **La vía agente (skill), en cambio, sí
preserva el OR** hasta el código final: el condicional de
`gestionarRespuestaAcceso()` en
`codigo/AccessActuatorComponent/AccessActuatorComponent.ino` realiza la rama
«desbloqueo ∨ alarma» que el CIM especificaba. El criterio de selección
(umbral de confianza + `authorized`) sí debió añadirse en la fase Code,
porque ningún modelo deduce la política de autorización — esa parte es
general a MDD4CPS y se mantiene como observación aparte.
(iv) Al tratarse de una herramienta en versión alfa con fines académicos, la
edición manual del PIM en diagrams.net sigue siendo necesaria para ajustar
disposición y atributos no solicitados por el cuestionario guiado.

**Balance.** Para un CPS pequeño como SVIF (2 nodos, 1 dependencia), el costo del
modelado se amortiza principalmente en documentación y trazabilidad; el beneficio
crecería con el número de componentes y dependencias, donde la generación del
andamiaje de comunicación es la parte más propensa a error si se escribe a mano.

---

## Al final — comparativa agente (skill) vs. herramienta `aomdd4cps`

Como cierre de la actividad, ofrezco la validación empírica del proceso MDD4CPS
ejecutado de las dos maneras posibles sobre **el mismo CIM de SVIF**:

- **Vía A — agente libre (skill):** un agente LLM aplica las reglas de
  transformación CIM → PIM → PSM → Code razonando en lenguaje natural.
  Es el método con que se produjo el `codigo/` de esta entrega.
- **Vía B — herramienta `aomdd4cps`:** la aplicación oficial del profesor
  ([repositorio](https://github.com/mdd4cps/aomdd4cps), Flask + SaxonC/XSLT +
  Docker Compose) corre las transformaciones XSLT y emite código. La ejecuté
  completa sobre SVIF (4 modelos XML generados, código emitido para 2 CPC).

**Qué se comparó** (en [`comparativa-agente-vs-app.md`](comparativa-agente-vs-app.md)):

| Dimensión | Veredicto |
|---|---|
| Conteo de constructos por fase (CIM→PIM, PIM→PSM, PSM→Code) | tabla con 9 constructos, ambas vías |
| Determinismo y homogeneidad del andamiaje | gana la herramienta (XSLT puro) |
| Compilabilidad del código y plataforma (ESP32) | gana el agente (la app emite MKR 1010 con sintaxis inválida) |
| **Preservación de la semántica AND/OR del CIM** | **gana el agente** (la herramienta descarta los operadores en CIM→PIM) |
| Cobertura de la fase Code | gana el agente (la app deja 22 *stubs*) |
| Verificación punta a punta con broker MQTT real | gana el agente (la app no compila) |
| Garantías de proceso (trazabilidad, auditabilidad) | gana la herramienta |

**Conclusión.** No son sustitutos, se complementan. La herramienta es el
patrón de oro en rigor y reproducibilidad; el agente, en corrección,
plataforma y cobertura de la fase Code. La combinación ideal — usar la
herramienta para el andamiaje determinista y un agente para la fase Code y
la semántica que el DSL aún no expresa — es exactamente lo que esta entrega
implementa en su primera mitad.

**Artefactos para reproducir la comparativa:**

- Análisis detallado: [`comparativa-agente-vs-app.md`](comparativa-agente-vs-app.md)
  (6 secciones: ejecución de cada vía, resultados por fase, lectura del ~78 %,
  síntesis con tabla de 9 criterios, reproducibilidad, referencias).
- Evidencia empírica: [`comparativa-app/`](comparativa-app/)
  ├─ `modelos/` — cadena CIM → PIM → PrePSM → PSM generada por la herramienta
  ├─ `codigo-generado/` — código emitido para MKR 1010 (no compila, conservado
  │  como evidencia del estado alfa de la herramienta)
  └─ `scripts/` — `inject_svif.py`, `inject_psm.py`, `drive.py` (emulan los
     formularios de la app y llaman al backend XSLT).

**Resultado neto:** aplicar MDD4CPS con un agente (Vía A) entregó un sistema
funcional, verificado de punta a punta, con todas las ramas del modelo
ejercitadas. Validar el proceso corriendo su herramienta oficial (Vía B)
reveló dos limitaciones concretas de `aomdd4cps` en su versión actual —
descarte de AND/OR y código no compilable — sin las cuales esta memoria no
habría podido refinar la limitación (iii) de §3.

## Referencias

- Bézivin, J. (2005). On the unification power of models. *Software & Systems
  Modeling, 4*(2), 171–188.
- Navarro, C., Devia, L., Labra Gayo, J. E., & Cares, C. (2025). An agent-oriented
  model-driven development process for cyber-physical systems. *CIbSE 2025*
  (pp. 150–164). SBC.
- Repositorio MDD4CPS: https://github.com/mdd4cps/aomdd4cps
