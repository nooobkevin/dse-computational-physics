"""Auto-grader for the Orbital mechanics fill-in-the-blank exercise.

Checks
------
1.  **NotImplementedError guard** — if the student hasn't filled in the hooks.
2.  **Gravitational force** — F = G M m / r².
3.  **Orbital velocity** — v = √(G M / r).
4.  **Escape velocity** — v_esc = √(2 G M / r) = √2 · v_orb.
5.  **Gravitational potential energy** — U = -G M m / r.
6.  **Total energy** — E = ½ m v² - G M m / r.
"""

from __future__ import annotations

import math
from typing import Type

import pytest

from physics_core.engineering.orbital import OrbitSim

G = 6.67430e-11
M = 5.972e24
m = 1000.0


class TestOrbitalExercise:
    """Auto-grader for the student orbital exercise."""

    def test_physics_implemented(self, orb_student_class: Type[OrbitSim]) -> None:
        """Fail immediately if the student hasn't filled in the hooks."""
        sim = orb_student_class(M=M, m=m)
        for hook_name, args in [
            ("gravitational_force", (7e6,)),
            ("orbital_velocity", (7e6,)),
            ("escape_velocity", (7e6,)),
            ("gravitational_potential_energy", (7e6,)),
            ("total_energy", (7e6, 7540.0)),
        ]:
            try:
                getattr(sim, hook_name)(*args)
            except NotImplementedError:
                pytest.fail(f"Your {hook_name}() is still raising NotImplementedError.")

    def test_gravitational_force(self, orb_student_class: Type[OrbitSim]) -> None:
        """F = G M m / r²."""
        sim = orb_student_class(M=M, m=m)
        r = 7.0e6
        expected = G * M * m / (r * r)
        actual = sim.gravitational_force(r)
        rel_err = abs(actual - expected) / expected
        assert rel_err < 0.01, f"gravitational_force: {actual} vs expected {expected}"

    def test_orbital_velocity(self, orb_student_class: Type[OrbitSim]) -> None:
        """v = √(G M / r)."""
        sim = orb_student_class(M=M, m=m)
        r = 7.0e6
        expected = math.sqrt(G * M / r)
        actual = sim.orbital_velocity(r)
        rel_err = abs(actual - expected) / expected
        assert rel_err < 0.01, f"orbital_velocity: {actual} vs expected {expected}"

    def test_escape_velocity(self, orb_student_class: Type[OrbitSim]) -> None:
        """v_esc = √(2 G M / r) = √2 · v_orb."""
        sim = orb_student_class(M=M, m=m)
        r = 7.0e6
        v_orb = sim.orbital_velocity(r)
        v_esc = sim.escape_velocity(r)
        ratio = v_esc / v_orb if v_orb != 0 else 0
        assert abs(ratio - math.sqrt(2)) < 0.02, \
            f"v_esc/v_orb = {ratio}, expected √2 ≈ {math.sqrt(2):.4f}"

    def test_gpe(self, orb_student_class: Type[OrbitSim]) -> None:
        """U = -G M m / r."""
        sim = orb_student_class(M=M, m=m)
        r = 7.0e6
        expected = -G * M * m / r
        actual = sim.gravitational_potential_energy(r)
        rel_err = abs(actual - expected) / abs(expected)
        assert rel_err < 0.01, f"gravitational_potential_energy: {actual} vs {expected}"

    def test_total_energy_circular(self, orb_student_class: Type[OrbitSim]) -> None:
        """E_total = -G M m / (2r) for circular orbit."""
        sim = orb_student_class(M=M, m=m)
        r = 7.0e6
        v = sim.orbital_velocity(r)
        total = sim.total_energy(r, v)
        expected = -G * M * m / (2.0 * r)
        rel_err = abs(total - expected) / abs(expected)
        assert rel_err < 0.02, f"total_energy: {total} vs expected {expected}"

    def test_ke_gpe_ratio(self, orb_student_class: Type[OrbitSim]) -> None:
        """KE = -½ GPE for circular orbit."""
        sim = orb_student_class(M=M, m=m)
        r = 7.0e6
        v = sim.orbital_velocity(r)
        ke = 0.5 * m * v * v
        gpe = sim.gravitational_potential_energy(r)
        ratio = ke / gpe
        assert abs(ratio - (-0.5)) < 0.02, \
            f"KE/GPE = {ratio}, expected -0.5"


# ===========================================================================
# Self-check
# ===========================================================================


def test_orb_selfcheck_correct_passes(
    orb_student_class: Type[OrbitSim],
) -> None:
    """Self-check: grader must PASS with correct solution."""
    sim = orb_student_class(M=M, m=m)
    r = 7.0e6
    f = sim.gravitational_force(r)
    expected_f = G * M * m / (r * r)
    assert f == pytest.approx(expected_f, rel=0.01)


def test_orb_selfcheck_wrong_fails(
    orb_wrong_student_class: Type[OrbitSim],
) -> None:
    """Self-check: grader must FAIL with deliberately wrong answer."""
    sim = orb_wrong_student_class(M=M, m=m)
    r = 7.0e6
    f = sim.gravitational_force(r)
    expected_f = G * M * m / (r * r)
    # Wrong answer uses F = GMm/r instead of GMm/r²
    assert f != pytest.approx(expected_f, rel=0.01), "Wrong answer should not match"


def test_orb_selfcheck_runner(
    request: pytest.FixtureRequest,
    orb_student_class: Type[OrbitSim],
    orb_wrong_student_class: Type[OrbitSim],
) -> None:
    """Orchestrate full self-check when --selfcheck is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")