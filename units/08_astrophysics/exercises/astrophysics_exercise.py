"""Astrophysics & Relativity simulation — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of the Doppler effect and Hubble's
law by overriding the hooks in one class:

    ``StudentDopplerShift`` — override ``observed_frequency(self, v)``,
    ``redshift(self, v)``, ``velocity_from_z(self, z)`` and
    ``hubble_velocity(self, distance, H0)`` with the correct formulas.

The base class (:class:`DopplerShift`) provides everything else: the
``step`` method, and properties like ``state``, ``position`` and
``energy``.  You only need to supply the physics.

---

Physics background
------------------
When a light source and an observer move relative to each other, the light
is Doppler shifted:

- The source **recedes** from the observer (positive *v*): the observed
  wavelength is longer — a **redshift**.
- The source **approaches** the observer (negative *v*): the observed
  wavelength is shorter — a **blueshift**.

For light, the exact (relativistic) Doppler formula is:

    f_obs = f_source · sqrt((1 − β) / (1 + β)),   β = v / c

where *β = v/c*.  Because wavelength and frequency are related by
*λ = c / f*, this is equivalent to:

    λ_obs / λ_source = sqrt((1 + β) / (1 − β))

The astronomical redshift is defined as:

    z = (λ_obs − λ_source) / λ_source = sqrt((1 + β) / (1 − β)) − 1

For small velocities (|v| << c) this is approximately:

    z ≈ v / c

Inverting the relativistic formula to recover the velocity from a measured
redshift z:

    v = c · ((z + 1)² − 1) / ((z + 1)² + 1)

Finally, **Hubble's law** describes the expansion of the universe: galaxies
recede from us with a velocity proportional to their distance:

    v = H0 · d

where *H0* is the Hubble constant (about 67.8 km/s per Mpc).

Constants
---------
``self.f0`` — source rest frequency (Hz), default 5.8e14 (visible light).
``self.c`` — speed of light (m/s), default 3.0e8.
``C`` / ``H0`` are imported at the top of this file.

What to do
----------
1. Read the docstring of each method in ``StudentDopplerShift``.
2. Replace the ``raise NotImplementedError`` lines with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/08_astrophysics/exercises/test_exercise.py -v
"""

from __future__ import annotations

import math

from physics_core.astrophysics.doppler import C, H0, DopplerShift


class StudentDopplerShift(DopplerShift):
    """Student implementation of Doppler shift and Hubble's law.

    Override the four hooks with the correct physics.  Everything else is
    inherited from :class:`DopplerShift`.

    Physics (fill this in):

        observed_frequency(v):
            beta = v / self.c
            if abs(beta) >= 1: raise ValueError(...)
            return self.f0 * sqrt((1 - beta) / (1 + beta))

        redshift(v):
            beta = v / self.c
            if abs(beta) >= 1: raise ValueError(...)
            return sqrt((1 + beta) / (1 - beta)) - 1

        velocity_from_z(z):
            if z < -1: raise ValueError(...)
            return self.c * ((z + 1)^2 - 1) / ((z + 1)^2 + 1)

        hubble_velocity(distance, H0=H0):
            return H0 * distance
    """

    def observed_frequency(self, v: float) -> float:
        """Compute the observed frequency (Hz) for a given velocity *v*.

        v > 0  → receding source (redshift, lower frequency)
        v < 0  → approaching source (blueshift, higher frequency)

        Replace NotImplementedError with the relativistic Doppler formula.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement observed_frequency(self, v) in "
            "StudentDopplerShift.  See the module docstring for the "
            "relativistic Doppler formula f_obs = f0 * sqrt((1-β)/(1+β))."
        )

    def redshift(self, v: float) -> float:
        """Compute the redshift *z* for a given velocity *v*.

        Recall z = (λ_obs − λ_source) / λ_source.  A receding source
        (v > 0) gives a positive redshift.

        Replace NotImplementedError with the correct formula.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement redshift(self, v) in StudentDopplerShift. "
            "Use z = sqrt((1+β)/(1-β)) - 1 with β = v/c."
        )

    def velocity_from_z(self, z: float) -> float:
        """Compute the recession velocity (m/s) from a redshift *z*.

        Replace NotImplementedError with the relativistic inverse formula.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement velocity_from_z(self, z) in "
            "StudentDopplerShift.  Use v = c * ((z+1)^2 - 1) / ((z+1)^2 + 1)."
        )

    def hubble_velocity(self, distance: float, H0: float = H0) -> float:
        """Compute the Hubble-flow recession velocity (km/s) at distance *d*.

        distance : float
            Distance to the galaxy (Mpc).
        H0 : float
            Hubble constant (km/s per Mpc).  Default 67.8.

        Replace NotImplementedError with Hubble's law v = H0 * d.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement hubble_velocity(self, distance, H0) in "
            "StudentDopplerShift.  Use Hubble's law v = H0 * d."
        )