# Guion hablado de las presentaciones — EMI305

Guion **lámina por lámina** de los cuatro mazos del curso. Complementa a los
`semana-N/guion-video.md`, que están organizados por bloques de tiempo para la
grabación; este documento va en el otro eje: **qué decir sobre cada diapositiva
concreta**, en el orden en que aparecen.

**Cómo usarlo.** Cada lámina trae tres cosas:

- **Idea única** — lo que la lámina tiene que dejar instalado. Si al terminar de
  hablar esa idea no quedó clara, la lámina falló.
- **Qué decir** — la línea hablada. No es un libreto para leer: es el argumento.
  Las cuatro rúbricas evalúan «Comunicación oral», y leer se nota.
- **Señalar / Nota** — qué apuntar en pantalla, o el riesgo típico de esa lámina.

**Mazos** (fuente HTML y PDF en `../slides/semana-N/`):

| Semana | Mazo | Láminas | Video |
|---|---|---|---|
| 1 | `presentacion` — Desafío abierto en CPS | 8 | 3–5 min |
| 2 | `analisis-c4` — Análisis del modelo C4 | 9 | 5–7 min |
| 3 | `presentacion` — Modelado con AO y DSL | 14 | 5–7 min |
| 4 | `presentacion` — Proceso MDD4CPS | 10 | 5–7 min |

> **Regla transversal de las cuatro rúbricas:** el video debe mostrar al expositor
> de forma continua. No se aceptan avatares sintéticos ni narración automática.

## Dónde se juega cada criterio de la rúbrica

Los seis criterios de cada rúbrica no se reparten parejo entre las láminas. Esta
tabla dice **en qué lámina se gana o se pierde cada punto**, para saber dónde
gastar el tiempo cuando el reloj aprieta.

**Semana 2 — Análisis de un lenguaje de modelado**

| Criterio | Lámina que lo sostiene | Riesgo |
|---|---|---|
| Comprensión del lenguaje | 2 (descripción general) · 6 (semántica) | Quedarse en «C4 tiene 4 niveles» sin decir para qué sirve cada uno |
| Identificación de constructos | 3 (sintaxis abstracta) | Listar los constructos sin nombrar las **restricciones** |
| Metamodelo propuesto | **4** | No explicar los tres tipos de flecha; leer las cajas en vez de las relaciones |
| Notación y semántica | 5 (notación) · 6 (semántica) | Describir la notación sin decir por qué es deliberadamente pobre |
| Reflexión crítica | **8** | Quedarse en «ventajas y desventajas» sin fundamentar ni proponer mejoras |
| Comunicación oral | todas | Leer la lámina |

**Semana 3 — Modelado de un CPS mediante AO y DSL**

| Criterio | Lámina que lo sostiene | Riesgo |
|---|---|---|
| Modelado AO (iStar) | **4** (el modelo) · 5–7 (paso a paso) | Describir el modelo sin mostrarlo |
| Uso de constructos iStar | 5 · 6 · 7 | Omitir NeededBy o Qualification, que son los que menos se recuerdan |
| Representación en DSL | **11** (el modelo DSL) · 10 (constructos) | Mostrar solo la tabla de constructos y nunca el modelo |
| Correspondencia AO–DSL | **12** | Enumerar los pares sin justificar **por qué** cada uno |
| Análisis y explicación | **13** | Describir la traducción sin decir qué se pierde en ella |
| Comunicación oral | todas | Perder tiempo en el iStar y llegar apurado al DSL |

> En Semana 3, **cuatro de los seis criterios viven en la segunda mitad del mazo**
> (láminas 10 a 13). Es el error de reparto más fácil de cometer: el modelo iStar
> es lo más vistoso, pero el DSL y la correspondencia son los que puntúan.

## Presupuesto de tiempo

> **Fuente única de los tiempos:** los bloques cronometrados viven en
> `semana-N/guion-video.md`. Esta tabla los resume; si hay que cambiar un tiempo,
> se cambia allá y se refleja aquí — nunca al revés, y nunca solo en uno de los dos.

**Semana 2 — 9 láminas · total 5:25 · margen sobre ambos límites (5:00–7:00)**

Versión compacta: las tres láminas "C4 aplicado a SVIF" (antes 7–9) se fusionaron
en una sola (lámina 7), y el resto de los bloques se ajustó un poco para dejar
más aire de habla. Bajó de 6:25 a 5:25 en total.

| Láminas | Bloque | Tiempo |
|---|---|---|
| 1 | Presentación y elección del lenguaje | 20 s |
| 2 | Descripción general | 40 s |
| 3 | Sintaxis abstracta | 40 s |
| 4 | **Metamodelo** | 50 s |
| 5 | Sintaxis concreta | 35 s |
| 6 | Semántica | 30 s |
| 7 | C4 aplicado a SVIF (los 3 niveles, una lámina) | 25 s |
| 8 | **Reflexión crítica** | 70 s |
| 9 | Cierre | 15 s |

**Semana 3 — 14 láminas · total 6:15 · margen 0:45**

| Láminas | Bloque | Tiempo |
|---|---|---|
| 1 | Presentación y encuadre | 25 s |
| 2 | Justificación | 30 s |
| 3–7 | **El modelo iStar** (la 4 lleva ~30 s) | 120 s |
| 8–9 | Trazabilidad y supuestos | 30 s |
| 10 | Por qué hace falta un DSL | 30 s |
| 11–12 | **Modelo DSL y correspondencia** | 65 s |
| 13 | **Análisis: qué se gana y qué se pierde** | 55 s |
| 14 | Cierre | 20 s |

**Si el ensayo se pasa de 7:00**, comprimir en este orden: Semana 2 → la lámina 7
(es ilustración, ya viene compacta); Semana 3 → las láminas 8–9 (ninguna sostiene
un criterio por sí sola). **Nunca** recortar la lámina 8 de Semana 2 ni la 13 de
Semana 3: son los criterios con más recorrido de cada rúbrica.

> **Semana 3 es un mazo denso:** 14 láminas en 6:15 son ~27 s por lámina. El ensayo
> cronometrado no es opcional.

---

# Semana 1 — Seguridad y privacidad en CPS de videovigilancia

**Duración objetivo: 3–5 min.** Es el mazo más corto: ~30 s por lámina de
contenido. El riesgo aquí es quedarse largo en el problema y llegar sin aire a la
reflexión, que es lo que la rúbrica premia.

### Lámina 1 · Portada

**Idea única:** cuál es el desafío abierto elegido y por qué es un desafío *de
CPS*, no de software a secas.

> «El desafío abierto que elegí es la **seguridad y la privacidad en sistemas
> ciberfísicos de videovigilancia con reconocimiento facial**. Lo elegí porque es
> un caso donde la tensión entre los dos objetivos no se puede resolver: mejorar
> uno empeora el otro.»

*Nota:* no más de 20 segundos. La portada no es el lugar para desarrollar.

### Lámina 2 · El problema

**Idea única:** el sistema procesa **datos biométricos**, que son irrevocables.

> «Un sistema de videovigilancia con identificación facial captura y procesa datos
> biométricos. La diferencia con una contraseña es que una contraseña se cambia y
> un rostro no. Si el dato se filtra, el daño es permanente.
>
> Y hay un segundo problema: el sistema toma decisiones que afectan al mundo
> físico —abrir o no abrir una puerta— sobre personas que muchas veces no
> consintieron ser identificadas.»

*Señalar:* si la lámina tiene el diagrama del ciclo percepción-decisión-actuación,
recorrerlo con el cursor.

### Lámina 3 · ¿Por qué es relevante para los CPS?

**Idea única:** en un CPS el ataque **cruza al mundo físico**.

> «Humayed y sus coautores, en el *IEEE Internet of Things Journal* de 2017,
> caracterizan por qué la seguridad en CPS es distinta: aquí un compromiso no
> termina en una filtración de datos, **termina en una puerta abierta**. El
> atacante no roba información, obtiene acceso físico.
>
> A eso se suma que los nodos son dispositivos limitados —poca memoria, poca
> capacidad de cómputo—, así que las defensas criptográficas convencionales no
> siempre caben.»

*Nota:* esta es la lámina que cubre el requisito «≥ 1 artículo que caracterice el
desafío». Nombrar a Humayed explícitamente.

### Lámina 4 · Soluciones en la literatura (1/2)

**Idea única:** se puede reconocer un rostro **sin ver el rostro**.

> «Erkin y coautores, en PETS 2009, proponen *privacy-preserving face
> recognition*: reconocimiento facial mediante criptografía homomórfica. El
> servidor compara plantillas cifradas y obtiene el resultado **sin haber visto
> nunca la imagen**. Es elegante, pero el costo computacional lo hace difícil de
> llevar a un microcontrolador.»

### Lámina 5 · Soluciones en la literatura (2/2)

**Idea única:** el *edge computing* ataca el mismo problema por otro lado.

> «Chen y Ran, en *Proceedings of the IEEE* de 2019, revisan aprendizaje profundo
> sobre *edge computing*. La idea es distinta: en vez de cifrar el dato para
> mandarlo, **no lo mandas**. El reconocimiento ocurre en el propio nodo y lo único
> que sale a la red es el resultado.
>
> Esto reduce la latencia y, sobre todo, achica la superficie de exposición.»

*Nota:* cubre el requisito «≥ 1 artículo que proponga una solución».

### Lámina 6 · Reflexión crítica

**Idea única:** ninguna de las dos soluciones cierra el problema; hay un
**compromiso** que se administra, no se elimina.

> «Mi lectura es que las dos líneas atacan la misma tensión desde extremos
> opuestos, y ninguna la cierra.
>
> El cifrado homomórfico da la garantía más fuerte pero no cabe en el hardware
> típico de un CPS. El procesamiento en el borde sí cabe, pero traslada el
> problema: ahora el dato biométrico vive distribuido en muchos nodos físicamente
> accesibles, cada uno un punto de ataque.
>
> Lo que me llevo es que **la privacidad en CPS es una decisión de arquitectura,
> no una capa que se agrega al final**. Se decide cuando decides dónde ocurre el
> cómputo.»

*Nota:* esta lámina es la que más pesa en la rúbrica. Es la única donde se espera
juicio propio, no resumen. No apurarla.

### Lámina 7 · Cómo se aplica al caso SVIF del curso

**Idea única:** la decisión de arquitectura ya está tomada en el proyecto.

> «Esto no quedó en teoría: en el sistema que desarrollo en el curso, la
> comparación contra los rostros enrolados ocurre **localmente en el nodo**, y por
> la red viaja solo la identidad y un nivel de confianza. **La imagen nunca sale
> del dispositivo.** Es exactamente la línea de Chen y Ran, aplicada.»

*Nota:* esta lámina **no existe** en las versiones Marp del mazo. Si se graba con
aquellas, este bloque queda sin soporte visual.

### Lámina 8 · Referencias

> «Las tres fuentes principales, en APA: Humayed y coautores 2017 para la
> caracterización del desafío; Erkin y coautores 2009 y Chen y Ran 2019 para las
> soluciones. Todas con DOI verificable.»

---

# Semana 2 — Análisis del modelo C4

**Duración objetivo: 5–7 min** (versión compacta: apunta a ~5:25). Nueve láminas
— las tres del ejemplo aplicado a SVIF (antes 7–9) se fusionaron en una sola
lámina 7. Se recorre rápido, es ilustración, no análisis. El peso está en la 4
(metamodelo) y la 8 (reflexión).

### Lámina 1 · Portada

**Idea única:** qué lenguaje se analiza y por qué ese.

> «El lenguaje visual que elegí es el **modelo C4**, de Simon Brown. Lo elegí
> porque es el que se usa de verdad para documentar arquitectura en la industria, y
> porque quería probar hasta dónde sirve para describir un sistema ciberfísico, que
> es el dominio del curso.»

### Lámina 2 · Descripción general

**Idea única:** responder las tres preguntas del enunciado, en orden y sin
saltarse ninguna.

> «**Propósito:** describir la arquitectura mediante mapas jerárquicos. La idea
> central es el *zoom* — cada nivel es un acercamiento del anterior, dirigido a una
> audiencia distinta. El eje es la estructura, pero el modelo también cubre
> comportamiento y despliegue.
>
> **Qué permite representar:** cualquier sistema compuesto por unidades
> desplegables que se comunican. Web, microservicios, integraciones… y también
> sistemas ciberfísicos, donde el **firmware** de cada nodo encaja como contenedor
> —el hardware en sí no tiene elemento propio.
>
> **En qué contexto se usa:** documentación de arquitectura, incorporación de gente
> nueva, revisiones de diseño y conversación con gente no técnica.»

*Señalar:* los cuatro niveles de la tarjeta derecha, nombrándolos: Context,
Container, Component, Code.

### Lámina 3 · Sintaxis abstracta

**Idea única:** seis constructos, una cadena de composición, y reglas que sí
existen.

> «Los constructos son **Person, SoftwareSystem, Container, Component** y
> **Relationship**.
>
> Los cuatro estructurales forman una **cadena estricta de composición**: un
> sistema contiene contenedores, un contenedor contiene componentes, un componente
> contiene unidades de código. Relationship es transversal.
>
> Y hay reglas de buena formación. La más importante: **una relación solo conecta
> el alcance del diagrama**: cada diagrama muestra un solo nivel de zoom. Las
> relaciones, en cambio, **sí cruzan niveles** — una Person se conecta con un
> Container—, llevan descripción y tecnología, y distinguen **síncrono de
> asíncrono**. Y el nivel 4 no tiene elemento en el metamodelo: C4 remite a UML.»

*Nota:* si preguntan por la fuente de estos atributos, están verificados sobre el
código de `structurizr/structurizr` — ver `semana-2/verificacion-de-fuentes.md`.

### Lámina 4 · Metamodelo

**Idea única:** el metamodelo propuesto es un diagrama de clases **correcto**, con
notación UML bien usada.

> «Este es el metamodelo simplificado que propongo.
>
> Arriba, la clase abstracta **Element**, con `name` y `description`, de la que
> heredan los cinco constructos concretos: esas son las flechas de generalización,
> con **triángulo hueco**.
>
> Los **rombos rellenos** son composiciones, con sus cardinalidades: SoftwareSystem
> contiene uno o más Containers y Container puede contener Components. El nivel 4
> aparece punteado y fuera de la jerarquía: no hay elemento para él.
>
> **Relationship** aparece como clase asociativa, con dos extremos navegables
> —`source` y `target`— que apuntan a Element: por eso puede conectar cualquier par.
>
> Y fíjense en la nota de restricción: la regla de que ambos extremos estén en el
> mismo nivel **no la impone el metamodelo**, va aparte. Eso lo retomo en la
> reflexión.»

*Nota:* la rúbrica evalúa «Metamodelo propuesto» como criterio independiente.
Recorrer el diagrama nombrando los tres tipos de flecha es lo que separa un 2 de un
3. Dejar caer el detalle de la restricción prepara el terreno de la lámina 8.

### Lámina 5 · Sintaxis concreta

**Idea única:** la notación no está prescrita — la forma es una opción de estilo.

> «La notación es a propósito mínima. Una **Person** es una figura humana; todo lo
> demás son **cajas** que se distinguen por color y por una etiqueta de tipo entre
> corchetes, como `[Container: ESP32-CAM]`. Las relaciones son flechas dirigidas,
> siempre etiquetadas.
>
> C4 no impone un estándar gráfico: el propio autor insiste en que cualquier
> notación sirve mientras el diagrama tenga leyenda. Eso lo hace facilísimo de
> adoptar. Más adelante voy a decir cuál es el costo.»

### Lámina 6 · Semántica

**Idea única:** el significado de C4 está en **qué abstrae cada nivel**.

> «La semántica de C4 no está en los símbolos, está en los niveles. Cada uno
> responde una pregunta distinta: quiénes rodean al sistema; qué unidades
> desplegables lo componen; qué módulos hay dentro de cada unidad; y con qué código
> se implementan.
>
> Un modelo C4 se interpreta entonces como una **jerarquía de contención con flujos
> de interacción**: dice qué existe, dentro de qué, y quién habla con quién.»

### Lámina 7 · C4 aplicado a SVIF: los tres niveles en una vista

**Idea única:** el mismo sistema con tres zooms — en el nivel 1 el sistema **no se
abre** (regla, no omisión), en el nivel 2 sí aparece la tecnología, y el nivel 3
llega a los módulos internos. Es ilustración, no análisis: recorrer rápido.

> «Lo apliqué a **SVIF**, un control de acceso con identificación facial.
> En **Context** hay dos personas —usuario y administrador— y el sistema como
> **una sola caja**; la cerradura y la alarma van rotuladas como **extensión
> propia**, porque el *System Context* se define sobre personas y otros sistemas
> de software. Fíjense en lo que no está: los dos nodos ESP32 y el broker MQTT
> son contenedores, y aparecen recién en el siguiente nivel.
>
> En **Container** —para mí, el nivel más valioso de C4— el sistema se abre en
> el *Face Monitor* sobre ESP32-CAM y el *Access Actuator* sobre ESP32 con relé
> y buzzer, conectados por MQTT: aquí sí aparece la tecnología.
>
> Y en **Component**, dentro del Face Monitor, la cadena capturar → detectar →
> identificar → publicar, apoyada en la base de rostros enrolados.»

*Nota:* señalar la nota al pie del diagrama de Container. Decir en voz alta por
qué el sistema es caja negra en el nivel 1 es lo que distingue «comprensión
adecuada» de «comprensión profunda» en la rúbrica.

### Lámina 8 · Reflexión personal y crítica

**Idea única:** C4 es adecuado **parcialmente**, y los límites señalan dónde
empieza a hacer falta otro lenguaje.

> «**Ventajas.** Escala en audiencia, es agnóstico de tecnología, y su mayor mérito
> es que **se aprende en diez minutos** — por eso la documentación efectivamente se
> escribe y se mantiene.
>
> **Limitaciones, y aquí conviene ser preciso.** Decir que C4 no describe
> comportamiento sería falso: la *Dynamic view* existe para eso. Lo que no alcanza
> es el dominio: la vista dinámica dice «paso 1, paso 2», no «cada 500
> milisegundos»; la secuencia es lineal, así que el OR —desbloquear o alarmar— no
> se representa; no hay plazos; y **no hay elemento para el mundo físico**, porque
> el *System Context* se define sobre personas y sistemas de software. Y la noción
> de *Container* abarca desde una app web hasta un ESP32 con 2 KB de RAM.
>
> **Qué mejoraría.** Un atributo estándar de periodicidad; estereotipos que
> distingan hardware embebido de servicios; un enlace explícito a los objetivos que
> justifican cada contenedor; y reglas de validación formales, porque hoy —como
> mostré en el metamodelo— la buena formación es convención documentada, no algo
> verificable.
>
> **¿Es adecuado para mi dominio? Sí, pero parcialmente**, y creo que esa es la
> respuesta honesta. El nivel 2 describe SVIF con precisión. Lo que le falta
> —tiempo, hardware, bifurcaciones— es justamente lo que motiva un **DSL propio para
> CPS**. No compiten: C4 aporta contexto y contenedores, el DSL aporta comportamiento
> y temporización.»

*Nota:* «Reflexión crítica» es el criterio con más recorrido de la rúbrica
(«profunda y fundamentada»), y por eso es la lámina con más tiempo asignado de
todo el mazo. Notar cómo la crítica se apoya en la lámina 4: eso es lo que la
vuelve fundamentada y no opinión.

### Lámina 9 · Referencias

> «La fuente principal es Simon Brown, tanto el libro de 2016 como la
> especificación en línea en c4model.com. Complementan Fowler y Parsons 2010 sobre lenguajes
> de dominio específico y Navarro y coautores 2025 para el DSL de CPS que mencioné.»

---

# Semana 3 — Modelado de un CPS mediante AO y DSL

**Duración objetivo: 5–7 min.** Catorce láminas, y **dos modelos que mostrar en
pantalla**. Tener `cim-istar-svif.drawio` y `pim-dsl-svif.drawio` abiertos en
pestañas antes de empezar a grabar — aunque ambos modelos ya están incrustados en
las láminas 4 y 11, así que si algo falla en la demostración en vivo, el mazo se
sostiene solo.

La rúbrica tiene seis criterios y **cuatro de ellos viven en la segunda mitad**
(representación en DSL, correspondencia, análisis, comunicación). No gastar el
tiempo en el iStar.

### Lámina 1 · Portada

**Idea única:** hay dos modelos y una correspondencia entre ellos.

> «Voy a modelar un sistema ciberfísico con **orientación a agentes usando iStar
> 2.0**, y después mostrar cómo esas mismas decisiones se representan en un **DSL
> pensado para CPS**.
>
> El sistema es **SVIF**: control de acceso a un recinto mediante identificación
> facial, con **dos componentes ciberfísicos que colaboran** — un *Face Monitor*
> sobre ESP32-CAM que percibe, y un *Access Actuator* sobre ESP32 que acciona una
> cerradura o una alarma.»

*Nota:* mencionar los dos nodos aquí cubre de entrada la instrucción 2 del
enunciado.

### Lámina 2 · Justificación

**Idea única:** se eligió AO porque hay **objetivos en conflicto**.

> «Elegí orientación a agentes porque en SVIF hay objetivos que entran en
> conflicto: la privacidad de los datos frente a la oportunidad de la
> identificación, y la seguridad del recinto frente al uso de recursos.
>
> La orientación a agentes permite capturar objetivos, responsabilidades y
> dependencias desde etapas tempranas —Cares, Sepúlveda y Navarro, 2019— y eso es
> lo que necesito para razonar sobre esos conflictos antes de escribir código.»

### Lámina 3 · Identificación de actores

**Idea única:** la distinción actor / agente es una decisión, no un detalle.

> «Modelé los dos nodos como **agentes**, porque en iStar 2.0 un agente es una
> instancia concreta con autonomía, y estos son dispositivos físicos específicos. Al
> Administrador de Seguridad lo modelé como **actor** genérico, porque no me
> interesa una persona en particular sino el rol.»

### Lámina 4 · El modelo iStar completo

**Idea única:** aquí está el modelo, y se lee de una forma concreta.

*Los dos límites de actor aparecen lado a lado en la lámina.*

> «Este es el modelo. A la izquierda el límite del **Face Monitor**, a la derecha
> el del **Access Actuator** — cada línea punteada encierra a un agente.
>
> Dentro de cada límite se lee igual: arriba el **objetivo**, refinado hacia abajo
> en **tareas**, y cada tarea apunta a los **recursos** que necesita, con el punto
> relleno del NeededBy.
>
> Las nubes de los costados son los **softgoals**, y hacia ellas llegan las
> contribuciones. La línea que sale por abajo a la izquierda y entra por arriba a
> la derecha, marcada con **D**, es la dependencia — la detallo en un momento.»

*Nota:* orientación de lectura, no análisis — ~30 s dentro del bloque del modelo
iStar. El detalle fino va en el archivo `.drawio` durante el video.

### Lámina 5 · Dependency & Refinement

**Idea única:** la dependencia central, y el refinamiento **OR**.

*Cambiar aquí a `cim-istar-svif.drawio`, vista SD.*

> «**Dependency.** El Access Actuator depende del Face Monitor por el recurso
> *Evento de identificación*: no puede decidir sobre el acceso si nadie identifica a
> la persona. Esta es la dependencia que articula todo el sistema.
>
> **Refinement.** *Monitorear presencia de personas* se refina en **AND** en cuatro
> tareas: capturar imagen, detectar rostro, identificar rostro y publicar el evento.
>
> Y en el actuador, *Gestionar respuesta de acceso* se refina en **OR**:
> desbloquear cerradura **o** activar alarma. Basta una de las dos — y **el modelo
> no dice cuál**. Esa decisión queda deliberadamente abierta en este nivel.»

*Nota:* dejar sembrado que el OR queda abierto: se cobra en la lámina 11.

### Lámina 6 · NeededBy · Qualification · Contribution

**Idea única:** aquí aparecen los **softgoals**, y con ellos el conflicto.

> «**NeededBy** conecta cada tarea con el recurso que necesita: capturar imagen
> necesita el sensor OV2640, desbloquear necesita la cerradura.
>
> **Qualification y Contribution** son lo interesante. *Comparar con rostros
> enrolados* contribuye **help** a *Privacidad de datos personales*, porque el
> reconocimiento ocurre localmente. Y *Publicar evento de identificación* contribuye
> **hurt** a esa misma cualidad, porque transmite datos personales por la red.
>
> Ese conflicto queda **visible en el modelo**. Es exactamente el tipo de tensión
> que la orientación a agentes permite discutir antes de implementar.»

*Señalar:* las dos aristas, help y hurt, llegando al mismo softgoal.

### Lámina 7 · La dependencia que articula SVIF

**Idea única:** las cinco partes de una dependencia iStar.

> «Vale la pena desarmar la dependencia completa, porque tiene cinco partes:
> el **depender** es el Access Actuator; el **dependerElmnt** es *Evaluar
> autorización*, que explica **por qué** existe la dependencia; el **dependum** es
> el *Evento de identificación*, el **qué**; el **dependee** es el Face Monitor; y
> el **dependeeElmnt** es *Publicar evento*, que explica **cómo** se provee.»

### Lámina 8 · Inventario de elementos (cim-*)

**Idea única:** la trazabilidad no es decorativa, es el mecanismo que sostiene
todo lo que viene después.

> «Cada elemento del modelo tiene un identificador estable: 27 en total — tres
> actores, dos objetivos, diez tareas, cinco recursos, cuatro cualidades y tres
> dependums.
>
> No es burocracia: estos IDs son los que van a viajar al modelo DSL en el atributo
> `id_cim_parent`, y de ahí al código. Es lo que me permite preguntar, frente a una
> función en C++, de qué objetivo venía.»

### Lámina 9 · Lo que el modelo asume (y deja abierto)

**Idea única:** distinguir lo decidido de lo diferido es parte del método.

> «Dos cosas quedan **cerradas**: que los nodos son agentes y el humano es actor, y
> que las cualidades se limitan a las cuatro con influencia arquitectónica
> demostrable, para que el modelo siga siendo legible.
>
> Y dos quedan **abiertas a propósito**: el criterio del OR —cuándo desbloquear y
> cuándo alarmar— y los tiempos. Ninguna de las dos pertenece a este nivel.»

### Lámina 10 · El DSL para CPS

**Idea única:** el DSL es un **puente**, y existe por una razón concreta.

> «El modelo de agentes me dice **qué** quiere cada componente y **por qué**. Pero
> si voy a implementar esto sobre Arduino, necesito hablar de hilos, temporizadores,
> funciones y acceso a recursos físicos. Entre el modelo y el código hay una
> distancia considerable.
>
> El DSL es el **puente**: conserva las decisiones del modelo de agentes pero las
> expresa con conceptos fáciles de mapear al software, **todavía sin comprometerse
> con una plataforma**.
>
> Sus constructos son: CP Component, On Interval Action, On Demand Action, HW y SW
> Resource, los operadores AND y OR, y Message Sender y Receiver.»

### Lámina 11 · El modelo DSL completo

**Idea única:** el mismo sistema, dibujado con otros constructos — y la dependencia
por fin es explícita.

> «Este es el modelo DSL, y conviene compararlo con el de recién: **es el mismo
> sistema**. Los dos rectángulos mayores son los **CP Components**; los círculos,
> las **On Interval Actions**; los rectángulos internos, las **On Demand Actions**;
> los cilindros y los cubos, los recursos de software y de hardware.
>
> Y miren el centro: los dos trapecios son el **Message Sender** y el **Message
> Receiver**, unidos por el enlace con el sobre. Lo que en iStar era una
> dependencia abstracta, aquí ya es un canal con un tópico:
> `svif/eventos/identificacion`.»

*Señalar:* pasar el cursor del trapecio izquierdo al derecho siguiendo el sobre.
Es la traducción más visible de todo el mazo.

### Lámina 12 · Correspondencia AO → DSL

**Idea única:** cada constructo iStar tiene su contraparte, y hay una razón para
cada par.

*Cambiar aquí a `pim-dsl-svif.drawio`.*

> «Cada **Agent** pasó a **CP Component**. Los objetivos, que son persistentes y
> requieren verificación continua, pasaron a **On Interval Actions** — y aquí el DSL
> me **obliga** a declarar el período: 500 milisegundos para la percepción, 250 para
> la actuación, porque la respuesta debe ser más reactiva que el muestreo.
>
> Las tareas pasaron a **On Demand Actions**. Los recursos se separaron: el sensor,
> la cerradura y la alarma son **HW Resources**; la base de rostros y la bitácora son
> **SW Resources**. Los refinamientos AND y OR se conservan explícitos.
>
> Y lo más interesante: la **dependencia** se materializó como un **Message Sender**
> en el monitor y un **Message Receiver** en el actuador. En un CPS los componentes
> están distribuidos, así que la delegación entre actores **se convierte en un
> mensaje por la red**.
>
> El dependum pasó a ser la estructura del mensaje: timestamp, person_id,
> person_name, confidence y authorized. Fíjense: transmito la **identidad**, nunca
> la imagen. Esa decisión viene directamente del softgoal de privacidad.»

*Señalar:* el diagrama de la derecha, que muestra la misma dependencia arriba en
iStar y abajo traducida a Sender/Receiver.

### Lámina 13 · Qué se gana y qué se pierde

**Idea única:** la traducción **no es neutra**, y decirlo es el análisis.

> «Al traducir gané información que el modelo de agentes no fijaba: los períodos,
> la estructura de los datos, los parámetros de cada acción.
>
> Pero también **perdí expresividad**, y vale la pena decirlo con honestidad.
>
> Primero, los **softgoals dejaron de ser nodos**. En iStar, la contribución *hurt*
> de publicar el evento sobre la privacidad es una arista que se ve y se discute. En
> el DSL es una entrada dentro de `contribution_array`: sobrevive, pero hay que ir a
> buscarla.
>
> Segundo, la distinción entre **actor, rol y agente** desaparece: los tres colapsan
> en CP Component.
>
> Tercero, el **actor humano** quedó fuera, porque el DSL modela nodos
> computacionales.
>
> Y cuarto —lo que anticipé—, el **criterio del OR** no se expresa: el DSL dice que
> basta una de las dos ramas, pero no bajo qué condición. Eso reaparece recién en el
> código.
>
> No lo veo como un defecto. Cada nivel retiene lo que necesita para la
> transformación siguiente, y `id_cim_parent` es justamente el mecanismo que me deja
> volver al modelo de agentes a recuperar el *porqué*.»

*Nota:* esta es la lámina del criterio «Análisis y explicación». Es la que
distingue una entrega que describe de una que analiza; no recortarla.

### Lámina 14 · Cierre

> «En resumen: modelé SVIF con iStar 2.0 en vistas SD y SR híbrida, con goals,
> softgoals, tasks y resources, y con la dependencia *Evento de identificación*
> entre los dos componentes. Construí la representación equivalente en el DSL y
> establecí la correspondencia elemento por elemento.
>
> Los dos archivos `.drawio` van adjuntos. En la Semana 4 este modelo se transforma
> en código para ESP32.»

---

# Semana 4 — Proceso MDD4CPS

**Duración objetivo: 5–7 min.** Diez láminas y una demostración. Es el mazo con
más material: el riesgo es quedarse en la mecánica de las transformaciones y llegar
sin tiempo al análisis crítico, que es lo que se evalúa.

### Lámina 1 · Portada

> «Voy a mostrar la aplicación del proceso **MDD4CPS** al caso SVIF: cómo el modelo
> de objetivos se transforma en modelo independiente de plataforma, después en
> código específico para ESP32, y cuánto de ese camino se automatiza.»

### Lámina 2 · SVIF y su modelo CIM

**Idea única:** el punto de partida es el modelo de la semana anterior.

> «El punto de partida es el CIM de la Semana 3: dos agentes, la dependencia
> *Evento de identificación*, un refinamiento OR entre desbloquear y alarmar, y
> cuatro softgoals — privacidad, oportunidad y trazabilidad.»

*Señalar:* la vista SD/SR si está incrustada.

### Lámina 3 · Transformación CIM → PIM

**Idea única:** la transformación es **regular**, y lo que agrega el diseñador
está acotado.

> «Las correspondencias son sistemáticas: Agent a CP Component, Goal a On Interval
> Action, Task a On Demand Action, Resource a HW o SW Resource, la dependencia a
> Sender más Receiver, y los softgoals a `qualification_array` y
> `contribution_array`.
>
> Lo que **agrego yo** en esta etapa, y que el CIM no tenía, son los períodos —500 y
> 250 milisegundos—, la estructura del dependum y los parámetros de entrada y salida.
> Nada de eso compromete todavía una plataforma.»

### Lámina 4 · Materialización PIM → PSM

**Idea única:** aquí y **solo aquí** aparece la tecnología.

> «En esta transformación aparece la plataforma: ESP32 con el core de Arduino, y
> MQTT como mecanismo de comunicación.
>
> Cada On Interval Action se convierte en un **hilo FreeRTOS** con su
> `vTaskDelay`. Cada On Demand Action, en una función C++. Los SW Resources, en
> structs tipadas. Los HW Resources, en definiciones de pin. Y el **OR del CIM se
> convierte en un condicional** dentro de `gestionarRespuestaAcceso`.
>
> Fíjense que MQTT no apareció antes: la separación de niveles obligó a postergar
> esa decisión hasta donde correspondía.»

### Lámina 5 · Completado manual y verificación

**Idea única:** hay una **corrida real**, y encontró un error.

> «Lo que completé a mano: credenciales, el umbral de confianza, la política de
> autorización y la simulación de cámara.
>
> Y lo verifiqué de punta a punta contra un broker Mosquitto: detección,
> identificación local, publicación, evaluación, desbloqueo o alarma, y bitácora.
> Catorce eventos: diez desbloqueos y cuatro alarmas.
>
> Y ahí apareció un hallazgo que vale la pena contar: con la regla sintética
> inicial, **la rama de alarma nunca se ejercitaba**. El sistema parecía funcionar
> porque el camino feliz funcionaba. Lo corregí y adopté como criterio de aceptación
> que **ambas ramas del OR queden cubiertas**.»

*Nota:* este hallazgo es el mejor material del mazo — muestra verificación real, no
declarada. Contarlo entero.

### Lámina 6 · Aplicación de la herramienta `aomdd4cps`

> «Además de mi implementación, corrí la herramienta oficial del proceso sobre el
> mismo modelo, para contrastar. Los artefactos de cada fase quedaron versionados en
> `comparativa-app/`.»

### Lámina 7 · Análisis del código generado

**Idea única:** la cifra, y con qué se compara.

> «Contando como generado el esqueleto estructural —hilos, funciones, structs,
> comunicación y comentarios de trazabilidad— y como personalizado lo que completé
> en la fase Code, el resultado es **alrededor de 78 % generado** sobre unas 627
> líneas.
>
> Es consistente con lo que Navarro y coautores reportan para el caso del
> invernadero en 2025.»

### Lámina 8 · Reflexiones finales

**Idea única:** fortalezas y limitaciones, ambas con evidencia.

> «**Fortalezas.** La trazabilidad es el mayor aporte: pude verificar que la
> decisión de privacidad sobrevive desde el softgoal del CIM hasta un comentario de
> contribución en la función que compara rostros. Y la separación de niveles obligó
> a postergar decisiones donde correspondía.
>
> **Limitaciones.** El DSL no expresa **restricciones temporales duras**: el período
> es un atributo, pero nada verifica que se cumpla. Los softgoals sobreviven solo
> como comentarios, así que la trazabilidad es informativa, no verificable
> automáticamente. Y el criterio del OR hay que reintroducirlo a mano.»

### Lámina 9 · Comparativa final: agente y herramienta

> «Comparando ambos caminos: la herramienta garantiza conformidad con el proceso;
> el desarrollo asistido dio más flexibilidad en la fase Code. Los dos convergen en
> la misma arquitectura, que es la señal de que el proceso es reproducible.»

### Lámina 10 · Entregables

> «Entrego el CIM, el PIM, el código de los dos componentes, la evidencia de la
> corrida y esta presentación. Queda pendiente completar la encuesta de la
> experiencia de modelado.»

---

## Antes de grabar — checklist común

- [ ] Cámara encendida y visible durante **toda** la exposición.
- [ ] PDF del mazo correcto abierto en pantalla completa (los de `slides/`, no las
      versiones Marp antiguas de las Semanas 1 y 4).
- [ ] Semana 3: los dos `.drawio` abiertos en pestañas.
- [ ] Semana 4: la corrida de `evidencia-de-pruebas.md` lista para mostrar.
- [ ] Ensayo cronometrado. Las cuatro rúbricas evalúan comunicación oral; pasarse
      de tiempo obliga a apurar justo la parte que más puntúa, que siempre es la
      reflexión final.
- [ ] Nombrar las fuentes al menos una vez cada una, en voz alta.
