"""Pytest configuration for the EM exercise auto-grader.

Adds two custom CLI options:

``--override-student PATH``
    Import ``StudentElectricField`` / ``StudentCircuit`` from *PATH* instead
    of the default ``em_exercise.py``.  Used by teachers to test the grader
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
from typing import Generator, Tuple, Type

import pytest

from physics_core.em.circuits import Circuit
from physics_core.em.electrostatics import ElectricField


def _load_student_classes_from_path(
    file_path: str,
) -> Tuple[Type[ElectricField], Type[Circuit]]:
    """Import ``StudentElectricField`` and ``StudentCircuit`` from a Python file."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Student file not found: {path}")
    spec = importlib.util.spec_from_file_location("_dynamic_student_em", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_dynamic_student_em"] = mod
    spec.loader.exec_module(mod)

    ef_cls = getattr(mod, "StudentElectricField", None)
    if ef_cls is None:
        raise AttributeError(f"{path} does not define a class named StudentElectricField")
    if not issubclass(ef_cls, ElectricField):
        raise TypeError(f"StudentElectricField in {path} must subclass ElectricField")

    ckt_cls = getattr(mod, "StudentCircuit", None)
    if ckt_cls is None:
        raise AttributeError(f"{path} does not define a class named StudentCircuit")
    if not issubclass(ckt_cls, Circuit):
        raise TypeError(f"StudentCircuit in {path} must subclass Circuit")

    return ef_cls, ckt_cls


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--override-student",
        action="store",
        default=None,
        help="Path to a Python file containing StudentElectricField and StudentCircuit",
    )
    parser.addoption(
        "--selfcheck",
        action="store_true",
        default=False,
        help="Run grader against correct solution (expect pass) and wrong answer (expect fail)",
    )


@pytest.fixture(scope="session")
def student_classes(
    request: pytest.FixtureRequest,
) -> Tuple[Type[ElectricField], Type[Circuit]]:
    """Return the ``StudentElectricField`` and ``StudentCircuit`` classes under test."""
    override = request.config.getoption("--override-student")
    if override:
        return _load_student_classes_from_path(override)

    exercises_dir = Path(__file__).parent
    exercise_path = exercises_dir / "em_exercise.py"
    return _load_student_classes_from_path(str(exercise_path))


# ---------------------------------------------------------------------------
# Self-check helpers
# ---------------------------------------------------------------------------

WRONG_ANSWER_SOURCE = """\
\"\"\"Deliberately wrong physics for grader self-test.\"\"\"
from __future__ import annotations
import math
import numpy as np
from physics_core.em.electrostatics import ElectricField
from physics_core.em.circuits import Circuit

class StudentElectricField(ElectricField):
    \"\"\"Wrong: uses +q/4πε₀r instead of +q/4πε₀r².\"\"\"
    def field(self, x, y):
        dx = x - self._position[0]
        dy = y - self._position[1]
        r = math.sqrt(dx*dx + dy*dy)
        if r < 1e-12:
            return (0.0, 0.0)
        E = self.q / (4 * math.pi * self.epsilon0 * r)
        return (E * dx / r, E * dy / r)
    def potential(self, x, y):
        dx = x - self._position[0]
        dy = y - self._position[1]
        r = math.sqrt(dx*dx + dy*dy)
        if r < 1e-12:
            return float('inf')
        return self.q / (4 * math.pi * self.epsilon0 * r)

class StudentCircuit(Circuit):
    \"\"\"Wrong: swaps current direction sign.\"\"\"
    def resolve(self):
        if not self.branches:
            self._currents = {}
            self._voltages = {}
            return
        max_node = max(max(frm, to) for frm, to, _, _ in self.branches)
        if max_node == 0:
            self._currents = {}
            self._voltages = {"0": 0.0}
            return
        n_nodes = max_node
        G = np.zeros((n_nodes, n_nodes), dtype=float)
        I_vec = np.zeros(n_nodes, dtype=float)
        for frm, to, res, vsrc in self.branches:
            if res <= 0:
                continue
            cond = 1.0 / res
            for n in (frm, to):
                if n > 0:
                    idx = n - 1
                    G[idx, idx] += cond
            if frm > 0 and to > 0:
                i, j = frm - 1, to - 1
                G[i, j] -= cond
                G[j, i] -= cond
            # WRONG sign
            if frm > 0:
                I_vec[frm - 1] += vsrc * cond
            if to > 0:
                I_vec[to - 1] -= vsrc * cond
        V_nodes = np.linalg.solve(G, I_vec)
        self._voltages = {"0": 0.0}
        for i in range(n_nodes):
            self._voltages[str(i + 1)] = float(V_nodes[i])
        self._currents = {}
        for i, (frm, to, res, vsrc) in enumerate(self.branches):
            v_from = self._voltages.get(str(frm), 0.0)
            v_to = self._voltages.get(str(to), 0.0)
            if res > 0:
                branch_i = (v_from - v_to + vsrc) / res
            else:
                branch_i = 0.0
            self._currents[str(i)] = branch_i
"""


@pytest.fixture(scope="session")
def wrong_student_classes() -> (
    Generator[Tuple[Type[ElectricField], Type[Circuit]], None, None]
):
    """Return deliberately WRONG ``StudentElectricField`` / ``StudentCircuit``."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="_wrong_em_"
    ) as f:
        f.write(WRONG_ANSWER_SOURCE)
        wrong_path = Path(f.name)
    try:
        classes = _load_student_classes_from_path(str(wrong_path))
        yield classes
    finally:
        wrong_path.unlink(missing_ok=True)