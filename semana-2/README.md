# Entrega Semana 2 — Análisis de un lenguaje de modelado

**Objetivo de la actividad** (diapositiva «Actividad semanal», Semana 2): analizar
un lenguaje de modelado visual utilizado en un contexto profesional o de interés
personal, identificando sus principales constructos, relaciones, restricciones y
mecanismos de representación.

**Lenguaje elegido: el modelo C4** (Simon Brown). El enunciado admite «lenguajes
específicos de alguna herramienta o dominio» además de UML, BPMN, SysML y E-R; C4
califica en esa categoría, es de uso profesional extendido y permite una reflexión
crítica genuina al confrontarlo con el dominio CPS del curso.

## Entregables declarados

| Entregable (diapositiva) | Estado | Archivo |
|---|---|---|
| Archivo de presentación utilizado en la exposición | ✅ 11 diapositivas | `../slides/semana-2/analisis-c4.pdf` (fuente: `.html`) |
| Video individual de 5–7 min | ⬜ Grabar (guion cronometrado listo) | `guion-video.md` |

## Aspectos exigidos por el enunciado

| Aspecto (diapositiva) | Diapositiva | Cubierto |
|---|---|---|
| **Descripción general**: propósito, qué sistemas representa, contexto de uso | 2 | ✅ las tres preguntas respondidas explícitamente |
| **Sintaxis abstracta**: constructos, cómo se relacionan, restricciones | 3 | ✅ 6 constructos + cadena de composición + 6 reglas de buena formación |
| **Metamodelo**: representación simplificada mediante **diagrama de clases** | 4 | ✅ clase abstracta `Element`, generalizaciones, composiciones con cardinalidad, `Relationship` como clase asociativa |
| **Sintaxis concreta**: representación visual de los constructos | 5 | ✅ notación de cada elemento y de las relaciones |
| **Semántica**: significado de los constructos, cómo interpretar los modelos | 6 (+ 7–9 aplicado a SVIF) | ✅ qué abstrae cada nivel, ilustrado en los niveles 1–3 |
| **Reflexión personal**: ¿adecuado para su dominio?, ventajas y limitaciones, ¿qué mejoraría? | 10 | ✅ las tres preguntas respondidas |

## Cobertura de la rúbrica

| Criterio de la rúbrica | Evidencia |
|---|---|
| Comprensión del lenguaje | Diapositiva 2 (propósito, alcance, contexto) |
| Identificación de constructos | Diapositiva 3 (constructos, relaciones y restricciones) |
| Metamodelo propuesto | Diapositiva 4 (diagrama de clases con notación UML correcta) |
| Notación y semántica | Diapositivas 5 y 6, aplicadas en 7–9 |
| Reflexión crítica | Diapositiva 10 (ventajas, limitaciones y mejoras propuestas) |
| Comunicación oral | `guion-video.md` |

## Material puente (no evaluado)

Instanciación de los conceptos de la clase —modelo, metamodelo, DSL y MDD— en el
caso de estudio del proyecto, como preparación para las Semanas 3 y 4:

| Contenido | Archivo |
|---|---|
| Modelo/metamodelo/metametamodelo, DSL y MDD aplicados a SVIF | `fundamentos-de-modelado.md` |
| Diapositivas puente | `../slides/semana-2/presentacion.html` |
| Resumen de la materia de la semana | `../slides/semana-2/materia.html` |

> El análisis alternativo del **DSL PIM para CPS** quedó archivado en
> `../slides/semana-2/analisis-dsl.html`. Se descartó como entrega porque el DSL se
> analiza en profundidad en las Semanas 3 y 4; C4 permite una reflexión crítica más
> independiente.
