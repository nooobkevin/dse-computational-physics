"""Tests for physics_core.astrophysics — Doppler shift and Hubble's law."""

import math

import pytest

from physics_core.astrophysics.doppler import C, H0, DopplerShift, ReferenceDopplerShift
from physics_core.astrophysics.hubble import HubbleLaw


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