"""Wave simulation with dependency-injection hooks.

Architecture
------------
:class:`WaveSim` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines framework methods (``step``, ``state``, ``position``,
``energy``) and physics **hooks** that raise ``NotImplementedError``.

:class:`ReferenceWaveSim` supplies the correct analytical physics:
traveling wave ``y(x,t) = A sin(kx - ωt)``, standing waves via
superposition of two counter-propagating traveling waves, and
intensity proportional to amplitude squared.

State representation
--------------------
Internal state is a dict ``{"t": ...}`` — the wave is purely analytical
so there is no ODE integration; ``step(dt)`` simply advances time.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple

import numpy as np


class WaveSim:
    """Abstract base wave simulation.

    Parameters
    ----------
    amplitude : float
        Wave amplitude A (m).
    wavelength : float
        Wavelength λ (m).
    frequency : float
        Frequency f (Hz).
    wave_speed : float
        Wave speed v (m/s).  If not given, computed from v = f λ.
    L : float
        Domain length (m).  Default 10.0.
    nx : int
        Number of spatial grid points.  Default 200.
    """

    def __init__(
        self,
        amplitude: float = 1.0,
        wavelength: float = 2.0,
        frequency: float = 1.0,
        wave_speed: Optional[float] = None,
        L: float = 10.0,
        nx: int = 200,
    ) -> None:
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.frequency = frequency
        self.L = L
        self.nx = nx

        # Derived quantities
        self.k = 2.0 * math.pi / wavelength  # wave number
        self.omega = 2.0 * math.pi * frequency  # angular frequency
        if wave_speed is not None:
            self.v = wave_speed
        else:
            self.v = frequency * wavelength  # v = f λ

        # Spatial grid
        self.x = np.linspace(0.0, L, nx)

        # Internal state
        self._state: Dict[str, float] = {"t": 0.0}

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------

    def displacement(self, x: float, t: float) -> float:
        """Return the wave displacement y(x, t) at a single point.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        x : float
            Spatial position (m).
        t : float
            Time (s).

        Returns
        -------
        float
            Displacement y(x, t) (m).
        """
        raise NotImplementedError(
            "Subclasses must implement displacement(self, x, t)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------

    def step(self, dt: float) -> None:
        """Advance the simulation by one time-step.

        Parameters
        ----------
        dt : float
            Time-step size (s).
        """
        self._state["t"] += dt

    @property
    def state(self) -> Dict[str, float]:
        """Current simulation state ``{"t": ...}``."""
        return dict(self._state)

    def field(self, x_array: np.ndarray, t: float) -> np.ndarray:
        """Return the wave displacement y(x, t) for an array of x positions.

        Parameters
        ----------
        x_array : np.ndarray
            Array of spatial positions (m).
        t : float
            Time (s).

        Returns
        -------
        np.ndarray
            Displacement y(x, t) for each x.
        """
        return np.array([self.displacement(float(xi), t) for xi in x_array])

    def position(self) -> Tuple[np.ndarray, np.ndarray]:
        """Return (x, y) arrays for the current wave profile.

        Returns
        -------
        tuple of np.ndarray
            (x_grid, y_profile) where y_profile = y(x, self._state["t"]).
        """
        t = self._state["t"]
        return self.x, self.field(self.x, t)

    def energy(self) -> Dict[str, float]:
        """Wave energy at the current state.

        For a wave, energy is proportional to amplitude squared.
        Returns a dict with ``"total"`` set to A² (arbitrary units).

        Returns
        -------
        dict
            ``{"total": ...}``
        """
        return {"total": self.amplitude**2}


class ReferenceWaveSim(WaveSim):
    """Reference wave with the correct analytical physics.

    Provides:
    - Traveling wave: ``y(x,t) = A sin(kx - ωt)``
    - Standing wave: superposition of two counter-propagating traveling waves
    - Intensity proportional to amplitude squared
    """

    def displacement(self, x: float, t: float) -> float:
        """Traveling wave displacement: ``y(x,t) = A sin(kx - ωt)``.

        Parameters
        ----------
        x : float
            Spatial position (m).
        t : float
            Time (s).

        Returns
        -------
        float
            Displacement y(x, t) (m).
        """
        return self.amplitude * math.sin(self.k * x - self.omega * t)

    def standing_wave(self, x: float, t: float) -> float:
        """Standing wave displacement via superposition.

        Two counter-propagating traveling waves of equal amplitude:
            y₁ = A sin(kx - ωt)
            y₂ = A sin(kx + ωt)
            y = y₁ + y₂ = 2A sin(kx) cos(ωt)

        Parameters
        ----------
        x : float
            Spatial position (m).
        t : float
            Time (s).

        Returns
        -------
        float
            Standing wave displacement y(x, t) (m).
        """
        return (
            self.amplitude * math.sin(self.k * x - self.omega * t)
            + self.amplitude * math.sin(self.k * x + self.omega * t)
        )

    def field(self, x_array: np.ndarray, t: float) -> np.ndarray:
        """Return the traveling wave displacement for an array of x positions.

        Parameters
        ----------
        x_array : np.ndarray
            Array of spatial positions (m).
        t : float
            Time (s).

        Returns
        -------
        np.ndarray
            Displacement y(x, t) for each x.
        """
        return self.amplitude * np.sin(self.k * x_array - self.omega * t)
