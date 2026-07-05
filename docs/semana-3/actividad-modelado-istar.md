# Actividad Semana 3 — Modelado orientado a agentes de SVIF con iStar 2.0

**Entregable:** modelo CIM en `modelos/cim-istar-svif.drawio`, construido con la
biblioteca de símbolos *scratchpad iStar 2.0* del curso para diagrams.net. El
archivo contiene dos páginas: **Vista SD** (Strategic Dependency) y **Vista híbrida
SD/SR** (Strategic Rationale).

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

## 5. Decisiones de modelado y supuestos

- Se modelan los nodos ciberfísicos como **agentes** (instancias concretas con
  autonomía) y al humano como **actor** genérico, siguiendo la distinción de iStar
  2.0 entre actores, agentes y roles.
- El refinamiento OR en la respuesta de acceso captura una **decisión de diseño
  abierta a nivel CIM**: el modelo no prescribe cuándo desbloquear o alarmar; esa
  lógica se incorporará en fases posteriores (atributo de autorización del evento).
- Las cualidades se limitan a las cuatro con influencia arquitectónica demostrable
  (oportunidad ×2, privacidad, trazabilidad) para mantener el modelo legible; otras
  (eficiencia energética, confiabilidad) se documentan como requisitos en
  `docs/00-diseno-del-sistema.md`.

## Referencias

- Cares, C., Sepúlveda, S., & Navarro, C. (2019). Agent-oriented engineering for
  cyber-physical systems. *ICITS 2019* (pp. 93–102). Springer.
- Dalpiaz, F., Franch, X., & Horkoff, J. (2016). iStar 2.0 language guide. *arXiv
  preprint arXiv:1605.07767*.
