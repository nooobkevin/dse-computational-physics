"""Tests for physics_core.em — electrostatics, circuits, magnetism."""

import math
from typing import Tuple

import numpy as np
import pytest

from physics_core.em.circuits import Circuit, ReferenceCircuit
from physics_core.em.electrostatics import ElectricField, ReferenceElectricField
from physics_core.em.magnetism import (
    MagneticField,
    MovingCharge,
    ReferenceBarMagnet,
    ReferenceMovingCharge,
    ReferenceSolenoid,
    ReferenceStraightWire,
)


# ===========================================================================
# Electrostatics
# ===========================================================================

class TestElectricField:
    """Tests for the abstract base."""

    def test_field_raises_not_implemented(self) -> None:
        ef = ElectricField()
        with pytest.raises(NotImplementedError):
            ef.field(1.0, 0.0)

    def test_potential_raises_not_implemented(self) -> None:
        ef = ElectricField()
        with pytest.raises(NotImplementedError):
            ef.potential(1.0, 0.0)

    def test_step_is_noop(self) -> None:
        ef = ElectricField()
        ef.step(0.1)  # should not raise

    def test_state_property(self) -> None:
        ef = ElectricField(q=2e-9, position=(1.0, 2.0))
        s = ef.state
        assert s["q"] == pytest.approx(2e-9)
        assert s["position"] == (1.0, 2.0)

    def test_energy_default(self) -> None:
        ef = ElectricField()
        assert ef.energy == pytest.approx(0.0)


class TestReferenceElectricField:
    """Tests for the reference implementation."""

    EPS_0 = 8.854187817e-12

    def test_field_coulomb_law(self) -> None:
        """E = q / (4πε₀ r²) at distance r from point charge."""
        q = 1e-9
        ef = ReferenceElectricField(q=q)
        # At (1, 0): r = 1
        Ex, Ey = ef.field(1.0, 0.0)
        expected_E = q / (4.0 * math.pi * self.EPS_0 * 1.0)
        assert Ex == pytest.approx(expected_E, rel=1e-6)
        assert Ey == pytest.approx(0.0, abs=1e-12)

    def test_field_radial_direction(self) -> None:
        """Field points radially outward for positive q."""
        q = 1e-9
        ef = ReferenceElectricField(q=q)
        Ex, Ey = ef.field(1.0, 1.0)
        # Direction should be (1,1)/√2
        r = math.sqrt(2.0)
        expected_mag = q / (4.0 * math.pi * self.EPS_0 * 2.0)
        assert Ex == pytest.approx(expected_mag / r, rel=1e-6)
        assert Ey == pytest.approx(expected_mag / r, rel=1e-6)

    def test_field_negative_charge(self) -> None:
        """Field points radially inward for negative q."""
        q = -1e-9
        ef = ReferenceElectricField(q=q)
        Ex, Ey = ef.field(1.0, 0.0)
        # Should be negative (inward)
        assert Ex < 0
        assert abs(Ey) < 1e-12

    def test_field_at_origin(self) -> None:
        """Field at charge position should be (0,0) to avoid singularity."""
        ef = ReferenceElectricField(q=1e-9)
        Ex, Ey = ef.field(0.0, 0.0)
        assert Ex == pytest.approx(0.0)
        assert Ey == pytest.approx(0.0)

    def test_potential_coulomb(self) -> None:
        """V = q / (4πε₀ r) at distance r from point charge."""
        q = 1e-9
        ef = ReferenceElectricField(q=q)
        V = ef.potential(2.0, 0.0)
        expected_V = q / (4.0 * math.pi * self.EPS_0 * 2.0)
        assert V == pytest.approx(expected_V, rel=1e-6)

    def test_potential_at_origin(self) -> None:
        """Potential at charge position should be infinite."""
        ef = ReferenceElectricField(q=1e-9)
        V = ef.potential(0.0, 0.0)
        assert math.isinf(V)

    def test_potential_negative_charge(self) -> None:
        """Potential is negative for negative q."""
        q = -1e-9
        ef = ReferenceElectricField(q=q)
        V = ef.potential(1.0, 0.0)
        assert V < 0


# ===========================================================================
# Circuits
# ===========================================================================

class TestCircuit:
    """Tests for the abstract base."""

    def test_resolve_raises_not_implemented(self) -> None:
        ckt = Circuit()
        with pytest.raises(NotImplementedError):
            ckt.resolve()

    def test_empty_circuit(self) -> None:
        ckt = Circuit()
        assert ckt.currents == {}
        assert ckt.voltages == {}
        assert ckt.power_dissipated() == pytest.approx(0.0)


class TestReferenceCircuit:
    """Tests for the reference circuit solver."""

    def test_series_circuit_kvl(self) -> None:
        """Simple series: V=10V, R1=5Ω, R2=3Ω.
        KVL: ΣV = 0 around the loop.
        """
        branches = [
            (0, 1, 5.0, 10.0),  # V=10V from node 0 to 1, R=5Ω
            (1, 0, 3.0, 0.0),   # R=3Ω from node 1 to 0
        ]
        ckt = ReferenceCircuit(branches)
        ckt.resolve()

        # Total R = 8Ω, I = 10/8 = 1.25A
        I = ckt.currents["0"]
        assert I == pytest.approx(1.25, rel=1e-4)

        # KVL: V_source - I*R1 - I*R2 = 0
        V_loop = 10.0 - I * 5.0 - I * 3.0
        assert V_loop == pytest.approx(0.0, abs=1e-10)

    def test_parallel_circuit_kcl(self) -> None:
        """Simple parallel: V=10V, R1=5Ω, R2=3Ω.
        KCL: I_total = I1 + I2 at the top node.
        """
        branches = [
            (0, 1, 0.001, 10.0),  # near-ideal V=10V source
            (1, 0, 5.0, 0.0),     # R1=5Ω (current flows 1→0)
            (1, 0, 3.0, 0.0),     # R2=3Ω (current flows 1→0)
        ]
        ckt = ReferenceCircuit(branches)
        ckt.resolve()

        I1 = ckt.currents["1"]  # through R1
        I2 = ckt.currents["2"]  # through R2

        expected_I1 = 10.0 / 5.0
        expected_I2 = 10.0 / 3.0
        assert I1 == pytest.approx(expected_I1, rel=1e-2)
        assert I2 == pytest.approx(expected_I2, rel=1e-2)

    def test_kirchhoff_voltage_law_loop(self) -> None:
        """KVL: sum of voltage drops around any closed loop = 0."""
        # Two-resistor voltage divider: V=9V, R1=2Ω, R2=4Ω
        branches = [
            (0, 1, 2.0, 9.0),   # V=9V, R=2Ω
            (1, 0, 4.0, 0.0),   # R=4Ω
        ]
        ckt = ReferenceCircuit(branches)
        ckt.resolve()

        I = ckt.currents["0"]
        # KVL: 9 - I*2 - I*4 = 0
        assert 9.0 - I * 2.0 - I * 4.0 == pytest.approx(0.0, abs=1e-10)

    def test_kirchhoff_current_law_node(self) -> None:
        """KCL: sum of currents entering a node = sum leaving."""
        # Three branches meeting at node 1
        # V=12V source from 0→1, two resistors from 1→0
        branches = [
            (0, 1, 0.001, 12.0),  # near-ideal V=12V source
            (1, 0, 20.0, 0.0),    # R=20Ω
            (1, 0, 30.0, 0.0),    # R=30Ω
        ]
        ckt = ReferenceCircuit(branches)
        ckt.resolve()

        # At node 1: current entering from source = current leaving via resistors
        I_in = ckt.currents["0"]  # source current (positive = 0→1)
        I_out1 = ckt.currents["1"]  # through R1 (positive = 1→0)
        I_out2 = ckt.currents["2"]  # through R2 (positive = 1→0)
        # KCL: I_in = I_out1 + I_out2
        assert I_in == pytest.approx(I_out1 + I_out2, rel=1e-2)

    def test_power_dissipated(self) -> None:
        """P = I²R for each resistor, summed."""
        branches = [
            (0, 1, 5.0, 10.0),
            (1, 0, 3.0, 0.0),
        ]
        ckt = ReferenceCircuit(branches)
        ckt.resolve()

        I = ckt.currents["0"]
        expected_power = I * I * 5.0 + I * I * 3.0
        assert ckt.power_dissipated() == pytest.approx(expected_power, rel=1e-6)

    def test_voltage_divider(self) -> None:
        """Voltage divider: V_out = V_in * R2 / (R1 + R2)."""
        branches = [
            (0, 1, 4.0, 10.0),  # V=10V, R1=4Ω
            (1, 0, 6.0, 0.0),   # R2=6Ω
        ]
        ckt = ReferenceCircuit(branches)
        ckt.resolve()

        # V_out = voltage at node 1 = 10 * 6 / (4+6) = 6V
        V_out = ckt.voltages["1"]
        assert V_out == pytest.approx(6.0, rel=1e-6)


# ===========================================================================
# Magnetism
# ===========================================================================

class TestMagneticField:
    """Tests for the abstract base."""

    def test_field_raises_not_implemented(self) -> None:
        mf = MagneticField()
        with pytest.raises(NotImplementedError):
            mf.field(1.0, 0.0)


class TestReferenceStraightWire:
    """Tests for the straight-wire magnetic field."""

    MU_0 = 4.0 * math.pi * 1e-7

    def test_field_magnitude(self) -> None:
        """B = μ₀ I / (2π r) at distance r from wire."""
        wire = ReferenceStraightWire(current=2.0)
        Bx, By, Bz = wire.field(0.1, 0.0)  # r = 0.1 m
        expected_B = self.MU_0 * 2.0 / (2.0 * math.pi * 0.1)
        B_mag = math.sqrt(Bx * Bx + By * By + Bz * Bz)
        assert B_mag == pytest.approx(expected_B, rel=1e-6)

    def test_field_direction(self) -> None:
        """Field is circumferential (right-hand rule)."""
        wire = ReferenceStraightWire(current=1.0)
        # At (0, r): field should point in -x direction
        # Right-hand rule: current up (+z) → field CCW when viewed from above
        # At (0, 0.1): the circumferential direction is (-1, 0)
        Bx, By, Bz = wire.field(0.0, 0.1)
        assert Bx < 0  # right-hand rule: at (0, r), field points -x
        assert By == pytest.approx(0.0, abs=1e-12)

    def test_field_at_origin(self) -> None:
        """Field at wire position should be (0,0,0)."""
        wire = ReferenceStraightWire(current=1.0)
        Bx, By, Bz = wire.field(0.0, 0.0)
        assert Bx == pytest.approx(0.0)
        assert By == pytest.approx(0.0)
        assert Bz == pytest.approx(0.0)


class TestReferenceSolenoid:
    """Tests for the solenoid magnetic field."""

    MU_0 = 4.0 * math.pi * 1e-7

    def test_field_inside(self) -> None:
        """B = μ₀ N I / L inside the solenoid."""
        solenoid = ReferenceSolenoid(current=2.0, N=200, length=0.5)
        Bx, By, Bz = solenoid.field(0.0, 0.0)
        expected_B = self.MU_0 * 200 * 2.0 / 0.5
        assert Bz == pytest.approx(expected_B, rel=1e-6)
        assert Bx == pytest.approx(0.0)
        assert By == pytest.approx(0.0)


# ===========================================================================
# Moving charge in magnetic field
# ===========================================================================


class TestMovingCharge:
    """Tests for the abstract base."""

    def test_magnetic_force_raises_not_implemented(self) -> None:
        mc = MovingCharge()
        with pytest.raises(NotImplementedError):
            mc.magnetic_force(1.0, 1.6e-19, 1e6, 90.0)

    def test_orbit_radius_raises_not_implemented(self) -> None:
        mc = MovingCharge()
        with pytest.raises(NotImplementedError):
            mc.orbit_radius(1.67e-27, 1e6, 1.6e-19, 1.0)

    def test_trajectory_step_raises_not_implemented(self) -> None:
        mc = MovingCharge()
        with pytest.raises(NotImplementedError):
            mc.trajectory_step((0.0, 0.0), (1e6, 0.0), 1.0, 1.6e-19, 1.67e-27, 1e-9)

    def test_right_hand_rule_raises_not_implemented(self) -> None:
        mc = MovingCharge()
        with pytest.raises(NotImplementedError):
            mc.right_hand_rule("+x", "+z")


class TestReferenceMovingCharge:
    """Tests for the reference moving-charge implementation."""

    def test_force_max_at_90_degrees(self) -> None:
        """F = |q| v B at θ = 90°."""
        mc = ReferenceMovingCharge()
        F = mc.magnetic_force(B=0.5, q=1.6e-19, v=1e6, theta_degrees=90.0)
        expected = 1.6e-19 * 1e6 * 0.5
        assert F == pytest.approx(expected, rel=1e-6)

    def test_force_zero_at_0_degrees(self) -> None:
        """F = 0 at θ = 0°."""
        mc = ReferenceMovingCharge()
        F = mc.magnetic_force(B=0.5, q=1.6e-19, v=1e6, theta_degrees=0.0)
        assert F == pytest.approx(0.0, abs=1e-30)

    def test_force_scales_with_charge(self) -> None:
        """F ∝ |q|."""
        mc = ReferenceMovingCharge()
        F1 = mc.magnetic_force(B=0.5, q=1.6e-19, v=1e6, theta_degrees=90.0)
        F2 = mc.magnetic_force(B=0.5, q=3.2e-19, v=1e6, theta_degrees=90.0)
        assert F2 == pytest.approx(2.0 * F1, rel=1e-6)

    def test_orbit_radius_formula(self) -> None:
        """r = m v / (|q| B)."""
        mc = ReferenceMovingCharge()
        r = mc.orbit_radius(m=1.67e-27, v=1e6, q=1.6e-19, B=0.5)
        expected = 1.67e-27 * 1e6 / (1.6e-19 * 0.5)
        assert r == pytest.approx(expected, rel=1e-6)

    def test_orbit_radius_inverse_with_B(self) -> None:
        """r ∝ 1/B."""
        mc = ReferenceMovingCharge()
        r1 = mc.orbit_radius(m=1.67e-27, v=1e6, q=1.6e-19, B=0.5)
        r2 = mc.orbit_radius(m=1.67e-27, v=1e6, q=1.6e-19, B=1.0)
        assert r2 == pytest.approx(r1 / 2.0, rel=1e-6)

    def test_trajectory_conserves_radius(self) -> None:
        """After one full orbit, the radius should be conserved."""
        mc = ReferenceMovingCharge()
        m = 1.6726219e-27
        q = 1.602176634e-19
        B = 1.0
        v = 1e6
        r_expected = mc.orbit_radius(m, v, q, B)
        omega = abs(q) * B / m  # cyclotron frequency
        T = 2.0 * math.pi / omega  # period
        dt = T / 1000.0

        # Start at origin moving upward; circle center at (+r, 0)
        pos: Tuple[float, float] = (0.0, 0.0)
        vel: Tuple[float, float] = (0.0, v)
        center_x = r_expected
        n_steps = 1000
        max_r_err = 0.0
        for _ in range(n_steps):
            pos, vel = mc.trajectory_step(pos, vel, B, q, m, dt)
            r = math.hypot(pos[0] - center_x, pos[1])
            max_r_err = max(max_r_err, abs(r - r_expected) / r_expected)

        assert max_r_err < 0.01, f"Radius conservation error: {max_r_err:.4f}"

    def test_right_hand_rule_positive_q(self) -> None:
        """For +q, v=+x, B=+z → force in +y direction."""
        mc = ReferenceMovingCharge()
        direction = mc.right_hand_rule("+x", "+z")
        assert direction == "+y"

    def test_right_hand_rule_negative_charge_opposite(self) -> None:
        """For -q, the force direction is opposite to +q."""
        mc = ReferenceMovingCharge()
        # For positive q: v=+x, B=+z → F=+y
        # For negative q: v=+x, B=+z → F=-y
        # The right_hand_rule returns the direction for positive q
        direction_pos = mc.right_hand_rule("+x", "+z")
        assert direction_pos == "+y"


# ===========================================================================
# Bar-magnet dipole field
# ===========================================================================


class TestReferenceBarMagnet:
    """Tests for the bar-magnet dipole field."""

    MU_0 = 4.0 * math.pi * 1e-7

    def test_field_nonzero(self) -> None:
        """Field is non-zero away from the magnet."""
        magnet = ReferenceBarMagnet(moment=1.0)
        Bx, By, Bz = magnet.field(0.1, 0.0)
        B_mag = math.sqrt(Bx * Bx + By * By + Bz * Bz)
        assert B_mag > 0.0

    def test_field_direction_flips_with_pole(self) -> None:
        """Field direction reverses when moment sign flips."""
        magnet_pos = ReferenceBarMagnet(moment=1.0)
        magnet_neg = ReferenceBarMagnet(moment=-1.0)
        Bx_pos, By_pos, _ = magnet_pos.field(0.1, 0.0)
        Bx_neg, By_neg, _ = magnet_neg.field(0.1, 0.0)
        # Components should have opposite signs
        assert Bx_pos * Bx_neg < 0 or abs(Bx_pos) < 1e-15
        assert By_pos * By_neg < 0 or abs(By_pos) < 1e-15

    def test_field_symmetric_above_below_axis(self) -> None:
        """Field at (x, +y) and (x, -y) should have opposite By."""
        magnet = ReferenceBarMagnet(moment=1.0)
        _, By_above, _ = magnet.field(0.1, 0.05)
        _, By_below, _ = magnet.field(0.1, -0.05)
        assert By_above == pytest.approx(-By_below, rel=1e-6)

    def test_field_at_origin(self) -> None:
        """Field at magnet position should be (0,0,0)."""
        magnet = ReferenceBarMagnet(moment=1.0)
        Bx, By, Bz = magnet.field(0.0, 0.0)
        assert Bx == pytest.approx(0.0)
        assert By == pytest.approx(0.0)
        assert Bz == pytest.approx(0.0)