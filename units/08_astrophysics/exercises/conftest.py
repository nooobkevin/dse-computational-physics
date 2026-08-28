"""Pytest configuration for the Astrophysics exercise auto-grader.

Adds two custom CLI options:

``--override-student PATH``
    Import ``StudentDopplerShift`` from *PATH* instead of the default
    ``astrophysics_exercise.py``.  Used by teachers to test the grader
    against the solution file or a deliberately wrong answer.

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

from physics_core.astrophysics.doppler import DopplerShift


def _load_student_class_from_path(file_path: str) -> Type[DopplerShift]:
    """Import ``StudentDopplerShift`` from a Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_student_astro", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_student_astro"] = mod
    spec.loader.exec_module(mod)

    cls = getattr(mod, "StudentDopplerShift", None)
    if cls is None:
        raise AttributeError(f"{path} does not define a class named StudentDopplerShift")
    if not issubclass(cls, DopplerShift):
        raise TypeError(f"StudentDopplerShift in {path} must subclass DopplerShift")

    return cls


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--override-student",
        action="store",
        default=None,
        help="Path to a Python file containing StudentDopplerShift",
    )
    parser.addoption(
        "--selfcheck",
        action="store_true",
        default=False,
        help="Run grader against correct solution (expect pass) and wrong answer (expect fail)",
    )


@pytest.fixture(scope="session")
def student_class(request: pytest.FixtureRequest) -> Type[DopplerShift]:
    """Return the ``StudentDopplerShift`` class under test."""
    override = request.config.getoption("--override-student")
    if override:
        return _load_student_class_from_path(override)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "astrophysics_exercise.py"
    return _load_student_class_from_path(str(exercise_path))


# ---------------------------------------------------------------------------
# Self-check helpers
# ---------------------------------------------------------------------------

WRONG_ANSWER_SOURCE = """\
\"\"\"Deliberately wrong physics for grader self-test.\"\"\"
from __future__ import annotations
from physics_core.astrophysics.doppler import H0, DopplerShift

class StudentDopplerShift(DopplerShift):
    \"\"\"Wrong: uses the square of the receding formula (too big a shift).\"\"\"
    def observed_frequency(self, v):
        beta = v / self.c
        return self.f0 * (1 - beta) ** 2
    def redshift(self, v):
        return v / self.c ** 2  # wrong: divides by c^2, far too small
    def velocity_from_z(self, z):
        return self.c * z  # non-relativistic inverse (too small at large z)
    def hubble_velocity(self, distance, H0=H0):
        return H0 * distance * 2.0  # wrong: double the correct value
"""


@pytest.fixture(scope="session")
def wrong_student_class() -> Generator[Type[DopplerShift], None, None]:
    """Return a deliberately WRONG ``StudentDopplerShift``."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_astro_"
    ) as f:
        f.write(WRONG_ANSWER_SOURCE)
        wrong_path = Path(f.name)
    try:
        yield _load_student_class_from_path(str(wrong_path))
    finally:
        wrong_path.unlink(missing_ok=True)