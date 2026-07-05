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
> [`recursos-comunes/referencias.md`](recursos-comunes/referencias.md).

SVIF controla el acceso a un recinto mediante dos nodos ciberfísicos que cooperan:

| Nodo (CPC) | Función | Hardware de referencia |
|---|---|---|
| **Face Monitor Component** | Captura imágenes, detecta e identifica rostros contra una base de rostros enrolados y publica eventos de identificación. | ESP32-CAM (sensor OV2640) |
| **Access Actuator Component** | Recibe los eventos, evalúa la autorización y acciona la cerradura o la alarma, registrando cada acceso. | ESP32 + relé + buzzer |

La comunicación entre nodos se realiza mediante **MQTT**. El diseño sigue el proceso
**MDD4CPS**: modelo orientado a agentes (CIM, iStar 2.0) → modelo independiente de
plataforma (PIM, DSL para CPS) → modelo específico de plataforma (PSM, C++ Arduino) →
código personalizado (Code).

## Estructura del repositorio (una carpeta por entrega)

```
.
├── semana-1/                     # ENTREGA 1: desafío abierto en CPS
│   ├── README.md                 #   checklist contra lo pedido en las diapositivas
│   ├── actividad-desafio-abierto.md
│   ├── presentacion.md           #   diapositivas (Marp → PDF/PPTX)
│   └── guion-video.md            #   video 3–5 min
├── semana-2/                     # (sin actividad evaluada; material puente)
│   └── fundamentos-de-modelado.md
├── semana-3/                     # ENTREGA 2: modelado iStar 2.0
│   ├── README.md
│   ├── actividad-modelado-istar.md
│   └── cim-istar-svif.drawio     #   EL MODELO (vistas SD y SD/SR)
├── semana-4/                     # ENTREGA 3: proceso MDD4CPS completo
│   ├── README.md
│   ├── actividad-mdd4cps.md      #   transformaciones + análisis crítico
│   ├── cim-istar-svif.drawio     #   entregable declarado (copia de semana-3)
│   ├── pim-dsl-svif.drawio       #   EL MODELO PIM (DSL para CPS)
│   ├── codigo/                   #   PSM + fase Code (C++ Arduino/ESP32)
│   ├── presentacion.md           #   diapositivas (Marp → PDF/PPTX)
│   ├── guion-video.md            #   video 5–7 min
│   └── evidencia-de-pruebas.md   #   corrida real de punta a punta
└── recursos-comunes/             # Apoyos transversales (no son entregables)
    ├── diseno-del-sistema.md     #   arquitectura del CPS
    ├── referencias.md            #   APA 7 con DOI/URL verificables
    ├── librerias-drawio/         #   bibliotecas de símbolos del curso
    └── herramientas/             #   broker/monitor MQTT y simulador
```

Cada carpeta `semana-N/` es autocontenida: puede comprimirse y entregarse tal
cual. El `README.md` de cada una mapea archivo por archivo contra los
requisitos y la rúbrica de la diapositiva «Actividad semanal» correspondiente.

## Cómo probar el sistema sin hardware

El código incluye un modo de simulación (`SIMULATION_MODE`) que genera detecciones
sintéticas, de modo que el flujo completo (detección → identificación → publicación
MQTT → actuación) puede verificarse con un broker MQTT local y los scripts de
`recursos-comunes/herramientas/`. Véase `semana-4/codigo/README.md`.

## Modelado

Los modelos `.drawio` utilizan las bibliotecas de símbolos del curso
(*scratchpad iStar 2.0* y *scratchpad PIM-DSL*) y pueden abrirse y editarse en
[diagrams.net](https://app.diagrams.net). Los elementos conservan los atributos de
trazabilidad (`id`, `name`, `id_cim_parent`, `qualification_array`,
`contribution_array`, `interval_in_milliseconds`, etc.) requeridos por las
transformaciones del proceso MDD4CPS.
