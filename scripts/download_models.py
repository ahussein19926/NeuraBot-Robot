"""
NeuraBot Model Downloader
Downloads required AI models before first run.
"""

import subprocess
import sys
from loguru import logger


def pip_install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])


def download_yolo():
    logger.info("Downloading YOLOv8n model...")
    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")  # auto-downloads
        logger.success("YOLOv8n downloaded.")
    except Exception as e:
        logger.error(f"YOLO download failed: {e}")


def download_whisper():
    logger.info("Downloading Whisper 'base' model...")
    try:
        import whisper
        whisper.load_model("base")
        logger.success("Whisper base model downloaded.")
    except Exception as e:
        logger.error(f"Whisper download failed: {e}")


def download_tts():
    logger.info("Downloading TTS model (tacotron2-DDC)...")
    try:
        from TTS.api import TTS
        TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True)
        logger.success("TTS model downloaded.")
    except Exception as e:
        logger.error(f"TTS download failed: {e}")


if __name__ == "__main__":
    logger.info("=== NeuraBot Model Downloader ===")
    download_yolo()
    download_whisper()
    download_tts()
    logger.success("All models ready!")
