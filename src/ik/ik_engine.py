"""
NeuraBot Inverse Kinematics Engine
Calculates joint angles for each leg given a target foot position.

Leg numbering:
    0: Front-Left   1: Front-Right
    2: Rear-Left    3: Rear-Right

Each leg has 3 DOF: Hip (abduction), Thigh, Knee
"""

import numpy as np
from dataclasses import dataclass
from loguru import logger


@dataclass
class LegConfig:
    """Physical dimensions of a leg (meters)."""
    hip_offset: float    # lateral distance from body center to hip joint
    thigh_len:  float    # upper leg length
    shin_len:   float    # lower leg length


@dataclass
class FootPosition:
    """Target foot position in body frame (meters)."""
    x: float  # forward (+) / backward (-)
    y: float  # left (+) / right (-)
    z: float  # up (+) / down (-)


@dataclass
class JointAngles:
    """Servo angles in radians for one leg."""
    hip:   float  # abduction/adduction
    thigh: float  # forward/backward swing
    knee:  float  # knee flexion


class InverseKinematics:
    """
    3-DOF IK solver for a quadruped leg using geometric approach.
    """

    def __init__(self, config: LegConfig):
        self.cfg = config

    def solve(self, foot: FootPosition, leg_side: int = 1) -> JointAngles:
        """
        Solve IK for a target foot position.

        Args:
            foot: Target position in body frame.
            leg_side: +1 for left legs, -1 for right legs.

        Returns:
            JointAngles with hip, thigh, knee angles in radians.
            Returns None if target is unreachable.
        """
        L1 = self.cfg.hip_offset
        L2 = self.cfg.thigh_len
        L3 = self.cfg.shin_len

        # --- Hip (abduction) ---
        # Project onto the YZ plane
        y_eff = foot.y - leg_side * L1
        hip_angle = np.arctan2(y_eff, -foot.z)

        # --- Distance in the sagittal plane ---
        # Effective leg length after accounting for hip offset
        D = np.sqrt(y_eff**2 + foot.z**2)
        # Distance from thigh pivot to foot
        R = np.sqrt(foot.x**2 + D**2)

        max_reach = L2 + L3
        if R > max_reach:
            logger.warning(f"Target unreachable: R={R:.4f} > max_reach={max_reach:.4f}")
            R = max_reach * 0.99  # clamp

        # --- Knee angle (law of cosines) ---
        cos_knee = (L2**2 + L3**2 - R**2) / (2 * L2 * L3)
        cos_knee = np.clip(cos_knee, -1.0, 1.0)
        knee_angle = np.pi - np.arccos(cos_knee)  # flexion is positive

        # --- Thigh angle ---
        alpha = np.arctan2(foot.x, D)
        cos_beta = (L2**2 + R**2 - L3**2) / (2 * L2 * R)
        cos_beta = np.clip(cos_beta, -1.0, 1.0)
        beta = np.arccos(cos_beta)
        thigh_angle = alpha + beta

        return JointAngles(hip=hip_angle, thigh=thigh_angle, knee=knee_angle)

    def angles_to_degrees(self, angles: JointAngles) -> JointAngles:
        return JointAngles(
            hip=np.degrees(angles.hip),
            thigh=np.degrees(angles.thigh),
            knee=np.degrees(angles.knee),
        )


class QuadrupedIK:
    """
    Full quadruped IK — manages IK for all 4 legs.
    """

    # Body frame leg positions (FR, FL, RR, RL) relative to body center
    LEG_ORIGINS = {
        "FL": np.array([ 0.12,  0.07, 0.0]),
        "FR": np.array([ 0.12, -0.07, 0.0]),
        "RL": np.array([-0.12,  0.07, 0.0]),
        "RR": np.array([-0.12, -0.07, 0.0]),
    }

    LEG_SIDES = {"FL": 1, "FR": -1, "RL": 1, "RR": -1}

    def __init__(self, leg_config: LegConfig):
        self.ik = InverseKinematics(leg_config)

    def solve_all(self, foot_positions: dict[str, FootPosition]) -> dict[str, JointAngles]:
        """
        Solve IK for all legs.

        Args:
            foot_positions: dict with keys "FL","FR","RL","RR"

        Returns:
            dict of JointAngles per leg
        """
        angles = {}
        for leg, foot in foot_positions.items():
            angles[leg] = self.ik.solve(foot, self.LEG_SIDES[leg])
        return angles

    def default_stance(self, body_height: float = 0.15) -> dict[str, FootPosition]:
        """Return default standing foot positions."""
        positions = {}
        for name, origin in self.LEG_ORIGINS.items():
            side = self.LEG_SIDES[name]
            positions[name] = FootPosition(
                x=origin[0],
                y=origin[1] + side * 0.0,
                z=-body_height,
            )
        return positions
