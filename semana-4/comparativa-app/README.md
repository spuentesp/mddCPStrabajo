# Evidencia: SVIF ejecutado por la herramienta `aomdd4cps`

Artefactos reales producidos al correr el pipeline MDD4CPS sobre el CIM de SVIF
con la herramienta oficial ([`aomdd4cps`](https://github.com/mdd4cps/aomdd4cps)),
para respaldar [`../comparativa-agente-vs-app.md`](../comparativa-agente-vs-app.md).

## Contenido

| Carpeta | Qué es |
|---|---|
| `modelos/` | Cadena de modelos de la herramienta: `svif-01-CIM-UserInputApplied` → `svif-02-PIM` → `svif-03-PIM-PrePSM` → `svif-04-PSM` |
| `codigo-generado/` | Código emitido por `psm_to_code-arduinomkr1010.py` (2 CPC, target Arduino MKR 1010) |
| `scripts/` | Automatización del pipeline (emulan los formularios de la app + llaman al backend XSLT) |

## Cómo se reprodujo

```bash
git clone https://github.com/mdd4cps/aomdd4cps.git && cd aomdd4cps/src
docker compose up --build -d          # frontend :5000, backend :3000

# scripts/ (rutas a los .xsl de aomdd4cps/src/frontend/static/input/xsl/)
python inject_svif.py cim-istar-svif.drawio svif-01-CIM-UserInputApplied.xml
python drive.py svif-01-CIM-UserInputApplied.xml CIM-PIM.xsl svif-02-PIM.xml
python inject_psm.py  svif-02-PIM.xml svif-03-PIM-PrePSM.xml
python drive.py svif-03-PIM-PrePSM.xml PIM-PSM.xsl svif-04-PSM.xml
python psm_to_code-arduinomkr1010.py svif-04-PSM.xml
```

- `inject_svif.py` emula el formulario **Apply Rules** (CIM→PIM): inyecta períodos,
  parámetros E/S, estructura del *dependum* y el disparador `is_a_cpc="true"`.
- `inject_psm.py` emula el formulario **PIM→PSM**: inyecta el tipado concreto
  (`unsigned long`/`char[32]`/`float`/`bool`) y las descripciones de integración HW.
- `drive.py` llama al endpoint `POST /transform` del backend (SaxonC/XSLT).

## Advertencias sobre el código generado

- **Plataforma:** Arduino MKR 1010 (`WiFiNINA` + `FreeRTOS_SAMD21`), **no** ESP32.
- **No compila tal cual:** `char[32] person_id;` (sintaxis C++ inválida) e
  identificadores con acentos; los cuerpos de función son *stubs*.

Se conserva sin modificar, a propósito, como evidencia del estado alfa de la herramienta.
