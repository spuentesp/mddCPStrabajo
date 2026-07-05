# SVIF — Sistema de Videovigilancia con Identificación Facial

**EMI305 · Producción de Software — Sistemas Ciberfísicos (UFRO, 2026)**

Este repositorio contiene el desarrollo integral de las actividades del módulo de
Sistemas Ciberfísicos (CPS), aplicadas sobre un caso de estudio único: **SVIF**, un
sistema ciberfísico de videovigilancia con identificación facial, deliberadamente
acotado para ser sencillo de construir, simular y probar.

## Caso de estudio

> **Sobre el nombre:** *SVIF* (Sistema de Videovigilancia con Identificación
> Facial) es la denominación asignada en este trabajo al caso de estudio; no
> proviene de la literatura. Cumple el mismo rol que el «invernadero
> automatizado» del ejemplo de cátedra de MDD4CPS. Las fuentes reales y
> verificables que sustentan el trabajo están consolidadas en formato APA en
> [`docs/referencias.md`](docs/referencias.md).

SVIF controla el acceso a un recinto mediante dos nodos ciberfísicos que cooperan:

| Nodo (CPC) | Función | Hardware de referencia |
|---|---|---|
| **Face Monitor Component** | Captura imágenes, detecta e identifica rostros contra una base de rostros enrolados y publica eventos de identificación. | ESP32-CAM (sensor OV2640) |
| **Access Actuator Component** | Recibe los eventos, evalúa la autorización y acciona la cerradura o la alarma, registrando cada acceso. | ESP32 + relé + buzzer |

La comunicación entre nodos se realiza mediante **MQTT**. El diseño sigue el proceso
**MDD4CPS**: modelo orientado a agentes (CIM, iStar 2.0) → modelo independiente de
plataforma (PIM, DSL para CPS) → modelo específico de plataforma (PSM, C++ Arduino) →
código personalizado (Code).

## Estructura del repositorio

```
.
├── docs/
│   ├── 00-diseno-del-sistema.md        # Descripción y arquitectura del CPS
│   ├── semana-1/                        # Actividad: desafío abierto en CPS
│   │   ├── actividad-desafio-abierto.md #   Análisis crítico + referencias
│   │   ├── presentacion.md              #   Diapositivas (formato Marp)
│   │   └── guion-video.md               #   Guion del video (3–5 min)
│   ├── semana-2/
│   │   └── fundamentos-de-modelado.md   # Modelo, metamodelo, DSL y MDD aplicados a SVIF
│   ├── semana-3/
│   │   └── actividad-modelado-istar.md  # Actividad: modelado orientado a agentes
│   └── semana-4/
│       ├── actividad-mdd4cps.md         # Actividad: proceso MDD4CPS completo
│       └── guion-video.md               # Guion del video (5–7 min)
├── modelos/
│   ├── cim-istar-svif.drawio            # CIM: modelo iStar 2.0 (vistas SD y SD/SR)
│   └── pim-dsl-svif.drawio              # PIM: modelo en el DSL para CPS
├── codigo/                              # PSM + fase Code (C++ Arduino / ESP32)
│   ├── FaceMonitorComponent/
│   └── AccessActuatorComponent/
└── herramientas/                        # Utilidades de prueba (broker MQTT, inyección de eventos)
```

## Cómo probar el sistema sin hardware

El código incluye un modo de simulación (`SIMULATION_MODE`) que genera detecciones
sintéticas, de modo que el flujo completo (detección → identificación → publicación
MQTT → actuación) puede verificarse con un broker MQTT local y los scripts de
`herramientas/`. Véase `codigo/README.md`.

## Modelado

Los modelos `.drawio` utilizan las bibliotecas de símbolos del curso
(*scratchpad iStar 2.0* y *scratchpad PIM-DSL*) y pueden abrirse y editarse en
[diagrams.net](https://app.diagrams.net). Los elementos conservan los atributos de
trazabilidad (`id`, `name`, `id_cim_parent`, `qualification_array`,
`contribution_array`, `interval_in_milliseconds`, etc.) requeridos por las
transformaciones del proceso MDD4CPS.
