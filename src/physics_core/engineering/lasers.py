"""Laser simulation with dependency-injection hooks.

Architecture
------------
:class:`Laser` is the **abstract base** that defines the laser physics
framework.  It defines one physics **hook**:

    ``stimulated_emission(self) -> float``

that raises ``NotImplementedError`` by default.  :class:`ReferenceLaser`
provides the correct reference implementation.

State representation
--------------------
Internal state is a dict ``{"N_upper", "N_lower", "photon_count", "t"}``.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple


class Laser:
    """Abstract base laser simulation.

    Parameters
    ----------
    N_upper : float
        Population of the upper laser level.  Default 100.
    N_lower : float
        Population of the lower laser level.  Default 10.
    pump_rate : float
        Pumping rate (atoms per second).  Default 50.0.
    """

    def __init__(
        self,
        N_upper: float = 100.0,
        N_lower: float = 10.0,
        pump_rate: float = 50.0,
    ) -> None:
        self.N_upper = N_upper
        self.N_lower = N_lower
        self.pump_rate = pump_rate
        self._state: Dict[str, float] = {
            "N_upper": N_upper,
            "N_lower": N_lower,
            "photon_count": 0.0,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def stimulated_emission(self) -> float:
        """Compute the number of photons emitted via stimulated emission.

        Override this in subclasses to supply the physics.

        Returns
        -------
        float
            Number of coherent photons emitted.
        """
        raise NotImplementedError(
            "Subclasses must implement stimulated_emission(self)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    @property
    def population_inversion(self) -> bool:
        """Whether a population inversion exists (N_upper > N_lower)."""
        return self.N_upper > self.N_lower

    def step(self, dt: float | None = None) -> None:
        """Advance the laser simulation by one time-step."""
        h = dt if dt is not None else 0.01
        photons = self.stimulated_emission()
        self._state["photon_count"] += photons * h
        self._state["t"] += h

    @property
    def state(self) -> Dict[str, Any]:
        """Current simulation state."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Placeholder position (laser output)."""
        return (0.0, 0.0)

    def energy(self) -> Dict[str, float]:
        """Energy in the laser field (proportional to photon count)."""
        return {"optical": self._state["photon_count"]}


class ReferenceLaser(Laser):
    """Reference laser with correct stimulated emission physics.

    Stimulated emission occurs when a population inversion exists.
    The emission rate is proportional to the upper-level population
    and the photon density already present.
    """

    def stimulated_emission(self) -> float:
        if not self.population_inversion:
            return 0.0
        # Simplified model: emission rate ∝ N_upper - N_lower
        rate = (self.N_upper - self.N_lower) * 0.1
        return max(0.0, rate)