#ifndef COMM_UTILS_H
#define COMM_UTILS_H

// ============================================================================
// comm_utils.h  --  Face Monitor Component
// Generado por la transformacion PIM -> PSM (proceso MDD4CPS).
// Contiene las utilidades de comunicacion (WiFi + MQTT), la estructura del
// dependum y su serializacion, derivadas del modelo PIM.
//
// Trazabilidad:
//   PIM: pim-fm-08 (comm_thread: eventoIdentificacionSender)
//   CIM: cim-d1 (dependum resource: "Evento de identificacion")
// ============================================================================

#include <WiFi.h>
#include <PubSubClient.h>
#include "secrets.h"

// --- Estructura del dependum -----------------------------------------------
// Origen: atributo dependum_data_structure de pim-fm-08 (PIM),
//         completado con tipos concretos durante la transformacion PIM -> PSM.
struct IdentificationEvent {
  unsigned long timestamp;   // Marca de tiempo del evento (ms)
  int           person_id;   // Identificador del rostro enrolado (-1 = desconocido)
  char          person_name[32]; // Nombre asociado al rostro enrolado
  float         confidence;  // Confianza de la identificacion (0.0 - 1.0)
  bool          authorized;  // true si pertenece a la lista de autorizados
};

// Topico MQTT del dependum (decision de la fase Code)
static const char* TOPIC_IDENTIFICATION_EVENT = "svif/eventos/identificacion";

static WiFiClient   wifiClient;
static PubSubClient mqttClient(wifiClient);

// --- Serializacion del dependum (JSON) --------------------------------------
inline void serializeIdentificationEvent(const IdentificationEvent& ev,
                                         char* buffer, size_t len) {
  snprintf(buffer, len,
           "{\"timestamp\":%lu,\"person_id\":%d,\"person_name\":\"%s\","
           "\"confidence\":%.2f,\"authorized\":%s}",
           ev.timestamp, ev.person_id, ev.person_name, ev.confidence,
           ev.authorized ? "true" : "false");
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
  Serial.print("[comm] IP: ");
  Serial.println(WiFi.localIP());
}

inline void connectMQTT(const char* clientId) {
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  while (!mqttClient.connected()) {
    Serial.println("[comm] Conectando al broker MQTT...");
    if (!mqttClient.connect(clientId)) {
      Serial.print("[comm] Fallo, rc=");
      Serial.println(mqttClient.state());
      delay(2000);
    }
  }
  Serial.println("[comm] MQTT conectado.");
}

inline void ensureConnectivity(const char* clientId) {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!mqttClient.connected()) connectMQTT(clientId);
  mqttClient.loop();
}

inline bool publishIdentificationEvent(const IdentificationEvent& ev) {
  char payload[192];
  serializeIdentificationEvent(ev, payload, sizeof(payload));
  bool ok = mqttClient.publish(TOPIC_IDENTIFICATION_EVENT, payload);
  Serial.print("[comm] publish ");
  Serial.print(TOPIC_IDENTIFICATION_EVENT);
  Serial.print(" -> ");
  Serial.println(ok ? payload : "ERROR");
  return ok;
}

#endif // COMM_UTILS_H
