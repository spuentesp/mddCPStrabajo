# Verificación de las afirmaciones sobre C4 (y, al final, sobre Semanas 3–4)

Registro de qué se afirma en el mazo de la Semana 2, contra qué fuente se
comprobó y con qué resultado. Sirve para defender la presentación si el profesor
pregunta de dónde sale cada dato. La última sección extiende el mismo método a
la terminología del DSL de Semanas 3–4 y a las citas usadas en todo el proyecto.

## Fuentes utilizadas

| Clave | Fuente | Tipo |
|---|---|---|
| **[B16]** | Brown, S. (2016). *Software architecture for developers. Volume 2: Visualise, document and explore your software architecture*. Leanpub. https://leanpub.com/visualising-software-architecture | Primaria (autor de C4) |
| **[SJ]** | Structurizr. *structurizr/structurizr*, paquetes `com.structurizr.model` y `com.structurizr.view`. https://github.com/structurizr/structurizr | Primaria (implementación de referencia del mismo autor) |
| **[C4]** | Especificación en línea https://c4model.com, mantenida por el autor | Primaria |

> **Nota sobre el método.** `c4model.com`, la documentación de Structurizr, arXiv y
> el portal de la SBC están bloqueados por el proxy de red de este entorno. Lo que
> **sí** se pudo leer directamente es el **código fuente del metamodelo** en
> GitHub, que es la implementación de referencia escrita por el propio autor de
> C4. Las afirmaciones marcadas «[SJ] leído» están verificadas contra ese código;
> las marcadas «buscador» proceden de resúmenes de búsqueda y tienen menos peso.

## Afirmaciones estructurales — verificadas sobre el código

| Afirmación en el mazo | Fuente | Evidencia | Estado |
|---|---|---|---|
| Los elementos estructurales son Person, SoftwareSystem, Container y Component | [SJ] leído | Las cuatro clases existen y heredan de `StaticStructureElement` | ✅ |
| Todos heredan atributos `name` y `description` | [SJ] leído | `Element.java`: campos `name`, `description`, `relationships` | ✅ |
| `Relationship` lleva `description` y `technology` | [SJ] leído | `Relationship.java`: campos `source`, `destination`, `description`, `technology` | ✅ |
| `Relationship` distingue **síncrono / asíncrono** | [SJ] leído | `InteractionStyle.java`: `enum { Synchronous, Asynchronous }` | ✅ |
| Un `Container` **puede no tener** componentes | [SJ] leído | `Container.java`: `Set<Component> components` se inicializa vacío; `addComponent()` es opcional | ✅ cardinalidad `0..*` |
| C4 tiene una rama aparte para despliegue | [SJ] leído | `DeploymentNode.java`, con `ContainerInstance`, `InfrastructureNode`, `SoftwareSystemInstance` | ✅ |
| El nivel 4 (*Code*) **no tiene elemento** en el metamodelo | [SJ] leído | No existe `CodeElement.java` en `com.structurizr.model` (404 en *master* y en versiones antiguas); `Component.java` no referencia elementos de código | ✅ |
| Una relación **puede cruzar niveles** (Person → Container) | [SJ] leído | `Relationship` se define entre dos `Element` cualesquiera, sin restricción de tipo | ✅ |
| Jerarquía de clases del metamodelo | [SJ] leído | `ModelItem` (id, tags, url, properties) → `Element` (name, description, relationships) → `GroupableElement` (group) → `StaticStructureElement` → {Person, SoftwareSystem, Container, Component} | ✅ |
| «Externo» **no es un atributo** | [SJ] leído | Ni `Person` ni `SoftwareSystem` tienen campo `external`; la distinción se hace con **tags** (`ModelItem.tags`), que además gobiernan el estilo visual | ✅ |
| Atributos propios reales | [SJ] leído | `Person`: ninguno. `SoftwareSystem`: `containers`. `Container`: `technology`, `components`. `Component`: `technology`. Todo lo demás se hereda | ✅ |
| Existen vistas más allá de los 4 niveles | [SJ] leído | Clases `SystemLandscapeView`, `SystemContextView`, `ContainerView`, `ComponentView`, `DynamicView`, `DeploymentView`, `FilteredView`, `ImageView` | ✅ |
| *System Landscape* se sitúa **por encima** del modelo | [SJ] leído | Javadoc: «Represents a System Landscape view that sits "above" the C4 model» | ✅ |
| C4 **sí modela comportamiento** | [SJ] leído | Javadoc de `DynamicView`: «used to describe behaviour between static elements at runtime»; tiene `SequenceNumber` y `RelationshipView.order` | ✅ |
| El *System Context* trata de personas y otros sistemas de software | [SJ] leído | Javadoc: «showing how a software system fits into its environment, in terms of the users (people) and other software system dependencies» | ✅ |
| *Deployment view* mapea instancias de contenedor a nodos | [SJ] leído | Javadoc: «show the mapping of container instances to deployment nodes» | ✅ |
| Structurizr es la **implementación de referencia** de C4, del mismo autor | [SJ] leído | README de `structurizr/structurizr`: «Structurizr was created by the author of the C4 model and remains the reference implementation» | ✅ |
| Los nombres oficiales de los constructos | [SJ] leído | `Terminology.java` tiene ranuras para `person`, `softwareSystem`, `container`, `component`, `code`, `deploymentNode`, `infrastructureNode`, `relationship` | ✅ *code* **sí** es un nivel nombrado, aunque sin clase en el modelo |
| La notación **no está prescrita**: la forma es una opción de estilo | [SJ] leído | `Shape.java`: 19 valores (Box, RoundedBox, Circle, Ellipse, Hexagon, Diamond, Cylinder, Bucket, Pipe, Person, Robot, Folder, WebBrowser, Window, Terminal, Shell, MobileDevicePortrait, MobileDeviceLandscape, Component) | ✅ |
| Cada caja lleva **nombre, tipo y descripción** | [SJ] leído | `ElementStyle.java`: flags booleanos `metadata` y `description` gobiernan si se muestran la etiqueta de tipo y la descripción | ✅ |
| C4 fue creado por Simon Brown entre **2006 y 2011** | buscador | Coincidente en varias fuentes secundarias | ⚠️ verificado solo por buscador |
| El libro de Brown es de **2016** | buscador | Ficha de Leanpub: 197 pp., noviembre de 2016 | ⚠️ edición Leanpub de actualización continua |

## Errores detectados y corregidos

Todos estaban en versiones anteriores de este mazo:

| Afirmación errónea | Por qué era falsa | Corrección |
|---|---|---|
| «**CodeUnit**» como constructo de C4 | El nombre no existe en ninguna fuente; el nivel 4 no tiene elemento en el metamodelo | Sustituido por «(nivel Code) — sin elemento, C4 remite a UML» |
| «Relationship: `type ∈ {Uses, Sends}`» | Invención. El metamodelo no tiene enumerado de tipo | Sustituido por `description`, `technology`, `interactionStyle` |
| «Una Relationship solo conecta elementos del **mismo nivel** de abstracción» | **Falso.** Las relaciones cruzan niveles con normalidad. La regla real es de **alcance del diagrama**: cada vista muestra un solo nivel de zoom | Reescrita la lista de restricciones |
| «Un Container contiene `1..*` Components» | No es obligatorio | Cardinalidad corregida a `0..*` |
| «Simon Brown (2006–2024)» | Mezclaba creación con vigencia | «entre 2006 y 2011» |
| Referencia a Brown fechada en 2018 | Sin base | 2016 |
| `Person: role, external` | Ninguno de los dos campos existe. `Person` no tiene atributos propios | «sin atributos propios (todo lo hereda)» |
| `SoftwareSystem: external, scope` | Tampoco existen. El único campo propio es `containers` | `containers : Set<Container>` + nota sobre los tags |
| `Container: type : ContainerType` | No existe tal enumerado | `components : Set<Component>` |
| `Component: responsibility` | No existe | «sin más atributos propios» |
| «C4 describe **estructura, no comportamiento**» | **Falso.** La *Dynamic view* existe justamente para describir comportamiento en ejecución, con números de secuencia | Reescrita la crítica: C4 sí modela comportamiento; lo que no expresa es **periodicidad**, **condicionalidad** ni **plazos** |
| «C4 describe la **arquitectura estática**» (lámina 2) | Se contradecía con la corrección de la lámina 10: existe la *Dynamic view* | «La estructura es el eje, pero el modelo también cubre comportamiento y despliegue» |
| «Container: … **nodo físico**» y «los nodos físicos se modelan como contenedores» | Impreciso. Un *Container* es una unidad desplegable y ejecutable —aplicación o almacén de datos—. En un CPS encaja el **firmware** del nodo, no el hardware | Reformulado: el firmware encaja como contenedor; el hardware no tiene elemento propio |
| Citación al repositorio `structurizr/java` | Ese repositorio fue **trasladado**: su README solo dice «The code in this repo has been moved to structurizr/structurizr» | Citación actualizada al repositorio canónico. Verificado que las clases del repo canónico coinciden en contenido con las del espejo |
| «Person: usuario o actor humano» | La definición de C4 es más amplia: «users, actors, roles, personas» | «Usuario, actor, rol o *persona*» |
| La cerradura y la alarma dibujadas como elementos de C4 en el nivel 1 | El *System Context* se define sobre «personas y otros sistemas de software»; un actuador no es ninguna de las dos cosas | Rotuladas «extensión: no es C4», y la carencia pasa a sostener la crítica de la lámina 10 |

## Afirmaciones de juicio (no verificables, y está bien)

Estas son opinión argumentada, no hechos, y así deben presentarse:

- «Hoy es **estándar de facto** en la industria» — apreciación; sostenible por la
  existencia de herramientas propias y soporte en diagrams.net, Miro y Visual
  Paradigm, pero no es un dato medido.
- «Su mayor mérito es que **se aprende en diez minutos**» — juicio propio.
- Todo el contenido de la lámina 10 (ventajas, limitaciones, mejoras propuestas)
  es reflexión personal: la rúbrica pide exactamente eso.

## Lo que esta verificación aportó al mazo

Además de corregir errores, el código fuente reveló un dato **a favor** que no
estaba: `InteractionStyle` distingue comunicación **síncrona de asíncrona**. Es
directamente aplicable a SVIF, donde el canal MQTT entre los dos nodos es
asíncrono, y refuerza la lámina de notación.

## Verificación extendida: terminología del DSL (Semanas 3–4) y citas transversales

Misma exigencia de fuente primaria, aplicada más allá de C4.

### Terminología del DSL PIM — triple confirmación

El repositorio oficial del proceso, [`mdd4cps/aomdd4cps`](https://github.com/mdd4cps/aomdd4cps),
es alcanzable (a diferencia de `c4model.com` o el portal de la SBC) y aporta tres
fuentes independientes para contrastar la terminología usada en `pim-dsl-svif.drawio`
y en las diapositivas de Semanas 3–4:

| Afirmación | Fuente | Resultado |
|---|---|---|
| Los constructos de comunicación se llaman **Message Sender / Message Receiver** | Biblioteca `scratchpad_pimdsl.xml` del curso: shapes con `type="comm_thread"` y `label="message sender"` (ídem `listener_thread`/"message receiver") | ✅ — coincide exactamente |
| El atributo de trazabilidad es **`id_cim_parent`** | `svif-02-PIM.xml`, generado por la herramienta oficial ejecutada sobre el propio CIM del proyecto: `id_cim_parent="cim-g1"`, etc. en cada objeto | ✅ |
| El período se llama **`interval_in_milliseconds`** | Mismo archivo: `interval_in_milliseconds="500"` en los `operational_goal`; confirmado también en la biblioteca del curso | ✅ |

**Nota sobre una fuente descartada.** El documento de proceso del mismo
repositorio (`MDD4CPS_process_overview.md`) usa en su prosa nombres ligeramente
distintos —"Comm Thread"/"Comm Listener" en vez de Message Sender/Receiver,
`cim_parent` y `checkInterval_in_milliseconds` en vez de los atributos reales—.
Se privilegió la evidencia más directa (el propio *schema* usado por la biblioteca
del curso y el XML realmente generado) sobre la prosa descriptiva de ese documento,
que es más laxa. El README del repositorio explica el porqué de la discrepancia:
es una reescritura («revised terminology») de un fork anterior
(`LD-111/MDD4CPS`), y su prosa no siempre se actualizó al mismo ritmo que el
código. Conclusión: **la terminología usada en el proyecto es correcta** y
coincide con la biblioteca de símbolos que el propio curso entrega.

### Corrección encontrada: `comparativa-agente-vs-app.md`

Al cruzar la tabla de conteos de §2.1 contra los archivos reales
(`svif-02-PIM.xml` y `pim-dsl-svif.drawio`), **todos los números coincidían**
exactamente (verificado con `grep -c` sobre ambos archivos). Pero la fila
`task | 2 | —` daba a entender que la vía agente no generó el atributo de
trazabilidad `id_cim_type` en los constructos de comunicación. **Sí lo generó**:
lo fijó en `"resource"` en vez de `"task"`, que es coherente con que el propio CIM
clasifica el dependum `cim-d1` como `resource (dependum)` — no como task. Se
corrigió la fila y se añadió una nota explicando la diferencia de valor.

### Integridad estructural de los cuatro `.drawio`

`cim-istar-svif.drawio` y `pim-dsl-svif.drawio` en Semanas 3 y 4 (4 archivos):

- **XML bien formado** en los cuatro (`xml.etree.ElementTree.parse` sin error).
- **Sin IDs duplicados** dentro de cada página de cada archivo.
- **Sin aristas colgantes**: todo `mxCell` con `edge="1"` tiene su `source` y
  `target` apuntando a un id existente en la misma página.

Relevante porque cualquiera de estos tres problemas puede hacer que el archivo
abra con errores silenciosos en diagrams.net (aristas invisibles, formas
duplicadas que se pisan).

### Citas verificadas contra fuentes (secundarias, vía buscador)

Todas coinciden exactamente con lo escrito en `referencias.md`:

| Cita | Verificado | Coincide |
|---|---|---|
| Humayed, Lin, Li & Luo (2017) | *IEEE IoT Journal*, vol. 4(6), pp. 1802–1831 | ✅ |
| Erkin et al. (2009) | PETS 2009, LNCS 5672, DOI `10.1007/978-3-642-03168-7_14` | ✅ |
| Chen & Ran (2019) | *Proc. IEEE*, vol. 107, pp. 1655–1674, DOI `10.1109/JPROC.2019.2921977` | ✅ |
| Cares, Sepúlveda & Navarro (2019) | AISC vol. 918, pp. 93–102, ICITS 2019, eds. Rocha/Ferrás/Paredes | ✅ |
| Navarro, Devia, Labra Gayo & Cares (2025) | 28.º CIbSE, Ciudad Real, pp. **150–164** | ✅ — página confirmada en esta ronda |

Quedan sin verificar contra fuente primaria (bloqueadas por el proxy: `c4model.com`,
Leanpub, arXiv, portal SBC): el rango exacto 2006–2011 de creación de C4 y el año
2016 del libro de Brown. Ambos coinciden en múltiples fuentes secundarias, pero no
se pudo leer la fuente primaria directamente.

### Ronda adicional: scripts, rutas relativas y una cita más

- **`semana-4/codigo/README.md`**: los comandos de ejemplo usaban
  `../recursos-comunes/herramientas/...`, pero el archivo vive dos niveles
  bajo la raíz (`semana-4/codigo/`), no uno. Verificado con `ls` (la ruta de
  un nivel falla; la de dos niveles existe). Corregido a `../../`.
- **`semana-4/run_demo.sh`**: no hacía `cd` a su propio directorio antes de
  invocar el simulador embebido; ese simulador resolvía la ruta de
  `simular_sistema.py` vía `Path(__file__).parent` (que para un script leído
  por stdin equivale al cwd, no a la ubicación real del script) con un
  fallback hardcodeado a `~/mddCPStrabajo`. Ejecutado tal como lo haría un
  usuario (`cd semana-4 && ./run_demo.sh`), el script fallaba con "No se
  encontró simular_sistema.py". Confirmado el fallo y luego la corrección
  ejecutando la simulación real contra un broker Mosquitto local.
- **`comparativa-app/scripts/{drive,inject_psm,inject_svif}.py`**: revisados
  contra `actividad-mdd4cps.md` y el código Arduino real — intervalos (500/250
  ms), tipos C++ del PSM, y pines `RELAY_PIN`/`BUZZER_PIN` coinciden
  exactamente (`grep` sobre los `.ino`). Sin errores.
- **`semana-1/presentacion.md`, `slides.html`, `guion-video.md`**: citas
  (Humayed 2017, Erkin 2009, Chen & Ran 2019, Lee 2006, Zanero 2017)
  consistentes con `referencias.md`. Sin errores.
- **Wooldridge & Ciancarini — año incorrecto (2000 → 2001):** el paper
  "Agent-oriented software engineering: the state of the art" (LNCS 1957,
  Springer, DOI `10.1007/3-540-44564-1_1`) se publicó en 2001; la página
  oficial de Springer lo confirma. `referencias.md` ya tenía el año correcto,
  pero `slides/semana-3/materia.html` y `recursos-comunes/apuntes-del-curso.md`
  (dos veces) citaban "(2000)". Corregido en las tres ubicaciones.

### Ronda adicional: qué tecnología implementa cada transformación de MDD4CPS

Tres piezas de la materia (`slides/semana-2/materia.html`,
`slides/semana-2/presentacion.html`, `slides/semana-4/materia.html`) y
`recursos-comunes/apuntes-del-curso.md` afirmaban «XSLT (CIM→PIM) y Python
(PIM→PSM)». Se verificó contra la fuente primaria — el documento
`MDD4CPS_repository_structure_and_transformations.md` del propio repositorio
`mdd4cps/aomdd4cps` (`raw.githubusercontent.com`, accesible pese a que
`api.github.com` está bloqueado por el proxy) — y **ambas** transformaciones
CIM→PIM y PIM→PSM se implementan con **XSLT** (`CIM-PIM.xsl`, `PIM-PSM.xsl`);
Python (`psm_to_code-arduinomkr1010.py`) es quien genera el **código** a
partir del PSM (PSM→Code), no quien produce el PSM. Corregido:

- `slides/semana-4/materia.html`: arrows y texto de "Cómo se implementan las
  transformaciones" y de la tarjeta "Herramientas" (Python pasó de PIM→PSM a
  PSM→Code; XSLT pasó a cubrir ambas etapas de modelo a modelo).
- `recursos-comunes/apuntes-del-curso.md` (§4.2): misma corrección.
- `slides/semana-2/materia.html` y `slides/semana-2/presentacion.html`: estos
  dos describen la **cadena concreta de SVIF** (no la herramienta oficial), y
  en SVIF las tres transformaciones las aplicó el diseñador/agente
  directamente sobre los modelos — no se corrió ninguna XSLT ni script Python
  para producir los artefactos entregados. Se relabeled las flechas a
  "agente" y se añadió una nota aclarando que la herramienta oficial
  `aomdd4cps` sí automatiza el proceso con XSLT/Python, para no confundir
  ambos hechos.
