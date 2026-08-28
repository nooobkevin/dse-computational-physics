"""Circuit simulation with dependency-injection hooks.

Architecture
------------
:class:`Circuit` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines one physics **hook**:

    ``resolve(self) -> None``

that raises ``NotImplementedError`` by default.  Subclasses override the
hook to supply the physics — students fill it in, while
:class:`ReferenceCircuit` provides the correct reference implementation
using nodal analysis (Kirchhoff's laws + Ohm's law).

State representation
--------------------
Internal state stores branch currents and node voltages as dicts.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np


class Circuit:
    """Abstract base circuit simulation.

    Parameters
    ----------
    branches : list of tuple
        Each branch is ``(from_node, to_node, R, V)`` where:
        - *from_node*, *to_node* : int  (node indices; 0 = ground)
        - *R* : float  (resistance in Ω)
        - *V* : float  (voltage source in V; positive = rise from from_node to to_node)
    """

    def __init__(self, branches: List[Tuple[int, int, float, float]] | None = None) -> None:
        self.branches = branches or []
        self._currents: Dict[str, float] = {}
        self._voltages: Dict[str, float] = {}

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def resolve(self) -> None:
        """Solve the circuit for branch currents and node voltages.

        Override this in subclasses to supply the physics.
        After calling, ``self.currents`` and ``self.voltages`` should
        be populated.
        """
        raise NotImplementedError(
            "Subclasses must implement resolve(self)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    @property
    def currents(self) -> Dict[str, float]:
        """Branch currents keyed by branch index, e.g. ``{"0": 1.25}``."""
        return dict(self._currents)

    @property
    def voltages(self) -> Dict[str, float]:
        """Node voltages keyed by node index, e.g. ``{"1": 6.25}``."""
        return dict(self._voltages)

    def power_dissipated(self) -> float:
        """Total power dissipated in all resistors (W)."""
        total = 0.0
        for i, (_, _, R, _) in enumerate(self.branches):
            I = self._currents.get(str(i), 0.0)
            total += I * I * R
        return total

    @property
    def state(self) -> Dict[str, Any]:
        """Current simulation state."""
        return {
            "currents": self.currents,
            "voltages": self.voltages,
            "branches": self.branches,
        }


class ReferenceCircuit(Circuit):
    """Reference circuit solver using nodal analysis (Kirchhoff + Ohm).

    Solves the linear system ``G · V = I`` where:
    - *G* is the conductance matrix (N×N, N = number of non-ground nodes)
    - *V* is the vector of unknown node voltages
    - *I* is the vector of current sources

    After solving for node voltages, branch currents are computed via
    Ohm's law: ``I_branch = (V_from - V_to + V_source) / R``.
    """

    def resolve(self) -> None:
        if not self.branches:
            self._currents = {}
            self._voltages = {}
            return

        # Find the highest node index to determine matrix size
        max_node = 0
        for frm, to, _, _ in self.branches:
            max_node = max(max_node, frm, to)

        # Node 0 is ground (reference).  We solve for nodes 1..max_node.
        n_nodes = max_node
        if n_nodes == 0:
            # All branches connected to ground — trivial
            self._currents = {}
            self._voltages = {"0": 0.0}
            return

        G = np.zeros((n_nodes, n_nodes), dtype=float)
        I_vec = np.zeros(n_nodes, dtype=float)

        for frm, to, res, vsrc in self.branches:
            if res <= 0:
                continue  # skip zero-resistance branches (ideal wire)
            cond = 1.0 / res

            # Map node indices to matrix indices (node 0 = ground, excluded)
            for n in (frm, to):
                if n > 0:
                    idx = n - 1
                    G[idx, idx] += cond

            if frm > 0 and to > 0:
                i, j = frm - 1, to - 1
                G[i, j] -= cond
                G[j, i] -= cond

            # Current contribution from voltage source
            # In nodal analysis: current leaving node frm due to source = -G*V_src
            # current entering node to due to source = +G*V_src
            if frm > 0:
                I_vec[frm - 1] -= vsrc * cond
            if to > 0:
                I_vec[to - 1] += vsrc * cond

        try:
            V_nodes = np.linalg.solve(G, I_vec)
        except np.linalg.LinAlgError:
            # Fallback: least-squares
            V_nodes, _, _, _ = np.linalg.lstsq(G, I_vec, rcond=None)

        # Store node voltages (node 0 = ground = 0V)
        self._voltages = {"0": 0.0}
        for i in range(n_nodes):
            self._voltages[str(i + 1)] = float(V_nodes[i])

        # Compute branch currents
        self._currents = {}
        for i, (frm, to, res, vsrc) in enumerate(self.branches):
            v_from = self._voltages.get(str(frm), 0.0)
            v_to = self._voltages.get(str(to), 0.0)
            if res > 0:
                branch_i = (v_from - v_to + vsrc) / res
            else:
                branch_i = 0.0
            self._currents[str(i)] = branch_i