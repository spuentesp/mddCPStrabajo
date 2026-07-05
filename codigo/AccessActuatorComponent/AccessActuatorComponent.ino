// ============================================================================
// AccessActuatorComponent.ino
// Unidad de despliegue del componente ciberfisico "Access Actuator Component".
// Generado por la transformacion PIM -> PSM del proceso MDD4CPS y completado
// durante la fase Code.
//
// Trazabilidad:
//   PSM  <- PIM: pim-aa-00 (cps_component: Access_Actuator_Component)
//   PIM  <- CIM: cim-a2    (agent: Access Actuator Component)
//
// Plataforma objetivo : ESP32 DevKit (Arduino core, FreeRTOS nativo)
// Comunicaciones      : MQTT (PubSubClient)
// ============================================================================

#include "comm_utils.h"
#include "secrets.h"

// ---------------------------------------------------------------------------
// HW Resource: Rele de cerradura
//   ID: pim-aa-07 | ID CIM Parent: cim-r3 (resource: "Cerradura electromecanica")
//   Integracion (fase Code): rele activo en alto conectado a RELAY_PIN.
//   Estado seguro por defecto: cerradura BLOQUEADA (pin LOW).
// ---------------------------------------------------------------------------
static const int RELAY_PIN = 26;

// ---------------------------------------------------------------------------
// HW Resource: Buzzer de alarma
//   ID: pim-aa-08 | ID CIM Parent: cim-r4 (resource: "Alarma sonora")
//   Integracion (fase Code): buzzer pasivo en BUZZER_PIN.
// ---------------------------------------------------------------------------
static const int BUZZER_PIN = 27;

static const unsigned long UNLOCK_SECONDS = 5;  // fase Code
static const unsigned long ALARM_SECONDS  = 3;  // fase Code

// ---------------------------------------------------------------------------
// SW Resource: Bitacora de accesos
//   ID: pim-aa-09 | ID CIM Parent: cim-r5 (resource: "Bitacora de accesos")
//   Estructura derivada del atributo data_structure del PIM.
// ---------------------------------------------------------------------------
struct AccessLogEntry {
  unsigned long timestamp;    // Momento del acceso
  int           person_id;    // Identidad reportada
  char          action_taken[16]; // "desbloqueo" o "alarma"
  float         confidence;   // Confianza reportada
};
static const int LOG_CAPACITY = 32;
static AccessLogEntry accessLog[LOG_CAPACITY];
static int logCount = 0;

// Buzon del listener (dependum recibido, disponible localmente)
static IdentificationEvent lastEvent;
static volatile bool eventReceived = false;

// ---------------------------------------------------------------------------
// Listener Thread ID: pim-aa-10 | Parent ID: pim-aa-00
// CIM Origin: cim-d1 (dependum: "Evento de identificacion")
// Tipo PIM  : MessageReceiver (listener_thread)
// Descripcion: recibe, deserializa y mantiene disponible localmente el
// dependum recibido desde el Face Monitor Component.
// ---------------------------------------------------------------------------
void eventoIdentificacionReceiverCallback(char* topic, byte* payload,
                                          unsigned int length) {
  Serial.println("===Running Listener 'eventoIdentificacionReceiver'===");
  static char buffer[256];
  unsigned int n = (length < sizeof(buffer) - 1) ? length : sizeof(buffer) - 1;
  memcpy(buffer, payload, n);
  buffer[n] = '\0';
  if (deserializeIdentificationEvent(buffer, &lastEvent)) {
    eventReceived = true;
  } else {
    Serial.println("[receiver] Payload invalido, evento descartado.");
  }
}

// ---------------------------------------------------------------------------
// Function ID: pim-aa-02 | Parent ID: pim-aa-00
// CIM Origin : cim-t6 (task: "Evaluar autorizacion")
// Input Parameters : identification_event -- Evento recibido
// Output Parameters: access_granted -- true si corresponde desbloquear
// ---------------------------------------------------------------------------
bool evaluarAutorizacion(const IdentificationEvent& ev) {
  Serial.println("===Running Function 'evaluarAutorizacion'===");
  // --- Your code goes here ---
  // Politica de la fase Code: autorizado por la base de enrolados Y persona conocida.
  return ev.authorized && ev.person_id >= 0;
}

// ---------------------------------------------------------------------------
// Function ID: pim-aa-04 | Parent ID: pim-aa-03
// CIM Origin : cim-t8 (task: "Desbloquear cerradura")
// Input Parameters : unlock_seconds -- Duracion del desbloqueo
// Hardware Resource Assigned: pim-aa-07 (Rele de cerradura)
// ---------------------------------------------------------------------------
void desbloquearCerradura(unsigned long unlock_seconds) {
  Serial.println("===Running Function 'desbloquearCerradura'===");
  digitalWrite(RELAY_PIN, HIGH);
  vTaskDelay(pdMS_TO_TICKS(unlock_seconds * 1000));
  digitalWrite(RELAY_PIN, LOW);   // retorno al estado seguro (bloqueada)
}

// ---------------------------------------------------------------------------
// Function ID: pim-aa-05 | Parent ID: pim-aa-03
// CIM Origin : cim-t9 (task: "Activar alarma")
// Input Parameters : alarm_seconds -- Duracion de la alarma
// Hardware Resource Assigned: pim-aa-08 (Buzzer de alarma)
// ---------------------------------------------------------------------------
void activarAlarma(unsigned long alarm_seconds) {
  Serial.println("===Running Function 'activarAlarma'===");
  for (unsigned long i = 0; i < alarm_seconds * 2; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    vTaskDelay(pdMS_TO_TICKS(250));
    digitalWrite(BUZZER_PIN, LOW);
    vTaskDelay(pdMS_TO_TICKS(250));
  }
}

// ---------------------------------------------------------------------------
// Function ID: pim-aa-03 | Parent ID: pim-aa-00
// CIM Origin : cim-t7 (task: "Gestionar respuesta de acceso")
// Refinamiento OR del CIM (cim-t8 | cim-t9): cualquiera de las dos ramas
// satisface la gestion de la respuesta -> estructura switch/if generada.
// Qualification Array: [{"softgoal_id":"cim-q3","name":"Oportunidad de la respuesta"}]
// ---------------------------------------------------------------------------
void gestionarRespuestaAcceso(bool access_granted, char* action_out,
                              size_t action_len) {
  Serial.println("===Running Function 'gestionarRespuestaAcceso'===");
  if (access_granted) {          // rama OR 1: cim-t8
    strncpy(action_out, "desbloqueo", action_len);
    desbloquearCerradura(UNLOCK_SECONDS);
  } else {                       // rama OR 2: cim-t9
    strncpy(action_out, "alarma", action_len);
    activarAlarma(ALARM_SECONDS);
  }
}

// ---------------------------------------------------------------------------
// Function ID: pim-aa-06 | Parent ID: pim-aa-00
// CIM Origin : cim-t10 (task: "Registrar evento de acceso")
// Contribution Array: [{"softgoal_id":"cim-q4",
//                       "name":"Trazabilidad de accesos",
//                       "contribution":"help"}]
// SW Resource: pim-aa-09 (Bitacora de accesos)
// ---------------------------------------------------------------------------
void registrarEventoAcceso(const IdentificationEvent& ev,
                           const char* action_taken) {
  Serial.println("===Running Function 'registrarEventoAcceso'===");
  AccessLogEntry& e = accessLog[logCount % LOG_CAPACITY];
  e.timestamp  = ev.timestamp;
  e.person_id  = ev.person_id;
  e.confidence = ev.confidence;
  strncpy(e.action_taken, action_taken, sizeof(e.action_taken));
  logCount++;
  Serial.printf("[bitacora] #%d t=%lu person=%d (%s) conf=%.2f accion=%s\n",
                logCount, ev.timestamp, ev.person_id, ev.person_name,
                ev.confidence, action_taken);
}

// ---------------------------------------------------------------------------
// Thread ID : pim-aa-01 | Parent ID: pim-aa-00
// CIM Origin: cim-g2 (goal: "Controlar acceso al recinto")
// Tipo PIM  : OnIntervalAction -> hilo periodico FreeRTOS
// interval_in_milliseconds: 250  (decision de diseno CIM -> PIM)
// Qualification Array: [{"softgoal_id":"cim-q3","name":"Oportunidad de la respuesta"}]
// ---------------------------------------------------------------------------
void controlarAccesoAlRecintoTask(void* pvParameters) {
  const TickType_t xDelay = pdMS_TO_TICKS(250);
  char action[16];
  for (;;) {
    if (eventReceived) {
      eventReceived = false;
      bool granted = evaluarAutorizacion(lastEvent);
      gestionarRespuestaAcceso(granted, action, sizeof(action));
      registrarEventoAcceso(lastEvent, action);
    }
    vTaskDelay(xDelay);
  }
}

// ---------------------------------------------------------------------------
// setup()/loop(): punto de entrada del CPComponent.
// ---------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  Serial.println("=== SVIF :: Access Actuator Component ===");
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);   // estado seguro: bloqueada
  digitalWrite(BUZZER_PIN, LOW);

  connectWiFi();
  connectMQTT("svif-access-actuator", eventoIdentificacionReceiverCallback);

  xTaskCreatePinnedToCore(controlarAccesoAlRecintoTask,
                          "controlarAcceso", 4096, NULL, 1, NULL, 1);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!mqttClient.connected())
    connectMQTT("svif-access-actuator", eventoIdentificacionReceiverCallback);
  mqttClient.loop();
  delay(50);
}
