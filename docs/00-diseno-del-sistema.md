# SVIF: diseño de un sistema ciberfísico de videovigilancia con identificación facial

## 1. Motivación y alcance

Los sistemas ciberfísicos (CPS) integran hardware distribuido controlado por software
distribuido con el propósito de controlar procesos físicos (Cares, Sepúlveda y
Navarro, 2019). El presente proyecto materializa dicho concepto en un caso de estudio
deliberadamente acotado: **SVIF**, un sistema de videovigilancia que controla el
acceso físico a un recinto mediante identificación facial.

El alcance se restringió con dos criterios: (i) que el sistema exhiba los cuatro
elementos constitutivos de un CPS —sensores, actuadores, cómputo y comunicaciones—
y (ii) que sea íntegramente verificable con hardware de bajo costo (ESP32) o, en su
defecto, mediante simulación, sin sacrificar la validez del proceso de ingeniería.

## 2. Descripción funcional

El sistema opera según el ciclo cibernético de **percepción, decisión y actuación**:

1. **Percepción.** Un nodo con cámara (ESP32-CAM, sensor OV2640) captura imágenes
   periódicamente y detecta la presencia de rostros.
2. **Decisión.** Ante una detección, el nodo compara el rostro con una base de
   rostros enrolados y determina la identidad y su nivel de confianza. El
   procesamiento ocurre **en el borde (edge)**, sin transmitir la imagen fuera del
   nodo, decisión de diseño orientada a la privacidad de los datos personales.
3. **Actuación.** El nodo de cámara publica un *evento de identificación* (MQTT).
   Un segundo nodo evalúa la autorización y, según el resultado, **desbloquea la
   cerradura electromecánica** o **activa la alarma sonora**, registrando el evento
   en una bitácora.

## 3. Arquitectura

Conforme a la organización por capas revisada en el curso (cloud/fog/edge/data
originators), SVIF se despliega principalmente en la capa *edge*, que es donde los
requisitos de tiempo de respuesta son más exigentes:

| Capa | Elemento en SVIF |
|---|---|
| Data originators | Sensor de imagen OV2640; relé de cerradura; buzzer |
| Edge | ESP32-CAM (detección e identificación facial); ESP32 actuador |
| Fog | Broker MQTT en la red local (p. ej., Mosquitto) |
| Cloud (opcional) | Consolidación de bitácoras y administración de enrolados |

### 3.1 Componentes ciberfísicos (CPC)

| CPC | Responsabilidades | Sensores/Actuadores |
|---|---|---|
| **Face Monitor Component** | Capturar imagen; detectar rostro; identificar contra base de enrolados; publicar evento de identificación | Cámara OV2640 |
| **Access Actuator Component** | Recibir eventos; evaluar autorización; desbloquear cerradura o activar alarma; registrar accesos | Relé (cerradura), buzzer (alarma) |

### 3.2 Comunicación

Los CPC intercambian el *dependum* **Evento de identificación** a través de MQTT
(tópico `svif/eventos/identificacion`), con la siguiente estructura de datos:

| Campo | Tipo | Descripción |
|---|---|---|
| `timestamp` | `unsigned long` | Marca de tiempo del evento (ms desde arranque / época) |
| `person_id` | `int` | Identificador del rostro enrolado (−1 si es desconocido) |
| `person_name` | `char[32]` | Nombre asociado al rostro enrolado |
| `confidence` | `float` | Confianza de la identificación (0.0–1.0) |
| `authorized` | `bool` | Verdadero si el rostro pertenece a la lista de autorizados |

## 4. Desafíos de CPS considerados como requisitos

Siguiendo la lectura de los desafíos como requerimientos (Semana 1), el diseño
adopta las siguientes decisiones:

| Desafío | Decisión de diseño en SVIF |
|---|---|
| *Timing predictability* | Identificación y actuación en la capa edge; período de monitoreo de 500 ms; evaluación de acceso cada 250 ms. |
| *Security* (confidencialidad) | La imagen nunca abandona el nodo de cámara; solo se transmite el evento de identificación (minimización de datos). |
| *Safety* | Ante falla de comunicación, la cerradura permanece bloqueada (estado seguro por defecto) y la alarma es accionable localmente. |
| *Reliability* | Registro de todos los eventos en bitácora; reconexión automática de WiFi/MQTT. |
| *Energy efficiency* | Frecuencia de muestreo configurable; el envío de mensajes se limita a eventos con detección efectiva. |
| *Verification problem* | Modo de simulación (`SIMULATION_MODE`) que permite validar el flujo completo sin hardware. |

## 5. Trazabilidad con el proceso MDD4CPS

| Fase | Artefacto en este repositorio |
|---|---|
| CIM (iStar 2.0) | `modelos/cim-istar-svif.drawio` |
| PIM (DSL para CPS) | `modelos/pim-dsl-svif.drawio` |
| PSM (C++ Arduino) | `codigo/FaceMonitorComponent/`, `codigo/AccessActuatorComponent/` |
| Code (personalización) | Secciones `// --- Your code goes here ---` y `secrets.h` |

## Referencias

- Cares, C., Sepúlveda, S., & Navarro, C. (2019). Agent-oriented engineering for
  cyber-physical systems. *International Conference on Information Technology &
  Systems* (pp. 93–102). Springer.
- Lee, E. A. (2015). The past, present and future of cyber-physical systems: A focus
  on models. *Sensors, 15*(3), 4837–4869.
- Marwedel, P., & Engel, M. (2016). Cyber-physical systems: opportunities, challenges
  and (some) solutions. *Management of Cyber Physical Objects in the Future Internet
  of Things* (pp. 1–30). Springer.
- Navarro, C., Devia, L., Labra Gayo, J. E., & Cares, C. (2025). An agent-oriented
  model-driven development process for cyber-physical systems. *CIbSE 2025*
  (pp. 150–164). SBC.
