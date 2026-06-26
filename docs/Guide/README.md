<div align="left">

<img src="docs/Guide/NeuraBotProject-V1.png" alt="NeuraBot" width="100%"/>

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

---

## 1. Overview & Safety

NeuraBot is a 8-DOF quadruped robot. **Read this guide fully before starting.**

⚠️ **Safety warnings:**
- LiPo batteries can cause fire if shorted, overcharged, or punctured. Always use a proper LiPo charger.
- Keep the robot off the ground when testing servo motion for the first time.
- Disconnect battery when doing any wiring work.

---

## 2. Tools & Materials

**Required tools:**
- 3D printer (PLA+ or PETG recommended)
- Soldering iron + solder
- Heat gun or soldering iron with flat tip (for heat inserts)
- M2 and M3 hex screwdrivers
- Wire strippers, crimping tool
- Multimeter

---

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
    ├─── 7.4V DC-DC BEC ──────────────→ Servo power rail (V+ bus)
    │
    ├─── 5V DC-DC Regulator ─────────→ Raspberry Pi / Jetson (USB-C)
    │
    ├─── INA219 (0x40) ──────────────→ Monitor main rail
    │
    └─── INA219 (0x41) ──────────────→ Monitor logic (5V) rail
```

1. Solder XT60 female connector to battery leads (red = +, black = −).
2. Wire battery + through main power switch.
3. Connect 7.4V BEC input to battery rail, output to servo power distribution bus.
4. Connect 5V regulator input to battery rail, output to SBC via USB-C.
5. Wire INA219 sensors inline with each rail — connect SDA/SCL to Raspberry Pi GPIO 2/3.
6. Set INA219 address jumpers: 0x40 (main), 0x41 (logic).

---

## 8. Electronics & SBC

1. Mount Raspberry Pi (or Jetson) in the SBC tray.
2. Connect camera to CSI ribbon connector (or USB port for USB camera).
3. Connect INA219 sensors to I2C bus
4. Connect USB to Serial adapters or UART wires for ESP32 communication.

---

## 9. ESP32 Wiring

- Connect 8x servo signal wires to ESP32 GPIO pins per the pinout table.
- Power all servo + lines to 7.4V BEC rail.
- Power all servo − lines to GND bus.
- ESP32 powered from 5V logic rail via VIN pin.

---

**First test sequence:**
1. Stand — verify posture looks correct.
2. Sit — verify rear legs lower properly.
3. Slow walk — verify all 4 legs move smoothly.
4. Say "NeuraBot hello" — verify speech recognition responds.
5. Check camera feed in web panel — verify Vision AI detection overlay.
6. Check battery voltage in status panel.

---

*🐾 Congratulations — NeuraBot is alive!*
