"""Auto-grader for the Unit 07 quantum physics quiz.

The grader is fully self-contained: it loads the ``StudentQuiz`` class from
``quiz_exercise.py`` by default, or from any file given by the environment
variable ``DSE_QUIZ_ANSWERS``.

Usage
-----
# Grade the student's quiz (default: quiz_exercise.py) — expect 10 failures
uv run pytest units/07_quantum/exercises/test_quiz.py

# Grade against the solution (teacher self-check) — expect 10 passes
DSE_QUIZ_ANSWERS=units/07_quantum/exercises/quiz_solution.py \
    uv run pytest units/07_quantum/exercises/test_quiz.py
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
    """Auto-grader for the Unit 07 quantum physics quiz (one test per
    question)."""

    # -- Numeric questions -------------------------------------------------

    def test_q1_bohr_energy_level(self, quiz: StudentQuiz) -> None:
        """E₂ = -13.6 / 2² = -3.4 eV."""
        assert quiz.q1_bohr_energy_level() == pytest.approx(-3.4, rel=1e-2)

    def test_q2_balmer_wavelength(self, quiz: StudentQuiz) -> None:
        """Hα (n=3→2): λ ≈ 656.5 nm."""
        assert quiz.q2_balmer_wavelength() == pytest.approx(656.5, rel=1e-2)

    def test_q3_photoelectric_ke_max(self, quiz: StudentQuiz) -> None:
        """K_max = hf − φ = 3.63e-19 J."""
        assert quiz.q3_photoelectric_ke_max() == pytest.approx(3.63e-19, rel=1e-2)

    def test_q4_threshold_frequency(self, quiz: StudentQuiz) -> None:
        """f₀ = φ / h ≈ 4.52e14 Hz."""
        assert quiz.q4_threshold_frequency() == pytest.approx(4.52e14, rel=1e-2)

    def test_q5_superposition_probability(self, quiz: StudentQuiz) -> None:
        """P(|0⟩) = 0.6² = 0.36."""
        assert quiz.q5_superposition_probability() == pytest.approx(0.36, rel=1e-2)

    def test_q6_de_broglie_wavelength(self, quiz: StudentQuiz) -> None:
        """λ = h / (mv) ≈ 7.28e-10 m."""
        assert quiz.q6_de_broglie_wavelength() == pytest.approx(7.28e-10, rel=1e-2)

    # -- Conceptual questions ----------------------------------------------

    def test_q7_photoelectric_frequency(self, quiz: StudentQuiz) -> None:
        """K_max depends on frequency, not intensity."""
        assert quiz.q7_photoelectric_frequency() == "B"

    def test_q8_bohr_level_spacing(self, quiz: StudentQuiz) -> None:
        """Bohr levels converge as n increases."""
        assert quiz.q8_bohr_level_spacing() == "B"

    def test_q9_superposition_measurement(self, quiz: StudentQuiz) -> None:
        """Measurement collapses the superposition."""
        assert quiz.q9_superposition_measurement() == "B"

    def test_q10_heisenberg_uncertainty(self, quiz: StudentQuiz) -> None:
        """Δx · Δp ≥ ħ/2."""
        assert quiz.q10_heisenberg_uncertainty() == "A"