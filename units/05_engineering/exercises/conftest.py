"""Pytest configuration for the Engineering exercise auto-grader.

Adds two custom CLI options:

``--override-student PATH``
    Import ``StudentOpticalFibre`` from *PATH* instead of the default
    ``engineering_exercise.py``.  Used by teachers to test the grader
    against the solution file or a deliberately wrong answer.

``--selfcheck``
    Run the grader against the known-correct solution (expect PASS) and
    against a deliberately wrong implementation (expect FAIL).  Exits with
    a summary of both outcomes.
"""

from __future__ import annotations

import importlib.util
import math
import sys
import tempfile
from pathlib import Path
from typing import Generator, Type

import pytest

from physics_core.engineering.optics import OpticalFibre


def _load_student_class_from_path(file_path: str) -> Type[OpticalFibre]:
    """Import ``StudentOpticalFibre`` from a Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location(
        "_dynamic_student_engineering", str(path)
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_student_engineering"] = mod
    spec.loader.exec_module(mod)

    cls = getattr(mod, "StudentOpticalFibre", None)
    if cls is None:
        raise AttributeError(
            f"{path} does not define a class named StudentOpticalFibre"
        )
    if not issubclass(cls, OpticalFibre):
        raise TypeError(
            f"StudentOpticalFibre in {path} must subclass OpticalFibre"
        )
    return cls


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--override-student",
        action="store",
        default=None,
        help="Path to a Python file containing StudentOpticalFibre",
    )
    parser.addoption(
        "--selfcheck",
        action="store_true",
        default=False,
        help="Run grader against correct solution (expect pass) and wrong answer (expect fail)",
    )


@pytest.fixture(scope="session")
def student_class(request: pytest.FixtureRequest) -> Type[OpticalFibre]:
    """Return the ``StudentOpticalFibre`` class under test."""
    override = request.config.getoption("--override-student")
    if override:
        return _load_student_class_from_path(override)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "engineering_exercise.py"
    return _load_student_class_from_path(str(exercise_path))


# ---------------------------------------------------------------------------
# Self-check helpers
# ---------------------------------------------------------------------------

WRONG_ANSWER_SOURCE = """\
\"\"\"Deliberately wrong physics for grader self-test.\"\"\"
from __future__ import annotations
import math
from physics_core.engineering.optics import OpticalFibre

class StudentOpticalFibre(OpticalFibre):
    \"\"\"Wrong: uses angle < critical instead of angle > critical.\"\"\"
    @property
    def critical_angle(self):
        if self.n1 <= self.n2:
            return math.pi / 2.0
        return math.asin(self.n2 / self.n1)

    def total_internal_reflection(self, angle):
        return angle < self.critical_angle  # WRONG: should be >
"""


@pytest.fixture(scope="session")
def wrong_student_class() -> Generator[Type[OpticalFibre], None, None]:
    """Return deliberately WRONG ``StudentOpticalFibre``."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_engineering_"
    ) as f:
        f.write(WRONG_ANSWER_SOURCE)
        wrong_path = Path(f.name)
    try:
        cls = _load_student_class_from_path(str(wrong_path))
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)