"""Tests for physics_core.mechanics.circular — CircularMotion."""

import math

import pytest

from physics_core.mechanics.circular import CircularMotion


class TestCircularMotion:
    def test_default_construction(self) -> None:
        m = CircularMotion()
        assert m.radius == pytest.approx(1.0)
        assert m.angle == pytest.approx(0.0)

    def test_step_advances_angle(self) -> None:
        m = CircularMotion(omega0=2.0, dt=0.1)
        m.step()
        assert m.angle == pytest.approx(0.2)

    def test_position_at_zero(self) -> None:
        m = CircularMotion(radius=2.0, theta0=0.0)
        x, y = m.position
        assert x == pytest.approx(2.0)
        assert y == pytest.approx(0.0)

    def test_position_at_pi_over_2(self) -> None:
        m = CircularMotion(radius=1.0, theta0=math.pi / 2)
        x, y = m.position
        assert x == pytest.approx(0.0, abs=1e-15)
        assert y == pytest.approx(1.0)

    def test_tangential_speed(self) -> None:
        m = CircularMotion(radius=2.0, omega0=3.0)
        assert m.tangential_speed == pytest.approx(6.0)

    def test_centripetal_accel(self) -> None:
        m = CircularMotion(radius=2.0, omega0=3.0)
        # a_c = v²/r = (6)²/2 = 18
        assert m.centripetal_accel == pytest.approx(18.0)

    def test_omega_hook_default(self) -> None:
        """The default omega() returns omega0 (constant)."""
        m = CircularMotion(omega0=1.5)
        assert m.omega() == pytest.approx(1.5)

    def test_omega_hook_override(self) -> None:
        """Subclass can override omega() for non-uniform motion."""
        class AcceleratingMotion(CircularMotion):
            def omega(self) -> float:
                return self._omega0 + 0.1 * self._t  # linear acceleration

        m = AcceleratingMotion(omega0=1.0, dt=0.1)
        m.step()
        # After first step: omega() is called before _t is updated,
        # so omega = 1.0 + 0.1*0.0 = 1.0, angle = 0 + 1.0*0.1 = 0.1
        assert m.angle == pytest.approx(0.1)