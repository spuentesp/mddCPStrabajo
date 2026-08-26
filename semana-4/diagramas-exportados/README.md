# Diagramas exportados (PNG)

Versiones PNG de los modelos `.drawio`, usadas en la presentación
(`slides/semana-4/presentacion.html` → PDF generado por Chromium).

| Archivo | Tamaño | Origen | Página |
|---|---|---|---|
| `cim-istar-svif.png` | 624×900 | `../cim-istar-svif.drawio` | 2 (vista híbrida SD/SR) |
| `pim-dsl-svif.png` | 1603×710 | `../pim-dsl-svif.drawio` | 1 |

El CIM tiene dos páginas: `SD - Dependencias Estratégicas` y
`SR - Vista híbrida SD-SR`. La presentación usa la página 2 (la híbrida),
que muestra ambos agentes con sus metas, tareas y dependencias en una sola vista.

## Cómo regenerar

Ejecutar desde `semana-4/` (el mount de Docker necesita una ruta absoluta;
`$(pwd)` la resuelve sin hardcodear ninguna ruta personal):

```bash
cd semana-4

docker run --rm \
  -v "$(pwd):/data" \
  rlespinasse/drawio-desktop-headless \
  --export --format png --page-index 2 --width 800 --height 1100 \
  --output /data/diagramas-exportados/cim-istar-svif.png \
  /data/cim-istar-svif.drawio

docker run --rm \
  -v "$(pwd):/data" \
  rlespinasse/drawio-desktop-headless \
  --export --format png --page-index 1 --width 1800 --height 800 \
  --output /data/diagramas-exportados/pim-dsl-svif.png \
  /data/pim-dsl-svif.drawio
```
