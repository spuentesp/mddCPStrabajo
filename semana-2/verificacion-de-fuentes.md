# Verificación de las afirmaciones sobre C4

Registro de qué se afirma en el mazo de la Semana 2, contra qué fuente se
comprobó y con qué resultado. Sirve para defender la presentación si el profesor
pregunta de dónde sale cada dato.

## Fuentes utilizadas

| Clave | Fuente | Tipo |
|---|---|---|
| **[B16]** | Brown, S. (2016). *Software architecture for developers. Volume 2: Visualise, document and explore your software architecture*. Leanpub. https://leanpub.com/visualising-software-architecture | Primaria (autor de C4) |
| **[SJ]** | Structurizr. *structurizr/java*, paquete `com.structurizr.model`. https://github.com/structurizr/java | Primaria (implementación de referencia del mismo autor) |
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
