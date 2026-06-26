<div align="center">

<img src="docs/Miscellaneous/Neurabot image 5.png" alt="NeuraBot" width="100%"/>

# 🐾 NeuraBot

**AI-Powered Quadruped Robot Dog**

[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-8A2BE2?style=flat-square&logo=raspberry-pi&logoColor=white)](https://www.raspberrypi.com)
[![MCU](https://img.shields.io/badge/MCU-Dual%20ESP32-1D9E75?style=flat-square&logo=espressif&logoColor=white)](https://www.espressif.com)
[![Vision](https://img.shields.io/badge/Vision%20AI-YOLOv5-EF9F27?style=flat-square&logo=opencv&logoColor=white)](https://ultralytics.com)
[![Speech](https://img.shields.io/badge/Speech-Whisper%20%2B%20TTS-D4537E?style=flat-square&logo=openai&logoColor=white)](https://openai.com/whisper)
[![IK](https://img.shields.io/badge/DOF-8%20Servos-378ADD?style=flat-square)](/)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=flat-square)](/)

---

*Vision · Speech · Inverse Kinematics · Web Control · Power Management*

</div>

---

## What is NeuraBot?

NeuraBot is a fully custom-built AI-powered quadruped robot dog. It walks using a real-time inverse kinematics engine, sees with YOLOv5, listens and speaks with Whisper + Google TTS, and can be controlled live from any browser. Everything — from the 3D-printed chassis to the dual ESP32 firmware — is built from scratch.

| | |
|---|---|
| 🦾 **8-DOF locomotion** | 2 joints per leg × 4 legs, driven by MG996R/DS3218 servos |
| 👁️ **Vision AI** | YOLOv5 real-time object detection at 15 fps |
| 🎙️ **Speech AI** | Whisper STT + Google TTS, wake word "NeuraBot" |
| ⚡ **Smart power system** | Dual INA219 rail monitoring, low-voltage cutoff |
| 🌐 **Web control panel** | Master Controller, gait controls via browser |
| 📺 **Onboard display** | I2C LCD face/status screen + USB mic + speaker |

---

## Gallery

### Full Unit 
To view 3D model, Click Here: [NeuraBot 3D Model]("docs/Miscellaneous/NeuraBotProject-FullBody.stl")]

<img src="docs/Miscellaneous/Neurabot image 1.jpg" alt="NeuraBot" width="100%"/>

### Build Process

| Step | Description |
|------|-----------|
| 1 | 3D printed parts — body, legs, head, mounts |
| 2 | Body frame & leg assembly |
| 3 | 8× servo installation (2 per leg) |
| 4 | Raspberry Pi & dual ESP32 mounting |
| 5 | Power distribution & LiPo bay wiring |
| 6 | Head assembly — display, camera & mic |
| 7 | Full cable routing & harness |
| 8 | First walk — IK gait test |
| 9 | Fully assembled NeuraBot |

---

## System Architecture

<img src="docs/Miscellaneous/Block Diagram-5.png" alt="NeuraBot" width="100%"/>


## Capabilities

| Module | Description |
|--------|-------------|
| 🔺 **Inverse Kinematics** | Geometric 2-DOF solver per leg. Trot, walk, sit, shake at 50 Hz |
| 👁️ **Vision AI** | YOLOv5 real-time detection with annotated web stream |
| 🎙️ **Speech AI** | Whisper STT + Google TTS with full voice command routing |
| ⚡ **Power System** | Dual INA219 monitoring, low-voltage cutoff |
| 🌐 **Web Control** | Client-Server model enables browser panel — D-pad, gaits, live camera, telemetry |
| 🔌 **Peripheral Bus** | LCD display · USB mic array · MAX98357 amp · WS2812B LEDs |

---

## Repository Structure

```
NeuraBot/

├── docs/
│   ├── Guide/           # Step-by-step assembly guide
│   ├── Architecture/    # Wiring diagrams & pinouts
│   └── Miscellaneous/   # Build photos & renders

```

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Build Guide](docs/Guide/README.md) | Full 9-step assembly from printing to first boot |
| [Power Architecture](docs/Architecture/README.md) | Power architecture |

---

## Hardware Overview

| Component | Spec | Qty |
|-----------|------|-----|
| SBC | Raspberry Pi 5 | 1 |
| MCU | ESP32 DevKit v1 | 2 |
| Servos | MG996R / DS3218MG (20 kg·cm) | 8 |
| Battery | 2S LiPo, 7000mAh, 30C+ | 1 |
| Camera | 5MP Raspberry Pi Infrared Night Vision Camera Module with OV5647 sensor | 1 |
| Microphone |  Generic USB Microphone | 1 |
| Display | 0.96" 128x64 I2C LCD Screen | 1 |
| Power sensor | INA219 I2C | 2 |
| Filament | PLA+

---

## Roadmap

- [x] Mechanical design & 3D printing `v0.1`
- [x] Basic servo control via ESP32 `v0.2`
- [x] Inverse Kinematics engine `v0.3`
- [x] Web control interface `v0.4`
- [x] Vision AI — YOLOv5 integration `v0.5`
- [x] Speech AI — Whisper + Google TTS `v0.6`
- [x] Power management system `v0.7`
- [ ] Autonomous navigation `v0.8`
- [ ] SLAM mapping `v0.9`
- [ ] Emotion expression system `v1.0`
- [ ] ROS2 integration `v1.1`

---

<div align="center">

Built from scratch · Private repository · 2025

</div>
