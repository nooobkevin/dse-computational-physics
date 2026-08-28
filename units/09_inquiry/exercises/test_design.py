"""Auto-grader for the engineering design exercise.

Usage
-----
    # Grade the student's exercise
    uv run pytest units/09_inquiry/exercises/test_design.py -v

    # Grade against the solution file
    uv run pytest units/09_inquiry/exercises/test_design.py -v \
        --override-design-student=units/09_inquiry/exercises/design_solution.py
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Callable

import numpy as np
import pytest

from physics_core.inquiry.analysis import ReferenceLinearFit


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _import_design_module(file_path: str):
    """Import the design_exercise module from an arbitrary Python file."""
    import importlib.util
    import sys
    from pathlib import Path

    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Design module not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_design", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_design"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def design_fns(request):
    override = request.config.getoption("--override-design-student", default=None)
    if override:
        mod = _import_design_module(override)
    else:
        exercises_dir = Path(__file__).parent
        exercise_path = exercises_dir / "design_exercise.py"
        mod = _import_design_module(str(exercise_path))
    return mod


@pytest.fixture(scope="session")
def student_fit_slope(design_fns) -> Callable:
    return design_fns.fit_slope


@pytest.fixture(scope="session")
def student_recommended_length(design_fns) -> Callable:
    return design_fns.recommended_length


@pytest.fixture(scope="session")
def student_iteration_error(design_fns) -> Callable:
    return design_fns.iteration_error


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestDesignExercise:
    """Auto-grader for the engineering design exercise."""

    def test_fit_slope_not_implemented(self, student_fit_slope) -> None:
        """Fail immediately if NotImplementedError is still raised."""
        try:
            student_fit_slope(np.array([1.0, 2.0, 3.0]), np.array([1.0, 2.0, 3.0]))
        except NotImplementedError:
            pytest.fail(
                "fit_slope() is still raising NotImplementedError.  "
                "Replace it with a call to ReferenceLinearFit."
            )

    def test_fit_slope_correct(self, student_fit_slope) -> None:
        """Fit known data: T² = 4 × L."""
        L = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
        T2 = 4.0 * L  # slope = 4
        slope = student_fit_slope(T2, L)
        assert slope == pytest.approx(4.0, abs=1e-6), (
            f"fit_slope returned {slope:.6f}, expected 4.0"
        )

    def test_recommended_length_not_implemented(
        self, student_recommended_length
    ) -> None:
        try:
            student_recommended_length(4.0, 2.0)
        except NotImplementedError:
            pytest.fail(
                "recommended_length() is still raising NotImplementedError."
            )

    def test_recommended_length_correct(
        self, student_recommended_length
    ) -> None:
        """L = T² / slope.  For slope=4, T=2 → L=1.0."""
        L = student_recommended_length(4.0, 2.0)
        assert L == pytest.approx(1.0, abs=1e-6), (
            f"recommended_length returned {L:.6f}, expected 1.0"
        )

    def test_iteration_error_not_implemented(
        self, student_iteration_error
    ) -> None:
        try:
            student_iteration_error(1.0, 2.0, 2.1)
        except NotImplementedError:
            pytest.fail(
                "iteration_error() is still raising NotImplementedError."
            )

    def test_iteration_error_correct(
        self, student_iteration_error
    ) -> None:
        """|2.1 - 2.0| / 2.0 * 100 = 5%"""
        err = student_iteration_error(1.0, 2.0, 2.1)
        assert err == pytest.approx(5.0, abs=1e-6), (
            f"iteration_error returned {err:.6f}, expected 5.0"
        )

    def test_integration_end_to_end(
        self, student_fit_slope, student_recommended_length
    ) -> None:
        """End-to-end: fit slope, compute L, verify against known g."""
        g_true = 9.81
        L_vals = np.array([0.4, 0.6, 0.8, 1.0, 1.2])
        T2 = (4.0 * math.pi**2 / g_true) * L_vals
        slope = student_fit_slope(T2, L_vals)
        g_est = 4.0 * math.pi**2 / slope
        assert abs(g_est - g_true) / g_true < 1e-6, (
            f"End-to-end: g_est={g_est:.6f}, expected {g_true:.6f}"
        )