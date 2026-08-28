"""Tests for physics_core.astrophysics — Doppler shift and Hubble's law."""

import math

import numpy as np
import pytest

from physics_core.astrophysics.doppler import C, H0, DopplerShift, ReferenceDopplerShift
from physics_core.astrophysics.hr_diagram import (
    HRDiagram,
    L_SUN,
    R_SUN,
    ReferenceHRDiagram,
    T_SUN,
)
from physics_core.astrophysics.hubble import HubbleLaw
from physics_core.astrophysics.relativity import (
    C as C_REL,
    ReferenceRelativityEngine,
    RelativityEngine,
)


# ===========================================================================
# DopplerShift — abstract base
# ===========================================================================


class TestDopplerShift:
    """Tests for the abstract base."""

    def test_observed_frequency_raises_not_implemented(self) -> None:
        ds = DopplerShift()
        with pytest.raises(NotImplementedError):
            ds.observed_frequency(0.0)

    def test_redshift_raises_not_implemented(self) -> None:
        ds = DopplerShift()
        with pytest.raises(NotImplementedError):
            ds.redshift(0.0)

    def test_velocity_from_z_raises_not_implemented(self) -> None:
        ds = DopplerShift()
        with pytest.raises(NotImplementedError):
            ds.velocity_from_z(0.0)

    def test_hubble_velocity_raises_not_implemented(self) -> None:
        ds = DopplerShift()
        with pytest.raises(NotImplementedError):
            ds.hubble_velocity(10.0)

    def test_step_advances_time(self) -> None:
        ds = DopplerShift(v=1000.0)
        ds.step(0.1)
        s = ds.state
        assert s["t"] == pytest.approx(0.1)
        assert s["s"] == pytest.approx(100.0)  # v * dt = 1000 * 0.1

    def test_state_property(self) -> None:
        ds = DopplerShift(f0=5e14, v=500.0)
        s = ds.state
        assert s["t"] == pytest.approx(0.0)
        assert s["v"] == pytest.approx(500.0)
        assert s["s"] == pytest.approx(0.0)

    def test_position(self) -> None:
        ds = DopplerShift(v=1000.0)
        ds.step(2.0)
        x, y = ds.position()
        assert x == pytest.approx(2000.0)
        assert y == pytest.approx(0.0)

    def test_energy_raises_if_hook_not_implemented(self) -> None:
        ds = DopplerShift()
        with pytest.raises(NotImplementedError):
            ds.energy()


# ===========================================================================
# ReferenceDopplerShift
# ===========================================================================


class TestReferenceDopplerShift:
    """Tests for the reference implementation."""

    def test_observed_frequency_at_rest(self) -> None:
        """f_obs → f0 as v → 0."""
        ds = ReferenceDopplerShift(f0=5.8e14)
        f_obs = ds.observed_frequency(0.0)
        assert f_obs == pytest.approx(5.8e14, rel=1e-12)

    def test_observed_frequency_approaching(self) -> None:
        """Blueshift: v < 0 → f_obs > f0."""
        ds = ReferenceDopplerShift(f0=5.8e14)
        f_obs = ds.observed_frequency(-1000.0)  # approaching at 1 km/s
        assert f_obs > 5.8e14

    def test_observed_frequency_receding(self) -> None:
        """Redshift: v > 0 → f_obs < f0."""
        ds = ReferenceDopplerShift(f0=5.8e14)
        f_obs = ds.observed_frequency(1000.0)  # receding at 1 km/s
        assert f_obs < 5.8e14

    def test_low_velocity_redshift_approx(self) -> None:
        """For small v, redshift z ≈ v/c within 1% tolerance."""
        ds = ReferenceDopplerShift()
        v = 1000.0  # 1 km/s, << c
        z = ds.redshift(v)
        expected_approx = v / C
        rel_err = abs(z - expected_approx) / expected_approx
        assert rel_err < 0.01, (
            f"Low-velocity redshift {z:.6e} should be ≈ v/c = {expected_approx:.6e}, "
            f"relative error {rel_err*100:.2f}%"
        )

    def test_relativistic_formula_tends_to_one_as_v_goes_to_zero(self) -> None:
        """f_obs / f0 → 1 as v → 0."""
        ds = ReferenceDopplerShift()
        for v in (1.0, 10.0, 100.0, 1000.0):
            ratio = ds.observed_frequency(v) / ds.f0
            assert ratio == pytest.approx(1.0, rel=1e-4), (
                f"f_obs/f0 should be ≈ 1 for v={v} m/s, got {ratio}"
            )

    def test_redshift_positive_for_receding(self) -> None:
        """z > 0 for receding source (v > 0)."""
        ds = ReferenceDopplerShift()
        assert ds.redshift(1000.0) > 0.0
        assert ds.redshift(1e6) > 0.0

    def test_redshift_negative_for_approaching(self) -> None:
        """z < 0 for approaching source (v < 0)."""
        ds = ReferenceDopplerShift()
        assert ds.redshift(-1000.0) < 0.0

    def test_velocity_from_z_relativistic(self) -> None:
        """Relativistic inverse: v_from_z(z) should recover v."""
        ds = ReferenceDopplerShift()
        v_original = 1e7  # 0.033c
        z = ds.redshift(v_original)
        v_recovered = ds.velocity_from_z(z)
        assert v_recovered == pytest.approx(v_original, rel=1e-6)

    def test_velocity_from_z_zero(self) -> None:
        """z = 0 → v = 0."""
        ds = ReferenceDopplerShift()
        assert ds.velocity_from_z(0.0) == pytest.approx(0.0, abs=1e-12)

    def test_hubble_velocity(self) -> None:
        """v = H0 * d."""
        ds = ReferenceDopplerShift()
        v = ds.hubble_velocity(10.0)  # 10 Mpc
        assert v == pytest.approx(H0 * 10.0, rel=1e-12)

    def test_hubble_velocity_custom_h0(self) -> None:
        """Custom H0 value."""
        ds = ReferenceDopplerShift()
        v = ds.hubble_velocity(5.0, H0=70.0)
        assert v == pytest.approx(350.0, rel=1e-12)

    def test_energy_positive(self) -> None:
        """Photon energy is positive."""
        ds = ReferenceDopplerShift(f0=5.8e14)
        e = ds.energy()
        assert e["frequency"] > 0.0
        assert e["photon_energy"] > 0.0

    def test_observed_frequency_raises_for_superluminal(self) -> None:
        """|v| >= c should raise ValueError."""
        ds = ReferenceDopplerShift()
        with pytest.raises(ValueError):
            ds.observed_frequency(C * 1.1)

    def test_redshift_raises_for_superluminal(self) -> None:
        """|v| >= c should raise ValueError."""
        ds = ReferenceDopplerShift()
        with pytest.raises(ValueError):
            ds.redshift(C * 1.1)

    def test_velocity_from_z_raises_for_less_than_minus_one(self) -> None:
        """z < -1 should raise ValueError."""
        ds = ReferenceDopplerShift()
        with pytest.raises(ValueError):
            ds.velocity_from_z(-2.0)


# ===========================================================================
# HubbleLaw
# ===========================================================================


class TestHubbleLaw:
    """Tests for Hubble's law."""

    def test_velocity_from_distance(self) -> None:
        """v = H0 * d."""
        hl = HubbleLaw(h0=67.8)
        v = hl.velocity(10.0)
        assert v == pytest.approx(678.0, rel=1e-12)

    def test_distance_from_velocity(self) -> None:
        """d = v / H0."""
        hl = HubbleLaw(h0=67.8)
        d = hl.distance(678.0)
        assert d == pytest.approx(10.0, rel=1e-12)

    def test_hubble_time_positive(self) -> None:
        """Hubble time is positive."""
        hl = HubbleLaw()
        assert hl.hubble_time > 0.0

    def test_custom_h0(self) -> None:
        """Custom H0 value."""
        hl = HubbleLaw(h0=70.0)
        assert hl.velocity(10.0) == pytest.approx(700.0, rel=1e-12)


# ===========================================================================
# RelativityEngine — abstract base
# ===========================================================================


class TestRelativityEngine:
    """Tests for the abstract base."""

    def test_lorentz_factor_raises_not_implemented(self) -> None:
        re = RelativityEngine()
        with pytest.raises(NotImplementedError):
            re.lorentz_factor(0.0)

    def test_time_dilated_raises_not_implemented(self) -> None:
        re = RelativityEngine()
        with pytest.raises(NotImplementedError):
            re.time_dilated(0.0, 1.0)

    def test_length_contracted_raises_not_implemented(self) -> None:
        re = RelativityEngine()
        with pytest.raises(NotImplementedError):
            re.length_contracted(0.0, 1.0)

    def test_lorentz_transform_raises_not_implemented(self) -> None:
        re = RelativityEngine()
        with pytest.raises(NotImplementedError):
            re.lorentz_transform(0.0, 0.0, 0.0)


# ===========================================================================
# ReferenceRelativityEngine
# ===========================================================================


class TestReferenceRelativityEngine:
    """Tests for the reference relativity implementation."""

    def test_gamma_at_rest(self) -> None:
        """γ = 1 at v = 0."""
        re = ReferenceRelativityEngine()
        assert re.lorentz_factor(0.0) == pytest.approx(1.0, rel=1e-12)

    def test_gamma_at_0_6c(self) -> None:
        """γ(0.6c) = 1.25."""
        re = ReferenceRelativityEngine()
        v = 0.6 * C_REL
        gamma = re.lorentz_factor(v)
        assert gamma == pytest.approx(1.25, rel=1e-4)

    def test_gamma_at_0_99c(self) -> None:
        """γ(0.99c) ≈ 7.09."""
        re = ReferenceRelativityEngine()
        v = 0.99 * C_REL
        gamma = re.lorentz_factor(v)
        assert gamma == pytest.approx(7.09, rel=1e-2)

    def test_gamma_increases_with_v(self) -> None:
        """γ increases monotonically with v."""
        re = ReferenceRelativityEngine()
        g1 = re.lorentz_factor(0.1 * C_REL)
        g2 = re.lorentz_factor(0.5 * C_REL)
        g3 = re.lorentz_factor(0.9 * C_REL)
        assert g1 < g2 < g3

    def test_time_dilation(self) -> None:
        """Δt = γ · Δt₀."""
        re = ReferenceRelativityEngine()
        v = 0.6 * C_REL
        t0 = 1.0
        dt = re.time_dilated(v, t0)
        assert dt == pytest.approx(1.25, rel=1e-4)

    def test_length_contraction(self) -> None:
        """l = l₀ / γ."""
        re = ReferenceRelativityEngine()
        v = 0.6 * C_REL
        l0 = 1.0
        l = re.length_contracted(v, l0)
        assert l == pytest.approx(1.0 / 1.25, rel=1e-4)

    def test_lorentz_transform_light_consistency(self) -> None:
        """A light signal at x = ct should transform to x' = ct'."""
        re = ReferenceRelativityEngine()
        v = 0.6 * C_REL
        t = 1.0
        x = C_REL * t  # light signal at x = ct
        t_prime, x_prime = re.lorentz_transform(v, t, x)
        # In any inertial frame, light speed is c: x'/t' = c
        assert abs(x_prime / t_prime - C_REL) < 1.0

    def test_lorentz_transform_invariance_of_c(self) -> None:
        """The speed of light is invariant under Lorentz transform."""
        re = ReferenceRelativityEngine()
        for v in (0.3 * C_REL, 0.6 * C_REL, 0.9 * C_REL):
            t = 2.0
            x = C_REL * t
            t_prime, x_prime = re.lorentz_transform(v, t, x)
            assert abs(x_prime / t_prime - C_REL) < 1.0

    def test_lorentz_transform_raises_for_superluminal(self) -> None:
        """|v| >= c should raise ValueError."""
        re = ReferenceRelativityEngine()
        with pytest.raises(ValueError):
            re.lorentz_factor(C_REL * 1.1)


# ===========================================================================
# HRDiagram — abstract base
# ===========================================================================


class TestHRDiagram:
    """Tests for the abstract base."""

    def test_luminosity_raises_not_implemented(self) -> None:
        hr = HRDiagram()
        with pytest.raises(NotImplementedError):
            hr.luminosity(5772.0, 6.96e8)

    def test_radius_from_luminosity_raises_not_implemented(self) -> None:
        hr = HRDiagram()
        with pytest.raises(NotImplementedError):
            hr.radius_from_luminosity(3.8e26, 5772.0)

    def test_peak_wavelength_raises_not_implemented(self) -> None:
        hr = HRDiagram()
        with pytest.raises(NotImplementedError):
            hr.peak_wavelength(5772.0)

    def test_blackbody_curve_raises_not_implemented(self) -> None:
        hr = HRDiagram()
        with pytest.raises(NotImplementedError):
            hr.blackbody_curve(5772.0, np.array([500e-9]))

    def test_classify_raises_not_implemented(self) -> None:
        hr = HRDiagram()
        with pytest.raises(NotImplementedError):
            hr.classify(3.8e26, 5772.0)


# ===========================================================================
# ReferenceHRDiagram
# ===========================================================================


class TestReferenceHRDiagram:
    """Tests for the reference H-R diagram implementation."""

    def test_sun_luminosity(self) -> None:
        """Sun: T=5772 K, R=6.96e8 m → L ≈ 3.8e26 W."""
        hr = ReferenceHRDiagram()
        L = hr.luminosity(T_SUN, R_SUN)
        assert L == pytest.approx(L_SUN, rel=0.05)

    def test_sun_radius_from_luminosity(self) -> None:
        """Recover solar radius from L and T."""
        hr = ReferenceHRDiagram()
        R = hr.radius_from_luminosity(L_SUN, T_SUN)
        assert R == pytest.approx(R_SUN, rel=0.05)

    def test_wien_peak_sun(self) -> None:
        """Sun: Wien peak ≈ 502 nm."""
        hr = ReferenceHRDiagram()
        lam = hr.peak_wavelength(T_SUN)
        assert lam * 1e9 == pytest.approx(502.0, rel=0.02)

    def test_wien_peak_hotter_shorter(self) -> None:
        """Hotter stars have shorter peak wavelengths."""
        hr = ReferenceHRDiagram()
        lam_cool = hr.peak_wavelength(3000.0)
        lam_hot = hr.peak_wavelength(10000.0)
        assert lam_hot < lam_cool

    def test_blackbody_curve_normalised(self) -> None:
        """Blackbody curve is normalised to peak = 1.0."""
        hr = ReferenceHRDiagram()
        wl = np.linspace(100e-9, 3000e-9, 500)
        curve = hr.blackbody_curve(T_SUN, wl)
        assert abs(float(np.max(curve)) - 1.0) < 1e-10

    def test_blackbody_curve_peak_at_wien(self) -> None:
        """Blackbody curve peak matches Wien's law."""
        hr = ReferenceHRDiagram()
        wl = np.linspace(100e-9, 3000e-9, 5000)
        curve = hr.blackbody_curve(T_SUN, wl)
        peak_idx = int(np.argmax(curve))
        peak_wl = wl[peak_idx]
        wien_wl = hr.peak_wavelength(T_SUN)
        assert abs(peak_wl - wien_wl) / wien_wl < 0.05

    def test_classify_sun_main_sequence(self) -> None:
        """Sun is main sequence."""
        hr = ReferenceHRDiagram()
        assert hr.classify(L_SUN, T_SUN) == "main sequence"

    def test_classify_giant(self) -> None:
        """High L, low T → giant."""
        hr = ReferenceHRDiagram()
        L_giant = 1000.0 * L_SUN
        T_giant = 3500.0
        assert hr.classify(L_giant, T_giant) == "giant"

    def test_classify_white_dwarf(self) -> None:
        """Low L, high T → white dwarf."""
        hr = ReferenceHRDiagram()
        L_wd = 0.01 * L_SUN
        T_wd = 20000.0
        assert hr.classify(L_wd, T_wd) == "white dwarf"