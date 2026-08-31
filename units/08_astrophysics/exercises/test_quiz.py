"""Auto-grader for the Unit 08 astrophysics quiz.

The grader is fully self-contained: it loads the ``StudentQuiz`` class from
``quiz_exercise.py`` by default, or from any file given by the environment
variable ``DSE_QUIZ_ANSWERS``.

Usage
-----
# Grade the student's quiz (default: quiz_exercise.py) — expect 10 failures
uv run pytest units/08_astrophysics/exercises/test_quiz.py

# Grade against the solution (teacher self-check) — expect 10 passes
DSE_QUIZ_ANSWERS=units/08_astrophysics/exercises/quiz_solution.py \
    uv run pytest units/08_astrophysics/exercises/test_quiz.py
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
    """Auto-grader for the Unit 08 astrophysics quiz (one test per
    question)."""

    # -- Numeric questions -------------------------------------------------

    def test_q1_hubble_velocity(self, quiz: StudentQuiz) -> None:
        """v = H₀·d = 7000 km/s."""
        assert quiz.q1_hubble_velocity() == pytest.approx(7000.0, rel=1e-2)

    def test_q2_parallax_distance(self, quiz: StudentQuiz) -> None:
        """d = 1 / p = 10 pc."""
        assert quiz.q2_parallax_distance() == pytest.approx(10.0, rel=1e-2)

    def test_q3_wien_peak_wavelength(self, quiz: StudentQuiz) -> None:
        """λ_max = b / T ≈ 5.0e-7 m."""
        assert quiz.q3_wien_peak_wavelength() == pytest.approx(5.0e-7, rel=1e-2)

    def test_q4_time_dilation(self, quiz: StudentQuiz) -> None:
        """Δt = Δt₀·γ = 1.25 s."""
        assert quiz.q4_time_dilation() == pytest.approx(1.25, rel=1e-2)

    def test_q5_lorentz_factor(self, quiz: StudentQuiz) -> None:
        """γ = 1/√(1 − 0.64) ≈ 1.667."""
        assert quiz.q5_lorentz_factor() == pytest.approx(1.667, rel=1e-2)

    def test_q6_doppler_redshift(self, quiz: StudentQuiz) -> None:
        """z = v / c = 0.01."""
        assert quiz.q6_doppler_redshift() == pytest.approx(0.01, rel=1e-2)

    # -- Conceptual questions ----------------------------------------------

    def test_q7_hr_diagram_sun(self, quiz: StudentQuiz) -> None:
        """The Sun lies on the main sequence."""
        assert quiz.q7_hr_diagram_sun() == "B"

    def test_q8_hr_diagram_temperature(self, quiz: StudentQuiz) -> None:
        """Hottest stars are on the left of the H-R diagram."""
        assert quiz.q8_hr_diagram_temperature() == "A"

    def test_q9_parallax_units(self, quiz: StudentQuiz) -> None:
        """d = 1 / 0.5 = 2 pc."""
        assert quiz.q9_parallax_units() == "B"

    def test_q10_time_dilation_concept(self, quiz: StudentQuiz) -> None:
        """Moving clocks run slow."""
        assert quiz.q10_time_dilation_concept() == "B"