"""
NeuraBot Power Monitor
Reads voltage, current, and power from INA219 sensors.
Manages battery safety cutoffs and alerts.
"""

import threading
import time
from dataclasses import dataclass
from loguru import logger

try:
    from ina219 import INA219, DeviceRangeError
    INA_AVAILABLE = True
except ImportError:
    logger.warning("ina219 library not available — using mock power data.")
    INA_AVAILABLE = False


@dataclass
class PowerReading:
    bus_voltage:    float  # V
    shunt_voltage:  float  # mV
    current:        float  # mA
    power:          float  # mW
    soc_percent:    float  # State of charge estimate


class PowerMonitor:
    """
    Monitors NeuraBot's power system via INA219 I2C sensors.

    Supports:
    - Main battery rail monitoring
    - 5V logic rail monitoring
    - Low-battery alerts & emergency shutdown trigger
    """

    # Battery voltage thresholds (3S LiPo)
    CELL_COUNT    = 3
    FULL_VOLTAGE  = 4.2 * CELL_COUNT   # 12.6V
    NOMINAL_V     = 3.7 * CELL_COUNT   # 11.1V
    CUTOFF_V      = 3.3 * CELL_COUNT   # 9.9V
    WARNING_V     = 3.5 * CELL_COUNT   # 10.5V

    def __init__(self, config: dict):
        self.config = config
        self._lock = threading.Lock()
        self._main_reading = PowerReading(0, 0, 0, 0, 100)
        self._logic_reading = PowerReading(0, 0, 0, 0, 100)
        self._low_battery_cb = None

        self.main_ina  = None
        self.logic_ina = None

        if INA_AVAILABLE:
            try:
                self.main_ina = INA219(
                    shunt_ohms=config.get("main_shunt_ohms", 0.1),
                    max_expected_amps=config.get("main_max_amps", 10.0),
                    address=config.get("main_i2c_addr", 0x40),
                )
                self.main_ina.configure()
                logger.info("Main INA219 initialized.")
            except Exception as e:
                logger.warning(f"Main INA219 init failed: {e}")

            try:
                self.logic_ina = INA219(
                    shunt_ohms=config.get("logic_shunt_ohms", 0.1),
                    max_expected_amps=config.get("logic_max_amps", 3.0),
                    address=config.get("logic_i2c_addr", 0x41),
                )
                self.logic_ina.configure()
                logger.info("Logic INA219 initialized.")
            except Exception as e:
                logger.warning(f"Logic INA219 init failed: {e}")

    def on_low_battery(self, callback):
        """Register a callback invoked when battery is critically low."""
        self._low_battery_cb = callback

    def start(self):
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("Power monitor started.")

    def check(self):
        """Called by main loop to process pending alerts."""
        pass  # Alerts are handled inside _loop

    def get_main(self) -> PowerReading:
        with self._lock:
            return self._main_reading

    def get_logic(self) -> PowerReading:
        with self._lock:
            return self._logic_reading

    def _loop(self):
        while True:
            main  = self._read_sensor(self.main_ina,  "Main")
            logic = self._read_sensor(self.logic_ina, "Logic")

            with self._lock:
                self._main_reading  = main
                self._logic_reading = logic

            # Battery safety checks
            if main.bus_voltage > 0:
                if main.bus_voltage < self.CUTOFF_V:
                    logger.critical(f"⚠️  CRITICAL BATTERY: {main.bus_voltage:.2f}V — initiating shutdown!")
                    if self._low_battery_cb:
                        self._low_battery_cb()
                elif main.bus_voltage < self.WARNING_V:
                    logger.warning(f"🔋 Low battery: {main.bus_voltage:.2f}V ({main.soc_percent:.0f}%)")

            time.sleep(2.0)

    def _read_sensor(self, sensor, label: str) -> PowerReading:
        if sensor is None or not INA_AVAILABLE:
            return self._mock_reading()
        try:
            v = sensor.voltage()
            c = sensor.current()
            p = sensor.power()
            sv = sensor.shunt_voltage()
            soc = self._estimate_soc(v)
            return PowerReading(bus_voltage=v, shunt_voltage=sv,
                                current=c, power=p, soc_percent=soc)
        except DeviceRangeError as e:
            logger.warning(f"{label} INA219 range error: {e}")
            return self._mock_reading()
        except Exception as e:
            logger.error(f"{label} INA219 read error: {e}")
            return self._mock_reading()

    def _mock_reading(self) -> PowerReading:
        return PowerReading(bus_voltage=11.8, shunt_voltage=2.5,
                            current=1200, power=14160, soc_percent=82)

    def _estimate_soc(self, voltage: float) -> float:
        """Simple linear SOC estimate."""
        soc = (voltage - self.CUTOFF_V) / (self.FULL_VOLTAGE - self.CUTOFF_V) * 100
        return max(0.0, min(100.0, soc))
