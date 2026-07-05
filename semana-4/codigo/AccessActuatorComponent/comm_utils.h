#ifndef COMM_UTILS_H
#define COMM_UTILS_H

// ============================================================================
// comm_utils.h  --  Access Actuator Component
// Generado por la transformacion PIM -> PSM (proceso MDD4CPS).
// Contiene las utilidades de comunicacion (WiFi + MQTT), la estructura del
// dependum y su deserializacion, derivadas del modelo PIM.
//
// Trazabilidad:
//   PIM: pim-aa-10 (listener_thread: eventoIdentificacionReceiver)
//   CIM: cim-d1 (dependum resource: "Evento de identificacion")
// ============================================================================

#include <WiFi.h>
#include <PubSubClient.h>
#include "secrets.h"

// --- Estructura del dependum (identica a la del emisor) ---------------------
struct IdentificationEvent {
  unsigned long timestamp;
  int           person_id;
  char          person_name[32];
  float         confidence;
  bool          authorized;
};

static const char* TOPIC_IDENTIFICATION_EVENT = "svif/eventos/identificacion";

static WiFiClient   wifiClient;
static PubSubClient mqttClient(wifiClient);

// --- Deserializacion (parser JSON minimo, sin dependencias) -----------------
inline bool extractLong(const char* json, const char* key, long* out) {
  const char* p = strstr(json, key);
  if (!p) return false;
  p = strchr(p, ':');
  if (!p) return false;
  *out = atol(p + 1);
  return true;
}

inline bool extractFloat(const char* json, const char* key, float* out) {
  const char* p = strstr(json, key);
  if (!p) return false;
  p = strchr(p, ':');
  if (!p) return false;
  *out = atof(p + 1);
  return true;
}

inline bool extractString(const char* json, const char* key, char* out,
                          size_t len) {
  const char* p = strstr(json, key);
  if (!p) return false;
  p = strchr(p + strlen(key), '"');       // apertura del valor
  if (!p) return false;
  p++;
  const char* q = strchr(p, '"');
  if (!q) return false;
  size_t n = (size_t)(q - p);
  if (n >= len) n = len - 1;
  strncpy(out, p, n);
  out[n] = '\0';
  return true;
}

inline bool deserializeIdentificationEvent(const char* payload,
                                           IdentificationEvent* ev) {
  long ts = 0, pid = -1;
  bool ok = extractLong(payload, "\"timestamp\"", &ts);
  ok &= extractLong(payload, "\"person_id\"", &pid);
  ok &= extractString(payload, "\"person_name\"", ev->person_name,
                      sizeof(ev->person_name));
  ok &= extractFloat(payload, "\"confidence\"", &ev->confidence);
  ev->timestamp  = (unsigned long)ts;
  ev->person_id  = (int)pid;
  ev->authorized = (strstr(payload, "\"authorized\":true") != NULL);
  return ok;
}

// --- Conectividad ------------------------------------------------------------
inline void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("[comm] Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
}

inline void connectMQTT(const char* clientId,
                        void (*callback)(char*, byte*, unsigned int)) {
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(callback);
  while (!mqttClient.connected()) {
    Serial.println("[comm] Conectando al broker MQTT...");
    if (mqttClient.connect(clientId)) {
      mqttClient.subscribe(TOPIC_IDENTIFICATION_EVENT);
      Serial.print("[comm] Suscrito a ");
      Serial.println(TOPIC_IDENTIFICATION_EVENT);
    } else {
      Serial.print("[comm] Fallo, rc=");
      Serial.println(mqttClient.state());
      delay(2000);
    }
  }
}

#endif // COMM_UTILS_H
