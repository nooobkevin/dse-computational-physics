"""Auto-grader for the Unit 02 thermal physics quiz.

The grader is fully self-contained: it loads the ``StudentQuiz`` class from
``quiz_exercise.py`` by default, or from any file given by the environment
variable ``DSE_QUIZ_ANSWERS``.

Usage
-----
# Grade the student's quiz (default: quiz_exercise.py) — expect 10 failures
uv run pytest units/02_thermal/exercises/test_quiz.py

# Grade against the solution (teacher self-check) — expect 10 passes
DSE_QUIZ_ANSWERS=units/02_thermal/exercises/quiz_solution.py \
    uv run pytest units/02_thermal/exercises/test_quiz.py
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

    def q1_ideal_gas_pressure(self) -> float: ...

    def q2_specific_heat_energy(self) -> float: ...

    def q3_kelvin_conversion(self) -> float: ...

    def q4_average_ke(self) -> float: ...

    def q5_charles_law(self) -> float: ...

    def q6_boyles_law(self) -> float: ...

    def q7_absolute_zero(self) -> str: ...

    def q8_boyles_law_identify(self) -> str: ...

    def q9_temperature_measure(self) -> str: ...

    def q10_mb_distribution(self) -> str: ...


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
    """Auto-grader for the Unit 02 thermal physics quiz (one test per
    question)."""

    # -- Numeric questions -------------------------------------------------

    def test_q1_ideal_gas_pressure(self, quiz: StudentQuiz) -> None:
        """p = nRT/V ≈ 1.013 × 10⁵ Pa."""
        assert quiz.q1_ideal_gas_pressure() == pytest.approx(1.013e5, rel=1e-2)

    def test_q2_specific_heat_energy(self, quiz: StudentQuiz) -> None:
        """Q = mcΔT = 84000 J."""
        assert quiz.q2_specific_heat_energy() == pytest.approx(84000.0, rel=1e-2)

    def test_q3_kelvin_conversion(self, quiz: StudentQuiz) -> None:
        """T = 25 + 273.15 = 298.15 K."""
        assert quiz.q3_kelvin_conversion() == pytest.approx(298.15, rel=1e-2)

    def test_q4_average_ke(self, quiz: StudentQuiz) -> None:
        """KE_avg = (3/2)kT = 6.21 × 10⁻²¹ J."""
        assert quiz.q4_average_ke() == pytest.approx(6.21e-21, rel=1e-2)

    def test_q5_charles_law(self, quiz: StudentQuiz) -> None:
        """V₂ = V₁T₂/T₁ = 3.0 L."""
        assert quiz.q5_charles_law() == pytest.approx(3.0, rel=1e-2)

    def test_q6_boyles_law(self, quiz: StudentQuiz) -> None:
        """p₂ = p₁V₁/V₂ = 200 kPa."""
        assert quiz.q6_boyles_law() == pytest.approx(200.0, rel=1e-2)

    # -- Conceptual questions ----------------------------------------------

    def test_q7_absolute_zero(self, quiz: StudentQuiz) -> None:
        """Absolute zero is -273.15 °C."""
        assert quiz.q7_absolute_zero() == "B"

    def test_q8_boyles_law_identify(self, quiz: StudentQuiz) -> None:
        """P ∝ 1/V at constant T is Boyle's law."""
        assert quiz.q8_boyles_law_identify() == "B"

    def test_q9_temperature_measure(self, quiz: StudentQuiz) -> None:
        """Temperature measures average molecular kinetic energy."""
        assert quiz.q9_temperature_measure() == "A"

    def test_q10_mb_distribution(self, quiz: StudentQuiz) -> None:
        """Higher T broadens the MB distribution, peak shifts up."""
        assert quiz.q10_mb_distribution() == "B"