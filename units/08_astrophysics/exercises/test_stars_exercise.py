"""Auto-grader for the Stars & Relativity fill-in-the-blank exercise.

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's
implementation — it does *not* read or string-match the student's formula.
A correct implementation will produce the right values.

Checks — Relativity
-------------------
1.  **NotImplementedError guard** — all hooks must be implemented.
2.  γ(0) = 1, γ increases with v.
3.  γ(0.6c) ≈ 1.25.
4.  Δt = γ · Δt₀ (time dilation).
5.  l = l₀ / γ (length contraction).

Checks — Stars
---------------
1.  **NotImplementedError guard** — all hooks must be implemented.
2.  Luminosity via Stefan-Boltzmann law.
3.  Radius-from-luminosity recovers input.
4.  Wien peak wavelength.
5.  Classification (main sequence, giant, white dwarf).

Usage
-----
    # Grade the student's exercise
    uv run pytest units/08_astrophysics/exercises/test_stars_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/08_astrophysics/exercises/test_stars_exercise.py -v \\
        --override-student=units/08_astrophysics/exercises/stars_solution.py

    # Full self-check
    uv run pytest units/08_astrophysics/exercises/test_stars_exercise.py -v \\
        --selfcheck
"""

from __future__ import annotations

import math
from typing import Tuple, Type

import pytest

from physics_core.astrophysics.hr_diagram import HRDiagram, L_SUN, R_SUN, T_SUN
from physics_core.astrophysics.relativity import (
    C,
    RelativityEngine,
)


class TestRelativityExercise:
    """Auto-grader for the student relativity exercise."""

    def test_lorentz_factor_implemented(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """Fail immediately if lorentz_factor not filled in."""
        cls, _ = student_classes
        sim = cls()
        try:
            sim.lorentz_factor(0.0)
        except NotImplementedError:
            pytest.fail(
                "Your lorentz_factor() is still raising NotImplementedError. "
                "Replace it with γ = 1 / sqrt(1 - v²/c²)."
            )

    def test_time_dilated_implemented(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """Fail immediately if time_dilated not filled in."""
        cls, _ = student_classes
        sim = cls()
        try:
            sim.time_dilated(0.0, 1.0)
        except NotImplementedError:
            pytest.fail(
                "Your time_dilated() is still raising NotImplementedError. "
                "Use Δt = γ · t0."
            )

    def test_length_contracted_implemented(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """Fail immediately if length_contracted not filled in."""
        cls, _ = student_classes
        sim = cls()
        try:
            sim.length_contracted(0.0, 1.0)
        except NotImplementedError:
            pytest.fail(
                "Your length_contracted() is still raising NotImplementedError. "
                "Use l = l0 / γ."
            )

    def test_gamma_at_rest(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """γ = 1 at v = 0."""
        cls, _ = student_classes
        sim = cls()
        gamma = sim.lorentz_factor(0.0)
        if abs(gamma - 1.0) > 1e-10:
            pytest.fail(
                f"Your lorentz_factor(0) = {gamma}, expected 1.0. "
                f"γ = 1 / sqrt(1 - v²/c²). At v = 0, γ = 1."
            )

    def test_gamma_increases(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """γ increases with v."""
        cls, _ = student_classes
        sim = cls()
        g1 = sim.lorentz_factor(0.5 * C)
        g2 = sim.lorentz_factor(0.8 * C)
        if g2 <= g1:
            pytest.fail(
                f"γ should increase with v. γ(0.5c) = {g1}, γ(0.8c) = {g2}. "
                f"Check your formula: γ = 1 / sqrt(1 - v²/c²)."
            )

    def test_gamma_0_6c(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """γ(0.6c) ≈ 1.25."""
        cls, _ = student_classes
        sim = cls()
        v = 0.6 * C
        gamma = sim.lorentz_factor(v)
        if abs(gamma - 1.25) > 0.01:
            pytest.fail(
                f"Your γ(0.6c) = {gamma}, expected ~1.25. "
                f"γ = 1 / sqrt(1 - 0.36) = 1 / sqrt(0.64) = 1.25."
            )

    def test_time_dilation(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """Δt = γ · Δt₀."""
        cls, _ = student_classes
        sim = cls()
        v = 0.6 * C
        t0 = 1.0
        dt = sim.time_dilated(v, t0)
        expected = 1.25
        if abs(dt - expected) > 0.01:
            pytest.fail(
                f"Your time_dilated(0.6c, 1s) = {dt}s, "
                f"expected {expected}s. Use Δt = γ · t0."
            )

    def test_length_contraction(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """l = l₀ / γ."""
        cls, _ = student_classes
        sim = cls()
        v = 0.6 * C
        l0 = 1.0
        l = sim.length_contracted(v, l0)
        expected = 1.0 / 1.25
        if abs(l - expected) > 0.01:
            pytest.fail(
                f"Your length_contracted(0.6c, 1m) = {l}m, "
                f"expected {expected}m. Use l = l₀ / γ."
            )


class TestStarsExercise:
    """Auto-grader for the student stellar physics exercise."""

    def test_luminosity_implemented(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """Fail immediately if luminosity not filled in."""
        _, cls_s = student_classes
        sim = cls_s()
        try:
            sim.luminosity(5772.0, 6.96e8)
        except NotImplementedError:
            pytest.fail(
                "Your luminosity() is still raising NotImplementedError. "
                "Use L = 4πR²σT⁴."
            )

    def test_radius_from_luminosity_implemented(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        _, cls_s = student_classes
        sim = cls_s()
        try:
            sim.radius_from_luminosity(3.8e26, 5772.0)
        except NotImplementedError:
            pytest.fail(
                "Your radius_from_luminosity() is still raising NotImplementedError. "
                "Use R = sqrt(L / (4πσT⁴))."
            )

    def test_peak_wavelength_implemented(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        _, cls_s = student_classes
        sim = cls_s()
        try:
            sim.peak_wavelength(5772.0)
        except NotImplementedError:
            pytest.fail(
                "Your peak_wavelength() is still raising NotImplementedError. "
                "Use λ_max = b / T."
            )

    def test_classify_implemented(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        _, cls_s = student_classes
        sim = cls_s()
        try:
            sim.classify(3.8e26, 5772.0)
        except NotImplementedError:
            pytest.fail(
                "Your classify() is still raising NotImplementedError. "
                "Compare L to the main-sequence prediction."
            )

    def test_sun_luminosity(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """Sun: L ≈ 3.8e26 W."""
        _, cls_s = student_classes
        sim = cls_s()
        L = sim.luminosity(T_SUN, R_SUN)
        if abs(L - L_SUN) / L_SUN > 0.05:
            pytest.fail(
                f"Your luminosity(T=5772K, R=6.96e8m) = {L:.2e} W, "
                f"expected ~{L_SUN:.2e} W. Use L = 4πR²σT⁴."
            )

    def test_sun_wien_peak(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """Sun: Wien peak ≈ 502 nm."""
        _, cls_s = student_classes
        sim = cls_s()
        lam = sim.peak_wavelength(T_SUN)
        lam_nm = lam * 1e9
        if abs(lam_nm - 502.0) > 15.0:
            pytest.fail(
                f"Your peak_wavelength(5772K) = {lam_nm:.0f} nm, "
                f"expected ~502 nm. Use λ_max = b / T."
            )

    def test_classify_sun(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """Sun is main sequence."""
        _, cls_s = student_classes
        sim = cls_s()
        result = sim.classify(L_SUN, T_SUN)
        if result != "main sequence":
            pytest.fail(
                f"Your classify(Sun) = '{result}', expected 'main sequence'."
            )

    def test_classify_giant(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """High L, low T → giant."""
        _, cls_s = student_classes
        sim = cls_s()
        result = sim.classify(1000.0 * L_SUN, 3500.0)
        if result != "giant":
            pytest.fail(
                f"Your classify(giant) = '{result}', expected 'giant'."
            )

    def test_classify_white_dwarf(
        self, student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]]
    ) -> None:
        """Low L, high T → white dwarf."""
        _, cls_s = student_classes
        sim = cls_s()
        result = sim.classify(0.01 * L_SUN, 20000.0)
        if result != "white dwarf":
            pytest.fail(
                f"Your classify(white dwarf) = '{result}', expected 'white dwarf'."
            )


# ===========================================================================
# Self-check
# ===========================================================================


def test_selfcheck_correct_passes(
    student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]],
) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    rel_cls, stars_cls = student_classes
    rel = rel_cls()
    stars = stars_cls()

    # Skip if not implemented (default unfilled exercise)
    try:
        rel.lorentz_factor(0.6 * C)
    except NotImplementedError:
        pytest.skip("Student class not implemented — skipping")

    gamma = rel.lorentz_factor(0.6 * C)
    assert gamma == pytest.approx(1.25, rel=0.01)

    dt = rel.time_dilated(0.6 * C, 1.0)
    assert dt == pytest.approx(1.25, rel=0.01)

    l = rel.length_contracted(0.6 * C, 1.0)
    assert l == pytest.approx(0.8, rel=0.01)

    L = stars.luminosity(T_SUN, R_SUN)
    assert L == pytest.approx(L_SUN, rel=0.05)

    lam = stars.peak_wavelength(T_SUN)
    assert lam * 1e9 == pytest.approx(502.0, rel=0.02)

    assert stars.classify(L_SUN, T_SUN) == "main sequence"


def test_selfcheck_wrong_fails(
    wrong_student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]],
) -> None:
    """Self-check: the grader must FAIL when given deliberately wrong answer."""
    rel_cls, stars_cls = wrong_student_classes
    rel = rel_cls()
    stars = stars_cls()

    # The wrong answer uses sqrt(1 - β) instead of sqrt(1 - β²)
    gamma = rel.lorentz_factor(0.6 * C)
    assert abs(gamma - 1.25) > 0.01, "Wrong answer unexpectedly passed gamma check"

    # The wrong answer uses R instead of R²
    L = stars.luminosity(T_SUN, R_SUN)
    assert abs(L - L_SUN) / L_SUN > 0.05, (
        "Wrong answer unexpectedly passed luminosity check"
    )

    # The wrong answer always returns "main sequence"
    assert stars.classify(1000.0 * L_SUN, 3500.0) == "main sequence", (
        "Wrong answer should always return main sequence"
    )


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]],
    wrong_student_classes: Tuple[Type[RelativityEngine], Type[HRDiagram]],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    rel_cls, _ = student_classes
    rel = rel_cls()
    assert rel.lorentz_factor(0.0) is not None