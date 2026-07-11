// CPC ID: cim-b2
// Parent ID: cim-a2sr-c
// Name: Access Actuator Component
// Description: 

#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <FreeRTOS_SAMD21.h>
#include <task.h>
#include "secrets.h"
#include "comm_utils.h"
#include <Arduino_JSON.h>
#include <ArduinoJson.h>

// Global variables for WiFi and MQTT connectivity
const char* eventoDeIdentificación_MessageReceiverClientId = "accessActuatorComponentClient_cim_b2";
WiFiClient eventoDeIdentificación_MessageReceiverClient;
PubSubClient eventoDeIdentificación_MessageReceiverMqttClient(eventoDeIdentificación_MessageReceiverClient);

bool debug = true;

// MQTT topics for this CPC ({CPS_id}/{CPC_id}/{comm_thread_id})

// Listener Topics(Receiver)
const char* eventoDeIdentificación_MessageReceiver_topic = "svif_sdSvif_sr_sd_DependenciasEstrategicasSr_VistaHibridaSd_sr/cim_b1/cim_d1_comm_thread/dependum";

// Thread Status variables
bool controlarAccesoAlRecinto_GoalAchieved = false; // Global variable for thread controlarAccesoAlRecinto(ID: cim-g2)
TaskHandle_t TaskcontrolarAccesoAlRecinto;

// Function output variables
bool evaluarAutorización_decision = false; // Decision de autorizacion.

// Global Operation Mode Variables


// Global Data Structures (software resources and/or any dependum)
struct eventoDeIdentificación_MessageReceiver_data_structure {
    double timestamp; // Marca de tiempo del evento.
    double person_id; // Identificador de la persona.
    double person_name; // Nombre de la persona.
    double confidence; // Confianza de la identificacion.
    double authorized; // Indicador de autorizacion.
} eventoDeIdentificación_MessageReceiver_data_structure;

struct bitácoraDeAccesos_data_structure {
    unsigned long timestamp; // Marca de tiempo del acceso.
    char[32] person_id; // Identificador de la persona.
    bool decision; // Resultado de la autorizacion.
} bitácoraDeAccesos_data_structure;


// Listener Thread Handles
TaskHandle_t TaskreceiveDependum_eventoDeIdentificación_MessageReceiver;

void setup() {
    if (debug) {
        Serial.begin(9600);
        while (!Serial);
    }
    connectToWiFi();

    // Listener Topics(Receiver)
    mqttSetup(eventoDeIdentificación_MessageReceiverMqttClient, callback_eventoDeIdentificación_MessageReceiver);
    connectToMQTT(eventoDeIdentificación_MessageReceiverMqttClient, eventoDeIdentificación_MessageReceiverClientId, eventoDeIdentificación_MessageReceiver_topic);
    
    // Create tasks for the operational goals
    xTaskCreate(
        controlarAccesoAlRecintoTask,        // Function to implement the task
        "controlarAccesoAlRecintoTask",      // Name of the task
        512,                      // Stack size (in words, not bytes)
        NULL,                     // Task input parameter
        1,                        // Priority of the task
        &TaskcontrolarAccesoAlRecinto        // Task handle
    );
    xTaskCreate(
        receiveDependum_eventoDeIdentificación_MessageReceiverTask,        // Function to implement the task
        "receiveDependum_eventoDeIdentificación_MessageReceiverTask",      // Name of the task
        512,                      // Stack size (in words, not bytes)
        NULL,                     // Task input parameter
        1,                        // Priority of the task
        &TaskreceiveDependum_eventoDeIdentificación_MessageReceiver        // Task handle
    );

    // Start the threads
    vTaskStartScheduler();
}


void callback_eventoDeIdentificación_MessageReceiver(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message on Topic 1: ");
    Serial.print(topic);
    Serial.println(" - ");
    // Parse the incoming JSON message
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (!error) {
        eventoDeIdentificación_MessageReceiver_data_structure.timestamp = doc["timestamp"];
        eventoDeIdentificación_MessageReceiver_data_structure.person_id = doc["person_id"];
        eventoDeIdentificación_MessageReceiver_data_structure.person_name = doc["person_name"];
        eventoDeIdentificación_MessageReceiver_data_structure.confidence = doc["confidence"];
        eventoDeIdentificación_MessageReceiver_data_structure.authorized = doc["authorized"];

        // Debug output to Serial
        Serial.println("Dependum data received:");
        if (debug) {
                    Serial.print("timestamp: ");
                    Serial.println(eventoDeIdentificación_MessageReceiver_data_structure.timestamp);
                    Serial.print("person_id: ");
                    Serial.println(eventoDeIdentificación_MessageReceiver_data_structure.person_id);
                    Serial.print("person_name: ");
                    Serial.println(eventoDeIdentificación_MessageReceiver_data_structure.person_name);
                    Serial.print("confidence: ");
                    Serial.println(eventoDeIdentificación_MessageReceiver_data_structure.confidence);
                    Serial.print("authorized: ");
                    Serial.println(eventoDeIdentificación_MessageReceiver_data_structure.authorized);
        }
    } else {
        Serial.println("Error parsing JSON message");
    }
    // Your custom code to process the dependum can go here



}




void receiveDependum_eventoDeIdentificación_MessageReceiverTask(void *pvParameters) {

        //
        // --- Listener Thread Information ---
        // Name: Evento de identificación - message receiver
        // ID: cim-d1-listener_thread
        // Description: This Listener Thread is responsible for receiving the dependum: eventoDeIdentificación_MessageReceiver_data_structure
        //
        // Original Element in PIM: Evento de identificación - message receiver
        // Transformed To: Function `eventoDeIdentificación_MessageReceiver()`
        //
        // Note for Developers:
        // The `dependum` data should be stored on and then retrieved from the function evaluarAutorización().
        // Ensure the function completes its operation and receives the required data 
        // in the appropriate format for reception.
        // 
        // Qualification Array:
        //  * None specified.
        // 
        // Contribution Array:
        //  * None specified.
        // 
        //
    // This variable handles the period in milliseconds for thread execution
    const TickType_t xDelay = pdMS_TO_TICKS(500);
    

    for (;;)
    {

        // Check MQTT connection status
        if (!eventoDeIdentificación_MessageReceiverMqttClient.connected())
        {
          connectToMQTT(eventoDeIdentificación_MessageReceiverMqttClient, eventoDeIdentificación_MessageReceiverClientId, eventoDeIdentificación_MessageReceiver_topic);
        }

        // Always poll MQTT for new messages
        eventoDeIdentificación_MessageReceiverMqttClient.loop();

        // Keep delay to avoid overloading loop but keep polling
        vTaskDelay(xDelay);
    }
}

void loop() {

    // Let FreeRTOS manage tasks, nothing to do here
    delay(100);
}

bool evaluarAutorización(IdentificationEvent identification_event) {
    // Function ID: cim-t6
    // Parent ID: cim-t6
    // Input Parameters:
        // identification_event(IdentificationEvent) - Evento de identificacion recibido.
    // Output Parameters:
        // decision(bool) - Decision de autorizacion.
    // Qualification Array:
    //  * None specified.
    // Contribution Array:
    //  * None specified.
    // Hardware Resource Assigned:
    // Set output parameters
    evaluarAutorización_decision = false; // Decision de autorizacion.


    // --- Your code goes here ---
    
    
    
    return true;

    // --- Your code goes here ---
}

bool gestionarRespuestaDeAcceso(bool decision) {
    // Function ID: cim-t7
    // Parent ID: cim-t7
    // Input Parameters:
        // decision(bool) - Decision de autorizacion.
    // Output Parameters:
    // Qualification Array:
    //  * None specified.
    // Contribution Array:
    //  * None specified.
    // Hardware Resource Assigned:
    // Set output parameters
 

    // --- Your code goes here ---
    
    
    
    return true;

    // --- Your code goes here ---
}

bool registrarEventoDeAcceso(AccessLogEntry access_event) {
    // Function ID: cim-t10
    // Parent ID: cim-t10
    // Input Parameters:
        // access_event(AccessLogEntry) - Evento de acceso a registrar.
    // Output Parameters:
    // Qualification Array:
    //  * None specified.
    // Contribution Array:
    //  * - "[{ "softgoal_id": "cim-q4", "name": "Trazabilidad de accesos", "contribution": "help"}]"
    // Hardware Resource Assigned:
    // Set output parameters
 

    // --- Your code goes here ---
    
    
    
    return true;

    // --- Your code goes here ---
}

bool desbloquearCerradura() {
    // Function ID: cim-t8
    // Parent ID: cim-t8
    // Input Parameters:
    // Output Parameters:
    // Qualification Array:
    //  * None specified.
    // Contribution Array:
    //  * None specified.
    // Hardware Resource Assigned:
    // Set output parameters
 

    // --- Your code goes here ---
    
    
    
    return true;

    // --- Your code goes here ---
}

bool activarAlarma() {
    // Function ID: cim-t9
    // Parent ID: cim-t9
    // Input Parameters:
    // Output Parameters:
    // Qualification Array:
    //  * None specified.
    // Contribution Array:
    //  * None specified.
    // Hardware Resource Assigned:
    // Set output parameters
 

    // --- Your code goes here ---
    
    
    
    return true;

    // --- Your code goes here ---
}

// Task for controlarAccesoAlRecinto
void controlarAccesoAlRecintoTask(void *pvParameters) {
    // This variable handles the period in milliseconds for thread execution
    const TickType_t xDelay = pdMS_TO_TICKS(250); // Example interval for controlarAccesoAlRecinto

    // --- controlarAccesoAlRecinto Context Information ---
    // ID: cim-g2
    // ID CIM Parent: cim-g2
    // qualification_array: 
    //  * - "[{ "softgoal_id": "cim-q3", "name": "Oportunidad de la respuesta"}]"
    // contribution_array: 
    //  * None specified.
    // ----------------------------------------------------------

    for (;;) {
        // --- Your code goes here ---
        // Evaluate the state of controlarAccesoAlRecinto

        controlarAccesoAlRecinto_GoalAchieved = !controlarAccesoAlRecinto_GoalAchieved; // Toggle state for simulation
        
        // --- Your code ends here ---

        vTaskDelay(xDelay);
    }
}
