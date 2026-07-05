// ============================================================================
// FaceMonitorComponent.ino
// Unidad de despliegue del componente ciberfisico "Face Monitor Component".
// Generado por la transformacion PIM -> PSM del proceso MDD4CPS y completado
// durante la fase Code.
//
// Trazabilidad:
//   PSM  <- PIM: pim-fm-00 (cps_component: Face_Monitor_Component)
//   PIM  <- CIM: cim-a1    (agent: Face Monitor Component)
//
// Plataforma objetivo : ESP32-CAM (Arduino core, FreeRTOS nativo)
// Comunicaciones      : MQTT (PubSubClient)
//
// SIMULATION_MODE: al estar definido, el componente genera detecciones
// sinteticas en lugar de usar la camara, lo que permite verificar el flujo
// completo (deteccion -> identificacion -> publicacion) sin hardware.
// ============================================================================

#define SIMULATION_MODE   // Comentar para compilar contra la camara real

#include "comm_utils.h"
#include "secrets.h"

// ---------------------------------------------------------------------------
// SW Resource: Base de rostros enrolados
//   ID: pim-fm-06 | ID CIM Parent: cim-r2 (resource: "Base de rostros enrolados")
//   Estructura derivada del atributo data_structure del PIM.
// ---------------------------------------------------------------------------
struct EnrolledFace {
  int   person_id;        // Identificador del enrolado
  char  person_name[32];  // Nombre de la persona
  float face_embedding;   // Plantilla facial almacenada (simplificada en simulacion)
  bool  authorized;       // Autorizacion de acceso
};

static const EnrolledFace ENROLLED_FACES[] = {
  {1, "Ana Perez",    0.11f, true},
  {2, "Juan Soto",    0.47f, true},
  {3, "Visita Roja",  0.83f, false},
};
static const int ENROLLED_COUNT = sizeof(ENROLLED_FACES) / sizeof(EnrolledFace);

// ---------------------------------------------------------------------------
// HW Resource: Camara OV2640
//   ID: pim-fm-07 | ID CIM Parent: cim-r1 (resource: "Sensor de camara OV2640")
//   Nota para desarrolladores: en despliegue real inicializar con esp_camera
//   (pines del modulo AI-Thinker) durante setup().
// ---------------------------------------------------------------------------

static const float CONFIDENCE_THRESHOLD = 0.75f;  // fase Code: umbral de aceptacion
static IdentificationEvent pendingEvent;
static bool eventPending = false;

// ---------------------------------------------------------------------------
// Function ID: pim-fm-02 | Parent ID: pim-fm-00
// CIM Origin : cim-t1 (task: "Capturar imagen")
// Input Parameters : * None specified.
// Output Parameters: frame -- Imagen capturada por la camara
// Qualification Array: * None specified.
// Contribution Array : * None specified.
// Hardware Resource Assigned: pim-fm-07 (Camara OV2640)
// ---------------------------------------------------------------------------
bool capturarImagen(float* frame) {
  Serial.println("===Running Function 'capturarImagen'===");
#ifdef SIMULATION_MODE
  // --- Your code goes here ---
  // Simulacion: un "frame" es un valor aleatorio que representa la escena.
  *frame = random(0, 100) / 100.0f;
  return true;
#else
  // --- Your code goes here ---
  // camera_fb_t* fb = esp_camera_fb_get(); ...
  return false;
#endif
}

// ---------------------------------------------------------------------------
// Function ID: pim-fm-03 | Parent ID: pim-fm-00
// CIM Origin : cim-t2 (task: "Detectar rostro")
// Input Parameters : frame -- Imagen capturada
// Output Parameters: face_detected -- true si hay un rostro en la imagen
// Qualification Array: * None specified.
// Contribution Array : * None specified.
// ---------------------------------------------------------------------------
bool detectarRostro(float frame) {
  Serial.println("===Running Function 'detectarRostro'===");
#ifdef SIMULATION_MODE
  // --- Your code goes here ---
  // Simulacion: ~30% de los ciclos de monitoreo contienen un rostro.
  return frame < 0.30f;
#else
  // --- Your code goes here ---
  return false;
#endif
}

// ---------------------------------------------------------------------------
// Function ID: pim-fm-05 | Parent ID: pim-fm-04
// CIM Origin : cim-t4 (task: "Comparar con rostros enrolados")
// Input Parameters : face_embedding -- Caracteristicas extraidas del rostro
// Output Parameters: person_id, confidence
// Qualification Array: * None specified.
// Contribution Array : [{"softgoal_id":"cim-q2",
//                        "name":"Privacidad de datos personales",
//                        "contribution":"help"}]
//   La comparacion ocurre LOCALMENTE en el nodo (edge): la imagen no se
//   transmite por la red, en apoyo del softgoal de privacidad.
// SW Resource: pim-fm-06 (Base de rostros enrolados)
// ---------------------------------------------------------------------------
int compararConRostrosEnrolados(float face_embedding, float* confidence) {
  Serial.println("===Running Function 'compararConRostrosEnrolados'===");
  int   best_id = -1;
  float best_distance = 1.0f;
  for (int i = 0; i < ENROLLED_COUNT; i++) {
    float d = fabs(ENROLLED_FACES[i].face_embedding - face_embedding);
    if (d < best_distance) {
      best_distance = d;
      best_id = i;
    }
  }
  *confidence = 1.0f - best_distance;
  return best_id;  // indice en ENROLLED_FACES (-1 si la base esta vacia)
}

// ---------------------------------------------------------------------------
// Function ID: pim-fm-04 | Parent ID: pim-fm-00
// CIM Origin : cim-t3 (task: "Identificar rostro")
// Input Parameters : frame -- Imagen con rostro detectado
// Output Parameters: identification_event -- Evento de identificacion
// Qualification Array: [{"softgoal_id":"cim-q1","name":"Identificacion oportuna"}]
// Contribution Array : * None specified.
// ---------------------------------------------------------------------------
void identificarRostro(float frame, IdentificationEvent* ev) {
  Serial.println("===Running Function 'identificarRostro'===");
  float confidence = 0.0f;
  // Extraccion de caracteristicas (simplificada): el embedding se deriva del frame.
  float face_embedding = frame;
  int idx = compararConRostrosEnrolados(face_embedding, &confidence);

  ev->timestamp  = millis();
  ev->confidence = confidence;
  if (idx >= 0 && confidence >= CONFIDENCE_THRESHOLD) {
    ev->person_id  = ENROLLED_FACES[idx].person_id;
    strncpy(ev->person_name, ENROLLED_FACES[idx].person_name,
            sizeof(ev->person_name));
    ev->authorized = ENROLLED_FACES[idx].authorized;
  } else {
    ev->person_id  = -1;
    strncpy(ev->person_name, "desconocido", sizeof(ev->person_name));
    ev->authorized = false;
  }
}

// ---------------------------------------------------------------------------
// Thread ID : pim-fm-01 | Parent ID: pim-fm-00
// CIM Origin: cim-g1 (goal: "Monitorear presencia de personas")
// Tipo PIM  : OnIntervalAction -> hilo periodico FreeRTOS
// interval_in_milliseconds: 500  (decision de diseno CIM -> PIM)
// Qualification Array: [{"softgoal_id":"cim-q1","name":"Identificacion oportuna"}]
// ---------------------------------------------------------------------------
void monitorearPresenciaDePersonasTask(void* pvParameters) {
  const TickType_t xDelay = pdMS_TO_TICKS(500);
  for (;;) {
    float frame;
    if (capturarImagen(&frame) && detectarRostro(frame)) {
      identificarRostro(frame, &pendingEvent);
      eventPending = true;
    }
    vTaskDelay(xDelay);
  }
}

// ---------------------------------------------------------------------------
// Thread ID : pim-fm-08 | Parent ID: pim-fm-00
// CIM Origin: cim-d1 (dependum: "Evento de identificacion") /
//             cim-t5 (task: "Publicar evento de identificacion")
// Tipo PIM  : MessageSender (comm_thread) -> hilo de comunicacion
// interval_in_milliseconds: 500
// Contribution Array: [{"softgoal_id":"cim-q2",
//                       "name":"Privacidad de datos personales",
//                       "contribution":"hurt"}]
//   Se transmiten datos personales minimizados (identidad, no imagen).
// ---------------------------------------------------------------------------
void eventoIdentificacionSenderTask(void* pvParameters) {
  const TickType_t xDelay = pdMS_TO_TICKS(500);
  for (;;) {
    ensureConnectivity("svif-face-monitor");
    if (eventPending) {
      if (publishIdentificationEvent(pendingEvent)) {
        eventPending = false;
      }
    }
    vTaskDelay(xDelay);
  }
}

// ---------------------------------------------------------------------------
// setup()/loop(): punto de entrada del CPComponent. Inicializa WiFi, MQTT y
// hardware, y crea los hilos generados a partir del modelo PIM.
// ---------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  Serial.println("=== SVIF :: Face Monitor Component ===");
#ifndef SIMULATION_MODE
  // --- Your code goes here ---
  // Inicializacion de la camara OV2640 (esp_camera_init con pines AI-Thinker).
#endif
  connectWiFi();
  connectMQTT("svif-face-monitor");

  xTaskCreatePinnedToCore(monitorearPresenciaDePersonasTask,
                          "monitorearPresencia", 4096, NULL, 1, NULL, 1);
  xTaskCreatePinnedToCore(eventoIdentificacionSenderTask,
                          "eventoSender", 4096, NULL, 1, NULL, 0);
}

void loop() {
  // Mantiene viva la comunicacion; el comportamiento reside en los hilos.
  mqttClient.loop();
  delay(100);
}
