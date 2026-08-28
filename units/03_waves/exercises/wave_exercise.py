"""Wave simulation — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of a traveling wave by overriding
the ``displacement`` method in ``StudentWaveSim``.

The base class :class:`physics_core.waves.wave_sim.WaveSim` provides
everything else: the simulation loop (``step``), the ``state`` property,
``position()``, ``energy()``, and ``field()``.  You only need to supply
the wave equation.

Physics background
------------------
A traveling wave on a string has the form:

    y(x, t) = A sin(kx - ωt)

where:
- A is the amplitude (maximum displacement from equilibrium)
- k = 2π / λ is the wave number
- ω = 2π f is the angular frequency
- λ is the wavelength
- f is the frequency

The wave speed is related by v = f λ = ω / k.

Key properties:
- The wave transports energy but not matter
- Energy is proportional to amplitude squared: I ∝ A²
- Two waves can superpose: y_total = y₁ + y₂
- Standing waves form when two identical waves travel in opposite directions

Units
-----
- x : metres (m)
- t : seconds (s)
- return value : metres (m) — displacement y(x, t)

What to do
----------
1. Read the docstring and signature of ``displacement`` below.
2. Replace the ``raise NotImplementedError`` line with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/03_waves/exercises/test_exercise.py -v

   The grader measures the **numerical behaviour** of your simulation
   (field values, superposition, intensity) — it does *not* read your
   source code, so any correct implementation will pass.
"""

from __future__ import annotations

import math

from physics_core.waves.wave_sim import WaveSim


class StudentWaveSim(WaveSim):
    """Student implementation of a traveling wave.

    Override :meth:`displacement` with the correct physics.
    Everything else is inherited from :class:`WaveSim`.

    Example
    -------
    >>> sim = StudentWaveSim(amplitude=1.0, wavelength=2.0, frequency=1.0)
    >>> y = sim.displacement(0.5, 0.1)
    >>> print(y)
    """

    def displacement(self, x: float, t: float) -> float:
        """Compute the wave displacement y(x, t).

        Parameters
        ----------
        x : float
            Spatial position (m).
        t : float
            Time (s).

        Returns
        -------
        float
            Displacement y(x, t) (m).

        Physics (fill this in)
        ----------------------
        Replace the line below with:

            return self.amplitude * math.sin(self.k * x - self.omega * t)

        (The attributes ``self.amplitude``, ``self.k``, and ``self.omega``
        are set by the base-class constructor.)
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement displacement(self, x, t) "
            "in StudentWaveSim.  See the docstring for the correct formula."
        )
