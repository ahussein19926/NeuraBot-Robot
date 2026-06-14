# NeuraBot — Bill of Materials (BOM)

> Last updated: 2025

## 🧠 Computing

| # | Component | Specification | Qty | Notes |
|---|-----------|--------------|-----|-------|
| 1 | SBC | Raspberry Pi 5 (8GB) or NVIDIA Jetson Nano / Orin NX | 1 | Main brain |
| 2 | MCU — Motion | ESP32 DevKit v1 | 1 | Servo control |
| 3 | MCU — Peripherals | ESP32 DevKit v1 | 1 | Display, audio, LEDs |
| 4 | Storage | 64GB+ microSD (A2 rated) or NVMe SSD | 1 | OS + models |

## 🦾 Actuators

| # | Component | Specification | Qty | Notes |
|---|-----------|--------------|-----|-------|
| 5 | Servos | MG996R or DS3218MG (20kg·cm) | 12 | 3 per leg |

## ⚡ Power System

| # | Component | Specification | Qty | Notes |
|---|-----------|--------------|-----|-------|
| 6 | Battery | 3S LiPo, 3000–5000mAh, 30C+ | 1–2 | Main power |
| 7 | BEC / Regulator | 5V 5A DC-DC (for SBC) | 1 | |
| 8 | Servo power rail | 6–7.4V DC-DC or direct 2S LiPo | 1 | |
| 9 | Power sensor | INA219 I2C module | 2 | Main + logic rails |
| 10 | Power switch | XT60 connector + main switch | 1 | |
| 11 | Battery charger | LiPo balance charger (B6 or similar) | 1 | |

## 📡 Sensors & Perception

| # | Component | Specification | Qty | Notes |
|---|-----------|--------------|-----|-------|
| 12 | Camera | Raspberry Pi Camera v3 / IMX477 / USB webcam | 1 | Vision AI |
| 13 | Microphone | USB mic or I2S MEMS mic array (INMP441) | 1 | Speech input |
| 14 | IMU | MPU6050 or BNO055 (I2C) | 1 | Optional: balance sensing |

## 🖥️ Peripherals / Display

| # | Component | Specification | Qty | Notes |
|---|-----------|--------------|-----|-------|
| 15 | Display | 2.4" SPI TFT (ST7789) or OLED 128×64 | 1 | Face / status |
| 16 | Speaker | 3W 4Ω mini speaker | 1 | Audio output |
| 17 | Amplifier | MAX98357 I2S DAC/Amp or PAM8403 | 1 | |
| 18 | LEDs | WS2812B NeoPixel strip/ring | 1 | Accent lighting |

## 🏗️ Structure

| # | Component | Specification | Qty | Notes |
|---|-----------|--------------|-----|-------|
| 19 | Body / chassis | 3D printed (PLA+/PETG) | 1 set | See `/hardware/3d_models/` |
| 20 | Screws | M2, M3 hex socket set | 1 set | |
| 21 | Servo horns | 25T type, matching servos | 12 | |
| 22 | Heat inserts | M3 brass heat inserts | 30+ | For structural parts |
| 23 | Servo cables | Extension cables 15–20cm | 12 | |

## 🔌 Wiring / Connectors

| # | Component | Specification | Qty | Notes |
|---|-----------|--------------|-----|-------|
| 24 | XT60 connectors | Male + Female pair | 2 | Battery connections |
| 25 | JST connectors | JST-PH 2.0 / JST-XH | 1 set | Power distribution |
| 26 | Dupont cables | F-F, M-F, M-M sets | 1 set | GPIO connections |
| 27 | USB-A to USB-C | Data + power | 2 | SBC connections |
| 28 | Silicone wire | 16AWG (power), 24AWG (signal) | 2m each | |

## 🔧 Tools Required

- 3D printer (minimum 220×220mm bed)
- Soldering iron
- Heat gun (for heat inserts)
- Multimeter
- M2/M3 hex drivers
- LiPo battery checker

---

## 💰 Estimated Cost

| Category | Estimated Cost (USD) |
|----------|---------------------|
| Computing (Pi 5 + 2× ESP32) | $80–120 |
| Servos (12×) | $40–80 |
| Power system | $30–50 |
| Sensors & camera | $20–50 |
| Display & audio | $15–30 |
| 3D printing filament | $20–40 |
| Fasteners, wiring, misc | $20–30 |
| **Total (estimate)** | **$225–400** |

> Costs vary by supplier. Check AliExpress, Amazon, or local electronics stores.
