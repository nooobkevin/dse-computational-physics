"""Tests for physics_core.inquiry.analysis — LinearFit and ReferenceLinearFit."""

import math

import numpy as np
import pytest

from physics_core.inquiry.analysis import (
    LinearFit,
    ReferenceLinearFit,
    percent_error,
    propagate_uncertainty,
)


class TestLinearFit:
    """Tests for the abstract base."""

    def test_model_raises_not_implemented(self) -> None:
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        with pytest.raises(NotImplementedError):
            fit.model(0.5)

    def test_step_is_noop(self) -> None:
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        fit.step()  # should not raise
        fit.step(0.01)  # should not raise

    def test_state_returns_defaults(self) -> None:
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        s = fit.state
        assert s["slope"] == pytest.approx(0.0)
        assert s["intercept"] == pytest.approx(0.0)
        assert s["r_squared"] == pytest.approx(0.0)

    def test_position_raises_not_implemented(self) -> None:
        """position() calls model() internally, so it should raise."""
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        with pytest.raises(NotImplementedError):
            fit.position()

    def test_energy_returns_defaults(self) -> None:
        fit = LinearFit(x_data=np.array([0.0, 1.0]), y_data=np.array([0.0, 1.0]))
        e = fit.energy()
        assert e["r_squared"] == pytest.approx(0.0)
        assert e["residual_sum_squares"] == pytest.approx(0.0)

    def test_shape_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="same shape"):
            LinearFit(
                x_data=np.array([0.0, 1.0, 2.0]),
                y_data=np.array([0.0, 1.0]),
            )

    def test_too_few_points_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 2"):
            LinearFit(
                x_data=np.array([0.0]),
                y_data=np.array([0.0]),
            )


class TestReferenceLinearFit:
    """Tests for the reference implementation."""

    def test_recovers_known_slope_intercept(self) -> None:
        """Fit a clean synthetic line y = 2x + 1."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        assert fit.slope() == pytest.approx(2.0, abs=1e-6)
        assert fit.intercept() == pytest.approx(1.0, abs=1e-6)

    def test_r_squared_perfect(self) -> None:
        """R² should be exactly 1 for noiseless data."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        assert fit.correlation_squared() == pytest.approx(1.0, abs=1e-10)

    def test_recovers_negative_slope(self) -> None:
        """Fit a line with negative slope y = -3x + 5."""
        x = np.array([0.0, 1.0, 2.0, 3.0])
        y = -3.0 * x + 5.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        assert fit.slope() == pytest.approx(-3.0, abs=1e-6)
        assert fit.intercept() == pytest.approx(5.0, abs=1e-6)

    def test_records_residuals(self) -> None:
        """Residuals should be zero for noiseless data."""
        x = np.array([0.0, 1.0, 2.0])
        y = 1.5 * x + 0.5
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        res = fit.residuals()
        assert np.allclose(res, 0.0, atol=1e-10)

    def test_model_evaluates(self) -> None:
        """model(x) should return slope*x + intercept."""
        x = np.array([0.0, 1.0, 2.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        assert fit.model(3.0) == pytest.approx(7.0, abs=1e-6)
        assert fit.model(-1.0) == pytest.approx(-1.0, abs=1e-6)

    def test_position_returns_arrays(self) -> None:
        """position() should return (x_fit, y_fit) arrays of length 200."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        x_fit, y_fit = fit.position()
        assert len(x_fit) == 200
        assert len(y_fit) == 200
        # y_fit should be approximately 2*x_fit + 1
        assert np.allclose(y_fit, 2.0 * x_fit + 1.0, atol=1e-6)

    def test_energy_returns_goodness_of_fit(self) -> None:
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        e = fit.energy()
        assert e["r_squared"] == pytest.approx(1.0, abs=1e-10)
        assert e["residual_sum_squares"] == pytest.approx(0.0, abs=1e-10)

    def test_step_is_noop(self) -> None:
        x = np.array([0.0, 1.0, 2.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        slope_before = fit.slope()
        fit.step()
        assert fit.slope() == pytest.approx(slope_before)

    def test_state_returns_fit_params(self) -> None:
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = ReferenceLinearFit(x_data=x, y_data=y)
        s = fit.state
        assert s["slope"] == pytest.approx(2.0, abs=1e-6)
        assert s["intercept"] == pytest.approx(1.0, abs=1e-6)
        assert s["r_squared"] == pytest.approx(1.0, abs=1e-10)


class TestHelpers:
    """Tests for standalone helper functions."""

    def test_percent_error_standard(self) -> None:
        err = percent_error(estimated=9.77, accepted=9.81)
        expected = abs(9.77 - 9.81) / 9.81 * 100.0
        assert err == pytest.approx(expected)

    def test_percent_error_exact(self) -> None:
        err = percent_error(estimated=9.81, accepted=9.81)
        assert err == pytest.approx(0.0)

    def test_percent_error_zero_accepted_raises(self) -> None:
        with pytest.raises(ZeroDivisionError):
            percent_error(estimated=1.0, accepted=0.0)

    def test_propagate_uncertainty_noiseless(self) -> None:
        """With noiseless data, uncertainty should be very small."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        slope_err, intercept_err = propagate_uncertainty(
            slope=2.0, intercept=1.0, x_data=x, y_data=y
        )
        # Noiseless data → residuals are zero → s² = 0 → uncertainties are 0
        assert slope_err == pytest.approx(0.0, abs=1e-10)
        assert intercept_err == pytest.approx(0.0, abs=1e-10)

    def test_propagate_uncertainty_noisy(self) -> None:
        """With noisy data, uncertainties should be non-zero."""
        rng = np.random.default_rng(42)
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0 + rng.normal(0, 0.1, size=len(x))
        slope_err, intercept_err = propagate_uncertainty(
            slope=2.0, intercept=1.0, x_data=x, y_data=y
        )
        assert slope_err > 0.0
        assert intercept_err > 0.0

    def test_propagate_uncertainty_too_few_points(self) -> None:
        x = np.array([0.0, 1.0])
        y = np.array([0.0, 1.0])
        with pytest.raises(ValueError, match="at least 3"):
            propagate_uncertainty(slope=1.0, intercept=0.0, x_data=x, y_data=y)

    def test_propagate_uncertainty_collinear(self) -> None:
        """Identical x values should cause delta <= 0."""
        x = np.array([1.0, 1.0, 1.0])
        y = np.array([0.0, 1.0, 2.0])
        with pytest.raises(ValueError, match="non-positive"):
            propagate_uncertainty(slope=1.0, intercept=0.0, x_data=x, y_data=y)