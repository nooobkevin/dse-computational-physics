"""Orbital mechanics simulation with dependency-injection hooks.

Architecture
------------
:class:`OrbitSim` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines physics **hooks**:

    ``gravitational_force(self, r) -> float``
    ``orbital_velocity(self, r) -> float``
    ``escape_velocity(self, r) -> float``
    ``gravitational_potential_energy(self, r) -> float``
    ``total_energy(self, r, v) -> float``

that raise ``NotImplementedError`` by default.  Subclasses override the
hooks to supply the physics — students fill them in, while
:class:`ReferenceOrbitalBody` provides the correct reference implementation.

State representation
--------------------
Internal state is a dict ``{"x", "y", "vx", "vy", "t"}``.
The central mass is at the origin (0, 0).
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple

from physics_core.integrators import DerivFn, State, verlet_step


class OrbitSim:
    """Abstract base orbital mechanics simulation.

    Parameters
    ----------
    M : float
        Mass of the central body (kg).  Default 5.972e24 (Earth).
    m : float
        Mass of the orbiting body (kg).  Default 1000.0.
    G : float
        Gravitational constant (m³ kg⁻¹ s⁻²).  Default 6.67430e-11.
    x : float
        Initial x-position (m).  Default 7.0e6.
    y : float
        Initial y-position (m).  Default 0.0.
    vx : float
        Initial x-velocity (m/s).  Default 0.0.
    vy : float
        Initial y-velocity (m/s).  Default 7540.0 (circular at R=7e6).
    """

    def __init__(
        self,
        M: float = 5.972e24,
        m: float = 1000.0,
        G: float = 6.67430e-11,
        x: float = 7.0e6,
        y: float = 0.0,
        vx: float = 0.0,
        vy: float = 7540.0,
    ) -> None:
        self.M = M
        self.m = m
        self.G = G
        self._state: Dict[str, float] = {
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def radius(self) -> float:
        """Distance from the centre of the central body (m)."""
        return math.hypot(self._state["x"], self._state["y"])

    @property
    def speed(self) -> float:
        """Orbital speed (m/s)."""
        return math.hypot(self._state["vx"], self._state["vy"])

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------

    def gravitational_force(self, r: float) -> float:
        """Compute the magnitude of the gravitational force at distance *r*.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        r : float
            Distance from the centre of the central body (m).

        Returns
        -------
        float
            Gravitational force magnitude (N).
        """
        raise NotImplementedError(
            "Subclasses must implement gravitational_force(self, r)"
        )

    def orbital_velocity(self, r: float) -> float:
        """Compute the circular orbital velocity at distance *r*.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        r : float
            Orbital radius (m).

        Returns
        -------
        float
            Orbital velocity magnitude (m/s).
        """
        raise NotImplementedError(
            "Subclasses must implement orbital_velocity(self, r)"
        )

    def escape_velocity(self, r: float) -> float:
        """Compute the escape velocity at distance *r*.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        r : float
            Distance from the centre of the central body (m).

        Returns
        -------
        float
            Escape velocity magnitude (m/s).
        """
        raise NotImplementedError(
            "Subclasses must implement escape_velocity(self, r)"
        )

    def gravitational_potential_energy(self, r: float) -> float:
        """Compute the gravitational potential energy at distance *r*.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        r : float
            Distance from the centre of the central body (m).

        Returns
        -------
        float
            Gravitational potential energy (J).
        """
        raise NotImplementedError(
            "Subclasses must implement gravitational_potential_energy(self, r)"
        )

    def total_energy(self, r: float, v: float) -> float:
        """Compute the total mechanical energy at distance *r* and speed *v*.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        r : float
            Distance from the centre of the central body (m).
        v : float
            Speed (m/s).

        Returns
        -------
        float
            Total mechanical energy (J).
        """
        raise NotImplementedError(
            "Subclasses must implement total_energy(self, r, v)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------

    def _acceleration(self, _x: float, _v: float, _t: float) -> float:
        """Dummy 1D acceleration — not used; orbital uses 2D step."""
        return 0.0

    def step(self, dt: float | None = None) -> None:
        """Advance the orbital simulation by one time-step using Verlet integration.

        Uses the velocity-Verlet integrator from ``physics_core.integrators``
        for energy-conserving orbit integration.
        """
        h = dt if dt is not None else 10.0
        r = self.radius
        if r < 1.0:
            return  # crashed
        force_mag = self.gravitational_force(r)
        # Acceleration components: a = -G * M / r² * (r̂)
        ax = -force_mag / self.m * (self._state["x"] / r)
        ay = -force_mag / self.m * (self._state["y"] / r)

        # Velocity-Verlet in 2D
        x_state: State = {"x": self._state["x"], "v": self._state["vx"], "t": self._state["t"]}
        y_state: State = {"x": self._state["y"], "v": self._state["vy"], "t": self._state["t"]}

        def deriv_x(x: float, v: float, t: float) -> float:
            return ax if abs(x - self._state["x"]) < 1e-9 else (
                -self.gravitational_force(math.hypot(x, self._state["y"])) / self.m
                * (x / math.hypot(x, self._state["y"]))
            )

        def deriv_y(y: float, v: float, t: float) -> float:
            return ay if abs(y - self._state["y"]) < 1e-9 else (
                -self.gravitational_force(math.hypot(self._state["x"], y)) / self.m
                * (y / math.hypot(self._state["x"], y))
            )

        # Single-step Verlet
        x_new = verlet_step(x_state, h, deriv_x)
        y_new = verlet_step(y_state, h, deriv_y)

        self._state["x"] = x_new["x"]
        self._state["vx"] = x_new["v"]
        self._state["y"] = y_new["x"]
        self._state["vy"] = y_new["v"]
        self._state["t"] = x_new.get("t", self._state["t"] + h)

    @property
    def state(self) -> Dict[str, Any]:
        """Current simulation state."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Orbiting body position ``(x, y)`` (m)."""
        return (self._state["x"], self._state["y"])

    def energy_components(self) -> Dict[str, float]:
        """Kinetic, potential, and total energy at the current state."""
        r = self.radius
        v = self.speed
        ke = 0.5 * self.m * v * v
        gpe = self.gravitational_potential_energy(r)
        te = self.total_energy(r, v)
        return {"kinetic": ke, "potential": gpe, "total": te}


class ReferenceOrbitalBody(OrbitSim):
    """Reference orbital body with correct Newtonian gravity physics.

    For a central mass *M* and orbiting mass *m* at distance *r*:

        F = G M m / r²
        v_orb = √(G M / r)
        v_esc = √(2 G M / r)
        U = -G M m / r
        E_total = KE + U = ½ m v² - G M m / r
    """

    def gravitational_force(self, r: float) -> float:
        """F = G M m / r²."""
        if r <= 0.0:
            return 0.0
        return self.G * self.M * self.m / (r * r)

    def orbital_velocity(self, r: float) -> float:
        """v_orb = √(G M / r)."""
        if r <= 0.0:
            return 0.0
        return math.sqrt(self.G * self.M / r)

    def escape_velocity(self, r: float) -> float:
        """v_esc = √(2 G M / r)."""
        if r <= 0.0:
            return 0.0
        return math.sqrt(2.0 * self.G * self.M / r)

    def gravitational_potential_energy(self, r: float) -> float:
        """U = -G M m / r."""
        if r <= 0.0:
            return float("-inf")
        return -self.G * self.M * self.m / r

    def total_energy(self, r: float, v: float) -> float:
        """E = ½ m v² - G M m / r."""
        ke = 0.5 * self.m * v * v
        gpe = self.gravitational_potential_energy(r)
        return ke + gpe