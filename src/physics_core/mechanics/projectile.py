"""Projectile motion simulation with dependency-injection hooks.

Architecture
------------
:class:`ProjectileSim` is the abstract base; it defines the physics hook
``acceleration(self, vx, vy, t) -> (ax, ay)`` that raises
``NotImplementedError``.  :class:`ReferenceProjectileSim` provides the
standard ``(0, -g)`` acceleration (with an optional linear-drag variant).

State representation
--------------------
Internal state is a dict ``{"x": ..., "y": ..., "vx": ..., "vy": ..., "t": ...}``
consumed by the generic integrators in :mod:`physics_core.integrators`.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

from physics_core.integrators import euler_step, verlet_step

# ---------------------------------------------------------------------------
# Default physical constants
# ---------------------------------------------------------------------------
G = 9.81  # gravitational acceleration (m/s²)


class ProjectileState:
    """Convenience container for projectile state.

    Parameters
    ----------
    x : float
        Horizontal position (m).
    y : float
        Vertical position (m).
    vx : float
        Horizontal velocity (m/s).
    vy : float
        Vertical velocity (m/s).
    t : float
        Time (s).
    """

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        vx: float = 0.0,
        vy: float = 0.0,
        t: float = 0.0,
    ) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.t = t

    def as_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "vx": self.vx, "vy": self.vy, "t": self.t}

    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> ProjectileState:
        return cls(x=d["x"], y=d["y"], vx=d["vx"], vy=d["vy"], t=d.get("t", 0.0))


class ProjectileSim:
    """Abstract base projectile simulation.

    Parameters
    ----------
    x0 : float
        Initial horizontal position (m).  Default 0.0.
    y0 : float
        Initial vertical position (m).  Default 0.0.
    vx0 : float
        Initial horizontal velocity (m/s).  Default 10.0.
    vy0 : float
        Initial vertical velocity (m/s).  Default 10.0.
    dt : float
        Default time-step (s).  Default 0.01.
    scheme : str
        Integration scheme — ``"euler"`` or ``"verlet"`` (default).
    """

    def __init__(
        self,
        x0: float = 0.0,
        y0: float = 0.0,
        vx0: float = 10.0,
        vy0: float = 10.0,
        dt: float = 0.01,
        scheme: str = "verlet",
    ) -> None:
        self.dt = dt
        if scheme not in ("euler", "verlet"):
            raise ValueError(f"scheme must be 'euler' or 'verlet', got {scheme!r}")
        self._scheme = scheme

        # Internal state dict — uses separate x/y entries for the integrator
        self._state: Dict[str, float] = {
            "x": x0,
            "y": y0,
            "vx": vx0,
            "vy": vy0,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def acceleration(self, vx: float, vy: float, t: float) -> Tuple[float, float]:
        """Compute acceleration ``(ax, ay)`` at the current state.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        vx : float
            Horizontal velocity (m/s).
        vy : float
            Vertical velocity (m/s).
        t : float
            Current time (s).

        Returns
        -------
        tuple of float
            ``(ax, ay)`` — horizontal and vertical acceleration (m/s²).
        """
        raise NotImplementedError(
            "Subclasses must implement acceleration(self, vx, vy, t)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def _deriv_x(self, x: float, vx: float, t: float) -> float:
        """Rate of change of position in x — just the x-velocity."""
        return self._state["vx"]

    def _deriv_y(self, y: float, vy: float, t: float) -> float:
        return self.acceleration(self._state["vx"], self._state["vy"], t)[1]

    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        Uses separate Verlet / Euler steps for the x and y degrees of
        freedom, each driven by the shared acceleration hook.
        """
        h = dt if dt is not None else self.dt
        stepper = verlet_step if self._scheme == "verlet" else euler_step

        # Step x degree of freedom
        x_state = {"x": self._state["x"], "v": self._state["vx"], "t": self._state["t"]}
        x_next = stepper(x_state, h, self._deriv_x)

        # Step y degree of freedom
        y_state = {"x": self._state["y"], "v": self._state["vy"], "t": self._state["t"]}
        y_next = stepper(y_state, h, self._deriv_y)

        self._state["x"] = x_next["x"]
        self._state["vx"] = x_next["v"]
        self._state["y"] = y_next["x"]
        self._state["vy"] = y_next["v"]
        self._state["t"] = x_next["t"]

    @property
    def state(self) -> ProjectileState:
        """Current state as a :class:`ProjectileState`."""
        return ProjectileState.from_dict(self._state)

    @property
    def position(self) -> Tuple[float, float]:
        """Current ``(x, y)`` position."""
        return (self._state["x"], self._state["y"])

    @property
    def velocity(self) -> Tuple[float, float]:
        """Current ``(vx, vy)`` velocity."""
        return (self._state["vx"], self._state["vy"])

    def trajectory(self) -> List[Tuple[float, float, float]]:
        """Return the full trajectory as a list of ``(x, y, t)`` tuples.

        .. note::
           This method re-simulates from the beginning.  For long
           simulations consider recording points during ``step()`` calls
           instead.
        """
        raise NotImplementedError(
            "trajectory() is not implemented in the base class. "
            "Subclasses may override it with a recording loop."
        )


class ReferenceProjectileSim(ProjectileSim):
    """Reference projectile with standard gravity ``(0, -g)``.

    Parameters
    ----------
    drag_coefficient : float
        Linear drag coefficient ``b`` (N·s/m).  When > 0, the acceleration
        becomes ``ax = -b * vx / m, ay = -g - b * vy / m``.  Default 0 (no drag).
    mass : float
        Projectile mass (kg).  Used only when drag > 0.  Default 1.0.
    """

    def __init__(
        self,
        drag_coefficient: float = 0.0,
        mass: float = 1.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.drag_coefficient = drag_coefficient
        self.mass = mass

    def acceleration(self, vx: float, vy: float, t: float) -> Tuple[float, float]:
        ax = -(self.drag_coefficient / self.mass) * vx
        ay = -G - (self.drag_coefficient / self.mass) * vy
        return (ax, ay)