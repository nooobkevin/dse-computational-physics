"""Gas simulation with dependency-injection hooks for molecular dynamics.

Architecture
------------
:class:`GasSim` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It implements framework methods (``step``, ``state``, ``position``,
``energy``) and defines two physics **hooks**:

    ``_collide_wall(self, positions, velocities) -> (positions, velocities)``
    ``_collide_particle(self, positions, velocities) -> velocities``

that raise ``NotImplementedError`` by default.  Subclasses override the
hooks to supply the physics — students fill them in, while
:class:`ReferenceGasSim` provides the correct reference implementation.

State representation
--------------------
Internal state uses NumPy arrays of shape ``(N, dim)`` for positions and
velocities.  The generic integrators in :mod:`physics_core.integrators`
are not used directly because the gas simulation operates on N particles
simultaneously with array operations.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Physical constants (simulation units)
# ---------------------------------------------------------------------------
KB = 1.0  # Boltzmann constant (simulation units)


class GasSim:
    """Abstract base gas simulation (molecular dynamics).

    Holds *N* rigid particles in a 2D box of side length *L*.  Particles
    move freely between collisions.  Two physics hooks let subclasses
    supply the collision logic.

    Parameters
    ----------
    N : int
        Number of particles.  Default 100.
    L : float
        Box side length.  Default 10.0.
    m : float
        Particle mass.  Default 1.0.
    T : float
        Initial temperature (determines initial velocity distribution).
        Default 1.0.
    dt : float
        Default time-step.  Default 0.01.
    scheme : str
        Integration scheme — ``"euler"`` or ``"verlet"`` (default).
    dim : int
        Number of spatial dimensions (2 or 3).  Default 2.
    seed : int or None
        Random seed for reproducibility.  Default None.
    """

    def __init__(
        self,
        N: int = 100,
        L: float = 10.0,
        m: float = 1.0,
        T: float = 1.0,
        dt: float = 0.01,
        scheme: str = "verlet",
        dim: int = 2,
        seed: Optional[int] = None,
    ) -> None:
        self.N = N
        self.L = L
        self.m = m
        self.T = T
        self.dt = dt
        self.dim = dim
        self.kB = KB

        if scheme not in ("euler", "verlet"):
            raise ValueError(f"scheme must be 'euler' or 'verlet', got {scheme!r}")
        self._scheme = scheme

        # RNG
        rng = np.random.default_rng(seed)

        # Initial positions: uniform random in [0, L]^dim
        self._positions: np.ndarray = rng.uniform(0.0, L, size=(N, dim)).astype(
            np.float64
        )

        # Initial velocities: Gaussian with variance kB*T/m per component
        sigma = math.sqrt(KB * T / m)
        self._velocities: np.ndarray = rng.normal(0.0, sigma, size=(N, dim)).astype(
            np.float64
        )

        # Remove centre-of-mass drift (only for N > 1)
        if N > 1:
            self._velocities -= np.mean(self._velocities, axis=0)

        self._t: float = 0.0

        # Effective particle radius for collision detection
        self._particle_radius: float = 0.1

        # Cumulative wall momentum transfer (for pressure calculation)
        self._momentum_transfer: float = 0.0

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------

    def _collide_wall(
        self, positions: np.ndarray, velocities: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Check and resolve particle-wall collisions.

        Parameters
        ----------
        positions : ndarray, shape (N, dim)
            Current particle positions.
        velocities : ndarray, shape (N, dim)
            Current particle velocities.

        Returns
        -------
        positions : ndarray
            Updated positions after wall collision resolution.
        velocities : ndarray
            Updated velocities after wall collision resolution.
        """
        raise NotImplementedError(
            "Subclasses must implement _collide_wall(self, positions, velocities)"
        )

    def _collide_particle(
        self, positions: np.ndarray, velocities: np.ndarray
    ) -> np.ndarray:
        """Check and resolve elastic particle-particle collisions.

        Parameters
        ----------
        positions : ndarray, shape (N, dim)
            Current particle positions.
        velocities : ndarray, shape (N, dim)
            Current particle velocities.

        Returns
        -------
        velocities : ndarray
            Updated velocities after particle collision resolution.
        """
        raise NotImplementedError(
            "Subclasses must implement _collide_particle(self, positions, velocities)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------

    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        For free particles (no inter-particle forces), the Verlet scheme
        reduces to: position update, collision handling, velocity update.
        The Euler scheme does the same but without the half-step structure.

        Parameters
        ----------
        dt : float or None
            Step size.  Uses ``self.dt`` if None.
        """
        h = dt if dt is not None else self.dt

        if self._scheme == "verlet":
            # Verlet integration for free particles (a=0 everywhere)
            # Half-step velocity: v(t+dt/2) = v(t) + (dt/2)*a(t) = v(t)
            # Full-step position: x(t+dt) = x(t) + dt*v(t+dt/2)
            self._positions += h * self._velocities

            # Handle collisions
            self._positions, self._velocities = self._collide_wall(
                self._positions, self._velocities
            )
            self._velocities = self._collide_particle(
                self._positions, self._velocities
            )

            # Full-step velocity: v(t+dt) = v(t+dt/2) + (dt/2)*a(t+dt) = v(t+dt/2)
        else:
            # Euler: x(t+dt) = x(t) + dt*v(t)
            self._positions += h * self._velocities

            # Handle collisions
            self._positions, self._velocities = self._collide_wall(
                self._positions, self._velocities
            )
            self._velocities = self._collide_particle(
                self._positions, self._velocities
            )

        self._t += h

    @property
    def state(self) -> Dict[str, Any]:
        """Current simulation state.

        Returns
        -------
        dict
            ``{"positions": ndarray, "velocities": ndarray,
              "t": float, "energies": dict}``
        """
        return {
            "positions": self._positions.copy(),
            "velocities": self._velocities.copy(),
            "t": self._t,
            "energies": self.energy(),
        }

    @property
    def position(self) -> np.ndarray:
        """Current particle positions, shape ``(N, dim)``."""
        return self._positions.copy()

    def energy(self) -> Dict[str, float]:
        """Kinetic energy of the system.

        Returns
        -------
        dict
            ``{"kinetic": ..., "total": ...}``  (no potential energy for
            free particles).
        """
        ke = 0.5 * self.m * float(np.sum(self._velocities**2))
        return {"kinetic": ke, "total": ke}


class ReferenceGasSim(GasSim):
    """Reference gas simulation with correct physics.

    Provides:
    - Perfectly elastic wall collisions (velocity reflection)
    - Perfectly elastic particle-particle collisions (equal-mass exchange)
    - Pressure computed from cumulative wall momentum transfer
    - Speed distribution histogram
    - Average and RMS speed
    - Temperature estimated from average kinetic energy (equipartition)

    Parameters
    ----------
    particle_radius : float
        Effective particle radius for collision detection.  Default 0.5.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Extract particle_radius before passing to super
        self._particle_radius = kwargs.pop("particle_radius", 0.1)
        super().__init__(*args, **kwargs)
        # Reset momentum transfer (super init may have set it)
        self._momentum_transfer = 0.0

    # ------------------------------------------------------------------
    # Physics hook implementations
    # ------------------------------------------------------------------

    def _collide_wall(
        self, positions: np.ndarray, velocities: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Perfectly elastic wall collisions.

        Particles that cross a wall boundary are reflected: the velocity
        component normal to the wall is reversed, and the position is
        mirrored back inside the box.  Momentum transfer is accumulated
        for pressure calculation.
        """
        eps = 1e-10
        for d in range(self.dim):
            # Left / lower wall (coordinate = 0)
            mask_low = positions[:, d] < -eps
            if np.any(mask_low):
                self._momentum_transfer += 2.0 * self.m * float(
                    np.sum(np.abs(velocities[mask_low, d]))
                )
                velocities[mask_low, d] = np.abs(velocities[mask_low, d])
                positions[mask_low, d] = -positions[mask_low, d]

            # Right / upper wall (coordinate = L)
            mask_high = positions[:, d] > self.L + eps
            if np.any(mask_high):
                self._momentum_transfer += 2.0 * self.m * float(
                    np.sum(np.abs(velocities[mask_high, d]))
                )
                velocities[mask_high, d] = -np.abs(velocities[mask_high, d])
                positions[mask_high, d] = 2.0 * self.L - positions[mask_high, d]

        return positions, velocities

    def _collide_particle(
        self, positions: np.ndarray, velocities: np.ndarray
    ) -> np.ndarray:
        """Elastic collisions between equal-mass particles.

        For each pair of particles whose centres are closer than
        ``2 * particle_radius``, the velocity component along the
        line of centres is exchanged (equal-mass elastic collision).
        """
        N = self.N
        min_dist = 2.0 * self._particle_radius

        for i in range(N):
            for j in range(i + 1, N):
                dr = positions[i] - positions[j]
                dist_sq = float(np.dot(dr, dr))
                if dist_sq < min_dist * min_dist and dist_sq > 1e-12:
                    dist = math.sqrt(dist_sq)
                    dv = velocities[i] - velocities[j]
                    v_rel = float(np.dot(dv, dr)) / dist
                    # Only collide if approaching
                    if v_rel < 0:
                        # Exchange velocity component along line of centres
                        impulse = (v_rel / dist) * dr
                        velocities[i] -= impulse
                        velocities[j] += impulse

        return velocities

    # ------------------------------------------------------------------
    # Thermodynamic observables
    # ------------------------------------------------------------------

    def pressure(self) -> float:
        """Time-averaged pressure from cumulative wall momentum transfer.

        In 2D/3D, the pressure on the walls is:

            P = (total momentum transfer) / (time * total wall area)

        where total wall area = 2 * dim * L^(dim-1)  (perimeter in 2D,
        surface area in 3D).

        Returns
        -------
        float
            Pressure in simulation units.
        """
        if self._t < 1e-12:
            return 0.0
        if self.dim == 2:
            wall_area = 2.0 * self.dim * self.L  # perimeter
        else:
            wall_area = 2.0 * self.dim * self.L ** (self.dim - 1)
        return self._momentum_transfer / (self._t * wall_area)

    def speed_distribution(
        self, bins: int = 20
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Histogram of particle speeds.

        Parameters
        ----------
        bins : int
            Number of histogram bins.  Default 20.

        Returns
        -------
        counts : ndarray
            Bin counts.
        bin_edges : ndarray
            Bin edges (length ``bins + 1``).
        """
        speeds = np.linalg.norm(self._velocities, axis=1)
        counts, bin_edges = np.histogram(speeds, bins=bins, density=False)
        return counts, bin_edges

    @property
    def average_speed(self) -> float:
        """Mean particle speed."""
        speeds = np.linalg.norm(self._velocities, axis=1)
        return float(np.mean(speeds))

    @property
    def rms_speed(self) -> float:
        """Root-mean-square particle speed."""
        speeds = np.linalg.norm(self._velocities, axis=1)
        return float(np.sqrt(np.mean(speeds**2)))

    def temperature_from_ke(self) -> float:
        """Estimate temperature from average kinetic energy via equipartition.

        For *dim* dimensions, each particle has *dim* quadratic degrees of
        freedom:

            <KE_per_particle> = (dim / 2) * kB * T

        so:

            T = (2 / dim) * <KE_per_particle> / kB

        Returns
        -------
        float
            Estimated temperature.
        """
        ke_total = self.energy()["kinetic"]
        ke_per_particle = ke_total / self.N
        return (2.0 / self.dim) * ke_per_particle / self.kB

    def ideal_gas_pressure(self) -> float:
        """Theoretical pressure from ideal gas law ``P = N kB T / V``.

        For a 2D box, V = L^2 (area).  For 3D, V = L^3 (volume).

        Returns
        -------
        float
            Theoretical pressure.
        """
        if self.dim == 2:
            volume = self.L**2
        else:
            volume = self.L**3
        return self.N * self.kB * self.T / volume