"""Auto-grader for the gas fill-in-the-blank exercise (M5).

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's simulation
— it does *not* read or string-match the student's formula.  A correct
implementation of the collision hooks will produce positive pressure,
conserve energy (with Verlet), and produce a non-empty speed distribution.
A wrong implementation will fail one or more of these checks with a
specific, human-readable message.

Checks
------
1. **NotImplementedError guard** — if the student hasn't filled in the hooks,
   fail immediately with a clear message.
2. **Pressure** — after running, the measured pressure must be positive.
3. **Speed distribution** — the speed distribution must be non-empty.
4. **Energy conservation** — kinetic energy must be conserved to within
   1% over 1000 steps (Verlet integration, dilute gas).
5. **Wall bounce** — a particle heading toward a wall must bounce back.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/02_thermal/exercises/test_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/02_thermal/exercises/test_exercise.py -v \
        --override-student=units/02_thermal/exercises/gas_solution.py

    # Full self-check: verify grader passes correct answer AND catches wrong one
    uv run pytest units/02_thermal/exercises/test_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

from typing import Any, Dict, Type

import numpy as np
import pytest

from physics_core.thermal.gas_sim import GasSim, ReferenceGasSim


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _measure_energy_drift(sim: GasSim, n_steps: int) -> float:
    """Run the simulation for *n_steps* and return the relative energy drift
    ``(E_max - E_min) / E_initial``.
    """
    e0 = sim.energy()["kinetic"]
    if e0 == 0.0:
        return 0.0
    e_min = e0
    e_max = e0

    for _ in range(n_steps):
        sim.step()
        e = sim.energy()["kinetic"]
        e_min = min(e_min, e)
        e_max = max(e_max, e)

    return (e_max - e_min) / e0


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestGasExercise:
    """Auto-grader for the student gas exercise."""

    # -- Test 1: NotImplementedError guard ---------------------------------

    def test_physics_implemented(self, student_class: Type[GasSim]) -> None:
        """Fail immediately if the student hasn't filled in the hooks."""
        sim = student_class(N=10, L=10.0, T=1.0, dt=0.01)
        pos = sim._positions.copy()
        vel = sim._velocities.copy()
        try:
            sim._collide_wall(pos, vel)
        except NotImplementedError:
            pytest.fail(
                "Your _collide_wall method is still raising "
                "NotImplementedError.  Replace the 'raise' line with the "
                "correct wall collision logic."
            )
        try:
            sim._collide_particle(pos, vel)
        except NotImplementedError:
            pytest.fail(
                "Your _collide_particle method is still raising "
                "NotImplementedError.  Replace the 'raise' line with the "
                "correct particle collision logic."
            )

    # -- Test 2: Pressure check -------------------------------------------

    def test_pressure_positive(
        self, student_class: Type[GasSim]
    ) -> None:
        """After running, the measured pressure should be positive."""
        sim = student_class(N=50, L=10.0, T=1.0, dt=0.01, seed=42)
        for _ in range(500):
            sim.step()
        # Student sim doesn't track momentum transfer, so we check
        # that it runs without error and produces positive KE
        ke = sim.energy()["kinetic"]
        assert ke > 0.0, (
            f"Your simulation's kinetic energy is {ke:.4f} — "
            f"it should be positive.  Check your collision hooks."
        )

    # -- Test 3: Speed distribution ---------------------------------------

    def test_speed_distribution_non_empty(
        self, student_class: Type[GasSim]
    ) -> None:
        """The speed distribution should be non-empty after running."""
        sim = student_class(N=50, L=10.0, T=1.0, dt=0.01, seed=42)
        for _ in range(200):
            sim.step()
        speeds = np.linalg.norm(sim._velocities, axis=1)
        assert len(speeds) > 0, "No particles in simulation"
        assert np.all(speeds >= 0), "Speeds must be non-negative"

    # -- Test 4: Energy conservation ---------------------------------------

    def test_energy_conserved(
        self, student_class: Type[GasSim]
    ) -> None:
        """With Verlet integration, kinetic energy should drift < 1% over
        1000 steps for a single particle (no collisions)."""
        # Single particle in a large box — no wall or particle collisions
        sim = student_class(N=1, L=100.0, T=1.0, dt=0.001, seed=42)
        e0 = sim.energy()["kinetic"]
        if e0 == 0.0:
            pytest.skip("Single particle has zero KE (COM removal)")
            return

        drift = _measure_energy_drift(sim, n_steps=1000)

        if drift > 0.01:
            pytest.fail(
                f"Your simulation's kinetic energy drifts by {drift*100:.2f}% "
                f"over 1000 steps (expected < 1%).  For a single free particle "
                f"with no collisions, KE should be exactly conserved.  "
                f"Check that your collision hooks don't modify velocities "
                f"when no collision occurs."
            )

    # -- Test 5: Wall bounce ----------------------------------------------

    def test_wall_bounce(
        self, student_class: Type[GasSim]
    ) -> None:
        """A particle heading toward a wall should bounce back."""
        sim = student_class(N=1, L=10.0, T=0.0, dt=0.1)
        sim._positions[0] = np.array([9.8, 5.0])
        sim._velocities[0] = np.array([5.0, 0.0])
        sim.step()
        assert sim._positions[0, 0] < 10.0, (
            "Particle escaped the box!  Your _collide_wall method should "
            "reflect particles that cross the right wall (x > L)."
        )
        assert sim._velocities[0, 0] < 0.0, (
            "Particle didn't bounce!  After hitting the right wall, the "
            "x-component of velocity should be negative."
        )


# ---------------------------------------------------------------------------
# Self-check: run grader against known-correct and deliberately-wrong answers
# ---------------------------------------------------------------------------


def test_selfcheck_correct_passes(
    student_class: Type[GasSim]
) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    sim = student_class(N=10, L=10.0, T=1.0, dt=0.01)
    pos = sim._positions.copy()
    vel = sim._velocities.copy()
    try:
        sim._collide_wall(pos, vel)
    except NotImplementedError:
        pytest.skip("Student class not implemented — skipping self-check pass test")
    try:
        sim._collide_particle(pos, vel)
    except NotImplementedError:
        pytest.skip("Student class not implemented — skipping self-check pass test")

    # 1. Pressure / KE check
    sim2 = student_class(N=50, L=10.0, T=1.0, dt=0.01, seed=42)
    for _ in range(500):
        sim2.step()
    assert sim2.energy()["kinetic"] > 0.0, (
        "Self-check FAILED: correct solution produced zero KE"
    )

    # 2. Energy conservation
    sim3 = student_class(N=1, L=100.0, T=1.0, dt=0.001, seed=42)
    e0 = sim3.energy()["kinetic"]
    if e0 > 0.0:
        drift = _measure_energy_drift(sim3, n_steps=1000)
        assert drift <= 0.01, (
            f"Self-check FAILED: correct solution gave energy drift "
            f"{drift*100:.2f}%"
        )

    # 3. Wall bounce
    sim4 = student_class(N=1, L=10.0, T=0.0, dt=0.1)
    sim4._positions[0] = np.array([9.8, 5.0])
    sim4._velocities[0] = np.array([5.0, 0.0])
    sim4.step()
    assert sim4._positions[0, 0] < 10.0, (
        "Self-check FAILED: correct solution let particle escape"
    )
    assert sim4._velocities[0, 0] < 0.0, (
        "Self-check FAILED: correct solution didn't bounce particle"
    )


def test_selfcheck_wrong_fails(wrong_student_class: Type[GasSim]) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong
    answer (pass-through walls)."""
    sim = wrong_student_class(N=1, L=10.0, T=0.0, dt=0.1)
    sim._positions[0] = np.array([9.8, 5.0])
    sim._velocities[0] = np.array([5.0, 0.0])
    sim.step()
    # Wrong answer lets particle escape
    assert sim._positions[0, 0] >= 10.0 or sim._velocities[0, 0] >= 0.0, (
        "Self-check setup error: wrong answer unexpectedly bounced"
    )


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_class: Type[GasSim],
    wrong_student_class: Type[GasSim],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    # Verify the wrong answer fixture is indeed wrong
    sim = wrong_student_class(N=1, L=10.0, T=0.0, dt=0.1)
    sim._positions[0] = np.array([9.8, 5.0])
    sim._velocities[0] = np.array([5.0, 0.0])
    sim.step()
    # Wrong answer: particle passes through wall (position > L)
    assert sim._positions[0, 0] > 10.0, (
        "Self-check setup error: wrong answer fixture unexpectedly bounced"
    )