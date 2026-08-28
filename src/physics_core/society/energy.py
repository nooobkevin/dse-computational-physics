"""Energy sources simulation with dependency-injection hooks.

Architecture
------------
:class:`EnergySim` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines physics **hooks**:

    ``mass_energy_delta(self, dm) -> tuple[float, float]``
    ``solar_power(self, area, solar_constant, efficiency) -> float``
    ``wind_power(self, r, wind_speed, air_density, efficiency) -> float``
    ``photovoltaic_power(self, area, solar_constant, efficiency) -> float``

that raise ``NotImplementedError`` by default.  Subclasses override the
hooks to supply the physics — students fill them in, while
:class:`ReferenceEnergySim` provides the correct reference implementation.

Physical constants
------------------
c  = 3.0e8 m/s          (speed of light)
amu_to_kg = 1.660539e-27 kg
eV_per_J  = 6.242e18
MeV_per_amu = 931.5     (1 amu ≈ 931.5 MeV/c²)
"""

from __future__ import annotations

import math
from typing import Tuple

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
C = 3.0e8  # speed of light (m/s)
AMU_TO_KG = 1.660539e-27  # 1 atomic mass unit in kg
MEV_PER_AMU = 931.5  # energy equivalent of 1 amu in MeV
EV_PER_J = 6.242e18  # eV per joule


class EnergySim:
    """Abstract base energy-sources simulation.

    Parameters
    ----------
    solar_constant : float
        Solar constant (W/m²).  Default 1000.0.
    air_density : float
        Air density (kg/m³).  Default 1.2.
    """

    def __init__(
        self,
        solar_constant: float = 1000.0,
        air_density: float = 1.2,
    ) -> None:
        self.solar_constant = solar_constant
        self.air_density = air_density

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------

    def mass_energy_delta(self, dm: float, in_amu: bool = True) -> Tuple[float, float]:
        """Compute the energy released from a mass defect.

        Parameters
        ----------
        dm : float
            Mass defect.  Interpreted as amu if *in_amu* is True, else kg.
        in_amu : bool
            If True, *dm* is in atomic mass units; if False, in kg.

        Returns
        -------
        tuple[float, float]
            ``(energy_J, energy_MeV)`` — energy in joules and MeV.
        """
        raise NotImplementedError(
            "Subclasses must implement mass_energy_delta(self, dm, in_amu)"
        )

    def solar_power(
        self, area: float, solar_constant: float | None = None, efficiency: float = 1.0
    ) -> float:
        """Compute the electrical power from a solar panel.

        P = solar_constant * area * efficiency

        Parameters
        ----------
        area : float
            Panel area (m²).
        solar_constant : float or None
            Solar constant (W/m²).  Uses ``self.solar_constant`` if None.
        efficiency : float
            Panel efficiency (0–1).  Default 1.0.

        Returns
        -------
        float
            Electrical power (W).
        """
        raise NotImplementedError(
            "Subclasses must implement solar_power(self, area, solar_constant, efficiency)"
        )

    def wind_power(
        self,
        r: float,
        wind_speed: float,
        air_density: float | None = None,
        efficiency: float = 1.0,
    ) -> float:
        """Compute the mechanical power from a wind turbine.

        P = 1/2 * eta * rho * pi * r² * v³

        Parameters
        ----------
        r : float
            Rotor radius (m).
        wind_speed : float
            Wind speed (m/s).
        air_density : float or None
            Air density (kg/m³).  Uses ``self.air_density`` if None.
        efficiency : float
            Turbine efficiency (0–1).  Default 1.0.

        Returns
        -------
        float
            Mechanical power (W).
        """
        raise NotImplementedError(
            "Subclasses must implement wind_power(self, r, wind_speed, air_density, efficiency)"
        )

    def photovoltaic_power(
        self, area: float, solar_constant: float | None = None, efficiency: float = 1.0
    ) -> float:
        """Compute the electrical power from a photovoltaic cell.

        This is a convenience wrapper around :meth:`solar_power` with
        a typical PV efficiency default.

        Parameters
        ----------
        area : float
            Cell area (m²).
        solar_constant : float or None
            Solar constant (W/m²).  Uses ``self.solar_constant`` if None.
        efficiency : float
            Cell efficiency (0–1).  Default 0.20 (typical commercial PV).

        Returns
        -------
        float
            Electrical power (W).
        """
        raise NotImplementedError(
            "Subclasses must implement photovoltaic_power(self, area, solar_constant, efficiency)"
        )


class ReferenceEnergySim(EnergySim):
    """Reference energy-sources implementation with correct physics.

    Physics formulas
    ----------------
    ΔE = Δm · c²
        Energy from mass defect.  1 amu ≈ 931.5 MeV.

    P_solar = S · A · η
        Solar panel power from solar constant S, area A, efficiency η.

    P_wind = ½ · η · ρ · π · r² · v³
        Wind turbine power from efficiency η, air density ρ, rotor
        radius r, wind speed v.

    P_pv = S · A · η
        Photovoltaic power (same as solar_power with η ≈ 0.20).
    """

    def mass_energy_delta(self, dm: float, in_amu: bool = True) -> Tuple[float, float]:
        """ΔE = Δm · c².

        If *in_amu* is True, converts amu → kg first.
        Returns ``(energy_J, energy_MeV)``.
        """
        if in_amu:
            dm_kg = dm * AMU_TO_KG
            energy_MeV = dm * MEV_PER_AMU
        else:
            dm_kg = dm
            energy_MeV = dm / AMU_TO_KG * MEV_PER_AMU
        energy_J = dm_kg * C * C
        return (energy_J, energy_MeV)

    def solar_power(
        self, area: float, solar_constant: float | None = None, efficiency: float = 1.0
    ) -> float:
        """P = S · A · η."""
        S = solar_constant if solar_constant is not None else self.solar_constant
        return S * area * efficiency

    def wind_power(
        self,
        r: float,
        wind_speed: float,
        air_density: float | None = None,
        efficiency: float = 1.0,
    ) -> float:
        """P = ½ · η · ρ · π · r² · v³."""
        rho = air_density if air_density is not None else self.air_density
        return 0.5 * efficiency * rho * math.pi * r * r * (wind_speed ** 3)

    def photovoltaic_power(
        self, area: float, solar_constant: float | None = None, efficiency: float = 1.0
    ) -> float:
        """P = S · A · η (with default η = 0.20)."""
        S = solar_constant if solar_constant is not None else self.solar_constant
        eta = efficiency if efficiency != 1.0 else 0.20
        return S * area * eta