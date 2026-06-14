<div align="center">
🐾 NEURABOT
AI-Powered Quadruped Robot Dog
VISION · SPEECH · GAIT · AUTONOMY
---
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20%2F%20Jetson-8A2BE2?style=for-the-badge&logo=raspberry-pi&logoColor=white)
![MCU](https://img.shields.io/badge/MCU-Dual%20ESP32-1D9E75?style=for-the-badge&logo=espressif&logoColor=white)
![Vision](https://img.shields.io/badge/Vision-YOLOv8-EF9F27?style=for-the-badge&logo=opencv&logoColor=white)
![Speech](https://img.shields.io/badge/Speech-Whisper%20%2B%20Coqui-D4537E?style=for-the-badge&logo=openai&logoColor=white)
![DOF](https://img.shields.io/badge/DOF-12%20Servos-378ADD?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)
---
SERVOS	IK RATE	VISION AI	LEGS	BATTERY
12	50 Hz	15 fps	4	3S LiPo
</div>
---
01 · UNIT OVERVIEW
> 📸 **Add your robot photo here**
> `docs/images/neurabot_hero.jpg`
<!--- Replace this line with: ![NeuraBot](docs/images/neurabot_hero.jpg) --->
---
02 · BUILD GALLERY
> Drop your build photos into `docs/images/` and replace each placeholder below.
		
![Chassis](https://placehold.co/320x240/0d1117/7F77DD?text=STRUC+%2F%2F+CHASSIS)	![Servos](https://placehold.co/320x240/0d1117/1D9E75?text=ACT+%2F%2F+SERVOS)	![Power](https://placehold.co/320x240/0d1117/EF9F27?text=PWR+%2F%2F+POWER+SYS)
Body frame & leg assembly	12× servo installation	Power distribution & LiPo bay
`build_chassis.jpg`	`build_servos.jpg`	`build_power.jpg`
![Electronics](https://placehold.co/320x240/0d1117/378ADD?text=COMP+%2F%2F+SBC+%2B+ESP32)	![Head](https://placehold.co/320x240/0d1117/D4537E?text=PERIPH+%2F%2F+HEAD)	![Wiring](https://placehold.co/320x240/0d1117/7F77DD?text=WIRE+%2F%2F+HARNESS)
Raspberry Pi & dual ESP32 mount	Display, camera & mic array	Cable routing & wiring harness
`build_electronics.jpg`	`build_head.jpg`	`build_wiring.jpg`
![3D Parts](https://placehold.co/320x240/0d1117/1D9E75?text=3DP+%2F%2F+PARTS)	![Gait](https://placehold.co/320x240/0d1117/EF9F27?text=IK+%2F%2F+GAIT+TEST)	![Final](https://placehold.co/320x240/0d1117/378ADD?text=FINAL+%2F%2F+COMPLETE)
3D printed components laid out	First walk — IK gait in action	Fully assembled NeuraBot
`build_3dparts.jpg`	`build_gait_test.jpg`	`build_final.jpg`
---
03 · CAPABILITY MATRIX
Module	ID	Description
🔺 Inverse Kinematics	`MOD // IK-ENGINE`	Geometric 3-DOF solver per leg. Trot, walk, sit, shake gaits at 50 Hz
👁️ Vision AI	`MOD // VISION-AI`	YOLOv8n real-time detection. Annotated frame stream to web panel
🎙️ Speech AI	`MOD // SPEECH-AI`	Whisper STT + Coqui TTS. Wake word "Neura". Full command routing
⚡ Power System	`MOD // POWER-SYS`	Dual INA219 rail monitoring. SOC estimation. Low-voltage cutoff
🌐 Web Control	`MOD // WEB-CTRL`	SocketIO panel. D-pad, gait actions, live camera, live telemetry
🔌 Peripheral Bus	`MOD // PERIPH-BUS`	TFT display · I2S mic · MAX98357 amp · WS2812B NeoPixels
---
04 · SYSTEM ARCHITECTURE
```
┌─────────────────────────────────────────────────────────┐
│         LAYER 2 — HIGH-LEVEL BRAIN                      │
│              Raspberry Pi / Jetson                      │
│                                                         │
│  ┌───────────┐  ┌───────────┐  ┌────────┐  ┌────────┐  │
│  │ Vision AI │  │ Speech AI │  │IK+Gait │  │Web+Pwr │  │
│  │  YOLOv8  │  │  Whisper  │  │ 50 Hz  │  │ Flask  │  │
│  └───────────┘  └───────────┘  └────────┘  └────────┘  │
└────────────────────┬───────────────────┬────────────────┘
                     │  UART 115200      │  UART / I2C
         ┌───────────▼──────┐   ┌────────▼──────────────┐
         │  LAYER 1 — ESP32 │   │  LAYER 1 — ESP32      │
         │  Motion Ctrl     │   │  Peripheral Ctrl       │
         │  12× Servos      │   │  TFT · Mic · Speaker   │
         └───────────┬──────┘   └────────┬──────────────┘
                     └────────┬──────────┘
              ┌───────────────▼───────────────┐
              │     LAYER 0 — HARDWARE        │
              │  3S LiPo · Servos · IMX477    │
              │  INMP441 · PETG/PLA+ Chassis  │
              └───────────────────────────────┘
```
---
05 · MISSION ROADMAP
Status	Milestone	Version
✅	Mechanical design & 3D printing	`v0.1`
✅	Basic servo control via ESP32	`v0.2`
✅	Inverse Kinematics engine	`v0.3`
✅	Web control interface	`v0.4`
✅	Vision AI — YOLOv8 integration	`v0.5`
✅	Speech AI — Whisper + Coqui	`v0.6`
✅	Power management system	`v0.7`
🔵	Autonomous navigation	`v0.8`
⬜	SLAM mapping	`v0.9`
⬜	Emotion expression system	`v1.0`
⬜	ROS2 integration	`v1.1`
---
06 · REPOSITORY STRUCTURE
```
NeuraBot/
├── src/
│   ├── ai/
│   │   ├── vision/          # YOLOv8 vision module
│   │   └── speech/          # Whisper STT + Coqui TTS
│   ├── ik/                  # Inverse Kinematics engine
│   ├── control/             # Gait controller + ESP32 comms
│   ├── power/               # INA219 power monitor
│   └── web/                 # Flask web control panel
├── firmware/
│   ├── esp32_motion/        # C++ servo firmware
│   └── esp32_peripherals/   # Display, audio, LEDs
├── hardware/
│   ├── 3d_models/           # STL / CAD files
│   ├── pcb/                 # PCB schematics
│   └── bom/                 # Bill of materials
├── docs/
│   ├── build_guide/         # Step-by-step assembly
│   ├── wiring/              # Wiring diagrams
│   └── images/              # Photos & renders
├── config/                  # config.yaml
├── scripts/                 # Calibration & setup tools
└── tests/                   # Unit tests
```
---
07 · QUICK START
```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/NeuraBot.git && cd NeuraBot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Flash ESP32 firmware
cd firmware/esp32_motion && pio run --target upload

# 4. Configure
cp config/config.example.yaml config/config.yaml

# 5. Download AI models
python scripts/download_models.py

# 6. Calibrate servos
python scripts/calibrate_servos.py

# 7. Launch
python src/main.py
```
---
<div align="center">
NEURABOT · Private Repository · Open Build · REV 2025.06
</div>
