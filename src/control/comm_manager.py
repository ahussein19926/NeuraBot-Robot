"""
NeuraBot Communication Manager
Handles serial UART communication between Raspberry Pi/Jetson and ESP32s.
"""

import json
import threading
import serial
import time
from loguru import logger


class CommManager:
    """
    Manages two serial connections:
      - motion_port  → ESP32 Motion (servos / gait)
      - periph_port  → ESP32 Peripherals (display, mic, speaker, LEDs)

    Protocol: newline-delimited JSON over UART.
    """

    def __init__(self, config: dict):
        self.motion_port  = config.get("motion_port",  "/dev/ttyUSB0")
        self.periph_port  = config.get("periph_port",  "/dev/ttyUSB1")
        self.baud         = config.get("baud_rate",    115200)
        self.timeout      = config.get("timeout",      0.1)

        self._motion_ser  = None
        self._periph_ser  = None
        self._lock_m      = threading.Lock()
        self._lock_p      = threading.Lock()

    def connect(self):
        try:
            self._motion_ser = serial.Serial(self.motion_port, self.baud, timeout=self.timeout)
            logger.success(f"Motion ESP32 connected on {self.motion_port}")
        except serial.SerialException as e:
            logger.warning(f"Motion ESP32 not available ({e}) — mock mode.")

        try:
            self._periph_ser = serial.Serial(self.periph_port, self.baud, timeout=self.timeout)
            logger.success(f"Peripheral ESP32 connected on {self.periph_port}")
        except serial.SerialException as e:
            logger.warning(f"Peripheral ESP32 not available ({e}) — mock mode.")

    def disconnect(self):
        if self._motion_ser and self._motion_ser.is_open:
            self._motion_ser.close()
        if self._periph_ser and self._periph_ser.is_open:
            self._periph_ser.close()
        logger.info("Serial connections closed.")

    def send_motion(self, angles: dict):
        """Send joint angles to ESP32 motion controller."""
        msg = json.dumps({"t": "angles", "d": angles}) + "\n"
        self._write(self._motion_ser, self._lock_m, msg)

    def send_display(self, text: str = None, emotion: str = None):
        """Update onboard display via ESP32 peripherals."""
        payload = {"t": "display"}
        if text:    payload["text"] = text
        if emotion: payload["emo"]  = emotion
        self._write(self._periph_ser, self._lock_p, json.dumps(payload) + "\n")

    def send_led(self, r: int, g: int, b: int, pattern: str = "solid"):
        """Control RGB LEDs."""
        msg = json.dumps({"t": "led", "r": r, "g": g, "b": b, "p": pattern}) + "\n"
        self._write(self._periph_ser, self._lock_p, msg)

    def _write(self, ser, lock, msg: str):
        if ser is None:
            return  # mock mode
        with lock:
            try:
                ser.write(msg.encode("utf-8"))
            except serial.SerialException as e:
                logger.error(f"Serial write error: {e}")

    def read_motion_feedback(self) -> dict | None:
        """Read any incoming feedback from motion ESP32."""
        return self._read(self._motion_ser, self._lock_m)

    def _read(self, ser, lock) -> dict | None:
        if ser is None:
            return None
        with lock:
            try:
                if ser.in_waiting:
                    line = ser.readline().decode("utf-8").strip()
                    return json.loads(line)
            except Exception:
                pass
        return None
