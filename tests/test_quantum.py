"""Tests for physics_core.quantum — QuantumWell, ReferenceQuantumWell, PhotoElectric."""

import math

import pytest

from physics_core.quantum.wavefunctions import (
    H,
    M_E,
    QuantumWell,
    ReferenceQuantumWell,
)
from physics_core.quantum.photoelectric import E_CHARGE, PhotoElectric


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
