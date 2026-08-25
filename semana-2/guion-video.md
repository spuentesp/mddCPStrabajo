# Guion del video — Semana 2 (5–7 minutos)

**Actividad:** Análisis de un lenguaje de modelado visual.
**Lenguaje analizado:** el **modelo C4** (Simon Brown), aplicado al caso SVIF.
**Formato exigido:** video individual, con el expositor visible de forma continua.
No se aceptan avatares sintéticos ni narración automática.
**Apoyo:** `../slides/semana-2/analisis-c4.pdf` (11 diapositivas).

> Los tiempos suman ≈ 6:20. El texto es la línea argumental, no un libreto para
> leer: la rúbrica evalúa «Comunicación oral» y «Comprensión del lenguaje».

---

## 0:00 – 0:30 · Presentación y elección del lenguaje *(diapositiva 1)*

> «El lenguaje visual que elegí analizar es el **modelo C4**, de Simon Brown. Lo
> elegí porque es el que efectivamente se usa para documentar arquitectura en la
> industria y porque quería comprobar hasta dónde sirve para describir un sistema
> ciberfísico, que es el dominio del curso.
>
> Voy a analizarlo en las seis dimensiones pedidas: descripción general, sintaxis
> abstracta, metamodelo, sintaxis concreta, semántica y una reflexión crítica.»

---

## 0:30 – 1:20 · Descripción general *(diapositiva 2)*

Responder las tres preguntas del enunciado, en orden:

> «**Propósito.** C4 describe la arquitectura estática de un sistema mediante un
> conjunto de mapas jerárquicos. La idea central es el *zoom*: cada nivel es un
> acercamiento del anterior, y cada uno está dirigido a una audiencia distinta.
>
> **Qué permite representar.** Cualquier sistema compuesto por unidades desplegables
> que se comunican: web, microservicios, integraciones… y también sistemas
> ciberfísicos, donde los nodos físicos se modelan como contenedores.
>
> **En qué contexto se usa.** Documentación de arquitectura, incorporación de gente
> nueva al equipo, revisiones de diseño y conversaciones con gente no técnica.
>
> Los cuatro niveles son: **Context**, el sistema y quiénes lo rodean; **Container**,
> las unidades desplegables; **Component**, los módulos dentro de cada unidad; y
> **Code**, las clases y funciones.»

---

## 1:20 – 2:10 · Sintaxis abstracta *(diapositiva 3)*

> «Los constructos principales son seis: **Person**, **SoftwareSystem**,
> **Container**, **Component**, **CodeUnit** y **Relationship**.
>
> Los cuatro estructurales forman una **cadena estricta de composición**: un sistema
> contiene contenedores, un contenedor contiene componentes, un componente contiene
> unidades de código. Relationship es transversal: conecta dos elementos
> cualesquiera.
>
> Y hay **reglas de buena formación**. La más importante: una relación solo puede
> conectar elementos del **mismo nivel de abstracción**. No existe un enlace de
> Container a CodeUnit. Cada diagrama representa un solo nivel; mezclarlos invalida
> el modelo. Además, toda relación es dirigida y debe llevar descripción.»

---

## 2:10 – 3:00 · Metamodelo *(diapositiva 4)*

Mostrar el diagrama de clases y recorrerlo:

> «Este es el metamodelo simplificado que propongo. Arriba está la clase abstracta
> **Element**, con `name` y `description`, de la que heredan los cinco constructos
> concretos —esas son las flechas de generalización, con triángulo hueco.
>
> Los rombos rellenos son **composiciones**: SoftwareSystem contiene uno o más
> Containers, Container contiene uno o más Components, y Component contiene una o
> más CodeUnits. Las cardinalidades están marcadas en rojo.
>
> **Relationship** aparece como una clase asociativa con dos extremos navegables,
> `source` y `target`, ambos apuntando a Element: por eso puede conectar cualquier
> par de elementos. La restricción de que ambos extremos estén en el mismo nivel
> está anotada aparte, porque el metamodelo por sí solo no la impide —y esa es una
> observación que retomo en la reflexión.»

---

## 3:00 – 3:45 · Sintaxis concreta *(diapositiva 5)*

> «La notación es deliberadamente pobre, y eso es una decisión de diseño. Una
> **Person** se dibuja como una figura humana; los demás elementos son **cajas
> rectangulares** que se distinguen por color y por una etiqueta de tipo entre
> corchetes —por ejemplo `[Container: ESP32-CAM]`.
>
> Las **relaciones** son flechas dirigidas, siempre etiquetadas con lo que hacen y,
> cuando corresponde, con la tecnología del canal.
>
> C4 no define un estándar gráfico obligatorio: el propio autor insiste en que
> cualquier notación sirve mientras el diagrama tenga leyenda. Eso lo hace muy fácil
> de adoptar, pero como veremos, tiene un costo.»

---

## 3:45 – 4:45 · Semántica + ejemplo aplicado *(diapositivas 6 a 9)*

> «La semántica de C4 está en **qué significa cada nivel**, y se entiende mejor con
> el caso. Apliqué C4 a **SVIF**, un control de acceso con identificación facial.
>
> En el **nivel 1, Context**, aparece el usuario que intenta acceder, el sistema como
> caja única y el broker MQTT como sistema externo. Es lo que le mostraría a alguien
> que no conoce el proyecto.
>
> En el **nivel 2, Container**, el sistema se abre en sus dos nodos: el *Face
> Monitor* sobre ESP32-CAM y el *Access Actuator* sobre ESP32 con relé y buzzer,
> conectados por MQTT. Aquí aparece la tecnología. Este nivel es, para mí, el más
> valioso: describe la arquitectura real del sistema en un solo diagrama.
>
> En el **nivel 3, Component**, entro en el Face Monitor y veo la cadena capturar →
> detectar → identificar → publicar, más la base de rostros enrolados.
>
> Un modelo C4 se interpreta entonces como una **jerarquía de contención con flujos
> de interacción**: dice qué existe, dentro de qué, y quién habla con quién.»

---

## 4:45 – 6:00 · Reflexión crítica *(diapositiva 10)*

Esta es la sección que la rúbrica evalúa como «Reflexión crítica: profunda y
fundamentada». Es la parte que más pesa: no apurarla.

> «**Ventajas.** Es escalable en audiencia; es agnóstico de tecnología; y su mayor
> mérito es que **se aprende en diez minutos**, lo que hace que la documentación
> efectivamente se escriba y se mantenga.
>
> **Limitaciones, y aquí es donde el dominio importa.** C4 describe **estructura**,
> no **comportamiento**. En SVIF eso significa que:
>
> — no puedo expresar que el monitoreo ocurre **cada 500 ms**;
> — no puedo expresar que la respuesta se bifurca: **desbloquear o alarmar**;
> — el hardware queda como texto libre: no hay forma de decir que el relé está en el
> pin 26;
> — y la noción de *Container* es tan amplia que abarca desde una aplicación web
> hasta un ESP32 con dos kilobytes de RAM.
>
> **Qué mejoraría.** Un atributo estándar de periodicidad; estereotipos que
> distingan hardware embebido de servicios; un enlace explícito a los objetivos que
> justifican cada contenedor; y reglas de validación formales, porque hoy la buena
> formación es convención documentada, no un metamodelo verificable.
>
> **¿Es adecuado para mi dominio?** Sí, pero parcialmente, y creo que esa es la
> respuesta honesta. El nivel 2 describe SVIF con precisión y es la vista que de
> hecho usaría para explicar el sistema. Lo que le falta —tiempo, hardware,
> bifurcaciones— es justamente lo que motiva construir un **DSL propio para CPS**.
> No compiten: C4 aporta contexto y contenedores, el DSL aporta comportamiento y
> temporización.»

---

## 6:00 – 6:20 · Cierre *(diapositiva 11)*

> «En síntesis: analicé C4 en sus tres capas —sintaxis abstracta, sintaxis concreta
> y semántica—, propuse un metamodelo y lo puse a prueba contra un sistema
> ciberfísico real. La conclusión que me llevo es que un lenguaje de modelado se
> juzga por su **propósito**: C4 cumple el suyo, y sus límites señalan exactamente
> dónde empieza a hacer falta otro lenguaje.»

---

## Checklist antes de grabar

- [ ] Cámara encendida y visible durante **toda** la exposición.
- [ ] `analisis-c4.pdf` abierto en pantalla completa.
- [ ] Duración entre 5 y 7 minutos (medir en un ensayo previo).
- [ ] Los dos entregables listos: el video y el archivo de presentación.
- [ ] Nombrar la fuente principal al menos una vez: **Brown, S. (2006–2024),
      c4model.com**.
