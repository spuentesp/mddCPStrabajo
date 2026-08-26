# EMI305 · Sistemas Ciberfísicos — Compendio de la materia (Semanas 1–4)

> Apunte de estudio que secciona, explica y resume el contenido de las cuatro
> semanas del módulo. Cada sección cierra con un recuadro **«En síntesis»** y,
> cuando ayuda, un ejemplo con el caso de estudio del curso (SVIF). Las fuentes
> corresponden a la bibliografía citada en las diapositivas; su detalle APA con
> DOI está en `referencias.md`.

---

## SEMANA 1 — Introducción a los Sistemas Ciberfísicos

### 1.1 Origen: la cibernética

- Los términos *cyberspace* y *cyber-physical* provienen de la **cibernética**
  (*cybernetics*), desarrollada por **Norbert Wiener** en la década de 1940 para
  estudiar sistemas de control y comunicación.
- Su interés central: cómo un sistema puede **percibir** su entorno, **tomar
  decisiones** y **actuar** sobre él. Para ello introdujo la
  **retroalimentación** (*feedback*): las acciones futuras dependen de los
  resultados observados previamente.
- La palabra viene del griego *kybernetes* (κυβερνήτης): timonel o gobernador —
  una metáfora de conducción y control.
- Estos principios persisten hoy en los CPS mediante **ciclos de percepción,
  decisión y actuación**.

> **En síntesis:** un CPS es heredero directo de la cibernética: percibe,
> decide y actúa en lazo cerrado sobre el mundo físico.

### 1.2 ¿Qué es un sistema ciberfísico?

Dos definiciones complementarias vistas en clase:

1. «Un CPS es una **orquestación de computadoras y sistemas físicos**»
   (Lee, 2015).
2. «Los CPS son la **integración de hardware distribuido controlado por
   software distribuido** con el propósito de **controlar procesos físicos**»
   (Cares, Sepúlveda y Navarro, 2019).

En la práctica, un CPS debe integrar **cuatro elementos**:

| Elemento | Función | En SVIF |
|---|---|---|
| **Sensores** | Percibir variables del mundo real | Cámara OV2640 |
| **Actuadores** | Actuar sobre el mundo real | Relé de cerradura, buzzer |
| **Cómputo** | Decidir (software en dispositivos y computadores) | ESP32 (identificación local) |
| **Comunicaciones** | Coordinar los nodos distribuidos | MQTT sobre WiFi |

**CPS frente a conceptos vecinos** (IoT, Industria 4.0, M2M, *Industrial
Internet*): CPS es el concepto **más amplio y fundamental** — no impone un
enfoque de implementación (como IoT, centrado en interconectar objetos) ni una
aplicación particular (como Industria 4.0). Se centra en el problema de **unir
la ingeniería del mundo cibernético con la del mundo físico**.

### 1.3 ¿Por qué auge ahora? Factores facilitadores

- **Bajo costo del cómputo embebido**: microcontroladores (MCU: ESP32, Arduino,
  PIC, AVR) y computadores de placa única (SBC: Raspberry Pi, ODROID), por
  algunos miles de pesos.
- **Sensores y actuadores asequibles**: ultrasonido, temperatura, PIR, cámaras,
  servos, relés, cerraduras electrónicas… (cientos a miles de CLP).
- **Conectividad ubicua** LAN/WAN y tecnologías como **SDN** (*Software-Defined
  Networking*), que separa el plano de control del plano de datos y permite
  «programar la red» (Kreutz et al., 2015).
- Impulso institucional: a comienzos de los 2000, la **NSF** (EE. UU.) instaló
  el concepto moderno de CPS como área de investigación prioritaria.

### 1.4 Ámbitos de aplicación

Automotriz, manufactura, dispositivos médicos, vida asistida (*assisted
living*), control de tráfico, sistemas militares, control de procesos,
generación y distribución de energía, HVAC, aeronaves, trenes, seguridad
física (control de acceso y monitoreo — el dominio de SVIF), robótica
distribuida, telemedicina (Zanero, 2017).

### 1.5 Desafíos abiertos (Marwedel & Engel, 2016)

| Desafío | Idea central |
|---|---|
| **Safety** (seguridad física) | Posibilidad de daño a personas/entorno (p. ej., robot industrial que aplasta a un trabajador). |
| **Security** (seguridad lógica) | Tríada CIA: **confidencialidad** (acceso solo autorizado), **integridad** (exactitud y completitud), **disponibilidad** (acceso cuando se requiera). |
| **Reliability** (fiabilidad) | Probabilidad de que el CPS haga lo esperado. |
| **Energy efficiency** | Muchos CPS operan con baterías o energía recolectada; la energía es un recurso escaso (ej.: rovers de Marte). |
| **Dynamism** | Componentes móviles y entornos cambiantes: calidades, velocidades y costos de comunicación variables → se exige tolerancia a fallos. |
| **Timing predictability** | «Responder a tiempo»: reaccionar dentro de un intervalo dictado por el entorno. Lee (2006) argumenta que los fundamentos de la computación priorizaron la corrección lógica y trataron el tiempo como secundario — inadecuado para CPS. |
| **Sampling intervals** | El procesamiento correcto de señales físicas depende de un muestreo adecuado (teorema del muestreo). |
| **Heterogeneity** | Interoperar componentes de distintos fabricantes/protocolos. |
| **Multidisciplinary nature** | Diversidad de dominios, terminologías y expectativas; no hay receta fácil de integración. |
| **Legal / Human & Social issues** | Responsabilidad por las acciones; impacto en empleos y formas de vida. |
| **Verification problem** | ¿Es correcto el CPS? Con componentes físicos imperfectos se requieren modelado y criterios de aceptación. |

### 1.6 De los desafíos a la arquitectura

**Si los desafíos se interpretan como requerimientos**, emergen arquitecturas
apropiadas, organizadas por capas según el tiempo de respuesta (organización de
referencia, cf. taxonomías edge/fog/cloud discutidas en la literatura, p. ej.
Satyanarayanan, 2017):

| Capa | Rol | Tiempo de respuesta | Tecnologías típicas |
|---|---|---|---|
| **Cloud** | Big data, lógica de negocio, data warehousing, gemelos digitales | Más lento | AWS/Azure/Google IoT, ThingSpeak |
| **Fog** | Análisis en red local, reducción del lazo de control | Intermedio | Brokers MQTT, Node-RED, Docker, bases de datos |
| **Edge** | Procesamiento de datos en tiempo real, micro-almacenamiento | Rápido | WiFi, LoRa, Zigbee, MQTT, CoAP, BLE, 5G |
| **Data originators** | Sensores y actuadores | Más rápido | I2C, SPI, UART, PWM, Modbus, CAN |

### 1.7 El equipo de trabajo y la disciplina «CPS Engineering»

Roles habituales: arquitecto de soluciones, ingenieros de hardware y de
software/firmware, especialista en seguridad, frontend/UX, científico de
datos, redes, gestor de proyecto, normas/regulaciones, nube/backend. Pregunta
provocadora de la clase: **¿no falta un “ingeniero CPS”?**

Argumento por analogía con 1968 (ingeniería de software): los CPS complejos a
gran escala son fundamentalmente distintos de construir controladores
pequeños; la mayoría de los proyectos científico-tecnológicos los involucra;
deben producirse de forma costo-efectiva y gestionarse. La ingeniería para CPS
está en la **intersección (no la unión)** de lo físico y lo informático, y
requiere **modelos y métodos propios** (Lee, 2015). Definición por similitud
con la IEEE:

> *Cyber-physical Systems Engineering* es la aplicación de enfoques
> sistemáticos, disciplinados y medibles al desarrollo, operación y
> mantenimiento de sistemas ciberfísicos.

> **En síntesis (Semana 1):** un CPS integra sensores, actuadores, cómputo y
> comunicaciones para controlar procesos físicos en lazo cerrado. Su auge se
> explica por hardware barato y conectividad. Sus desafíos (tiempo, energía,
> seguridad, verificación…) se leen como requerimientos que moldean
> arquitecturas cloud/fog/edge, y motivan una disciplina de ingeniería propia.

---

## SEMANA 2 — Modelo, niveles de modelado, metamodelo, DSL y MDD

### 2.1 ¿Qué es un modelo y para qué sirve?

- «Un modelo es una **representación de la realidad para algún propósito
  definido**» (Pidd, 2003). Ejemplo de clase: distintos mapas de una ciudad
  (transporte público, ciclovías) resaltan aspectos distintos según el
  propósito.
- Un modelo es útil para **documentar**, **razonar** (propiciar buenas
  decisiones de diseño) y **comunicar**.
- Un modelo útil es (Selic, 2003): **abstracto**, **fácil de entender**,
  **preciso**, **predictivo** y **barato** (mucho más que construir el sistema).
- Relaciones clave: el sistema *is-represented-by* el modelo; el modelo
  *conforms-to* un paradigma de modelado (Aßmann, Zschaler y Wagner, 2006).

### 2.2 Niveles de modelado (¿quién define las reglas?)

Analogía cartográfica y su equivalente en software:

| Analogía (mapa) | Espacio visual | Espacio textual |
|---|---|---|
| Ciudad (realidad) | Sistema | Sistema |
| Mapa | **Modelo** | Código fuente |
| Leyenda | **Metamodelo** (p. ej., UML) | Sintaxis |
| Cartografía | **Metametamodelo** (MOF) | Metalenguaje (EBNF) |

Cada nivel «conforma-a» el superior; los niveles superiores son
autodescriptivos (metacircularidad).

### 2.3 ¿Basta UML? → los DSL

UML describe muy bien clases, objetos, componentes e interacciones, pero
dominios como los CPS incorporan **conceptos muy específicos** (mecanismos
físicos, hilos periódicos, recursos de hardware). Extender UML es posible pero
incrementa la complejidad. La alternativa: **crear un lenguaje propio**.

Un **DSL** (*Domain-Specific Language*) es «un lenguaje bien definido diseñado
para expresar soluciones utilizando conceptos especializados de un dominio
particular» (adaptado de Fowler y Parsons, 2010; Mernik, Heering y Sloane, 2005). Todo
DSL posee **tres elementos**:

| Elemento | Qué define | Ejemplo (DSL PIM del curso) |
|---|---|---|
| **Sintaxis abstracta** (metamodelo) | Conceptos, relaciones y reglas de buena formación | `CPComponent` contiene acciones, recursos y comunicación |
| **Sintaxis concreta** (notación) | Representación gráfica o textual | Biblioteca de figuras para diagrams.net |
| **Semántica** (significado) | Cómo interpretar los conceptos; se define traduciéndolos a un lenguaje destino conocido | `OnIntervalAction` → hilo periódico en C++ |

Ejemplos de DSL: SQL (bases de datos), HTML (documentos web), Terraform
(infraestructura), Simulink (control), BPMN (procesos de negocio).

**Ventajas**: conceptos expresivos, modelos comprensibles para expertos del
dominio, menos complejidad y errores. **Desventajas**: curva de aprendizaje,
falta de estándares/herramientas, costo de evolución. Regla práctica: *el DSL
debe aportar suficiente valor al dominio para justificar construirlo y
mantenerlo*.

### 2.4 MDD: Desarrollo Dirigido por Modelos

- Bézivin (2005) propone ver **el ciclo de vida del software como una cadena de
  transformaciones de modelos**. Dos artefactos principales: **modelos** y
  **transformaciones**.
- La idea no es nueva: (diagrama de clases → generación de código → Java) y
  (código fuente → compilación → ejecutable) ya son transformaciones
  entrada-proceso-salida.

> **En síntesis (Semana 2):** modelamos para razonar barato y sin ambigüedad;
> las reglas del modelado viven en el metamodelo. Cuando UML no expresa bien
> el dominio, se construye un DSL (metamodelo + notación + semántica). MDD
> encadena transformaciones automáticas de modelos hasta llegar al producto.

---

## SEMANA 3 — Orientación a agentes y DSL para CPS

### 3.1 ¿Por qué agentes para CPS?

Los CPS involucran componentes distribuidos cuyos objetivos **pueden entrar en
conflicto** (ej.: ahorro de energía vs. precisión). La orientación a agentes
(OA) es reconocida como paradigma adecuado para modelar sistemas complejos,
autónomos y distribuidos, capturando **objetivos, responsabilidades y
dependencias desde etapas tempranas** (Cares, Sepúlveda y Navarro, 2019).

### 3.2 El paradigma BDI (Bratman, 1987)

- Propuesto por el filósofo **Michael Bratman** para explicar la acción humana
  racional; luego adoptado por la IA para construir agentes de software.
- Tres actitudes mentales:
  - **Creencias** (*Beliefs*): lo que el agente considera verdadero del mundo.
  - **Deseos** (*Desires*): estados del mundo que quisiera alcanzar.
  - **Intenciones** (*Intentions*): compromisos prácticos que adopta para
    actuar → **planes**.
- Matiz importante: una **acción racional no es** una sucesión de reacciones
  aisladas; **sí es** actividad organizada por planes e intenciones que
  persisten en el tiempo. Las intenciones estabilizan el comportamiento y
  evitan reconsiderarlo todo continuamente.
- Codificación (Rao & Georgeff, 1995): creencias → variables/BD/expresiones
  lógicas; deseos → estructuras objetivo; intenciones → hilos de ejecución,
  procedimientos.

### 3.3 ¿Qué es un agente (de software)?

- «Un agente es un sistema computacional **situado en un entorno**, capaz de
  **acción autónoma flexible** para cumplir sus objetivos de diseño»
  (Jennings, Sycara y Wooldridge, 1998).
- Propiedades según Wooldridge & Ciancarini (2001):

| Propiedad | Significado |
|---|---|
| **Autonomía** | Estado interno propio; decide con base en él |
| **Reactividad** | Percibe su ambiente y responde a los cambios |
| **Proactividad** | Tiene objetivos propios y toma la iniciativa |
| **Habilidad social** | Coopera, colabora, negocia con otros agentes/humanos |

- Evolución de conceptos: programa → subrutina → **objeto** (estado local
  persistente) → **agente** (objeto + hilo de ejecución independiente +
  iniciativa) (Lind, 2001). Fórmula de clase: *agente = objeto + autonomía*.
- Taxonomía de Nwana (1996): según combinen **cooperación**, **aprendizaje** y
  **autonomía** surgen agentes colaboradores, de interfaz, inteligentes, etc.
- **El entorno es el problema; el agente es la solución** (Russell & Norvig).
  Dimensiones del entorno: totalmente/parcialmente observable, determinista/
  estocástico, episódico/secuencial, estático/dinámico, discreto/continuo,
  individual/multiagente (competitivo o cooperativo).

### 3.4 iStar 2.0: modelado orientado a agentes (Dalpiaz, Franch y Horkoff, 2016)

Lenguaje para análisis y diseño **temprano** de sistemas complejos, centrado en
actores intencionales, sus objetivos y sus dependencias.

**Constructos:**

| Grupo | Elementos |
|---|---|
| Actores | **Actor** (genérico), **Agente** (instancia concreta), **Rol** (función abstracta); *boundary* (límite) delimita lo interno |
| Elementos intencionales | **Goal** (objetivo), **Quality/Softgoal** (cualidad deseada, sin criterio nítido de satisfacción), **Task** (tarea), **Resource** (recurso) |
| Enlaces de actores | `is-a`, `participates-in` |
| Enlaces intencionales | **Dependency**, **Refinement** (AND/OR), **NeededBy**, **Qualification**, **Contribution** (make/help/hurt/break) |

**La dependencia** tiene cinco partes: *depender* (quien depende) →
*dependerElmnt* (por qué) → **dependum** (qué) → *dependee* (quien provee) →
*dependeeElmnt* (cómo). Ejemplo SVIF: el actuador (depender, «Evaluar
autorización») depende del monitor (dependee, «Publicar evento») para el
recurso «Evento de identificación» (dependum).

**Refinamientos**: AND = todos los hijos son necesarios; OR = cualquier hijo
basta. **NeededBy** vincula una tarea con el recurso que necesita.
**Qualification** asocia una cualidad al elemento que califica.
**Contribution** indica aportes positivos o negativos a un softgoal.

**Vistas**: **SD** (*Strategic Dependency*: solo actores y dependencias),
**SR** (*Strategic Rationale*: detalle interno) e **híbrida SD/SR**.

**Paso a paso sugerido en clase**: (1) *Dependency* — identificar agentes e
interdependencias (vista SD); (2) *Refinement* — refinar objetivos y tareas;
(3) *NeededBy* — recursos que requieren las tareas; (4) *Qualification* —
softgoals y qué elementos deben alcanzarlos; (5) *Contribution* — cómo cada
elemento apoya o perjudica los softgoals.

### 3.5 Del modelo AO hacia la implementación: el DSL PIM para CPS

- Los modelos AO capturan objetivos y dependencias de alto nivel, pero las
  plataformas concretas (p. ej., Arduino) exigen conceptos más específicos:
  funciones, hilos, temporizadores, variables de estado, comunicación, acceso
  a recursos físicos. Hay **distancia considerable** entre ambos niveles.
- Solución: una representación **puente**, independiente de tecnología pero
  suficientemente específica → el **DSL para CPS** (biblioteca personalizada
  de diagrams.net), con constructos:

| Constructo DSL | Semántica | Representa del CIM |
|---|---|---|
| **Cyber-Physical Component (CPC)** | Contenedor computacional de un nodo CPS (acciones, recursos, comunicación); trazabilidad por `id`, `name`, `id_cim_parent` | Actor / Agente / Rol |
| **On Interval Action** | Proceso evaluado **periódicamente** (atributo `interval_in_milliseconds`); conserva softgoals vía `qualification_array` y `contribution_array` | Goal |
| **On Demand Action** | Procedimiento ejecutado **bajo demanda** (evento o solicitud); con parámetros de entrada/salida independientes de tecnología y modos de operación | Task |
| **SW Resource** | Recurso de software con estructura de datos | Resource (software) |
| **HW Resource** | Recurso físico requerido | Resource (hardware) |
| **Message Sender / Receiver** | Hilos de comunicación que intercambian el *dependum* | Dependency |
| **AND / OR** | Operadores de refinamiento | Refinement |
| **From-To Relation** | Flujo entre constructos | enlaces internos |

> **En síntesis (Semana 3):** los agentes (autonomía + reactividad +
> proactividad + habilidad social; BDI: creencias-deseos-intenciones) permiten
> modelar CPS con objetivos en conflicto. iStar 2.0 expresa actores,
> dependencias, refinamientos y softgoals; el DSL PIM traduce esos conceptos a
> constructos implementables sin fijar aún la tecnología.

---

## SEMANA 4 — MDD4CPS: proceso de desarrollo dirigido por modelos para CPS

### 4.1 La cadena de modelos

MDD organiza el desarrollo como secuencia de modelos con niveles de
abstracción decrecientes; **cada transformación incorpora decisiones de diseño
del siguiente nivel**, preservando la información relevante del anterior:

```
CIM  ──►  PIM  ──►  PSM  ──►  Code
```

En **MDD4CPS** (Navarro, Devia, Labra Gayo y Cares, 2025), cada etapa usa un
lenguaje adecuado:

| Fase | Modelo | Lenguaje |
|---|---|---|
| **CIM** (*Computation Independent Model*) | Diseño de contexto | iStar 2.0 (orientado a agentes) |
| **PIM** (*Platform Independent Model*) | Modelado funcional independiente de tecnología | DSL para CPS |
| **PSM** (*Platform Specific Model*) | Código generado para la plataforma elegida | C++ Arduino |
| **Code** | Configuración y personalización manual | C++ Arduino |

### 4.2 Cómo se implementan las transformaciones

- Opciones en el estado del arte: ATL, QVT, Acceleo, EMF, XML. MDD4CPS optó
  por **tecnologías abiertas**: modelado visual en **diagrams.net** (que
  serializa a **XML**) y transformaciones con **XSLT** (CIM→PIM) y scripts
  Python (PIM→PSM).
- **XSLT** es un lenguaje declarativo que transforma documentos XML en otros
  documentos: una transformación **reconoce elementos del modelo de entrada y
  genera automáticamente la estructura correspondiente en el de salida** — la
  misma idea de MDD.
- **Pero no todo es deducible automáticamente**: el diseñador incorpora
  progresivamente la información ausente en el nivel anterior. Una
  **herramienta web** guía esa captura, solicitando solo los datos necesarios.

**CIM → PIM** (decisiones aún independientes de tecnología): periodicidad de
las `OnIntervalActions`, parámetros de entrada/salida de las
`OnDemandActions`, estructura del *dependum* y de los `SW Resources`. El PIM
resultante puede seguir editándose en diagrams.net.

**PIM → PSM** (decisiones de plataforma): plataforma objetivo (Arduino),
tecnología de comunicación (MQTT), tipado concreto de estructuras y
parámetros. El resultado es **código fuente C++ que sigue siendo un modelo**:
quedan aspectos abiertos para la fase Code (credenciales WiFi, configuración
del broker, integración con pines).

### 4.3 Correspondencias PIM → PSM (qué genera cada constructo)

| Constructo PIM | Se materializa como |
|---|---|
| **CPComponent** | **Unidad de despliegue**: archivos `.ino` (entrada: inicializa WiFi/MQTT/hardware, `setup()`, `loop()` mínimo y creación de hilos), `comm_utils.h` (publicación/suscripción MQTT, serialización del *dependum*, estructuras de mensaje) y `secrets.h` (manual: credenciales y parámetros sensibles) |
| **OnDemandAction** | **Función ejecutable** invocada por eventos u otros elementos; nombre, parámetros y tipos derivados del modelo; la lógica específica queda abierta para la fase Code |
| **OnIntervalAction** | **Hilo periódico** (FreeRTOS en Arduino MKR1010) cuyo período proviene de `interval_in_milliseconds` |
| **MessageSender / MessageReceiver** | **Hilos de comunicación**: publicar periódicamente el *dependum* / recibir, deserializar y mantenerlo disponible localmente; comparten estructura y periodicidad |
| **SWResource** | **Estructuras de datos / variables tipadas** |
| **HWResource** | **Comentarios estructurados** y marcas de trazabilidad que orientan la integración del hardware en la fase Code |
| **Softgoals** | No generan estructuras ejecutables: se preservan como **comentarios de trazabilidad** (calificaciones y contribuciones) visibles desde iStar hasta el código |
| **Refinamientos AND/OR** | **Estructuras lógicas** (condicionales/funciones de evaluación) |

### 4.4 Grado de automatización y herramientas

- En el caso de estudio del curso (invernadero automatizado, Arduino MKR1010),
  la generación automática produjo **≈78 % del código final** (1216 de 1567
  líneas); el ~22 % restante es configuración de plataforma y lógica propia.
- Herramientas por fase: CIM y PIM se modelan en **diagrams.net** con
  bibliotecas personalizadas (representación gráfica y XML); PSM y Code son
  textuales (C++ Arduino). Las transformaciones son **semiautomáticas y
  guiadas por el usuario**.
- Repositorio público del proceso: https://github.com/mdd4cps/aomdd4cps
  (bibliotecas, scripts de transformación, herramienta de captura de
  decisiones, caso de estudio completo).

> **En síntesis (Semana 4):** MDD4CPS concreta el MDD para CPS con la cadena
> iStar → DSL → C++ Arduino → código final. Las transformaciones (XSLT/Python)
> capturan automáticamente lo trazable (ids, nombres, relaciones, softgoals) y
> piden al diseñador solo lo nuevo de cada nivel (períodos, dependum,
> plataforma, tipos). Resultado: ~78 % del código generado y trazabilidad
> completa desde el objetivo de negocio hasta el hilo que lo ejecuta.

---

## Hilo conductor de las cuatro semanas (mapa mental en una frase)

**Semana 1** define el *qué* (CPS: percibir-decidir-actuar, desafíos como
requerimientos); **Semana 2** aporta el *con qué pensar* (modelos, metamodelos,
DSL, MDD); **Semana 3** aporta el *cómo conceptualizar* (agentes/iStar y el DSL
puente); y **Semana 4** entrega el *cómo producir* (MDD4CPS: transformaciones
sucesivas hasta el código). El caso SVIF de este repositorio recorre el ciclo
completo.

## Bibliografía del compendio

La lista APA 7 completa, con DOI/URL verificables, está en
[`referencias.md`](referencias.md). Fuentes principales por semana:

- **S1:** Lee (2006, 2015); Cares, Sepúlveda y Navarro (2019); Marwedel y
  Engel (2016); Zanero (2017); Kreutz et al. (2015).
- **S2:** Pidd (2003); Selic (2003); Aßmann, Zschaler y Wagner (2006);
  Fowler y Parsons (2010); Mernik, Heering y Sloane (2005); Bézivin (2005); Kleppe et
  al. (2003).
- **S3:** Bratman (1987); Rao y Georgeff (1995); Jennings, Sycara y Wooldridge
  (1998); Wooldridge y Ciancarini (2001); Nwana (1996); Lind (2001); Russell y
  Norvig (2004); Dalpiaz, Franch y Horkoff (2016).
- **S4:** Bézivin (2005); Navarro, Devia, Labra Gayo y Cares (2025).
