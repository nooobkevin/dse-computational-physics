"""Auto-grader for the Physics & Society fill-in-the-blank exercise (M5).

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's
simulation — it does *not* read or string-match the student's formula.
A correct implementation of ``decay_probability`` will produce the right
analytic N(t) and a Monte Carlo half-life estimate within tolerance.
A wrong implementation will fail one or more of these checks.

Checks
------
1.  **NotImplementedError guard** — if the student hasn't filled in the hook,
    fail immediately with a clear message.
2.  **Analytic N** — ``N(t) = N0 * (1/2)^(t/T)`` matches at t = T.
3.  **Monte Carlo half-life** — estimated half-life within 10% of true T.
4.  **Decay probability bounds** — p in [0, 1] for all dt.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/06_society/exercises/test_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/06_society/exercises/test_exercise.py -v \
        --override-student=units/06_society/exercises/society_solution.py

    # Full self-check
    uv run pytest units/06_society/exercises/test_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

import math
from typing import Type

import pytest

from physics_core.society.decay import DecaySim, ReferenceDecaySim

LN2 = math.log(2.0)


# ===========================================================================
# Tests
# ===========================================================================


class TestDecayExercise:
    """Auto-grader for the student decay exercise."""

    def test_physics_implemented(self, student_class: Type[DecaySim]) -> None:
        """Fail immediately if the student hasn't filled in the hook."""
        sim = student_class()
        try:
            sim.decay_probability(0.01)
        except NotImplementedError:
            pytest.fail(
                "Your decay_probability() method is still raising NotImplementedError. "
                "Replace the 'raise' line with: "
                "p = 1 - exp(-ln(2) * dt / T)"
            )

    def test_decay_probability_bounds(self, student_class: Type[DecaySim]) -> None:
        """Decay probability must be in [0, 1] for all dt."""
        sim = student_class(N0=10000, half_life=1.0)
        for dt in [0.0, 0.001, 0.01, 0.1, 1.0, 10.0]:
            p = sim.decay_probability(dt)
            if p < 0.0 or p > 1.0:
                pytest.fail(
                    f"Your decay_probability({dt}) = {p:.6f}, "
                    f"which is outside [0, 1]. "
                    f"Check your formula — p must be a probability."
                )

    def test_analytic_N_at_half_life(self, student_class: Type[DecaySim]) -> None:
        """N(T) = N0/2 when using the analytic formula via ReferenceDecaySim.

        This test verifies that the student's decay_probability, when used
        in a ReferenceDecaySim-like context, produces the correct analytic
        behaviour.  We use the ReferenceDecaySim's analytic_N as the
        reference and check that the student's Monte Carlo simulation
        approximates it.
        """
        N0 = 50000
        T = 1.0
        dt = 0.02
        n_steps = 150

        sim = student_class(N0=N0, half_life=T, dt=dt, seed=42)
        for _ in range(n_steps):
            sim.step()

        t = sim.state["t"]
        ref = ReferenceDecaySim(N0=N0, half_life=T)
        analytic_N = ref.analytic_N(t)
        mc_N = sim.nuclei_remaining()

        rel_err = abs(mc_N - analytic_N) / analytic_N
        if rel_err > 0.05:
            pytest.fail(
                f"Your Monte Carlo simulation at t={t:.2f}s gives "
                f"N={mc_N}, but the analytic value is {analytic_N:.1f} "
                f"(relative error {rel_err*100:.2f}%). "
                f"Check your decay_probability() formula."
            )

    def test_half_life_estimate(self, student_class: Type[DecaySim]) -> None:
        """Monte Carlo half-life estimate should be within 10% of true T."""
        N0 = 50000
        T = 1.0
        dt = 0.02
        n_steps = 200

        sim = student_class(N0=N0, half_life=T, dt=dt, seed=42)
        for _ in range(n_steps):
            sim.step()

        estimated_T = sim.half_life()
        if estimated_T == float("inf"):
            pytest.fail(
                "Your simulation did not reach N0/2 within the simulation time. "
                "Check your decay_probability() formula."
            )

        rel_err = abs(estimated_T - T) / T
        if rel_err > 0.10:
            pytest.fail(
                f"Your estimated half-life is {estimated_T:.4f}s, "
                f"but the true half-life is T={T}s "
                f"(relative error {rel_err*100:.2f}%). "
                f"Check your decay_probability() formula."
            )


# ===========================================================================
# Self-check
# ===========================================================================


def test_selfcheck_correct_passes(student_class: Type[DecaySim]) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    sim = student_class(N0=50000, half_life=1.0, dt=0.02, seed=42)

    p_implemented = True
    try:
        sim.decay_probability(0.01)
    except NotImplementedError:
        p_implemented = False
    if not p_implemented:
        pytest.skip("Student class not implemented — skipping")

    # Check decay probability formula
    p = sim.decay_probability(0.1)
    expected_p = 1.0 - math.exp(-LN2 * 0.1 / 1.0)
    assert p == pytest.approx(expected_p, rel=0.01)

    # Run simulation and check analytic N
    for _ in range(150):
        sim.step()
    t = sim.state["t"]
    ref = ReferenceDecaySim(N0=50000, half_life=1.0)
    analytic_N = ref.analytic_N(t)
    mc_N = sim.nuclei_remaining()
    rel_err = abs(mc_N - analytic_N) / analytic_N
    assert rel_err < 0.05, f"MC N={mc_N} vs analytic N={analytic_N:.1f} (rel_err={rel_err*100:.2f}%)"

    # Check half-life estimate
    estimated_T = sim.half_life()
    assert estimated_T != float("inf")
    assert abs(estimated_T - 1.0) / 1.0 < 0.10


def test_selfcheck_wrong_fails(wrong_student_class: Type[DecaySim]) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong answer."""
    sim = wrong_student_class(N0=50000, half_life=1.0, dt=0.02, seed=42)

    # Wrong decay probability should give wrong results
    p = sim.decay_probability(0.1)
    expected_correct = 1.0 - math.exp(-LN2 * 0.1 / 1.0)
    # The wrong answer uses p = dt/T which gives p=0.1 instead of ~0.067
    err = abs(p - expected_correct) / expected_correct
    assert err > 0.1, (
        f"Wrong answer unexpectedly passed: p(0.1)={p:.4f}, "
        f"expected {expected_correct:.4f} (err={err*100:.2f}%)"
    )

    # Run simulation — should give wrong half-life
    for _ in range(200):
        sim.step()
    estimated_T = sim.half_life()
    if estimated_T != float("inf"):
        assert abs(estimated_T - 1.0) / 1.0 > 0.05, (
            f"Wrong answer unexpectedly gave half-life={estimated_T:.4f}s"
        )


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_class: Type[DecaySim],
    wrong_student_class: Type[DecaySim],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    sim = student_class()
    assert sim is not None, "StudentDecaySim should be importable"
    assert hasattr(sim, "decay_probability"), "StudentDecaySim should have decay_probability()"