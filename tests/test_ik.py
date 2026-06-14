"""
Unit tests for NeuraBot IK Engine.
Run with: python -m pytest tests/
"""

import pytest
import math
import sys
sys.path.insert(0, ".")

from src.ik.ik_engine import InverseKinematics, QuadrupedIK, LegConfig, FootPosition


@pytest.fixture
def leg_config():
    return LegConfig(hip_offset=0.045, thigh_len=0.10, shin_len=0.10)


@pytest.fixture
def ik(leg_config):
    return InverseKinematics(leg_config)


@pytest.fixture
def quad_ik(leg_config):
    return QuadrupedIK(leg_config)


class TestIKSolver:
    def test_neutral_stance(self, ik):
        """Foot directly below the hip should give ~0° hip, reasonable thigh/knee."""
        foot = FootPosition(x=0.0, y=0.045, z=-0.15)
        angles = ik.solve(foot, leg_side=1)
        assert angles is not None
        assert abs(angles.hip) < math.radians(15)

    def test_angles_in_range(self, ik):
        """All angles should be physically plausible (within ±180°)."""
        foot = FootPosition(x=0.05, y=0.045, z=-0.13)
        angles = ik.solve(foot, leg_side=1)
        for a in [angles.hip, angles.thigh, angles.knee]:
            assert -math.pi <= a <= math.pi, f"Angle {math.degrees(a):.1f}° out of range"

    def test_unreachable_clamped(self, ik):
        """Unreachable targets should be clamped, not raise an error."""
        foot = FootPosition(x=0.5, y=0.0, z=-0.5)  # far away
        angles = ik.solve(foot, leg_side=1)
        assert angles is not None

    def test_left_vs_right(self, ik):
        """Left and right leg solutions should mirror each other in hip angle."""
        foot_l = FootPosition(x=0.0, y= 0.07, z=-0.15)
        foot_r = FootPosition(x=0.0, y=-0.07, z=-0.15)
        a_l = ik.solve(foot_l, leg_side= 1)
        a_r = ik.solve(foot_r, leg_side=-1)
        assert abs(a_l.thigh - a_r.thigh) < math.radians(5)


class TestQuadrupedIK:
    def test_default_stance_all_legs(self, quad_ik):
        """Default stance should return angles for all 4 legs."""
        foot_pos = quad_ik.default_stance(body_height=0.15)
        angles = quad_ik.solve_all(foot_pos)
        assert set(angles.keys()) == {"FL", "FR", "RL", "RR"}

    def test_symmetry_trot(self, quad_ik):
        """FL and FR at same x,z (mirrored y) should have same thigh/knee."""
        stance = quad_ik.default_stance(0.15)
        angles = quad_ik.solve_all(stance)
        assert abs(angles["FL"].thigh - angles["FR"].thigh) < math.radians(5)
        assert abs(angles["FL"].knee  - angles["FR"].knee)  < math.radians(5)

    def test_lower_body_height(self, quad_ik):
        """Lower body height should result in greater knee flexion."""
        a_high = quad_ik.solve_all(quad_ik.default_stance(0.18))
        a_low  = quad_ik.solve_all(quad_ik.default_stance(0.10))
        assert a_low["FL"].knee > a_high["FL"].knee


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
