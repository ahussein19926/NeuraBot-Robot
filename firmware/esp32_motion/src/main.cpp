/**
 * NeuraBot — ESP32 Motion Controller Firmware
 * Controls 12 servos via PWM.
 * Receives JSON commands over UART from Raspberry Pi / Jetson.
 */

#include <Arduino.h>
#include <ESP32Servo.h>
#include <ArduinoJson.h>

// ---- Servo pin mapping ----
#define PIN_FL_HIP    13
#define PIN_FL_THIGH  12
#define PIN_FL_KNEE   14
#define PIN_FR_HIP    27
#define PIN_FR_THIGH  26
#define PIN_FR_KNEE   25
#define PIN_RL_HIP    33
#define PIN_RL_THIGH  32
#define PIN_RL_KNEE   35
#define PIN_RR_HIP    34
#define PIN_RR_THIGH  21
#define PIN_RR_KNEE   22

// ---- UART ----
#define UART_RX 16
#define UART_TX 17
#define BAUD    115200

// ---- Servo limits ----
#define SERVO_MIN_US 500
#define SERVO_MAX_US 2500
#define ANGLE_OFFSET 90   // Neutral = 90 degrees

Servo servos[12];
const int pins[12] = {
  PIN_FL_HIP, PIN_FL_THIGH, PIN_FL_KNEE,
  PIN_FR_HIP, PIN_FR_THIGH, PIN_FR_KNEE,
  PIN_RL_HIP, PIN_RL_THIGH, PIN_RL_KNEE,
  PIN_RR_HIP, PIN_RR_THIGH, PIN_RR_KNEE,
};
const char* legNames[4]  = {"FL","FR","RL","RR"};
const char* jointNames[3] = {"hip","thigh","knee"};

// Leg index map: legNames[i] → servo base index i*3
int legIndex(const char* name) {
  for (int i = 0; i < 4; i++)
    if (strcmp(name, legNames[i]) == 0) return i;
  return -1;
}

void setAngle(int leg, int joint, float angle) {
  int idx = leg * 3 + joint;
  int deg = constrain((int)(angle + ANGLE_OFFSET), 0, 180);
  servos[idx].write(deg);
}

void setup() {
  Serial2.begin(BAUD, SERIAL_8N1, UART_RX, UART_TX);
  Serial.begin(115200);
  Serial.println("NeuraBot Motion ESP32 ready.");

  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);

  for (int i = 0; i < 12; i++) {
    servos[i].setPeriodHertz(50);
    servos[i].attach(pins[i], SERVO_MIN_US, SERVO_MAX_US);
    servos[i].write(ANGLE_OFFSET);  // neutral
  }
  delay(500);
}

String inputBuffer = "";

void loop() {
  while (Serial2.available()) {
    char c = Serial2.read();
    if (c == '\n') {
      // Parse JSON
      StaticJsonDocument<512> doc;
      DeserializationError err = deserializeJson(doc, inputBuffer);
      inputBuffer = "";

      if (err) {
        Serial.printf("JSON error: %s\n", err.c_str());
        continue;
      }

      const char* type = doc["t"];
      if (strcmp(type, "angles") == 0) {
        JsonObject d = doc["d"];
        for (JsonPair kv : d) {
          int legIdx = legIndex(kv.key().c_str());
          if (legIdx < 0) continue;
          JsonObject joints = kv.value().as<JsonObject>();
          for (int j = 0; j < 3; j++) {
            float angle = joints[jointNames[j]] | 0.0f;
            setAngle(legIdx, j, angle);
          }
        }
        // Send ack
        Serial2.println("{\"ack\":1}");
      }
    } else {
      inputBuffer += c;
      if (inputBuffer.length() > 1024) inputBuffer = "";  // overflow guard
    }
  }
}
