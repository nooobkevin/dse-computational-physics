"""Auto-grader for the Unit 06 physics & society quiz.

The grader is fully self-contained: it loads the ``StudentQuiz`` class from
``quiz_exercise.py`` by default, or from any file given by the environment
variable ``DSE_QUIZ_ANSWERS``.

Usage
-----
# Grade the student's quiz (default: quiz_exercise.py) — expect 10 failures
uv run pytest units/06_society/exercises/test_quiz.py

# Grade against the solution (teacher self-check) — expect 10 passes
DSE_QUIZ_ANSWERS=units/06_society/exercises/quiz_solution.py \
    uv run pytest units/06_society/exercises/test_quiz.py
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Type

import pytest


def _load_student_quiz() -> Type[Any]:
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
def quiz() -> Any:
    """Instantiate the student quiz class under test."""
    return _load_student_quiz()()


class TestQuiz:
    """Auto-grader for the Unit 06 physics & society quiz (one test per question)."""

    # -- Numeric questions -------------------------------------------------

    def test_q1_half_life_remaining(self, quiz: Any) -> None:
        """N = N₀(1/2)^(t/τ) = 100 nuclei."""
        assert quiz.q1_half_life_remaining() == pytest.approx(100.0, rel=1e-2)

    def test_q2_fraction_remaining(self, quiz: Any) -> None:
        """N/N₀ = (1/2)³ = 0.125."""
        assert quiz.q2_fraction_remaining() == pytest.approx(0.125, rel=1e-2)

    def test_q3_activity(self, quiz: Any) -> None:
        """A = λN = 1.0 × 10⁵ Bq."""
        assert quiz.q3_activity() == pytest.approx(1.0e5, rel=1e-2)

    def test_q4_half_life_from_data(self, quiz: Any) -> None:
        """τ = 60 / 3 = 20 min."""
        assert quiz.q4_half_life_from_data() == pytest.approx(20.0, rel=1e-2)

    def test_q5_wind_power(self, quiz: Any) -> None:
        """P = ½ηρAv³ = 30000 W."""
        assert quiz.q5_wind_power() == pytest.approx(30000.0, rel=1e-2)

    def test_q6_solar_power(self, quiz: Any) -> None:
        """P = S·A·η = 400 W."""
        assert quiz.q6_solar_power() == pytest.approx(400.0, rel=1e-2)

    # -- Conceptual questions ----------------------------------------------

    def test_q7_most_penetrating(self, quiz: Any) -> None:
        """Gamma is the most penetrating radiation."""
        assert quiz.q7_most_penetrating() == "C"

    def test_q8_medical_imaging(self, quiz: Any) -> None:
        """Medical tracer / gamma camera uses gamma emission for imaging."""
        assert quiz.q8_medical_imaging() == "B"

    def test_q9_chain_reaction_regime(self, quiz: Any) -> None:
        """k = 1.0 → critical (self-sustaining)."""
        assert quiz.q9_chain_reaction_regime() == "B"

    def test_q10_renewable_source(self, quiz: Any) -> None:
        """Solar is the renewable energy source."""
        assert quiz.q10_renewable_source() == "C"