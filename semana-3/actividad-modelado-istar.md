# Actividad Semana 3 — Modelado de SVIF mediante orientación a agentes (iStar 2.0) y DSL para CPS

**Objetivo de la actividad:** aplicar conceptos de orientación a agentes mediante
iStar y analizar cómo las decisiones arquitectónicas capturadas en dichos modelos
pueden representarse posteriormente utilizando un DSL orientado a sistemas
ciberfísicos.

**Entregables de esta carpeta:**

| Entregable | Archivo |
|---|---|
| Archivo fuente del modelo iStar | `cim-istar-svif.drawio` (páginas: vista SD y vista híbrida SD/SR) |
| Archivo fuente del modelo DSL | `pim-dsl-svif.drawio` |
| Presentación | `../slides/semana-3/presentacion.html` (+ `.pdf`) |
| Video individual 5–7 min | guion en `guion-video.md` |

Ambos modelos se construyeron con las bibliotecas de símbolos del curso para
diagrams.net (*scratchpad iStar 2.0* y *scratchpad PIM-DSL*), disponibles en
`../recursos-comunes/librerias-drawio/`.

**El CPS seleccionado** es SVIF, con **dos componentes ciberfísicos que colaboran**:
*Face Monitor Component* (percepción) y *Access Actuator Component* (actuación).

## 1. Justificación del paradigma

SVIF involucra componentes de software y hardware que interactúan de manera
distribuida y persiguen objetivos que pueden entrar en conflicto (privacidad de los
datos frente a oportunidad de la identificación; seguridad del recinto frente a
eficiencia de recursos). La orientación a agentes permite capturar objetivos,
responsabilidades y dependencias desde etapas tempranas (Cares, Sepúlveda y
Navarro, 2019), y iStar 2.0 (Dalpiaz, Franch y Horkoff, 2016) provee los constructos
necesarios: actores, agentes y roles; objetivos, tareas, recursos y cualidades; y
enlaces de dependencia, refinamiento, *needed-by*, calificación y contribución.

## 2. Identificación de actores

| Actor | Tipo iStar | Justificación |
|---|---|---|
| Face Monitor Component | **Agente** | Entidad concreta (nodo ESP32-CAM) con autonomía para percibir y decidir |
| Access Actuator Component | **Agente** | Entidad concreta (nodo ESP32) que actúa sobre el mundo físico |
| Administrador de Seguridad | **Actor** | Interesado humano; depende del sistema para mantener el recinto controlado |

## 3. Aplicación del paso a paso sugerido

1. **Dependency (vista SD).** El Administrador de Seguridad depende del Access
   Actuator Component para el objetivo **«Acceso controlado al recinto»** y para el
   recurso **«Registro de accesos»**. A su vez, el Access Actuator Component
   depende del Face Monitor Component para el recurso **«Evento de
   identificación»**: no puede decidir sobre el acceso sin que alguien perciba e
   identifique a la persona.
2. **Refinement.** En la vista SR, el objetivo «Monitorear presencia de personas»
   se refina (AND) en las tareas «Capturar imagen», «Detectar rostro», «Identificar
   rostro» y «Publicar evento de identificación»; «Identificar rostro» se refina en
   «Comparar con rostros enrolados». En el actuador, «Controlar acceso al recinto»
   se refina (AND) en «Evaluar autorización», «Gestionar respuesta de acceso» y
   «Registrar evento de acceso»; y «Gestionar respuesta de acceso» se refina
   (**OR**) en «Desbloquear cerradura» y «Activar alarma»: cualquiera de las dos
   satisface la gestión de la respuesta, según el resultado de la autorización.
3. **NeededBy.** «Capturar imagen» requiere el recurso «Sensor de cámara OV2640»;
   «Comparar con rostros enrolados» requiere la «Base de rostros enrolados»;
   «Desbloquear cerradura» requiere la «Cerradura electromecánica»; «Activar
   alarma» requiere la «Alarma sonora»; «Registrar evento de acceso» requiere la
   «Bitácora de accesos».
4. **Qualification.** La cualidad **«Identificación oportuna»** califica al objetivo
   «Monitorear presencia de personas» (la percepción vale en tanto sea oportuna);
   la cualidad **«Oportunidad de la respuesta»** califica a «Controlar acceso al
   recinto».
5. **Contribution.** «Comparar con rostros enrolados» (procesamiento local en el
   borde) contribuye **help** a «Privacidad de datos personales»; «Publicar evento
   de identificación» contribuye **hurt** a la misma cualidad (transmite datos
   personales por la red, aunque minimizados); «Registrar evento de acceso»
   contribuye **help** a «Trazabilidad de accesos».

## 4. Inventario de elementos y trazabilidad

Los identificadores siguientes se conservan en el PIM mediante `id_cim_parent`
(Semana 4).

| ID | Elemento | Tipo iStar | Actor propietario |
|---|---|---|---|
| cim-a1 | Face Monitor Component | agent | — |
| cim-a2 | Access Actuator Component | agent | — |
| cim-a3 | Administrador de Seguridad | actor | — |
| cim-g1 | Monitorear presencia de personas | goal | cim-a1 |
| cim-t1 | Capturar imagen | task | cim-a1 |
| cim-t2 | Detectar rostro | task | cim-a1 |
| cim-t3 | Identificar rostro | task | cim-a1 |
| cim-t4 | Comparar con rostros enrolados | task | cim-a1 |
| cim-t5 | Publicar evento de identificación | task | cim-a1 |
| cim-r1 | Sensor de cámara OV2640 | resource | cim-a1 |
| cim-r2 | Base de rostros enrolados | resource | cim-a1 |
| cim-q1 | Identificación oportuna | quality | cim-a1 |
| cim-q2 | Privacidad de datos personales | quality | cim-a1 |
| cim-g2 | Controlar acceso al recinto | goal | cim-a2 |
| cim-t6 | Evaluar autorización | task | cim-a2 |
| cim-t7 | Gestionar respuesta de acceso | task | cim-a2 |
| cim-t8 | Desbloquear cerradura | task | cim-a2 |
| cim-t9 | Activar alarma | task | cim-a2 |
| cim-t10 | Registrar evento de acceso | task | cim-a2 |
| cim-r3 | Cerradura electromecánica | resource | cim-a2 |
| cim-r4 | Alarma sonora | resource | cim-a2 |
| cim-r5 | Bitácora de accesos | resource | cim-a2 |
| cim-q3 | Oportunidad de la respuesta | quality | cim-a2 |
| cim-q4 | Trazabilidad de accesos | quality | cim-a2 |
| cim-d1 | Evento de identificación | resource (dependum) | — |
| cim-d2 | Acceso controlado al recinto | goal (dependum) | — |
| cim-d3 | Registro de accesos | resource (dependum) | — |

La dependencia central del sistema queda expresada como:

```
[cim-a2] Evaluar autorización  ──D──►  Evento de identificación  ──D──►  Publicar evento de identificación [cim-a1]
        (dependerElmnt: por qué)            (dependum: qué)                 (dependeeElmnt: cómo)
```

## 5. Representación equivalente en el DSL para CPS

El modelo `pim-dsl-svif.drawio` expresa el mismo sistema con los constructos del
DSL para CPS (Navarro et al., 2025), cuya sintaxis abstracta está pensada para
acercarse a la implementación sin comprometerse aún con una plataforma. La
correspondencia se estableció así:

| Constructo iStar 2.0 (AO) | Constructo del DSL | Fundamento de la correspondencia |
|---|---|---|
| **Agent** | `CP Component` | El CPComponent representa el contenedor computacional de un nodo CPS y se utiliza para representar *Actors*, *Roles* y *Agents* del modelo AO |
| **Goal** | `On Interval Action` | Un objetivo persistente requiere verificación continua; el DSL lo expresa como proceso evaluado periódicamente |
| **Task** | `On Demand Action` | Las tareas son procedimientos concretos activados por un evento o solicitud explícita |
| **Resource** (físico) | `HW Resource` | Sensores, actuadores y módulos de E/S, sin detalles de plataforma |
| **Resource** (informacional) | `SW Resource` | Datos, parámetros y configuraciones; incorpora `data_structure` |
| **Refinement AND / OR** | Operadores `AND` / `OR` | Se conservan explícitamente como operadores de refinamiento del DSL |
| **NeededBy** | `From-To Relation` | Enlace dirigido entre una acción y el recurso que requiere |
| **Dependency** (depender/dependum/dependee) | `Message Sender` + `Message Receiver` + `From-To Message` | En un CPS la delegación entre actores se materializa como intercambio de información por la red |
| **Quality** (softgoal) | `qualification_array` / `contribution_array` | Los softgoals no tienen símbolo propio en el DSL: se preservan como atributos de los elementos que los califican o contribuyen a ellos |

### 5.1 Instancias concretas de la correspondencia

| Elemento AO | ID CIM | Elemento DSL | ID PIM |
|---|---|---|---|
| Face Monitor Component (agent) | cim-a1 | CP Component | pim-fm-00 |
| Access Actuator Component (agent) | cim-a2 | CP Component | pim-aa-00 |
| Monitorear presencia de personas (goal) | cim-g1 | On Interval Action | pim-fm-01 |
| Controlar acceso al recinto (goal) | cim-g2 | On Interval Action | pim-aa-01 |
| Capturar imagen … Comparar con enrolados (tasks) | cim-t1..t4 | On Demand Actions | pim-fm-02..05 |
| Evaluar autorización … Registrar evento (tasks) | cim-t6..t10 | On Demand Actions | pim-aa-02..06 |
| Sensor de cámara OV2640 (resource) | cim-r1 | HW Resource | pim-fm-07 |
| Cerradura electromecánica / Alarma sonora | cim-r3 / cim-r4 | HW Resource | pim-aa-07 / pim-aa-08 |
| Base de rostros enrolados (resource) | cim-r2 | SW Resource | pim-fm-06 |
| Bitácora de accesos (resource) | cim-r5 | SW Resource | pim-aa-09 |
| Refinamiento OR de «Gestionar respuesta» | cim-t7→t8/t9 | Operador `OR` | pim-aa-o1 |
| **Dependencia «Evento de identificación»** | cim-d1 | Message Sender → Message Receiver | pim-fm-08 → pim-aa-10 |

### 5.2 Qué se gana y qué se pierde en la traducción

**Se gana (información que el DSL exige y el CIM no tenía).** El DSL obliga a
declarar `interval_in_milliseconds` en las *On Interval Actions* (500 ms para la
percepción, 250 ms para la actuación), la `data_structure` de los recursos SW y el
`dependum_data_structure` del mensaje. Son decisiones de diseño que el modelo AO
deliberadamente no fijaba, y que aquí deben tomarse porque el DSL está más cerca de
la implementación.

**Se pierde (expresividad del CIM que el DSL no representa gráficamente).**

- Los **softgoals dejan de ser nodos de primera clase**: `Identificación oportuna`,
  `Privacidad de datos personales`, `Oportunidad de la respuesta` y `Trazabilidad
  de accesos` sobreviven únicamente como texto dentro de `qualification_array` y
  `contribution_array`. La contribución **hurt** de «Publicar evento de
  identificación» sobre la privacidad, que en el CIM es una arista visible y
  discutible, en el PIM es un atributo que hay que ir a leer.
- La distinción entre **actor, rol y agente** desaparece: los tres colapsan en
  `CP Component`.
- El **actor humano** (Administrador de Seguridad, cim-a3) no tiene representación
  en el DSL, porque el DSL modela nodos computacionales; sus dependencias (cim-d2,
  cim-d3) quedan fuera del PIM y se convierten en requisitos de interfaz.
- El **criterio del refinamiento OR** no se expresa: el DSL indica que basta uno de
  los hijos, pero no bajo qué condición se elige cada rama. Esa condición se
  reintroduce recién en el código.

Esta pérdida no es un defecto del DSL sino una consecuencia de su propósito: cada
nivel de modelado retiene lo que necesita para la transformación siguiente. La
trazabilidad mediante `id_cim_parent` es precisamente el mecanismo que permite
volver al CIM a recuperar el «porqué» cuando se lo necesita.

## 6. Decisiones de modelado y supuestos

- Se modelan los nodos ciberfísicos como **agentes** (instancias concretas con
  autonomía) y al humano como **actor** genérico, siguiendo la distinción de iStar
  2.0 entre actores, agentes y roles.
- El refinamiento OR en la respuesta de acceso captura una **decisión de diseño
  abierta a nivel CIM**: el modelo no prescribe cuándo desbloquear o alarmar; esa
  lógica se incorporará en fases posteriores (atributo de autorización del evento).
- Las cualidades se limitan a las cuatro con influencia arquitectónica demostrable
  (oportunidad ×2, privacidad, trazabilidad) para mantener el modelo legible; otras
  (eficiencia energética, confiabilidad) se documentan como requisitos en
  `../recursos-comunes/diseno-del-sistema.md`.

## Referencias

- Cares, C., Sepúlveda, S., & Navarro, C. (2019). Agent-oriented engineering for
  cyber-physical systems. *ICITS 2019* (pp. 93–102). Springer.
- Dalpiaz, F., Franch, X., & Horkoff, J. (2016). iStar 2.0 language guide. *arXiv
  preprint arXiv:1605.07767*.
- Navarro, C., Devia, L., Labra Gayo, J. E., & Cares, C. (2025). An agent-oriented
  model-driven development process for cyber-physical systems. *CIbSE 2025*
  (pp. 150–164). SBC.
