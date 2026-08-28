"""Orbital mechanics exercise — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of orbital motion by overriding
the hooks in ``StudentOrbitSim``.

The base class (:class:`OrbitSim`) provides everything else: the
``step`` method, properties like ``state``, ``position``,
``energy_components``, ``radius``, and ``speed``.  You only need to
supply the physics.

What to do
----------
1. Implement ``gravitational_force(self, r)`` — F = G M m / r²
2. Implement ``orbital_velocity(self, r)`` — v = sqrt(G M / r)
3. Implement ``escape_velocity(self, r)`` — v_esc = sqrt(2 G M / r)
4. Implement ``gravitational_potential_energy(self, r)`` — U = -G M m / r
5. Implement ``total_energy(self, r, v)`` — E = ½ m v² + U
6. Run the auto-grader:

       uv run pytest units/05_engineering/exercises/test_orbital_exercise.py -v
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple

from physics_core.engineering.orbital import OrbitSim


class StudentOrbitSim(OrbitSim):
    """Student implementation of orbital mechanics.

    Override the five physics hooks with the correct formulas.
    Everything else is inherited from :class:`OrbitSim`.

    Physics (fill this in):
        gravitational_force(r):
            return self.G * self.M * self.m / (r * r)

        orbital_velocity(r):
            return math.sqrt(self.G * self.M / r)

        escape_velocity(r):
            return math.sqrt(2.0 * self.G * self.M / r)

        gravitational_potential_energy(r):
            return -self.G * self.M * self.m / r

        total_energy(r, v):
            return 0.5 * self.m * v * v + self.gravitational_potential_energy(r)
    """

    def gravitational_force(self, r: float) -> float:
        """F = G M m / r²."""
        raise NotImplementedError(
            "You must implement gravitational_force(self, r). "
            "Use: return self.G * self.M * self.m / (r * r)"
        )

    def orbital_velocity(self, r: float) -> float:
        """v = sqrt(G M / r)."""
        raise NotImplementedError(
            "You must implement orbital_velocity(self, r). "
            "Use: return math.sqrt(self.G * self.M / r)"
        )

    def escape_velocity(self, r: float) -> float:
        """v_esc = sqrt(2 G M / r)."""
        raise NotImplementedError(
            "You must implement escape_velocity(self, r). "
            "Use: return math.sqrt(2.0 * self.G * self.M / r)"
        )

    def gravitational_potential_energy(self, r: float) -> float:
        """U = -G M m / r."""
        raise NotImplementedError(
            "You must implement gravitational_potential_energy(self, r). "
            "Use: return -self.G * self.M * self.m / r"
        )

    def total_energy(self, r: float, v: float) -> float:
        """E = ½ m v² + U."""
        raise NotImplementedError(
            "You must implement total_energy(self, r, v). "
            "Use: return 0.5 * self.m * v * v + self.gravitational_potential_energy(r)"
        )