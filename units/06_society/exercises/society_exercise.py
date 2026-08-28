"""Radioactive decay simulation — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of radioactive decay by overriding
the ``decay_probability`` method in ``StudentDecaySim``.

The base class :class:`physics_core.society.decay.DecaySim` provides
everything else: the Monte Carlo integration loop (``step``), the ``state``
property, ``position()``, ``energy()``, ``nuclei_remaining()``, and
``history()``.  You only need to supply the decay probability.

Physics background
------------------
For a radioactive isotope with half-life *T*, the decay constant is:

    λ = ln(2) / T

The probability that a single nucleus decays in a small time interval *dt* is:

    p = 1 - exp(-λ dt)

This is the exact probability for a Poisson process with rate λ.

In the Monte Carlo method, each of the remaining N nuclei decays
independently with probability *p* per time-step.  This simulates the
random nature of radioactive decay.

Constants
---------
``self.T`` — half-life (s)
``self.dt`` — simulation time-step (s)
``self.N0`` — initial number of nuclei
``self._N`` — current number of undecayed nuclei
``self._t`` — elapsed simulation time (s)

What to do
----------
1. Read the docstring and signature of ``decay_probability`` below.
2. Replace the ``raise NotImplementedError`` line with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/06_society/exercises/test_exercise.py -v

   The grader measures the **numerical behaviour** of your simulation
   (analytic N matches, Monte Carlo half-life estimate) — it does *not*
   read your source code, so any correct implementation will pass.
"""

from __future__ import annotations

import math

from physics_core.society.decay import DecaySim


class StudentDecaySim(DecaySim):
    """Student implementation of radioactive decay.

    Override :meth:`decay_probability` with the correct physics.
    Everything else is inherited from :class:`DecaySim`.

    Example
    -------
    >>> sim = StudentDecaySim(N0=10000, half_life=1.0, dt=0.01)
    >>> for _ in range(100):
    ...     sim.step()
    >>> print(sim.nuclei_remaining())
    """

    def decay_probability(self, dt: float) -> float:
        """Compute the probability that a single nucleus decays in *dt*.

        Parameters
        ----------
        dt : float
            Time interval (s).

        Returns
        -------
        float
            Decay probability in [0, 1].

        Physics (fill this in)
        ----------------------
        Replace the line below with:

            lam = math.log(2.0) / self.T
            return 1.0 - math.exp(-lam * dt)

        (The attribute ``self.T`` is the half-life set by the base-class
        constructor.)
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement decay_probability(self, dt) "
            "in StudentDecaySim.  See the docstring for the correct formula."
        )