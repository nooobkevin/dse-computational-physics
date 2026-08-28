"""Magnetic field simulation with dependency-injection hooks.

Architecture
------------
:class:`MagneticField` is the **abstract base**.  It defines one physics
**hook**:

    ``field(self, x, y, z) -> tuple[float, float, float]``

that raises ``NotImplementedError`` by default.  Reference implementations
provide the correct physics for a straight wire and a solenoid.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
MU_0 = 4.0 * math.pi * 1e-7  # vacuum permeability (T·m/A)


class MagneticField:
    """Abstract base magnetic-field simulation.

    Parameters
    ----------
    position : tuple[float, float]
        Position of the source (m).  Default (0.0, 0.0).
    """

    def __init__(self, position: Tuple[float, float] = (0.0, 0.0)) -> None:
        self._position = position

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def field(self, x: float, y: float, z: float = 0.0) -> Tuple[float, float, float]:
        """Compute magnetic field ``(Bx, By, Bz)`` at point ``(x, y, z)``.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        x : float
            x-coordinate (m).
        y : float
            y-coordinate (m).
        z : float
            z-coordinate (m).  Default 0.0.

        Returns
        -------
        tuple[float, float, float]
            Magnetic field components ``(Bx, By, Bz)`` (T).
        """
        raise NotImplementedError(
            "Subclasses must implement field(self, x, y, z)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """No-op for static fields."""
        pass

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @property
    def state(self) -> Dict[str, float | Tuple[float, float]]:
        return {"position": self._position}


class ReferenceStraightWire(MagneticField):
    """Magnetic field around a long straight current-carrying wire.

    The wire lies along the z-axis.  The field at a radial distance *r*
    is circumferential (right-hand rule):

        B = μ₀ I / (2 π r)

    Parameters
    ----------
    current : float
        Current in the wire (A).  Default 1.0.
    mu0 : float
        Vacuum permeability (T·m/A).  Default 4π × 10⁻⁷.
    """

    def __init__(
        self,
        current: float = 1.0,
        mu0: float = MU_0,
        position: Tuple[float, float] = (0.0, 0.0),
    ) -> None:
        super().__init__(position=position)
        self.I = current
        self.mu0 = mu0

    def field(self, x: float, y: float, z: float = 0.0) -> Tuple[float, float, float]:
        # Displacement from wire position
        dx = x - self._position[0]
        dy = y - self._position[1]
        r = math.sqrt(dx * dx + dy * dy)
        if r < 1e-12:
            return (0.0, 0.0, 0.0)
        B_mag = self.mu0 * self.I / (2.0 * math.pi * r)
        # Circumferential direction (right-hand rule): B ⟂ r̂
        Bx = -B_mag * dy / r
        By = B_mag * dx / r
        return (Bx, By, 0.0)


class ReferenceSolenoid(MagneticField):
    """Magnetic field inside an ideal solenoid.

    The field is uniform inside and approximately zero outside:

        B = μ₀ N I / L   (inside, along the axis)

    Parameters
    ----------
    current : float
        Current in the solenoid (A).  Default 1.0.
    N : int
        Number of turns.  Default 100.
    length : float
        Length of the solenoid (m).  Default 0.5.
    mu0 : float
        Vacuum permeability (T·m/A).  Default 4π × 10⁻⁷.
    """

    def __init__(
        self,
        current: float = 1.0,
        N: int = 100,
        length: float = 0.5,
        mu0: float = MU_0,
        position: Tuple[float, float] = (0.0, 0.0),
    ) -> None:
        super().__init__(position=position)
        self.I = current
        self.N = N
        self.L = length
        self.mu0 = mu0

    def field(self, x: float, y: float, z: float = 0.0) -> Tuple[float, float, float]:
        # Uniform field along the z-axis inside the solenoid
        B_mag = self.mu0 * self.N * self.I / self.L
        return (0.0, 0.0, B_mag)