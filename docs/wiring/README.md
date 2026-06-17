# NeuraBot — Wiring Guide

## Power Architecture

<img src="docs/images/Power diagram.png" width="100%"/>

## Raspberry Pi GPIO Pinout

```
Pi GPIO Header (26-pin subset shown)
Pin  1: 3.3V  ────────────── INA219 VCC, ESP32 3.3V ref
Pin  2: 5V    ────────────── Power input from BEC/regulator
Pin  6: GND   ────────────── Common ground
Pin  8: TX    ────────────── → ESP32 Motion GPIO16 (RX)
Pin 10: RX    ────────────── ← ESP32 Motion GPIO17 (TX)
Pin  3: SDA   ────────────── INA219 SDA (both sensors)
Pin  5: SCL   ────────────── INA219 SCL (both sensors)
```

---

## ESP32 Motion — Servo Wiring

Connect servo signal wires to ESP32 GPIOs. Servo power (red) to 6V rail, ground (black/brown) to GND rail.

```
GPIO 13 ── FL Hip  servo signal
GPIO 12 ── FL Thigh servo signal
GPIO 14 ── FL Knee  servo signal

GPIO 27 ── FR Hip  servo signal
GPIO 26 ── FR Thigh servo signal
GPIO 25 ── FR Knee  servo signal

GPIO 33 ── RL Hip  servo signal
GPIO 32 ── RL Thigh servo signal
GPIO 35 ── RL Knee  servo signal

GPIO 34 ── RR Hip  servo signal
GPIO 21 ── RR Thigh servo signal
GPIO 22 ── RR Knee  servo signal
```

---

## ESP32 Peripherals — Peripheral Wiring

### TFT Display (ST7789, SPI)
```
ESP32 GPIO 18 (SCK)  ── Display CLK
ESP32 GPIO 23 (MOSI) ── Display MOSI
ESP32 GPIO  5 (CS)   ── Display CS
ESP32 GPIO  2        ── Display DC
ESP32 GPIO  4        ── Display RST
ESP32 3.3V           ── Display VCC
ESP32 GND            ── Display GND
```

### I2S Microphone (INMP441)
```
ESP32 GPIO 26 ── MIC SCK (clock)
ESP32 GPIO 22 ── MIC WS  (word select)
ESP32 GPIO 34 ── MIC SD  (data in)
3.3V             ── MIC VDD
GND              ── MIC GND + L/R (to GND for left channel)
```

### I2S Amplifier (MAX98357A)
```
ESP32 GPIO 27 ── AMP BCLK
ESP32 GPIO 25 ── AMP LRC
ESP32 GPIO 32 ── AMP DIN
5V               ── AMP VIN
GND              ── AMP GND
AMP + / −        ── Speaker terminals
```

### WS2812B LEDs
```
ESP32 GPIO 33 ── LED Data In
5V              ── LED VCC
GND             ── LED GND
```

---

## INA219 Power Sensors (I2C)

Two INA219 modules on shared I2C bus.

```
INA219 #1 (Address 0x40 — Main Rail Monitor)
  VCC ── Pi 3.3V
  GND ── GND
  SDA ── Pi GPIO 2 (SDA)
  SCL ── Pi GPIO 3 (SCL)
  V+  ── Battery (+) after switch
  V−  ── 6V BEC input (+)

INA219 #2 (Address 0x41 — Logic Rail Monitor)
  VCC ── Pi 3.3V
  GND ── GND
  SDA ── Pi GPIO 2 (SDA, same bus)
  SCL ── Pi GPIO 3 (SCL, same bus)
  V+  ── 5V regulator output
  V−  ── Pi 5V input

Address configuration:
  0x40 = A0:GND, A1:GND (default)
  0x41 = A0:VCC, A1:GND
```

---

## Wiring Tips

1. **Use color coding**: Red = power, Black = ground, Yellow = signal.
2. **Twist signal+ground pairs** for servo wires to reduce noise.
3. **Add 100µF capacitor** across servo power rail close to ESP32.
4. **Fuse the battery output** with a 15–20A blade fuse for protection.
5. **Secure all cables** with cable ties every 40mm to prevent snagging.
