"""Auto-grader for the Unit 04 electricity & magnetism quiz.

The grader is fully self-contained: it loads the ``StudentQuiz`` class from
``quiz_exercise.py`` by default, or from any file given by the environment
variable ``DSE_QUIZ_ANSWERS``.

Usage
-----
# Grade the student's quiz (default: quiz_exercise.py) — expect 10 failures
uv run pytest units/04_em/exercises/test_quiz.py

# Grade against the solution (teacher self-check) — expect 10 passes
DSE_QUIZ_ANSWERS=units/04_em/exercises/quiz_solution.py \
    uv run pytest units/04_em/exercises/test_quiz.py
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
    """Auto-grader for the Unit 04 electricity & magnetism quiz (one test per question)."""

    # -- Numeric questions -------------------------------------------------

    def test_q1_wire_force(self, quiz: Any) -> None:
        """F = BIL sin90° = 0.30 N."""
        assert quiz.q1_wire_force() == pytest.approx(0.30, rel=1e-2)

    def test_q2_wire_force_angle(self, quiz: Any) -> None:
        """F = BIL sin30° = 0.15 N."""
        assert quiz.q2_wire_force_angle() == pytest.approx(0.15, rel=1e-2)

    def test_q3_solenoid_field(self, quiz: Any) -> None:
        """B = μ₀nI ≈ 2.51 × 10⁻³ T."""
        assert quiz.q3_solenoid_field() == pytest.approx(2.513e-3, rel=1e-2)

    def test_q4_ohm_law(self, quiz: Any) -> None:
        """V = IR = 6.0 V."""
        assert quiz.q4_ohm_law() == pytest.approx(6.0, rel=1e-2)

    def test_q5_kcl_total_current(self, quiz: Any) -> None:
        """I_total = I₁ + I₂ = 5.0 A."""
        assert quiz.q5_kcl_total_current() == pytest.approx(5.0, rel=1e-2)

    def test_q6_motor_torque(self, quiz: Any) -> None:
        """τ = NBIAsin90° = 0.15 N·m."""
        assert quiz.q6_motor_torque() == pytest.approx(0.15, rel=1e-2)

    # -- Conceptual questions ----------------------------------------------

    def test_q7_max_force_orientation(self, quiz: Any) -> None:
        """Force is maximum when the wire is perpendicular to B."""
        assert quiz.q7_max_force_orientation() == "B"

    def test_q8_solenoid_field_inside(self, quiz: Any) -> None:
        """Inside a long solenoid the field is uniform."""
        assert quiz.q8_solenoid_field_inside() == "A"

    def test_q9_kcl_statement(self, quiz: Any) -> None:
        """KCL: ΣI_in = ΣI_out at a junction."""
        assert quiz.q9_kcl_statement() == "A"

    def test_q10_force_direction_rule(self, quiz: Any) -> None:
        """Fleming's left-hand rule gives the force direction."""
        assert quiz.q10_force_direction_rule() == "B"