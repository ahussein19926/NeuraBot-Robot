"""
NeuraBot Vision AI Module
Real-time object detection and tracking using YOLOv8.
"""

import cv2
import threading
import time
import numpy as np
from dataclasses import dataclass, field
from loguru import logger

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    logger.warning("ultralytics not installed — Vision AI disabled.")
    YOLO_AVAILABLE = False


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: tuple        # (x1, y1, x2, y2)
    center: tuple      # (cx, cy)
    distance_est: float = 0.0  # rough distance in meters (if depth available)


@dataclass
class VisionState:
    detections: list[Detection] = field(default_factory=list)
    frame: np.ndarray = None
    fps: float = 0.0
    timestamp: float = 0.0


class VisionModule:
    """
    Runs YOLOv8 inference on camera frames in a background thread.
    Maintains a shared VisionState accessible by other modules.
    """

    def __init__(self, config: dict):
        self.config = config
        self.state = VisionState()
        self._running = False
        self._thread = None
        self._lock = threading.Lock()

        self.model_path  = config.get("model_path", "yolov8n.pt")
        self.camera_idx  = config.get("camera_index", 0)
        self.conf_thresh = config.get("confidence_threshold", 0.45)
        self.img_size    = config.get("image_size", 640)
        self.target_fps  = config.get("target_fps", 15)

        self.model = None
        self.cap   = None

    def start(self):
        if not YOLO_AVAILABLE:
            logger.warning("Vision AI skipped (ultralytics not available).")
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("Vision AI module started.")

    def stop(self):
        self._running = False
        if self.cap:
            self.cap.release()
        logger.info("Vision AI module stopped.")

    def get_state(self) -> VisionState:
        with self._lock:
            return self.state

    def get_detections(self) -> list[Detection]:
        with self._lock:
            return list(self.state.detections)

    def _run(self):
        logger.info(f"Loading YOLO model: {self.model_path}")
        self.model = YOLO(self.model_path)

        self.cap = cv2.VideoCapture(self.camera_idx)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, self.target_fps)

        interval = 1.0 / self.target_fps
        prev = time.time()

        while self._running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue

            results = self.model(
                frame,
                imgsz=self.img_size,
                conf=self.conf_thresh,
                verbose=False,
            )[0]

            detections = []
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf  = float(box.conf[0])
                cls   = int(box.cls[0])
                label = self.model.names[cls]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                detections.append(Detection(
                    label=label,
                    confidence=conf,
                    bbox=(x1, y1, x2, y2),
                    center=(cx, cy),
                ))

            now = time.time()
            fps = 1.0 / max(now - prev, 1e-6)
            prev = now

            with self._lock:
                self.state = VisionState(
                    detections=detections,
                    frame=frame.copy(),
                    fps=fps,
                    timestamp=now,
                )

            elapsed = time.time() - now
            sleep_t = max(0.0, interval - elapsed)
            time.sleep(sleep_t)

    def annotated_frame(self) -> np.ndarray:
        """Return current frame with bounding boxes drawn."""
        state = self.get_state()
        if state.frame is None:
            return None
        frame = state.frame.copy()
        for d in state.detections:
            x1, y1, x2, y2 = d.bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{d.label} {d.confidence:.2f}",
                        (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"FPS: {state.fps:.1f}",
                    (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
        return frame
