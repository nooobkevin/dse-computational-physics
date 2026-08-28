"""Doppler shift simulation with dependency-injection hooks.

Architecture
------------
:class:`DopplerShift` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It implements framework methods (``step``, ``state``, ``position``,
``energy``) and defines four physics **hooks**:

    ``observed_frequency(self, v) -> float``
    ``redshift(self, v) -> float``
    ``velocity_from_z(self, z) -> float``
    ``hubble_velocity(self, distance, H0) -> float``

that raise ``NotImplementedError`` by default.  Subclasses override the
hooks to supply the physics — students fill them in, while
:class:`ReferenceDopplerShift` provides the correct reference implementation.

State representation
--------------------
Internal state is a dict ``{"t": ..., "v": ..., "s": ...}`` where *v* is the
relative line-of-sight velocity (positive = receding) and *s* is the
line-of-sight distance travelled.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
C = 3.0e8  # speed of light (m/s)
H0 = 67.8  # Hubble constant (km/s per Mpc)
H_PLANCK = 6.62607015e-34  # Planck constant (J·s)


class DopplerShift:
    """Abstract base Doppler-shift simulation.

    Parameters
    ----------
    f0 : float
        Source rest frequency (Hz).  Default 5.8e14 (visible light ~517 nm).
    v : float
        Initial relative line-of-sight velocity (m/s).  Positive = receding
        (redshift), negative = approaching (blueshift).  Default 0.0.
    c : float
        Speed of light (m/s).  Default 3.0e8.
    dt : float
        Default time-step (s).  Default 0.01.
    """

    def __init__(
        self,
        f0: float = 5.8e14,
        v: float = 0.0,
        c: float = C,
        dt: float = 0.01,
    ) -> None:
        self.f0 = f0
        self.c = c
        self.dt = dt

        # Internal state dict
        self._state: Dict[str, float] = {
            "t": 0.0,
            "v": v,
            "s": 0.0,  # line-of-sight distance travelled (m)
        }

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------
    def observed_frequency(self, v: float) -> float:
        """Compute the observed frequency for a given relative velocity.

        Parameters
        ----------
        v : float
            Relative line-of-sight velocity (m/s).  Positive = receding.

        Returns
        -------
        float
            Observed frequency (Hz).
        """
        raise NotImplementedError(
            "Subclasses must implement observed_frequency(self, v)"
        )

    def redshift(self, v: float) -> float:
        """Compute the redshift *z* for a given relative velocity.

        Redshift is defined as *z = (λ_obs - λ_source) / λ_source*.

        Parameters
        ----------
        v : float
            Relative line-of-sight velocity (m/s).  Positive = receding.

        Returns
        -------
        float
            Redshift *z* (dimensionless).
        """
        raise NotImplementedError(
            "Subclasses must implement redshift(self, v)"
        )

    def velocity_from_z(self, z: float) -> float:
        """Compute the relative velocity from a given redshift *z*.

        Parameters
        ----------
        z : float
            Redshift (dimensionless).

        Returns
        -------
        float
            Relative line-of-sight velocity (m/s).
        """
        raise NotImplementedError(
            "Subclasses must implement velocity_from_z(self, z)"
        )

    def hubble_velocity(self, distance: float, H0: float = H0) -> float:
        """Compute the Hubble-flow velocity at a given distance.

        Parameters
        ----------
        distance : float
            Distance to the galaxy (Mpc).
        H0 : float
            Hubble constant (km/s per Mpc).  Default 67.8.

        Returns
        -------
        float
            Recession velocity (km/s).
        """
        raise NotImplementedError(
            "Subclasses must implement hubble_velocity(self, distance, H0)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        Advances the internal time counter and updates the line-of-sight
        distance travelled.  The relative velocity *v* is held constant
        (consumers may set ``self._state["v"]`` directly to sweep it).

        Parameters
        ----------
        dt : float or None
            Step size.  Uses ``self.dt`` if None.
        """
        h = dt if dt is not None else self.dt
        v = self._state["v"]
        self._state["t"] += h
        self._state["s"] += v * h

    @property
    def state(self) -> Dict[str, float]:
        """Current simulation state ``{"t", "v", "s"}``."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Line-of-sight position ``(s, 0)`` of the source.

        *s* is the distance travelled along the line of sight (m).
        """
        return (self._state["s"], 0.0)

    def energy(self) -> Dict[str, float]:
        """Photon energy at the current state.

        Returns
        -------
        dict
            ``{"frequency": f_obs, "photon_energy": h * f_obs}``
        """
        v = self._state["v"]
        f_obs = self.observed_frequency(v)
        return {"frequency": f_obs, "photon_energy": H_PLANCK * f_obs}


class ReferenceDopplerShift(DopplerShift):
    """Reference Doppler shift with correct relativistic physics.

    The relativistic Doppler formula for light (source receding, β = v/c > 0):

        f_obs = f_source * sqrt((1 - β) / (1 + β))   # < f_source  → redshift

    for an approaching source replace β with -β, giving
    f_obs = f_source * sqrt((1 + β) / (1 - β))  → blueshift.

    The redshift *z* is:

        z = (λ_obs - λ_source) / λ_source = sqrt((1 + β) / (1 - β)) - 1

    Low-velocity approximation (|v| << c):

        Δλ / λ ≈ v / c          (redshift)
        f_obs ≈ f_source * (1 - v/c)   (receding, v > 0)
    """

    def observed_frequency(self, v: float) -> float:
        beta = v / self.c
        if abs(beta) >= 1.0:
            raise ValueError(f"|v/c| must be < 1, got {beta}")
        # Relativistic Doppler: f_obs = f0 * sqrt((1 - β)/(1 + β))
        # v > 0 (receding) → f_obs < f0 (redshift)
        # v < 0 (approaching) → f_obs > f0 (blueshift)
        return self.f0 * math.sqrt((1.0 - beta) / (1.0 + beta))

    def redshift(self, v: float) -> float:
        beta = v / self.c
        if abs(beta) >= 1.0:
            raise ValueError(f"|v/c| must be < 1, got {beta}")
        return math.sqrt((1.0 + beta) / (1.0 - beta)) - 1.0

    def velocity_from_z(self, z: float) -> float:
        if z < -1.0:
            raise ValueError(f"z must be >= -1, got {z}")
        # Relativistic inverse: v = c * ((z+1)² - 1) / ((z+1)² + 1)
        return self.c * ((z + 1.0) ** 2 - 1.0) / ((z + 1.0) ** 2 + 1.0)

    def hubble_velocity(self, distance: float, H0: float = H0) -> float:
        return H0 * distance