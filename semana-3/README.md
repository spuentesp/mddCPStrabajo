# Entrega Semana 3 — Modelado de un CPS mediante AO y DSL

**Objetivo de la actividad** (diapositiva «Actividad semanal», Semana 3): aplicar
conceptos de orientación a agentes mediante iStar y analizar cómo las decisiones
arquitectónicas capturadas en dichos modelos pueden representarse posteriormente
utilizando un DSL orientado a sistemas ciberfísicos.

## Entregables declarados

| Entregable (diapositiva) | Estado | Archivo |
|---|---|---|
| Archivo fuente (`.drawio`) del modelo iStar | ✅ | `cim-istar-svif.drawio` |
| Archivo fuente (`.drawio`) del modelo DSL | ✅ | `pim-dsl-svif.drawio` |
| Presentación utilizada en la exposición (PDF o PowerPoint) |  ✅ 14 diapositivas, con ambos modelos incrustados | `../slides/semana-3/presentacion.pdf` |
| Video individual de 5–7 min | ⬜ Grabar (guion cronometrado listo) | `guion-video.md` |

## Instrucciones cubiertas

| Instrucción (diapositiva) | Dónde se responde |
|---|---|
| Seleccione un CPS de su interés | SVIF — `../recursos-comunes/diseno-del-sistema.md` |
| Identifique al menos **dos componentes ciberfísicos (nodos)** que colaboren | *Face Monitor Component* y *Access Actuator Component* — `actividad-modelado-istar.md`, §2 |
| Modele los actores y sus dependencias mediante una **vista SD o híbrida SD/SR** | `cim-istar-svif.drawio`: páginas «SD - Dependencias Estrategicas» y «SR - Vista hibrida SD-SR» |
| Incorpore **Goals, Softgoals, Tasks y Resources** | `actividad-modelado-istar.md`, §3 y §4 (inventario de 27 elementos) |
| Identifique **al menos una dependencia** entre los actores | «Evento de identificación» (cim-d1) — `actividad-modelado-istar.md`, §4 |
| Construya una **representación equivalente** con la biblioteca DSL | `pim-dsl-svif.drawio` |
| Explique **cómo los principales elementos del modelo AO fueron representados en el DSL** | `actividad-modelado-istar.md`, §5 (tabla de correspondencia, instancias y análisis de la traducción) |

## Cobertura de la rúbrica

| Criterio de la rúbrica | Evidencia |
|---|---|
| Modelado AO (iStar) | `cim-istar-svif.drawio`, dos vistas; modelo incrustado en la lámina 4 |
| Uso de constructos iStar | Paso a paso Dependency → Refinement → NeededBy → Qualification → Contribution, documentado en §3 |
| Representación en DSL | `pim-dsl-svif.drawio`, incrustado en la lámina 11; CP Component, On Interval/On Demand Action, HW/SW Resource, AND/OR, Message Sender/Receiver |
| Correspondencia AO–DSL | §5 y §5.1: tabla constructo-a-constructo e instancias `cim-*` → `pim-*`; lámina 12 |
| Análisis y explicación | §5.2: qué se gana y qué se pierde en la traducción; lámina 13 |
| Comunicación oral | `guion-video.md` |

## Cómo abrir los modelos

app.diagrams.net → **File → Open** → el `.drawio` correspondiente.
Las bibliotecas de símbolos están en `../recursos-comunes/librerias-drawio/`
(**File → Open Library**): `scratchpad_istar2.0.xml` para el modelo iStar y
`scratchpad_pimdsl.xml` para el modelo DSL.

> **Nota sobre la Semana 4.** El mismo modelo DSL es el insumo del proceso MDD4CPS,
> por lo que `semana-4/pim-dsl-svif.drawio` es una copia de este archivo, igual que
> `semana-4/cim-istar-svif.drawio` lo es del modelo iStar. Cada carpeta queda
> autocontenida y puede entregarse por separado.

**Guion hablado lámina por lámina:** `../recursos-comunes/guion-de-presentaciones.md`.

**Verificación de fuentes:** `../semana-2/verificacion-de-fuentes.md` (sección
final) — terminología del DSL PIM verificada contra la biblioteca del curso y el
XML generado por la herramienta oficial `mdd4cps/aomdd4cps` sobre el propio CIM
del proyecto.
