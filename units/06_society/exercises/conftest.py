"""Pytest configuration for the Physics & Society exercise auto-grader.

Adds two custom CLI options:

``--override-student PATH``
    Import ``StudentDecaySim`` from *PATH* instead of the default
    ``society_exercise.py``.  Used by teachers to test the grader against
    the solution file or a deliberately wrong answer.

``--selfcheck``
    Run the grader against the known-correct solution (expect PASS) and
    against a deliberately wrong implementation (expect FAIL).  Exits with
    a summary of both outcomes.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path
from typing import Generator, Type

import pytest

from physics_core.society.decay import DecaySim


def _load_student_class_from_path(file_path: str) -> Type[DecaySim]:
    """Import ``StudentDecaySim`` from an arbitrary Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_student_society", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_student_society"] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, "StudentDecaySim", None)
    if cls is None:
        raise AttributeError(
            f"{path} does not define a class named StudentDecaySim"
        )
    if not issubclass(cls, DecaySim):
        raise TypeError(f"StudentDecaySim in {path} must subclass DecaySim")
    return cls


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--override-student",
        action="store",
        default=None,
        help="Path to a Python file containing StudentDecaySim (for self-checking)",
    )
    parser.addoption(
        "--selfcheck",
        action="store_true",
        default=False,
        help="Run grader against correct solution (expect pass) and wrong answer (expect fail)",
    )


@pytest.fixture(scope="session")
def student_class(request: pytest.FixtureRequest) -> Type[DecaySim]:
    """Return the ``StudentDecaySim`` class under test.

    Uses ``--override-student`` if provided; otherwise imports from the
    default ``society_exercise`` module.
    """
    override = request.config.getoption("--override-student")
    if override:
        return _load_student_class_from_path(override)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "society_exercise.py"
    return _load_student_class_from_path(str(exercise_path))


# ---------------------------------------------------------------------------
# Self-check helpers
# ---------------------------------------------------------------------------

WRONG_ANSWER_SOURCE = """\
\"\"\"Deliberately wrong decay physics for grader self-test.\"\"\"
from __future__ import annotations
import math
from physics_core.society.decay import DecaySim

class StudentDecaySim(DecaySim):
    \"\"\"Wrong: uses p = dt / T (wrong scaling, not exponential).\"\"\"
    def decay_probability(self, dt: float) -> float:
        # WRONG: uses linear dt/T instead of 1 - exp(-lambda*dt)
        return dt / self.T
"""


@pytest.fixture(scope="session")
def wrong_student_class() -> Generator[Type[DecaySim], None, None]:
    """Return a deliberately WRONG ``StudentDecaySim`` for self-check."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_society_"
    ) as f:
        f.write(WRONG_ANSWER_SOURCE)
        wrong_path = Path(f.name)
    try:
        cls = _load_student_class_from_path(str(wrong_path))
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)