"""Special relativity simulation with dependency-injection hooks.

Architecture
------------
:class:`RelativityEngine` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines four physics **hooks**:

    ``lorentz_factor(self, v) -> float``
    ``time_dilated(self, v, t0) -> float``
    ``length_contracted(self, v, l0) -> float``
    ``lorentz_transform(self, v, t, x) -> tuple[float, float]``

that raise ``NotImplementedError`` by default.  Subclasses override the
hooks to supply the physics — students fill them in, while
:class:`ReferenceRelativityEngine` provides the correct reference
implementation.

Physical constants
------------------
``C`` — speed of light in vacuum (3.0e8 m/s).
"""

from __future__ import annotations

import math
from typing import Tuple

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
C: float = 3.0e8  # speed of light (m/s)


class RelativityEngine:
    """Abstract base special-relativity simulation.

    Parameters
    ----------
    c : float
        Speed of light (m/s).  Default 3.0e8.
    """

    def __init__(self, c: float = C) -> None:
        self.c: float = c

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------

    def lorentz_factor(self, v: float) -> float:
        """Compute the Lorentz factor γ = 1 / sqrt(1 - v²/c²).

        Parameters
        ----------
        v : float
            Relative velocity between frames (m/s).  Must satisfy |v| < c.

        Returns
        -------
        float
            Lorentz factor γ (dimensionless, ≥ 1).
        """
        raise NotImplementedError(
            "Subclasses must implement lorentz_factor(self, v)"
        )

    def time_dilated(self, v: float, t0: float) -> float:
        """Compute the dilated time interval Δt = γ · t0.

        Parameters
        ----------
        v : float
            Relative velocity (m/s).
        t0 : float
            Proper time interval (s) — time measured in the rest frame.

        Returns
        -------
        float
            Dilated time interval (s) — time measured in the moving frame.
        """
        raise NotImplementedError(
            "Subclasses must implement time_dilated(self, v, t0)"
        )

    def length_contracted(self, v: float, l0: float) -> float:
        """Compute the contracted length l = l0 / γ.

        Parameters
        ----------
        v : float
            Relative velocity (m/s).
        l0 : float
            Proper length (m) — length measured in the rest frame.

        Returns
        -------
        float
            Contracted length (m) — length measured in the moving frame.
        """
        raise NotImplementedError(
            "Subclasses must implement length_contracted(self, v, l0)"
        )

    def lorentz_transform(
        self, v: float, t: float, x: float
    ) -> Tuple[float, float]:
        """Lorentz-transform an event (t, x) from the rest frame to a frame
        moving at velocity *v*.

        The transformation is:

            t' = γ (t - v x / c²)
            x' = γ (x - v t)

        Parameters
        ----------
        v : float
            Relative velocity of the moving frame (m/s).  Positive = frame
            moves in the +x direction.
        t : float
            Time coordinate of the event in the rest frame (s).
        x : float
            Spatial coordinate of the event in the rest frame (m).

        Returns
        -------
        tuple[float, float]
            ``(t_prime, x_prime)`` — coordinates in the moving frame.
        """
        raise NotImplementedError(
            "Subclasses must implement lorentz_transform(self, v, t, x)"
        )


class ReferenceRelativityEngine(RelativityEngine):
    """Reference special-relativity implementation with correct physics.

    Formulas
    --------
    Lorentz factor:
        γ = 1 / sqrt(1 - β²),   β = v / c

    Time dilation:
        Δt = γ · Δt₀

    Length contraction:
        l = l₀ / γ

    Lorentz transformation (boost along +x):
        t' = γ (t - β x / c)
        x' = γ (x - v t)
    """

    def lorentz_factor(self, v: float) -> float:
        beta: float = v / self.c
        if abs(beta) >= 1.0:
            raise ValueError(f"|v/c| must be < 1, got {beta}")
        return 1.0 / math.sqrt(1.0 - beta * beta)

    def time_dilated(self, v: float, t0: float) -> float:
        return self.lorentz_factor(v) * t0

    def length_contracted(self, v: float, l0: float) -> float:
        return l0 / self.lorentz_factor(v)

    def lorentz_transform(
        self, v: float, t: float, x: float
    ) -> Tuple[float, float]:
        gamma: float = self.lorentz_factor(v)
        beta: float = v / self.c
        t_prime: float = gamma * (t - beta * x / self.c)
        x_prime: float = gamma * (x - v * t)
        return (t_prime, x_prime)