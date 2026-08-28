"""Auto-grader for the Engineering fill-in-the-blank exercise (M5).

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's
simulation — it does *not* read or string-match the student's formula.
A correct implementation of ``critical_angle`` and
``total_internal_reflection`` will produce the right TIR physics.
A wrong implementation will fail one or more of these checks.

Checks
------
1.  **NotImplementedError guard** — if the student hasn't filled in the hooks,
    fail immediately with a clear message.
2.  **Critical angle formula** — ``θ_c = arcsin(n₂/n₁)``.
3.  **TIR above critical** — ray above critical angle undergoes TIR.
4.  **Leak below critical** — ray below critical angle leaks out.
5.  **No TIR when n₁ ≤ n₂** — no TIR possible when core index ≤ cladding index.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/05_engineering/exercises/test_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/05_engineering/exercises/test_exercise.py -v \\
        --override-student=units/05_engineering/exercises/engineering_solution.py

    # Full self-check
    uv run pytest units/05_engineering/exercises/test_exercise.py -v \\
        --selfcheck
"""

from __future__ import annotations

import math
from typing import Type

import pytest

from physics_core.engineering.optics import OpticalFibre


# ===========================================================================
# Tests — Optical fibre
# ===========================================================================


class TestOpticalFibreExercise:
    """Auto-grader for the student optical fibre exercise."""

    def test_physics_implemented(
        self, student_class: Type[OpticalFibre]
    ) -> None:
        """Fail immediately if the student hasn't filled in the hooks."""
        sim = student_class(n1=1.50, n2=1.45)
        try:
            _ = sim.critical_angle
        except NotImplementedError:
            pytest.fail(
                "Your critical_angle property is still raising "
                "NotImplementedError.  Replace the 'raise' line with "
                "math.asin(self.n2 / self.n1)."
            )
        try:
            sim.total_internal_reflection(0.5)
        except NotImplementedError:
            pytest.fail(
                "Your total_internal_reflection() method is still raising "
                "NotImplementedError.  Replace the 'raise' line with "
                "return angle > self.critical_angle."
            )

    def test_critical_angle_formula(
        self, student_class: Type[OpticalFibre]
    ) -> None:
        """θ_c = arcsin(n₂ / n₁)."""
        sim = student_class(n1=1.50, n2=1.45)
        expected = math.asin(1.45 / 1.50)
        actual = sim.critical_angle
        rel_err = abs(actual - expected) / expected
        if rel_err > 0.01:
            pytest.fail(
                f"Your critical_angle is {actual:.6f} rad, "
                f"expected {expected:.6f} rad "
                f"(relative error {rel_err*100:.2f}%). "
                f"Use math.asin(self.n2 / self.n1)."
            )

    def test_tir_above_critical(
        self, student_class: Type[OpticalFibre]
    ) -> None:
        """Ray above critical angle undergoes TIR."""
        sim = student_class(n1=1.50, n2=1.45)
        crit = sim.critical_angle
        if not sim.total_internal_reflection(crit + 0.1):
            pytest.fail(
                f"A ray at angle {crit + 0.1:.4f} rad (above critical "
                f"angle {crit:.4f} rad) should undergo TIR, "
                f"but your method returned False."
            )

    def test_leak_below_critical(
        self, student_class: Type[OpticalFibre]
    ) -> None:
        """Ray below critical angle leaks out (not TIR)."""
        sim = student_class(n1=1.50, n2=1.45)
        crit = sim.critical_angle
        test_angle = max(0.01, crit - 0.1)
        if sim.total_internal_reflection(test_angle):
            pytest.fail(
                f"A ray at angle {test_angle:.4f} rad (below critical "
                f"angle {crit:.4f} rad) should leak out, "
                f"but your method returned True."
            )

    def test_no_tir_when_n1_le_n2(
        self, student_class: Type[OpticalFibre]
    ) -> None:
        """No TIR possible when core index <= cladding index."""
        sim = student_class(n1=1.45, n2=1.50)
        if sim.total_internal_reflection(1.5):
            pytest.fail(
                "When n1 <= n2, no TIR is possible. "
                "Your method returned True for a ray at 1.5 rad."
            )


# ===========================================================================
# Self-check
# ===========================================================================


def test_selfcheck_correct_passes(
    student_class: Type[OpticalFibre],
) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    sim = student_class(n1=1.50, n2=1.45)

    implemented = True
    try:
        _ = sim.critical_angle
    except NotImplementedError:
        implemented = False
    if not implemented:
        pytest.skip("Student class not implemented — skipping")

    expected_crit = math.asin(1.45 / 1.50)
    assert sim.critical_angle == pytest.approx(expected_crit, rel=0.01)
    assert sim.total_internal_reflection(expected_crit + 0.1) is True
    assert sim.total_internal_reflection(max(0.01, expected_crit - 0.1)) is False


def test_selfcheck_wrong_fails(
    wrong_student_class: Type[OpticalFibre],
) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong answer."""
    sim = wrong_student_class(n1=1.50, n2=1.45)
    crit = sim.critical_angle
    # Wrong answer uses angle < critical instead of angle > critical
    # So a ray above critical should return False (wrong)
    assert sim.total_internal_reflection(crit + 0.1) is False, (
        "Wrong answer unexpectedly passed TIR check"
    )


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_class: Type[OpticalFibre],
    wrong_student_class: Type[OpticalFibre],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    sim = student_class()
    a: float | None = None
    implemented = True
    try:
        a = sim.critical_angle
    except NotImplementedError:
        implemented = False
    if not implemented:
        pytest.skip("Student class not implemented — skipping")
    assert a is not None, "critical_angle should return a float"