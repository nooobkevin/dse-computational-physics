"""Gas simulation — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of an ideal gas by overriding
the two collision hooks in ``StudentGasSim``.

The base class :class:`physics_core.thermal.gas_sim.GasSim` provides
everything else: the integration loop (``step``), the ``state`` property,
``position()``, and ``energy()``.  You only need to supply the collision
logic.

Physics background
------------------
You are simulating *N* rigid particles in a 2D box of side length *L*.
Particles move freely between collisions.  Two types of collisions keep
the gas in equilibrium:

1. **Wall collisions**: when a particle reaches a wall, it bounces off
   elastically — the velocity component normal to the wall is reversed.
2. **Particle-particle collisions**: when two particles meet, they
   exchange the component of velocity along the line joining their
   centres (elastic collision of equal masses).

What to do
----------
1. Read the docstrings of ``_collide_wall`` and ``_collide_particle`` below.
2. Replace the ``raise NotImplementedError`` lines with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/02_thermal/exercises/test_exercise.py -v

   The grader measures the **numerical behaviour** of your simulation
   (pressure, energy conservation, speed distribution) — it does *not*
   read your source code, so any correct implementation will pass.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np

from physics_core.thermal.gas_sim import GasSim


class StudentGasSim(GasSim):
    """Student implementation of the gas simulation.

    Override :meth:`_collide_wall` and :meth:`_collide_particle` with
    the correct physics.  Everything else is inherited from
    :class:`GasSim`.

    Example
    -------
    >>> sim = StudentGasSim(N=50, L=10.0, T=1.0, dt=0.01)
    >>> for _ in range(100):
    ...     sim.step()
    >>> print(sim.state["t"])
    """

    def _collide_wall(
        self, positions: np.ndarray, velocities: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Check and resolve particle-wall collisions.

        For each spatial dimension *d*:

        - If a particle's coordinate ``positions[i, d]`` is **less than 0**
          (left/bottom wall), reflect it: set the velocity component to its
          absolute value and mirror the position back inside.
        - If a particle's coordinate ``positions[i, d]`` is **greater than L**
          (right/top wall), reflect it: set the velocity component to its
          negative absolute value and mirror the position back inside.

        Parameters
        ----------
        positions : ndarray, shape (N, dim)
            Current particle positions.
        velocities : ndarray, shape (N, dim)
            Current particle velocities.

        Returns
        -------
        positions : ndarray
            Updated positions after wall collision resolution.
        velocities : ndarray
            Updated velocities after wall collision resolution.

        Physics (fill this in)
        ----------------------
        For each dimension d:
            mask_low = positions[:, d] < 0
            velocities[mask_low, d] = abs(velocities[mask_low, d])
            positions[mask_low, d] = -positions[mask_low, d]

            mask_high = positions[:, d] > self.L
            velocities[mask_high, d] = -abs(velocities[mask_high, d])
            positions[mask_high, d] = 2*self.L - positions[mask_high, d]
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement _collide_wall(self, positions, velocities) "
            "in StudentGasSim.  See the docstring for the correct logic."
        )

    def _collide_particle(
        self, positions: np.ndarray, velocities: np.ndarray
    ) -> np.ndarray:
        """Check and resolve elastic particle-particle collisions.

        For each pair of particles *(i, j)* with *i < j*:

        - Compute the vector from *j* to *i*: ``dr = positions[i] - positions[j]``
        - Compute the distance between them: ``dist = sqrt(sum(dr**2))``
        - If ``dist < 2 * self._particle_radius`` and ``dist > 1e-12``:
            - Compute the relative velocity along the line of centres:
              ``v_rel = dot(velocities[i] - velocities[j], dr) / dist``
            - If ``v_rel < 0`` (particles are approaching):
                - Exchange the velocity component along the line of centres:
                  ``impulse = (v_rel / dist) * dr``
                  ``velocities[i] -= impulse``
                  ``velocities[j] += impulse``

        Parameters
        ----------
        positions : ndarray, shape (N, dim)
            Current particle positions.
        velocities : ndarray, shape (N, dim)
            Current particle velocities.

        Returns
        -------
        velocities : ndarray
            Updated velocities after particle collision resolution.

        Physics (fill this in)
        ----------------------
        N = self.N
        min_dist = 2.0 * self._particle_radius
        for i in range(N):
            for j in range(i + 1, N):
                dr = positions[i] - positions[j]
                dist_sq = float(np.dot(dr, dr))
                if dist_sq < min_dist * min_dist and dist_sq > 1e-12:
                    dist = math.sqrt(dist_sq)
                    dv = velocities[i] - velocities[j]
                    v_rel = float(np.dot(dv, dr)) / dist
                    if v_rel < 0:
                        impulse = (v_rel / dist) * dr
                        velocities[i] -= impulse
                        velocities[j] += impulse
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement _collide_particle(self, positions, velocities) "
            "in StudentGasSim.  See the docstring for the correct logic."
        )