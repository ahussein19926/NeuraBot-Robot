# NeuraBot — Full Build Guide

## Table of Contents

1. [Overview & Safety](#1-overview--safety)
2. [Tools & Materials](#2-tools--materials)
3. [3D Printing Parts](#3-3d-printing-parts)
4. [Servo Preparation](#4-servo-preparation)
5. [Leg Assembly](#5-leg-assembly)
6. [Body Assembly](#6-body-assembly)
7. [Power System Wiring](#7-power-system-wiring)
8. [Electronics & SBC](#8-electronics--sbc)
9. [ESP32 Wiring](#9-esp32-wiring)
10. [Display & Audio](#10-display--audio)
11. [Camera Installation](#11-camera-installation)
12. [Firmware Flashing](#12-firmware-flashing)
13. [Software Setup](#13-software-setup)
14. [Calibration](#14-calibration)
15. [First Boot & Testing](#15-first-boot--testing)

---

## 1. Overview & Safety

NeuraBot is a 12-DOF quadruped robot. **Read this guide fully before starting.**

⚠️ **Safety warnings:**
- LiPo batteries can cause fire if shorted, overcharged, or punctured. Always use a proper LiPo charger.
- Keep the robot off the ground when testing servo motion for the first time.
- Disconnect battery when doing any wiring work.

---

## 2. Tools & Materials

See [BOM.md](../bom/BOM.md) for the full parts list.

**Required tools:**
- 3D printer (PLA+ or PETG recommended)
- Soldering iron + solder
- Heat gun or soldering iron with flat tip (for heat inserts)
- M2 and M3 hex screwdrivers
- Wire strippers, crimping tool
- Multimeter

---

## 3. 3D Printing Parts

All STL files are in `/hardware/3d_models/`.

| File | Qty | Material | Notes |
|------|-----|----------|-------|
| `body/body_main.stl` | 1 | PETG or PLA+ | Main chassis |
| `body/body_top_cover.stl` | 1 | PLA+ | Electronics cover |
| `legs/hip_bracket.stl` | 4 | PETG | Hip mount |
| `legs/thigh_link.stl` | 4 | PETG | Upper leg |
| `legs/shin_link.stl` | 4 | PETG | Lower leg |
| `legs/foot_pad.stl` | 4 | TPU 95A | Rubber-like foot pad |
| `head/head_shell.stl` | 1 | PLA+ | Head enclosure |
| `head/camera_mount.stl` | 1 | PLA+ | Camera bracket |
| `mounts/sbc_tray.stl` | 1 | PLA+ | SBC mounting tray |
| `mounts/battery_sled.stl` | 1 | PETG | Battery holder |

**Print settings:**
- Layer height: 0.2mm
- Infill: 40% (structural parts), 20% (covers)
- Supports: Yes for overhangs >45°
- Wall count: 4 perimeters on structural parts

**Heat inserts:**
- Press M3 brass heat inserts into all marked holes using a soldering iron at ~220°C
- Allow 30s to cool before moving the part

---

## 4. Servo Preparation

1. Unbox all 12 servos.
2. Center each servo by connecting to 5V + signal = 1.5ms PWM pulse, or use a servo tester.
3. Mount 25T servo horns at the neutral (centered) position.
4. Label servos FL_HIP, FL_THIGH, FL_KNEE ... RR_KNEE with masking tape.

---

## 5. Leg Assembly

Repeat for all 4 legs (FL, FR, RL, RR).

**Step 5.1 — Hip**
1. Insert HIP servo into `hip_bracket.stl`, secure with M2×8 screws.
2. Attach hip bracket to body mounting points with M3×12 screws.

**Step 5.2 — Thigh**
1. Mount THIGH servo into `thigh_link.stl`.
2. Connect thigh link to hip servo horn — use the provided M3 screw + washer.
3. Route servo cable back through the hip bracket cable channel.

**Step 5.3 — Shin & Foot**
1. Mount KNEE servo into the lower portion of `thigh_link.stl`.
2. Connect `shin_link.stl` to knee servo horn.
3. Press-fit or glue `foot_pad.stl` (TPU) to the bottom of the shin link.

**Step 5.4 — Cable routing**
- Route all servo cables through the body frame channels toward the ESP32 board.
- Use cable ties every 40mm to secure cables.

---

## 6. Body Assembly

1. Install the 4 completed leg assemblies onto the body frame using M3×16 bolts through the hip brackets.
2. Ensure FL and RL are on the left side (positive Y), FR and RR on the right.
3. Install `battery_sled.stl` on the underside of the body — slide the LiPo battery in and secure with velcro straps.
4. Mount `sbc_tray.stl` inside the body, screw down the Raspberry Pi / Jetson using M2.5 standoffs.

---

## 7. Power System Wiring

> **Always wire with battery disconnected!**

```
LiPo Battery (3S)
    │
    ├─── XT60 Connector → Main switch
    │
    ├─── 6V DC-DC BEC ──────────────→ Servo power rail (V+ bus)
    │
    ├─── 5V DC-DC Regulator ─────────→ Raspberry Pi / Jetson (USB-C)
    │
    ├─── INA219 (0x40) ──────────────→ Monitor main rail
    │
    └─── INA219 (0x41) ──────────────→ Monitor logic (5V) rail
```

1. Solder XT60 female connector to battery leads (red = +, black = −).
2. Wire battery + through main power switch.
3. Connect 6V BEC input to battery rail, output to servo power distribution bus.
4. Connect 5V regulator input to battery rail, output to SBC via USB-C.
5. Wire INA219 sensors inline with each rail — connect SDA/SCL to Raspberry Pi GPIO 2/3.
6. Set INA219 address jumpers: 0x40 (main), 0x41 (logic).

---

## 8. Electronics & SBC

1. Mount Raspberry Pi (or Jetson) in the SBC tray.
2. Connect camera to CSI ribbon connector (or USB port for USB camera).
3. Connect INA219 sensors to I2C bus (GPIO 2=SDA, 3=SCL, 3.3V, GND).
4. Connect USB to Serial adapters or UART wires for ESP32 communication.

**Raspberry Pi GPIO Map:**

| GPIO | Function |
|------|----------|
| 2 (SDA) | I2C data (INA219, display) |
| 3 (SCL) | I2C clock |
| 14 (TX) | UART to ESP32 Motion (RX) |
| 15 (RX) | UART from ESP32 Motion (TX) |
| USB | USB-to-Serial for Peripheral ESP32 |

---

## 9. ESP32 Wiring

### Motion ESP32
See [firmware/esp32_motion/README.md](../../firmware/esp32_motion/README.md) for full pinout.

- Connect 12 servo signal wires to ESP32 GPIO pins per the pinout table.
- Power all servo + lines to 6V BEC rail.
- Power all servo − lines to GND bus.
- ESP32 powered from 5V logic rail via VIN pin.
- UART wires: ESP32 GPIO16 (RX) → Pi TX, ESP32 GPIO17 (TX) → Pi RX.

### Peripheral ESP32
- SPI to display (CLK, MOSI, CS, DC, RST).
- I2S to microphone (SCK, WS, SD).
- I2S to amplifier/speaker (BCLK, LRC, DIN).
- WS2812B data line to LED strip.

---

## 10. Display & Audio

1. Mount the TFT display inside `head_shell.stl`, secure with M2 screws.
2. Glue or mount the speaker in the head shell.
3. Mount the microphone in a forward-facing cutout in the head.
4. Mount camera in `camera_mount.stl` at the front of the head.
5. Snap/screw the head shell onto the body frame.

---

## 11. Camera Installation

1. Route the camera ribbon cable through the neck channel to the SBC.
2. For USB camera: route USB cable and connect to Raspberry Pi.
3. Angle camera slightly downward (~10–15°) for better ground-level view.

---

## 12. Firmware Flashing

### ESP32 Motion
```bash
cd firmware/esp32_motion
pip install platformio
pio run --target upload --upload-port /dev/ttyUSB0
```

### ESP32 Peripherals
```bash
cd firmware/esp32_peripherals
pio run --target upload --upload-port /dev/ttyUSB1
```

---

## 13. Software Setup

On the Raspberry Pi / Jetson:

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/NeuraBot.git
cd NeuraBot

# Install Python dependencies
pip install -r requirements.txt

# Copy and configure
cp config/config.example.yaml config/config.yaml
nano config/config.yaml

# Download AI models
python scripts/download_models.py
```

---

## 14. Calibration

```bash
python scripts/calibrate_servos.py
```

This script:
1. Sets all servos to neutral (0°).
2. Steps through each servo so you can verify range of motion.
3. Saves trim values to `config/servo_trims.yaml`.

Also run:
```bash
python scripts/test_ik.py     # Verify IK for each leg
python scripts/test_power.py  # Verify INA219 readings
```

---

## 15. First Boot & Testing

```bash
# Start NeuraBot
python src/main.py

# Open web control panel in browser
http://<robot-ip>:5000
```

**First test sequence:**
1. Stand — verify posture looks correct.
2. Sit — verify rear legs lower properly.
3. Slow walk — verify all 4 legs move smoothly.
4. Say "Neura hello" — verify speech recognition responds.
5. Check camera feed in web panel — verify Vision AI detection overlay.
6. Check battery voltage in status panel.

---

*🐾 Congratulations — NeuraBot is alive!*
