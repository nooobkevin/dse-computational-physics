"""Auto-grader for the pendulum fill-in-the-blank exercise (M5).

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's simulation
— it does *not* read or string-match the student's formula.  A correct
implementation of ``angular_acceleration`` will produce the right period,
conserve energy (with Verlet), and keep the amplitude bounded.  A wrong
implementation will fail one or more of these checks with a specific,
human-readable message.

Checks
------
1. **NotImplementedError guard** — if the student hasn't filled in the hook,
   fail immediately with a clear message.
2. **Period** — measure the oscillation period via zero-crossings and compare
   to the small-angle formula ``T = 2π√(L/g)`` (tolerance 1%).
3. **Energy conservation** — run for ~2000 steps with Verlet; total energy
   drift must be < 2%.
4. **Stability / sign** — the amplitude must stay bounded (not blow up) over
   many periods.  A wrong sign (e.g. ``+(g/L)θ``) will cause exponential
   growth and fail this check.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/01_mechanics/exercises/test_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/01_mechanics/exercises/test_exercise.py -v \
        --override-student=units/01_mechanics/exercises/pendulum_solution.py

    # Full self-check: verify grader passes correct answer AND catches wrong one
    uv run pytest units/01_mechanics/exercises/test_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

import math
from typing import Any, Dict, Type

import pytest

from physics_core.mechanics.pendulum import PendulumSim, ReferencePendulumSim


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _measure_period(sim: PendulumSim, max_steps: int = 50_000) -> float:
    """Run the simulation and measure the oscillation period via
    zero-crossings (positive → negative).

    Returns the average period in seconds.
    Raises ``RuntimeError`` if fewer than 2 crossings are found.
    """
    prev_theta = sim.state["theta"]
    first_crossing_t: float | None = None
    last_crossing_t: float | None = None
    crossings = 0

    for _ in range(max_steps):
        sim.step()
        theta = sim.state["theta"]
        if prev_theta > 0 and theta <= 0:
            crossings += 1
            if first_crossing_t is None:
                first_crossing_t = sim.state["t"]
            last_crossing_t = sim.state["t"]
        prev_theta = theta

    if crossings < 2 or first_crossing_t is None or last_crossing_t is None:
        raise RuntimeError(
            f"Could not measure period: only {crossings} zero-crossing(s) "
            f"detected in {max_steps} steps.  Your angular_acceleration may "
            f"be producing a non-oscillatory or diverging solution."
        )

    # Period = (time between first and last crossing) / (number of intervals)
    measured_T = (last_crossing_t - first_crossing_t) / (crossings - 1)
    return measured_T


def _measure_energy_drift(sim: PendulumSim, n_steps: int) -> float:
    """Run the simulation for *n_steps* and return the relative energy drift
    ``(E_max - E_min) / E_initial``.
    """
    e0 = sim.energy()["total"]
    e_min = e0
    e_max = e0

    for _ in range(n_steps):
        sim.step()
        e = sim.energy()["total"]
        e_min = min(e_min, e)
        e_max = max(e_max, e)

    if e0 == 0.0:
        return 0.0
    return (e_max - e_min) / e0


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestPendulumExercise:
    """Auto-grader for the student pendulum exercise."""

    # -- Parameterisation for different test scenarios ----------------------

    @pytest.fixture(params=[
        {"length": 1.0, "g": 9.81, "theta0": 0.05, "dt": 0.001, "scheme": "verlet"},
        {"length": 0.5, "g": 9.81, "theta0": 0.03, "dt": 0.0005, "scheme": "verlet"},
        {"length": 2.0, "g": 9.81, "theta0": 0.08, "dt": 0.002, "scheme": "verlet"},
    ])
    def sim_params(self, request: pytest.FixtureRequest) -> Dict[str, Any]:
        return request.param

    # -- Test 1: NotImplementedError guard ---------------------------------

    def test_physics_implemented(self, student_class: Type[PendulumSim]) -> None:
        """Fail immediately if the student hasn't filled in the hook."""
        sim = student_class()
        try:
            sim.angular_acceleration(0.1, 0.0)
        except NotImplementedError:
            pytest.fail(
                "Your angular_acceleration method is still raising "
                "NotImplementedError.  Replace the 'raise' line with the "
                "correct physics formula:  return -(self.g / self.length) "
                "* math.sin(theta)"
            )

    # -- Test 2: Period check ----------------------------------------------

    def test_period_matches_formula(
        self, student_class: Type[PendulumSim], sim_params: Dict[str, Any]
    ) -> None:
        """The measured period should match 2π√(L/g) to within 1%."""
        student = student_class(**sim_params)
        reference = ReferencePendulumSim(**sim_params)

        student_T = _measure_period(student)
        ref_T = _measure_period(reference)
        formula_T = student.period_from_formula

        rel_err = abs(student_T - formula_T) / formula_T
        if rel_err > 0.01:
            pytest.fail(
                f"Your pendulum's period is {student_T:.4f} s, but the "
                f"expected small-angle period is {formula_T:.4f} s "
                f"(relative error {rel_err*100:.2f}%).  "
                f"The reference implementation gives {ref_T:.4f} s.  "
                f"Check your angular_acceleration formula — did you use "
                f"the correct sign and the full -(g/L)*sin(θ) expression?"
            )

    # -- Test 3: Energy conservation ---------------------------------------

    def test_energy_conserved(
        self, student_class: Type[PendulumSim], sim_params: Dict[str, Any]
    ) -> None:
        """With Verlet integration, total energy should drift < 2% over
        ~2000 steps."""
        params = dict(sim_params)
        params["scheme"] = "verlet"
        student = student_class(**params)

        drift = _measure_energy_drift(student, n_steps=2000)

        if drift > 0.02:
            pytest.fail(
                f"Your simulation's total energy drifts by {drift*100:.2f}% "
                f"over 2000 steps (expected < 2%).  This usually means your "
                f"angular_acceleration formula is wrong.  Common mistakes:\n"
                f"  - Wrong sign (e.g. +(g/L)*θ instead of -(g/L)*sin(θ))\n"
                f"  - Using θ instead of sin(θ) at large amplitude\n"
                f"  - Using omega (ω) instead of theta (θ)\n"
                f"Check your implementation and re-run."
            )

    # -- Test 4: Stability / sign check ------------------------------------

    def test_amplitude_bounded(
        self, student_class: Type[PendulumSim]
    ) -> None:
        """The oscillation amplitude should stay bounded (not blow up) over
        many periods.  A wrong sign in angular_acceleration causes
        exponential growth."""
        sim = student_class(length=1.0, g=9.81, theta0=0.1, dt=0.01, scheme="verlet")
        initial_amplitude = abs(sim.state["theta"])

        for _ in range(10_000):
            sim.step()

        final_amplitude = abs(sim.state["theta"])

        if final_amplitude > 10.0 * initial_amplitude:
            pytest.fail(
                f"Your pendulum's amplitude grew from {initial_amplitude:.3f} rad "
                f"to {final_amplitude:.3f} rad — it's blowing up!  This usually "
                f"means your angular_acceleration has the wrong sign.  "
                f"The correct formula is  -(g/L) * sin(θ),  NOT  +(g/L) * θ."
            )


# ---------------------------------------------------------------------------
# Self-check: run grader against known-correct and deliberately-wrong answers
# ---------------------------------------------------------------------------

def test_selfcheck_correct_passes(
    student_class: Type[PendulumSim]
) -> None:
    """Self-check: the grader must PASS when given the correct solution.

    This test is only active when ``--override-student`` points to the
    solution file (or when ``--selfcheck`` is used, which sets it up).
    """
    # Verify the student class actually works (doesn't raise NotImplementedError)
    sim = student_class()
    try:
        a = sim.angular_acceleration(0.1, 0.0)
    except NotImplementedError:
        pytest.skip("Student class not implemented — skipping self-check pass test")

    # Run all the standard checks manually
    # 1. Period
    params = {"length": 1.0, "g": 9.81, "theta0": 0.05, "dt": 0.001, "scheme": "verlet"}
    s = student_class(**params)
    T = _measure_period(s)
    formula_T = s.period_from_formula
    rel_err = abs(T - formula_T) / formula_T
    assert rel_err <= 0.01, (
        f"Self-check FAILED: correct solution gave period error "
        f"{rel_err*100:.2f}% (T={T:.4f}, expected {formula_T:.4f})"
    )

    # 2. Energy conservation
    s2 = student_class(**params)
    drift = _measure_energy_drift(s2, n_steps=2000)
    assert drift <= 0.02, (
        f"Self-check FAILED: correct solution gave energy drift "
        f"{drift*100:.2f}%"
    )

    # 3. Stability
    s3 = student_class(length=1.0, g=9.81, theta0=0.1, dt=0.01, scheme="verlet")
    initial_amp = abs(s3.state["theta"])
    for _ in range(10_000):
        s3.step()
    assert abs(s3.state["theta"]) <= 10.0 * initial_amp, (
        "Self-check FAILED: correct solution amplitude blew up"
    )


def test_selfcheck_wrong_fails(wrong_student_class: Type[PendulumSim]) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong
    answer (``+(g/L)*theta`` instead of ``-(g/L)*sin(theta)``).

    This test is only active when ``--selfcheck`` is used.
    """
    # The wrong answer should fail the period test (it will oscillate
    # with the wrong frequency / blow up)
    params = {"length": 1.0, "g": 9.81, "theta0": 0.05, "dt": 0.001, "scheme": "verlet"}
    sim = wrong_student_class(**params)

    with pytest.raises((RuntimeError, AssertionError, pytest.fail.Exception)):
        T = _measure_period(sim)
        formula_T = sim.period_from_formula
        rel_err = abs(T - formula_T) / formula_T
        assert rel_err > 0.01, (
            f"Self-check FAILED: wrong answer unexpectedly passed period check "
            f"(T={T:.4f}, formula={formula_T:.4f}, error={rel_err*100:.2f}%)"
        )

    # Also verify energy drift is large
    sim2 = wrong_student_class(**params)
    drift = _measure_energy_drift(sim2, n_steps=2000)
    assert drift > 0.02, (
        f"Self-check FAILED: wrong answer unexpectedly passed energy check "
        f"(drift={drift*100:.2f}%)"
    )


# ---------------------------------------------------------------------------
# Self-check runner (invoked by --selfcheck CLI flag)
# ---------------------------------------------------------------------------

def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_class: Type[PendulumSim],
    wrong_student_class: Type[PendulumSim],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    # The correct-solution tests are already parametrised above;
    # this test just confirms the wrong answer is caught.
    # (The actual pass/fail assertions are in the dedicated tests.)
    # We verify the wrong answer fixture is indeed wrong.
    sim = wrong_student_class()
    a = sim.angular_acceleration(0.1, 0.0)
    # Wrong answer uses +(g/L)*theta, so for theta=0.1, L=1.0, g=9.81:
    # a should be +0.981 (positive), while correct is -0.981 (negative)
    assert a > 0, (
        "Self-check setup error: wrong answer fixture produced "
        f"a={a:.4f}, expected positive value"
    )