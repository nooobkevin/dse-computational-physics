"""Uniform circular motion simulation with a DI hook.

Architecture
------------
:class:`CircularMotion` provides kinematics for uniform circular motion.
The physics hook ``omega(self)`` returns the angular velocity (rad/s);
the default implementation returns the constant ``omega0`` passed at
construction, so the base class is already usable out of the box.
Subclasses override ``omega`` to implement non-uniform rotation.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple


class CircularMotion:
    """Uniform circular motion kinematics.

    Parameters
    ----------
    radius : float
        Radius of the circle (m).
    omega0 : float
        Constant angular velocity (rad/s).  Default 1.0.
    theta0 : float
        Initial angle (rad).  Default 0.0.
    dt : float
        Default time-step (s).  Default 0.01.
    """

    def __init__(
        self,
        radius: float = 1.0,
        omega0: float = 1.0,
        theta0: float = 0.0,
        dt: float = 0.01,
    ) -> None:
        self.radius = radius
        self._omega0 = omega0
        self.dt = dt
        self._theta = theta0
        self._t = 0.0

    # ------------------------------------------------------------------
    # Physics hook
    # ------------------------------------------------------------------
    def omega(self) -> float:
        """Angular velocity at the current state (rad/s).

        Override this to implement non-uniform rotation.
        The default returns the constant ``omega0``.
        """
        return self._omega0

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        The angle advances as ``θ += ω * dt`` where ``ω`` is obtained
        from the ``omega()`` hook.
        """
        h = dt if dt is not None else self.dt
        self._theta += self.omega() * h
        self._t += h

    @property
    def angle(self) -> float:
        """Current angular displacement (rad)."""
        return self._theta

    @property
    def position(self) -> Tuple[float, float]:
        """Cartesian coordinates ``(x, y)`` on the circle."""
        x = self.radius * math.cos(self._theta)
        y = self.radius * math.sin(self._theta)
        return (x, y)

    @property
    def tangential_speed(self) -> float:
        """Tangential speed ``v = ω r`` (m/s)."""
        return self.omega() * self.radius

    @property
    def centripetal_accel(self) -> float:
        """Centripetal acceleration ``a_c = v² / r = ω² r`` (m/s²)."""
        return self.tangential_speed**2 / self.radius