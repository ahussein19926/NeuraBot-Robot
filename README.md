<div align="center">

<img src="docs/images/neurabot_hero.jpg" alt="NeuraBot" width="100%"/>

# 🐾 NeuraBot

**AI-Powered Quadruped Robot Dog**

[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20%2F%20Jetson-8A2BE2?style=flat-square&logo=raspberry-pi&logoColor=white)](https://www.raspberrypi.com)
[![MCU](https://img.shields.io/badge/MCU-Dual%20ESP32-1D9E75?style=flat-square&logo=espressif&logoColor=white)](https://www.espressif.com)
[![Vision](https://img.shields.io/badge/Vision%20AI-YOLOv8-EF9F27?style=flat-square&logo=opencv&logoColor=white)](https://ultralytics.com)
[![Speech](https://img.shields.io/badge/Speech-Whisper%20%2B%20TTS-D4537E?style=flat-square&logo=openai&logoColor=white)](https://openai.com/whisper)
[![IK](https://img.shields.io/badge/DOF-12%20Servos-378ADD?style=flat-square)](/)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=flat-square)](/)
[![License](https://img.shields.io/badge/Repo-Private-red?style=flat-square)](/)

---

*Vision · Speech · Inverse Kinematics · Web Control · Power Management*

</div>

---

## What is NeuraBot?

NeuraBot is a fully custom-built AI-powered quadruped robot dog. It walks using a real-time inverse kinematics engine, sees with YOLOv8, listens and speaks with Whisper + Coqui TTS, and can be controlled live from any browser. Everything — from the 3D-printed chassis to the dual ESP32 firmware — is built from scratch.

| | |
|---|---|
| 🦾 **12-DOF locomotion** | 3 joints per leg × 4 legs, driven by MG996R/DS3218 servos |
| 👁️ **Vision AI** | YOLOv8n real-time object detection at 15 fps |
| 🎙️ **Speech AI** | Whisper STT + Coqui TTS, wake word "Neura" |
| ⚡ **Smart power system** | Dual INA219 rail monitoring, SOC estimation, low-voltage cutoff |
| 🌐 **Web control panel** | Live camera feed, D-pad, gait controls via browser |
| 📺 **Onboard display** | SPI TFT face/status screen + I2S mic + speaker |

---

## Gallery

### Full Unit

> 📸 Replace with your photo: `docs/images/neurabot_hero.jpg`

### Build Process

| Step | Photo | Description |
|------|-------|-------------|
| 1 | ![](docs/images/build_3dparts.jpg) | 3D printed parts — body, legs, head, mounts |
| 2 | ![](docs/images/build_chassis.jpg) | Body frame & leg assembly |
| 3 | ![](docs/images/build_servos.jpg) | 12× servo installation (3 per leg) |
| 4 | ![](docs/images/build_electronics.jpg) | Raspberry Pi & dual ESP32 mounting |
| 5 | ![](docs/images/build_power.jpg) | Power distribution & LiPo bay wiring |
| 6 | ![](docs/images/build_head.jpg) | Head assembly — display, camera & mic |
| 7 | ![](docs/images/build_wiring.jpg) | Full cable routing & harness |
| 8 | ![](docs/images/build_gait_test.jpg) | First walk — IK gait test |
| 9 | ![](docs/images/build_final.jpg) | Fully assembled NeuraBot |

---

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│               Raspberry Pi / Jetson                      │
│                                                          │
│   Vision AI (YOLOv8)      Speech AI (Whisper + TTS)     │
│   IK Engine (50 Hz)       Web Panel (Flask + SocketIO)  │
│   Power Monitor (INA219)  Comm Manager (UART)           │
└─────────────┬────────────────────────┬───────────────────┘
              │ UART 115200            │ UART / I2C / SPI
   ┌──────────▼──────────┐  ┌─────────▼───────────────┐
   │   ESP32 — Motion    │  │  ESP32 — Peripherals    │
   │   12× servo control │  │  TFT · Mic · Speaker    │
   │   JSON protocol     │  │  NeoPixel LEDs          │
   └──────────┬──────────┘  └─────────────────────────┘
              │
   ┌──────────▼──────────────────────────────────────┐
   │  Hardware Layer                                  │
   │  3S LiPo (11.1V) · MG996R Servos · IMX477 Cam  │
   │  INMP441 Mic · PETG/PLA+ Chassis · TPU Feet     │
   └──────────────────────────────────────────────────┘
```

---

## Capabilities

| Module | Description |
|--------|-------------|
| 🔺 **Inverse Kinematics** | Geometric 3-DOF solver per leg. Trot, walk, sit, shake at 50 Hz |
| 👁️ **Vision AI** | YOLOv8n real-time detection with annotated web stream |
| 🎙️ **Speech AI** | Whisper STT + Coqui TTS with full voice command routing |
| ⚡ **Power System** | Dual INA219 monitoring, SOC estimation, low-voltage cutoff |
| 🌐 **Web Control** | SocketIO browser panel — D-pad, gaits, live camera, telemetry |
| 🔌 **Peripheral Bus** | TFT display · I2S mic array · MAX98357 amp · WS2812B LEDs |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/NeuraBot.git
cd NeuraBot

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Flash ESP32 firmware
cd firmware/esp32_motion && pio run --target upload
cd ../esp32_peripherals && pio run --target upload

# 4. Configure
cp config/config.example.yaml config/config.yaml

# 5. Download AI models
python scripts/download_models.py

# 6. Calibrate servos
python scripts/calibrate_servos.py

# 7. Launch
python src/main.py
# Web panel: http://<robot-ip>:5000
```

---

## Repository Structure

```
NeuraBot/
├── src/
│   ├── ai/
│   │   ├── vision/            # YOLOv8 vision module
│   │   └── speech/            # Whisper STT + Coqui TTS
│   ├── ik/                    # Inverse Kinematics engine
│   ├── control/               # Gait controller + ESP32 comms
│   ├── power/                 # INA219 power monitor
│   └── web/                   # Flask + SocketIO web panel
├── firmware/
│   ├── esp32_motion/          # C++ servo firmware (PlatformIO)
│   └── esp32_peripherals/     # Display, audio, LED firmware
├── hardware/
│   ├── 3d_models/             # STL / CAD files
│   │   ├── body/
│   │   ├── legs/
│   │   ├── head/
│   │   └── mounts/
│   ├── pcb/                   # PCB schematics
│   └── bom/                   # Bill of materials
├── docs/
│   ├── build_guide/           # Step-by-step assembly guide
│   ├── wiring/                # Wiring diagrams & pinouts
│   └── images/                # Build photos & renders
├── config/
│   └── config.example.yaml    # Hardware configuration
├── scripts/
│   ├── calibrate_servos.py    # Interactive servo calibration
│   └── download_models.py     # AI model downloader
└── tests/
    └── test_ik.py             # IK unit tests
```

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Build Guide](docs/build_guide/README.md) | Full 15-step assembly from printing to first boot |
| [Wiring Guide](docs/wiring/README.md) | All wiring diagrams, pinouts, power architecture |
| [Bill of Materials](hardware/bom/BOM.md) | Full parts list with estimated cost ($225–$400) |

---

## Hardware Overview

| Component | Spec | Qty |
|-----------|------|-----|
| SBC | Raspberry Pi 5 / Jetson Nano | 1 |
| MCU | ESP32 DevKit v1 | 2 |
| Servos | MG996R / DS3218MG (20 kg·cm) | 12 |
| Battery | 3S LiPo, 5000mAh, 30C+ | 1 |
| Camera | IMX477 / USB webcam | 1 |
| Microphone | INMP441 I2S MEMS | 1 |
| Display | 2.4" SPI TFT (ST7789) | 1 |
| Power sensor | INA219 I2C | 2 |
| Filament | PETG (structural), PLA+ (covers), TPU (feet) | — |

---

## Roadmap

- [x] Mechanical design & 3D printing `v0.1`
- [x] Basic servo control via ESP32 `v0.2`
- [x] Inverse Kinematics engine `v0.3`
- [x] Web control interface `v0.4`
- [x] Vision AI — YOLOv8 integration `v0.5`
- [x] Speech AI — Whisper + Coqui `v0.6`
- [x] Power management system `v0.7`
- [ ] Autonomous navigation `v0.8`
- [ ] SLAM mapping `v0.9`
- [ ] Emotion expression system `v1.0`
- [ ] ROS2 integration `v1.1`

---

<div align="center">

Built from scratch · Private repository · 2025

</div>
