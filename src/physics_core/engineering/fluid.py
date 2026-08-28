"""Fluid dynamics simulations with dependency-injection hooks.

Architecture
------------
:class:`FluidFlow` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines physics **hooks**:

    ``continuity_velocity(self, A1, A2, v1) -> float``
    ``bernoulli_pressure(self, P1, v1, v2, h1, h2, rho) -> float``
    ``pitot_speed(self, delta_P, rho) -> float``

that raise ``NotImplementedError`` by default.  Subclasses override the
hooks to supply the physics — students fill them in, while
:class:`ReferenceFluidFlow` provides the correct reference implementation.

State representation
--------------------
Internal state is a dict ``{"A1", "A2", "v1", "v2", "P1", "P2", "h1", "h2", "rho", "t"}``.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple


class FluidFlow:
    """Abstract base fluid dynamics simulation.

    Parameters
    ----------
    A1 : float
        Cross-sectional area at point 1 (m²).  Default 0.1.
    A2 : float
        Cross-sectional area at point 2 (m²).  Default 0.05.
    v1 : float
        Flow speed at point 1 (m/s).  Default 2.0.
    P1 : float
        Pressure at point 1 (Pa).  Default 101325.0.
    h1 : float
        Height at point 1 (m).  Default 0.0.
    h2 : float
        Height at point 2 (m).  Default 0.0.
    rho : float
        Fluid density (kg/m³).  Default 1000.0 (water).
    """

    def __init__(
        self,
        A1: float = 0.1,
        A2: float = 0.05,
        v1: float = 2.0,
        P1: float = 101325.0,
        h1: float = 0.0,
        h2: float = 0.0,
        rho: float = 1000.0,
    ) -> None:
        self.A1 = A1
        self.A2 = A2
        self.v1 = v1
        self.P1 = P1
        self.h1 = h1
        self.h2 = h2
        self.rho = rho
        self._state: Dict[str, float] = {
            "A1": A1,
            "A2": A2,
            "v1": v1,
            "v2": 0.0,
            "P1": P1,
            "P2": 0.0,
            "h1": h1,
            "h2": h2,
            "rho": rho,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------

    def continuity_velocity(self, A1: float, A2: float, v1: float) -> float:
        """Compute the flow speed at point 2 using the continuity equation.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        A1 : float
            Cross-sectional area at point 1 (m²).
        A2 : float
            Cross-sectional area at point 2 (m²).
        v1 : float
            Flow speed at point 1 (m/s).

        Returns
        -------
        float
            Flow speed at point 2 (m/s).
        """
        raise NotImplementedError(
            "Subclasses must implement continuity_velocity(self, A1, A2, v1)"
        )

    def bernoulli_pressure(
        self, P1: float, v1: float, v2: float,
        h1: float, h2: float, rho: float,
    ) -> float:
        """Compute the pressure at point 2 using Bernoulli's equation.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        P1 : float
            Pressure at point 1 (Pa).
        v1 : float
            Flow speed at point 1 (m/s).
        v2 : float
            Flow speed at point 2 (m/s).
        h1 : float
            Height at point 1 (m).
        h2 : float
            Height at point 2 (m).
        rho : float
            Fluid density (kg/m³).

        Returns
        -------
        float
            Pressure at point 2 (Pa).
        """
        raise NotImplementedError(
            "Subclasses must implement bernoulli_pressure(self, ...)"
        )

    def pitot_speed(self, delta_P: float, rho: float) -> float:
        """Compute the flow speed from a pitot tube pressure difference.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        delta_P : float
            Stagnation minus static pressure (Pa).
        rho : float
            Fluid density (kg/m³).

        Returns
        -------
        float
            Flow speed (m/s).
        """
        raise NotImplementedError(
            "Subclasses must implement pitot_speed(self, delta_P, rho)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------

    def step(self, dt: float | None = None) -> None:
        """Advance the fluid simulation by one time-step.

        Recomputes v2 from continuity and P2 from Bernoulli.
        """
        self._state["v2"] = self.continuity_velocity(
            self._state["A1"], self._state["A2"], self._state["v1"]
        )
        self._state["P2"] = self.bernoulli_pressure(
            self._state["P1"], self._state["v1"],
            self._state["v2"], self._state["h1"],
            self._state["h2"], self._state["rho"],
        )
        if dt is not None:
            self._state["t"] += dt

    @property
    def state(self) -> Dict[str, Any]:
        """Current simulation state."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Placeholder."""
        return (0.0, 0.0)

    def energy(self) -> Dict[str, float]:
        """Energy per unit volume at each point (Bernoulli constant)."""
        v2 = self._state["v2"]
        P2 = self._state["P2"]
        const1 = self._state["P1"] + 0.5 * self.rho * self.v1 * self.v1 + self.rho * 9.81 * self.h1
        const2 = P2 + 0.5 * self.rho * v2 * v2 + self.rho * 9.81 * self.h2
        return {
            "bernoulli_constant_1": const1,
            "bernoulli_constant_2": const2,
            "conserved": abs(const1 - const2) < 1e-6,
        }


class ReferenceFluidFlow(FluidFlow):
    """Reference fluid flow with correct continuity and Bernoulli physics.

    Continuity equation (incompressible fluid):

        A₁ v₁ = A₂ v₂  →  v₂ = A₁ v₁ / A₂

    Bernoulli's equation:

        P₁ + ½ρv₁² + ρgh₁ = P₂ + ½ρv₂² + ρgh₂

    Pitot tube:

        v = √(2 ΔP / ρ)
    """

    def continuity_velocity(self, A1: float, A2: float, v1: float) -> float:
        """v2 = A1 * v1 / A2."""
        if A2 <= 0.0:
            return float("inf")
        return A1 * v1 / A2

    def bernoulli_pressure(
        self, P1: float, v1: float, v2: float,
        h1: float, h2: float, rho: float,
    ) -> float:
        """P2 = P1 + ½ρ(v1² - v2²) + ρg(h1 - h2)."""
        g = 9.81
        return P1 + 0.5 * rho * (v1 * v1 - v2 * v2) + rho * g * (h1 - h2)

    def pitot_speed(self, delta_P: float, rho: float) -> float:
        """v = √(2 ΔP / ρ)."""
        if delta_P < 0.0 or rho <= 0.0:
            return 0.0
        return math.sqrt(2.0 * delta_P / rho)