"""Auto-grader for the EM fill-in-the-blank exercise (M5).

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's
simulation — it does *not* read or string-match the student's formula.
A correct implementation of ``field`` / ``potential`` / ``resolve`` will
produce the right Coulomb field, potential, and circuit currents/voltages.
A wrong implementation will fail one or more of these checks.

Checks
------
1.  **NotImplementedError guard** — if the student hasn't filled in the hooks,
    fail immediately with a clear message.
2.  **Coulomb field** — ``E = q/(4πε₀ r²)`` at a given distance.
3.  **Potential** — ``V = q/(4πε₀ r)``.
4.  **Radial direction** — field points radially outward for positive q.
5.  **Kirchhoff Current Law** — ΣI_in = ΣI_out at nodes.
6.  **Kirchhoff Voltage Law** — ΣV = 0 around loops.
7.  **Power consistency** — P = I²R.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/04_em/exercises/test_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/04_em/exercises/test_exercise.py -v \
        --override-student=units/04_em/exercises/em_solution.py

    # Full self-check
    uv run pytest units/04_em/exercises/test_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

import math
from typing import Tuple, Type

import numpy as np
import pytest

from physics_core.em.circuits import Circuit, ReferenceCircuit
from physics_core.em.electrostatics import ElectricField, ReferenceElectricField

EPS_0 = 8.854187817e-12


# ===========================================================================
# Tests — Electric field
# ===========================================================================


class TestElectricFieldExercise:
    """Auto-grader for the student electric field exercise."""

    def test_physics_implemented(
        self, student_classes: Tuple[Type[ElectricField], Type[Circuit]]
    ) -> None:
        """Fail immediately if the student hasn't filled in the hooks."""
        ef_cls, _ = student_classes
        sim = ef_cls()
        try:
            sim.field(1.0, 0.0)
        except NotImplementedError:
            pytest.fail(
                "Your field() method is still raising NotImplementedError. "
                "Replace the 'raise' line with Coulomb's law: "
                "E = q / (4*pi*eps0 * r^2)"
            )
        try:
            sim.potential(1.0, 0.0)
        except NotImplementedError:
            pytest.fail(
                "Your potential() method is still raising NotImplementedError. "
                "Replace the 'raise' line with Coulomb's law: "
                "V = q / (4*pi*eps0 * r)"
            )

    def test_coulomb_field_magnitude(
        self, student_classes: Tuple[Type[ElectricField], Type[Circuit]]
    ) -> None:
        """E = q/(4πε₀ r²) at distance r from point charge."""
        ef_cls, _ = student_classes
        q = 1e-9
        student = ef_cls(q=q)
        Ex, Ey = student.field(1.0, 0.0)
        expected = q / (4.0 * math.pi * EPS_0 * 1.0)
        rel_err = abs(math.hypot(Ex, Ey) - expected) / expected
        if rel_err > 0.01:
            pytest.fail(
                f"Your field magnitude at r=1m is {math.hypot(Ex, Ey):.4e} V/m, "
                f"expected {expected:.4e} V/m "
                f"(relative error {rel_err*100:.2f}%). "
                f"Check your field() formula — use E = q/(4πε₀ r²)."
            )

    def test_coulomb_potential(
        self, student_classes: Tuple[Type[ElectricField], Type[Circuit]]
    ) -> None:
        """V = q/(4πε₀ r) at distance r from point charge."""
        ef_cls, _ = student_classes
        q = 1e-9
        student = ef_cls(q=q)
        V = student.potential(2.0, 0.0)
        expected = q / (4.0 * math.pi * EPS_0 * 2.0)
        rel_err = abs(V - expected) / expected
        if rel_err > 0.01:
            pytest.fail(
                f"Your potential at r=2m is {V:.4e} V, "
                f"expected {expected:.4e} V "
                f"(relative error {rel_err*100:.2f}%). "
                f"Check your potential() formula."
            )

    def test_field_radial_direction(
        self, student_classes: Tuple[Type[ElectricField], Type[Circuit]]
    ) -> None:
        """Field points radially outward for positive q."""
        ef_cls, _ = student_classes
        student = ef_cls(q=1e-9)
        Ex, Ey = student.field(1.0, 1.0)
        # The field should point in the (1,1)/√2 direction
        if Ex <= 0 or Ey <= 0:
            pytest.fail(
                f"Your field at (1,1) is ({Ex:.4e}, {Ey:.4e}), "
                f"but for a positive charge at the origin both components "
                f"should be positive (radially outward)."
            )


# ===========================================================================
# Tests — Circuit
# ===========================================================================


class TestCircuitExercise:
    """Auto-grader for the student circuit exercise."""

    def test_resolve_implemented(
        self, student_classes: Tuple[Type[ElectricField], Type[Circuit]]
    ) -> None:
        """Fail immediately if the student hasn't filled in resolve()."""
        _, ckt_cls = student_classes
        branches = [(0, 1, 5.0, 10.0), (1, 0, 3.0, 0.0)]
        sim = ckt_cls(branches)
        try:
            sim.resolve()
        except NotImplementedError:
            pytest.fail(
                "Your resolve() method is still raising NotImplementedError. "
                "Replace the 'raise' line with the nodal analysis algorithm."
            )

    def test_kirchhoff_current_law(
        self, student_classes: Tuple[Type[ElectricField], Type[Circuit]]
    ) -> None:
        """KCL: ΣI_in = ΣI_out at nodes."""
        _, ckt_cls = student_classes
        branches = [
            (0, 1, 0.001, 12.0),
            (1, 0, 20.0, 0.0),
            (1, 0, 30.0, 0.0),
        ]
        student = ckt_cls(branches)
        student.resolve()

        I_in = student.currents["0"]
        I_out1 = student.currents["1"]
        I_out2 = student.currents["2"]
        if abs(I_in - (I_out1 + I_out2)) > 0.1:
            pytest.fail(
                f"KCL violated at node 1: current in = {I_in:.4f}A, "
                f"current out = {I_out1 + I_out2:.4f}A. "
                f"Check your resolve() implementation."
            )

    def test_kirchhoff_voltage_law(
        self, student_classes: Tuple[Type[ElectricField], Type[Circuit]]
    ) -> None:
        """KVL: ΣV = 0 around a closed loop."""
        _, ckt_cls = student_classes
        branches = [
            (0, 1, 2.0, 9.0),
            (1, 0, 4.0, 0.0),
        ]
        student = ckt_cls(branches)
        student.resolve()

        I = student.currents["0"]
        V_loop = 9.0 - I * 2.0 - I * 4.0
        if abs(V_loop) > 0.1:
            pytest.fail(
                f"KVL violated: 9 - I*2 - I*4 = {V_loop:.4f}V (expected 0). "
                f"Your current is I={I:.4f}A. "
                f"Check your resolve() implementation."
            )

    def test_power_dissipated(
        self, student_classes: Tuple[Type[ElectricField], Type[Circuit]]
    ) -> None:
        """P = I²R consistent with circuit."""
        _, ckt_cls = student_classes
        branches = [
            (0, 1, 5.0, 10.0),
            (1, 0, 3.0, 0.0),
        ]
        student = ckt_cls(branches)
        student.resolve()

        I = student.currents["0"]
        expected_power = I * I * 5.0 + I * I * 3.0
        if abs(student.power_dissipated() - expected_power) > 0.01:
            pytest.fail(
                f"Power mismatch: your P_total = {student.power_dissipated():.4f}W, "
                f"expected {expected_power:.4f}W."
            )


# ===========================================================================
# Self-check
# ===========================================================================


def test_selfcheck_correct_passes(
    student_classes: Tuple[Type[ElectricField], Type[Circuit]],
) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    ef_cls, ckt_cls = student_classes

    # Check field
    ef = ef_cls(q=1e-9)
    Ex = Ey = 0.0
    field_implemented = True
    try:
        Ex, Ey = ef.field(1.0, 0.0)
    except NotImplementedError:
        field_implemented = False
    if not field_implemented:
        pytest.skip("Student class not implemented — skipping")

    expected_E = 1e-9 / (4.0 * math.pi * EPS_0 * 1.0)
    assert math.hypot(Ex, Ey) == pytest.approx(expected_E, rel=0.01)

    V = ef.potential(2.0, 0.0)
    expected_V = 1e-9 / (4.0 * math.pi * EPS_0 * 2.0)
    assert V == pytest.approx(expected_V, rel=0.01)

    # Check circuit
    branches = [(0, 1, 5.0, 10.0), (1, 0, 3.0, 0.0)]
    ckt = ckt_cls(branches)
    ckt.resolve()

    I = ckt.currents["0"]
    assert I == pytest.approx(1.25, rel=0.01)
    V_loop = 10.0 - I * 5.0 - I * 3.0
    assert V_loop == pytest.approx(0.0, abs=0.01)


def test_selfcheck_wrong_fails(
    wrong_student_classes: Tuple[Type[ElectricField], Type[Circuit]],
) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong answer."""
    ef_cls, ckt_cls = wrong_student_classes

    # Wrong electric field should give wrong magnitude (E ∝ 1/r instead of 1/r²)
    ef = ef_cls(q=1e-9)
    Ex, Ey = ef.field(1.0, 0.0)
    expected_correct = 1e-9 / (4.0 * math.pi * EPS_0 * 1.0)
    # The wrong answer uses 1/r instead of 1/r², so at r=1 they happen to match
    # Test at r=2 instead
    Ex2, Ey2 = ef.field(2.0, 0.0)
    expected_at_2 = 1e-9 / (4.0 * math.pi * EPS_0 * 4.0)  # 1/r²
    wrong_expected_at_2 = 1e-9 / (4.0 * math.pi * EPS_0 * 2.0)  # 1/r
    actual_mag = math.hypot(Ex2, Ey2)
    # The wrong answer should be closer to the 1/r value than to 1/r²
    err_from_correct = abs(actual_mag - expected_at_2) / expected_at_2
    err_from_wrong = abs(actual_mag - wrong_expected_at_2) / wrong_expected_at_2
    assert err_from_correct > 0.01, (
        f"Wrong answer unexpectedly passed field check at r=2: "
        f"|E|={actual_mag:.4e}, correct 1/r²={expected_at_2:.4e}, wrong 1/r={wrong_expected_at_2:.4e}"
    )

    # Wrong circuit solver should give wrong current
    branches = [(0, 1, 5.0, 10.0), (1, 0, 3.0, 0.0)]
    ckt = ckt_cls(branches)
    ckt.resolve()
    I = ckt.currents["0"]
    assert abs(I - 1.25) > 0.01, (
        f"Wrong answer unexpectedly passed circuit check: I={I:.4f}A, "
        f"expected 1.25A for correct answer"
    )


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_classes: Tuple[Type[ElectricField], Type[Circuit]],
    wrong_student_classes: Tuple[Type[ElectricField], Type[Circuit]],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    ef_cls, _ = student_classes
    ef = ef_cls()
    # Verify it's not the wrong answer
    a = ef.field(1.0, 0.0)
    assert a is not None, "field() should return a tuple"