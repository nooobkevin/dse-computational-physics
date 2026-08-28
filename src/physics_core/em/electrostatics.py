"""Electric field simulation with dependency-injection hooks.

Architecture
------------
:class:`ElectricField` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines two physics **hooks**:

    ``field(self, x, y) -> tuple[float, float]``
    ``potential(self, x, y) -> float``

that raise ``NotImplementedError`` by default.  Subclasses override the
hooks to supply the physics — students fill them in, while
:class:`ReferenceElectricField` provides the correct reference implementation.

State representation
--------------------
Internal state is a dict ``{"q": ..., "position": (x, y)}``.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
EPSILON_0 = 8.854187817e-12  # vacuum permittivity (F/m)


class ElectricField:
    """Abstract base electric-field simulation.

    Parameters
    ----------
    q : float
        Charge magnitude (C).  Default 1e-9.
    epsilon0 : float
        Vacuum permittivity (F/m).  Default 8.854e-12.
    position : tuple[float, float]
        Charge position (m).  Default (0.0, 0.0).
    """

    def __init__(
        self,
        q: float = 1e-9,
        epsilon0: float = EPSILON_0,
        position: Tuple[float, float] = (0.0, 0.0),
    ) -> None:
        self.q = q
        self.epsilon0 = epsilon0
        self._position = position

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------
    def field(self, x: float, y: float) -> Tuple[float, float]:
        """Compute electric field ``(Ex, Ey)`` at point ``(x, y)``.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        x : float
            x-coordinate of the evaluation point (m).
        y : float
            y-coordinate of the evaluation point (m).

        Returns
        -------
        tuple[float, float]
            Electric field components ``(Ex, Ey)`` (N/C or V/m).
        """
        raise NotImplementedError(
            "Subclasses must implement field(self, x, y)"
        )

    def potential(self, x: float, y: float) -> float:
        """Compute electric potential ``V`` at point ``(x, y)``.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        x : float
            x-coordinate of the evaluation point (m).
        y : float
            y-coordinate of the evaluation point (m).

        Returns
        -------
        float
            Electric potential (V).
        """
        raise NotImplementedError(
            "Subclasses must implement potential(self, x, y)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        For static fields this is a no-op.  Subclasses that model
        time-varying fields may override this.
        """
        pass

    @property
    def position(self) -> Tuple[float, float]:
        """Current charge position ``(x, y)``."""
        return self._position

    @property
    def energy(self) -> float:
        """Self-energy of the charge configuration.

        For a point charge the self-energy is infinite; return 0 as a
        placeholder.  Subclasses with multiple charges may override.
        """
        return 0.0

    @property
    def state(self) -> Dict[str, float | Tuple[float, float]]:
        """Current simulation state ``{"q", "position"}``."""
        return {"q": self.q, "position": self._position}


class ReferenceElectricField(ElectricField):
    """Reference electric field with correct Coulomb physics.

    The electric field at a point ``(x, y)`` due to a point charge ``q``
    at the origin is:

        E = q / (4 π ε₀ r²)  r̂

    where ``r`` is the distance from the charge and ``r̂`` is the unit
    radial vector.

    The electric potential is:

        V = q / (4 π ε₀ r)
    """

    def field(self, x: float, y: float) -> Tuple[float, float]:
        dx = x - self._position[0]
        dy = y - self._position[1]
        r2 = dx * dx + dy * dy
        if r2 < 1e-12:
            return (0.0, 0.0)
        r = math.sqrt(r2)
        E_mag = self.q / (4.0 * math.pi * self.epsilon0 * r2)
        return (E_mag * dx / r, E_mag * dy / r)

    def potential(self, x: float, y: float) -> float:
        dx = x - self._position[0]
        dy = y - self._position[1]
        r = math.sqrt(dx * dx + dy * dy)
        if r < 1e-12:
            return float("inf")
        return self.q / (4.0 * math.pi * self.epsilon0 * r)