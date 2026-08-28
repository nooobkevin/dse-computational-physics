"""Tests for physics_core.quantum — QuantumWell, ReferenceQuantumWell, PhotoElectric, Laser, Rutherford, Bohr."""

import math

import pytest

from physics_core.quantum.wavefunctions import (
    H,
    M_E,
    QuantumWell,
    ReferenceQuantumWell,
)
from physics_core.quantum.photoelectric import E_CHARGE, PhotoElectric
from physics_core.quantum.lasers import Laser, ReferenceLaser
from physics_core.quantum.rutherford import (
    K_COULOMB,
    RutherfordScattering,
    ReferenceRutherfordScattering,
)
from physics_core.quantum.bohr import BohrHydrogen


class TestQuantumWell:
    """Tests for the abstract base."""

    def test_energy_level_raises_not_implemented(self) -> None:
        well = QuantumWell()
        with pytest.raises(NotImplementedError):
            well.energy_level(1)

    def test_wavefunction_raises_not_implemented(self) -> None:
        well = QuantumWell()
        with pytest.raises(NotImplementedError):
            well.wavefunction(0.5e-10, 1)

    def test_step_does_not_raise(self) -> None:
        """step() is a no-op for the base class."""
        well = QuantumWell()
        well.step()  # should not raise
        assert well.state["t"] == pytest.approx(0.01)

    def test_state_property(self) -> None:
        well = QuantumWell(L=2e-10, n=3)
        s = well.state
        assert s["n"] == 3
        assert s["x"] == pytest.approx(1e-10)
        assert s["t"] == pytest.approx(0.0)

    def test_state_is_copy(self) -> None:
        well = QuantumWell()
        s1 = well.state
        s1["n"] = 99
        assert well.state["n"] == 1

    def test_position(self) -> None:
        well = QuantumWell(L=2e-10)
        pos = well.position
        assert pos[0] == pytest.approx(1e-10)
        assert pos[1] == pytest.approx(0.0)

    def test_energy_raises_not_implemented(self) -> None:
        well = QuantumWell()
        with pytest.raises(NotImplementedError):
            _ = well.energy

    def test_de_broglie_wavelength(self) -> None:
        well = QuantumWell()
        p = 1.0e-24
        lam = well.de_broglie_wavelength(p)
        assert lam == pytest.approx(H / p)

    def test_de_broglie_zero_momentum_raises(self) -> None:
        well = QuantumWell()
        with pytest.raises(ValueError, match="Momentum cannot be zero"):
            well.de_broglie_wavelength(0.0)


class TestReferenceQuantumWell:
    """Tests for the reference implementation."""

    def test_energy_level_n1(self) -> None:
        """E_1 = h² / (8 m L²)"""
        L = 1e-10
        m = M_E
        well = ReferenceQuantumWell(L=L, m=m)
        expected = (1 * 1 * H * H) / (8.0 * m * L * L)
        assert well.energy_level(1) == pytest.approx(expected)

    def test_energy_level_n2(self) -> None:
        """E_2 = 4 * E_1"""
        well = ReferenceQuantumWell(L=1e-10)
        e1 = well.energy_level(1)
        e2 = well.energy_level(2)
        assert e2 == pytest.approx(4.0 * e1)

    def test_energy_level_n3(self) -> None:
        """E_3 = 9 * E_1"""
        well = ReferenceQuantumWell(L=1e-10)
        e1 = well.energy_level(1)
        e3 = well.energy_level(3)
        assert e3 == pytest.approx(9.0 * e1)

    def test_energy_level_n_lt_1_raises(self) -> None:
        well = ReferenceQuantumWell()
        with pytest.raises(ValueError, match="Quantum number n must be >= 1"):
            well.energy_level(0)

    def test_wavefunction_n1_at_centre(self) -> None:
        """ψ_1(L/2) = √(2/L) sin(π/2) = √(2/L)"""
        L = 1e-10
        well = ReferenceQuantumWell(L=L)
        x = L / 2.0
        expected = math.sqrt(2.0 / L)
        assert well.wavefunction(x, 1) == pytest.approx(expected)

    def test_wavefunction_n1_at_walls(self) -> None:
        """ψ_1(0) = ψ_1(L) = 0"""
        L = 1e-10
        well = ReferenceQuantumWell(L=L)
        assert well.wavefunction(0.0, 1) == pytest.approx(0.0, abs=1e-10)
        assert well.wavefunction(L, 1) == pytest.approx(0.0, abs=1e-10)

    def test_wavefunction_n2_node_at_centre(self) -> None:
        """ψ_2(L/2) = 0 (node at centre)"""
        L = 1e-10
        well = ReferenceQuantumWell(L=L)
        assert well.wavefunction(L / 2.0, 2) == pytest.approx(0.0, abs=1e-10)

    def test_wavefunction_outside_well(self) -> None:
        """ψ_n(x) = 0 for x < 0 or x > L"""
        L = 1e-10
        well = ReferenceQuantumWell(L=L)
        assert well.wavefunction(-1e-11, 1) == pytest.approx(0.0)
        assert well.wavefunction(L + 1e-11, 1) == pytest.approx(0.0)

    def test_probability_density_integrates_to_one(self) -> None:
        """∫₀ᴸ |ψ_n(x)|² dx ≈ 1 (numerical integration)"""
        L = 1e-10
        well = ReferenceQuantumWell(L=L)
        n_steps = 1000
        dx = L / n_steps
        total = 0.0
        for i in range(n_steps):
            x = (i + 0.5) * dx
            total += well.probability_density(x, 1) * dx
        assert total == pytest.approx(1.0, rel=0.01)

    def test_transition_energy(self) -> None:
        """ΔE = E_2 - E_1"""
        well = ReferenceQuantumWell(L=1e-10)
        delta = well.transition_energy(1, 2)
        expected = well.energy_level(2) - well.energy_level(1)
        assert delta == pytest.approx(expected)

    def test_transition_wavelength(self) -> None:
        """λ = hc / ΔE"""
        well = ReferenceQuantumWell(L=1e-10)
        lam = well.transition_wavelength(1, 2)
        delta_e = well.transition_energy(1, 2)
        expected = H * 299792458.0 / delta_e
        assert lam == pytest.approx(expected)

    def test_energy_property(self) -> None:
        well = ReferenceQuantumWell(L=1e-10, n=2)
        assert well.energy == pytest.approx(well.energy_level(2))

    def test_de_broglie_wavelength(self) -> None:
        """λ = h/p for a given momentum."""
        well = ReferenceQuantumWell()
        p = 1.0e-24
        lam = well.de_broglie_wavelength(p)
        assert lam == pytest.approx(H / p)


class TestPhotoElectric:
    """Tests for the photoelectric effect calculator."""

    def test_threshold_frequency(self) -> None:
        """f_0 = φ / h"""
        phi = 2.0 * E_CHARGE  # 2 eV
        pe = PhotoElectric(work_function=phi)
        expected = phi / H
        assert pe.threshold_frequency() == pytest.approx(expected)

    def test_max_kinetic_energy_above_threshold(self) -> None:
        """K_max = hf - φ"""
        phi = 2.0 * E_CHARGE
        pe = PhotoElectric(work_function=phi)
        f = 1.0e15  # Hz (above threshold)
        expected = H * f - phi
        assert pe.max_kinetic_energy(f) == pytest.approx(expected)

    def test_max_kinetic_energy_below_threshold(self) -> None:
        """K_max = 0 when f < f_0"""
        phi = 5.0 * E_CHARGE  # high work function
        pe = PhotoElectric(work_function=phi)
        f = 1.0e14  # Hz (below threshold)
        assert pe.max_kinetic_energy(f) == pytest.approx(0.0)

    def test_stopping_potential(self) -> None:
        """V_0 = (hf - φ) / e"""
        phi = 2.0 * E_CHARGE
        pe = PhotoElectric(work_function=phi)
        f = 1.0e15
        expected = (H * f - phi) / E_CHARGE
        assert pe.stopping_potential(f) == pytest.approx(expected)

    def test_stopping_potential_below_threshold(self) -> None:
        """V_0 = 0 when f < f_0"""
        phi = 5.0 * E_CHARGE
        pe = PhotoElectric(work_function=phi)
        f = 1.0e14
        assert pe.stopping_potential(f) == pytest.approx(0.0)

    def test_work_function_eV(self) -> None:
        phi = 3.0 * E_CHARGE
        pe = PhotoElectric(work_function=phi)
        assert pe.work_function_eV() == pytest.approx(3.0)

    def test_max_ke_eV(self) -> None:
        phi = 2.0 * E_CHARGE
        pe = PhotoElectric(work_function=phi)
        f = 1.0e15
        expected_eV = (H * f - phi) / E_CHARGE
        assert pe.max_ke_eV(f) == pytest.approx(expected_eV)


# ===========================================================================
# Laser
# ===========================================================================


class TestLaser:
    """Tests for the abstract base."""

    def test_stimulated_emission_raises_not_implemented(self) -> None:
        laser = Laser()
        with pytest.raises(NotImplementedError):
            laser.stimulated_emission()


class TestReferenceLaser:
    """Tests for the reference laser."""

    def test_population_inversion(self) -> None:
        laser = ReferenceLaser(N_upper=100, N_lower=10)
        assert laser.population_inversion is True

    def test_no_inversion(self) -> None:
        laser = ReferenceLaser(N_upper=10, N_lower=100)
        assert laser.population_inversion is False

    def test_stimulated_emission_with_inversion(self) -> None:
        laser = ReferenceLaser(N_upper=100, N_lower=10)
        photons = laser.stimulated_emission()
        assert photons > 0

    def test_no_emission_without_inversion(self) -> None:
        laser = ReferenceLaser(N_upper=10, N_lower=100)
        photons = laser.stimulated_emission()
        assert photons == pytest.approx(0.0)

    def test_step_increases_photon_count(self) -> None:
        laser = ReferenceLaser(N_upper=100, N_lower=10)
        initial = laser.state["photon_count"]
        laser.step(0.1)
        assert laser.state["photon_count"] > initial


# ===========================================================================
# Rutherford scattering
# ===========================================================================


class TestRutherfordScattering:
    """Tests for the abstract base."""

    def test_scattering_angle_raises_not_implemented(self) -> None:
        r = RutherfordScattering()
        with pytest.raises(NotImplementedError):
            r.scattering_angle(1e-14, 5e6 * E_CHARGE)

    def test_coulomb_constant_value(self) -> None:
        r = RutherfordScattering(Z1=2, Z2=79)
        k = r.coulomb_constant()
        expected = K_COULOMB * 2 * 79 * E_CHARGE * E_CHARGE
        assert k == pytest.approx(expected)

    def test_impact_parameters_length(self) -> None:
        r = RutherfordScattering()
        bs = r.impact_parameters(10)
        assert len(bs) == 10

    def test_state_property(self) -> None:
        r = ReferenceRutherfordScattering(b=1e-14, E=5e6 * E_CHARGE)
        s = r.state
        assert "b" in s
        assert "E" in s
        assert "theta" in s
        assert "t" in s

    def test_trajectory_points_nonempty(self) -> None:
        r = ReferenceRutherfordScattering(b=1e-14, E=5e6 * E_CHARGE)
        pts = r.trajectory_points(b=1e-14, E=5e6 * E_CHARGE, n_points=50)
        assert len(pts) > 0


class TestReferenceRutherfordScattering:
    """Tests for the reference implementation."""

    def test_head_on_backscattering(self) -> None:
        """b → 0 gives θ → π (180°)."""
        r = ReferenceRutherfordScattering(Z1=2, Z2=79)
        theta = r.scattering_angle(b=1e-20, E=5e6 * E_CHARGE)
        assert theta == pytest.approx(math.pi, rel=0.01)

    def test_head_on_limit_exact(self) -> None:
        """b = 0 exactly gives π."""
        r = ReferenceRutherfordScattering()
        assert r.scattering_angle(b=0.0, E=5e6 * E_CHARGE) == pytest.approx(math.pi)

    def test_large_b_small_angle(self) -> None:
        """Large impact parameter → small scattering angle."""
        r = ReferenceRutherfordScattering(Z1=2, Z2=79)
        theta_small = r.scattering_angle(b=1e-12, E=5e6 * E_CHARGE)
        theta_large = r.scattering_angle(b=1e-10, E=5e6 * E_CHARGE)
        assert theta_large < theta_small

    def test_larger_b_gives_smaller_theta(self) -> None:
        """Monotonic: increasing b must decrease θ."""
        r = ReferenceRutherfordScattering(Z1=2, Z2=79, E=5e6 * E_CHARGE)
        bs = [1e-15, 1e-14, 1e-13, 1e-12]
        thetas = [r.scattering_angle(b, 5e6 * E_CHARGE) for b in bs]
        for i in range(1, len(thetas)):
            assert thetas[i] < thetas[i - 1], (
                f"Scattering angle should decrease with increasing b. "
                f"θ({bs[i-1]})={thetas[i-1]}, θ({bs[i]})={thetas[i]}"
            )

    def test_higher_energy_smaller_angle(self) -> None:
        """Higher energy at same b → smaller θ."""
        r = ReferenceRutherfordScattering(Z1=2, Z2=79, b=1e-14)
        theta_low = r.scattering_angle(1e-14, 1e6 * E_CHARGE)
        theta_high = r.scattering_angle(1e-14, 10e6 * E_CHARGE)
        assert theta_high < theta_low

    def test_symmetry_zero_energy_gives_pi(self) -> None:
        """E = 0 gives head-on result π."""
        r = ReferenceRutherfordScattering()
        assert r.scattering_angle(b=1e-14, E=0.0) == pytest.approx(math.pi)

    def test_trajectory_head_on(self) -> None:
        """Head-on trajectory should be along x-axis (y ≈ 0)."""
        r = ReferenceRutherfordScattering(b=1e-20, E=5e6 * E_CHARGE)
        pts = r.trajectory_points(b=1e-20, E=5e6 * E_CHARGE, n_points=50)
        ys = [abs(p[1]) for p in pts]
        assert max(ys) < 1e-20 or all(y < 1e-12 for y in ys)


# ===========================================================================
# Bohr hydrogen atom
# ===========================================================================


class TestBohrHydrogen:
    """Tests for the Bohr hydrogen atom model."""

    def test_energy_level_n1(self) -> None:
        """E₁ = -13.6 eV"""
        bohr = BohrHydrogen()
        e1 = bohr.energy_level(1)
        assert e1 == pytest.approx(-13.6, abs=0.01)  # -13.6 eV

    def test_energy_level_n2(self) -> None:
        """E₂ = -13.6 / 4 = -3.4 eV"""
        bohr = BohrHydrogen()
        e2 = bohr.energy_level(2)
        assert e2 == pytest.approx(-13.6 / 4.0, abs=0.01)

    def test_energy_level_n3(self) -> None:
        """E₃ = -13.6 / 9 ≈ -1.511 eV"""
        bohr = BohrHydrogen()
        e3 = bohr.energy_level(3)
        assert e3 == pytest.approx(-13.6 / 9.0, abs=0.01)

    def test_energy_level_negative(self) -> None:
        """All energy levels are negative (bound states)."""
        bohr = BohrHydrogen()
        for n in range(1, 10):
            assert bohr.energy_level(n) < 0

    def test_energy_level_converges_to_zero(self) -> None:
        """E_n → 0 as n → ∞."""
        bohr = BohrHydrogen()
        e100 = bohr.energy_level(100)
        assert abs(e100) < 0.01  # -0.00136 eV, very close to zero

    def test_lyman_alpha_wavelength(self) -> None:
        """Lyman-alpha (n=2 → n=1): λ ≈ 121.6 nm."""
        bohr = BohrHydrogen()
        lam = bohr.transition_wavelength(2, 1)
        expected = 121.6e-9
        assert lam == pytest.approx(expected, rel=0.01)

    def test_balmer_alpha_wavelength(self) -> None:
        """Hα (n=3 → n=2): λ ≈ 656.3 nm."""
        bohr = BohrHydrogen()
        lam = bohr.transition_wavelength(3, 2)
        expected = 656.3e-9
        assert lam == pytest.approx(expected, rel=0.01)

    def test_balmer_beta_wavelength(self) -> None:
        """Hβ (n=4 → n=2): λ ≈ 486.1 nm."""
        bohr = BohrHydrogen()
        lam = bohr.transition_wavelength(4, 2)
        assert lam == pytest.approx(486.1e-9, rel=0.01)

    def test_balmer_gamma_wavelength(self) -> None:
        """Hγ (n=5 → n=2): λ ≈ 434.0 nm."""
        bohr = BohrHydrogen()
        lam = bohr.transition_wavelength(5, 2)
        assert lam == pytest.approx(434.0e-9, rel=0.01)

    def test_ionisation_energy_n1(self) -> None:
        """Ionisation from n=1 = 13.6 eV."""
        bohr = BohrHydrogen()
        ion = bohr.ionisation_energy(1)
        assert ion == pytest.approx(13.6, abs=0.01)

    def test_ionisation_energy_n2(self) -> None:
        """Ionisation from n=2 = 3.4 eV."""
        bohr = BohrHydrogen()
        ion = bohr.ionisation_energy(2)
        assert ion == pytest.approx(13.6 / 4.0, abs=0.01)

    def test_transition_photon_energy(self) -> None:
        """ΔE = hc/λ for Lyman-alpha."""
        bohr = BohrHydrogen()
        lam = bohr.transition_wavelength(2, 1)
        delta_e = bohr.transition_energy(2, 1)
        hc = 1239.84  # eV·nm
        expected_lam = hc / abs(delta_e) * 1e-9  # convert nm to m
        assert lam == pytest.approx(expected_lam, rel=0.01)

    def test_emission_photon_energy_positive(self) -> None:
        """Photon energy for emission is always positive (using absolute value)."""
        bohr = BohrHydrogen()
        e_photon = bohr.transition_energy(3, 2)
        # For emission (n_f < n_i), ΔE is negative; the photon energy is |ΔE|
        assert abs(e_photon) > 0
        expected = 13.6 * (1.0 / 4.0 - 1.0 / 9.0)
        assert abs(e_photon) == pytest.approx(expected, abs=0.01)

    def test_absorption_photon_energy(self) -> None:
        """Energy required for n=1 → n=2 equals |E₂ - E₁|."""
        bohr = BohrHydrogen()
        e_abs = bohr.transition_energy(1, 2)
        assert e_abs == pytest.approx(10.2, abs=0.1)
