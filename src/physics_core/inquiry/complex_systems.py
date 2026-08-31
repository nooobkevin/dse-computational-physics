"""Cellular-automaton / agent-based complex-systems engines.

This module provides three deterministic complex-system models covering the
CAF Topic 9 "societal processes" — **disease transmission**, **forest fires**
and **crowd control**:

- :class:`EpidemicModel` / :class:`ReferenceEpidemicModel` — a cellular
  automaton SIR epidemic on an N×M grid.
- :class:`ForestFireModel` / :class:`ReferenceForestFire` — a cellular
  automaton forest fire with wind-biased spread.
- :class:`CrowdModel` / :class:`ReferenceCrowdModel` — an agent-based crowd
  evacuation through a single exit, with panic-dependent congestion.

Every model follows the same pattern as
:class:`~physics_core.inquiry.analysis.LinearFit`: an abstract base defines
the interface (plus shared bookkeeping such as ``run`` and count/metrics
history), while a ``Reference`` subclass provides the per-step update logic.
All stochastic engines are seeded and therefore deterministic by default.

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


# ---------------------------------------------------------------------------
# Forest-fire cellular automaton
# ---------------------------------------------------------------------------

# Forest-fire cell states
TREE: int = 0
EMPTY: int = 1
BURNING: int = 2
BURNED: int = 3


class ForestFireModel:
    """Abstract base for the forest-fire cellular automaton.

    An N×M grid of cells, each in one of four states — tree (0), empty (1),
    burning (2), burned (3).  Burning cells ignite neighbouring trees with
    probability *p_ignite*, biased by wind, and burn out (→ burned) after
    *burn_duration* steps; the fire therefore dies out once the fuel (trees)
    is exhausted.

    Subclasses implement :meth:`step` and the wind-dependent ignition
    probability hook :meth:`_ignition_probability`.
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        p_ignite: float = 0.3,
        wind_direction: int = 0,
        wind_bias: float = 0.0,
        burn_duration: int = 1,
        tree_density: float = 0.85,
        seed: Optional[int] = 42,
    ) -> None:
        if rows < 3 or cols < 3:
            raise ValueError(f"Grid must be at least 3×3, got {rows}×{cols}")
        if not (0.0 <= p_ignite <= 1.0):
            raise ValueError(f"p_ignite must be in [0, 1], got {p_ignite}")
        if wind_direction not in (0, 1, 2, 3):
            raise ValueError(
                f"wind_direction must be 0..3, got {wind_direction}"
            )
        if wind_bias < 0.0:
            raise ValueError(f"wind_bias must be >= 0, got {wind_bias}")
        if burn_duration < 1:
            raise ValueError(
                f"burn_duration must be >= 1, got {burn_duration}"
            )
        if not (0.0 <= tree_density <= 1.0):
            raise ValueError(
                f"tree_density must be in [0, 1], got {tree_density}"
            )

        self.rows: int = rows
        self.cols: int = cols
        self.p_ignite: float = p_ignite
        self.wind_direction: int = wind_direction
        self.wind_bias: float = wind_bias
        self.burn_duration: int = burn_duration
        self.tree_density: float = tree_density

        self._rng = np.random.default_rng(seed)

        # Random seeded forest (trees), rest empty.
        self._grid: np.ndarray = np.full(
            (rows, cols), EMPTY, dtype=np.int8
        )
        tree_mask = self._rng.random((rows, cols)) < tree_density
        self._grid[tree_mask] = TREE

        # Ignition at the centre cell — force fuel under the spark.
        centre_r: int = rows // 2
        centre_c: int = cols // 2
        if self._grid[centre_r, centre_c] == EMPTY:
            self._grid[centre_r, centre_c] = TREE
        self._grid[centre_r, centre_c] = BURNING

        # Remaining burn time per cell (0 = not burning).
        self._burn_age: np.ndarray = np.zeros(
            (rows, cols), dtype=np.int16
        )
        self._burn_age[centre_r, centre_c] = burn_duration

        self._step: int = 0
        self._step_counts: List[Tuple[int, int, int]] = []

    @property
    def grid(self) -> np.ndarray:
        """Return a read-only copy of the current grid."""
        return self._grid.copy()

    @property
    def step_number(self) -> int:
        """Current step number (0 = initial state)."""
        return self._step

    def fire_counts(self) -> Tuple[int, int, int]:
        """Return ``(trees, burning, burned)`` at the current state."""
        trees = int(np.sum(self._grid == TREE))
        burning = int(np.sum(self._grid == BURNING))
        burned = int(np.sum(self._grid == BURNED))
        return (trees, burning, burned)

    def history(self) -> List[Tuple[int, int, int]]:
        """Return the per-step (trees, burning, burned) history."""
        return list(self._step_counts)

    def _ignition_probability(self, dr: int, dc: int) -> float:
        """Ignition probability for a tree neighbour at offset (dr, dc)."""
        raise NotImplementedError(
            "Subclasses must implement _ignition_probability"
        )

    def step(self) -> None:
        """Advance the simulation by one time step."""
        raise NotImplementedError("Subclasses must implement step")

    def run(self, steps: int) -> List[Tuple[int, int, int]]:
        """Run for *steps* steps, returning per-step fire counts.

        The returned list includes the initial state (t=0).
        """
        history: List[Tuple[int, int, int]] = [self.fire_counts()]
        for _ in range(steps):
            self.step()
            history.append(self.fire_counts())
        self._step_counts = history
        return history


class ReferenceForestFire(ForestFireModel):
    """Deterministic forest-fire CA with wind-biased spread.

    Burning cells ignite each of their 8 neighbours; the ignition probability
    is *p_ignite* boosted toward the wind direction and suppressed upwind.
    A burning cell stays alight for *burn_duration* steps then becomes burned.
    """

    _NEIGHBOUR_OFFSETS: List[Tuple[int, int]] = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]
    _WIND_DIRECTIONS: Dict[int, Tuple[int, int]] = {
        0: (0, 1),    # east
        1: (1, 0),    # south
        2: (0, -1),   # west
        3: (-1, 0),   # north
    }

    def __init__(
        self,
        rows: int,
        cols: int,
        p_ignite: float = 0.3,
        wind_direction: int = 0,
        wind_bias: float = 0.0,
        burn_duration: int = 1,
        tree_density: float = 0.85,
        seed: Optional[int] = 42,
    ) -> None:
        super().__init__(
            rows,
            cols,
            p_ignite,
            wind_direction,
            wind_bias,
            burn_duration,
            tree_density,
            seed,
        )
        self._step_counts = [self.fire_counts()]

    def _ignition_probability(self, dr: int, dc: int) -> float:
        wind_dr, wind_dc = self._WIND_DIRECTIONS[self.wind_direction]
        base = self.p_ignite
        if (dr, dc) == (wind_dr, wind_dc):
            return min(1.0, base + self.wind_bias)
        if (dr, dc) == (-wind_dr, -wind_dc):
            return max(0.0, base - self.wind_bias * 0.5)
        if dr * wind_dr + dc * wind_dc > 0:
            return min(1.0, base + self.wind_bias * 0.5)
        return base

    def step(self) -> None:
        new_grid = self._grid.copy()
        new_age = self._burn_age.copy()
        burning = list(zip(*np.where(self._grid == BURNING)))
        for r, c in burning:
            for dr, dc in self._NEIGHBOUR_OFFSETS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self._grid[nr, nc] == TREE:
                        if self._rng.random() < self._ignition_probability(dr, dc):
                            new_grid[nr, nc] = BURNING
                            new_age[nr, nc] = self.burn_duration
            new_age[r, c] -= 1
            if new_age[r, c] <= 0:
                new_grid[r, c] = BURNED
        self._grid = new_grid
        self._burn_age = new_age
        self._step += 1


# ---------------------------------------------------------------------------
# Crowd evacuation agent model
# ---------------------------------------------------------------------------


class CrowdModel:
    """Abstract base for an agent-based crowd-evacuation model.

    *N* agents start inside a rectangular hall with a single exit in the
    middle of a wall (right wall by default).  Each step every active agent
    moves toward the exit; its speed is reduced by local crowding (more
    nearby agents → slower) and scaled by the *panic* parameter (higher panic
    → faster but with more pushing/collisions).  Agents reaching the exit
    opening are counted as exited.

    Subclasses implement :meth:`step` (movement + collision resolution).
    """

    def __init__(
        self,
        n_agents: int,
        hall_width: float = 10.0,
        hall_height: float = 6.0,
        exit_size: float = 1.0,
        base_speed: float = 1.0,
        panic: float = 0.0,
        neighbour_radius: float = 0.8,
        agent_radius: float = 0.12,
        exit_radius: float = 1.0,
        exit_on: str = "right",
        seed: Optional[int] = 42,
        init_positions: Optional[np.ndarray] = None,
    ) -> None:
        if n_agents < 1:
            raise ValueError(f"n_agents must be >= 1, got {n_agents}")
        if hall_width <= 0 or hall_height <= 0:
            raise ValueError("hall dimensions must be positive")
        if exit_size <= 0:
            raise ValueError(f"exit_size must be > 0, got {exit_size}")
        if base_speed <= 0:
            raise ValueError(f"base_speed must be > 0, got {base_speed}")
        if panic < 0.0:
            raise ValueError(f"panic must be >= 0, got {panic}")
        if neighbour_radius <= 0:
            raise ValueError("neighbour_radius must be > 0")
        if agent_radius <= 0:
            raise ValueError("agent_radius must be > 0")
        if exit_radius <= 0:
            raise ValueError("exit_radius must be > 0")
        if exit_on not in ("right", "top"):
            raise ValueError(
                f"exit_on must be 'right' or 'top', got {exit_on}"
            )

        self.n_agents: int = n_agents
        self.hall_width: float = hall_width
        self.hall_height: float = hall_height
        self.exit_size: float = exit_size
        self.base_speed: float = base_speed
        self.panic: float = panic
        self.neighbour_radius: float = neighbour_radius
        self.agent_radius: float = agent_radius
        self.exit_radius: float = exit_radius
        self.exit_on: str = exit_on

        self._rng = np.random.default_rng(seed)

        # Exit centre + opening half-width along the wall.
        if exit_on == "right":
            self._exit_centre: np.ndarray = np.array(
                [hall_width, hall_height / 2.0]
            )
            self._exit_half: float = exit_size / 2.0
        else:  # top
            self._exit_centre = np.array([hall_width / 2.0, hall_height])
            self._exit_half = exit_size / 2.0

        if init_positions is not None:
            arr = np.asarray(init_positions, dtype=np.float64)
            if arr.shape != (n_agents, 2):
                raise ValueError(
                    f"init_positions must have shape {(n_agents, 2)}, "
                    f"got {arr.shape}"
                )
            lo, hi = np.asarray([0.0, 0.0]), np.asarray(
                [hall_width, hall_height]
            )
            if np.any(arr < lo) or np.any(arr > hi):
                raise ValueError("init_positions must lie inside the hall")
            self._positions: np.ndarray = arr
        else:
            self._positions = np.column_stack(
                [
                    self._rng.uniform(0.0, hall_width, n_agents),
                    self._rng.uniform(0.0, hall_height, n_agents),
                ]
            )

        self._exited: np.ndarray = np.zeros(n_agents, dtype=bool)
        self._last_mean_speed: float = 0.0
        self._step: int = 0
        self._step_metrics: List[Tuple[float, int, int]] = []

    @property
    def positions(self) -> np.ndarray:
        """Return a read-only copy of all agent positions."""
        return self._positions.copy()

    @property
    def exited(self) -> np.ndarray:
        """Return a read-only copy of the exited-agent boolean array."""
        return self._exited.copy()

    @property
    def step_number(self) -> int:
        """Current step number (0 = initial state)."""
        return self._step

    def crowd_metrics(self) -> Tuple[float, int, int]:
        """Return ``(mean_speed, exited, bottleneck_pressure)``.

        ``mean_speed`` is the mean step speed of active agents; ``exited`` is
        the number of agents that have reached the exit; ``bottleneck_pressure``
        is the number of active agents within *exit_radius* of the exit.
        """
        active = ~self._exited
        dx = self._positions[:, 0] - self._exit_centre[0]
        dy = self._positions[:, 1] - self._exit_centre[1]
        dist = np.hypot(dx, dy)
        pressure = int(np.sum(active & (dist < self.exit_radius)))
        exited = int(np.sum(self._exited))
        return (self._last_mean_speed, exited, pressure)

    def history(self) -> List[Tuple[float, int, int]]:
        """Return the per-step (mean_speed, exited, bottleneck) history."""
        return list(self._step_metrics)

    def step(self) -> None:
        """Advance the simulation by one time step."""
        raise NotImplementedError("Subclasses must implement step")

    def run(self, steps: int) -> List[Tuple[float, int, int]]:
        """Run for *steps* steps, returning per-step crowd metrics.

        The returned list includes the initial state (t=0).
        """
        history: List[Tuple[float, int, int]] = [self.crowd_metrics()]
        for _ in range(steps):
            self.step()
            history.append(self.crowd_metrics())
        self._step_metrics = history
        return history


class ReferenceCrowdModel(CrowdModel):
    """Deterministic agent-based crowd evacuation with panic congestion.

    Agents move toward the single exit, slowing as crowding grows.  Panic
    raises the desired speed and the pushing force applied during collision
    resolution.  A small deterministic per-agent jitter (seeded, indexed in
    agent order) breaks symmetry, so the crowd always resolves and everyone
    eventually exits.
    """

    # Speed damping: more neighbours within *neighbour_radius* → slower.
    _DAMPING_COEFF: float = 0.6
    # Maximum push applied per collision resolution step.
    _PUSH_CAP: float = 0.4
    # Jitter angle magnitude (radians) used to break symmetry.
    _JITTER_AMP: float = 0.12

    def __init__(
        self,
        n_agents: int,
        hall_width: float = 10.0,
        hall_height: float = 6.0,
        exit_size: float = 1.0,
        base_speed: float = 1.0,
        panic: float = 0.0,
        neighbour_radius: float = 0.8,
        agent_radius: float = 0.12,
        exit_radius: float = 1.0,
        exit_on: str = "right",
        seed: Optional[int] = 42,
        init_positions: Optional[np.ndarray] = None,
    ) -> None:
        super().__init__(
            n_agents,
            hall_width,
            hall_height,
            exit_size,
            base_speed,
            panic,
            neighbour_radius,
            agent_radius,
            exit_radius,
            exit_on,
            seed,
            init_positions,
        )
        self._step_metrics = [self.crowd_metrics()]

    def step(self) -> None:
        n = self.n_agents
        pos = self._positions
        exited = self._exited
        active_idx = [i for i in range(n) if not exited[i]]
        if not active_idx:
            self._last_mean_speed = 0.0
            self._step += 1
            return

        # Pre-move positions (needed for continuous exit crossing tests).
        old_pos = self._positions.copy()

        desired_speed = self.base_speed * (1.0 + self.panic)
        min_sep = 2.0 * self.agent_radius
        ex, ey = self._exit_centre
        speeds = np.zeros(n, dtype=np.float64)

        # 1. Move each active agent toward the exit (index order = tie-break).
        for i in active_idx:
            px, py = pos[i]
            dx, dy = ex - px, ey - py
            dist = math.hypot(dx, dy)
            if dist > 1e-9:
                dirx, diry = dx / dist, dy / dist
            else:
                dirx, diry = 0.0, 0.0
            count = 0
            for j in active_idx:
                if j != i:
                    d = math.hypot(pos[j, 0] - px, pos[j, 1] - py)
                    if d < self.neighbour_radius:
                        count += 1
            damp_coeff = self._DAMPING_COEFF * (1.0 + self.panic)
            damping = 1.0 / (1.0 + damp_coeff * max(0, count - 1))
            speed = desired_speed * damping
            speeds[i] = speed
            ang = (self._rng.random() - 0.5) * self._JITTER_AMP
            ca, sa = math.cos(ang), math.sin(ang)
            rdx = dirx * ca - diry * sa
            rdy = dirx * sa + diry * ca
            pos[i][0] = px + rdx * speed
            pos[i][1] = py + rdy * speed

        self._last_mean_speed = float(np.mean(speeds[active_idx]))

        # 2. Resolve overlaps (smaller index pushed first — deterministic).
        for a in active_idx:
            for b in active_idx:
                if b <= a:
                    continue
                d = math.hypot(pos[a, 0] - pos[b, 0], pos[a, 1] - pos[b, 1])
                if d < min_sep:
                    push = min(
                        (min_sep - d) * (0.5 + self.panic * 0.25),
                        self._PUSH_CAP,
                    )
                    if d > 1e-9:
                        ux = (pos[b, 0] - pos[a, 0]) / d
                        uy = (pos[b, 1] - pos[a, 1]) / d
                    elif pos[a, 1] <= pos[b, 1]:
                        ux, uy = 0.0, 1.0
                    else:
                        ux, uy = 1.0, 0.0
                    pos[a][0] -= ux * push
                    pos[a][1] -= uy * push
                    pos[b][0] += ux * push
                    pos[b][1] += uy * push

        # 3. Wall bounds + absorb at the exit (continuous crossing test).
        for i in active_idx:
            nx, ny = pos[i]
            ox, oy = old_pos[i]
            x = max(nx, self.agent_radius)
            y = max(ny, self.agent_radius)
            y = min(y, self.hall_height - self.agent_radius)
            if self.exit_on == "right":
                x = min(x, self.hall_width)
                plane = self.hall_width - self.agent_radius
                if ox < plane <= x:
                    frac = (plane - ox) / (x - ox)
                    y_cross = oy + frac * (ny - oy)
                    if abs(y_cross - ey) <= self._exit_half:
                        exited[i] = True
                elif ox >= plane:
                    if min(oy, ny) <= ey + self._exit_half and max(
                        oy, ny
                    ) >= ey - self._exit_half:
                        exited[i] = True
            else:  # top
                x = min(x, self.hall_width - self.agent_radius)
                plane = self.hall_height - self.agent_radius
                if oy < plane <= y:
                    frac = (plane - oy) / (y - oy)
                    x_cross = ox + frac * (nx - ox)
                    if abs(x_cross - ex) <= self._exit_half:
                        exited[i] = True
                elif oy >= plane:
                    if min(ox, nx) <= ex + self._exit_half and max(
                        ox, nx
                    ) >= ex - self._exit_half:
                        exited[i] = True
            pos[i][0] = x
            pos[i][1] = y

        self._step += 1