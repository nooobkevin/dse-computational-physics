"""Auto-grader for the Unit 05 physics & engineering quiz.

The grader is fully self-contained: it loads the ``StudentQuiz`` class from
``quiz_exercise.py`` by default, or from any file given by the environment
variable ``DSE_QUIZ_ANSWERS``.

Usage
-----
# Grade the student's quiz (default: quiz_exercise.py) — expect 10 failures
uv run pytest units/05_engineering/exercises/test_quiz.py

# Grade against the solution (teacher self-check) — expect 10 passes
DSE_QUIZ_ANSWERS=units/05_engineering/exercises/quiz_solution.py \
    uv run pytest units/05_engineering/exercises/test_quiz.py
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
    """Auto-grader for the Unit 05 physics & engineering quiz (one test per question)."""

    # -- Numeric questions -------------------------------------------------

    def test_q1_mechanical_power(self, quiz: Any) -> None:
        """P = Fv = 30000 W."""
        assert quiz.q1_mechanical_power() == pytest.approx(30000.0, rel=1e-2)

    def test_q2_pitot_speed(self, quiz: Any) -> None:
        """v = √(2ΔP/ρ) ≈ 28.87 m/s."""
        assert quiz.q2_pitot_speed() == pytest.approx(28.87, rel=1e-2)

    def test_q3_orbital_velocity(self, quiz: Any) -> None:
        """v = √(GM/r) ≈ 8.17 × 10³ m/s."""
        assert quiz.q3_orbital_velocity() == pytest.approx(8166.4, rel=1e-2)

    def test_q4_induced_emf(self, quiz: Any) -> None:
        """ε = BLv = 0.40 V."""
        assert quiz.q4_induced_emf() == pytest.approx(0.40, rel=1e-2)

    def test_q5_appliance_current(self, quiz: Any) -> None:
        """I = P/V = 10.0 A."""
        assert quiz.q5_appliance_current() == pytest.approx(10.0, rel=1e-2)

    def test_q6_transformer_voltage(self, quiz: Any) -> None:
        """V_s = V_p × N_s / N_p = 22.0 V."""
        assert quiz.q6_transformer_voltage() == pytest.approx(22.0, rel=1e-2)

    # -- Conceptual questions ----------------------------------------------

    def test_q7_bernoulli_pressure(self, quiz: Any) -> None:
        """Higher fluid speed → lower pressure."""
        assert quiz.q7_bernoulli_pressure() == "B"

    def test_q8_orbit_speed_vs_radius(self, quiz: Any) -> None:
        """Larger orbital radius → smaller orbital speed."""
        assert quiz.q8_orbit_speed_vs_radius() == "B"

    def test_q9_lenz_law(self, quiz: Any) -> None:
        """Induced current opposes the change in flux producing it."""
        assert quiz.q9_lenz_law() == "A"

    def test_q10_step_up_transformer(self, quiz: Any) -> None:
        """A step-up transformer increases the secondary voltage."""
        assert quiz.q10_step_up_transformer() == "A"