"""Electromagnetic induction simulation with dependency-injection hooks.

Architecture
------------
:class:`InductionCoil` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines physics **hooks**:

    ``magnetic_flux(self, B, A, theta) -> float``
    ``induced_emf(self, flux_old, flux_new, dt) -> float``
    ``lenz_direction(self, flux_old, flux_new) -> str``

that raise ``NotImplementedError`` by default.  Subclasses override the
hooks to supply the physics — students fill them in, while
:class:`ReferenceInductionCoil` provides the correct reference implementation.

State representation
--------------------
Internal state is a dict ``{"B", "A", "theta", "flux", "emf", "t", "magnet_position"}``.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple


class InductionCoil:
    """Abstract base electromagnetic induction simulation.

    Parameters
    ----------
    B : float
        Magnetic field strength (T).  Default 0.5.
    A : float
        Area of the coil (m²).  Default 0.01.
    theta : float
        Angle between B and coil normal (rad).  Default 0.0.
    magnet_position : float
        Position of the magnet relative to the coil (m).  Default 0.0.
        Positive = approaching the coil.
    """

    def __init__(
        self,
        B: float = 0.5,
        A: float = 0.01,
        theta: float = 0.0,
        magnet_position: float = 0.0,
    ) -> None:
        self.B = B
        self.A = A
        self.theta = theta
        self.magnet_position = magnet_position
        self._state: Dict[str, float] = {
            "B": B,
            "A": A,
            "theta": theta,
            "flux": 0.0,
            "flux_prev": 0.0,
            "emf": 0.0,
            "magnet_position": magnet_position,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------

    def magnetic_flux(self, B: float, A: float, theta: float) -> float:
        """Compute the magnetic flux through the coil.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        B : float
            Magnetic field strength (T).
        A : float
            Area of the coil (m²).
        theta : float
            Angle between B and coil normal (rad).

        Returns
        -------
        float
            Magnetic flux (Wb).
        """
        raise NotImplementedError(
            "Subclasses must implement magnetic_flux(self, B, A, theta)"
        )

    def induced_emf(self, flux_old: float, flux_new: float, dt: float) -> float:
        """Compute the average induced e.m.f. over a time interval.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        flux_old : float
            Magnetic flux at the start of the interval (Wb).
        flux_new : float
            Magnetic flux at the end of the interval (Wb).
        dt : float
            Time interval (s).

        Returns
        -------
        float
            Average induced e.m.f. (V).
        """
        raise NotImplementedError(
            "Subclasses must implement induced_emf(self, flux_old, flux_new, dt)"
        )

    def lenz_direction(self, flux_old: float, flux_new: float) -> str:
        """Determine the direction of induced current (Lenz's law).

        Returns "CW" (clockwise) or "CCW" (counter-clockwise) as viewed
        from the approaching magnet.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        flux_old : float
            Magnetic flux at the start of the interval (Wb).
        flux_new : float
            Magnetic flux at the end of the interval (Wb).

        Returns
        -------
        str
            "CW" or "CCW".
        """
        raise NotImplementedError(
            "Subclasses must implement lenz_direction(self, flux_old, flux_new)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------

    def step(self, dt: float | None = None) -> None:
        """Advance the induction simulation by one time-step.

        The magnetic field strength depends on the magnet position
        (simulated as B ∝ 1 / (d² + offset) for a dipole approximation).
        """
        h = dt if dt is not None else 0.01
        d = self.magnet_position
        # B field from a dipole: B ∝ 1 / (d² + a²)^(3/2)
        offset = 0.05  # m, prevents singularity
        B_effective = self.B / ((d * d + offset * offset) ** 1.5)

        self._state["flux_prev"] = self._state["flux"]
        self._state["flux"] = self.magnetic_flux(B_effective, self.A, self.theta)
        self._state["emf"] = self.induced_emf(
            self._state["flux_prev"], self._state["flux"], h
        )
        self._state["t"] += h

    @property
    def state(self) -> Dict[str, Any]:
        """Current simulation state."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Magnet position (schematic)."""
        return (self.magnet_position, 0.0)

    def energy(self) -> Dict[str, float]:
        """Energy-related diagnostics."""
        flux = self._state["flux"]
        emf = self._state["emf"]
        return {"flux": flux, "induced_emf": emf}


class ReferenceInductionCoil(InductionCoil):
    """Reference induction coil with correct flux, Faraday, and Lenz physics.

    Magnetic flux:

        Φ = B A cos θ

    Faraday's law (average over a step):

        ε = -ΔΦ / Δt

    Lenz's law:

        The induced current opposes the change in magnetic flux.
        If flux is increasing (ΔΦ > 0), the induced current creates a
        field opposing the increase (direction CW or CCW depending on
        the geometry).  For a coil with the magnet approaching from
        the left, increasing flux produces CCW current (viewed from
        the magnet side).
    """

    def magnetic_flux(self, B: float, A: float, theta: float) -> float:
        """Φ = B A cos θ."""
        return B * A * math.cos(theta)

    def induced_emf(self, flux_old: float, flux_new: float, dt: float) -> float:
        """ε = -ΔΦ / Δt."""
        if dt <= 0.0:
            return 0.0
        return -(flux_new - flux_old) / dt

    def lenz_direction(self, flux_old: float, flux_new: float) -> str:
        """Determine induced current direction.

        Returns:
            "CCW" when flux is increasing (magnet approaching)
            "CW" when flux is decreasing (magnet receding)
        """
        if flux_new > flux_old:
            return "CCW"  # opposes increase
        elif flux_new < flux_old:
            return "CW"   # opposes decrease
        return "CW"  # no change