"""Pytest configuration for the wave exercise auto-grader.

Adds two custom CLI options:

``--override-student PATH``
    Import ``StudentWaveSim`` from *PATH* instead of the default
    ``wave_exercise.py``.  Used by teachers to test the grader against
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

from physics_core.waves.wave_sim import WaveSim


def _load_student_class_from_path(file_path: str) -> Type[WaveSim]:
    """Import ``StudentWaveSim`` from an arbitrary Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_student", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_student"] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, "StudentWaveSim", None)
    if cls is None:
        raise AttributeError(
            f"{path} does not define a class named StudentWaveSim"
        )
    if not issubclass(cls, WaveSim):
        raise TypeError(f"StudentWaveSim in {path} must subclass WaveSim")
    return cls


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--override-student",
        action="store",
        default=None,
        help="Path to a Python file containing StudentWaveSim (for self-checking)",
    )
    parser.addoption(
        "--selfcheck",
        action="store_true",
        default=False,
        help="Run grader against correct solution (expect pass) and wrong answer (expect fail)",
    )


@pytest.fixture(scope="session")
def student_class(request: pytest.FixtureRequest) -> Type[WaveSim]:
    """Return the ``StudentWaveSim`` class under test.

    Uses ``--override-student`` if provided; otherwise imports from the
    default ``wave_exercise`` module.
    """
    override = request.config.getoption("--override-student")
    if override:
        return _load_student_class_from_path(override)

    # Default: import from wave_exercise.py via file path
    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "wave_exercise.py"
    return _load_student_class_from_path(str(exercise_path))


# ---------------------------------------------------------------------------
# Self-check helpers (used by test_selfcheck.py or inline)
# ---------------------------------------------------------------------------

WRONG_ANSWER_SOURCE = """\
\"\"\"Deliberately wrong wave physics for grader self-test.\"\"\"
from __future__ import annotations
import math
from physics_core.waves.wave_sim import WaveSim

class StudentWaveSim(WaveSim):
    \"\"\"Wrong: uses cos instead of sin — completely different wave shape.\"\"\"
    def displacement(self, x: float, t: float) -> float:
        # WRONG: cos instead of sin — different phase behaviour
        return self.amplitude * math.cos(self.k * x - self.omega * t)
"""


@pytest.fixture(scope="session")
def wrong_student_class() -> Generator[Type[WaveSim], None, None]:
    """Return a deliberately WRONG ``StudentWaveSim`` for self-check."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_wave_"
    ) as f:
        f.write(WRONG_ANSWER_SOURCE)
        wrong_path = Path(f.name)
    try:
        cls = _load_student_class_from_path(str(wrong_path))
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)
