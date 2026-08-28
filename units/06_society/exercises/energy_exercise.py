"""Energy sources exercise — student fill-in-the-blank.

Task
----
Your job is to implement the **physics** of energy sources by overriding
the hooks in ``StudentEnergySim``.

The base class :class:`physics_core.society.energy.EnergySim` provides
the framework.  You only need to supply the physics formulas.

Physics background
------------------
Mass-energy equivalence:
    ΔE = Δm · c²
    1 amu ≈ 931.5 MeV

Solar power:
    P = S · A · η
    where S = solar constant (W/m²), A = area (m²), η = efficiency

Wind turbine power:
    P = ½ · η · ρ · π · r² · v³
    where η = efficiency, ρ = air density (kg/m³), r = rotor radius (m),
    v = wind speed (m/s)

Photovoltaic power:
    P = S · A · η  (same as solar, with η ≈ 0.20 typical)

Constants
---------
``self.solar_constant`` — solar constant (W/m²), default 1000.0
``self.air_density`` — air density (kg/m³), default 1.2

What to do
----------
1. Read the docstrings of each method below.
2. Replace the ``raise NotImplementedError`` lines with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/06_society/exercises/test_energy_exercise.py -v
"""

from __future__ import annotations

import math
from typing import Tuple

from physics_core.society.energy import EnergySim


class StudentEnergySim(EnergySim):
    """Student implementation of energy sources physics.

    Override the physics hooks below.  Everything else is inherited
    from :class:`EnergySim`.
    """

    def mass_energy_delta(self, dm: float, in_amu: bool = True) -> Tuple[float, float]:
        """Compute energy from mass defect ΔE = Δm · c².

        Parameters
        ----------
        dm : float
            Mass defect (amu if in_amu=True, kg if False).
        in_amu : bool
            Unit flag.

        Returns
        -------
        tuple[float, float]
            (energy_J, energy_MeV)

        Physics (fill this in)
        ----------------------
        If in_amu:
            dm_kg = dm * 1.660539e-27
            energy_MeV = dm * 931.5
        else:
            dm_kg = dm
            energy_MeV = dm / 1.660539e-27 * 931.5
        energy_J = dm_kg * (3.0e8) ** 2
        return (energy_J, energy_MeV)
        """
        raise NotImplementedError(
            "You must implement mass_energy_delta(self, dm, in_amu) "
            "in StudentEnergySim."
        )

    def solar_power(
        self, area: float, solar_constant: float | None = None, efficiency: float = 1.0
    ) -> float:
        """Compute solar panel power P = S · A · η.

        Parameters
        ----------
        area : float
            Panel area (m²).
        solar_constant : float or None
            Solar constant (W/m²).  Uses self.solar_constant if None.
        efficiency : float
            Panel efficiency (0–1).

        Returns
        -------
        float
            Power (W).

        Physics (fill this in)
        ----------------------
        S = solar_constant if solar_constant is not None else self.solar_constant
        return S * area * efficiency
        """
        raise NotImplementedError(
            "You must implement solar_power(self, area, solar_constant, efficiency) "
            "in StudentEnergySim."
        )

    def wind_power(
        self,
        r: float,
        wind_speed: float,
        air_density: float | None = None,
        efficiency: float = 1.0,
    ) -> float:
        """Compute wind turbine power P = ½ · η · ρ · π · r² · v³.

        Parameters
        ----------
        r : float
            Rotor radius (m).
        wind_speed : float
            Wind speed (m/s).
        air_density : float or None
            Air density (kg/m³).  Uses self.air_density if None.
        efficiency : float
            Turbine efficiency (0–1).

        Returns
        -------
        float
            Power (W).

        Physics (fill this in)
        ----------------------
        rho = air_density if air_density is not None else self.air_density
        return 0.5 * efficiency * rho * math.pi * r * r * (wind_speed ** 3)
        """
        raise NotImplementedError(
            "You must implement wind_power(self, r, wind_speed, air_density, efficiency) "
            "in StudentEnergySim."
        )

    def photovoltaic_power(
        self, area: float, solar_constant: float | None = None, efficiency: float = 1.0
    ) -> float:
        """Compute photovoltaic power P = S · A · η (default η = 0.20).

        Parameters
        ----------
        area : float
            Cell area (m²).
        solar_constant : float or None
            Solar constant (W/m²).  Uses self.solar_constant if None.
        efficiency : float
            Cell efficiency (0–1).  Default 1.0 (uses 0.20 if not overridden).

        Returns
        -------
        float
            Power (W).

        Physics (fill this in)
        ----------------------
        S = solar_constant if solar_constant is not None else self.solar_constant
        eta = efficiency if efficiency != 1.0 else 0.20
        return S * area * eta
        """
        raise NotImplementedError(
            "You must implement photovoltaic_power(self, area, solar_constant, efficiency) "
            "in StudentEnergySim."
        )