"""
NeuraBot Gait Controller
Generates trot, walk, and stand gaits using the IK engine.
"""

import time
import math
import threading
from enum import Enum
from loguru import logger

from src.ik.ik_engine import QuadrupedIK, LegConfig, FootPosition


class Gait(Enum):
    STAND   = "stand"
    TROT    = "trot"
    WALK    = "walk"
    SIT     = "sit"
    SHAKE   = "shake"


class GaitController:
    def __init__(self, config: dict, comm):
        self.config = config
        self.comm = comm
        self.current_gait = Gait.STAND
        self.running = False
        self._thread = None
        self._lock = threading.Lock()

        leg_cfg = LegConfig(
            hip_offset=config["leg"]["hip_offset"],
            thigh_len=config["leg"]["thigh_len"],
            shin_len=config["leg"]["shin_len"],
        )
        self.ik = QuadrupedIK(leg_cfg)
        self.body_height = config.get("default_height", 0.15)
        self.speed = config.get("default_speed", 1.0)

        # Velocity commands
        self.vx = 0.0   # forward/backward
        self.vy = 0.0   # lateral
        self.wz = 0.0   # yaw rate

    def set_velocity(self, vx=0.0, vy=0.0, wz=0.0):
        with self._lock:
            self.vx = vx
            self.vy = vy
            self.wz = wz
            if abs(vx) > 0.01 or abs(vy) > 0.01 or abs(wz) > 0.01:
                self.current_gait = Gait.TROT
            else:
                self.current_gait = Gait.STAND

    def set_gait(self, gait: Gait):
        with self._lock:
            self.current_gait = gait
        logger.info(f"Gait changed to: {gait.value}")

    def set_height(self, height: float):
        self.body_height = max(0.08, min(0.22, height))

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("Gait controller started.")

    def stop(self):
        self.running = False

    def _loop(self):
        t = 0.0
        dt = 0.02  # 50Hz

        while self.running:
            with self._lock:
                gait = self.current_gait
                vx, vy, wz = self.vx, self.vy, self.wz

            if gait == Gait.STAND:
                foot_pos = self.ik.default_stance(self.body_height)
            elif gait == Gait.TROT:
                foot_pos = self._trot_step(t, vx, vy, wz)
            elif gait == Gait.SIT:
                foot_pos = self._sit_pose()
            else:
                foot_pos = self.ik.default_stance(self.body_height)

            angles = self.ik.solve_all(foot_pos)
            self._send_angles(angles)

            t += dt
            time.sleep(dt)

    def _trot_step(self, t: float, vx: float, vy: float, wz: float) -> dict:
        """Diagonal trot gait — FL+RR swing together, FR+RL swing together."""
        freq = 2.0 * self.speed
        stride = 0.04
        lift  = 0.03

        phase = {"FL": 0.0, "RR": 0.0, "FR": 0.5, "RL": 0.5}
        stance = self.ik.default_stance(self.body_height)
        foot_pos = {}

        for leg, ph in phase.items():
            s = math.sin(2 * math.pi * (freq * t + ph))
            c = math.cos(2 * math.pi * (freq * t + ph))
            swing = s > 0

            base = stance[leg]
            dx = vx * stride * c
            dy = vy * stride * c
            dz = lift * max(0, s) if swing else 0.0

            foot_pos[leg] = FootPosition(
                x=base.x + dx,
                y=base.y + dy,
                z=base.z - dz,
            )

        return foot_pos

    def _sit_pose(self) -> dict:
        stance = self.ik.default_stance(self.body_height)
        # Lower rear legs, keep front up
        stance["RL"].z -= 0.05
        stance["RR"].z -= 0.05
        return stance

    def _send_angles(self, angles: dict):
        """Send joint angles to ESP32 motion controller."""
        payload = {}
        for leg, a in angles.items():
            payload[leg] = {
                "hip":   round(math.degrees(a.hip), 1),
                "thigh": round(math.degrees(a.thigh), 1),
                "knee":  round(math.degrees(a.knee), 1),
            }
        self.comm.send_motion(payload)
