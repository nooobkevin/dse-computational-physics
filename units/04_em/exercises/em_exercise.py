"""Electricity & Magnetism simulation — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of electric fields and circuits
by overriding the hooks in two classes:

1. ``StudentElectricField`` — override ``field(self, x, y)`` and
   ``potential(self, x, y)`` with Coulomb's law.
2. ``StudentCircuit`` — override ``resolve(self)`` to compute branch
   currents and node voltages using Kirchhoff's laws + Ohm's law.

The base classes (:class:`ElectricField` and :class:`Circuit`) provide
everything else: the ``step`` method, properties like ``state``, ``position``,
``energy``, ``currents``, ``voltages``, and ``power_dissipated()``.  You
only need to supply the physics.

---

## Part 1 — Electric field

Physics background
------------------
For a point charge *q* at the origin, the electric field at position
*(x, y)* is:

    r = √(x² + y²)
    E = q / (4 π ε₀ r²)   (radially outward for q > 0)

    Ex = E · cos(θ) = E · x/r
    Ey = E · sin(θ) = E · y/r

The electric potential is:

    V = q / (4 π ε₀ r)

Constants
---------
``self.q`` — charge (C)  
``self.epsilon0`` — vacuum permittivity (F/m), default 8.854e-12  
``self._position`` — charge position (x, y)

What to do
----------
1. Read the docstring of ``field(self, x, y)`` and ``potential(self, x, y)``.
2. Replace the ``raise NotImplementedError`` lines with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/04_em/exercises/test_exercise.py -v

---

## Part 2 — Circuit

Physics background
------------------
For a circuit with branches (each branch has from_node, to_node, R, V),
Kirchhoff's laws give:

- **KCL**: at any node, Σ I_in = Σ I_out
- **KVL**: around any closed loop, Σ V_drops = Σ V_rises
- **Ohm's law**: V = I R

The branches are stored in ``self.branches`` as a list of tuples
``(from_node, to_node, R, V)``:
- ``from_node``, ``to_node``: node indices (0 = ground)
- ``R``: resistance in Ω
- ``V``: voltage source in V (positive = voltage rise from *from_node* to *to_node*)

After solving, set:
- ``self._currents`` = dict mapping branch index ``"0"``, ``"1"``, … to current (A)
- ``self._voltages`` = dict mapping node index ``"0"``, ``"1"``, … to voltage (V)

For a series circuit (V=10V, R1=5Ω, R2=3Ω):
- Total resistance = 8Ω, current = 10/8 = 1.25A
- V_R1 = 1.25 × 5 = 6.25V, V_R2 = 1.25 × 3 = 3.75V
- Node voltage at node 1 = V_R2 = 3.75V (with ground at node 0)

What to do
----------
1. Read the docstring of ``resolve(self)``.
2. Replace ``raise NotImplementedError`` with nodal analysis.
3. Run the auto-grader to verify.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

from physics_core.em.circuits import Circuit
from physics_core.em.electrostatics import ElectricField
from physics_core.em.magnetism import MovingCharge


# ===========================================================================
# Part 1: Electric field
# ===========================================================================


class StudentElectricField(ElectricField):
    """Student implementation of electric field.

    Override :meth:`field` and :meth:`potential` with the correct
    Coulomb physics.  Everything else is inherited from :class:`ElectricField`.

    Physics (fill this in):
        field(x, y):
            dx = x - self._position[0]
            dy = y - self._position[1]
            r2 = dx*dx + dy*dy
            if r2 == 0: return (0.0, 0.0)
            r = sqrt(r2)
            E = self.q / (4 * pi * self.epsilon0 * r2)
            return (E * dx / r, E * dy / r)

        potential(x, y):
            dx = x - self._position[0]
            dy = y - self._position[1]
            r = sqrt(dx*dx + dy*dy)
            if r == 0: return float('inf')
            return self.q / (4 * pi * self.epsilon0 * r)
    """

    def field(self, x: float, y: float) -> Tuple[float, float]:
        """Compute electric field ``(Ex, Ey)`` at point ``(x, y)``.

        Replace NotImplementedError with Coulomb's law.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement field(self, x, y) in StudentElectricField. "
            "See the docstring for the correct formula."
        )

    def potential(self, x: float, y: float) -> float:
        """Compute electric potential ``V`` at point ``(x, y)``.

        Replace NotImplementedError with Coulomb's law.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement potential(self, x, y) in StudentElectricField. "
            "See the docstring for the correct formula."
        )


# ===========================================================================
# Part 2: Circuit
# ===========================================================================


class StudentCircuit(Circuit):
    """Student implementation of circuit solver.

    Override :meth:`resolve` to compute branch currents and node voltages
    using Kirchhoff's laws (nodal analysis).  Everything else is inherited
    from :class:`Circuit`.

    Steps for resolve():
        1. Find the highest node index.
        2. Set up the nodal-analysis matrix G (N×N) and vector I (N).
        3. For each branch (frm, to, R, V):
           - Skip if R <= 0
           - cond = 1.0 / R
           - Add cond to G[i][i] and G[j][j] if nodes > 0
           - Subtract cond from G[i][j] and G[j][i] if both > 0
           - I[frm-1] -= V * cond, I[to-1] += V * cond (if nodes > 0)
        4. Solve G * V_nodes = I (use numpy.linalg.solve).
        5. Store node voltages in self._voltages (node 0 = 0V).
        6. For each branch, compute current:
               I_branch = (V_from - V_to + V_src) / R
           Store in self._currents.

    Example (series circuit):
        branches = [(0, 1, 5.0, 10.0), (1, 0, 3.0, 0.0)]
        After resolve:
            self._voltages = {"0": 0.0, "1": 3.75}
            self._currents = {"0": 1.25, "1": 1.25}
    """

    def resolve(self) -> None:
        """Solve the circuit using nodal analysis.

        Replace NotImplementedError with the correct solver.
        See the class docstring for the algorithm.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement resolve(self) in StudentCircuit. "
            "See the docstring for the nodal analysis algorithm."
        )


# ===========================================================================
# Part 3: Magnetism — Lorentz force on a moving charge
# ===========================================================================


class StudentMagnetism(MovingCharge):
    """Student implementation of Lorentz force physics.

    Override :meth:`magnetic_force` and :meth:`orbit_radius` with the
    correct formulas.  Everything else is inherited from :class:`MovingCharge`.

    Physics (fill this in):
        magnetic_force(B, q, v, theta_degrees):
            theta = radians(theta_degrees)
            return abs(q) * v * B * sin(theta)

        orbit_radius(m, v, q, B):
            return m * v / (abs(q) * B)

    Parameters
    ----------
    m : float
        Particle mass (kg).  Default 1.67e-27 (proton mass).
    q : float
        Charge (C).  Default 1.60e-19 (elementary charge).
    """

    def magnetic_force(self, B: float, q: float, v: float, theta_degrees: float) -> float:
        """Magnitude of the Lorentz force ``F = |q| v B sinθ``.

        Replace NotImplementedError with the correct formula.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement magnetic_force(self, B, q, v, theta_degrees). "
            "Use F = |q| * v * B * sin(theta)."
        )

    def orbit_radius(self, m: float, v: float, q: float, B: float) -> float:
        """Orbital radius ``r = m v / (|q| B)`` for circular motion in uniform B.

        Replace NotImplementedError with the correct formula.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement orbit_radius(self, m, v, q, B). "
            "Use r = m * v / (|q| * B)."
        )