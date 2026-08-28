"""Tests for physics_core.engineering — optical fibres, motors, transformers, orbital, fluid, induction."""

import math

import pytest

from physics_core.engineering.fluid import FluidFlow, ReferenceFluidFlow
from physics_core.engineering.induction import InductionCoil, ReferenceInductionCoil
from physics_core.engineering.motors import (
    Motor,
    ReferenceMotor,
    ReferenceTransformer,
    Transformer,
)
from physics_core.engineering.optics import OpticalFibre, ReferenceOpticalFibre
from physics_core.engineering.orbital import OrbitSim, ReferenceOrbitalBody


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


# ===========================================================================
# Orbital Mechanics
# ===========================================================================


class TestOrbitSim:
    """Tests for the abstract base."""

    def test_gravitational_force_raises(self) -> None:
        sim = OrbitSim()
        with pytest.raises(NotImplementedError):
            sim.gravitational_force(7e6)

    def test_orbital_velocity_raises(self) -> None:
        sim = OrbitSim()
        with pytest.raises(NotImplementedError):
            sim.orbital_velocity(7e6)

    def test_escape_velocity_raises(self) -> None:
        sim = OrbitSim()
        with pytest.raises(NotImplementedError):
            sim.escape_velocity(7e6)

    def test_gpe_raises(self) -> None:
        sim = OrbitSim()
        with pytest.raises(NotImplementedError):
            sim.gravitational_potential_energy(7e6)

    def test_total_energy_raises(self) -> None:
        sim = OrbitSim()
        with pytest.raises(NotImplementedError):
            sim.total_energy(7e6, 7540.0)

    def test_properties(self) -> None:
        sim = OrbitSim(x=7e6, y=0.0)
        assert sim.radius == pytest.approx(7e6)
        assert sim.speed == pytest.approx(7540.0)


class TestReferenceOrbitalBody:
    """Tests for the reference orbital body."""

    G = 6.67430e-11
    M = 5.972e24
    m = 1000.0
    R = 7.0e6

    def test_gravitational_force_formula(self) -> None:
        """F = G M m / r²."""
        sim = ReferenceOrbitalBody(M=self.M, m=self.m)
        r = self.R
        expected = self.G * self.M * self.m / (r * r)
        assert sim.gravitational_force(r) == pytest.approx(expected, rel=1e-6)

    def test_orbital_velocity_formula(self) -> None:
        """v_orb = √(G M / r)."""
        sim = ReferenceOrbitalBody(M=self.M)
        r = self.R
        expected = math.sqrt(self.G * self.M / r)
        assert sim.orbital_velocity(r) == pytest.approx(expected, rel=1e-6)

    def test_escape_velocity_formula(self) -> None:
        """v_esc = √(2 G M / r)."""
        sim = ReferenceOrbitalBody(M=self.M)
        r = self.R
        v_orb = math.sqrt(self.G * self.M / r)
        v_esc_actual = sim.escape_velocity(r)
        assert v_esc_actual == pytest.approx(math.sqrt(2) * v_orb, rel=1e-6)
        # v_esc ≈ 11.2 km/s for Earth at surface
        earth_surface_r = 6.371e6
        v_esc_earth = sim.escape_velocity(earth_surface_r)
        assert v_esc_earth == pytest.approx(11200.0, rel=0.1)

    def test_gpe_formula(self) -> None:
        """U = -G M m / r."""
        sim = ReferenceOrbitalBody(M=self.M, m=self.m)
        r = self.R
        expected = -self.G * self.M * self.m / r
        assert sim.gravitational_potential_energy(r) == pytest.approx(expected, rel=1e-6)

    def test_total_energy_circular_orbit(self) -> None:
        """For a circular orbit, E_total = -G M m / (2r) = -KE."""
        sim = ReferenceOrbitalBody(M=self.M, m=self.m)
        r = self.R
        v = sim.orbital_velocity(r)
        total = sim.total_energy(r, v)
        # For circular orbit: KE = GMm/(2r), GPE = -GMm/r, total = -GMm/(2r)
        expected = -self.G * self.M * self.m / (2.0 * r)
        assert total == pytest.approx(expected, rel=1e-6)

    def test_step_advances_state(self) -> None:
        """Step moves the satellite along its orbit."""
        sim = ReferenceOrbitalBody(M=self.M, m=self.m)
        initial_x = sim.state["x"]
        sim.step(10.0)
        assert sim.state["x"] != initial_x
        assert sim.state["t"] == pytest.approx(10.0)

    def test_energy_conservation_orbital_step(self) -> None:
        """Total energy is conserved (to O(dt²)) over an orbital step."""
        sim = ReferenceOrbitalBody(M=self.M, m=self.m)
        initial_energy = sim.total_energy(sim.radius, sim.speed)
        for _ in range(100):
            sim.step(10.0)
        final_energy = sim.total_energy(sim.radius, sim.speed)
        # Verlet conserves energy to O(dt²); allow ~2% drift over 100 steps
        rel_error = abs(final_energy - initial_energy) / abs(initial_energy)
        assert rel_error < 0.02, f"Energy drifted by {rel_error * 100:.3f}%"

    def test_v_orb_leo(self) -> None:
        """LEO orbital velocity ≈ 7.8 km/s."""
        sim = ReferenceOrbitalBody(M=self.M)
        r = 6.371e6 + 400e3  # 400 km altitude
        v_orb = sim.orbital_velocity(r)
        assert v_orb == pytest.approx(7800.0, rel=0.1)


# ===========================================================================
# Fluid Dynamics
# ===========================================================================


class TestFluidFlow:
    """Tests for the abstract base."""

    def test_continuity_raises(self) -> None:
        f = FluidFlow()
        with pytest.raises(NotImplementedError):
            f.continuity_velocity(0.1, 0.05, 2.0)

    def test_bernoulli_raises(self) -> None:
        f = FluidFlow()
        with pytest.raises(NotImplementedError):
            f.bernoulli_pressure(101325.0, 2.0, 4.0, 0.0, 0.0, 1000.0)

    def test_pitot_raises(self) -> None:
        f = FluidFlow()
        with pytest.raises(NotImplementedError):
            f.pitot_speed(500.0, 1000.0)


class TestReferenceFluidFlow:
    """Tests for the reference fluid flow."""

    def test_continuity_velocity(self) -> None:
        """v2 = A1 * v1 / A2."""
        f = ReferenceFluidFlow(A1=0.1, A2=0.05, v1=2.0)
        expected = 0.1 * 2.0 / 0.05  # = 4.0
        assert f.continuity_velocity(0.1, 0.05, 2.0) == pytest.approx(expected)

    def test_continuity_throat_speed_up(self) -> None:
        """Fluid speeds up in a constriction."""
        f = ReferenceFluidFlow(A1=0.1, A2=0.05, v1=2.0)
        assert f.continuity_velocity(0.1, 0.05, 2.0) > 2.0

    def test_bernoulli_pressure_drop(self) -> None:
        """Pressure drops where velocity increases (Bernoulli)."""
        f = ReferenceFluidFlow(rho=1000.0)
        P2 = f.bernoulli_pressure(101325.0, 2.0, 4.0, 0.0, 0.0, 1000.0)
        # P2 = P1 + ½ρ(v1² - v2²) = 101325 + 500*(4-16) = 101325 - 6000 = 95325
        assert P2 < 101325.0, "Pressure should drop when velocity increases"
        expected = 101325.0 + 0.5 * 1000.0 * (4.0 - 16.0)
        assert P2 == pytest.approx(expected)

    def test_bernoulli_horizontal(self) -> None:
        """Bernoulli constant is conserved for horizontal flow."""
        f = ReferenceFluidFlow(rho=1000.0)
        P1 = 101325.0
        v1 = 2.0
        v2 = 4.0
        P2 = f.bernoulli_pressure(P1, v1, v2, 0.0, 0.0, 1000.0)
        const1 = P1 + 0.5 * 1000.0 * v1 * v1
        const2 = P2 + 0.5 * 1000.0 * v2 * v2
        assert const1 == pytest.approx(const2, rel=1e-6)

    def test_pitot_speed(self) -> None:
        """v = √(2 ΔP / ρ)."""
        f = ReferenceFluidFlow()
        delta_P = 500.0  # Pa
        rho = 1000.0  # kg/m³
        expected = math.sqrt(2.0 * 500.0 / 1000.0)
        assert f.pitot_speed(delta_P, rho) == pytest.approx(expected)

    def test_pitot_air_speed(self) -> None:
        """Pitot speed from ΔP = ½ρv² -> v = √(2ΔP/ρ)."""
        f = ReferenceFluidFlow()
        # For air at sea level: ρ ≈ 1.225 kg/m³, v = 100 m/s → ΔP = ½*1.225*10000 = 6125 Pa
        delta_P = 0.5 * 1.225 * 100.0 * 100.0  # 6125 Pa
        v = f.pitot_speed(delta_P, 1.225)
        assert v == pytest.approx(100.0, rel=0.01)

    def test_step_updates_state(self) -> None:
        """Step updates v2 and P2."""
        f = ReferenceFluidFlow(A1=0.1, A2=0.05, v1=2.0)
        assert f.state["v2"] == pytest.approx(0.0)  # not yet computed
        f.step()
        assert f.state["v2"] == pytest.approx(4.0)
        assert f.state["P2"] < f.state["P1"]


# ===========================================================================
# Electromagnetic Induction
# ===========================================================================


class TestInductionCoil:
    """Tests for the abstract base."""

    def test_flux_raises(self) -> None:
        coil = InductionCoil()
        with pytest.raises(NotImplementedError):
            coil.magnetic_flux(0.5, 0.01, 0.0)

    def test_emf_raises(self) -> None:
        coil = InductionCoil()
        with pytest.raises(NotImplementedError):
            coil.induced_emf(0.01, 0.02, 0.01)

    def test_lenz_raises(self) -> None:
        coil = InductionCoil()
        with pytest.raises(NotImplementedError):
            coil.lenz_direction(0.01, 0.02)


class TestReferenceInductionCoil:
    """Tests for the reference induction coil."""

    def test_magnetic_flux(self) -> None:
        """Φ = B A cos θ."""
        coil = ReferenceInductionCoil(B=0.5, A=0.01, theta=0.0)
        assert coil.magnetic_flux(0.5, 0.01, 0.0) == pytest.approx(0.005)

    def test_magnetic_flux_angled(self) -> None:
        """Φ = B A cos θ with θ = 60°."""
        coil = ReferenceInductionCoil()
        theta = math.radians(60.0)
        expected = 0.5 * 0.01 * math.cos(theta)
        assert coil.magnetic_flux(0.5, 0.01, theta) == pytest.approx(expected)

    def test_induced_emf(self) -> None:
        """ε = -ΔΦ / Δt."""
        coil = ReferenceInductionCoil()
        emf = coil.induced_emf(0.01, 0.02, 0.01)
        assert emf == pytest.approx(-1.0)  # -(0.02-0.01)/0.01 = -1.0

    def test_induced_emf_negative(self) -> None:
        """ε is positive when flux decreases."""
        coil = ReferenceInductionCoil()
        emf = coil.induced_emf(0.02, 0.01, 0.01)
        assert emf == pytest.approx(1.0)  # -(0.01-0.02)/0.01 = 1.0

    def test_lenz_ccw_increasing_flux(self) -> None:
        """Increasing flux → CCW current."""
        coil = ReferenceInductionCoil()
        assert coil.lenz_direction(0.01, 0.02) == "CCW"

    def test_lenz_cw_decreasing_flux(self) -> None:
        """Decreasing flux → CW current."""
        coil = ReferenceInductionCoil()
        assert coil.lenz_direction(0.02, 0.01) == "CW"

    def test_step_updates_state(self) -> None:
        """Step computes flux and emf."""
        coil = ReferenceInductionCoil(B=0.5, A=0.01, magnet_position=0.1)
        assert coil.state["flux"] == pytest.approx(0.0)  # not yet stepped
        coil.step(0.01)
        assert coil.state["flux"] != pytest.approx(0.0)
        assert coil.state["emf"] != pytest.approx(0.0)

    def test_emf_sign_flips_with_magnet_direction(self) -> None:
        """EMF flips sign as magnet passes the coil."""
        coil = ReferenceInductionCoil(B=0.5, A=0.01, magnet_position=-0.2)
        emfs = []
        for _ in range(50):
            coil.magnet_position += 0.01
            coil.step(0.01)
            emfs.append(coil.state["emf"])
        # EMF should start negative (flux increasing as magnet approaches)
        # and become positive after the magnet passes (flux decreasing)
        first_half = emfs[:20]
        second_half = emfs[30:]
        assert any(e < 0 for e in first_half), "Should have negative EMF initially"
        assert any(e > 0 for e in second_half), "Should have positive EMF after passing"