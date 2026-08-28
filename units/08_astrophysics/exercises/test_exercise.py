"""Auto-grader for the Astrophysics fill-in-the-blank exercise.

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's
implementation — it does *not* read or string-match the student's formula.
A correct implementation of the four hooks will produce the right observed
frequency, redshift, recovered velocity, and Hubble velocity.  A wrong
implementation will fail one or more of these checks.

Checks
------
1.  **NotImplementedError guard** — if the student hasn't filled in the
    hooks, fail immediately with a clear message.
2.  **Redshift velocity** — ``velocity_from_z(z)`` recovers the input
    velocity of ``redshift(v)`` to within 1%.
3.  **Hubble velocity** — ``v = H0 * d`` to within 1%.
4.  **Blueshift / redshift direction** — approaching gives higher frequency,
    receding gives lower frequency.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/08_astrophysics/exercises/test_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/08_astrophysics/exercises/test_exercise.py -v \
        --override-student=units/08_astrophysics/exercises/astrophysics_solution.py

    # Full self-check
    uv run pytest units/08_astrophysics/exercises/test_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

import math
from typing import Type

import pytest

from physics_core.astrophysics.doppler import H0, C, DopplerShift


class TestDopplerShiftExercise:
    """Auto-grader for the student Doppler shift exercise."""

    def test_physics_implemented(
        self, student_class: Type[DopplerShift]
    ) -> None:
        """Fail immediately if the student hasn't filled in the hooks."""
        sim = student_class()
        try:
            sim.observed_frequency(1000.0)
        except NotImplementedError:
            pytest.fail(
                "Your observed_frequency() method is still raising "
                "NotImplementedError.  Replace the 'raise' line with the "
                "relativistic Doppler formula: "
                "f_obs = f0 * sqrt((1-β)/(1+β))."
            )
        try:
            sim.redshift(1000.0)
        except NotImplementedError:
            pytest.fail(
                "Your redshift() method is still raising NotImplementedError. "
                "Replace the 'raise' line with z = sqrt((1+β)/(1-β)) - 1."
            )
        try:
            sim.velocity_from_z(0.1)
        except NotImplementedError:
            pytest.fail(
                "Your velocity_from_z() method is still raising "
                "NotImplementedError.  Replace the 'raise' line with the "
                "relativistic inverse: v = c * ((z+1)^2 - 1) / ((z+1)^2 + 1)."
            )
        try:
            sim.hubble_velocity(10.0)
        except NotImplementedError:
            pytest.fail(
                "Your hubble_velocity() method is still raising "
                "NotImplementedError.  Replace the 'raise' line with "
                "Hubble's law: v = H0 * d."
            )

    def test_observed_frequency_redshift(
        self, student_class: Type[DopplerShift]
    ) -> None:
        """Receding source → f_obs < f0 (redshift)."""
        sim = student_class()
        f_obs = sim.observed_frequency(1000.0)
        if f_obs >= sim.f0:
            pytest.fail(
                f"Your observed_frequency at v = +1000 m/s is {f_obs:.4e} Hz, "
                f"but a receding source should give f_obs < f0 = {sim.f0:.4e} Hz "
                f"(redshift)."
            )

    def test_observed_frequency_blueshift(
        self, student_class: Type[DopplerShift]
    ) -> None:
        """Approaching source → f_obs > f0 (blueshift)."""
        sim = student_class()
        f_obs = sim.observed_frequency(-1000.0)
        if f_obs <= sim.f0:
            pytest.fail(
                f"Your observed_frequency at v = -1000 m/s is {f_obs:.4e} Hz, "
                f"but an approaching source should give f_obs > f0 = {sim.f0:.4e} Hz "
                f"(blueshift)."
            )

    def test_redshift_matches_low_velocity_approx(
        self, student_class: Type[DopplerShift]
    ) -> None:
        """For small v, z ≈ v/c within 5%."""
        sim = student_class()
        v = 1000.0  # 1 km/s, << c
        z = sim.redshift(v)
        expected_approx = v / C
        if abs(z - expected_approx) / expected_approx > 0.05:
            pytest.fail(
                f"Your redshift at v = 1000 m/s is {z:.6e}, "
                f"but the low-velocity approximation gives z ≈ v/c = {expected_approx:.6e}. "
                f"Check your redshift() formula: z = sqrt((1+β)/(1-β)) - 1."
            )

    def test_velocity_from_z_recovers_input(
        self, student_class: Type[DopplerShift]
    ) -> None:
        """velocity_from_z(redshift(v)) ≈ v (round-trip within 1%)."""
        sim = student_class()
        v_original = 1e7  # 0.033c — moderately relativistic
        z = sim.redshift(v_original)
        v_recovered = sim.velocity_from_z(z)
        if abs(v_recovered - v_original) / v_original > 0.01:
            pytest.fail(
                f"velocity_from_z should recover the original velocity. "
                f"redshift(v={v_original:.1f}) gave z = {z:.6f}, but "
                f"velocity_from_z(z) returned {v_recovered:.1f} m/s "
                f"(expected ~{v_original:.1f}, 1% tolerance)."
            )

    def test_hubble_velocity(
        self, student_class: Type[DopplerShift]
    ) -> None:
        """v = H0 * d within 1%."""
        sim = student_class()
        d = 10.0  # Mpc
        v = sim.hubble_velocity(d)
        expected = H0 * d
        if abs(v - expected) / expected > 0.01:
            pytest.fail(
                f"Your hubble_velocity for d = {d} Mpc is {v:.4f} km/s, "
                f"expected {expected:.4f} km/s (H0 = {H0} km/s/Mpc). "
                f"Check your formula: v = H0 * d."
            )

    def test_hubble_velocity_custom_h0(
        self, student_class: Type[DopplerShift]
    ) -> None:
        """Custom H0: v = H0 * d within 1%."""
        sim = student_class()
        v = sim.hubble_velocity(5.0, H0=70.0)
        expected = 70.0 * 5.0
        if abs(v - expected) / expected > 0.01:
            pytest.fail(
                f"Your hubble_velocity with H0 = 70 for d = 5 Mpc is {v:.4f} km/s, "
                f"expected {expected:.4f} km/s."
            )


# ===========================================================================
# Self-check
# ===========================================================================


def test_selfcheck_correct_passes(student_class: Type[DopplerShift]) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    sim = student_class()

    # Skip if not implemented (default unfilled exercise)
    try:
        sim.observed_frequency(1000.0)
    except NotImplementedError:
        pytest.skip("Student class not implemented — skipping")

    f_obs = sim.observed_frequency(1000.0)
    assert f_obs < sim.f0  # receding → redshift

    z = sim.redshift(1000.0)
    assert z == pytest.approx(1000.0 / C, rel=0.05)

    v_recovered = sim.velocity_from_z(z)
    assert v_recovered == pytest.approx(1000.0, rel=0.01)

    v_hubble = sim.hubble_velocity(10.0)
    assert v_hubble == pytest.approx(H0 * 10.0, rel=0.01)


def test_selfcheck_wrong_fails(wrong_student_class: Type[DopplerShift]) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong answer."""
    sim = wrong_student_class()

    # The wrong answer's hubble_velocity is double the correct value
    v_hubble = sim.hubble_velocity(10.0)
    assert abs(v_hubble - H0 * 10.0) > 0.01 * H0 * 10.0, (
        "Wrong answer unexpectedly passed Hubble check"
    )

    z = sim.redshift(1000.0)
    assert z != pytest.approx(1000.0 / C, rel=0.05), (
        "Wrong answer unexpectedly passed redshift check"
    )


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_class: Type[DopplerShift],
    wrong_student_class: Type[DopplerShift],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    sim = student_class()
    a = sim.observed_frequency(0.0)
    assert a is not None, "observed_frequency() should return a number"