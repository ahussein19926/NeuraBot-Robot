"""
NeuraBot — Main Entry Point
Starts all subsystems and coordinates the robot brain.
"""

import time
import signal
import sys
import yaml
from loguru import logger

from src.control.gait_controller import GaitController
from src.ai.vision.vision_module import VisionModule
from src.ai.speech.speech_module import SpeechModule
from src.power.power_monitor import PowerMonitor
from src.web.web_server import WebServer
from src.control.comm_manager import CommManager


def load_config(path: str = "config/config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def shutdown_handler(sig, frame):
    logger.warning("Shutdown signal received. Stopping NeuraBot...")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    logger.info("🐾 NeuraBot starting up...")

    config = load_config()

    # Initialize communication with ESP32s
    comm = CommManager(config["comm"])
    comm.connect()

    # Initialize subsystems
    power   = PowerMonitor(config["power"])
    gait    = GaitController(config["gait"], comm)
    vision  = VisionModule(config["vision"])
    speech  = SpeechModule(config["speech"])
    web     = WebServer(config["web"], gait, vision, speech, power)

    # Start all subsystems
    power.start()
    vision.start()
    speech.start()
    web.start()

    logger.success("✅ NeuraBot is online!")

    # Main loop
    try:
        while True:
            power.check()
            time.sleep(0.05)
    except SystemExit:
        logger.info("Shutting down subsystems...")
        vision.stop()
        speech.stop()
        web.stop()
        comm.disconnect()
        logger.info("NeuraBot offline. Goodbye! 🐾")


if __name__ == "__main__":
    main()
