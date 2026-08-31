"""Auto-grader for the Unit 01 mechanics quiz.

The grader is fully self-contained: it loads the ``StudentQuiz`` class from
``quiz_exercise.py`` by default, or from any file given by the environment
variable ``DSE_QUIZ_ANSWERS``.

Usage
-----
# Grade the student's quiz (default: quiz_exercise.py) — expect 10 failures
uv run pytest units/01_mechanics/exercises/test_quiz.py

# Grade against the solution (teacher self-check) — expect 10 passes
DSE_QUIZ_ANSWERS=units/01_mechanics/exercises/quiz_solution.py \
    uv run pytest units/01_mechanics/exercises/test_quiz.py
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

    def q1_suvat_distance(self) -> float: ...

    def q2_free_fall_speed(self) -> float: ...

    def q3_shm_period(self) -> float: ...

    def q4_kinetic_energy(self) -> float: ...

    def q5_momentum(self) -> float: ...

    def q6_projectile_time(self) -> float: ...

    def q7_vector_quantity(self) -> str: ...

    def q8_shm_acceleration(self) -> str: ...

    def q9_suvat_equation(self) -> str: ...

    def q10_newton_second_law(self) -> str: ...


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
    """Auto-grader for the Unit 01 mechanics quiz (one test per question)."""

    # -- Numeric questions -------------------------------------------------

    def test_q1_suvat_distance(self, quiz: StudentQuiz) -> None:
        """s = ut + ½at² = 25.0 m."""
        assert quiz.q1_suvat_distance() == pytest.approx(25.0, rel=1e-2)

    def test_q2_free_fall_speed(self, quiz: StudentQuiz) -> None:
        """v = gt = 19.62 m/s."""
        assert quiz.q2_free_fall_speed() == pytest.approx(19.62, rel=1e-2)

    def test_q3_shm_period(self, quiz: StudentQuiz) -> None:
        """T = 2π√(L/g) ≈ 2.006 s."""
        assert quiz.q3_shm_period() == pytest.approx(2.006, rel=1e-2)

    def test_q4_kinetic_energy(self, quiz: StudentQuiz) -> None:
        """KE = ½mv² = 9.0 J."""
        assert quiz.q4_kinetic_energy() == pytest.approx(9.0, rel=1e-2)

    def test_q5_momentum(self, quiz: StudentQuiz) -> None:
        """p = mv = 2.0 kg·m/s."""
        assert quiz.q5_momentum() == pytest.approx(2.0, rel=1e-2)

    def test_q6_projectile_time(self, quiz: StudentQuiz) -> None:
        """t = √(2h/g) = 2.0 s."""
        assert quiz.q6_projectile_time() == pytest.approx(2.0, rel=1e-2)

    # -- Conceptual questions ----------------------------------------------

    def test_q7_vector_quantity(self, quiz: StudentQuiz) -> None:
        """Displacement is the vector quantity."""
        assert quiz.q7_vector_quantity() == "C"

    def test_q8_shm_acceleration(self, quiz: StudentQuiz) -> None:
        """SHM acceleration is proportional to displacement."""
        assert quiz.q8_shm_acceleration() == "A"

    def test_q9_suvat_equation(self, quiz: StudentQuiz) -> None:
        """v² = u² + 2as."""
        assert quiz.q9_suvat_equation() == "C"

    def test_q10_newton_second_law(self, quiz: StudentQuiz) -> None:
        """Doubling F at constant m doubles a."""
        assert quiz.q10_newton_second_law() == "B"