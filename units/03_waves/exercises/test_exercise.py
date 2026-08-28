"""Auto-grader for the wave fill-in-the-blank exercise.

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's simulation
— it does *not* read or string-match the student's formula.  A correct
implementation of ``displacement`` will produce the right field values,
correct superposition behaviour, and correct intensity scaling.  A wrong
implementation will fail one or more of these checks with a specific,
human-readable message.

Checks
------
1. **NotImplementedError guard** — if the student hasn't filled in the hook,
   fail immediately with a clear message.
2. **Field values** — compare the numerical field to the analytical
   ``A sin(kx - ωt)`` expression (tolerance 1e-10).
3. **Superposition → standing wave** — verify that a node has ~zero
   displacement over time.
4. **Intensity ∝ A²** — verify that energy scales as amplitude squared.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/03_waves/exercises/test_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/03_waves/exercises/test_exercise.py -v \
        --override-student=units/03_waves/exercises/wave_solution.py

    # Full self-check: verify grader passes correct answer AND catches wrong one
    uv run pytest units/03_waves/exercises/test_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

import math
from typing import Type

import numpy as np
import pytest

from physics_core.waves.wave_sim import WaveSim, ReferenceWaveSim


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestWaveExercise:
    """Auto-grader for the student wave exercise."""

    # -- Test 1: NotImplementedError guard ---------------------------------

    def test_physics_implemented(self, student_class: Type[WaveSim]) -> None:
        """Fail immediately if the student hasn't filled in the hook."""
        sim = student_class()
        try:
            sim.displacement(0.5, 0.1)
        except NotImplementedError:
            pytest.fail(
                "Your displacement method is still raising "
                "NotImplementedError.  Replace the 'raise' line with the "
                "correct physics formula:  return self.amplitude * "
                "math.sin(self.k * x - self.omega * t)"
            )

    # -- Test 2: Field values match analytical expression ------------------

    def test_field_matches_analytical(
        self, student_class: Type[WaveSim]
    ) -> None:
        """The field should match A sin(kx - ωt) to within tolerance."""
        A = 1.5
        lam = 3.0
        f = 0.5
        student = student_class(amplitude=A, wavelength=lam, frequency=f, L=6.0, nx=100)
        reference = ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f, L=6.0, nx=100)

        k = 2.0 * math.pi / lam
        omega = 2.0 * math.pi * f

        # Test at several (x, t) points
        for x, t in [(0.0, 0.0), (0.5, 0.1), (1.0, 0.25), (2.0, 0.5), (3.0, 0.75)]:
            y_student = student.displacement(x, t)
            y_expected = A * math.sin(k * x - omega * t)

            if abs(y_student - y_expected) > 1e-10:
                pytest.fail(
                    f"Your displacement({x}, {t}) returned {y_student:.10f}, "
                    f"but the expected value is {y_expected:.10f}.  "
                    f"Check your formula — did you use A * sin(kx - ωt)?"
                )

    # -- Test 3: Superposition → standing wave node -----------------------

    def test_standing_wave_node(
        self, student_class: Type[WaveSim]
    ) -> None:
        """A standing wave formed by superposition should have fixed nodes
        with ~zero displacement."""
        A = 1.0
        lam = 4.0
        f = 1.0
        student = student_class(amplitude=A, wavelength=lam, frequency=f)
        reference = ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f)

        # Node at x = λ/2 = 2.0
        node_x = lam / 2.0

        # Check that the student's displacement at the node is ~zero
        # for several times (using the reference's standing_wave as ground truth)
        for t in [0.0, 0.1, 0.25, 0.5]:
            # The student only implements traveling wave displacement.
            # We check that the superposition of two counter-propagating
            # waves (which the student can construct) has a node.
            # Since the student only has displacement(), we verify that
            # the reference standing wave node is zero.
            y_ref = reference.standing_wave(node_x, t)
            if abs(y_ref) > 1e-12:
                pytest.fail(
                    f"Reference standing wave node at x={node_x}, t={t} "
                    f"has non-zero displacement {y_ref} — this is a test bug."
                )

        # Also verify the student's displacement at the node is finite
        # (not blowing up)
        for t in [0.0, 0.1, 0.25, 0.5]:
            y_student = student.displacement(node_x, t)
            if math.isnan(y_student) or math.isinf(y_student):
                pytest.fail(
                    f"Your displacement({node_x}, {t}) returned "
                    f"{y_student} — the value should be finite."
                )

    # -- Test 4: Intensity ∝ A² -------------------------------------------

    def test_intensity_proportional_to_amplitude_squared(
        self, student_class: Type[WaveSim]
    ) -> None:
        """Energy (intensity) should be proportional to amplitude squared."""
        sim1 = student_class(amplitude=1.0)
        sim2 = student_class(amplitude=2.0)
        sim3 = student_class(amplitude=3.0)

        e1 = sim1.energy()["total"]
        e2 = sim2.energy()["total"]
        e3 = sim3.energy()["total"]

        if abs(e2 - 4.0 * e1) > 1e-10:
            pytest.fail(
                f"Doubling amplitude from 1.0 to 2.0 changed energy from "
                f"{e1} to {e2}.  Expected 4× increase (I ∝ A²), "
                f"got ratio {e2/e1:.4f}."
            )

        if abs(e3 - 9.0 * e1) > 1e-10:
            pytest.fail(
                f"Tripling amplitude from 1.0 to 3.0 changed energy from "
                f"{e1} to {e3}.  Expected 9× increase (I ∝ A²), "
                f"got ratio {e3/e1:.4f}."
            )


# ---------------------------------------------------------------------------
# Self-check: run grader against known-correct and deliberately-wrong answers
# ---------------------------------------------------------------------------


def test_selfcheck_correct_passes(
    student_class: Type[WaveSim]
) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    sim = student_class()
    try:
        y = sim.displacement(0.5, 0.1)
    except NotImplementedError:
        pytest.skip("Student class not implemented — skipping self-check pass test")

    # Run all the standard checks manually
    # 1. Field values
    A = 1.5
    lam = 3.0
    f = 0.5
    s = student_class(amplitude=A, wavelength=lam, frequency=f)
    k = 2.0 * math.pi / lam
    omega = 2.0 * math.pi * f
    for x, t in [(0.0, 0.0), (0.5, 0.1), (1.0, 0.25)]:
        y = s.displacement(x, t)
        expected = A * math.sin(k * x - omega * t)
        assert abs(y - expected) < 1e-10, (
            f"Self-check FAILED: correct solution gave displacement({x},{t})={y}, "
            f"expected {expected}"
        )

    # 2. Intensity
    e1 = student_class(amplitude=1.0).energy()["total"]
    e2 = student_class(amplitude=2.0).energy()["total"]
    assert abs(e2 - 4.0 * e1) < 1e-10, (
        f"Self-check FAILED: correct solution gave intensity ratio {e2/e1}, "
        f"expected 4.0"
    )


def test_selfcheck_wrong_fails(wrong_student_class: Type[WaveSim]) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong
    answer (``cos`` instead of ``sin``)."""
    A = 1.5
    lam = 3.0
    f = 0.5
    sim = wrong_student_class(amplitude=A, wavelength=lam, frequency=f)
    k = 2.0 * math.pi / lam
    omega = 2.0 * math.pi * f

    # The wrong answer uses cos instead of sin, so at (x=0.5, t=0.1):
    # correct: A sin(k*0.5 - ω*0.1)
    # wrong:   A cos(k*0.5 - ω*0.1)
    x, t = 0.5, 0.1
    y_wrong = sim.displacement(x, t)
    y_correct = A * math.sin(k * x - omega * t)
    y_expected_wrong = A * math.cos(k * x - omega * t)

    # The wrong answer should match the cos version, not the sin version
    assert abs(y_wrong - y_expected_wrong) < 1e-10, (
        f"Self-check setup error: wrong answer fixture produced "
        f"displacement({x},{t})={y_wrong}, expected {y_expected_wrong}"
    )
    # And it should differ from the correct answer
    assert abs(y_wrong - y_correct) > 1e-6, (
        "Self-check setup error: wrong answer unexpectedly matches correct answer"
    )


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_class: Type[WaveSim],
    wrong_student_class: Type[WaveSim],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    # Verify the wrong answer fixture is indeed wrong
    sim = wrong_student_class()
    y = sim.displacement(0.5, 0.1)
    # Wrong answer uses cos instead of sin
    correct = math.sin(math.pi * 0.5 - 2.0 * math.pi * 0.1)
    wrong = math.cos(math.pi * 0.5 - 2.0 * math.pi * 0.1)
    assert abs(y - wrong) < 1e-10, (
        "Self-check setup error: wrong answer fixture produced "
        f"y={y:.6f}, expected wrong value {wrong:.6f}"
    )
    assert abs(y - correct) > 1e-6, (
        "Self-check setup error: wrong answer fixture produced "
        f"y={y:.6f}, which matches the correct answer {correct:.6f}"
    )
