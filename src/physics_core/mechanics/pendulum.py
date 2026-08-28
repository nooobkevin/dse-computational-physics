"""Pendulum simulation with dependency-injection hooks.

Architecture
------------
:class:`PendulumSim` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It implements framework methods (``step``, ``state``, ``position``,
``energy``, ``period_from_formula``) and defines one physics **hook**:

    ``angular_acceleration(self, theta, omega) -> float``

that raises ``NotImplementedError`` by default.  Subclasses override the
hook to supply the physics — students fill it in, while
:class:`ReferencePendulumSim` provides the correct reference implementation.

State representation
--------------------
Internal state is a dict ``{"theta": ..., "omega": ..., "t": ...}`` consumed
by the generic integrators in :mod:`physics_core.integrators`.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple

from physics_core.integrators import euler_step, verlet_step

# ---------------------------------------------------------------------------
# Default physical constants
# ---------------------------------------------------------------------------
G = 9.81  # gravitational acceleration (m/s²)


class PendulumSim:
    """Abstract base pendulum simulation.

    Parameters
    ----------
    length : float
        Pendulum length (m).
    g : float
        Gravitational acceleration (m/s²).  Default 9.81.
    mass : float
        Bob mass (kg).  Default 1.0.
    theta0 : float
        Initial angular displacement (rad).  Default 0.1.
    omega0 : float
        Initial angular velocity (rad/s).  Default 0.0.
    dt : float
        Default time-step (s).  Default 0.01.
    scheme : str
        Integration scheme — ``"euler"`` or ``"verlet"`` (default).
    small_angle : bool
        If True, use the small-angle approximation sin(θ) ≈ θ in the
        reference implementation.  Default False.
    """

    def __init__(
        self,
        length: float = 1.0,
        g: float = G,
        mass: float = 1.0,
        theta0: float = 0.1,
        omega0: float = 0.0,
        dt: float = 0.01,
        scheme: str = "verlet",
        small_angle: bool = False,
    ) -> None:
        self.length = length
        self.g = g
        self.mass = mass
        self.dt = dt
        self.small_angle = small_angle

        if scheme not in ("euler", "verlet"):
            raise ValueError(f"scheme must be 'euler' or 'verlet', got {scheme!r}")
        self._scheme = scheme

        # Internal state dict
        self._state: Dict[str, float] = {
            "theta": theta0,
            "omega": omega0,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def angular_acceleration(self, theta: float, omega: float) -> float:
        """Compute angular acceleration ``d²θ/dt²``.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        theta : float
            Current angular displacement (rad).
        omega : float
            Current angular velocity (rad/s).

        Returns
        -------
        float
            Angular acceleration (rad/s²).
        """
        raise NotImplementedError(
            "Subclasses must implement angular_acceleration(self, theta, omega)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def _deriv(self, theta: float, omega: float, t: float) -> float:
        """Adapter that calls the hook (ignores *t* for a time-independent
        pendulum, but accepts it for integrator compatibility)."""
        return self.angular_acceleration(theta, omega)

    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        Parameters
        ----------
        dt : float or None
            Step size.  Uses ``self.dt`` if None.
        """
        h = dt if dt is not None else self.dt
        stepper = verlet_step if self._scheme == "verlet" else euler_step

        # Map pendulum state (theta, omega) to integrator state (x, v)
        int_state = {
            "x": self._state["theta"],
            "v": self._state["omega"],
            "t": self._state["t"],
        }
        int_result = stepper(int_state, h, self._deriv)
        self._state = {
            "theta": int_result["x"],
            "omega": int_result["v"],
            "t": int_result["t"],
        }

    @property
    def state(self) -> Dict[str, float]:
        """Current simulation state ``{"theta", "omega", "t"}``."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Cartesian coordinates ``(x, y)`` of the bob.

        The pivot is at ``(0, 0)``; y points upward.
        """
        theta = self._state["theta"]
        x = self.length * math.sin(theta)
        y = -self.length * math.cos(theta)
        return (x, y)

    def energy(self) -> Dict[str, float]:
        """Kinetic and potential energy at the current state.

        Kinetic energy: ½ m L² ω²
        Gravitational PE: m g (L - y)  — zero at the bottom (θ = 0).

        Returns
        -------
        dict
            ``{"kinetic": ..., "potential": ..., "total": ...}``
        """
        omega = self._state["omega"]
        _, y = self.position()
        ke = 0.5 * self.mass * self.length**2 * omega**2
        pe = self.mass * self.g * (y + self.length)  # zero at bottom (y = -L)
        return {"kinetic": ke, "potential": pe, "total": ke + pe}

    @property
    def period_from_formula(self) -> float:
        """Small-angle period ``T = 2π √(L/g)``."""
        return 2.0 * math.pi * math.sqrt(self.length / self.g)


class ReferencePendulumSim(PendulumSim):
    """Reference pendulum with the correct physics.

    The angular acceleration is the exact non-linear expression
    ``-(g/L) sin(θ)``, or ``-(g/L) θ`` when *small_angle* is True.
    """

    def angular_acceleration(self, theta: float, omega: float) -> float:
        if self.small_angle:
            return -(self.g / self.length) * theta
        return -(self.g / self.length) * math.sin(theta)