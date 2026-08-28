"""Pytest configuration for the inquiry exercise auto-grader.

Adds two custom CLI options:

``--override-student PATH``
    Import ``StudentLinearFit`` from *PATH* instead of the default
    ``inquiry_exercise.py``.  Used by teachers to test the grader against
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

from physics_core.inquiry.analysis import LinearFit


def _load_student_class_from_path(file_path: str) -> Type[LinearFit]:
    """Import ``StudentLinearFit`` from an arbitrary Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_student", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    # Avoid polluting sys.modules permanently
    sys.modules["_dynamic_student"] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, "StudentLinearFit", None)
    if cls is None:
        raise AttributeError(
            f"{path} does not define a class named StudentLinearFit"
        )
    if not issubclass(cls, LinearFit):
        raise TypeError(f"StudentLinearFit in {path} must subclass LinearFit")
    return cls


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--override-student",
        action="store",
        default=None,
        help="Path to a Python file containing StudentLinearFit (for self-checking)",
    )
    parser.addoption(
        "--selfcheck",
        action="store_true",
        default=False,
        help="Run grader against correct solution (expect pass) and wrong answer (expect fail)",
    )


@pytest.fixture(scope="session")
def student_class(request: pytest.FixtureRequest) -> Type[LinearFit]:
    """Return the ``StudentLinearFit`` class under test.

    Uses ``--override-student`` if provided; otherwise imports from the
    default ``inquiry_exercise`` module.
    """
    override = request.config.getoption("--override-student")
    if override:
        return _load_student_class_from_path(override)

    # Default: import from inquiry_exercise via file path
    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "inquiry_exercise.py"
    return _load_student_class_from_path(str(exercise_path))


# ---------------------------------------------------------------------------
# Self-check helpers (used by test_selfcheck.py or inline)
# ---------------------------------------------------------------------------

WRONG_ANSWER_SOURCE = """\
\"\"\"Deliberately wrong linear fit for grader self-test.\"\"\"
from __future__ import annotations
import numpy as np
from physics_core.inquiry.analysis import LinearFit

class StudentLinearFit(LinearFit):
    \"\"\"Wrong: returns slope=0, intercept=0 regardless of data.\"\"\"
    def __init__(self, x_data, y_data, model_type='linear'):
        super().__init__(x_data, y_data, model_type)
        self._slope = 0.0
        self._intercept = 0.0
        self._r_squared = 0.0
        self._residuals_arr = y_data.copy()

    def model(self, x: float) -> float:
        # WRONG: always returns 0
        return 0.0
"""


@pytest.fixture(scope="session")
def wrong_student_class() -> Generator[Type[LinearFit], None, None]:
    """Return a deliberately WRONG ``StudentLinearFit`` for self-check."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_inquiry_"
    ) as f:
        f.write(WRONG_ANSWER_SOURCE)
        wrong_path = Path(f.name)
    try:
        cls = _load_student_class_from_path(str(wrong_path))
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)