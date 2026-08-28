"""Pytest configuration for the quantum well exercise auto-grader.

Adds two custom CLI options:

``--override-student PATH``
    Import ``StudentQuantumWell`` from *PATH* instead of the default
    ``quantum_exercise.py``.  Used by teachers to test the grader against
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

from physics_core.quantum.wavefunctions import QuantumWell
from physics_core.quantum.bohr import BohrHydrogen


def _load_student_class_from_path(file_path: str) -> Type[QuantumWell]:
    """Import ``StudentQuantumWell`` from an arbitrary Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_student", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_student"] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, "StudentQuantumWell", None)
    if cls is None:
        raise AttributeError(
            f"{path} does not define a class named StudentQuantumWell"
        )
    if not issubclass(cls, QuantumWell):
        raise TypeError(f"StudentQuantumWell in {path} must subclass QuantumWell")
    return cls


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--override-student",
        action="store",
        default=None,
        help="Shared override: path to a student/solution file (applies to whichever exercise it defines a class for)",
    )
    parser.addoption(
        "--override-student-quantum",
        action="store",
        default=None,
        help="Override for the StudentQuantumWell exercise only",
    )
    parser.addoption(
        "--override-student-hydrogen",
        action="store",
        default=None,
        help="Override for the StudentBohrHydrogen exercise only",
    )
    parser.addoption(
        "--selfcheck",
        action="store_true",
        default=False,
        help="Run grader against correct solution (expect pass) and wrong answer (expect fail)",
    )


def _resolve_override(
    request: pytest.FixtureRequest, dedicated_option: str, class_name: str
) -> str | None:
    """Pick an override path for one exercise.

    The dedicated option wins; the shared ``--override-student`` is used as a
    fallback only when it actually defines *class_name* (each exercise has its
    own solution file, so the shared flag cannot serve both at once).
    """
    dedicated = request.config.getoption(dedicated_option)
    if dedicated:
        return dedicated
    shared = request.config.getoption("--override-student")
    if not shared:
        return None
    path = Path(shared).resolve()
    spec = importlib.util.spec_from_file_location("_probe_override", str(path))
    if spec is not None and spec.loader is not None:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if getattr(mod, class_name, None) is not None:
            return shared
    return None


@pytest.fixture(scope="session")
def student_class(request: pytest.FixtureRequest) -> Type[QuantumWell]:
    """Return the ``StudentQuantumWell`` class under test.

    Uses ``--override-student-quantum`` (or a compatible ``--override-student``)
    if provided; otherwise imports from the default ``quantum_exercise`` module.
    """
    override = _resolve_override(request, "--override-student-quantum", "StudentQuantumWell")
    if override:
        return _load_student_class_from_path(override)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "quantum_exercise.py"
    return _load_student_class_from_path(str(exercise_path))


# ---------------------------------------------------------------------------
# Self-check helpers (used by test_selfcheck.py or inline)
# ---------------------------------------------------------------------------

WRONG_ANSWER_SOURCE = """\
\"\"\"Deliberately wrong quantum well physics for grader self-test.\"\"\"
from __future__ import annotations
import math
from physics_core.quantum.wavefunctions import H, QuantumWell

class StudentQuantumWell(QuantumWell):
    \"\"\"Wrong: uses E_n = n * h² / (8 m L²) instead of n².\"\"\"
    def energy_level(self, n: int) -> float:
        # WRONG: linear in n instead of n²
        return (n * H * H) / (8.0 * self.m * self.L * self.L)
"""


@pytest.fixture(scope="session")
def wrong_student_class() -> Generator[Type[QuantumWell], None, None]:
    """Return a deliberately WRONG ``StudentQuantumWell`` for self-check."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_quantum_"
    ) as f:
        f.write(WRONG_ANSWER_SOURCE)
        wrong_path = Path(f.name)
    try:
        cls = _load_student_class_from_path(str(wrong_path))
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Bohr hydrogen exercise fixtures
# ---------------------------------------------------------------------------


def _load_hydrogen_class_from_path(file_path: str) -> type:
    """Import ``StudentBohrHydrogen`` from an arbitrary Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_hydrogen", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_hydrogen"] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, "StudentBohrHydrogen", None)
    if cls is None:
        raise AttributeError(
            f"{path} does not define a class named StudentBohrHydrogen"
        )
    if not issubclass(cls, BohrHydrogen):
        raise TypeError(
            f"StudentBohrHydrogen in {path} must subclass BohrHydrogen"
        )
    return cls


@pytest.fixture(scope="session")
def hydrogen_class(request: pytest.FixtureRequest) -> type:
    """Return the ``StudentBohrHydrogen`` class under test.

    Uses ``--override-student-hydrogen`` (or a compatible ``--override-student``)
    if provided; otherwise imports from the default ``hydrogen_exercise`` module.
    """
    override = _resolve_override(
        request, "--override-student-hydrogen", "StudentBohrHydrogen"
    )
    if override:
        return _load_hydrogen_class_from_path(override)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "hydrogen_exercise.py"
    return _load_hydrogen_class_from_path(str(exercise_path))
