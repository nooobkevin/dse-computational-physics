"""Tests for physics_core.engineering — optical fibres, lasers, motors, transformers."""

import math

import pytest

from physics_core.engineering.lasers import Laser, ReferenceLaser
from physics_core.engineering.motors import (
    Motor,
    ReferenceMotor,
    ReferenceTransformer,
    Transformer,
)
from physics_core.engineering.optics import OpticalFibre, ReferenceOpticalFibre


# ===========================================================================
# Optical Fibre
# ===========================================================================


class TestOpticalFibre:
    """Tests for the abstract base."""

    def test_tir_raises_not_implemented(self) -> None:
        of = OpticalFibre()
        with pytest.raises(NotImplementedError):
            of.total_internal_reflection(0.5)

    def test_critical_angle_raises_not_implemented(self) -> None:
        of = OpticalFibre()
        with pytest.raises(NotImplementedError):
            _ = of.critical_angle

    def test_step_is_noop(self) -> None:
        of = OpticalFibre()
        of.step(0.1)  # should not raise

    def test_state_property(self) -> None:
        of = OpticalFibre(n1=1.5, n2=1.45, length=10.0, angle=0.5)
        s = of.state
        assert s["n1"] == pytest.approx(1.5)
        assert s["n2"] == pytest.approx(1.45)
        assert s["length"] == pytest.approx(10.0)
        assert s["angle"] == pytest.approx(0.5)


class TestReferenceOpticalFibre:
    """Tests for the reference implementation."""

    def test_critical_angle_formula(self) -> None:
        """θ_c = arcsin(n₂ / n₁)."""
        of = ReferenceOpticalFibre(n1=1.50, n2=1.45)
        expected = math.asin(1.45 / 1.50)
        assert of.critical_angle == pytest.approx(expected, rel=1e-6)

    def test_tir_above_critical(self) -> None:
        """Ray above critical angle undergoes TIR."""
        of = ReferenceOpticalFibre(n1=1.50, n2=1.45)
        crit = of.critical_angle
        assert of.total_internal_reflection(crit + 0.1) is True

    def test_leak_below_critical(self) -> None:
        """Ray below critical angle leaks out (not TIR)."""
        of = ReferenceOpticalFibre(n1=1.50, n2=1.45)
        crit = of.critical_angle
        assert of.total_internal_reflection(max(0.0, crit - 0.1)) is False

    def test_acceptance_condition(self) -> None:
        """acceptance_condition matches TIR."""
        of = ReferenceOpticalFibre(n1=1.50, n2=1.45, angle=0.5)
        crit = of.critical_angle
        assert of.acceptance_condition == (0.5 > crit)

    def test_energy_tir(self) -> None:
        """Energy is fully transmitted under TIR."""
        of = ReferenceOpticalFibre(n1=1.50, n2=1.45, angle=1.4)
        e = of.energy()
        assert e["transmitted"] == pytest.approx(1.0)
        assert e["leaked"] == pytest.approx(0.0)

    def test_energy_leak(self) -> None:
        """Energy leaks when below critical angle."""
        of = ReferenceOpticalFibre(n1=1.50, n2=1.45, angle=0.1)
        e = of.energy()
        assert e["transmitted"] == pytest.approx(0.0)
        assert e["leaked"] == pytest.approx(1.0)

    def test_ray_path_length(self) -> None:
        """Path length = L / cos(θ) for TIR."""
        of = ReferenceOpticalFibre(n1=1.50, n2=1.45, length=10.0, angle=1.4)
        expected = 10.0 / math.cos(1.4)
        assert of.ray_path_length() == pytest.approx(expected, rel=1e-6)

    def test_no_tir_possible_when_n1_le_n2(self) -> None:
        """No TIR when core index <= cladding index."""
        of = ReferenceOpticalFibre(n1=1.45, n2=1.50)
        assert of.total_internal_reflection(1.5) is False


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
# Motor
# ===========================================================================


class TestMotor:
    """Tests for the abstract base."""

    def test_torque_raises_not_implemented(self) -> None:
        motor = Motor()
        with pytest.raises(NotImplementedError):
            motor.torque()


class TestReferenceMotor:
    """Tests for the reference motor."""

    def test_torque_nonzero(self) -> None:
        motor = ReferenceMotor(B=0.5, I=2.0, L=0.1, N=1)
        tau = motor.torque()
        assert tau > 0.0

    def test_step_advances_state(self) -> None:
        motor = ReferenceMotor(B=0.5, I=2.0, L=0.1, N=1)
        initial_theta = motor.state["theta"]
        motor.step(0.01)
        assert motor.state["theta"] != initial_theta


# ===========================================================================
# Transformer
# ===========================================================================


class TestTransformer:
    """Tests for the abstract base."""

    def test_secondary_voltage_raises_not_implemented(self) -> None:
        t = Transformer()
        with pytest.raises(NotImplementedError):
            t.secondary_voltage()

    def test_primary_current_raises_not_implemented(self) -> None:
        t = Transformer()
        with pytest.raises(NotImplementedError):
            t.primary_current()


class TestReferenceTransformer:
    """Tests for the reference transformer."""

    def test_voltage_ratio(self) -> None:
        """Vp / Vs ≈ Np / Ns."""
        t = ReferenceTransformer(Np=100, Ns=50, Vp=230.0)
        t.step()
        Vs = t.state["Vs"]
        ratio_actual = 230.0 / Vs
        ratio_expected = 100.0 / 50.0
        assert ratio_actual == pytest.approx(ratio_expected, rel=1e-6)

    def test_current_ratio(self) -> None:
        """Ip / Is = Ns / Np for ideal transformer."""
        t = ReferenceTransformer(Np=100, Ns=50, Vp=230.0, load_resistance=20.0)
        t.step()
        Ip = t.state["Ip"]
        Is = t.state["Is"]
        # Ip/Is should be Ns/Np = 50/100 = 0.5
        assert Ip / Is == pytest.approx(50.0 / 100.0, rel=1e-6)

    def test_power_conservation(self) -> None:
        """Vp * Ip ≈ Vs * Is for ideal transformer."""
        t = ReferenceTransformer(Np=100, Ns=50, Vp=230.0, load_resistance=20.0)
        t.step()
        Pp = t.state["Vp"] * t.state["Ip"]
        Ps = t.state["Vs"] * t.state["Is"]
        assert Pp == pytest.approx(Ps, rel=1e-6)

    def test_step_up_voltage(self) -> None:
        """Step-up: Ns > Np → Vs > Vp."""
        t = ReferenceTransformer(Np=50, Ns=100, Vp=230.0)
        t.step()
        assert t.state["Vs"] > t.state["Vp"]

    def test_step_down_voltage(self) -> None:
        """Step-down: Ns < Np → Vs < Vp."""
        t = ReferenceTransformer(Np=100, Ns=50, Vp=230.0)
        t.step()
        assert t.state["Vs"] < t.state["Vp"]