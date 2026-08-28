"""Cellular-automaton complex-systems engine — epidemic SIR model.

Architecture
------------
This module provides a deterministic cellular-automaton epidemic model on an
N×M grid with three cell states:

- **Susceptible** (0) — healthy, can be infected by infected neighbours
- **Infected** (1) — currently infected, can spread to susceptible neighbours
- **Recovered** (2) — immune, cannot be re-infected

Each step:
1. Infected cells recover with probability *p_recover* (→ Recovered).
2. Infected cells infect each susceptible neighbour with probability
   *p_infect* per contact.
3. State transitions use a seeded RNG for reproducibility.

The engine follows the same pattern as :class:`~physics_core.inquiry.analysis.LinearFit`:
an abstract base (:class:`EpidemicModel`) defines the interface, while
:class:`ReferenceEpidemicModel` provides the cell-update logic.

Example
-------
>>> model = ReferenceEpidemicModel(
...     rows=50, cols=50, p_infect=0.3, p_recover=0.1, seed=42
... )
>>> counts = model.run(100)
>>> len(counts)  # 101 snapshots (initial + 100 steps)
101
>>> counts[0]  # (S, I, R) at t=0
(2499, 1, 0)
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Cell states (int constants for readability)
# ---------------------------------------------------------------------------
SUSCEPTIBLE: int = 0
INFECTED: int = 1
RECOVERED: int = 2


class EpidemicModel:
    """Abstract base for cellular-automaton epidemic models.

    Parameters
    ----------
    rows : int
        Number of grid rows.
    cols : int
        Number of grid columns.
    p_infect : float
        Probability that a susceptible cell becomes infected when an infected
        neighbour is present (per contact, per step).
    p_recover : float
        Probability that an infected cell recovers in one step.
    seed : Optional[int]
        RNG seed for deterministic behaviour.  ``None`` = non-deterministic.
        Default is 42.
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        p_infect: float,
        p_recover: float,
        seed: Optional[int] = 42,
    ) -> None:
        if rows < 3 or cols < 3:
            raise ValueError(
                f"Grid must be at least 3×3, got {rows}×{cols}"
            )
        if not (0.0 <= p_infect <= 1.0):
            raise ValueError(
                f"p_infect must be in [0, 1], got {p_infect}"
            )
        if not (0.0 <= p_recover <= 1.0):
            raise ValueError(
                f"p_recover must be in [0, 1], got {p_recover}"
            )

        self.rows: int = rows
        self.cols: int = cols
        self.p_infect: float = p_infect
        self.p_recover: float = p_recover

        # RNG
        self._rng = np.random.default_rng(seed)

        # Grid: 0= susceptible, 1= infected, 2= recovered
        self._grid: np.ndarray = np.full((rows, cols), SUSCEPTIBLE, dtype=np.int8)

        # Seed infection at the centre cell
        centre_r: int = rows // 2
        centre_c: int = cols // 2
        self._grid[centre_r, centre_c] = INFECTED

        # Per-step history
        self._step_counts: List[Tuple[int, int, int]] = []
        self._step: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def grid(self) -> np.ndarray:
        """Return a read-only copy of the current grid."""
        return self._grid.copy()

    @property
    def step_number(self) -> int:
        """Current step number (0 = initial state)."""
        return self._step

    def sir_counts(self) -> Tuple[int, int, int]:
        """Return ``(S, I, R)`` counts at the current state."""
        s = int(np.sum(self._grid == SUSCEPTIBLE))
        i = int(np.sum(self._grid == INFECTED))
        r = int(np.sum(self._grid == RECOVERED))
        return (s, i, r)

    def history(self) -> List[Tuple[int, int, int]]:
        """Return the per-step S/I/R count history (list of tuples)."""
        return list(self._step_counts)

    # ------------------------------------------------------------------
    # Physics hooks — subclasses override these for custom update logic
    # ------------------------------------------------------------------

    def _infect_neighbours(self, r: int, c: int) -> None:
        """Infect susceptible neighbours of cell (r, c).

        Subclasses override this to implement different infection dynamics.
        The default implementation (used by ReferenceEpidemicModel) infects
        each of the 4 orthogonal neighbours with probability *p_infect*.

        Parameters
        ----------
        r : int
            Row of the infected cell.
        c : int
            Column of the infected cell.
        """
        raise NotImplementedError("Subclasses must implement _infect_neighbours")

    def _update_cell(self, r: int, c: int) -> int:
        """Compute the next state for a single cell.

        Subclasses override this.  The default implementation:
        - Susceptible → Infected if an infected neighbour infects it.
        - Infected → Recovered with probability *p_recover*.
        - Recovered stays Recovered.

        Parameters
        ----------
        r : int
            Cell row.
        c : int
            Cell column.

        Returns
        -------
        int
            New cell state (SUSCEPTIBLE, INFECTED, or RECOVERED).
        """
        raise NotImplementedError("Subclasses must implement _update_cell")

    def step(self) -> None:
        """Advance the simulation by one time step."""
        raise NotImplementedError("Subclasses must implement step")

    def run(self, steps: int) -> List[Tuple[int, int, int]]:
        """Run the simulation for *steps* time steps.

        Parameters
        ----------
        steps : int
            Number of steps to run.

        Returns
        -------
        list of (S, I, R) tuples
            Per-step S/I/R counts **including** the initial state (t=0).
        """
        history: List[Tuple[int, int, int]] = [self.sir_counts()]
        for _ in range(steps):
            self.step()
            history.append(self.sir_counts())
        self._step_counts = history
        return history


# ======================================================================
# Reference implementation
# ======================================================================


class ReferenceEpidemicModel(EpidemicModel):
    """Deterministic cellular-automaton SIR epidemic on a 2-D grid.

    Infection spreads via 4-connectivity (von Neumann neighbourhood).
    Recovered cells are permanently immune.
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        p_infect: float = 0.3,
        p_recover: float = 0.1,
        seed: Optional[int] = 42,
    ) -> None:
        super().__init__(rows, cols, p_infect, p_recover, seed)
        self._step_counts = [self.sir_counts()]

    # ------------------------------------------------------------------
    # Neighbour offsets (4-connectivity)
    # ------------------------------------------------------------------
    _NEIGHBOUR_OFFSETS: List[Tuple[int, int]] = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
    ]

    def _infect_neighbours(self, r: int, c: int) -> None:
        """Infect susceptible neighbours of cell (r, c).

        Each orthogonal susceptible neighbour becomes infected with
        probability *p_infect*, using the seeded RNG.
        """
        for dr, dc in self._NEIGHBOUR_OFFSETS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self._grid[nr, nc] == SUSCEPTIBLE:
                    if self._rng.random() < self.p_infect:
                        self._grid[nr, nc] = INFECTED

    def _update_cell(self, r: int, c: int) -> int:
        """Compute the next state for a single cell.

        - Susceptible stays susceptible (infection is handled by
          infected neighbours in a separate pass).
        - Infected → Recovered with probability *p_recover*.
        - Recovered stays recovered.
        """
        current = self._grid[r, c]
        if current == INFECTED:
            if self._rng.random() < self.p_recover:
                return RECOVERED
            return INFECTED
        # Susceptible and recovered stay as-is (infected neighbours
        # are handled by _infect_neighbours before this pass)
        return current

    def step(self) -> None:
        """Advance the simulation by one time step.

        Two-pass update:
        1. Infected cells try to infect susceptible neighbours.
        2. Infected cells try to recover.
        (Both passes use the grid state *before* this step.)
        """
        # Phase 1: infection spread (from current infected cells)
        infected_positions = list(
            zip(*np.where(self._grid == INFECTED))
        )
        for r, c in infected_positions:
            self._infect_neighbours(r, c)

        # Phase 2: recovery (using the post-infection grid)
        new_grid = self._grid.copy()
        for r in range(self.rows):
            for c in range(self.cols):
                new_grid[r, c] = self._update_cell(r, c)
        self._grid = new_grid

        self._step += 1


# ---------------------------------------------------------------------------
# Standalone helpers
# ---------------------------------------------------------------------------


def basic_reproduction_number(
    p_infect: float,
    p_recover: float,
    effective_neighbours: int = 4,
) -> float:
    """Compute the basic reproduction number R₀ for the CA model.

    R₀ ≈ (p_infect × effective_neighbours) / p_recover

    When R₀ > 1 the infection grows; when R₀ < 1 it dies out.

    Parameters
    ----------
    p_infect : float
        Per-contact infection probability.
    p_recover : float
        Per-step recovery probability.
    effective_neighbours : int
        Effective number of susceptible neighbours (default 4 for
        von Neumann neighbourhood).

    Returns
    -------
    float
        The basic reproduction number.
    """
    if p_recover <= 0.0:
        return math.inf
    return (p_infect * effective_neighbours) / p_recover