# Guion del video — Semana 2 (5–7 minutos)

**Actividad:** Análisis de un lenguaje de modelado visual.
**Lenguaje analizado:** el **modelo C4** (Simon Brown), aplicado al caso SVIF.
**Formato exigido:** video individual, con el expositor visible de forma continua.
No se aceptan avatares sintéticos ni narración automática.
**Apoyo:** `../slides/semana-2/analisis-c4.pdf` (9 diapositivas).

> Versión compacta: los tiempos suman ≈ 5:25, con margen tanto sobre el piso (5:00)
> como sobre el techo (7:00) del enunciado. Las diapositivas «C4 aplicado a SVIF»
> se fusionaron en una sola lámina (antes 3) para dejar más aire y bajar el ritmo
> de habla. El texto es la línea argumental, no un libreto para leer: la rúbrica
> evalúa «Comunicación oral» y «Comprensión del lenguaje».

---

## 0:00 – 0:20 · Presentación y elección del lenguaje *(diapositiva 1)*

> «El lenguaje visual que elegí analizar es el **modelo C4**, de Simon Brown: se
> usa de verdad para documentar arquitectura en la industria, y quería probar
> hasta dónde sirve para describir un sistema ciberfísico, el dominio del curso.
> Lo analizo en las seis dimensiones pedidas: descripción general, sintaxis
> abstracta, metamodelo, sintaxis concreta, semántica y reflexión crítica.»

---

## 0:20 – 1:00 · Descripción general *(diapositiva 2)*

Responder las tres preguntas del enunciado, sin detenerse en ninguna:

> «**Propósito:** describir la arquitectura de un sistema mediante mapas
> jerárquicos — la idea central es el *zoom*, cada nivel dirigido a una audiencia
> distinta. El eje es la estructura, pero también cubre comportamiento y despliegue.
>
> **Qué representa:** cualquier sistema de unidades desplegables que se comunican.
> En un CPS, el firmware de cada nodo encaja como contenedor; el hardware en sí no
> tiene elemento propio — lo retomo en la reflexión.
>
> **Contexto de uso:** documentación de arquitectura, *onboarding*, revisiones de
> diseño. Los cuatro niveles: Context, Container, Component y Code.»

---

## 1:00 – 1:40 · Sintaxis abstracta *(diapositiva 3)*

> «Los constructos son **Person, SoftwareSystem, Container, Component** y
> **Relationship**. Los cuatro estructurales forman una jerarquía de composición;
> Relationship es transversal, conecta cualquier par **incluso de niveles
> distintos** — una Person con un Container.
>
> La regla central de buena formación **no es sobre las relaciones, es sobre el
> alcance del diagrama**: cada uno muestra un solo nivel de zoom. Un sistema
> externo se modela como caja negra. Y una precisión: el **nivel 4 no tiene
> elemento** en el metamodelo — C4 remite a UML.»

---

## 1:40 – 2:30 · Metamodelo *(diapositiva 4)*

Mostrar el diagrama de clases y recorrerlo — no apurar, es criterio propio de la rúbrica:

> «Este es el metamodelo simplificado que propongo. Arriba, la clase abstracta
> **Element**, de la que heredan los constructos concretos —generalización, con
> triángulo hueco. Los rombos rellenos son **composiciones**: SoftwareSystem
> contiene Containers, Container contiene Components. El **nivel 4 aparece
> punteado y fuera de la jerarquía**.
>
> **Relationship** es una clase asociativa con dos extremos navegables, `source`
> y `target`, ambos apuntando a Element: por eso conecta cualquier par. Y algo
> importante: las relaciones **sí cruzan niveles**; lo que se mantiene por nivel
> es el diagrama. Ninguna de estas reglas la impone una gramática: son
> convenciones — lo retomo en la reflexión.»

---

## 2:30 – 3:05 · Sintaxis concreta *(diapositiva 5)*

> «La notación es deliberadamente pobre: una **Person** es una figura humana; el
> resto son **cajas** que se distinguen por color y una etiqueta de tipo, como
> `[Container: ESP32-CAM]`. Las relaciones son flechas dirigidas y etiquetadas.
>
> La forma es solo una **opción de estilo** —hay diecinueve—, y lo esencial no es
> la forma sino tres datos: **nombre, tipo y descripción**.»

---

## 3:05 – 3:35 · Semántica *(diapositiva 6)*

> «La semántica de C4 no está en los símbolos, está en **los niveles**: cada uno
> responde una pregunta distinta — quiénes rodean al sistema, qué unidades lo
> componen, qué módulos hay dentro, con qué código se implementan. Un modelo C4
> es una **jerarquía de contención con flujos de interacción**.»

---

## 3:35 – 4:00 · C4 aplicado a SVIF *(diapositiva 7)*

Una sola lámina con los tres niveles; ritmo rápido, es ilustración, no análisis.

> «Lo apliqué a **SVIF**. En **Context**, dos personas y el sistema como una sola
> caja — la cerradura y la alarma van rotuladas como extensión propia, no son
> elementos C4. En **Container** —el nivel que más vale de este análisis—, el
> sistema se abre en el *Face Monitor* y el *Access Actuator*, conectados por
> MQTT: aquí aparece la tecnología. Y en **Component**, dentro del Face Monitor,
> la cadena capturar → detectar → identificar → publicar.»

---

## 4:00 – 5:10 · Reflexión crítica *(diapositiva 8)*

Esta es la sección que la rúbrica evalúa como «Reflexión crítica: profunda y
fundamentada». Es la parte que más pesa: no apurarla, aunque el resto vaya rápido.

> «**Ventajas.** Escalable, agnóstico de tecnología, y se aprende en diez minutos
> — por eso la documentación efectivamente se escribe y se mantiene.
>
> **Limitaciones, con precisión.** Decir que C4 no describe comportamiento sería
> falso: la *Dynamic view* existe para eso. Lo que no alcanza es el dominio: no
> hay atributo de período —dice «paso 1, paso 2», no «cada 500 ms»—; el **OR** de
> SVIF no tiene representación porque la secuencia es lineal; no hay plazos ni
> *jitter*; y **no hay elemento para el mundo físico** — el *System Context* se
> define sobre personas y sistemas de software, un sensor no encaja.
>
> **Qué mejoraría:** un atributo de periodicidad, estereotipos de hardware
> embebido, y reglas de validación formales — hoy la buena formación es
> convención, no un metamodelo verificable.
>
> **¿Adecuado para mi dominio? Sí, pero parcialmente.** El nivel 2 describe SVIF
> con precisión. Lo que le falta —tiempo, hardware, bifurcaciones— es justamente
> lo que motiva un **DSL propio para CPS**: no compiten, C4 aporta contexto y
> contenedores, el DSL aporta comportamiento y temporización.»

---

## 5:10 – 5:25 · Cierre *(diapositiva 9)*

> «En síntesis: analicé C4 en sintaxis abstracta, concreta y semántica, propuse
> un metamodelo y lo puse a prueba contra un sistema ciberfísico real. Un
> lenguaje de modelado se juzga por su propósito: C4 cumple el suyo, y sus
> límites señalan justo dónde empieza a hacer falta otro lenguaje.»

---

## Checklist antes de grabar

- [ ] Cámara encendida y visible durante **toda** la exposición.
- [ ] `analisis-c4.pdf` abierto en pantalla completa (9 diapositivas).
- [ ] Duración entre 5 y 7 minutos (medir en un ensayo previo; esta versión apunta
      a ~5:25, con margen de sobra hacia ambos límites).
- [ ] Los dos entregables listos: el video y el archivo de presentación.
- [ ] Nombrar la fuente principal al menos una vez: **Brown, S. (2016)** y la
      especificación en línea, c4model.com. Si preguntan de dónde salen los
      atributos del metamodelo: del código de `structurizr/structurizr`, la
      implementación de referencia del mismo autor.
