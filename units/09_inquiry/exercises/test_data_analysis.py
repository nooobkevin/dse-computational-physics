"""Auto-grader for the data analysis exercise.

Usage
-----
    # Grade the student's exercise
    uv run pytest units/09_inquiry/exercises/test_data_analysis.py -v

    # Grade against the solution file
    uv run pytest units/09_inquiry/exercises/test_data_analysis.py -v \
        --override-data-student=units/09_inquiry/exercises/data_analysis_solution.py
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Callable

import numpy as np
import pytest

from physics_core.inquiry.analysis import ReferenceLinearFit, percent_error


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _import_data_module(file_path: str):
    import importlib.util
    import sys

    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Data analysis module not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_data", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_data"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def data_fns(request):
    override = request.config.getoption("--override-data-student", default=None)
    if override:
        mod = _import_data_module(override)
    else:
        exercises_dir = Path(__file__).parent
        exercise_path = exercises_dir / "data_analysis_exercise.py"
        mod = _import_data_module(str(exercise_path))
    return mod


@pytest.fixture
def fns(data_fns):
    return data_fns


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestDataAnalysisExercise:
    """Auto-grader for the data analysis exercise."""

    def test_to_si_not_implemented(self, data_fns) -> None:
        try:
            data_fns.to_si(np.array([100.0]))
        except NotImplementedError:
            pytest.fail("to_si() is still raising NotImplementedError.")

    def test_to_si_converts_cm_to_m(self, data_fns) -> None:
        L_m = data_fns.to_si(np.array([100.0, 50.0, 200.0]))
        assert np.allclose(L_m, [1.0, 0.5, 2.0]), (
            f"to_si returned {L_m}, expected [1.0, 0.5, 2.0]"
        )

    def test_remove_outliers_not_implemented(self, data_fns) -> None:
        try:
            data_fns.remove_outliers(
                np.array([0.5, 1.0]), np.array([1.0, 2.0])
            )
        except NotImplementedError:
            pytest.fail("remove_outliers() is still raising NotImplementedError.")

    def test_remove_outliers_identifies_correct(self, data_fns) -> None:
        """Dataset: [1.0, 1.1, 1.2, 5.0, 1.05] — 4th is outlier."""
        T = np.array([1.0, 1.1, 1.2, 5.0, 1.05])
        L = np.array([0.5, 0.6, 0.7, 0.8, 0.55])
        Lc, Tc = data_fns.remove_outliers(L, T)
        assert len(Tc) == 4, (
            f"remove_outliers returned {len(Tc)} points, expected 4"
        )
        assert 5.0 not in Tc, "Outlier value 5.0 was not removed"

    def test_fit_slope_not_implemented(self, data_fns) -> None:
        try:
            data_fns.fit_slope(
                np.array([1.0, 2.0]), np.array([0.5, 1.0])
            )
        except NotImplementedError:
            pytest.fail("fit_slope() is still raising NotImplementedError.")

    def test_fit_slope_correct(self, data_fns) -> None:
        """Known line: T² = 4 × L (g ≈ 9.87)."""
        L = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
        T = np.sqrt(4.0 * L)
        slope = data_fns.fit_slope(T, L)
        assert slope == pytest.approx(4.0, abs=1e-4), (
            f"fit_slope returned {slope:.4f}, expected ~4.0"
        )

    def test_estimate_g_not_implemented(self, data_fns) -> None:
        try:
            data_fns.estimate_g(4.0)
        except NotImplementedError:
            pytest.fail("estimate_g() is still raising NotImplementedError.")

    def test_estimate_g_correct(self, data_fns) -> None:
        g = data_fns.estimate_g(4.0)
        expected = 4.0 * math.pi**2 / 4.0
        assert g == pytest.approx(expected, abs=1e-6), (
            f"estimate_g(4.0) returned {g:.4f}, expected {expected:.4f}"
        )

    def test_percent_uncertainty_not_implemented(self, data_fns) -> None:
        try:
            data_fns.percent_uncertainty(9.5, 9.81)
        except NotImplementedError:
            pytest.fail(
                "percent_uncertainty() is still raising NotImplementedError."
            )

    def test_percent_uncertainty_correct(self, data_fns) -> None:
        err = data_fns.percent_uncertainty(9.5, 9.81)
        expected = percent_error(9.5, 9.81)
        assert err == pytest.approx(expected, abs=1e-6)

    def test_end_to_end(self, data_fns) -> None:
        """Full pipeline: SI conversion → outlier removal → fit → g estimate."""
        # Use the hard-coded dataset from the exercise
        L_cm = data_fns.L_cm
        T_s = data_fns.T_s
        L_m = data_fns.to_si(L_cm)
        Lc, Tc = data_fns.remove_outliers(L_m, T_s)
        slope = data_fns.fit_slope(Tc, Lc)
        g_est = data_fns.estimate_g(slope)
        err = data_fns.percent_uncertainty(g_est, 9.81)
        # g should be within 10% of 9.81 for this dataset
        assert err < 10.0, (
            f"End-to-end: g_est={g_est:.3f}, err={err:.2f}%"
        )


# ---------------------------------------------------------------------------
# CLI option (registered in conftest.py)
# ---------------------------------------------------------------------------