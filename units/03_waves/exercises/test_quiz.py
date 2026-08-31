"""Auto-grader for the Unit 03 waves quiz.

The grader is fully self-contained: it loads the ``StudentQuiz`` class from
``quiz_exercise.py`` by default, or from any file given by the environment
variable ``DSE_QUIZ_ANSWERS``.

Usage
-----
# Grade the student's quiz (default: quiz_exercise.py) — expect 10 failures
uv run pytest units/03_waves/exercises/test_quiz.py

# Grade against the solution (teacher self-check) — expect 10 passes
DSE_QUIZ_ANSWERS=units/03_waves/exercises/quiz_solution.py \
    uv run pytest units/03_waves/exercises/test_quiz.py
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Protocol, Type

import pytest


class StudentQuiz(Protocol):
    """Structural type of the dynamically loaded quiz class."""

    def q1_wave_speed(self) -> float: ...

    def q2_diffraction_grating(self) -> float: ...

    def q3_malus_law(self) -> float: ...

    def q4_ultrasound_echo(self) -> float: ...

    def q5_inverse_square(self) -> float: ...

    def q6_fringe_spacing(self) -> float: ...

    def q7_transverse_wave(self) -> str: ...

    def q8_crossed_polarisers(self) -> str: ...

    def q9_standing_wave_wavelength(self) -> str: ...

    def q10_sound_polarisation(self) -> str: ...


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
    """Auto-grader for the Unit 03 waves quiz (one test per question)."""

    # -- Numeric questions -------------------------------------------------

    def test_q1_wave_speed(self, quiz: StudentQuiz) -> None:
        """v = fλ = 340 m/s."""
        assert quiz.q1_wave_speed() == pytest.approx(340.0, rel=1e-2)

    def test_q2_diffraction_grating(self, quiz: StudentQuiz) -> None:
        """sinθ = nλ/d = 0.5 → θ = 30°."""
        assert quiz.q2_diffraction_grating() == pytest.approx(30.0, rel=1e-2)

    def test_q3_malus_law(self, quiz: StudentQuiz) -> None:
        """I = I₀ cos²θ = 25 W/m²."""
        assert quiz.q3_malus_law() == pytest.approx(25.0, rel=1e-2)

    def test_q4_ultrasound_echo(self, quiz: StudentQuiz) -> None:
        """d = vt/2 = 3.0 m."""
        assert quiz.q4_ultrasound_echo() == pytest.approx(3.0, rel=1e-2)

    def test_q5_inverse_square(self, quiz: StudentQuiz) -> None:
        """I = I₀/r² = 10 W/m²."""
        assert quiz.q5_inverse_square() == pytest.approx(10.0, rel=1e-2)

    def test_q6_fringe_spacing(self, quiz: StudentQuiz) -> None:
        """Δy = λD/d = 1.0 × 10⁻³ m."""
        assert quiz.q6_fringe_spacing() == pytest.approx(1.0e-3, rel=1e-2)

    # -- Conceptual questions ----------------------------------------------

    def test_q7_transverse_wave(self, quiz: StudentQuiz) -> None:
        """Light is the transverse wave."""
        assert quiz.q7_transverse_wave() == "B"

    def test_q8_crossed_polarisers(self, quiz: StudentQuiz) -> None:
        """Crossed polarisers transmit zero intensity."""
        assert quiz.q8_crossed_polarisers() == "C"

    def test_q9_standing_wave_wavelength(self, quiz: StudentQuiz) -> None:
        """λₙ = 2L/n for a string fixed at both ends."""
        assert quiz.q9_standing_wave_wavelength() == "A"

    def test_q10_sound_polarisation(self, quiz: StudentQuiz) -> None:
        """Sound is longitudinal, so it cannot be polarised."""
        assert quiz.q10_sound_polarisation() == "B"