"""Pytest configuration for the gas exercise auto-grader.

Adds two custom CLI options:

``--override-student PATH``
    Import ``StudentGasSim`` from *PATH* instead of the default
    ``gas_exercise.py``.  Used by teachers to test the grader against
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

from physics_core.thermal.gas_sim import GasSim


def _load_student_class_from_path(file_path: str) -> Type[GasSim]:
    """Import ``StudentGasSim`` from an arbitrary Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_student", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_student"] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, "StudentGasSim", None)
    if cls is None:
        raise AttributeError(
            f"{path} does not define a class named StudentGasSim"
        )
    if not issubclass(cls, GasSim):
        raise TypeError(f"StudentGasSim in {path} must subclass GasSim")
    return cls


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--override-student",
        action="store",
        default=None,
        help="Path to a Python file containing StudentGasSim (for self-checking)",
    )
    parser.addoption(
        "--selfcheck",
        action="store_true",
        default=False,
        help="Run grader against correct solution (expect pass) and wrong answer (expect fail)",
    )


@pytest.fixture(scope="session")
def student_class(request: pytest.FixtureRequest) -> Type[GasSim]:
    """Return the ``StudentGasSim`` class under test.

    Uses ``--override-student`` if provided; otherwise imports from the
    default ``gas_exercise`` module.
    """
    override = request.config.getoption("--override-student")
    if override:
        return _load_student_class_from_path(override)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "gas_exercise.py"
    return _load_student_class_from_path(str(exercise_path))


# ---------------------------------------------------------------------------
# Self-check helpers
# ---------------------------------------------------------------------------

WRONG_ANSWER_SOURCE = """\
\"\"\"Deliberately wrong gas physics for grader self-test.\"\"\"
from __future__ import annotations
from typing import Tuple
import numpy as np
from physics_core.thermal.gas_sim import GasSim

class StudentGasSim(GasSim):
    \"\"\"Wrong: does NOT reflect wall velocities (passes through walls).\"\"\"
    def _collide_wall(self, positions, velocities):
        return positions, velocities
    def _collide_particle(self, positions, velocities):
        return velocities
"""


@pytest.fixture(scope="session")
def wrong_student_class() -> Generator[Type[GasSim], None, None]:
    """Return a deliberately WRONG ``StudentGasSim`` for self-check."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_gas_"
    ) as f:
        f.write(WRONG_ANSWER_SOURCE)
        wrong_path = Path(f.name)
    try:
        cls = _load_student_class_from_path(str(wrong_path))
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)