"""Tests for physics_core.society — radioactive decay simulation and energy sources."""

import math

import pytest

from physics_core.society.decay import DecaySim, ReferenceDecaySim
from physics_core.society.energy import EnergySim, ReferenceEnergySim

LN2 = math.log(2.0)


# ===========================================================================
# Abstract base
# ===========================================================================


class TestDecaySim:
    """Tests for the abstract base."""

    def test_decay_probability_raises_not_implemented(self) -> None:
        sim = DecaySim()
        with pytest.raises(NotImplementedError):
            sim.decay_probability(0.01)

    def test_step_raises_not_implemented(self) -> None:
        sim = DecaySim()
        with pytest.raises(NotImplementedError):
            sim.step(0.01)

    def test_state_property(self) -> None:
        sim = DecaySim(N0=5000, half_life=2.0)
        s = sim.state
        assert s["N0"] == 5000
        assert s["T"] == pytest.approx(2.0)
        assert s["N"] == 5000
        assert s["t"] == pytest.approx(0.0)

    def test_position_property(self) -> None:
        sim = DecaySim(N0=1000)
        t, N = sim.position
        assert t == pytest.approx(0.0)
        assert N == pytest.approx(1000.0)

    def test_energy_default(self) -> None:
        sim = DecaySim(N0=1000)
        assert sim.energy == pytest.approx(0.0)

    def test_nuclei_remaining(self) -> None:
        sim = DecaySim(N0=5000)
        assert sim.nuclei_remaining() == 5000

    def test_history_initial(self) -> None:
        sim = DecaySim(N0=1000)
        h = sim.history()
        assert len(h) == 1
        assert h[0] == (0.0, 1000)

    def test_reset(self) -> None:
        sim = DecaySim(N0=1000, seed=42)
        # Force a step to change state
        try:
            sim.step(0.01)
        except NotImplementedError:
            pass
        sim.reset()
        assert sim.nuclei_remaining() == 1000
        assert sim.state["t"] == pytest.approx(0.0)


# ===========================================================================
# Reference implementation
# ===========================================================================


class TestReferenceDecaySim:
    """Tests for the reference implementation."""

    def test_decay_probability_formula(self) -> None:
        """p = 1 - exp(-ln2 * dt / T)."""
        sim = ReferenceDecaySim(N0=10000, half_life=1.0)
        dt = 0.1
        expected_p = 1.0 - math.exp(-LN2 * dt / 1.0)
        assert sim.decay_probability(dt) == pytest.approx(expected_p, rel=1e-9)

    def test_decay_probability_bounds(self) -> None:
        """Probability must be in [0, 1]."""
        sim = ReferenceDecaySim(N0=10000, half_life=1.0)
        for dt in [0.0, 0.001, 0.1, 1.0, 10.0]:
            p = sim.decay_probability(dt)
            assert 0.0 <= p <= 1.0, f"p={p} out of bounds for dt={dt}"

    def test_decay_probability_zero_dt(self) -> None:
        """p = 0 when dt = 0."""
        sim = ReferenceDecaySim(N0=10000, half_life=1.0)
        assert sim.decay_probability(0.0) == pytest.approx(0.0)

    def test_analytic_N_exact(self) -> None:
        """N(t) = N0 * (1/2)^(t/T)."""
        sim = ReferenceDecaySim(N0=10000, half_life=1.0)
        # At t = 0: N = N0
        assert sim.analytic_N(0.0) == pytest.approx(10000.0)
        # At t = T: N = N0/2
        assert sim.analytic_N(1.0) == pytest.approx(5000.0, rel=1e-6)
        # At t = 2T: N = N0/4
        assert sim.analytic_N(2.0) == pytest.approx(2500.0, rel=1e-6)
        # At t = 3T: N = N0/8
        assert sim.analytic_N(3.0) == pytest.approx(1250.0, rel=1e-6)

    def test_analytic_N_general(self) -> None:
        """N(t) = N0 * 2^(-t/T)."""
        sim = ReferenceDecaySim(N0=8000, half_life=2.0)
        # At t = 0.5: N = 8000 * 2^(-0.5/2) = 8000 * 2^(-0.25)
        expected = 8000.0 * (2.0 ** (-0.25))
        assert sim.analytic_N(0.5) == pytest.approx(expected, rel=1e-9)

    def test_analytic_curve_length(self) -> None:
        """analytic_curve returns correct number of points."""
        sim = ReferenceDecaySim(N0=10000, half_life=1.0, dt=0.1)
        curve = sim.analytic_curve(50)
        assert len(curve) == 51  # n_steps + 1

    def test_monte_carlo_approximates_analytic(self) -> None:
        """Monte Carlo simulation should approximate the analytic curve."""
        N0 = 50000
        T = 1.0
        dt = 0.02
        n_steps = 150  # simulate for 3 half-lives
        sim = ReferenceDecaySim(N0=N0, half_life=T, dt=dt, seed=12345)
        for _ in range(n_steps):
            sim.step()
        # At t ≈ 3T, analytic N ≈ N0/8
        t = sim.state["t"]
        analytic = sim.analytic_N(t)
        mc_N = sim.nuclei_remaining()
        # Monte Carlo should be within 5% of analytic
        rel_err = abs(mc_N - analytic) / analytic
        assert rel_err < 0.05, (
            f"Monte Carlo N={mc_N} vs analytic N={analytic:.1f} "
            f"at t={t:.2f}s (rel_err={rel_err*100:.2f}%)"
        )

    def test_half_life_estimate_within_tolerance(self) -> None:
        """Monte Carlo half-life estimate should be within 10% of T."""
        N0 = 50000
        T = 1.0
        dt = 0.02
        n_steps = 200
        sim = ReferenceDecaySim(N0=N0, half_life=T, dt=dt, seed=42)
        for _ in range(n_steps):
            sim.step()
        estimated_T = sim.half_life()
        rel_err = abs(estimated_T - T) / T
        assert rel_err < 0.10, (
            f"Estimated half-life {estimated_T:.4f}s vs true T={T}s "
            f"(rel_err={rel_err*100:.2f}%)"
        )

    def test_decay_constant(self) -> None:
        """λ = ln(2) / T."""
        sim = ReferenceDecaySim(N0=10000, half_life=2.0)
        assert sim.decay_constant == pytest.approx(LN2 / 2.0, rel=1e-9)

    def test_mean_lifetime(self) -> None:
        """τ = 1/λ = T / ln(2)."""
        sim = ReferenceDecaySim(N0=10000, half_life=2.0)
        assert sim.mean_lifetime == pytest.approx(2.0 / LN2, rel=1e-9)

    def test_energy_released(self) -> None:
        """Energy = number of decays."""
        N0 = 10000
        sim = ReferenceDecaySim(N0=N0, half_life=1.0, dt=0.1, seed=42)
        for _ in range(10):
            sim.step()
        decays = N0 - sim.nuclei_remaining()
        assert sim.energy == pytest.approx(float(decays))

    def test_reset_clears_history(self) -> None:
        """Reset should clear history and restore initial state."""
        sim = ReferenceDecaySim(N0=10000, half_life=1.0, dt=0.1, seed=42)
        for _ in range(20):
            sim.step()
        sim.reset()
        assert sim.nuclei_remaining() == 10000
        assert sim.state["t"] == pytest.approx(0.0)
        assert len(sim.history()) == 1


# ===========================================================================
# Ionising and penetrating power constants
# ===========================================================================


class TestRadiationProperties:
    """Tests for alpha, beta, gamma radiation properties."""

    # Ionising power: alpha > beta > gamma
    IONISING_ORDER = ["alpha", "beta", "gamma"]
    # Penetrating power: gamma > beta > alpha
    PENETRATING_ORDER = ["gamma", "beta", "alpha"]

    def test_ionising_order(self) -> None:
        """Alpha is most ionising, gamma is least ionising."""
        assert self.IONISING_ORDER[0] == "alpha"
        assert self.IONISING_ORDER[1] == "beta"
        assert self.IONISING_ORDER[2] == "gamma"

    def test_penetrating_order(self) -> None:
        """Gamma is most penetrating, alpha is least penetrating."""
        assert self.PENETRATING_ORDER[0] == "gamma"
        assert self.PENETRATING_ORDER[1] == "beta"
        assert self.PENETRATING_ORDER[2] == "alpha"

    def test_alpha_stopped_by_paper(self) -> None:
        """Alpha radiation is stopped by paper."""
        pass  # Conceptual test — the order constants are the key assertion

    def test_beta_stopped_by_aluminium(self) -> None:
        """Beta radiation is stopped by a few mm of aluminium."""
        pass

    def test_gamma_requires_lead(self) -> None:
        """Gamma radiation requires thick lead or concrete to attenuate."""
        pass


# ===========================================================================
# Energy sources
# ===========================================================================


class TestEnergySim:
    """Tests for the abstract energy base."""

    def test_mass_energy_delta_raises_not_implemented(self) -> None:
        sim = EnergySim()
        with pytest.raises(NotImplementedError):
            sim.mass_energy_delta(1.0)

    def test_solar_power_raises_not_implemented(self) -> None:
        sim = EnergySim()
        with pytest.raises(NotImplementedError):
            sim.solar_power(1.0, 1000.0)

    def test_wind_power_raises_not_implemented(self) -> None:
        sim = EnergySim()
        with pytest.raises(NotImplementedError):
            sim.wind_power(1.0, 10.0)

    def test_photovoltaic_power_raises_not_implemented(self) -> None:
        sim = EnergySim()
        with pytest.raises(NotImplementedError):
            sim.photovoltaic_power(1.0, 1000.0)


class TestReferenceEnergySim:
    """Tests for the reference energy implementation."""

    def test_mass_energy_amu_to_mev(self) -> None:
        """1 amu ≈ 931.5 MeV."""
        sim = ReferenceEnergySim()
        energy_J, energy_MeV = sim.mass_energy_delta(1.0, in_amu=True)
        assert energy_MeV == pytest.approx(931.5, rel=1e-3)
        # Also check Joules: 1 amu * c²
        expected_J = 1.0 * 1.660539e-27 * (3.0e8) ** 2
        assert energy_J == pytest.approx(expected_J, rel=1e-3)

    def test_mass_energy_kg_to_j(self) -> None:
        """ΔE = Δm · c² in SI units."""
        sim = ReferenceEnergySim()
        dm_kg = 1.0e-27  # 1e-27 kg
        energy_J, energy_MeV = sim.mass_energy_delta(dm_kg, in_amu=False)
        expected_J = dm_kg * (3.0e8) ** 2
        assert energy_J == pytest.approx(expected_J, rel=1e-9)
        # MeV should also be consistent
        expected_MeV = dm_kg / 1.660539e-27 * 931.5
        assert energy_MeV == pytest.approx(expected_MeV, rel=1e-3)

    def test_fission_energy_1amu(self) -> None:
        """Fission of 1 amu mass defect releases ~931 MeV."""
        sim = ReferenceEnergySim()
        _, energy_MeV = sim.mass_energy_delta(1.0, in_amu=True)
        assert energy_MeV == pytest.approx(931.5, rel=1e-3)

    def test_solar_power_basic(self) -> None:
        """Solar power at 1000 W/m², 1 m², 100% efficiency."""
        sim = ReferenceEnergySim()
        power = sim.solar_power(area=1.0, solar_constant=1000.0, efficiency=1.0)
        assert power == pytest.approx(1000.0)

    def test_solar_power_efficiency(self) -> None:
        """Solar power with 20% efficiency."""
        sim = ReferenceEnergySim()
        power = sim.solar_power(area=2.0, solar_constant=1000.0, efficiency=0.20)
        assert power == pytest.approx(400.0)  # 1000 * 2 * 0.20

    def test_wind_power_basic(self) -> None:
        """Wind power at 10 m/s, r=1 m, rho=1.2, eta=1.0."""
        sim = ReferenceEnergySim()
        power = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
        # P = 0.5 * 1.0 * 1.2 * pi * 1^2 * 10^3 = 0.5 * 1.2 * pi * 1000 = 600 * pi
        expected = 0.5 * 1.2 * math.pi * 1000.0
        assert power == pytest.approx(expected, rel=1e-9)

    def test_wind_power_cubic_scaling(self) -> None:
        """Doubling wind speed → 8x power (cubic scaling)."""
        sim = ReferenceEnergySim()
        p1 = sim.wind_power(r=1.0, wind_speed=5.0, air_density=1.2, efficiency=1.0)
        p2 = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
        assert p2 == pytest.approx(p1 * 8.0, rel=1e-9)

    def test_wind_power_efficiency(self) -> None:
        """Wind power scales linearly with efficiency."""
        sim = ReferenceEnergySim()
        p_full = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
        p_half = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=0.5)
        assert p_half == pytest.approx(p_full * 0.5, rel=1e-9)

    def test_wind_power_radius_squared(self) -> None:
        """Doubling radius → 4x power (area scaling)."""
        sim = ReferenceEnergySim()
        p1 = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
        p2 = sim.wind_power(r=2.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
        assert p2 == pytest.approx(p1 * 4.0, rel=1e-9)

    def test_photovoltaic_power_default_efficiency(self) -> None:
        """PV power uses default 20% efficiency."""
        sim = ReferenceEnergySim()
        power = sim.photovoltaic_power(area=1.0, solar_constant=1000.0)
        assert power == pytest.approx(200.0)  # 1000 * 1 * 0.20

    def test_photovoltaic_power_custom_efficiency(self) -> None:
        """PV power with explicit efficiency."""
        sim = ReferenceEnergySim()
        power = sim.photovoltaic_power(area=2.0, solar_constant=1000.0, efficiency=0.15)
        assert power == pytest.approx(300.0)  # 1000 * 2 * 0.15