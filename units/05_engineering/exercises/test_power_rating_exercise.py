"""Auto-grader for the domestic electricity exercise.

Checks
------
1. Operating current I = P/V
2. Fuse rating selection (3A, 5A, 13A)
3. Energy in kWh
4. Cost calculation
"""

from __future__ import annotations

from typing import Type

import pytest


class TestPowerRatingExercise:
    """Auto-grader for the power rating exercise."""

    def test_physics_implemented(self, pr_student_class: Type) -> None:
        """Fail immediately if hooks are not implemented."""
        sim = pr_student_class()
        method_args = {
            "operating_current": (100, 230),
            "fuse_rating": (5.0,),
            "energy_kwh": (100, 2.0),
            "cost": (4.0, 1.20),
        }
        for method, args in method_args.items():
            try:
                getattr(sim, method)(*args)
            except NotImplementedError:
                pytest.fail(f"Your {method}() is still raising NotImplementedError.")

    def test_operating_current(self, pr_student_class: Type) -> None:
        """I = P / V."""
        sim = pr_student_class()
        # 2000 W hair dryer at 230 V
        i = sim.operating_current(2000.0, 230.0)
        expected = 2000.0 / 230.0
        assert abs(i - expected) / expected < 0.01, \
            f"operating_current: {i} vs {expected}"

    def test_operating_current_zero_voltage(self, pr_student_class: Type) -> None:
        """Handle zero voltage gracefully."""
        sim = pr_student_class()
        i = sim.operating_current(100.0, 0.0)
        assert i == 0.0, "Should return 0 for zero voltage"

    def test_fuse_rating_3a(self, pr_student_class: Type) -> None:
        """Appliance drawing < 3A should use 3A fuse."""
        sim = pr_student_class()
        i = sim.operating_current(500.0, 230.0)
        assert sim.fuse_rating(i) == 3.0, \
            f"500W at 230V (I={i:.3f}A) should use 3A fuse"

    def test_fuse_rating_5a(self, pr_student_class: Type) -> None:
        """Appliance drawing between 3A and 5A should use 5A fuse."""
        sim = pr_student_class()
        i = sim.operating_current(1000.0, 230.0)
        assert sim.fuse_rating(i) == 5.0, \
            f"1000W at 230V (I={i:.3f}A) should use 5A fuse"

    def test_fuse_rating_13a(self, pr_student_class: Type) -> None:
        """Appliance drawing between 5A and 13A should use 13A fuse."""
        sim = pr_student_class()
        i = sim.operating_current(2000.0, 230.0)
        assert sim.fuse_rating(i) == 13.0, \
            f"2000W at 230V (I={i:.3f}A) should use 13A fuse"

    def test_energy_kwh(self, pr_student_class: Type) -> None:
        """E = P * t / 1000."""
        sim = pr_student_class()
        # 2000 W for 2 hours = 4 kWh
        e = sim.energy_kwh(2000.0, 2.0)
        assert e == pytest.approx(4.0, rel=0.01), f"energy_kwh: {e} vs 4.0"

    def test_cost(self, pr_student_class: Type) -> None:
        """Cost = energy_kwh * rate."""
        sim = pr_student_class()
        # 4 kWh at $1.20/kWh = $4.80
        c = sim.cost(4.0, 1.20)
        assert c == pytest.approx(4.80, rel=0.01), f"cost: {c} vs 4.80"


# ===========================================================================
# Self-check
# ===========================================================================


def test_pr_selfcheck_correct_passes(pr_student_class: Type) -> None:
    """Self-check: grader must PASS with correct solution."""
    sim = pr_student_class()
    i = sim.operating_current(2000.0, 230.0)
    assert i == pytest.approx(2000.0 / 230.0, rel=0.01)
    assert sim.fuse_rating(i) == 13.0


def test_pr_selfcheck_wrong_fails(pr_wrong_student_class: Type) -> None:
    """Self-check: grader must FAIL with deliberately wrong answer."""
    sim = pr_wrong_student_class()
    i = sim.operating_current(2000.0, 230.0)
    assert i != pytest.approx(2000.0 / 230.0, rel=0.01), \
        "Wrong answer should not match"


def test_pr_selfcheck_runner(
    request: pytest.FixtureRequest,
    pr_student_class: Type,
    pr_wrong_student_class: Type,
) -> None:
    """Full self-check when --selfcheck is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")