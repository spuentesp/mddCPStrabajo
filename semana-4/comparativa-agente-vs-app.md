# Comparativa del proceso MDD4CPS: agente libre (skill) vs. herramienta `aomdd4cps`

**Contexto.** El desarrollo de SVIF (Semanas 3–4) aplicó el *proceso* MDD4CPS —
la metodología CIM → PIM → PSM → Code de Navarro et al. (2025)— razonando las
reglas de transformación con un agente LLM. Existe además una *herramienta de
software* que implementa ese proceso: el repositorio
[`aomdd4cps`](https://github.com/mdd4cps/aomdd4cps) (transformaciones XSLT +
generador de código en Python).

Este documento compara **las dos vías de ejecución del mismo proceso, sobre el
mismo CIM de SVIF**, con evidencia empírica: la herramienta se ejecutó realmente
sobre `cim-istar-svif.drawio` y se contrastaron sus artefactos con los producidos
por el agente (`pim-dsl-svif.drawio` y `codigo/`).

> **Importante — misma entrada de diseñador en ambas vías.** Para que la
> comparación sea justa, a la herramienta se le suministraron *exactamente* los
> mismos parámetros de diseño que documenta la actividad (períodos 500/250 ms,
> parámetros E/S de las tareas, estructura del *dependum*, tipado concreto
> `unsigned long`/`char[32]`/`float`/`bool`, pines HW). Lo que se compara es la
> **transformación y generación**, no la información de diseño.

---

## 1. Cómo se ejecutó cada vía

### Vía A — Agente libre (skill)
Un agente LLM aplica el proceso interpretando las reglas de transformación y
completando la fase Code. Es el método con que se produjo el `codigo/` de la
entrega. No requiere infraestructura; opera sobre lenguaje natural y edición
directa de los `.drawio`. **Decisión deliberada del agente: preservar el
refinamiento OR del CIM** — la rama «desbloquear ∨ alarmar» sobrevive hasta
el condicional de `gestionarRespuestaAcceso()`; la herramienta oficial, en
cambio, lo descarta al transformar (ver §2.1).

### Vía B — Herramienta `aomdd4cps`
Aplicación web (Flask + SaxonC/XSLT) desplegada con Docker Compose. El pipeline
completo se reprodujo de forma reproducible (scripts en
[`comparativa-app/scripts/`](comparativa-app/scripts/)):

1. **Validación del entorno.** Se reprodujo el caso greenhouse oficial: la
   herramienta regenera su PIM y su PSM **idénticos** a los del repositorio
   (mismo conteo de constructos), confirmando que el despliegue es fiel.
2. **CIM→PIM (SVIF).** Se inyectaron los parámetros del diseñador en el CIM
   (`inject_svif.py`, emulando el formulario "Apply Rules") y se aplicó
   `CIM-PIM.xsl`. El disparador clave es el atributo `is_a_cpc="true"`, que marca
   qué agentes se vuelven CPS Component.
3. **PIM→PSM (SVIF).** Se inyectó el tipado concreto (`inject_psm.py`) y se aplicó
   `PIM-PSM.xsl`, obteniendo el modelo intermedio `<root>/<cpc>/<function>/…`.
4. **PSM→Code (SVIF).** Se ejecutó `psm_to_code-arduinomkr1010.py` sobre el PSM.

Todos los artefactos generados quedan versionados en
[`comparativa-app/`](comparativa-app/).

---

## 2. Resultados por fase

### 2.1 CIM → PIM

| Constructo PIM | App `aomdd4cps` | Agente (`pim-dsl-svif.drawio`) |
|---|---:|---:|
| `cps_component` | 2 | 2 |
| `operational_goal` | 2 | 2 |
| `action` | 10 | 9 |
| `id_cim_type="task"` (en `comm_thread`/`listener_thread`) | 2 | 0 |
| `sw_resource` | 2 | 2 |
| `hw_resource` | 3 | 3 |
| `comm_thread` / `listener_thread` | 1 / 1 | 1 / 1 |
| `and_ref_operator` | **0** | 2 |
| `or_ref_operator` | **0** | **1** |

**Coincidencia estructural alta** en componentes, metas, acciones, recursos y
andamiaje de comunicación. **Divergencia crítica:** la herramienta `aomdd4cps`
**no generó los operadores de refinamiento AND/OR** para SVIF — los descarta
en la transformación CIM→PIM (el atributo `is_a_cpc="true"` no basta para
propagar el refinamiento). La **vía agente (skill), en cambio, preservó el
operador OR** (rama alarma vs. desbloqueo), que se materializa en
`gestionarRespuestaAcceso()` y es verificable ejecutando el sistema.

**Precisión sobre la fila `id_cim_type`.** No significa que el agente omitiera el
atributo de trazabilidad: ambas vías lo escriben en `comm_thread`/`listener_thread`.
La diferencia es el **valor**. La herramienta lo fija en `"task"`, mientras que el
agente lo fija en `"resource"` — coherente con el propio inventario del CIM
(`actividad-modelado-istar.md`, §4), donde `cim-d1` («Evento de identificación»)
está clasificado como **resource (dependum)**, no como task. En ese sentido, el
valor del agente es más fiel a la clasificación iStar del propio modelo que el de
la herramienta.

Este es un punto importante para la actividad: lo que el §3 (iii) de
[`actividad-mdd4cps.md`](actividad-mdd4cps.md) describía como limitación
**general** de MDD4CPS (*«el refinamiento OR pierde semántica en la
transformación»*) es, según la evidencia empírica recogida aquí, una
**limitación específica de la herramienta `aomdd4cps`** — el agente (skill)
sí la preserva.

### 2.2 PIM → PSM

| Constructo PSM (`svif-04-PSM.xml`) | App `aomdd4cps` | Agente (PSM materializado en `codigo/`) |
|---|---:|---:|
| `cpc` (componentes ciberfísicos) | 2 | 2 (Face Monitor / Access Actuator) |
| `function` (acciones de la fase Code) | 10 | 10 (`capturarImagen`, `identificarRostro`, `evaluarAutorizacion`, …) |
| `thread` periódicos | 2 (500 ms / 250 ms) | 2 (`monitorear…Task` 500 ms, `controlar…Task` 250 ms) |
| `hw_resource` | 3 (cámara, cerradura, alarma) | 3 (mismos) |
| `sw_resource` | 2 (enrolados, bitácora) | 2 (`EnrolledFace`, `AccessLogEntry`) |
| `commThread` + `listenerThread` | 1 + 1 (dependum `cim-d1`) | 1 + 1 (mismo) |
| `and_ref_operator` | **0** | 2 |
| `or_ref_operator` | **0** | **1** |
| Compila el código generado | — (target MKR 1010, sintaxis inválida) | sí (ESP32) |

**Lectura.** En PIM→PSM la coincidencia estructural es total en componentes,
funciones, hilos con período, recursos y andamiaje del *dependum*: es la fase
donde la herramienta rinde mejor. La divergencia se mantiene en los operadores
de refinamiento — la herramienta los descartó ya en el PIM, por lo que el PSM
tampoco los refleja. **El agente (skill) los preserva hasta el código**, donde
el condicional de `gestionarRespuestaAcceso()` realiza la rama OR (desbloqueo
∨ alarma) que el CIM especificaba.

### 2.3 PSM → Code

Aquí aparecen las diferencias de fondo. Ambas vías generan la **misma estructura
de archivos** (`<CPC>.ino` + `comm_utils.h` + `secrets.h`), pero:

| Dimensión | App `aomdd4cps` | Agente (`codigo/`) |
|---|---|---|
| **Plataforma objetivo** | ⚠️ **Arduino MKR 1010** (`WiFiNINA.h`, `FreeRTOS_SAMD21.h`) | ✅ **ESP32-CAM** (`esp_camera`, `xTaskCreatePinnedToCore`) |
| **¿Compila?** | ❌ **No.** `char[32] person_id;` (sintaxis C++ inválida ×6); identificadores con acentos (`eventoDeIdentificación_…`) | ✅ Verificado punta a punta con broker MQTT real |
| **Líneas `.ino`** | 622 | 427 |
| **Cuerpos de función** | 22 *stubs* `// Your code goes here` | Lógica implementada (`SIMULATION_MODE`, política de autorización, rama OR) |
| **Struct del *dependum*** | Campos + tipos concretos ✅ (con error de sintaxis) | Campos + tipos concretos ✅ (válidos) |
| **Hilos FreeRTOS + períodos** | ✅ | ✅ |
| **Andamiaje MQTT** | ✅ (tópico auto-derivado del id del modelo) | ✅ |
| **Trazabilidad** | Comentarios `CPC ID` / `Thread ID cim-g1` | Comentarios `Qualification/Contribution Array` con `cim-q1`/`cim-q2` |
| **Buenas prácticas** | `secrets.h` con credenciales en claro | `secrets.h.example` + README |

> El código de la herramienta es **andamiaje de calidad estructural, pero no
> compila y apunta a otra placa** (MKR 1010, incompatible con la cámara OV2640
> del caso). Para llegar a un binario funcional habría que: corregir la sintaxis
> de los `struct`, renombrar identificadores acentuados, **portar de SAMD21 a
> ESP32**, y rellenar los 22 *stubs*.

---

## 3. Lectura para el grado de automatización

La actividad estima ~78 % "generado". La ejecución real matiza esa cifra:

- **Lo que mide bien:** el *volumen de andamiaje* estructural (hilos, funciones,
  structs, comunicación, trazabilidad) sí ronda ese porcentaje y la herramienta
  lo produce de forma determinista.
- **Lo que oculta:** ese andamiaje **no es código funcional**. El 100 % de la
  lógica de negocio queda en *stubs*, y el andamiaje de la herramienta **ni
  siquiera compila** sin retoques. "% generado" mide *cantidad de esqueleto*, no
  *código utilizable*.

---

## 4. Síntesis: fortalezas de cada vía

| Criterio | Gana | Por qué |
|---|---|---|
| **Determinismo / reproducibilidad** | **App** | XSLT puro: misma entrada → misma salida (greenhouse reproducido idéntico en cada fase). El agente no lo garantiza. |
| **Homogeneidad estructural** | **App** | Las reglas imponen una arquitectura uniforme (hilos + buzón del *dependum*). |
| **Trazabilidad formal** | **Empate** | Ambas propagan `id_cim_parent` y softgoals; en ambas es informativa, no verificable. |
| **Preservación semántica (AND/OR)** | **Agente** | La app descartó los operadores AND y OR en la transformación CIM→PIM (limitación de la herramienta `aomdd4cps`, no del proceso MDD4CPS en abstracto); el agente preservó el OR hasta el código. |
| **Corrección / compilabilidad** | **Agente** | La app genera código que no compila y de plataforma equivocada. |
| **Ajuste de plataforma (ESP32)** | **Agente** | La app solo emite Arduino MKR 1010; el agente apunta al ESP32-CAM del caso. |
| **Cobertura de la fase Code** | **Agente** | El agente completa la lógica; la app la deja como *stubs*. |
| **Esfuerzo de integración manual** | **Agente** | La app exige portar placa + corregir sintaxis + rellenar 22 *stubs*. |
| **Garantías de proceso** | **App** | Trazabilidad y transformación auditables por reglas, no por un modelo probabilístico. |

**Balance.** La herramienta `aomdd4cps` es el patrón de oro en *rigor,
reproducibilidad y homogeneidad* del andamiaje —justamente lo más propenso a error
si se escribe a mano en un CPS grande—, pero en su versión actual produce código
que no compila, descarta la semántica de refinamiento (AND/OR) y emite sólo para
Arduino MKR 1010. El agente libre entrega código correcto, específico de
plataforma (ESP32), verificado punta a punta y con la semántica del OR
preservada, cubriendo la fase Code, pero sin la garantía formal de determinismo
y auditabilidad que da el XSLT. **No son sustitutos: la combinación ideal es
usar la herramienta para el andamiaje
determinista y un agente para completar la fase Code y la semántica que el DSL aún
no expresa.**

---

## 5. Reproducibilidad

```bash
# 1. Desplegar la herramienta
git clone https://github.com/mdd4cps/aomdd4cps.git && cd aomdd4cps/src
docker compose up --build -d          # frontend :5000, backend :3000

# 2. Ejecutar el pipeline SVIF (scripts en comparativa-app/scripts/)
python inject_svif.py cim-istar-svif.drawio svif-01-CIM-UserInputApplied.xml
python drive.py svif-01-CIM-UserInputApplied.xml CIM-PIM.xsl svif-02-PIM.xml
python inject_psm.py  svif-02-PIM.xml svif-03-PIM-PrePSM.xml
python drive.py svif-03-PIM-PrePSM.xml PIM-PSM.xsl svif-04-PSM.xml
python psm_to_code-arduinomkr1010.py svif-04-PSM.xml   # -> output/<CPC>/
```

**Artefactos generados por la herramienta** (evidencia versionada):
- Modelos: [`comparativa-app/modelos/`](comparativa-app/modelos/)
- Código: [`comparativa-app/codigo-generado/`](comparativa-app/codigo-generado/)
- Scripts: [`comparativa-app/scripts/`](comparativa-app/scripts/)

## Referencias

- Navarro, C., Devia, L., Labra Gayo, J. E., & Cares, C. (2025). An agent-oriented
  model-driven development process for cyber-physical systems. *CIbSE 2025*
  (pp. 150–164). SBC.
- Repositorio `aomdd4cps`: https://github.com/mdd4cps/aomdd4cps (CC BY-NC 4.0).
