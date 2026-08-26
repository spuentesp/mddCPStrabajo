# Guion del video — Semana 3 (5–7 minutos)

**Actividad:** Modelado de un CPS mediante AO y DSL.
**Formato exigido:** video individual, con la cámara mostrando de forma continua al
expositor durante la presentación. No se aceptan avatares sintéticos ni narración
automática.
**Apoyo:** `../slides/semana-3/presentacion.pdf` (13 diapositivas) y los dos modelos
abiertos en diagrams.net para mostrarlos en pantalla.

> Versión compacta: los tiempos suman ≈ 5:25, con margen sobre ambos límites del
> enunciado (5:00–7:00). Las láminas «Inventario de elementos» y «Lo que el modelo
> asume (y deja abierto)» (antes 8 y 9) se fusionaron en una sola, y el resto de
> los bloques se ajustó un poco. El texto no está para leerse literalmente: es la
> línea argumental. Hablar con las propias palabras es parte de lo que la rúbrica
> evalúa («Comunicación oral»).

---

## 0:00 – 0:20 · Presentación y encuadre *(diapositiva 1)*

> «El objetivo es aplicar orientación a agentes con iStar 2.0 sobre un sistema
> ciberfísico y mostrar cómo esas mismas decisiones se representan en un DSL
> pensado para CPS.
>
> El sistema es **SVIF**: control de acceso mediante identificación facial, con
> dos componentes ciberfísicos que colaboran — un *Face Monitor* sobre
> ESP32-CAM, que percibe e identifica, y un *Access Actuator* sobre ESP32, que
> acciona una cerradura o una alarma.»

---

## 0:20 – 0:45 · Por qué orientación a agentes *(diapositiva 2)*

> «Elegí orientación a agentes porque en SVIF hay objetivos que entran en
> conflicto: la privacidad frente a la oportunidad de la identificación, y la
> seguridad del recinto frente al uso de recursos. La orientación a agentes
> permite capturar objetivos, responsabilidades y dependencias desde etapas
> tempranas —Cares, Sepúlveda y Navarro, 2019.»

---

## 0:45 – 2:35 · El modelo iStar *(diapositivas 3 a 7; el modelo está en la lámina 4)*

**Mostrar `cim-istar-svif.drawio` en diagrams.net.** Recorrer el paso a paso
sugerido en la clase, nombrando los constructos — este bloque concentra la
mitad del video, es el más denso pero también el más visual:

> «Modelé los dos nodos como **agentes**, porque son instancias concretas con
> autonomía, y al Administrador de Seguridad como **actor**.
>
> **Dependency** — el Access Actuator depende del Face Monitor por el recurso
> *Evento de identificación*: no puede decidir sobre el acceso si nadie
> identifica a la persona. Es la dependencia que articula todo el sistema.
>
> **Refinement** — *Monitorear presencia de personas* se refina en AND en cuatro
> tareas: capturar, detectar, identificar y publicar. En el actuador,
> *Gestionar respuesta de acceso* se refina en **OR**: desbloquear o activar
> alarma. Basta una de las dos.
>
> **NeededBy** — *Capturar imagen* necesita el sensor OV2640; *Desbloquear*
> necesita la cerradura.
>
> **Qualification y Contribution** — aquí están los softgoals. *Comparar con
> rostros enrolados* contribuye **help** a *Privacidad de datos personales*,
> porque el reconocimiento ocurre localmente. *Publicar evento de
> identificación* contribuye **hurt** a esa misma cualidad, porque transmite
> datos por la red. Ese conflicto queda **visible en el modelo**.
>
> Y la dependencia central tiene cinco partes: depender —Access Actuator—,
> dependerElmnt —por qué—, dependum —el evento—, dependee —Face Monitor— y
> dependeeElmnt —cómo lo provee.»

---

## 2:35 – 2:55 · Inventario y qué queda abierto *(diapositiva 8)*

> «Cada elemento tiene un identificador estable —27 en total—: viajan al DSL en
> `id_cim_parent`, y de ahí al código. Dos decisiones quedan abiertas a
> propósito: el criterio del OR y los tiempos — ninguna pertenece a este nivel.»

---

## 2:55 – 3:20 · Por qué hace falta un DSL *(diapositiva 9)*

> «El modelo de agentes me dice qué quiere cada componente y por qué. Pero para
> implementar esto sobre Arduino necesito hilos, temporizadores, funciones y
> acceso a recursos físicos. El DSL es el puente: conserva las decisiones del
> modelo AO pero las expresa en conceptos más fáciles de mapear al software,
> todavía sin comprometerse con una plataforma.»

---

## 3:20 – 4:20 · El modelo DSL y la correspondencia *(diapositivas 10 y 11)*

**Mostrar `pim-dsl-svif.drawio`.** Ir señalando los pares:

> «Cada **Agent** pasó a **CP Component**. Los objetivos pasaron a **On
> Interval Actions** —y aquí el DSL me obliga a declarar el período: 500 ms
> para la percepción, 250 para la actuación. Las tareas pasaron a **On Demand
> Actions**; los recursos se separaron en **HW** y **SW Resources**. Los
> refinamientos AND y OR se conservan explícitos.
>
> Y lo más interesante: la dependencia se materializó como un **Message
> Sender** en el monitor y un **Message Receiver** en el actuador — en un CPS
> distribuido, la delegación entre actores se convierte en un mensaje por la
> red. El dependum pasó a ser la estructura del mensaje: timestamp, person_id,
> person_name, confidence y authorized. Transmito la **identidad**, nunca la
> imagen — esa decisión viene del softgoal de privacidad.»

---

## 4:20 – 5:10 · Qué se gana y qué se pierde *(diapositiva 12)*

Esta es la lámina del criterio «Análisis y explicación». No apurarla, aunque el
resto del video vaya rápido.

> «Al traducir gané información que el modelo de agentes no fijaba: períodos,
> estructura de datos, parámetros de cada acción. Pero perdí expresividad:
> primero, los **softgoals dejaron de ser nodos** — sobreviven en
> `contribution_array`, pero hay que ir a buscarlos. Segundo, actor, rol y
> agente colapsan en CP Component. Tercero, el actor humano quedó fuera. Y
> cuarto, el **criterio del OR no se expresa**: reaparece recién en el código.
>
> No lo veo como un defecto: cada nivel retiene lo que necesita para la
> transformación siguiente, y `id_cim_parent` es el mecanismo que me permite
> volver al modelo de agentes a recuperar el porqué.»

---

## 5:10 – 5:25 · Cierre *(diapositiva 13)*

> «En resumen: modelé SVIF con iStar 2.0, con goals, softgoals, tasks y
> resources, y con la dependencia *Evento de identificación* entre los dos
> componentes. Construí la representación equivalente en el DSL y establecí la
> correspondencia elemento por elemento. En la Semana 4 este modelo se
> transforma en código para ESP32.»

---

## Checklist antes de grabar

- [ ] Cámara encendida y visible durante **toda** la exposición.
- [ ] `cim-istar-svif.drawio` y `pim-dsl-svif.drawio` abiertos en pestañas listas.
      Ambos modelos ya están incrustados en las láminas 4 y 10, así que si la
      demostración en vivo falla, el mazo se sostiene solo.
- [ ] Duración entre 5 y 7 minutos (medir en un ensayo previo; esta versión apunta
      a ~5:25, con margen de sobra hacia ambos límites).
- [ ] Los cuatro entregables listos: los dos `.drawio`, la presentación en PDF y el video.
- [ ] Nombrar al menos una vez las fuentes: Dalpiaz et al. (2016) para iStar 2.0,
      Navarro et al. (2025) para el DSL, Cares et al. (2019) para la justificación del
      paradigma.
