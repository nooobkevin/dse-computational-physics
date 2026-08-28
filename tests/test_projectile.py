"""Tests for physics_core.mechanics.projectile — ProjectileSim and ReferenceProjectileSim."""

import math

import pytest

from physics_core.mechanics.projectile import ProjectileSim, ReferenceProjectileSim


class TestProjectileSim:
    """Tests for the abstract base."""

    def test_acceleration_raises_not_implemented(self) -> None:
        sim = ProjectileSim()
        with pytest.raises(NotImplementedError):
            sim.acceleration(10.0, 10.0, 0.0)

    def test_step_raises_not_implemented(self) -> None:
        sim = ProjectileSim()
        with pytest.raises(NotImplementedError):
            sim.step()

    def test_state_property(self) -> None:
        sim = ProjectileSim(x0=1.0, y0=2.0, vx0=3.0, vy0=4.0)
        s = sim.state
        assert s.x == pytest.approx(1.0)
        assert s.y == pytest.approx(2.0)
        assert s.vx == pytest.approx(3.0)
        assert s.vy == pytest.approx(4.0)
        assert s.t == pytest.approx(0.0)

    def test_position_property(self) -> None:
        sim = ProjectileSim(x0=5.0, y0=10.0)
        x, y = sim.position
        assert x == pytest.approx(5.0)
        assert y == pytest.approx(10.0)

    def test_velocity_property(self) -> None:
        sim = ProjectileSim(vx0=15.0, vy0=20.0)
        vx, vy = sim.velocity
        assert vx == pytest.approx(15.0)
        assert vy == pytest.approx(20.0)

    def test_invalid_scheme(self) -> None:
        with pytest.raises(ValueError, match="scheme must be"):
            ProjectileSim(scheme="rk4")


class TestReferenceProjectileSim:
    """Tests for the reference implementation."""

    def test_acceleration_no_drag(self) -> None:
        sim = ReferenceProjectileSim()
        ax, ay = sim.acceleration(10.0, 10.0, 0.0)
        assert ax == pytest.approx(0.0)
        assert ay == pytest.approx(-9.81)

    def test_acceleration_with_drag(self) -> None:
        sim = ReferenceProjectileSim(drag_coefficient=0.5, mass=1.0)
        ax, ay = sim.acceleration(10.0, 10.0, 0.0)
        assert ax == pytest.approx(-5.0)   # -b*vx/m
        assert ay == pytest.approx(-9.81 - 5.0)  # -g - b*vy/m

    def test_step_advances_state(self) -> None:
        sim = ReferenceProjectileSim(vx0=10.0, vy0=10.0, dt=0.01)
        sim.step()
        s = sim.state
        assert s.t == pytest.approx(0.01)
        # With verlet and vy0=10, the half-step velocity is still positive,
        # so y should increase slightly before gravity reverses it
        assert s.x != pytest.approx(0.0) or s.y != pytest.approx(0.0)

    def test_free_fall_analytic(self) -> None:
        """Drop from rest: y = -½gt²."""
        sim = ReferenceProjectileSim(x0=0.0, y0=0.0, vx0=0.0, vy0=0.0, dt=0.001)
        t_total = 1.0
        steps = int(t_total / sim.dt)
        for _ in range(steps):
            sim.step()
        s = sim.state
        expected_y = -0.5 * 9.81 * t_total**2
        assert s.y == pytest.approx(expected_y, rel=1e-3)
        assert s.vy == pytest.approx(-9.81 * t_total, rel=1e-3)