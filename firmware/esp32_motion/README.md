# ESP32 Motion Firmware

Controls all 12 servos (3 per leg × 4 legs) for NeuraBot's locomotion.

## Hardware

| Pin   | Function              |
|-------|-----------------------|
| GPIO 13 | Servo FL Hip        |
| GPIO 12 | Servo FL Thigh      |
| GPIO 14 | Servo FL Knee       |
| GPIO 27 | Servo FR Hip        |
| GPIO 26 | Servo FR Thigh      |
| GPIO 25 | Servo FR Knee       |
| GPIO 33 | Servo RL Hip        |
| GPIO 32 | Servo RL Thigh      |
| GPIO 35 | Servo RL Knee       |
| GPIO 34 | Servo RR Hip        |
| GPIO 21 | Servo RR Thigh      |
| GPIO 22 | Servo RR Knee       |
| GPIO 16 | UART RX (from Pi)   |
| GPIO 17 | UART TX (to Pi)     |

## Protocol

Receives JSON over UART (115200 baud), newline-delimited:

```json
{
  "t": "angles",
  "d": {
    "FL": {"hip": 0.0, "thigh": 45.0, "knee": -90.0},
    "FR": {"hip": 0.0, "thigh": 45.0, "knee": -90.0},
    "RL": {"hip": 0.0, "thigh": 45.0, "knee": -90.0},
    "RR": {"hip": 0.0, "thigh": 45.0, "knee": -90.0}
  }
}
```

## Flash Instructions

```bash
# Install PlatformIO
pip install platformio

cd firmware/esp32_motion
pio run --target upload
```

## Dependencies

- Arduino framework for ESP32
- ESP32Servo library
- ArduinoJson
