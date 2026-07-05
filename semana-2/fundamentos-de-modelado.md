# Semana 2 — Modelo, niveles de modelado, metamodelo, DSL y MDD aplicados a SVIF

> La Semana 2 no contempla una actividad evaluada; este documento consolida los
> fundamentos teóricos y los instancia en el caso de estudio SVIF, dejando
> establecido el marco conceptual que sustenta las actividades de las Semanas 3 y 4.

## 1. El modelo como representación con propósito

Un modelo es una representación de la realidad para algún propósito definido
(Pidd, 2000). Entre el sistema y el modelo media la relación *is-represented-by*, y
todo modelo se construye conforme a un paradigma de modelado (Aßmann, Zschaler y
Wagner, 2006). Un modelo útil es abstracto, comprensible, preciso, predictivo y
significativamente más barato que construir el sistema (Selic, 2003).

En SVIF esto se concreta así: antes de escribir una línea de C++, el sistema de
videovigilancia queda representado por modelos que permiten razonar sobre objetivos
en conflicto (privacidad frente a oportunidad de la respuesta), documentar la
arquitectura de dos nodos y comunicar las decisiones al equipo.

## 2. Niveles de modelado en el proyecto

La jerarquía *realidad → modelo → metamodelo → metametamodelo* se instancia en SVIF
de la siguiente forma:

| Nivel | Espacio visual (usado en SVIF) | Ejemplo en el proyecto |
|---|---|---|
| Sistema (realidad) | Recinto con cámara y cerradura | ESP32-CAM vigilando la puerta |
| Modelo | `cim-istar-svif.drawio`, `pim-dsl-svif.drawio` | El agente *Face Monitor Component* con su objetivo «Monitorear presencia de personas» |
| Metamodelo | iStar 2.0 (Dalpiaz, Franch y Horkoff, 2016); metamodelo del DSL PIM del curso | Reglas: una *dependency* conecta depender–dependum–dependee; una *OnIntervalAction* posee `interval_in_milliseconds` |
| Metametamodelo | XML de diagrams.net (mxGraph) | Los modelos se serializan como XML y por ello son transformables con XSLT |

## 3. ¿Por qué un DSL y no solo UML?

UML describe bien clases, objetos, componentes e interacciones, pero el dominio CPS
incorpora conceptos específicos —hilos periódicos, recursos de hardware, mensajes
entre nodos físicos— cuya representación mediante extensiones UML incrementaría la
complejidad del modelado. Un Lenguaje de Dominio Específico (DSL) es un lenguaje
bien definido diseñado para expresar soluciones con conceptos especializados de un
dominio particular (Fowler, 2010; Mernik, Heering y Sloane, 2005), y posee tres
elementos:

| Elemento del DSL | En el DSL PIM para CPS del curso |
|---|---|
| **Sintaxis abstracta** (metamodelo) | Constructos `CPComponent`, `OnIntervalAction`, `OnDemandAction`, `SWResource`, `HWResource`, `MessageSender`, `MessageReceiver`, operadores AND/OR y relaciones from-to |
| **Sintaxis concreta** (notación) | Biblioteca de figuras para diagrams.net (*scratchpad PIM-DSL*) |
| **Semántica** (significado) | Traducción definida hacia estructuras de un lenguaje destino: hilos FreeRTOS, funciones C++, structs y comentarios de trazabilidad en Arduino |

El valor que aporta al dominio justifica su construcción: en SVIF, el DSL permite
expresar «identificar un rostro cada 500 ms y publicar el evento» sin comprometerse
aún con una plataforma.

## 4. MDD: el ciclo de vida como cadena de transformaciones

El Desarrollo Dirigido por Modelos concibe el ciclo de vida del software como una
cadena de transformaciones de modelos (Bézivin, 2005), con dos artefactos
principales: **modelos** y **transformaciones**. Aplicado a SVIF mediante el proceso
MDD4CPS:

```
CIM (iStar 2.0)  ──transformación──►  PIM (DSL CPS)  ──transformación──►  PSM (C++ Arduino)  ──►  Code
   objetivos,                            arquitectura                        hilos, funciones,      credenciales,
   dependencias,                         independiente                       structs generados      lógica específica
   softgoals                             de plataforma
```

Cada transformación incorpora decisiones de diseño que no existían en el nivel
anterior (p. ej., el período de una acción, el tipado de una estructura, la
tecnología MQTT), preservando la trazabilidad mediante identificadores
(`id_cim_parent`). Las Semanas 3 y 4 desarrollan, respectivamente, el CIM y el
resto de la cadena.

## Referencias

- Aßmann, U., Zschaler, S., & Wagner, G. (2006). Ontologies, meta-models, and the
  model-driven paradigm. *Ontologies for Software Engineering and Software
  Technology* (pp. 249–273). Springer.
- Bézivin, J. (2005). On the unification power of models. *Software & Systems
  Modeling, 4*(2), 171–188.
- Dalpiaz, F., Franch, X., & Horkoff, J. (2016). iStar 2.0 language guide. *arXiv
  preprint arXiv:1605.07767*.
- Fowler, M. (2010). *Domain-Specific Languages*. Pearson Education.
- Mernik, M., Heering, J., & Sloane, A. M. (2005). When and how to develop
  domain-specific languages. *ACM Computing Surveys, 37*(4), 316–344.
- Pidd, M. (2000). *Tools for Thinking — Modelling in Management Science*. Wiley.
- Selic, B. (2003). The pragmatics of model-driven development. *IEEE Software,
  20*(5), 19–25.
