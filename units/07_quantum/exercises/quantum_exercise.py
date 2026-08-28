"""Infinite square well — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of an infinite square well by
overriding the ``energy_level`` method in ``StudentQuantumWell``.

The base class :class:`physics_core.quantum.wavefunctions.QuantumWell`
provides everything else: ``step``, ``state``, ``position``, ``energy``,
``wavefunction``, ``probability_density``, ``transition_energy``, and
``de_broglie_wavelength``.  You only need to supply the energy level formula.

Physics background
------------------
For a particle of mass *m* in an infinite square well of width *L*:

    E_n = n² h² / (8 m L²)

where:
- n = 1, 2, 3, ... is the quantum number
- h = 6.62607015 × 10⁻³⁴ J·s is Planck's constant
- m is the particle mass (kg)
- L is the well width (m)

The wavefunctions are:

    ψ_n(x) = √(2/L) sin(nπx/L)    for 0 ≤ x ≤ L
    ψ_n(x) = 0                     otherwise

The probability density is |ψ_n(x)|².

What to do
----------
1. Read the docstring and signature of ``energy_level`` below.
2. Replace the ``raise NotImplementedError`` line with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/07_quantum/exercises/test_exercise.py -v

   The grader measures the **numerical behaviour** of your implementation
   (energy levels, wavefunction values) — it does *not* read your source
   code, so any correct implementation will pass.
"""

from __future__ import annotations

import math

from physics_core.quantum.wavefunctions import H, QuantumWell


class StudentQuantumWell(QuantumWell):
    """Student implementation of the infinite square well.

    Override :meth:`energy_level` with the correct physics.
    Everything else is inherited from :class:`QuantumWell`.

    Example
    -------
    >>> sim = StudentQuantumWell(L=1e-10, n=1)
    >>> print(sim.energy)
    """

    def energy_level(self, n: int) -> float:
        """Compute the energy of the *n*-th stationary state.

        Parameters
        ----------
        n : int
            Quantum number (1, 2, 3, ...).

        Returns
        -------
        float
            Energy in joules.

        Physics (fill this in)
        ----------------------
        Replace the line below with:

            return (n * n * H * H) / (8.0 * self.m * self.L * self.L)

        (The attributes ``self.m``, ``self.L``, and the constant ``H``
        are available from the base class and module.)
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement energy_level(self, n) "
            "in StudentQuantumWell.  See the docstring for the correct formula."
        )
