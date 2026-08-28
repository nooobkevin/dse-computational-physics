"""Radioactive decay simulation with dependency-injection hooks.

Architecture
------------
:class:`DecaySim` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines one physics **hook**:

    ``decay_probability(self, dt) -> float``

that raises ``NotImplementedError`` by default.  Subclasses override the
hook to supply the physics — students fill it in, while
:class:`ReferenceDecaySim` provides the correct reference implementation
using both analytic and Monte Carlo methods.

State representation
--------------------
Internal state is a dict ``{"N": ..., "t": ..., "N0": ..., "T": ...}``.
"""

from __future__ import annotations

import math
import random
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
LN2 = math.log(2.0)


class DecaySim:
    """Abstract base radioactive-decay simulation.

    Parameters
    ----------
    N0 : int
        Initial number of nuclei.  Default 10000.
    half_life : float
        Half-life of the isotope (s).  Default 1.0.
    dt : float
        Simulation time-step (s).  Default 0.01.
    seed : int or None
        Random seed for reproducibility.  Default None.
    """

    def __init__(
        self,
        N0: int = 10000,
        half_life: float = 1.0,
        dt: float = 0.01,
        seed: int | None = None,
    ) -> None:
        self.N0 = N0
        self.T = half_life
        self.dt = dt
        self._N = N0
        self._t = 0.0
        self._history: List[Tuple[float, int]] = [(0.0, N0)]
        self._rng = random.Random(seed)

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def decay_probability(self, dt: float) -> float:
        """Compute the probability that a single nucleus decays in *dt*.

        For radioactive decay: p = 1 - exp(-λ dt) where λ = ln(2)/T.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        dt : float
            Time interval (s).

        Returns
        -------
        float
            Decay probability in [0, 1].
        """
        raise NotImplementedError(
            "Subclasses must implement decay_probability(self, dt)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        Uses Monte Carlo: each of the remaining N nuclei decays
        independently with probability ``decay_probability(dt)``.

        Parameters
        ----------
        dt : float or None
            Time-step (s).  Uses ``self.dt`` if None.
        """
        h = dt if dt is not None else self.dt
        p = self.decay_probability(h)
        # Monte Carlo: each nucleus decays with probability p
        decays = 0
        for _ in range(self._N):
            if self._rng.random() < p:
                decays += 1
        self._N -= decays
        self._t += h
        self._history.append((self._t, self._N))

    @property
    def state(self) -> Dict[str, float | int]:
        """Current simulation state ``{"N", "t", "N0", "T"}``."""
        return {"N": self._N, "t": self._t, "N0": self.N0, "T": self.T}

    @property
    def position(self) -> Tuple[float, float]:
        """Current position ``(t, N)`` — elapsed time vs remaining nuclei."""
        return (self._t, float(self._N))

    @property
    def energy(self) -> float:
        """Total energy released so far (arbitrary units).

        Proportional to the number of decays that have occurred.
        """
        return float(self.N0 - self._N)

    def nuclei_remaining(self) -> int:
        """Number of undecayed nuclei remaining."""
        return self._N

    def history(self) -> List[Tuple[float, int]]:
        """Full decay history as list of ``(t, N)`` pairs."""
        return list(self._history)

    def reset(self) -> None:
        """Reset the simulation to its initial state."""
        self._N = self.N0
        self._t = 0.0
        self._history = [(0.0, self.N0)]

    def half_life(self) -> float:
        """Estimate the half-life from the simulated (Monte Carlo) trajectory.

        Finds the first time at which N <= N0/2 by interpolating the
        history.  This is the computational-physics method — measuring
        half-life from simulated data rather than using the analytic *T*.
        """
        target = self.N0 / 2.0
        history = self._history
        for i in range(1, len(history)):
            t_prev, n_prev = history[i - 1]
            t_curr, n_curr = history[i]
            if n_curr <= target:
                # Linear interpolation
                if n_prev == n_curr:
                    return t_curr
                fraction = (n_prev - target) / (n_prev - n_curr)
                return t_prev + fraction * (t_curr - t_prev)
        # If never reached (shouldn't happen with enough steps), extrapolate
        return float("inf")


class ReferenceDecaySim(DecaySim):
    """Reference radioactive decay with correct physics.

    Provides both analytic and Monte Carlo methods.

    Analytic formula
    ----------------
        N(t) = N0 * (1/2)^(t / T)

    Monte Carlo method
    ------------------
        p = 1 - exp(-λ dt)    where λ = ln(2) / T

    Each nucleus decays independently with probability *p* per step.
    """

    def __init__(
        self,
        N0: int = 10000,
        half_life: float = 1.0,
        dt: float = 0.01,
        seed: int | None = None,
    ) -> None:
        super().__init__(N0=N0, half_life=half_life, dt=dt, seed=seed)
        self._lambda = LN2 / self.T

    # ------------------------------------------------------------------
    # Physics hook
    # ------------------------------------------------------------------
    def decay_probability(self, dt: float) -> float:
        """p = 1 - exp(-λ dt) where λ = ln(2) / T."""
        return 1.0 - math.exp(-self._lambda * dt)

    # ------------------------------------------------------------------
    # Analytic helpers
    # ------------------------------------------------------------------
    def analytic_N(self, t: float) -> float:
        """Return the analytic number of nuclei at time *t*.

        N(t) = N0 * (1/2)^(t / T)
        """
        return self.N0 * (0.5 ** (t / self.T))

    def analytic_curve(self, n_steps: int) -> List[Tuple[float, float]]:
        """Generate the full analytic decay curve.

        Returns a list of ``(t, N)`` pairs at uniform intervals up to
        ``n_steps * self.dt``.
        """
        curve: List[Tuple[float, float]] = []
        for i in range(n_steps + 1):
            t = i * self.dt
            curve.append((t, self.analytic_N(t)))
        return curve

    # ------------------------------------------------------------------
    # Derived quantities
    # ------------------------------------------------------------------
    @property
    def decay_constant(self) -> float:
        """Decay constant λ = ln(2) / T (s⁻¹)."""
        return self._lambda

    @property
    def mean_lifetime(self) -> float:
        """Mean lifetime τ = 1/λ = T / ln(2) (s)."""
        return 1.0 / self._lambda

    @property
    def activity(self) -> float:
        """Activity A = λN (decays per second, Bq).

        Returns the current activity based on the number of undecayed
        nuclei and the decay constant.
        """
        return self._lambda * self._N