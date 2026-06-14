"""
NeuraBot Speech AI Module
Voice command recognition (Whisper STT) + Text-to-speech (Coqui TTS).
"""

import io
import queue
import threading
import time
import numpy as np
import sounddevice as sd
import soundfile as sf
from loguru import logger

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    logger.warning("openai-whisper not installed — STT disabled.")
    WHISPER_AVAILABLE = False

try:
    from TTS.api import TTS as CoquiTTS
    TTS_AVAILABLE = True
except ImportError:
    logger.warning("Coqui TTS not installed — TTS disabled.")
    TTS_AVAILABLE = False


# --- Voice command registry ---
COMMANDS = {
    "stand":       "stand",
    "sit":         "sit",
    "walk":        "walk",
    "forward":     "forward",
    "stop":        "stop",
    "come here":   "come_here",
    "shake":       "shake",
    "hello":       "greet",
    "what do you see": "describe_vision",
    "power":       "power_status",
}


class SpeechModule:
    """
    Runs STT and TTS in background threads.
    Recognized commands are put into a command queue for the main controller.
    """

    def __init__(self, config: dict):
        self.config = config
        self.command_queue = queue.Queue()
        self._running = False
        self._stt_thread = None
        self._tts_thread = None
        self._tts_queue = queue.Queue()

        self.sample_rate    = config.get("sample_rate", 16000)
        self.chunk_duration = config.get("chunk_duration", 3.0)  # seconds
        self.mic_device     = config.get("mic_device", None)
        self.whisper_model  = config.get("whisper_model", "base")
        self.tts_model      = config.get("tts_model", "tts_models/en/ljspeech/tacotron2-DDC")
        self.wake_word      = config.get("wake_word", "neura").lower()

        self.stt_model = None
        self.tts_engine = None

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def start(self):
        self._running = True
        if WHISPER_AVAILABLE:
            self._stt_thread = threading.Thread(target=self._stt_loop, daemon=True)
            self._stt_thread.start()
        if TTS_AVAILABLE:
            self._tts_thread = threading.Thread(target=self._tts_loop, daemon=True)
            self._tts_thread.start()
        logger.info("Speech AI module started.")

    def stop(self):
        self._running = False

    def speak(self, text: str):
        """Queue text for speech output."""
        logger.info(f"TTS: {text}")
        self._tts_queue.put(text)

    def get_command(self) -> str | None:
        """Non-blocking read of the next recognized command."""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None

    # ------------------------------------------------------------------ #
    # STT loop
    # ------------------------------------------------------------------ #

    def _stt_loop(self):
        logger.info(f"Loading Whisper model: {self.whisper_model}")
        self.stt_model = whisper.load_model(self.whisper_model)
        logger.success("Whisper ready. Listening for wake word...")

        chunk_size = int(self.sample_rate * self.chunk_duration)

        while self._running:
            try:
                audio = sd.rec(
                    chunk_size,
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype="float32",
                    device=self.mic_device,
                )
                sd.wait()

                audio_np = audio.flatten()
                result = self.stt_model.transcribe(audio_np, language="en", fp16=False)
                text = result["text"].strip().lower()

                if not text:
                    continue

                logger.debug(f"Heard: '{text}'")

                # Wake word detection
                if self.wake_word in text:
                    phrase = text.replace(self.wake_word, "").strip()
                    self._match_command(phrase)

            except Exception as e:
                logger.error(f"STT error: {e}")
                time.sleep(1.0)

    def _match_command(self, phrase: str):
        for trigger, cmd in COMMANDS.items():
            if trigger in phrase:
                logger.info(f"Command recognized: {cmd}")
                self.command_queue.put(cmd)
                return
        logger.debug(f"No command matched for: '{phrase}'")

    # ------------------------------------------------------------------ #
    # TTS loop
    # ------------------------------------------------------------------ #

    def _tts_loop(self):
        logger.info(f"Loading TTS model: {self.tts_model}")
        self.tts_engine = CoquiTTS(model_name=self.tts_model, progress_bar=False)
        logger.success("TTS engine ready.")

        while self._running:
            try:
                text = self._tts_queue.get(timeout=0.5)
                wav = self.tts_engine.tts(text=text)
                sd.play(np.array(wav, dtype="float32"), samplerate=22050)
                sd.wait()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"TTS error: {e}")
