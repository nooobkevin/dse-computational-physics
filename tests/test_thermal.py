"""Tests for physics_core.thermal — GasSim and ReferenceGasSim."""

import math

import numpy as np
import pytest

from physics_core.thermal.gas_sim import GasSim, ReferenceGasSim, KB
from physics_core.thermal.equations import (
    maxwell_boltzmann,
    mean_speed,
    most_probable_speed,
    rms_speed,
)


class TestGasSim:
    """Tests for the abstract base."""

    def test_collide_wall_raises_not_implemented(self) -> None:
        sim = GasSim(N=10)
        pos = sim._positions.copy()
        vel = sim._velocities.copy()
        with pytest.raises(NotImplementedError):
            sim._collide_wall(pos, vel)

    def test_collide_particle_raises_not_implemented(self) -> None:
        sim = GasSim(N=10)
        pos = sim._positions.copy()
        vel = sim._velocities.copy()
        with pytest.raises(NotImplementedError):
            sim._collide_particle(pos, vel)

    def test_step_raises_not_implemented(self) -> None:
        """step() calls the hooks internally, so it should also raise."""
        sim = GasSim(N=10)
        with pytest.raises(NotImplementedError):
            sim.step()

    def test_state_property(self) -> None:
        sim = GasSim(N=5, L=10.0, T=1.0, seed=42)
        s = sim.state
        assert s["positions"].shape == (5, 2)
        assert s["velocities"].shape == (5, 2)
        assert s["t"] == pytest.approx(0.0)
        assert "kinetic" in s["energies"]

    def test_state_is_copy(self) -> None:
        sim = GasSim(N=5, seed=42)
        s1 = sim.state
        s1["positions"][0, 0] = 999.0
        assert sim.state["positions"][0, 0] != pytest.approx(999.0)

    def test_energy_zero_velocity(self) -> None:
        """If all velocities are zero, kinetic energy should be zero."""
        sim = GasSim(N=10, T=0.0)
        # At T=0, all velocities should be zero
        e = sim.energy()
        assert e["kinetic"] == pytest.approx(0.0)
        assert e["total"] == pytest.approx(0.0)

    def test_energy_positive(self) -> None:
        """At T>0, kinetic energy should be positive."""
        sim = GasSim(N=50, T=1.0, seed=42)
        e = sim.energy()
        assert e["kinetic"] > 0.0

    def test_invalid_scheme(self) -> None:
        with pytest.raises(ValueError, match="scheme must be"):
            GasSim(scheme="rk4")

    def test_position_shape(self) -> None:
        sim = GasSim(N=20, dim=3, seed=42)
        pos = sim.position
        assert pos.shape == (20, 3)

    def test_initial_positions_in_box(self) -> None:
        sim = GasSim(N=100, L=5.0, seed=42)
        pos = sim.position
        assert np.all(pos >= 0.0)
        assert np.all(pos <= 5.0)


class TestReferenceGasSim:
    """Tests for the reference implementation."""

    def test_step_advances_state(self) -> None:
        sim = ReferenceGasSim(N=10, L=10.0, T=1.0, dt=0.01, seed=42)
        pos_before = sim._positions.copy()
        sim.step()
        s = sim.state
        assert s["t"] == pytest.approx(0.01)
        # Positions should have changed
        assert not np.allclose(s["positions"], pos_before)

    def test_energy_conserved_single_particle(self) -> None:
        """A single free particle (no walls to hit) should conserve KE."""
        sim = ReferenceGasSim(N=1, L=100.0, T=1.0, dt=0.001, seed=42)
        e0 = sim.energy()["kinetic"]
        assert e0 > 0.0, "Initial KE should be positive"
        for _ in range(1000):
            sim.step()
        e_final = sim.energy()["kinetic"]
        # KE should be conserved (no collisions for a single particle in a big box)
        assert abs(e_final - e0) / e0 < 0.001, (
            f"KE drifted by {abs(e_final - e0) / e0 * 100:.3f}%"
        )

    def test_particle_bounces_off_wall(self) -> None:
        """A particle heading toward a wall should bounce back."""
        # Place a particle near the right wall moving right
        sim = ReferenceGasSim(N=1, L=10.0, T=0.0, dt=0.1)
        sim._positions[0] = np.array([9.8, 5.0])
        sim._velocities[0] = np.array([5.0, 0.0])
        sim.step()
        # After step, the particle should have bounced and be moving left
        assert sim._positions[0, 0] < 10.0, "Particle escaped the box!"
        assert sim._velocities[0, 0] < 0.0, "Particle didn't bounce!"

    def test_pressure_positive(self) -> None:
        """After running, pressure should be positive."""
        sim = ReferenceGasSim(N=50, L=10.0, T=1.0, dt=0.01, seed=42)
        for _ in range(500):
            sim.step()
        p = sim.pressure()
        assert p > 0.0, f"Pressure should be positive, got {p}"

    def test_speed_distribution_non_empty(self) -> None:
        """Speed distribution should return non-empty bins."""
        sim = ReferenceGasSim(N=50, L=10.0, T=1.0, dt=0.01, seed=42)
        for _ in range(100):
            sim.step()
        counts, bin_edges = sim.speed_distribution(bins=10)
        assert len(counts) > 0
        assert len(bin_edges) > 0
        assert np.sum(counts) == pytest.approx(sim.N)

    def test_average_speed_positive(self) -> None:
        sim = ReferenceGasSim(N=50, T=1.0, seed=42)
        assert sim.average_speed > 0.0

    def test_rms_speed_positive(self) -> None:
        sim = ReferenceGasSim(N=50, T=1.0, seed=42)
        assert sim.rms_speed > 0.0

    def test_rms_greater_than_average(self) -> None:
        """RMS speed should be >= average speed (equality only if all
        speeds are equal)."""
        sim = ReferenceGasSim(N=50, T=1.0, seed=42)
        assert sim.rms_speed >= sim.average_speed

    def test_temperature_from_ke(self) -> None:
        """Estimated T from KE should be close to the input T."""
        sim = ReferenceGasSim(N=100, L=10.0, T=1.0, dt=0.005, seed=42)
        # Run for a while to equilibrate
        for _ in range(1000):
            sim.step()
        T_est = sim.temperature_from_ke()
        assert T_est == pytest.approx(1.0, rel=0.1), (
            f"Estimated T={T_est:.4f} vs input T=1.0"
        )

    def test_ideal_gas_law(self) -> None:
        """Measured pressure should approximate the ideal gas law
        P = N kB T / V to within a reasonable tolerance.

        Uses a dilute gas (small particle radius, large box) to minimise
        excluded-volume effects.
        """
        sim = ReferenceGasSim(
            N=100, L=20.0, T=2.0, dt=0.005, seed=42, particle_radius=0.05
        )
        for _ in range(2000):
            sim.step()
        P_measured = sim.pressure()
        P_ideal = sim.ideal_gas_pressure()
        # Tolerance: 15% — MD pressure fluctuates
        assert P_measured == pytest.approx(P_ideal, rel=0.15), (
            f"Measured P={P_measured:.4f} vs ideal P={P_ideal:.4f}"
        )

    def test_euler_scheme_accepted(self) -> None:
        """Euler scheme should be accepted and run without error."""
        sim = ReferenceGasSim(
            N=10, L=10.0, T=1.0, dt=0.01, scheme="euler", seed=42
        )
        for _ in range(100):
            sim.step()
        # Should still have positive energy
        assert sim.energy()["kinetic"] > 0.0

    def test_verlet_conserves_energy(self) -> None:
        """Verlet should conserve energy much better than Euler."""
        sim = ReferenceGasSim(
            N=10, L=10.0, T=1.0, dt=0.01, scheme="verlet", seed=42
        )
        e0 = sim.energy()["kinetic"]
        for _ in range(500):
            sim.step()
        e_final = sim.energy()["kinetic"]
        drift = abs(e_final - e0) / e0
        assert drift < 0.005, (
            f"Verlet drift {drift * 100:.3f}% — expected < 0.5%"
        )


class TestMaxwellBoltzmannEquations:
    """Tests for the Maxwell-Boltzmann distribution helpers."""

    def test_maxwell_boltzmann_2d_normalization(self) -> None:
        """The 2D MB distribution should approximately integrate to 1."""
        T, m = 1.0, 1.0
        v_max = 5.0
        n_steps = 1000
        dv = v_max / n_steps
        integral = 0.0
        for i in range(n_steps):
            v = (i + 0.5) * dv
            integral += maxwell_boltzmann(v, T, m, dim=2) * dv
        assert integral == pytest.approx(1.0, rel=0.01)

    def test_maxwell_boltzmann_3d_normalization(self) -> None:
        """The 3D MB distribution should approximately integrate to 1."""
        T, m = 1.0, 1.0
        v_max = 5.0
        n_steps = 1000
        dv = v_max / n_steps
        integral = 0.0
        for i in range(n_steps):
            v = (i + 0.5) * dv
            integral += maxwell_boltzmann(v, T, m, dim=3) * dv
        assert integral == pytest.approx(1.0, rel=0.01)

    def test_most_probable_speed_2d(self) -> None:
        """For 2D: v_p = sqrt(kB*T/m)."""
        vp = most_probable_speed(T=1.0, m=1.0, dim=2)
        assert vp == pytest.approx(math.sqrt(1.0))

    def test_most_probable_speed_3d(self) -> None:
        """For 3D: v_p = sqrt(2*kB*T/m)."""
        vp = most_probable_speed(T=1.0, m=1.0, dim=3)
        assert vp == pytest.approx(math.sqrt(2.0))

    def test_mean_speed_2d(self) -> None:
        """For 2D: <v> = sqrt(π*kB*T/(2*m))."""
        vm = mean_speed(T=1.0, m=1.0, dim=2)
        assert vm == pytest.approx(math.sqrt(math.pi / 2.0))

    def test_mean_speed_3d(self) -> None:
        """For 3D: <v> = sqrt(8*kB*T/(π*m))."""
        vm = mean_speed(T=1.0, m=1.0, dim=3)
        assert vm == pytest.approx(math.sqrt(8.0 / math.pi))

    def test_rms_speed_2d(self) -> None:
        """For 2D: v_rms = sqrt(2*kB*T/m)."""
        vr = rms_speed(T=1.0, m=1.0, dim=2)
        assert vr == pytest.approx(math.sqrt(2.0))

    def test_rms_speed_3d(self) -> None:
        """For 3D: v_rms = sqrt(3*kB*T/m)."""
        vr = rms_speed(T=1.0, m=1.0, dim=3)
        assert vr == pytest.approx(math.sqrt(3.0))

    def test_peak_of_distribution(self) -> None:
        """The MB distribution should peak near the most probable speed."""
        T, m = 1.0, 1.0
        vp = most_probable_speed(T, m, dim=2)
        # Sample near vp
        f_at_vp = maxwell_boltzmann(vp, T, m, dim=2)
        f_before = maxwell_boltzmann(vp * 0.5, T, m, dim=2)
        f_after = maxwell_boltzmann(vp * 1.5, T, m, dim=2)
        assert f_at_vp > f_before
        assert f_at_vp > f_after