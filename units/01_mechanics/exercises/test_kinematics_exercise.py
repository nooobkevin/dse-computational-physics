"""Auto-grader for the kinematics fill-in-the-blank exercise.

Grading philosophy
------------------
This grader measures the **numerical correctness** of the student's
SUVAT implementations — it does not read or string-match the formulas.
A correct implementation will produce the right values for all SUVAT
quantities; a wrong one will fail one or more checks.

Checks
------
1. **NotImplementedError guard** for each method
2. **velocity_after** — v = u + at at various (u, a, t)
3. **displacement** — s = ut + ½at²
4. **displacement_from_uv** — s = ½(u+v)t
5. **final_velocity_sq** — v² = u² + 2as
6. **acceleration_from_graph** — a = Δv/Δt

Usage
-----
    uv run pytest units/01_mechanics/exercises/test_kinematics_exercise.py -v
"""

from __future__ import annotations

from typing import Any, Type

import pytest


# ---------------------------------------------------------------------------
# Helpers to load student class
# ---------------------------------------------------------------------------

def _load_student_class() -> Type[Any]:
    """Import StudentKinematics from the exercise file."""
    import importlib.util
    import sys
    from pathlib import Path

    path = Path(__file__).parent / "kinematics_exercise.py"
    spec = importlib.util.spec_from_file_location("_kinematics_student", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_kinematics_student"] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, "StudentKinematics", None)
    if cls is None:
        raise AttributeError(f"{path} does not define StudentKinematics")
    return cls


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def kinematics_class() -> Type[Any]:
    """Return the StudentKinematics class under test."""
    return _load_student_class()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestKinematicsExercise:
    """Auto-grader for the student kinematics exercise."""

    def test_velocity_after_implemented(self, kinematics_class: Type[Any]) -> None:
        sim = kinematics_class(u=5.0, a=2.0)
        try:
            sim.velocity_after(3.0)
        except NotImplementedError:
            pytest.fail(
                "Your velocity_after method is still raising NotImplementedError. "
                "Replace it with: return self.u + self.a * t"
            )

    def test_displacement_implemented(self, kinematics_class: Type[Any]) -> None:
        sim = kinematics_class(u=5.0, a=2.0)
        try:
            sim.displacement(3.0)
        except NotImplementedError:
            pytest.fail(
                "Your displacement method is still raising NotImplementedError. "
                "Replace it with: return self.u * t + 0.5 * self.a * t * t"
            )

    def test_displacement_from_uv_implemented(
        self, kinematics_class: Type[Any],
    ) -> None:
        sim = kinematics_class(u=5.0, a=2.0)
        try:
            sim.displacement_from_uv(11.0, 3.0)
        except NotImplementedError:
            pytest.fail(
                "Your displacement_from_uv method is still raising NotImplementedError."
            )

    def test_final_velocity_sq_implemented(
        self, kinematics_class: Type[Any],
    ) -> None:
        sim = kinematics_class(u=5.0, a=2.0)
        try:
            sim.final_velocity_sq(24.0)
        except NotImplementedError:
            pytest.fail(
                "Your final_velocity_sq method is still raising NotImplementedError."
            )

    def test_acceleration_from_graph_implemented(
        self, kinematics_class: Type[Any],
    ) -> None:
        sim = kinematics_class()
        try:
            sim.acceleration_from_graph(10.0, 20.0, 0.0, 5.0)
        except NotImplementedError:
            pytest.fail(
                "Your acceleration_from_graph is still raising NotImplementedError."
            )

    def test_velocity_after_correct(self, kinematics_class: Type[Any]) -> None:
        """v = u + at for various parameter sets."""
        test_cases = [
            (0.0, 9.81, 2.0, 19.62),
            (5.0, 2.0, 3.0, 11.0),
            (10.0, -9.81, 1.0, 0.19),
            (0.0, 0.0, 100.0, 0.0),
        ]
        for u, a, t, expected in test_cases:
            sim = kinematics_class(u=u, a=a)
            result = sim.velocity_after(t)
            assert abs(result - expected) < 1e-9, (
                f"velocity_after(u={u}, a={a}, t={t}) = {result}, "
                f"expected {expected}"
            )

    def test_displacement_correct(self, kinematics_class: Type[Any]) -> None:
        """s = ut + ½at²."""
        test_cases = [
            (0.0, 9.81, 2.0, 19.62),
            (5.0, 2.0, 3.0, 24.0),
            (10.0, -9.81, 1.0, 5.095),
            (0.0, 0.0, 100.0, 0.0),
        ]
        for u, a, t, expected in test_cases:
            sim = kinematics_class(u=u, a=a)
            result = sim.displacement(t)
            assert abs(result - expected) < 1e-9, (
                f"displacement(u={u}, a={a}, t={t}) = {result}, "
                f"expected {expected}"
            )

    def test_displacement_from_uv_correct(
        self, kinematics_class: Type[Any],
    ) -> None:
        """s = ½(u+v)t."""
        test_cases = [
            (0.0, 19.62, 2.0, 19.62),
            (5.0, 11.0, 3.0, 24.0),
            (10.0, 0.19, 1.0, 5.095),
        ]
        for u, v, t, expected in test_cases:
            sim = kinematics_class(u=u, a=0.0)
            result = sim.displacement_from_uv(v, t)
            assert abs(result - expected) < 1e-9, (
                f"displacement_from_uv(u={u}, v={v}, t={t}) = {result}, "
                f"expected {expected}"
            )

    def test_final_velocity_sq_correct(
        self, kinematics_class: Type[Any],
    ) -> None:
        """v² = u² + 2as."""
        test_cases = [
            (0.0, 9.81, 19.62, 384.9444),
            (5.0, 2.0, 24.0, 121.0),
            (10.0, -9.81, 5.095, 0.0361),
        ]
        for u, a, s, expected in test_cases:
            sim = kinematics_class(u=u, a=a)
            result = sim.final_velocity_sq(s)
            assert abs(result - expected) < 1e-9, (
                f"final_velocity_sq(u={u}, a={a}, s={s}) = {result}, "
                f"expected {expected}"
            )

    def test_acceleration_from_graph_correct(
        self, kinematics_class: Type[Any],
    ) -> None:
        """a = Δv / Δt."""
        test_cases = [
            (10.0, 20.0, 0.0, 5.0, 2.0),
            (0.0, 9.81, 0.0, 1.0, 9.81),
            (50.0, 0.0, 0.0, 10.0, -5.0),
        ]
        for v1, v2, t1, t2, expected in test_cases:
            sim = kinematics_class()
            result = sim.acceleration_from_graph(v1, v2, t1, t2)
            assert abs(result - expected) < 1e-9, (
                f"acceleration_from_graph(v1={v1}, v2={v2}, t1={t1}, t2={t2}) = "
                f"{result}, expected {expected}"
            )


# ---------------------------------------------------------------------------
# Self-check: run grader against known-correct and wrong answers
# ---------------------------------------------------------------------------

def test_selfcheck_kinematics_correct_passes(kinematics_class: Type[Any]) -> None:
    """Self-check: grader must PASS when given the correct solution."""
    sim = kinematics_class(u=5.0, a=2.0)
    # velocity_after
    v = sim.velocity_after(3.0)
    assert abs(v - 11.0) < 1e-9, f"velocity_after gave {v}, expected 11.0"
    # displacement
    s = sim.displacement(3.0)
    assert abs(s - 24.0) < 1e-9, f"displacement gave {s}, expected 24.0"


def test_selfcheck_kinematics_wrong_fails() -> None:
    """Self-check: grader must FAIL for a deliberately wrong answer."""

    class WrongKinematics:
        def __init__(self, u: float = 0.0, a: float = 9.81) -> None:
            self.u = u
            self.a = a

        def velocity_after(self, t: float) -> float:
            # WRONG: uses u + a + t instead of u + a*t
            return self.u + self.a + t

        def displacement(self, t: float) -> float:
            # WRONG: missing ½
            return self.u * t + self.a * t * t

        def displacement_from_uv(self, v: float, t: float) -> float:
            return 0.5 * (self.u + v) * t  # correct

        def final_velocity_sq(self, s: float) -> float:
            return self.u * self.u + 2.0 * self.a * s  # correct

        def acceleration_from_graph(
            self, v1: float, v2: float, t1: float, t2: float
        ) -> float:
            return (v2 - v1) / (t2 - t1)  # correct

    wrong = WrongKinematics(u=5.0, a=2.0)
    # velocity_after should be 11.0 but wrong gives 10.0
    v = wrong.velocity_after(3.0)
    assert abs(v - 11.0) > 1e-6, "Wrong velocity_after unexpectedly passed"
    # displacement should be 24.0 but wrong gives 33.0
    s = wrong.displacement(3.0)
    assert abs(s - 24.0) > 1e-6, "Wrong displacement unexpectedly passed"