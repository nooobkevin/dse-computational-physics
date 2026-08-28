"""Auto-grader for the energy sources fill-in-the-blank exercise.

Grading philosophy
------------------
This grader measures the **numerical behaviour** of the student's
implementation — it does *not* read or string-match the student's formula.

Checks
------
1.  **NotImplementedError guard** — fail immediately if hooks not filled in.
2.  **Mass-energy** — 1 amu → ~931.5 MeV; kg input correct.
3.  **Solar power** — P = S · A · η.
4.  **Wind power** — P = ½ηρπr²v³; cubic scaling (double v → 8× power).
5.  **Photovoltaic** — default efficiency 20%.

Usage
-----
    # Grade the student's exercise (default)
    uv run pytest units/06_society/exercises/test_energy_exercise.py -v

    # Grade against the solution file (teacher self-check)
    uv run pytest units/06_society/exercises/test_energy_exercise.py -v \
        --override-student-energy=units/06_society/exercises/energy_solution.py

    # Full self-check
    uv run pytest units/06_society/exercises/test_energy_exercise.py -v \
        --selfcheck
"""

from __future__ import annotations

import math
from typing import Type

import pytest

from physics_core.society.energy import EnergySim, ReferenceEnergySim


# ===========================================================================
# Tests
# ===========================================================================


class TestEnergyExercise:
    """Auto-grader for the student energy exercise."""

    def test_physics_implemented(self, student_energy_class: Type[EnergySim]) -> None:
        """Fail immediately if the student hasn't filled in the hooks."""
        sim = student_energy_class()
        for method_name in ["mass_energy_delta", "solar_power", "wind_power", "photovoltaic_power"]:
            method = getattr(sim, method_name)
            try:
                if method_name == "mass_energy_delta":
                    method(1.0)
                elif method_name == "solar_power":
                    method(1.0, 1000.0)
                elif method_name == "wind_power":
                    method(1.0, 10.0)
                else:
                    method(1.0, 1000.0)
            except NotImplementedError:
                pytest.fail(
                    f"Your {method_name}() is still raising NotImplementedError. "
                    f"Replace the 'raise' line with the correct physics."
                )

    def test_mass_energy_amu(self, student_energy_class: Type[EnergySim]) -> None:
        """1 amu mass defect → ~931.5 MeV."""
        sim = student_energy_class()
        _, energy_MeV = sim.mass_energy_delta(1.0, in_amu=True)
        assert energy_MeV == pytest.approx(931.5, rel=0.01), (
            f"mass_energy_delta(1 amu) = {energy_MeV:.1f} MeV, "
            f"expected ~931.5 MeV"
        )

    def test_mass_energy_kg(self, student_energy_class: Type[EnergySim]) -> None:
        """ΔE = Δm · c² in SI."""
        sim = student_energy_class()
        dm_kg = 1.0e-27
        energy_J, _ = sim.mass_energy_delta(dm_kg, in_amu=False)
        expected = dm_kg * (3.0e8) ** 2
        assert energy_J == pytest.approx(expected, rel=0.01), (
            f"mass_energy_delta({dm_kg} kg) = {energy_J:.2e} J, "
            f"expected {expected:.2e} J"
        )

    def test_solar_power(self, student_energy_class: Type[EnergySim]) -> None:
        """P = S · A · η."""
        sim = student_energy_class()
        power = sim.solar_power(area=2.0, solar_constant=1000.0, efficiency=0.20)
        assert power == pytest.approx(400.0, rel=0.01), (
            f"solar_power(2 m², 1000 W/m², 20%) = {power:.1f} W, "
            f"expected 400 W"
        )

    def test_wind_power_formula(self, student_energy_class: Type[EnergySim]) -> None:
        """P = ½ηρπr²v³."""
        sim = student_energy_class()
        power = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
        expected = 0.5 * 1.2 * math.pi * 1000.0
        assert power == pytest.approx(expected, rel=0.01), (
            f"wind_power(r=1, v=10) = {power:.1f} W, "
            f"expected {expected:.1f} W"
        )

    def test_wind_power_cubic(self, student_energy_class: Type[EnergySim]) -> None:
        """Doubling wind speed → 8× power."""
        sim = student_energy_class()
        p1 = sim.wind_power(r=1.0, wind_speed=5.0, air_density=1.2, efficiency=1.0)
        p2 = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
        ratio = p2 / p1
        assert ratio == pytest.approx(8.0, rel=0.01), (
            f"Wind power ratio (v=10 / v=5) = {ratio:.2f}, "
            f"expected 8.0 (cubic scaling)"
        )

    def test_photovoltaic_default(self, student_energy_class: Type[EnergySim]) -> None:
        """PV power uses default 20% efficiency."""
        sim = student_energy_class()
        power = sim.photovoltaic_power(area=1.0, solar_constant=1000.0)
        assert power == pytest.approx(200.0, rel=0.01), (
            f"photovoltaic_power(1 m²) = {power:.1f} W, "
            f"expected 200 W (20% of 1000 W)"
        )


# ===========================================================================
# Self-check
# ===========================================================================


def test_selfcheck_correct_passes(student_energy_class: Type[EnergySim]) -> None:
    """Self-check: the grader must PASS when given the correct solution."""
    sim = student_energy_class()

    # Check mass-energy
    _, mev = sim.mass_energy_delta(1.0, in_amu=True)
    assert mev == pytest.approx(931.5, rel=0.01)

    # Check solar
    p_solar = sim.solar_power(area=2.0, solar_constant=1000.0, efficiency=0.20)
    assert p_solar == pytest.approx(400.0, rel=0.01)

    # Check wind
    p_wind = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
    expected_wind = 0.5 * 1.2 * math.pi * 1000.0
    assert p_wind == pytest.approx(expected_wind, rel=0.01)

    # Check cubic scaling
    p1 = sim.wind_power(r=1.0, wind_speed=5.0, air_density=1.2, efficiency=1.0)
    p2 = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
    assert p2 / p1 == pytest.approx(8.0, rel=0.01)

    # Check PV default
    p_pv = sim.photovoltaic_power(area=1.0, solar_constant=1000.0)
    assert p_pv == pytest.approx(200.0, rel=0.01)


def test_selfcheck_wrong_fails(wrong_energy_class: Type[EnergySim]) -> None:
    """Self-check: the grader must FAIL when given a deliberately wrong answer."""
    sim = wrong_energy_class()

    # Wrong mass-energy (uses dm instead of dm*c²)
    _, mev = sim.mass_energy_delta(1.0, in_amu=True)
    err = abs(mev - 931.5) / 931.5
    assert err > 0.5, (
        f"Wrong answer unexpectedly gave {mev:.1f} MeV for 1 amu"
    )

    # Wrong wind power (linear instead of cubic)
    p1 = sim.wind_power(r=1.0, wind_speed=5.0, air_density=1.2, efficiency=1.0)
    p2 = sim.wind_power(r=1.0, wind_speed=10.0, air_density=1.2, efficiency=1.0)
    ratio = p2 / p1
    assert abs(ratio - 8.0) > 0.5, (
        f"Wrong answer unexpectedly gave cubic scaling (ratio={ratio:.2f})"
    )


def test_selfcheck_runner(
    request: pytest.FixtureRequest,
    student_energy_class: Type[EnergySim],
    wrong_energy_class: Type[EnergySim],
) -> None:
    """Orchestrate the full self-check when ``--selfcheck`` is passed."""
    if not request.config.getoption("--selfcheck"):
        pytest.skip("Use --selfcheck to run the full self-check")

    sim = student_energy_class()
    assert sim is not None, "StudentEnergySim should be importable"
    assert hasattr(sim, "mass_energy_delta"), "StudentEnergySim should have mass_energy_delta()"