---
marp: true
theme: default
paginate: true
size: 16:9
header: "EMI305 · Producción de Software — Sistemas Ciberfísicos"
footer: "Semana 4 · Desarrollo mediante MDD4CPS"
---

<!-- Exportable a PDF/PPTX con Marp: `marp presentacion.md --pdf` -->

# Desarrollo de un CPS mediante MDD4CPS

**Caso de estudio: sistema de videovigilancia con identificación facial (SVIF)**

Actividad Semana 4 — EMI305 · Producción de Software
UFRO, 2026

---

## El caso de estudio y su modelo CIM (iStar 2.0)

- **SVIF**: dos nodos ciberfísicos — *Face Monitor* (ESP32-CAM: captura,
  detecta e identifica rostros) y *Access Actuator* (cerradura o alarma).
- CIM orientado a agentes (semana anterior):
  - agentes con límites; objetivos refinados en tareas (AND) y
    **refinamiento OR**: desbloquear ∨ alarmar;
  - **softgoals**: privacidad de datos, oportunidad, trazabilidad;
  - dependencia central: recurso **«Evento de identificación»**
    (depender: actuador → dependee: monitor).

*(Mostrar `cim-istar-svif.drawio`, vista SD/SR.)*

---

## Transformación CIM → PIM

Correspondencias identificadas automáticamente (trazabilidad `id_cim_parent`):

| CIM (iStar) | PIM (DSL) |
|---|---|
| Agent | CP Component |
| Goal | On Interval Action |
| Task | On Demand Action |
| Resource | SW / HW Resource |
| Dependency | Message Sender + Message Receiver |
| Refinamientos AND/OR | Operadores AND / OR |
| Quality | `qualification_array` / `contribution_array` |

**Decisiones de diseño incorporadas** (independientes de tecnología):
períodos (monitoreo **500 ms**, control **250 ms**), parámetros E/S de las
acciones y estructura del *dependum* (`timestamp`, `person_id`, `person_name`,
`confidence`, `authorized`) — identidad sí, imagen **nunca** (privacidad).

---

## Transformación PIM → PSM

**Decisiones de esta etapa:** plataforma **Arduino/ESP32**, comunicación
**MQTT**, tipado concreto de las estructuras.

| PIM | PSM (código generado) |
|---|---|
| CP Component | Unidad de despliegue: `.ino` + `comm_utils.h` + `secrets.h` |
| On Interval Action | Hilo FreeRTOS con `vTaskDelay(pdMS_TO_TICKS(500))` |
| On Demand Action | Función C++ con bloque de trazabilidad |
| Sender / Receiver | Hilos MQTT con la struct del *dependum* |
| SW Resource | `struct` tipada (`EnrolledFace`, `AccessLogEntry`) |
| HW Resource | Comentario de integración + pin (`RELAY_PIN`, `BUZZER_PIN`) |
| OR del CIM | Condicional en `gestionarRespuestaAcceso()` |
| Softgoals | Comentarios `Qualification/Contribution Array` |

---

## Fase Code y verificación

- Completado manualmente: credenciales (`secrets.h`), umbral de confianza,
  política de autorización, simulación de cámara (`SIMULATION_MODE`).
- **Ejecución de punta a punta** contra broker Mosquitto:
  detección → identificación local → publicación MQTT → evaluación →
  **desbloqueo o alarma** → bitácora (14 eventos: 10 desbloqueos, 4 alarmas).
- Hallazgo de verificación: la rama de **alarma no se ejercitaba** con la
  regla sintética inicial → corregida (cobertura de ambas ramas del OR como
  criterio de aceptación).

*(Demostración en vivo o captura de `evidencia-de-pruebas.md`.)*

---

## Automatización y análisis crítico

**Generado vs. personalizado:** ≈ **78 %** del código fue generado
(consistente con lo reportado para el caso del invernadero; Navarro, Devia,
Labra Gayo & Cares, 2025).

**Fortalezas:** trazabilidad softgoal → código; decisiones postergadas al
nivel correcto; andamiaje homogéneo de hilos y comunicación.

**Limitaciones:** sin restricciones temporales duras en el DSL; softgoals solo
como comentarios; el criterio del OR se reintroduce a mano; herramienta en
versión alfa (ajustes manuales en diagrams.net).

---

## Referencias

- Bézivin, J. (2005). On the unification power of models. *Software & Systems
  Modeling, 4*(2), 171–188.
- Dalpiaz, F., Franch, X., & Horkoff, J. (2016). iStar 2.0 language guide.
  *arXiv:1605.07767*.
- Navarro, C., Devia, L., Labra Gayo, J. E., & Cares, C. (2025). An
  agent-oriented model-driven development process for cyber-physical systems.
  *CIbSE 2025* (pp. 150–164). SBC.
- Repositorio MDD4CPS: https://github.com/mdd4cps/aomdd4cps
