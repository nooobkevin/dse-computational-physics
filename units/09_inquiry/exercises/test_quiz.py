"""Auto-grader for the Unit 09 scientific inquiry quiz.

The grader is fully self-contained: it loads the ``StudentQuiz`` class from
``quiz_exercise.py`` by default, or from any file given by the environment
variable ``DSE_QUIZ_ANSWERS``.

Usage
-----
# Grade the student's quiz (default: quiz_exercise.py) — expect 10 failures
uv run pytest units/09_inquiry/exercises/test_quiz.py

# Grade against the solution (teacher self-check) — expect 10 passes
DSE_QUIZ_ANSWERS=units/09_inquiry/exercises/quiz_solution.py \
    uv run pytest units/09_inquiry/exercises/test_quiz.py
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Type

import pytest


def _load_student_quiz() -> Type[StudentQuiz]:
    """Import the ``StudentQuiz`` class under test.

    Uses the ``DSE_QUIZ_ANSWERS`` environment variable if set; otherwise
    imports from the default ``quiz_exercise.py`` in this directory.
    """
    default = Path(__file__).parent / "quiz_exercise.py"
    raw = os.environ.get("DSE_QUIZ_ANSWERS", str(default))
    path = Path(raw).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_quiz", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_quiz"] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, "StudentQuiz", None)
    if cls is None:
        raise AttributeError(f"{path} does not define a class named StudentQuiz")
    return cls


@pytest.fixture(scope="module")
def quiz() -> StudentQuiz:
    """Instantiate the student quiz class under test."""
    return _load_student_quiz()()


class TestQuiz:
    """Auto-grader for the Unit 09 scientific inquiry quiz (one test per
    question)."""

    # -- Numeric questions -------------------------------------------------

    def test_q1_linearisation_slope(self, quiz: StudentQuiz) -> None:
        """slope = 4π² / g ≈ 4.024 s²/m."""
        assert quiz.q1_linearisation_slope() == pytest.approx(4.024, rel=1e-2)

    def test_q2_linearisation_constant(self, quiz: StudentQuiz) -> None:
        """k = y · x² = 5.0."""
        assert quiz.q2_linearisation_constant() == pytest.approx(5.0, rel=1e-2)

    def test_q3_uncertainty_propagation(self, quiz: StudentQuiz) -> None:
        """Δz = √(0.5² + 0.5²) ≈ 0.707."""
        assert quiz.q3_uncertainty_propagation() == pytest.approx(0.707, rel=1e-2)

    def test_q4_percent_uncertainty(self, quiz: StudentQuiz) -> None:
        """(0.20 / 9.81) × 100 ≈ 2.04%."""
        assert quiz.q4_percent_uncertainty() == pytest.approx(2.04, rel=1e-2)

    def test_q5_epidemic_r0(self, quiz: StudentQuiz) -> None:
        """R₀ = β / γ = 3.0."""
        assert quiz.q5_epidemic_r0() == pytest.approx(3.0, rel=1e-2)

    def test_q6_herd_immunity_threshold(self, quiz: StudentQuiz) -> None:
        """1 − 1/R₀ = 0.75."""
        assert quiz.q6_herd_immunity_threshold() == pytest.approx(0.75, rel=1e-2)

    # -- Conceptual questions ----------------------------------------------

    def test_q7_linearisation_purpose(self, quiz: StudentQuiz) -> None:
        """Linearisation yields a straight line with constant slope."""
        assert quiz.q7_linearisation_purpose() == "B"

    def test_q8_uncertainty_reduction(self, quiz: StudentQuiz) -> None:
        """Repeated measurements averaged reduce random uncertainty."""
        assert quiz.q8_uncertainty_reduction() == "B"

    def test_q9_epidemic_threshold(self, quiz: StudentQuiz) -> None:
        """Epidemic spreads when R₀ > 1."""
        assert quiz.q9_epidemic_threshold() == "C"

    def test_q10_complex_system_property(self, quiz: StudentQuiz) -> None:
        """Emergence: global patterns from local interactions."""
        assert quiz.q10_complex_system_property() == "B"