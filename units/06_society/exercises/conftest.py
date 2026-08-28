"""Pytest configuration for the Physics & Society exercise auto-grader.

Adds custom CLI options:

``--override-student PATH``
    Import ``StudentDecaySim`` from *PATH* instead of the default
    ``society_exercise.py``.  Used by teachers to test the grader against
    the solution file or a deliberately wrong answer.

``--override-student-energy PATH``
    Import ``StudentEnergySim`` from *PATH* instead of the default
    ``energy_exercise.py``.

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
from physics_core.society.energy import EnergySim


def _load_student_class_from_path(file_path: str, class_name: str, base_type: type) -> type:
    """Import a class from an arbitrary Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_student", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_student"] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, class_name, None)
    if cls is None:
        raise AttributeError(
            f"{path} does not define a class named {class_name}"
        )
    if not issubclass(cls, base_type):
        raise TypeError(f"{class_name} in {path} must subclass {base_type.__name__}")
    return cls


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--override-student",
        action="store",
        default=None,
        help="Path to a Python file containing StudentDecaySim (for self-checking)",
    )
    parser.addoption(
        "--override-student-energy",
        action="store",
        default=None,
        help="Path to a Python file containing StudentEnergySim (for self-checking)",
    )
    parser.addoption(
        "--override-student-decay-analysis",
        action="store",
        default=None,
        help="Path to a Python file containing decay analysis functions (for self-checking)",
    )
    parser.addoption(
        "--selfcheck",
        action="store_true",
        default=False,
        help="Run grader against correct solution (expect pass) and wrong answer (expect fail)",
    )


@pytest.fixture(scope="session")
def student_class(request: pytest.FixtureRequest) -> Type[DecaySim]:
    """Return the ``StudentDecaySim`` class under test."""
    override = request.config.getoption("--override-student")
    if override:
        return _load_student_class_from_path(override, "StudentDecaySim", DecaySim)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "society_exercise.py"
    return _load_student_class_from_path(str(exercise_path), "StudentDecaySim", DecaySim)


@pytest.fixture(scope="session")
def student_energy_class(request: pytest.FixtureRequest) -> Type[EnergySim]:
    """Return the ``StudentEnergySim`` class under test."""
    override = request.config.getoption("--override-student-energy")
    if override:
        return _load_student_class_from_path(override, "StudentEnergySim", EnergySim)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "energy_exercise.py"
    return _load_student_class_from_path(str(exercise_path), "StudentEnergySim", EnergySim)


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

WRONG_ENERGY_SOURCE = """\
\"\"\"Deliberately wrong energy physics for grader self-test.\"\"\"
from __future__ import annotations
import math
from typing import Tuple
from physics_core.society.energy import EnergySim

class StudentEnergySim(EnergySim):
    \"\"\"Wrong: uses dm instead of dm*c^2, linear wind scaling.\"\"\"
    def mass_energy_delta(self, dm: float, in_amu: bool = True) -> Tuple[float, float]:
        # WRONG: returns dm directly, not dm*c^2
        if in_amu:
            return (dm, dm * 1.0)
        return (dm, dm / 1.660539e-27)

    def solar_power(self, area: float, solar_constant: float | None = None, efficiency: float = 1.0) -> float:
        S = solar_constant if solar_constant is not None else self.solar_constant
        return S * area * efficiency

    def wind_power(self, r: float, wind_speed: float, air_density: float | None = None, efficiency: float = 1.0) -> float:
        rho = air_density if air_density is not None else self.air_density
        # WRONG: linear v instead of v^3
        return 0.5 * efficiency * rho * math.pi * r * r * wind_speed

    def photovoltaic_power(self, area: float, solar_constant: float | None = None, efficiency: float = 1.0) -> float:
        S = solar_constant if solar_constant is not None else self.solar_constant
        eta = efficiency if efficiency != 1.0 else 0.20
        return S * area * eta
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
        cls = _load_student_class_from_path(str(wrong_path), "StudentDecaySim", DecaySim)
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def wrong_energy_class() -> Generator[Type[EnergySim], None, None]:
    """Return a deliberately WRONG ``StudentEnergySim`` for self-check."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_energy_"
    ) as f:
        f.write(WRONG_ENERGY_SOURCE)
        wrong_path = Path(f.name)
    try:
        cls = _load_student_class_from_path(str(wrong_path), "StudentEnergySim", EnergySim)
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)