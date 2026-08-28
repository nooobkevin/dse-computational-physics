"""Optical fibre simulation with dependency-injection hooks.

Architecture
------------
:class:`OpticalFibre` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines one physics **hook**:

    ``total_internal_reflection(self, angle) -> bool``

that raises ``NotImplementedError`` by default.  Subclasses override the
hook to supply the physics — students fill it in, while
:class:`ReferenceOpticalFibre` provides the correct reference implementation.

State representation
--------------------
Internal state is a dict ``{"n1", "n2", "length", "angle", "t"}``.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple


class OpticalFibre:
    """Abstract base optical fibre simulation.

    Parameters
    ----------
    n1 : float
        Refractive index of the core.  Default 1.50.
    n2 : float
        Refractive index of the cladding.  Default 1.45.
    length : float
        Fibre length (m).  Default 10.0.
    angle : float
        Ray incidence angle relative to the normal (rad).  Default 0.5.
    """

    def __init__(
        self,
        n1: float = 1.50,
        n2: float = 1.45,
        length: float = 10.0,
        angle: float = 0.5,
    ) -> None:
        self.n1 = n1
        self.n2 = n2
        self.length = length
        self.angle = angle
        self._state: Dict[str, float] = {
            "n1": n1,
            "n2": n2,
            "length": length,
            "angle": angle,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------
    def total_internal_reflection(self, angle: float) -> bool:
        """Determine whether a ray at *angle* undergoes TIR.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        angle : float
            Incidence angle (rad).

        Returns
        -------
        bool
            True if the ray undergoes total internal reflection.
        """
        raise NotImplementedError(
            "Subclasses must implement total_internal_reflection(self, angle)"
        )

    @property
    def critical_angle(self) -> float:
        """Critical angle for TIR (rad).

        Override in subclasses to supply the physics.
        """
        raise NotImplementedError(
            "Subclasses must implement critical_angle property"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        For a static ray this is a no-op.  Subclasses that model
        time-varying rays may override this.
        """
        pass

    @property
    def state(self) -> Dict[str, Any]:
        """Current simulation state."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Ray position inside the fibre ``(x, y)``.

        Returns a schematic position based on the current angle.
        """
        x = self._state.get("t", 0.0) * math.sin(self.angle)
        y = self._state.get("t", 0.0) * math.cos(self.angle)
        return (x, y)

    def energy(self) -> Dict[str, float]:
        """Energy carried by the ray.

        For an ideal fibre with TIR, all energy is transmitted.
        If the ray leaks, transmitted energy is zero.
        """
        if self.total_internal_reflection(self.angle):
            return {"transmitted": 1.0, "leaked": 0.0, "total": 1.0}
        return {"transmitted": 0.0, "leaked": 1.0, "total": 1.0}

    @property
    def acceptance_condition(self) -> bool:
        """Whether the current ray angle satisfies TIR."""
        return self.total_internal_reflection(self.angle)


class ReferenceOpticalFibre(OpticalFibre):
    """Reference optical fibre with correct TIR physics.

    Total internal reflection occurs when the incidence angle exceeds
    the critical angle:

        θ_c = arcsin(n₂ / n₁)

    where n₁ > n₂ (core index > cladding index).
    """

    @property
    def critical_angle(self) -> float:
        """Critical angle for TIR: θ_c = arcsin(n₂ / n₁).

        Returns π/2 when n₁ ≤ n₂ (no TIR possible), so that
        :meth:`total_internal_reflection` always returns False.
        """
        if self.n1 <= self.n2:
            return math.pi / 2.0  # no TIR possible
        ratio = self.n2 / self.n1
        if ratio > 1.0:
            return math.pi / 2.0
        return math.asin(ratio)

    def total_internal_reflection(self, angle: float) -> bool:
        """Return True if *angle* exceeds the critical angle."""
        return angle > self.critical_angle

    def ray_path_length(self, angle: float | None = None) -> float:
        """Compute the zigzag path length inside the fibre.

        For a fibre of length *L* and ray angle *θ* (relative to the
        fibre axis), the actual path length is L / cos(θ).
        """
        if angle is None:
            angle = self.angle
        if not self.total_internal_reflection(angle):
            return float("inf")  # ray leaks out
        return self.length / math.cos(angle)