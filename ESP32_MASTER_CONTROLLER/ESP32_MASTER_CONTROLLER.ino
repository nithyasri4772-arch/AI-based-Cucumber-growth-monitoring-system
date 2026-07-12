/*
 * Cucumber Detection System - ESP32 Master Controller
 * --------------------------------------------------
 * This code is the "Brain" of your robot. 
 * It listens to your Computer (Python) and moves the Motors.
 */

#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>
#include <DHT.h>

// --- STEP 1: Put your WiFi Name and Password here! ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// --- STEP 2: Tell the computer where the wires are connected ---
#define SERVO_PIN 13   // The Orange wire of the Servo
#define FAN_PIN 12     // The Signal wire of the Relay
#define DHT_PIN 4      // The Data wire of the DHT Sensor
#define DHT_TYPE DHT11 // Set to DHT11 (Blue) or DHT22 (White)

// --- CREATING THE OBJECTS ---
WebServer server(80); // This makes the ESP32 look like a Website
Servo myservo;        // This is your Motor
DHT dht(DHT_PIN, DHT_TYPE); // This is your Sensor

// --- THIS PART READS THE TEMPERATURE ---
void handleSensor() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  String json = "{";
  json += "\"temperature_c\":" + String(t) + ",";
  json += "\"humidity_percent\":" + String(h);
  json += "}";
  server.send(200, "application/json", json);
}

// --- THIS PART MOVES THE MOTOR (LEFT/RIGHT) ---
void handleMove() {
  if (server.hasArg("angle")) {
    int angle = server.arg("angle").toInt();
    myservo.write(angle);
    server.send(200, "text/plain", "OK: Moving to " + String(angle));
  }
}

// --- THIS PART TURNS THE FAN ON AND OFF ---
void handleFan() {
  if (server.hasArg("state")) {
    String state = server.arg("state");
    if (state == "on") {
      digitalWrite(FAN_PIN, HIGH);
      server.send(200, "text/plain", "OK: Fan ON");
    } else {
      digitalWrite(FAN_PIN, LOW);
      server.send(200, "text/plain", "OK: Fan OFF");
    }
  }
}

// --- THIS PART RUNS ONLY ONCE WHEN YOU START ---
void setup() {
  Serial.begin(115200);
  
  pinMode(FAN_PIN, OUTPUT);
  digitalWrite(FAN_PIN, LOW); // Start with fan OFF
  
  myservo.attach(SERVO_PIN);
  myservo.write(90); // Start in the Middle
  
  dht.begin();

  // CONNECTING TO INTERNET
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nI am Connected to WiFi!");
  Serial.print("My IP address is: ");
  Serial.println(WiFi.localIP()); // COPY THIS IP ADDRESS!

  // MAKING THE ENDPOINTS (The "Pages" the Computer visits)
  server.on("/sensor", handleSensor);
  server.on("/move", handleMove);
  server.on("/fan", handleFan);

  server.begin();
}

// --- THIS PART RUNS FOREVER AND EVER ---
void loop() {
  server.handleClient(); // Always wait for messages from Python
}
