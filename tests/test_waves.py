"""Tests for physics_core.waves — WaveSim and ReferenceWaveSim."""

import math

import numpy as np
import pytest

from physics_core.waves.wave_sim import WaveSim, ReferenceWaveSim
from physics_core.waves.equations import (
    malus_law,
    ultrasound_echo_distance,
    young_slit_intensity,
)


class TestWaveSim:
    """Tests for the abstract base."""

    def test_displacement_raises_not_implemented(self) -> None:
        sim = WaveSim()
        with pytest.raises(NotImplementedError):
            sim.displacement(1.0, 0.0)

    def test_step_advances_time(self) -> None:
        sim = WaveSim()
        sim.step(0.1)
        assert sim.state["t"] == pytest.approx(0.1)

    def test_state_property(self) -> None:
        sim = WaveSim()
        s = sim.state
        assert s["t"] == pytest.approx(0.0)

    def test_state_is_copy(self) -> None:
        sim = WaveSim()
        s1 = sim.state
        s1["t"] = 99.0
        assert sim.state["t"] == pytest.approx(0.0)

    def test_energy_proportional_to_amplitude_squared(self) -> None:
        sim = WaveSim(amplitude=2.0)
        e = sim.energy()
        assert e["total"] == pytest.approx(4.0)

    def test_position_returns_x_and_y(self) -> None:
        sim = ReferenceWaveSim(L=5.0, nx=10)
        x, y = sim.position()
        assert len(x) == 10
        assert len(y) == 10
        assert x[0] == pytest.approx(0.0)
        assert x[-1] == pytest.approx(5.0)


class TestReferenceWaveSim:
    """Tests for the reference implementation."""

    def test_displacement_traveling_wave(self) -> None:
        """y(x,t) = A sin(kx - ωt) for a traveling wave."""
        A = 1.0
        lam = 2.0
        f = 1.0
        sim = ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f)
        k = 2.0 * math.pi / lam
        omega = 2.0 * math.pi * f

        # Test at several (x, t) points
        for x, t in [(0.0, 0.0), (0.5, 0.1), (1.0, 0.25), (0.0, 0.5)]:
            expected = A * math.sin(k * x - omega * t)
            assert sim.displacement(x, t) == pytest.approx(expected, abs=1e-12)

    def test_field_array_matches_analytical(self) -> None:
        """ReferenceWaveSim.field(x, t) reproduces A sin(kx - ωt) analytically."""
        A = 1.5
        lam = 3.0
        f = 0.5
        sim = ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f, L=6.0, nx=100)
        k = 2.0 * math.pi / lam
        omega = 2.0 * math.pi * f

        t = 0.3
        x_arr = sim.x
        y_num = sim.field(x_arr, t)
        y_exact = A * np.sin(k * x_arr - omega * t)

        np.testing.assert_allclose(y_num, y_exact, atol=1e-12)

    def test_superposition_standing_wave(self) -> None:
        """Superposition of two counter-propagating traveling waves yields
        a standing wave with fixed nodes."""
        A = 1.0
        lam = 4.0
        f = 1.0
        sim = ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f)
        k = 2.0 * math.pi / lam
        omega = 2.0 * math.pi * f

        # Standing wave: y = 2A sin(kx) cos(ωt)
        # Nodes occur at x where sin(kx) = 0, i.e. x = nπ/k = nλ/2
        # For λ=4, nodes at x = 0, 2, 4, ...
        node_x = 2.0  # first node after origin

        # At a node, displacement should be ~0 for all t
        for t in [0.0, 0.1, 0.25, 0.5, 0.75]:
            y = sim.standing_wave(node_x, t)
            assert abs(y) < 1e-12, (
                f"Standing wave node at x={node_x}, t={t} "
                f"has non-zero displacement {y}"
            )

        # Anti-node at x = λ/4 = 1.0 should have max displacement 2A
        antinode_x = lam / 4.0
        y_max = sim.standing_wave(antinode_x, 0.0)
        assert y_max == pytest.approx(2.0 * A, abs=1e-12), (
            f"Standing wave anti-node at x={antinode_x}, t=0 "
            f"expected {2*A}, got {y_max}"
        )

    def test_intensity_proportional_to_amplitude_squared(self) -> None:
        """Energy (intensity) ∝ A²."""
        sim1 = ReferenceWaveSim(amplitude=1.0)
        sim2 = ReferenceWaveSim(amplitude=2.0)
        sim3 = ReferenceWaveSim(amplitude=3.0)

        e1 = sim1.energy()["total"]
        e2 = sim2.energy()["total"]
        e3 = sim3.energy()["total"]

        # I ∝ A²: doubling A quadruples I
        assert e2 == pytest.approx(4.0 * e1, rel=1e-12)
        assert e3 == pytest.approx(9.0 * e1, rel=1e-12)

    def test_wave_speed_formula(self) -> None:
        """v = f λ should hold."""
        sim = ReferenceWaveSim(wavelength=2.0, frequency=3.0)
        assert sim.v == pytest.approx(6.0)

    def test_standing_wave_field(self) -> None:
        """standing_wave via superposition matches 2A sin(kx) cos(ωt)."""
        A = 1.0
        lam = 4.0
        f = 1.0
        sim = ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f)
        k = 2.0 * math.pi / lam
        omega = 2.0 * math.pi * f

        for x, t in [(0.5, 0.0), (1.0, 0.2), (1.5, 0.5)]:
            expected = 2.0 * A * math.sin(k * x) * math.cos(omega * t)
            assert sim.standing_wave(x, t) == pytest.approx(expected, abs=1e-12)


class TestMalusLaw:
    """Tests for malus_law()."""

    def test_zero_angle_full_transmission(self) -> None:
        """cos²(0) = 1 → full transmission."""
        assert malus_law(1.0, 0.0) == pytest.approx(1.0)

    def test_ninety_degrees_zero(self) -> None:
        """cos²(π/2) = 0 → zero transmission."""
        assert malus_law(1.0, math.pi / 2.0) == pytest.approx(0.0, abs=1e-15)

    def test_forty_five_degrees_half(self) -> None:
        """cos²(π/4) = 0.5."""
        assert malus_law(1.0, math.pi / 4.0) == pytest.approx(0.5)

    def test_scales_with_intensity(self) -> None:
        """Doubling I₀ doubles transmitted intensity."""
        assert malus_law(2.0, math.pi / 3.0) == pytest.approx(
            2.0 * malus_law(1.0, math.pi / 3.0)
        )

    def test_crossed_polarisers_zero(self) -> None:
        """Two crossed polarisers: first at 0°, second at 90° → I=0."""
        I1 = malus_law(1.0, 0.0)  # first polariser at 0°
        I2 = malus_law(I1, math.pi / 2.0)  # second at 90°
        assert I2 == pytest.approx(0.0, abs=1e-15)


class TestUltrasoundEcho:
    """Tests for ultrasound_echo_distance()."""

    def test_known_distance(self) -> None:
        """d = v * t / 2: speed 1540 m/s, echo 0.0013 s → 1.0 m."""
        d = ultrasound_echo_distance(1540.0, 0.0013)
        assert d == pytest.approx(1.001, abs=0.001)

    def test_zero_echo_time_zero_distance(self) -> None:
        """Zero echo time → zero distance."""
        assert ultrasound_echo_distance(1540.0, 0.0) == pytest.approx(0.0)

    def test_negative_echo_time_raises(self) -> None:
        """Negative echo time raises ValueError."""
        with pytest.raises(ValueError):
            ultrasound_echo_distance(1540.0, -0.1)

    def test_linear_with_speed(self) -> None:
        """Doubling speed doubles distance for same echo time."""
        d1 = ultrasound_echo_distance(100.0, 0.1)
        d2 = ultrasound_echo_distance(200.0, 0.1)
        assert d2 == pytest.approx(2.0 * d1)


class TestYoungSlitIntensity:
    """Tests for young_slit_intensity()."""

    def test_central_maximum(self) -> None:
        """At y=0, I = I₀ (both cos² and sinc² = 1)."""
        I = young_slit_intensity(0.0, slit_separation=0.1e-3, slit_width=0.02e-3, screen_distance=1.0, wavelength=500e-9)
        assert I == pytest.approx(1.0)

    def test_first_minimum(self) -> None:
        """First minimum of interference at y = λD/(2d)."""
        wavelength = 500e-9
        d = 0.1e-3
        D = 1.0
        y_min = wavelength * D / (2.0 * d)
        I = young_slit_intensity(y_min, slit_separation=d, slit_width=0.02e-3, screen_distance=D, wavelength=wavelength)
        assert I == pytest.approx(0.0, abs=1e-12)

    def test_negative_y_symmetric(self) -> None:
        """Intensity is symmetric: I(-y) = I(y)."""
        wavelength = 500e-9
        I_pos = young_slit_intensity(0.005, slit_separation=0.1e-3, slit_width=0.02e-3, screen_distance=1.0, wavelength=wavelength)
        I_neg = young_slit_intensity(-0.005, slit_separation=0.1e-3, slit_width=0.02e-3, screen_distance=1.0, wavelength=wavelength)
        assert I_pos == pytest.approx(I_neg)

    def test_negative_wavelength_raises(self) -> None:
        """Non-positive wavelength raises ValueError."""
        with pytest.raises(ValueError):
            young_slit_intensity(0.0, slit_separation=0.1e-3, slit_width=0.02e-3, screen_distance=1.0, wavelength=-1.0)
