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
from physics_core.thermal.random_walk import RandomWalk


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

    # ------------------------------------------------------------------
    # Gas-law helper tests
    # ------------------------------------------------------------------

    def test_set_volume_scales_positions(self) -> None:
        """set_volume should rescale positions proportionally."""
        sim = ReferenceGasSim(N=10, L=10.0, T=1.0, seed=42)
        old_pos = sim._positions.copy()
        sim.set_volume(5.0)
        assert sim.L == pytest.approx(5.0)
        # Positions should be scaled by 0.5
        np.testing.assert_array_almost_equal(
            sim._positions, old_pos * 0.5
        )

    def test_set_volume_raises_for_non_positive(self) -> None:
        sim = ReferenceGasSim(N=5, L=10.0, T=1.0)
        with pytest.raises(ValueError, match="Box side length must be positive"):
            sim.set_volume(-1.0)

    def test_set_temperature_rescales_ke(self) -> None:
        """set_temperature should change KE proportionally."""
        sim = ReferenceGasSim(N=50, L=10.0, T=1.0, dt=0.01, seed=42)
        ke_before = sim.energy()["kinetic"]
        sim.set_temperature(4.0)
        ke_after = sim.energy()["kinetic"]
        # KE should scale by factor of 4 (T doubles, so KE doubles in 2D)
        # In 2D: KE = N * kB * T, so KE ratio = T_ratio
        ratio = ke_after / ke_before
        assert ratio == pytest.approx(4.0, rel=0.05), (
            f"KE ratio={ratio:.4f}, expected 4.0"
        )

    def test_set_temperature_raises_for_non_positive(self) -> None:
        sim = ReferenceGasSim(N=5, L=10.0, T=1.0)
        with pytest.raises(ValueError, match="Temperature must be positive"):
            sim.set_temperature(-1.0)

    def test_gas_law_isothermal_curve_boyle(self) -> None:
        """Isothermal P-V curve should approximately follow P ∝ 1/V."""
        sim = ReferenceGasSim(
            N=100, L=15.0, T=2.0, dt=0.01, dim=2,
            particle_radius=0.05, seed=42,
        )
        V_values = [100.0, 150.0, 225.0, 300.0]
        curve = sim.gas_law_isothermal_curve(
            V_values, equilibration_steps=300, sample_steps=100, seed=42
        )
        # P * V should be approximately constant (Boyle's law)
        pv_products = [P * V for V, P in curve]
        mean_pv = float(np.mean(pv_products))
        for V, P in curve:
            pv = P * V
            assert pv == pytest.approx(mean_pv, rel=0.25), (
                f"P*V={pv:.4f} at V={V:.1f}, mean={mean_pv:.4f}"
            )

    def test_gas_law_isochoric_curve_p_t(self) -> None:
        """Isochoric P-T curve should approximately follow P ∝ T."""
        sim = ReferenceGasSim(
            N=100, L=15.0, T=2.0, dt=0.01, dim=2,
            particle_radius=0.05, seed=42,
        )
        T_values = [1.0, 2.0, 3.0, 4.0]
        curve = sim.gas_law_isochoric_curve(
            T_values, equilibration_steps=500, sample_steps=200, seed=42
        )
        # P / T should be approximately constant
        pt_ratios = [P / T for T, P in curve]
        mean_ratio = float(np.mean(pt_ratios))
        for T, P in curve:
            ratio = P / T
            assert ratio == pytest.approx(mean_ratio, rel=0.35), (
                f"P/T={ratio:.4f} at T={T:.1f}, mean={mean_ratio:.4f}"
            )

    def test_gas_law_isochoric_curve_backward_compatible(self) -> None:
        """n_averaging_windows=1 must reproduce the default single-trajectory
        behaviour exactly (backward compatibility)."""
        sim = ReferenceGasSim(
            N=100, L=15.0, T=2.0, dt=0.01, dim=2,
            particle_radius=0.05, seed=42,
        )
        T_values = [1.0, 2.0, 3.0]
        curve_default = sim.gas_law_isochoric_curve(
            T_values, equilibration_steps=300, sample_steps=200, seed=42
        )
        curve_explicit = sim.gas_law_isochoric_curve(
            T_values, equilibration_steps=300, sample_steps=200, seed=42,
            n_averaging_windows=1,
        )
        assert curve_default == curve_explicit

    def test_gas_law_isochoric_curve_invalid_windows(self) -> None:
        """n_averaging_windows must be >= 1."""
        sim = ReferenceGasSim(N=50, L=15.0, T=2.0, seed=42)
        with pytest.raises(ValueError, match="n_averaging_windows must be >= 1"):
            sim.gas_law_isochoric_curve(
                [1.0, 2.0], n_averaging_windows=0
            )

    def test_gas_law_isochoric_curve_absolute_zero(self) -> None:
        """Isochoric P-T curve should extrapolate to absolute zero within 15%.

        The low-temperature points are statistically coarse (few wall
        collisions), so the extrapolation uses a variance-weighted linear
        fit (weights ``1 / T_sim**1.5``).  Calibration: simulation T=0
        (where P=0) maps to -273.15°C, so each simulation unit is
        273.15/2.0 °C (T_sim=2.0 → 0°C).
        """
        sim = ReferenceGasSim(
            N=100, L=15.0, T=2.0, dt=0.01, dim=2,
            particle_radius=0.05, seed=42,
        )
        T_values = [1.0, 2.0, 3.0, 4.0]
        curve = sim.gas_law_isochoric_curve(
            T_values, equilibration_steps=500, sample_steps=600, seed=42
        )
        Ts = np.array([t for t, _ in curve], dtype=np.float64)
        P = np.array([p for _, p in curve], dtype=np.float64)
        weights = 1.0 / Ts**1.5
        slope, intercept = np.polyfit(Ts, P, 1, w=weights)
        abs_zero_sim = -intercept / slope
        # True absolute zero is T_sim = 0; tolerance is 15% of the
        # T_sim=2.0 reference (i.e. 15% of 273.15 K in Celsius terms).
        assert abs(abs_zero_sim) / 2.0 < 0.15, (
            f"Absolute zero extrapolation: got T_sim={abs_zero_sim:.3f}, "
            f"expected ~0"
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


class TestRandomWalk:
    """Tests for the RandomWalk engine."""

    def test_rms_scaling_with_n(self) -> None:
        """RMS displacement should scale as sqrt(N) * step_length."""
        rw = RandomWalk(n_walkers=5000, n_steps=100, step_length=1.0, dim=2, seed=42)
        # Check RMS at final step
        rms_final = rw.rms[-1]
        theoretical = rw.rms_theoretical[-1]
        # Should be close (within 5% for 5000 walkers)
        assert rms_final == pytest.approx(theoretical, rel=0.05), (
            f"RMS={rms_final:.4f}, theoretical={theoretical:.4f}"
        )

    def test_rms_scaling_multi_step(self) -> None:
        """RMS at each step should approximately follow sqrt(N)."""
        rw = RandomWalk(n_walkers=2000, n_steps=50, step_length=0.5, dim=2, seed=42)
        # Check a few intermediate steps
        for s in [10, 25, 40]:
            rms_s = rw.rms[s]
            theo_s = rw.rms_theoretical[s]
            assert rms_s == pytest.approx(theo_s, rel=0.1), (
                f"At step {s}: RMS={rms_s:.4f}, theoretical={theo_s:.4f}"
            )

    def test_determinism_same_seed(self) -> None:
        """Same seed should produce identical trajectories."""
        rw1 = RandomWalk(n_walkers=10, n_steps=50, dim=2, seed=123)
        rw2 = RandomWalk(n_walkers=10, n_steps=50, dim=2, seed=123)
        np.testing.assert_array_equal(rw1.positions, rw2.positions)

    def test_determinism_different_seed(self) -> None:
        """Different seeds should produce different trajectories."""
        rw1 = RandomWalk(n_walkers=10, n_steps=50, dim=2, seed=123)
        rw2 = RandomWalk(n_walkers=10, n_steps=50, dim=2, seed=456)
        assert not np.allclose(rw1.positions, rw2.positions)

    def test_1d_rms_scaling(self) -> None:
        """1D random walk RMS should also scale as sqrt(N)."""
        rw = RandomWalk(n_walkers=5000, n_steps=100, step_length=1.0, dim=1, seed=42)
        rms_final = rw.rms[-1]
        theoretical = rw.rms_theoretical[-1]
        assert rms_final == pytest.approx(theoretical, rel=0.05)

    def test_distribution_symmetric(self) -> None:
        """Final displacement distribution should be roughly symmetric
        about zero (mean near zero for many walkers)."""
        rw = RandomWalk(n_walkers=2000, n_steps=50, step_length=1.0, dim=2, seed=42)
        final_pos = rw.positions[:, -1, :]  # (W, 2)
        mean_x = float(np.mean(final_pos[:, 0]))
        mean_y = float(np.mean(final_pos[:, 1]))
        # Mean should be near zero (within 0.3 step lengths)
        assert abs(mean_x) < 0.3, f"Mean x={mean_x:.4f} too far from zero"
        assert abs(mean_y) < 0.3, f"Mean y={mean_y:.4f} too far from zero"

    def test_final_displacement_distribution(self) -> None:
        """Final displacement distribution should return valid bins."""
        rw = RandomWalk(n_walkers=100, n_steps=30, dim=2, seed=42)
        counts, bin_edges = rw.final_displacement_distribution(bins=10)
        assert len(counts) > 0
        assert len(bin_edges) == 11
        assert np.sum(counts) == rw.n_walkers

    def test_step_length_affects_rms(self) -> None:
        """Doubling step length should double RMS."""
        rw1 = RandomWalk(n_walkers=2000, n_steps=50, step_length=1.0, dim=2, seed=42)
        rw2 = RandomWalk(n_walkers=2000, n_steps=50, step_length=2.0, dim=2, seed=42)
        ratio = rw2.rms[-1] / rw1.rms[-1]
        assert ratio == pytest.approx(2.0, rel=0.1), (
            f"RMS ratio={ratio:.4f}, expected 2.0"
        )

    def test_origin_start(self) -> None:
        """All walkers should start at the origin."""
        rw = RandomWalk(n_walkers=50, n_steps=20, dim=2, seed=42)
        positions = rw.positions
        assert np.all(positions[:, 0, :] == 0.0)

    def test_invalid_dim(self) -> None:
        """dim must be 1 or 2."""
        with pytest.raises(ValueError, match="dim must be 1 or 2"):
            RandomWalk(dim=3)

    def test_invalid_n_walkers(self) -> None:
        with pytest.raises(ValueError, match="n_walkers must be >= 1"):
            RandomWalk(n_walkers=0)

    def test_invalid_n_steps(self) -> None:
        with pytest.raises(ValueError, match="n_steps must be >= 1"):
            RandomWalk(n_steps=0)

    def test_invalid_step_length(self) -> None:
        with pytest.raises(ValueError, match="step_length must be positive"):
            RandomWalk(step_length=0.0)

    def test_position_distribution_at_step_2d(self) -> None:
        """position_distribution_at_step should return valid bins for 2D."""
        rw = RandomWalk(n_walkers=100, n_steps=30, dim=2, seed=42)
        xc, xe, yc, ye = rw.position_distribution_at_step(step=15, bins=10)
        assert len(xc) > 0
        assert len(yc) > 0
        assert len(xe) == 11
        assert len(ye) == 11

    def test_position_distribution_at_step_1d_raises(self) -> None:
        """position_distribution_at_step should raise for dim=1."""
        rw = RandomWalk(n_walkers=10, n_steps=10, dim=1, seed=42)
        with pytest.raises(ValueError, match="requires dim=2"):
            rw.position_distribution_at_step(step=5)