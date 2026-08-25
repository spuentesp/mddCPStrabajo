# Guion del video — Semana 3 (5–7 minutos)

**Actividad:** Modelado de un CPS mediante AO y DSL.
**Formato exigido:** video individual, con la cámara mostrando de forma continua al
expositor durante la presentación. No se aceptan avatares sintéticos ni narración
automática.
**Apoyo:** `../slides/semana-3/presentacion.pdf` (12 diapositivas) y los dos modelos
abiertos en diagrams.net para mostrarlos en pantalla.

> Los tiempos son orientativos y suman ≈ 6:15, dentro de la ventana de 5–7 min.
> El texto no está para leerse literalmente: es la línea argumental. Hablar con
> las propias palabras es parte de lo que la rúbrica evalúa («Comunicación oral»).

---

## 0:00 – 0:35 · Presentación y encuadre *(diapositiva 1)*

Presentarse y enunciar el objetivo de la actividad:

> «El objetivo es aplicar orientación a agentes con iStar 2.0 sobre un sistema
> ciberfísico y luego mostrar cómo esas mismas decisiones se representan en un DSL
> pensado para CPS.
>
> El sistema que elegí es **SVIF**: un control de acceso a un recinto mediante
> videovigilancia con identificación facial. Tiene **dos componentes ciberfísicos
> que colaboran**: un *Face Monitor* sobre ESP32-CAM, que percibe e identifica, y un
> *Access Actuator* sobre ESP32, que acciona una cerradura o una alarma.»

---

## 0:35 – 1:15 · Por qué orientación a agentes *(diapositiva 2)*

> «Elegí orientación a agentes porque en SVIF hay **objetivos que entran en
> conflicto**: la privacidad de los datos de las personas frente a la oportunidad de
> la identificación, y la seguridad del recinto frente al uso de recursos.
>
> La orientación a agentes permite capturar objetivos, responsabilidades y
> dependencias desde etapas tempranas —Cares, Sepúlveda y Navarro, 2019— y eso es
> justamente lo que necesito para razonar sobre esos conflictos antes de escribir
> código.»

---

## 1:15 – 2:45 · El modelo iStar *(diapositivas 3 a 6 + modelo en pantalla)*

**Mostrar `cim-istar-svif.drawio` en diagrams.net.** Recorrer el paso a paso
sugerido en la clase, nombrando los constructos:

> «Modelé los dos nodos como **agentes**, porque son instancias concretas con
> autonomía, y al Administrador de Seguridad como **actor**.
>
> **Dependency** — en la vista SD, el Access Actuator depende del Face Monitor por el
> recurso *Evento de identificación*: no puede decidir sobre el acceso si nadie
> identifica a la persona. Esta es la dependencia que articula todo el sistema.
>
> **Refinement** — el objetivo *Monitorear presencia de personas* se refina en AND en
> cuatro tareas: capturar imagen, detectar rostro, identificar rostro y publicar el
> evento. En el actuador, *Gestionar respuesta de acceso* se refina en **OR**:
> desbloquear cerradura **o** activar alarma. Basta una de las dos.
>
> **NeededBy** — *Capturar imagen* necesita el sensor OV2640; *Desbloquear cerradura*
> necesita la cerradura electromecánica.
>
> **Qualification y Contribution** — aquí están los softgoals. *Comparar con rostros
> enrolados* contribuye **help** a *Privacidad de datos personales*, porque el
> reconocimiento ocurre localmente en el nodo. Y *Publicar evento de identificación*
> contribuye **hurt** a esa misma cualidad, porque transmite datos personales por la
> red. Ese conflicto queda **visible en el modelo**, y es exactamente el tipo de
> tensión que la orientación a agentes permite discutir.»

---

## 2:45 – 3:20 · Por qué hace falta un DSL *(diapositiva 9)*

> «El modelo AO me dice **qué** quiere cada componente y **por qué**. Pero si voy a
> implementar esto sobre Arduino, necesito hablar de hilos, temporizadores,
> funciones y acceso a recursos físicos. Entre el modelo y el código hay una
> distancia considerable.
>
> El DSL para CPS es el **puente**: conserva las decisiones del modelo AO pero las
> expresa con conceptos más fáciles de mapear al software, todavía sin comprometerse
> con una plataforma concreta.»

---

## 3:20 – 4:40 · El modelo DSL y la correspondencia *(diapositiva 10 + modelo en pantalla)*

**Mostrar `pim-dsl-svif.drawio`.** Ir señalando los pares:

> «Cada **Agent** pasó a ser un **CP Component**. Los dos objetivos, que son
> persistentes y requieren verificación continua, pasaron a **On Interval Actions**
> —y aquí el DSL me obliga a declarar el período: 500 ms para la percepción, 250 ms
> para la actuación, porque la respuesta debe ser más reactiva que el muestreo.
>
> Las **tareas** pasaron a **On Demand Actions**. Los recursos se separaron según su
> naturaleza: el sensor, la cerradura y la alarma son **HW Resources**; la base de
> rostros enrolados y la bitácora son **SW Resources**, con su `data_structure`.
>
> Los refinamientos **AND** y **OR** se conservan como operadores explícitos.
>
> Y lo más interesante: la **dependencia** del modelo iStar se materializó como un
> **Message Sender** en el Face Monitor y un **Message Receiver** en el Access
> Actuator. En un CPS los componentes están distribuidos, así que la delegación
> entre actores se convierte en intercambio de información por la red. El *dependum*
> pasó a ser el `dependum_data_structure` del mensaje: timestamp, person_id,
> person_name, confidence y authorized.
>
> Fíjense en esa estructura: transmito la **identidad**, nunca la imagen. Esa
> decisión viene directamente del softgoal de privacidad del modelo AO.»

---

## 4:40 – 5:45 · Análisis: qué se gana y qué se pierde *(diapositiva 11)*

Esta es la parte que la rúbrica evalúa como «Análisis y explicación». No apurarla.

> «Al traducir gané información que el CIM deliberadamente no fijaba: los períodos,
> la estructura de los datos, los parámetros de entrada y salida de cada acción.
>
> Pero también **perdí expresividad**, y creo que vale la pena decirlo con
> honestidad:
>
> Primero, los **softgoals dejaron de ser nodos**. En iStar, la contribución *hurt*
> de publicar el evento sobre la privacidad es una arista que se ve y se discute. En
> el DSL es una entrada dentro de `contribution_array`: sobrevive, pero hay que ir a
> buscarla.
>
> Segundo, la distinción entre **actor, rol y agente** desaparece: los tres colapsan
> en CP Component.
>
> Tercero, el **actor humano** quedó fuera del PIM, porque el DSL modela nodos
> computacionales.
>
> Y cuarto, el **criterio del OR** no se expresa: el DSL dice que basta una de las
> dos ramas, pero no bajo qué condición se elige cada una. Eso reaparece recién en
> el código.
>
> No lo veo como un defecto del DSL. Cada nivel retiene lo que necesita para la
> transformación siguiente, y el atributo `id_cim_parent` es justamente el mecanismo
> que me permite volver al modelo de agentes a recuperar el *porqué* cuando lo
> necesito.»

---

## 5:45 – 6:15 · Cierre *(diapositiva 12)*

> «En resumen: modelé SVIF con iStar 2.0 en vistas SD y SR híbrida, con goals,
> softgoals, tasks y resources, y con la dependencia *Evento de identificación*
> entre los dos componentes. Construí la representación equivalente en el DSL para
> CPS y establecí la correspondencia elemento por elemento, analizando qué se
> conserva y qué no.
>
> Los dos archivos `.drawio` van adjuntos. En la Semana 4 este PIM se transforma en
> código para ESP32.»

---

## Checklist antes de grabar

- [ ] Cámara encendida y visible durante **toda** la exposición.
- [ ] `cim-istar-svif.drawio` y `pim-dsl-svif.drawio` abiertos en pestañas listas.
- [ ] Duración entre 5 y 7 minutos (medir en un ensayo previo).
- [ ] Los cuatro entregables listos: los dos `.drawio`, la presentación en PDF y el video.
- [ ] Nombrar al menos una vez las fuentes: Dalpiaz et al. (2016) para iStar 2.0,
      Navarro et al. (2025) para el DSL, Cares et al. (2019) para la justificación del
      paradigma.
