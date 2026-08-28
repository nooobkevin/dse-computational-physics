"""Auto-grader for the quantum well fill-in-the-blank exercise.

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's
implementation — it does *not* read or string-match the student's formula.
A correct implementation of ``energy_level`` will produce the right energy
values and wavefunctions.  A wrong implementation will fail one or more of
these checks with a specific, human-readable message.

Checks
------
1. **NotImplementedError guard** — if the student hasn't filled in the hook,
   fail immediately with a clear message.
2. **E₁ energy level** — E₁ = h² / (8 m L²) must match the formula.
3. **E₂ / E₁ ratio** — E₂ must equal 4 × E₁ (n² scaling).
4. **Wavefunction at centre** — ψ₁(L/2) = √(2/L) must be correct.
5. **Probability density integration** — ∫|ψ|² dx ≈ 1.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/07_quantum/exercises/test_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/07_quantum/exercises/test_exercise.py -v \
        --override-student=units/07_quantum/exercises/quantum_solution.py

    # Full self-check: verify grader passes correct answer AND catches wrong one
    uv run pytest units/07_quantum/exercises/test_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Type

import pytest

from physics_core.quantum.wavefunctions import H, M_E, QuantumWell, ReferenceQuantumWell


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
L = 1e-10  # well width (m)
MASS = M_E  # particle mass


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestQuantumWellExercise:
    """Auto-grader for the student quantum well exercise."""

    # -- Test 1: NotImplementedError guard ---------------------------------

    def test_physics_implemented(self, student_class: Type[QuantumWell]) -> None:
        """Fail immediately if the student hasn't filled in the hook."""
        sim = student_class(L=L, m=MASS)
        try:
            sim.energy_level(1)
        except NotImplementedError:
            pytest.fail(
                "Your energy_level method is still raising "
                "NotImplementedError.  Replace the 'raise' line with the "
                "correct physics formula:  "
                "return (n * n * H * H) / (8.0 * self.m * self.L * self.L)"
            )

    # -- Test 2: E₁ energy level ------------------------------------------

    def test_energy_level_n1(self, student_class: Type[QuantumWell]) -> None:
        """E₁ = h² / (8 m L²)"""
        sim = student_class(L=L, m=MASS)
        e1 = sim.energy_level(1)
        expected = (1 * 1 * H * H) / (8.0 * MASS * L * L)

        rel_err = abs(e1 - expected) / expected
        if rel_err > 0.001:
            pytest.fail(
                f"Your E₁ energy level is {e1:.4e} J, but the expected "
                f"value is {expected:.4e} J (relative error "
                f"{rel_err*100:.2f}%).  "
                f"Check your formula: E_n = n² h² / (8 m L²)"
            )

    # -- Test 3: E₂ / E₁ ratio --------------------------------------------

    def test_energy_level_ratio(self, student_class: Type[QuantumWell]) -> None:
        """E₂ must equal 4 × E₁ (n² scaling)."""
        sim = student_class(L=L, m=MASS)
        e1 = sim.energy_level(1)
        e2 = sim.energy_level(2)

        ratio = e2 / e1
        if abs(ratio - 4.0) > 0.01:
            pytest.fail(
                f"E₂ / E₁ = {ratio:.4f}, but expected 4.0 (since "
                f"E_n ∝ n²).  Your energy_level formula may not be "
                f"using n² correctly."
            )

    # -- Test 4: Wavefunction at centre -----------------------------------

    def test_wavefunction_at_centre(self, student_class: Type[QuantumWell]) -> None:
        """ψ₁(L/2) = √(2/L)"""
        sim = student_class(L=L, m=MASS)
        try:
            psi = sim.wavefunction(L / 2.0, 1)
        except NotImplementedError:
            pytest.skip("wavefunction not overridden — using base class default")

        expected = math.sqrt(2.0 / L)
        rel_err = abs(psi - expected) / expected
        if rel_err > 0.001:
            pytest.fail(
                f"Your ψ₁(L/2) = {psi:.4e}, but the expected value "
                f"is √(2/L) = {expected:.4e} (relative error "
                f"{rel_err*100:.2f}%)."
            )

    # -- Test 5: Probability density integration --------------------------

    def test_probability_integrates_to_one(
        self, student_class: Type[QuantumWell]
    ) -> None:
        """∫₀ᴸ |ψ_n(x)|² dx ≈ 1"""
        sim = student_class(L=L, m=MASS)
        try:
            # Use the base class probability_density which calls wavefunction
            n_steps = 500
            dx = L / n_steps
            total = 0.0
            for i in range(n_steps):
                x = (i + 0.5) * dx
                total += sim.probability_density(x, 1) * dx
        except NotImplementedError:
            pytest.skip("wavefunction not overridden — skipping integration test")

        if abs(total - 1.0) > 0.05:
            pytest.fail(
                f"∫₀ᴸ |ψ₁(x)|² dx = {total:.4f}, but expected ~1.0.  "
                f"The wavefunction may not be correctly normalised."
            )


# ---------------------------------------------------------------------------
# Self-check: run grader against known-correct and deliberately-wrong answers
# ---------------------------------------------------------------------------


def test_selfcheck_correct_passes(
    student_class: Type[QuantumWell]
) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    sim = student_class(L=L, m=MASS)
    try:
        e1 = sim.energy_level(1)
    except NotImplementedError:
        pytest.skip("Student class not implemented — skipping self-check pass test")

    expected = (H * H) / (8.0 * MASS * L * L)
    rel_err = abs(e1 - expected) / expected
    assert rel_err <= 0.001, (
        f"Self-check FAILED: correct solution gave E₁ error "
        f"{rel_err*100:.2f}% (E₁={e1:.4e}, expected {expected:.4e})"
    )

    e2 = sim.energy_level(2)
    ratio = e2 / e1
    assert abs(ratio - 4.0) <= 0.01, (
        f"Self-check FAILED: correct solution gave E₂/E₁ = {ratio:.4f}"
    )

    # Wavefunction check
    try:
        psi = sim.wavefunction(L / 2.0, 1)
        expected_psi = math.sqrt(2.0 / L)
        assert abs(psi - expected_psi) <= 0.001 * expected_psi, (
            f"Self-check FAILED: correct solution gave wrong wavefunction"
        )
    except NotImplementedError:
        pass


def test_selfcheck_wrong_fails(wrong_student_class: Type[QuantumWell]) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong
    answer (``E_n = n * h² / (8 m L²)`` instead of ``n²``)."""
    params = {"L": L, "m": MASS}
    sim = wrong_student_class(**params)

    # The wrong answer uses n instead of n², so E₁ is correct but E₂ is half
    e1 = sim.energy_level(1)
    e2 = sim.energy_level(2)

    expected_e2 = (4 * H * H) / (8.0 * MASS * L * L)
    rel_err = abs(e2 - expected_e2) / expected_e2
    assert rel_err > 0.01, (
        f"Self-check FAILED: wrong answer unexpectedly passed energy check "
        f"(E₂={e2:.4e}, expected={expected_e2:.4e}, error={rel_err*100:.2f}%)"
    )


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_class: Type[QuantumWell],
    wrong_student_class: Type[QuantumWell],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    # When --selfcheck is used without --override-student, load the solution
    import importlib.util
    exercises_dir = Path(__file__).parent
    conftest_path = exercises_dir / "conftest.py"
    spec = importlib.util.spec_from_file_location("_conftest_loader", str(conftest_path))
    conftest_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conftest_mod)
    _load_student_class_from_path = conftest_mod._load_student_class_from_path

    solution_path = exercises_dir / "quantum_solution.py"
    if not solution_path.exists():
        pytest.skip("quantum_solution.py not found — skipping self-check")

    correct_cls = _load_student_class_from_path(str(solution_path))

    # Verify correct solution passes
    sim = correct_cls(L=L, m=MASS)
    e1 = sim.energy_level(1)
    expected = (H * H) / (8.0 * MASS * L * L)
    rel_err = abs(e1 - expected) / expected
    assert rel_err <= 0.001, (
        f"Self-check FAILED: correct solution gave E₁ error "
        f"{rel_err*100:.2f}%"
    )

    # Verify wrong answer fails
    wrong_sim = wrong_student_class(L=L, m=MASS)
    e2_wrong = wrong_sim.energy_level(2)
    expected_e2 = (4 * H * H) / (8.0 * MASS * L * L)
    rel_err_wrong = abs(e2_wrong - expected_e2) / expected_e2
    assert rel_err_wrong > 0.01, (
        f"Self-check FAILED: wrong answer unexpectedly passed "
        f"(E₂ error {rel_err_wrong*100:.2f}%)"
    )