"""Tests for physics_core.mechanics.pendulum — PendulumSim and ReferencePendulumSim."""

import math

import pytest

from physics_core.mechanics.pendulum import PendulumSim, ReferencePendulumSim


class TestPendulumSim:
    """Tests for the abstract base."""

    def test_angular_acceleration_raises_not_implemented(self) -> None:
        sim = PendulumSim()
        with pytest.raises(NotImplementedError):
            sim.angular_acceleration(0.1, 0.0)

    def test_step_raises_not_implemented(self) -> None:
        """step() calls the hook internally, so it should also raise."""
        sim = PendulumSim()
        with pytest.raises(NotImplementedError):
            sim.step()

    def test_state_property(self) -> None:
        sim = PendulumSim(theta0=0.5, omega0=1.0)
        s = sim.state
        assert s["theta"] == pytest.approx(0.5)
        assert s["omega"] == pytest.approx(1.0)
        assert s["t"] == pytest.approx(0.0)

    def test_state_is_copy(self) -> None:
        sim = PendulumSim()
        s1 = sim.state
        s1["theta"] = 99.0
        assert sim.state["theta"] != pytest.approx(99.0)

    def test_position_at_theta_zero(self) -> None:
        sim = PendulumSim(theta0=0.0, length=2.0)
        x, y = sim.position()
        assert x == pytest.approx(0.0)
        assert y == pytest.approx(-2.0)

    def test_position_at_theta_pi_over_2(self) -> None:
        sim = PendulumSim(theta0=math.pi / 2, length=1.0)
        x, y = sim.position()
        assert x == pytest.approx(1.0)
        assert y == pytest.approx(0.0)

    def test_energy_at_bottom(self) -> None:
        """At theta=0, omega=0: KE=0, PE=0 (reference at bottom)."""
        sim = PendulumSim(theta0=0.0, omega0=0.0, length=1.0, mass=2.0)
        e = sim.energy()
        assert e["kinetic"] == pytest.approx(0.0)
        assert e["potential"] == pytest.approx(0.0)
        assert e["total"] == pytest.approx(0.0)

    def test_energy_at_max_displacement(self) -> None:
        """At theta=0.1, omega=0: KE=0, PE = mgL(1-cosθ)."""
        sim = PendulumSim(theta0=0.1, omega0=0.0, length=1.0, mass=1.0, g=9.81)
        e = sim.energy()
        assert e["kinetic"] == pytest.approx(0.0)
        expected_pe = 1.0 * 9.81 * 1.0 * (1.0 - math.cos(0.1))
        assert e["potential"] == pytest.approx(expected_pe)

    def test_period_from_formula(self) -> None:
        sim = PendulumSim(length=1.0, g=9.81)
        expected = 2.0 * math.pi * math.sqrt(1.0 / 9.81)
        assert sim.period_from_formula == pytest.approx(expected)

    def test_invalid_scheme(self) -> None:
        with pytest.raises(ValueError, match="scheme must be"):
            PendulumSim(scheme="rk4")


class TestReferencePendulumSim:
    """Tests for the reference implementation."""

    def test_angular_acceleration_small_angle(self) -> None:
        sim = ReferencePendulumSim(length=1.0, g=9.81, small_angle=True)
        # a = -(g/L) * theta
        a = sim.angular_acceleration(0.1, 0.0)
        assert a == pytest.approx(-9.81 * 0.1)

    def test_angular_acceleration_full(self) -> None:
        sim = ReferencePendulumSim(length=1.0, g=9.81, small_angle=False)
        a = sim.angular_acceleration(0.1, 0.0)
        assert a == pytest.approx(-9.81 * math.sin(0.1))

    def test_step_advances_state(self) -> None:
        sim = ReferencePendulumSim(theta0=0.1, dt=0.01)
        sim.step()
        s = sim.state
        assert s["t"] == pytest.approx(0.01)
        # theta should have changed (started at rest, so omega becomes slightly negative)
        assert s["theta"] != pytest.approx(0.1)

    def test_period_small_amplitude(self) -> None:
        """For small amplitude, the numerical period should approximate
        2π√(L/g) to within 1%."""
        L = 1.0
        sim = ReferencePendulumSim(length=L, g=9.81, theta0=0.05, dt=0.001, small_angle=True)
        T_formula = sim.period_from_formula

        # Measure period from zero-crossings (positive→negative).
        # Starting at max displacement, each positive→negative crossing
        # is one full period apart.
        prev_theta = sim.state["theta"]
        first_crossing_t = None
        crossings = 0
        max_steps = 50_000
        steps = 0
        while crossings < 4 and steps < max_steps:
            sim.step()
            steps += 1
            theta = sim.state["theta"]
            if prev_theta > 0 and theta <= 0:
                crossings += 1
                if first_crossing_t is None:
                    first_crossing_t = sim.state["t"]
            prev_theta = theta

        # Period = (time between first and last crossing) / (number of intervals)
        assert first_crossing_t is not None
        measured_T = (sim.state["t"] - first_crossing_t) / (crossings - 1)
        assert measured_T == pytest.approx(T_formula, rel=0.01), (
            f"Measured period {measured_T:.4f}s vs formula {T_formula:.4f}s"
        )

    def test_energy_conserved(self) -> None:
        """Reference pendulum with Verlet should conserve energy to within
        0.1% over 10 periods."""
        sim = ReferencePendulumSim(
            length=1.0, g=9.81, theta0=0.1, dt=0.001, scheme="verlet"
        )
        e0 = sim.energy()["total"]
        e_min, e_max = e0, e0

        for _ in range(20_000):  # ~20 periods
            sim.step()
            e = sim.energy()["total"]
            e_min = min(e_min, e)
            e_max = max(e_max, e)

        drift = (e_max - e_min) / e0
        assert drift < 0.001, f"Energy drift {drift*100:.3f}%"

    def test_euler_does_not_conserve_energy(self) -> None:
        """Euler scheme should show significant energy drift."""
        sim = ReferencePendulumSim(
            length=1.0, g=9.81, theta0=0.1, dt=0.001, scheme="euler"
        )
        e0 = sim.energy()["total"]

        for _ in range(10_000):
            sim.step()

        e_final = sim.energy()["total"]
        # Euler should have drifted by more than 5%
        assert abs(e_final - e0) / e0 > 0.05, (
            f"Euler drift {(e_final - e0) / e0 * 100:.3f}% — expected > 5%"
        )


class TestDampedPendulumSim:
    """Tests for damping behaviour."""

    def test_b_zero_gives_undamped_motion(self) -> None:
        """b=0 (default) should conserve energy like the undamped reference."""
        sim = ReferencePendulumSim(
            length=1.0, g=9.81, theta0=0.1, dt=0.001, scheme="verlet",
            damping_coefficient=0.0,
        )
        e0 = sim.energy()["total"]
        e_min, e_max = e0, e0
        for _ in range(10_000):
            sim.step()
            e = sim.energy()["total"]
            e_min = min(e_min, e)
            e_max = max(e_max, e)
        drift = (e_max - e_min) / e0
        assert drift < 0.001, f"b=0 should conserve energy, drift={drift*100:.3f}%"

    def test_damped_amplitude_decays(self) -> None:
        """With b>0, the oscillation amplitude should decay over time."""
        sim = ReferencePendulumSim(
            length=1.0, g=9.81, theta0=0.3, dt=0.001, scheme="verlet",
            damping_coefficient=0.5,
        )
        # Record peak amplitudes in first and last quarters of 10 periods
        period = sim.period_from_formula
        n_steps = int(10 * period / sim.dt)

        amplitudes: list[float] = []
        prev_theta = sim.state["theta"]
        for i in range(n_steps):
            sim.step()
            theta = sim.state["theta"]
            if prev_theta > 0 and theta <= 0:
                amplitudes.append(abs(sim.state["theta"]))
            prev_theta = theta

        assert len(amplitudes) >= 4, f"Expected >=4 zero-crossings, got {len(amplitudes)}"
        # Final amplitude should be less than half of initial
        half_idx = len(amplitudes) // 2
        # Check that amplitude trend is clearly downward
        assert amplitudes[-1] < amplitudes[0] * 0.5, (
            f"Damped amplitude did not decay: initial={amplitudes[0]:.4f}, "
            f"final={amplitudes[-1]:.4f}"
        )

    def test_damped_energy_decreases(self) -> None:
        """Total energy should decrease over time when b>0."""
        sim = ReferencePendulumSim(
            length=1.0, g=9.81, theta0=0.3, dt=0.001, scheme="verlet",
            damping_coefficient=0.5,
        )
        e0 = sim.energy()["total"]
        for _ in range(5_000):
            sim.step()
        e_final = sim.energy()["total"]
        assert e_final < e0 * 0.5, (
            f"Damped energy did not decay enough: e0={e0:.6f}, "
            f"e_final={e_final:.6f}"
        )