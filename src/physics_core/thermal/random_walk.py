"""Random walk engine for modelling diffusion / gas molecule motion.

Provides a seeded, deterministic random walk in 1D or 2D with step-length
control, position history, RMS displacement, and a histogram helper.

Architecture
------------
:class:`RandomWalk` is a standalone engine (no abstract base / Reference
pattern needed — the physics is trivial).  It is consumed by the Manim
scene and could be used by a student exercise.

Physical background
-------------------
For a random walk of *N* steps of length *s* in *dim* dimensions:

    RMS displacement = s * sqrt(N)

This is the key result: the RMS distance from the origin grows as the
square root of the number of steps, not linearly.  This models diffusion
and the random motion of gas molecules.
"""

from __future__ import annotations

import math
from typing import Optional

import numpy as np


class RandomWalk:
    """Seeded deterministic random walk in 1D or 2D.

    Parameters
    ----------
    n_walkers : int
        Number of independent walkers.  Default 1.
    n_steps : int
        Number of steps per walker.  Default 100.
    step_length : float
        Step length *s*.  Default 1.0.
    dim : int
        Number of spatial dimensions (1 or 2).  Default 2.
    seed : int or None
        Random seed for reproducibility.  Default 42.
    """

    def __init__(
        self,
        n_walkers: int = 1,
        n_steps: int = 100,
        step_length: float = 1.0,
        dim: int = 2,
        seed: int = 42,
    ) -> None:
        if dim not in (1, 2):
            raise ValueError(f"dim must be 1 or 2, got {dim}")
        if n_walkers < 1:
            raise ValueError(f"n_walkers must be >= 1, got {n_walkers}")
        if n_steps < 1:
            raise ValueError(f"n_steps must be >= 1, got {n_steps}")
        if step_length <= 0.0:
            raise ValueError(f"step_length must be positive, got {step_length}")

        self.n_walkers = n_walkers
        self.n_steps = n_steps
        self.step_length = step_length
        self.dim = dim
        self._seed = seed

        # RNG — seeded for determinism
        rng = np.random.default_rng(seed)

        # Pre-generate all steps: shape (n_walkers, n_steps, dim)
        # Each step is a random direction on the unit sphere in dim dimensions.
        if dim == 1:
            # Random sign: +1 or -1 with equal probability
            directions = rng.choice([-1.0, 1.0], size=(n_walkers, n_steps, 1))
        else:
            # 2D: random angle on [0, 2π)
            angles = rng.uniform(0.0, 2.0 * math.pi, size=(n_walkers, n_steps))
            directions = np.stack(
                [np.cos(angles), np.sin(angles)], axis=-1
            )

        self._steps: np.ndarray = step_length * directions  # (W, N, dim)

        # Cumulative positions: shape (n_walkers, n_steps + 1, dim)
        # Start at origin for all walkers.
        self._positions: np.ndarray = np.zeros(
            (n_walkers, n_steps + 1, dim), dtype=np.float64
        )
        self._positions[:, 1:, :] = np.cumsum(self._steps, axis=1)

        # Displacement from origin at each step: shape (n_walkers, n_steps + 1)
        self._displacements: np.ndarray = np.linalg.norm(
            self._positions, axis=-1
        )

        # RMS displacement at each step: shape (n_steps + 1,)
        self._rms: np.ndarray = np.sqrt(
            np.mean(self._displacements**2, axis=0)
        )

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def positions(self) -> np.ndarray:
        """All walker positions at all steps.

        Returns
        -------
        ndarray, shape (n_walkers, n_steps + 1, dim)
            ``positions[w, s]`` is the position of walker *w* after *s* steps
            (``s=0`` is the origin).
        """
        return self._positions.copy()

    @property
    def steps(self) -> np.ndarray:
        """Step vectors.

        Returns
        -------
        ndarray, shape (n_walkers, n_steps, dim)
            ``steps[w, s]`` is the *s*-th step vector of walker *w*.
        """
        return self._steps.copy()

    @property
    def displacements(self) -> np.ndarray:
        """Distance from origin for each walker at each step.

        Returns
        -------
        ndarray, shape (n_walkers, n_steps + 1)
        """
        return self._displacements.copy()

    @property
    def rms(self) -> np.ndarray:
        """RMS displacement at each step.

        Returns
        -------
        ndarray, shape (n_steps + 1,)
            ``rms[s]`` is the RMS displacement after *s* steps.
        """
        return self._rms.copy()

    @property
    def rms_theoretical(self) -> np.ndarray:
        """Theoretical RMS displacement: ``step_length * sqrt(N)``.

        Returns
        -------
        ndarray, shape (n_steps + 1,)
        """
        return self.step_length * np.sqrt(np.arange(self.n_steps + 1, dtype=np.float64))

    def final_displacement_distribution(
        self, bins: int = 20
    ) -> tuple[np.ndarray, np.ndarray]:
        """Histogram of final displacements (after all steps).

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
        final_d = self._displacements[:, -1]
        counts, bin_edges = np.histogram(final_d, bins=bins, density=False)
        return counts, bin_edges

    def position_distribution_at_step(
        self, step: int, bins: int = 20
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Histogram of x and y positions at a given step (2D only).

        Parameters
        ----------
        step : int
            Step index (0 to n_steps).
        bins : int
            Number of bins per axis.  Default 20.

        Returns
        -------
        x_counts : ndarray
        x_edges : ndarray
        y_counts : ndarray
        y_edges : ndarray

        Raises
        ------
        ValueError
            If dim != 2.
        """
        if self.dim != 2:
            raise ValueError("position_distribution_at_step requires dim=2")
        x_vals = self._positions[:, step, 0]
        y_vals = self._positions[:, step, 1]
        x_counts, x_edges = np.histogram(x_vals, bins=bins, density=False)
        y_counts, y_edges = np.histogram(y_vals, bins=bins, density=False)
        return x_counts, x_edges, y_counts, y_edges