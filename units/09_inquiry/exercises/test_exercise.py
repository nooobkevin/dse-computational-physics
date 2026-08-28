"""Auto-grader for the inquiry fill-in-the-blank exercise.

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's analysis
— it does *not* read or string-match the student's formula.  A correct
implementation of ``model`` will produce the right slope, intercept, and
R².  A wrong implementation will fail one or more of these checks with a
specific, human-readable message.

Checks
------
1. **NotImplementedError guard** — if the student hasn't filled in the hook,
   fail immediately with a clear message.
2. **Slope recovery** — fit a known line y = 2x + 1; slope must match to
   within 1e-6.
3. **Intercept recovery** — intercept must match to within 1e-6.
4. **R²** — for noiseless data, R² must be ≈ 1 (tol 1e-10).
5. **Percent error** — estimate a physical constant from the slope and
   compute percent error vs the accepted value.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/09_inquiry/exercises/test_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/09_inquiry/exercises/test_exercise.py -v \
        --override-student=units/09_inquiry/exercises/inquiry_solution.py

    # Full self-check: verify grader passes correct answer AND catches wrong one
    uv run pytest units/09_inquiry/exercises/test_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

import math
from typing import Type

import numpy as np
import pytest

from physics_core.inquiry.analysis import (
    LinearFit,
    ReferenceLinearFit,
    percent_error,
)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestInquiryExercise:
    """Auto-grader for the student inquiry exercise."""

    # -- Test 1: NotImplementedError guard ---------------------------------

    def test_physics_implemented(self, student_class: Type[LinearFit]) -> None:
        """Fail immediately if the student hasn't filled in the hook."""
        x = np.array([0.0, 1.0, 2.0])
        y = np.array([0.0, 1.0, 2.0])
        sim = student_class(x_data=x, y_data=y)
        try:
            sim.model(0.5)
        except NotImplementedError:
            pytest.fail(
                "Your model method is still raising NotImplementedError.  "
                "Replace the 'raise' line with the correct physics:  "
                "return self._slope * x + self._intercept"
            )

    # -- Test 2: Slope recovery -------------------------------------------

    def test_recovers_known_slope(
        self, student_class: Type[LinearFit]
    ) -> None:
        """Fit a known line y = 2x + 1; slope must match to within 1e-6."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = student_class(x_data=x, y_data=y)
        try:
            slope = fit.slope()
        except NotImplementedError:
            pytest.skip("Student class not implemented — skipping slope test")
            return

        if abs(slope - 2.0) > 1e-6:
            pytest.fail(
                f"Your fit returned slope = {slope:.6f}, but the expected "
                f"slope is 2.0 (for y = 2x + 1).  Check your least-squares "
                f"formula or numpy polyfit call."
            )

    # -- Test 3: Intercept recovery ---------------------------------------

    def test_recovers_known_intercept(
        self, student_class: Type[LinearFit]
    ) -> None:
        """Fit a known line y = 2x + 1; intercept must match to within 1e-6."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = student_class(x_data=x, y_data=y)
        try:
            intercept = fit.intercept()
        except NotImplementedError:
            pytest.skip("Student class not implemented — skipping intercept test")
            return

        if abs(intercept - 1.0) > 1e-6:
            pytest.fail(
                f"Your fit returned intercept = {intercept:.6f}, but the "
                f"expected intercept is 1.0 (for y = 2x + 1).  Check your "
                f"least-squares formula."
            )

    # -- Test 4: R² check --------------------------------------------------

    def test_r_squared_perfect(
        self, student_class: Type[LinearFit]
    ) -> None:
        """R² must be ≈ 1 for noiseless data."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        fit = student_class(x_data=x, y_data=y)
        try:
            r_sq = fit.correlation_squared()
        except NotImplementedError:
            pytest.skip("Student class not implemented — skipping R² test")
            return

        if abs(r_sq - 1.0) > 1e-10:
            pytest.fail(
                f"Your fit returned R² = {r_sq:.10f}, but the expected "
                f"value is 1.0 for noiseless data.  Check your R² formula."
            )

    # -- Test 5: Percent error from physical constant ----------------------

    def test_percent_error(
        self, student_class: Type[LinearFit]
    ) -> None:
        """Estimate g from pendulum data and compute percent error."""
        # Generate synthetic pendulum data: T² = (4π²/g) * L
        g_true = 9.81
        lengths = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])
        t_sq = (4.0 * math.pi**2 / g_true) * lengths  # noiseless

        fit = student_class(x_data=lengths, y_data=t_sq)
        try:
            slope = fit.slope()
        except NotImplementedError:
            pytest.skip("Student class not implemented — skipping percent error test")
            return

        # g = 4π² / slope
        g_est = 4.0 * math.pi**2 / slope
        err = percent_error(g_est, g_true)

        if err > 1e-6:
            pytest.fail(
                f"Your fit gave g_est = {g_est:.6f} m/s² with percent error "
                f"{err:.6f}% (expected < 1e-6% for noiseless data).  "
                f"Check your slope calculation."
            )


# ---------------------------------------------------------------------------
# Self-check: run grader against known-correct and deliberately-wrong answers
# ---------------------------------------------------------------------------


def test_selfcheck_correct_passes(
    student_class: Type[LinearFit]
) -> None:
    """Self-check: the grader must PASS when given the correct solution.

    This test is only active when ``--override-student`` points to the
    solution file (or when ``--selfcheck`` is used, which sets it up).
    """
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    y = 2.0 * x + 1.0
    fit = student_class(x_data=x, y_data=y)
    try:
        a = fit.model(0.5)
    except NotImplementedError:
        pytest.skip("Student class not implemented — skipping self-check pass test")
        return

    # 1. Slope
    slope = fit.slope()
    assert abs(slope - 2.0) <= 1e-6, (
        f"Self-check FAILED: correct solution gave slope {slope:.6f}"
    )

    # 2. Intercept
    intercept = fit.intercept()
    assert abs(intercept - 1.0) <= 1e-6, (
        f"Self-check FAILED: correct solution gave intercept {intercept:.6f}"
    )

    # 3. R²
    r_sq = fit.correlation_squared()
    assert abs(r_sq - 1.0) <= 1e-10, (
        f"Self-check FAILED: correct solution gave R² {r_sq:.10f}"
    )

    # 4. Model evaluation
    assert fit.model(3.0) == pytest.approx(7.0, abs=1e-6), (
        "Self-check FAILED: correct solution gave wrong model(3.0)"
    )


def test_selfcheck_wrong_fails(wrong_student_class: Type[LinearFit]) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong
    answer (always returns slope=0, intercept=0).

    This test is only active when ``--selfcheck`` is used.
    """
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    y = 2.0 * x + 1.0
    sim = wrong_student_class(x_data=x, y_data=y)

    # The wrong answer should fail the slope test
    slope = sim.slope()
    assert slope == 0.0, "Wrong answer fixture should give slope=0"
    assert abs(slope - 2.0) > 1e-6, (
        "Self-check FAILED: wrong answer unexpectedly passed slope check"
    )

    # The wrong answer should fail the R² test
    r_sq = sim.correlation_squared()
    assert r_sq == 0.0, "Wrong answer fixture should give R²=0"
    assert abs(r_sq - 1.0) > 1e-10, (
        "Self-check FAILED: wrong answer unexpectedly passed R² check"
    )


# ---------------------------------------------------------------------------
# Self-check runner (invoked by --selfcheck CLI flag)
# ---------------------------------------------------------------------------


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_class: Type[LinearFit],
    wrong_student_class: Type[LinearFit],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    # Verify the wrong answer fixture is indeed wrong
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    y = 2.0 * x + 1.0
    sim = wrong_student_class(x_data=x, y_data=y)
    slope = sim.slope()
    assert slope == 0.0, (
        "Self-check setup error: wrong answer fixture produced "
        f"slope={slope:.4f}, expected 0.0"
    )