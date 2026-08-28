"""Tests for physics_core.integrators — Euler and velocity-Verlet steppers."""

import math

import pytest

from physics_core.integrators import euler_step, verlet_step


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def constant_accel(a: float):
    """Return a deriv fn that always returns *a*."""
    def _deriv(x: float, v: float, t: float) -> float:
        return a
    return _deriv


def spring_deriv(k: float = 1.0):
    """Simple harmonic oscillator: a = -k x (unit mass)."""
    def _deriv(x: float, v: float, t: float) -> float:
        return -k * x
    return _deriv


# ---------------------------------------------------------------------------
# Euler
# ---------------------------------------------------------------------------

class TestEulerStep:
    def test_constant_acceleration(self) -> None:
        """Euler over constant accel: x = x0 + v0*dt + 0.5*a*dt²."""
        state = {"x": 0.0, "v": 0.0, "t": 0.0}
        dt = 0.1
        a = 2.0
        result = euler_step(state, dt, constant_accel(a))
        # Euler: x1 = x0 + v0*dt = 0, v1 = v0 + a*dt = 0.2
        assert result["x"] == pytest.approx(0.0)
        assert result["v"] == pytest.approx(a * dt)
        assert result["t"] == pytest.approx(dt)

    def test_euler_advances_time(self) -> None:
        state = {"x": 1.0, "v": 0.5, "t": 0.0}
        result = euler_step(state, 0.01, constant_accel(0.0))
        assert result["t"] == pytest.approx(0.01)

    def test_euler_no_t_in_state(self) -> None:
        """If state has no 't', the result should not have 't'."""
        state = {"x": 1.0, "v": 0.0}
        result = euler_step(state, 0.01, constant_accel(0.0))
        assert "t" not in result


# ---------------------------------------------------------------------------
# Velocity-Verlet
# ---------------------------------------------------------------------------

class TestVerletStep:
    def test_constant_acceleration(self) -> None:
        """Verlet over constant accel should match the analytic result."""
        state = {"x": 0.0, "v": 0.0, "t": 0.0}
        dt = 0.1
        a = 2.0
        result = verlet_step(state, dt, constant_accel(a))
        # Velocity-Verlet with constant a:
        #   v_half = 0 + 0.5*dt*a = 0.1
        #   x_new  = 0 + dt*0.1 = 0.01
        #   a_new  = a (constant)
        #   v_new  = 0.1 + 0.5*dt*a = 0.2
        assert result["x"] == pytest.approx(0.5 * a * dt**2)  # 0.01
        assert result["v"] == pytest.approx(a * dt)           # 0.2

    def test_verlet_advances_time(self) -> None:
        state = {"x": 1.0, "v": 0.5, "t": 0.0}
        result = verlet_step(state, 0.01, constant_accel(0.0))
        assert result["t"] == pytest.approx(0.01)

    def test_verlet_no_t_in_state(self) -> None:
        state = {"x": 1.0, "v": 0.0}
        result = verlet_step(state, 0.01, constant_accel(0.0))
        assert "t" not in result

    # ------------------------------------------------------------------
    # Energy conservation for SHO (the key correctness test)
    # ------------------------------------------------------------------
    def test_sho_energy_conservation(self) -> None:
        """Velocity-Verlet conserves energy for a simple harmonic oscillator.

        For a unit-mass SHO with k=1, total energy E = ½v² + ½x² should
        remain constant to within O(dt²) over many periods.  We use a
        moderate dt = 0.05 and integrate for 1000 steps (5 periods).
        """
        k = 1.0
        dt = 0.05
        state = {"x": 1.0, "v": 0.0, "t": 0.0}
        deriv = spring_deriv(k)

        # Initial energy
        def energy(s):
            return 0.5 * s["v"] ** 2 + 0.5 * k * s["x"] ** 2

        e0 = energy(state)
        e_min, e_max = e0, e0

        for _ in range(1000):
            state = verlet_step(state, dt, deriv)
            e = energy(state)
            e_min = min(e_min, e)
            e_max = max(e_max, e)

        # Energy should be conserved to within 1% over 1000 steps
        # (typical Verlet drift is O(dt²) per step, so ~0.25% for dt=0.05)
        assert e_max - e_min < 0.01 * e0, (
            f"Energy drifted by {(e_max - e_min) / e0 * 100:.3f}%"
        )
        # Final energy should be close to initial
        assert energy(state) == pytest.approx(e0, rel=1e-3)

    def test_sho_euler_drifts(self) -> None:
        """Euler should NOT conserve energy — it should drift upward.

        This test confirms the test infrastructure is honest: Euler
        systematically adds energy to the SHO.
        """
        k = 1.0
        dt = 0.05
        state = {"x": 1.0, "v": 0.0, "t": 0.0}
        deriv = spring_deriv(k)

        def energy(s):
            return 0.5 * s["v"] ** 2 + 0.5 * k * s["x"] ** 2

        e0 = energy(state)
        for _ in range(500):
            state = euler_step(state, dt, deriv)

        # Euler should have gained significant energy
        final_e = energy(state)
        assert final_e > 1.5 * e0, (
            f"Euler energy ratio {final_e / e0:.3f} — expected drift > 50%"
        )

    def test_verlet_does_not_explode(self) -> None:
        """Verlet with moderate dt should remain bounded for many steps."""
        k = 1.0
        dt = 0.1
        state = {"x": 1.0, "v": 0.0, "t": 0.0}
        deriv = spring_deriv(k)

        for _ in range(5000):
            state = verlet_step(state, dt, deriv)
            # Position should stay bounded by initial amplitude
            assert abs(state["x"]) < 2.0, f"Position exploded: {state['x']}"