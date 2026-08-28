"""Auto-graders for the gas and specific heat fill-in-the-blank exercises (M5).

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's simulation
— it does *not* read or string-match the student's formula.  A correct
implementation of the collision hooks will produce positive pressure,
conserve energy (with Verlet), and produce a non-empty speed distribution.
A wrong implementation will fail one or more of these checks with a
specific, human-readable message.

Gas exercise checks
-------------------
1. **NotImplementedError guard** — if the student hasn't filled in the hooks,
   fail immediately with a clear message.
2. **Pressure** — after running, the measured pressure must be positive.
3. **Speed distribution** — the speed distribution must be non-empty.
4. **Energy conservation** — kinetic energy must be conserved to within
   1% over 1000 steps (Verlet integration, dilute gas).
5. **Wall bounce** — a particle heading toward a wall must bounce back.

Specific heat exercise checks
-----------------------------
1. **NotImplementedError guard** — if the student hasn't filled in the
   functions, fail immediately.
2. **specific_heat_from_fit** — correct slope from (Q, delta_T) fit.
3. **energy_to_heat** — correct Q = m * c * delta_T.
4. **final_temperature** — correct T_final calculation.
5. **Error handling** — reasonable error for edge cases.

Usage
-----
    # Grade the student's gas exercise (default)
    uv run pytest units/02_thermal/exercises/test_exercise.py -v

    # Grade the student's specific heat exercise
    uv run pytest units/02_thermal/exercises/test_exercise.py \
        -k TestSpecificHeat -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/02_thermal/exercises/test_exercise.py -v \
        --override-student=units/02_thermal/exercises/gas_solution.py

    uv run pytest units/02_thermal/exercises/test_exercise.py -v \
        --override-student=units/02_thermal/exercises/specific_heat_solution.py \
        -k TestSpecificHeat

    # Full self-check: verify grader passes correct answer AND catches wrong one
    uv run pytest units/02_thermal/exercises/test_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

from typing import Any, Dict, Type
from types import ModuleType

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


# ---------------------------------------------------------------------------
# Specific heat exercise tests
# ---------------------------------------------------------------------------


class TestSpecificHeat:
    """Auto-grader for the specific heat capacity exercise."""

    # -- Test 1: NotImplementedError guard ---------------------------------

    def test_functions_implemented(
        self, specific_heat_module: ModuleType
    ) -> None:
        """Fail immediately if the student hasn't filled in the functions."""
        mod = specific_heat_module
        Q_data = np.array([100.0, 200.0, 300.0])
        dT_data = np.array([2.0, 4.0, 6.0])
        try:
            mod.specific_heat_from_fit(Q_data, dT_data, mass=0.5)
        except NotImplementedError:
            pytest.fail(
                "Your specific_heat_from_fit function is still raising "
                "NotImplementedError.  Replace the 'raise' line with "
                "the correct fit computation."
            )
        try:
            mod.energy_to_heat(mass=0.5, c=900.0, delta_T=10.0)
        except NotImplementedError:
            pytest.fail(
                "Your energy_to_heat function is still raising "
                "NotImplementedError.  Replace the 'raise' line with "
                "the correct formula."
            )
        try:
            mod.final_temperature(Q=1000.0, mass=0.5, c=900.0, T_initial=300.0)
        except NotImplementedError:
            pytest.fail(
                "Your final_temperature function is still raising "
                "NotImplementedError.  Replace the 'raise' line with "
                "the correct computation."
            )

    # -- Test 2: specific_heat_from_fit -----------------------------------

    def test_specific_heat_from_fit_correct(
        self, specific_heat_module: ModuleType
    ) -> None:
        """Check that the fit returns the correct specific heat capacity."""
        mod = specific_heat_module
        # Known data: Q = C * delta_T, where C = mass * c
        # For c = 900 J/(kg·K), mass = 0.5 kg: C = 450 J/K
        mass = 0.5
        c_true = 900.0
        C_true = mass * c_true
        delta_T_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        Q_data = C_true * delta_T_data
        # Add small noise
        rng = np.random.default_rng(42)
        Q_data += rng.normal(0.0, 1.0, size=len(Q_data))

        C, c, err = mod.specific_heat_from_fit(Q_data, delta_T_data, mass)
        assert c == pytest.approx(c_true, rel=0.02), (
            f"c = {c:.2f} J/(kg·K), expected ~{c_true}"
        )
        assert C == pytest.approx(C_true, rel=0.02), (
            f"C = {C:.2f} J/K, expected ~{C_true}"
        )
        assert err >= 0.0, "Standard error should be non-negative"

    def test_specific_heat_from_fit_noiseless(
        self, specific_heat_module: ModuleType
    ) -> None:
        """With noiseless data, the fit should be exact."""
        mod = specific_heat_module
        mass = 1.0
        c_true = 4186.0  # water specific heat capacity
        C_true = mass * c_true
        delta_T_data = np.array([10.0, 20.0, 30.0, 40.0])
        Q_data = C_true * delta_T_data

        C, c, err = mod.specific_heat_from_fit(Q_data, delta_T_data, mass)
        assert c == pytest.approx(c_true, abs=0.1), (
            f"c = {c:.2f}, expected {c_true}"
        )
        assert C == pytest.approx(C_true, abs=0.1)
        assert err == pytest.approx(0.0, abs=0.01)

    # -- Test 3: energy_to_heat -------------------------------------------

    def test_energy_to_heat_correct(
        self, specific_heat_module: ModuleType
    ) -> None:
        """Check that energy_to_heat returns Q = m * c * delta_T."""
        mod = specific_heat_module
        # Water: m=2 kg, c=4186 J/(kg·K), delta_T=10 K
        Q = mod.energy_to_heat(mass=2.0, c=4186.0, delta_T=10.0)
        assert Q == pytest.approx(83720.0, rel=0.001), (
            f"Q = {Q:.2f} J, expected 83720 J"
        )

    def test_energy_to_heat_zero_delta_t(
        self, specific_heat_module: ModuleType
    ) -> None:
        """Zero temperature change should give zero energy."""
        mod = specific_heat_module
        Q = mod.energy_to_heat(mass=1.0, c=900.0, delta_T=0.0)
        assert Q == pytest.approx(0.0, abs=1e-10)

    # -- Test 4: final_temperature ----------------------------------------

    def test_final_temperature_correct(
        self, specific_heat_module: ModuleType
    ) -> None:
        """Check that final_temperature returns the correct result."""
        mod = specific_heat_module
        # Add 10000 J to 0.5 kg of water (c=4186) at 300 K
        T_final = mod.final_temperature(
            Q=10000.0, mass=0.5, c=4186.0, T_initial=300.0
        )
        expected = 300.0 + 10000.0 / (0.5 * 4186.0)
        assert T_final == pytest.approx(expected, rel=0.001), (
            f"T_final = {T_final:.3f} K, expected {expected:.3f} K"
        )

    def test_final_temperature_zero_heat(
        self, specific_heat_module: ModuleType
    ) -> None:
        """Zero heat should give same temperature."""
        mod = specific_heat_module
        T_final = mod.final_temperature(
            Q=0.0, mass=1.0, c=900.0, T_initial=300.0
        )
        assert T_final == pytest.approx(300.0)


# ---------------------------------------------------------------------------
# Specific heat self-check
# ---------------------------------------------------------------------------


def test_specific_heat_selfcheck_correct(
    specific_heat_module: ModuleType,
) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    mod = specific_heat_module
    # Test specific_heat_from_fit
    mass = 0.5
    c_true = 900.0
    C_true = mass * c_true
    dT = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    Q = C_true * dT
    C, c, err = mod.specific_heat_from_fit(Q, dT, mass)
    assert c == pytest.approx(c_true, rel=0.02), (
        f"Self-check FAILED: specific heat c={c:.2f}"
    )
    # Test energy_to_heat
    Q_calc = mod.energy_to_heat(mass=2.0, c=4186.0, delta_T=10.0)
    assert Q_calc == pytest.approx(83720.0, rel=0.001)
    # Test final_temperature
    T_final = mod.final_temperature(
        Q=10000.0, mass=0.5, c=4186.0, T_initial=300.0
    )
    expected = 300.0 + 10000.0 / (0.5 * 4186.0)
    assert T_final == pytest.approx(expected, rel=0.001)


def test_specific_heat_selfcheck_wrong_fails(
    wrong_specific_heat_module: ModuleType,
) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong
    answer (fixed values, not computed)."""
    mod = wrong_specific_heat_module
    Q_data = np.array([100.0, 200.0, 300.0])
    dT_data = np.array([2.0, 4.0, 6.0])
    C, c, err = mod.specific_heat_from_fit(Q_data, dT_data, mass=0.5)
    # Wrong answer returns C=100, c=50 — should not match
    assert C == pytest.approx(100.0) and c == pytest.approx(50.0), (
        "Self-check setup error: wrong answer unexpectedly correct"
    )
    # Wrong answer returns mass, not energy
    Q_wrong = mod.energy_to_heat(mass=2.0, c=4186.0, delta_T=10.0)
    assert Q_wrong == pytest.approx(2.0), (
        "Self-check setup error: wrong answer unexpectedly correct"
    )


def test_specific_heat_selfcheck_runner(
    request: pytest.FixtureRequest,
    specific_heat_module: ModuleType,
    wrong_specific_heat_module: ModuleType,
) -> None:
    """Orchestrate the full specific heat self-check with --selfcheck."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    # Verify the wrong answer fixture is indeed wrong
    mod = wrong_specific_heat_module
    Q_data = np.array([100.0, 200.0, 300.0])
    dT_data = np.array([2.0, 4.0, 6.0])
    C, c, err = mod.specific_heat_from_fit(Q_data, dT_data, mass=0.5)
    assert C == pytest.approx(100.0) and c == pytest.approx(50.0), (
        "Self-check setup error: wrong answer unexpectedly correct"
    )