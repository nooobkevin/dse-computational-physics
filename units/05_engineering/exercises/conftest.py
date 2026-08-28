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
from physics_core.engineering.orbital import OrbitSim


def _load_student_class_from_path(file_path: str, class_name: str = "StudentOpticalFibre",
                                   base_type: type | None = None) -> type:
    """Import a class from a Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location(
        f"_dynamic_{path.stem}", str(path)
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"_dynamic_{path.stem}"] = mod
    spec.loader.exec_module(mod)

    cls = getattr(mod, class_name, None)
    if cls is None:
        raise AttributeError(
            f"{path} does not define a class named {class_name}"
        )
    if base_type is not None and not issubclass(cls, base_type):
        raise TypeError(
            f"{class_name} in {path} must subclass {base_type.__name__}"
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


# ---------------------------------------------------------------------------
# Optical fibre fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def student_class(request: pytest.FixtureRequest) -> Type[OpticalFibre]:
    """Return the ``StudentOpticalFibre`` class under test."""
    override = request.config.getoption("--override-student")
    if override:
        return _load_student_class_from_path(override, "StudentOpticalFibre", OpticalFibre)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "engineering_exercise.py"
    return _load_student_class_from_path(str(exercise_path), "StudentOpticalFibre", OpticalFibre)


# ---------------------------------------------------------------------------
# Orbital exercise fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def orb_student_class(request: pytest.FixtureRequest) -> Type[OrbitSim]:
    """Return the ``StudentOrbitSim`` class under test."""
    override = request.config.getoption("--override-student")
    exercises_dir = Path(__file__).parent
    path = exercises_dir / "orbital_exercise.py"
    if override:
        path = Path(override)
    return _load_student_class_from_path(str(path), "StudentOrbitSim", OrbitSim)


@pytest.fixture(scope="session")
def orb_wrong_student_class() -> Generator[Type[OrbitSim], None, None]:
    """Return deliberately WRONG ``StudentOrbitSim``."""
    source = """\
from __future__ import annotations
import math
from physics_core.engineering.orbital import OrbitSim

class StudentOrbitSim(OrbitSim):
    def gravitational_force(self, r):
        return self.G * self.M * self.m / r  # WRONG: should be /r^2
    def orbital_velocity(self, r):
        return math.sqrt(self.G * self.M / (r * r))  # WRONG
    def escape_velocity(self, r):
        return math.sqrt(self.G * self.M / r)  # WRONG: missing sqrt(2)
    def gravitational_potential_energy(self, r):
        return -self.G * self.M * self.m / (r * r)  # WRONG
    def total_energy(self, r, v):
        return 0.5 * self.m * v * v  # WRONG: missing GPE
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_orbital_"
    ) as f:
        f.write(source)
        wrong_path = Path(f.name)
    try:
        cls = _load_student_class_from_path(str(wrong_path), "StudentOrbitSim", OrbitSim)
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Power rating exercise fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def pr_student_class(request: pytest.FixtureRequest) -> type:
    """Return the ``StudentPowerRating`` class under test."""
    override = request.config.getoption("--override-student")
    exercises_dir = Path(__file__).parent
    path = exercises_dir / "power_rating_exercise.py"
    if override:
        # Allow override for power rating exercise using filename pattern
        override_path = Path(override)
        if "power_rating" in str(override_path):
            path = override_path
    return _load_student_class_from_path(str(path), "StudentPowerRating")


@pytest.fixture(scope="session")
def pr_wrong_student_class() -> Generator[type, None, None]:
    """Return deliberately WRONG ``StudentPowerRating``."""
    source = """\
from __future__ import annotations

class StudentPowerRating:
    STANDARD_FUSE_RATINGS = [3.0, 5.0, 13.0]
    def operating_current(self, power, voltage):
        return power * voltage  # WRONG: should be power/voltage
    def fuse_rating(self, current):
        return 13.0  # WRONG: always 13A
    def energy_kwh(self, power_watts, hours):
        return power_watts * hours  # WRONG: missing /1000
    def cost(self, energy_kwh, rate_per_kwh):
        return energy_kwh / rate_per_kwh  # WRONG: should be *
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_power_"
    ) as f:
        f.write(source)
        wrong_path = Path(f.name)
    try:
        cls = _load_student_class_from_path(str(wrong_path), "StudentPowerRating")
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Self-check helpers (legacy)
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
        cls = _load_student_class_from_path(str(wrong_path), "StudentOpticalFibre", OpticalFibre)
        yield cls
    finally:
        wrong_path.unlink(missing_ok=True)