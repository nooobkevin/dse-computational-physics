"""Stars and Relativity simulation — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of special relativity and stellar
physics by overriding the hooks in TWO classes:

1. ``StudentRelativity`` — override ``lorentz_factor(self, v)``,
   ``time_dilated(self, v, t0)``, and ``length_contracted(self, v, l0)``
   with the correct formulas.

2. ``StudentStars`` — override ``luminosity(self, T, R)``,
   ``radius_from_luminosity(self, L, T)``, ``peak_wavelength(self, T)``,
   and ``classify(self, L, T)`` with the correct formulas.

The base classes (:class:`RelativityEngine` and :class:`HRDiagram`) provide
everything else.  You only need to supply the physics.

---

Physics background — Relativity
--------------------------------
Lorentz factor:
    γ = 1 / sqrt(1 − v²/c²)

Time dilation:
    Δt = γ · Δt₀   (a moving clock appears to run slow)

Length contraction:
    l = l₀ / γ     (a moving object appears shortened along its direction of motion)

Physics background — Stars
---------------------------
Stefan-Boltzmann law:
    L = 4πR²σT⁴    (luminosity of a spherical blackbody)

Wien's displacement law:
    λ_max = b / T   (peak wavelength of blackbody radiation)

Constants (imported at top of file):
    ``self.c`` — speed of light (m/s), default 3.0e8.
    ``self.sigma`` — Stefan-Boltzmann constant (5.670374419e-8 W m⁻² K⁻⁴).
    ``self.b`` — Wien displacement constant (2.897771955e-3 m·K).

What to do
----------
1. Read the docstring of each method.
2. Replace the ``raise NotImplementedError`` lines with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/08_astrophysics/exercises/test_stars_exercise.py -v
"""

from __future__ import annotations

import math

from physics_core.astrophysics.hr_diagram import HRDiagram, L_SUN, T_SUN
from physics_core.astrophysics.relativity import RelativityEngine


# ===========================================================================
# Part 1 — Special Relativity
# ===========================================================================


class StudentRelativity(RelativityEngine):
    """Student implementation of special relativity formulas.

    Override the three hooks with the correct physics:

        lorentz_factor(v):
            beta = v / self.c
            if abs(beta) >= 1: raise ValueError(...)
            return 1 / sqrt(1 - beta^2)

        time_dilated(v, t0):
            return self.lorentz_factor(v) * t0

        length_contracted(v, l0):
            return l0 / self.lorentz_factor(v)
    """

    def lorentz_factor(self, v: float) -> float:
        """Compute the Lorentz factor γ = 1 / sqrt(1 - v²/c²).

        Parameters
        ----------
        v : float
            Relative velocity (m/s). |v| must be < c.

        Returns
        -------
        float
            Lorentz factor γ (dimensionless, ≥ 1).
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement lorentz_factor(self, v) in "
            "StudentRelativity.  Use γ = 1 / sqrt(1 - v²/c²)."
        )

    def time_dilated(self, v: float, t0: float) -> float:
        """Compute the dilated time interval Δt = γ · t0.

        Parameters
        ----------
        v : float
            Relative velocity (m/s).
        t0 : float
            Proper time interval (s).

        Returns
        -------
        float
            Dilated time interval (s).
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement time_dilated(self, v, t0) in "
            "StudentRelativity.  Use Δt = γ · t0."
        )

    def length_contracted(self, v: float, l0: float) -> float:
        """Compute the contracted length l = l0 / γ.

        Parameters
        ----------
        v : float
            Relative velocity (m/s).
        l0 : float
            Proper length (m).

        Returns
        -------
        float
            Contracted length (m).
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement length_contracted(self, v, l0) in "
            "StudentRelativity.  Use l = l0 / γ."
        )


# ===========================================================================
# Part 2 — Stellar Physics (H-R Diagram)
# ===========================================================================


class StudentStars(HRDiagram):
    """Student implementation of stellar physics formulas.

    Override the five hooks with the correct physics:

        luminosity(T, R):
            return 4 * π * R² * σ * T⁴

        radius_from_luminosity(L, T):
            return sqrt(L / (4 * π * σ * T⁴))

        peak_wavelength(T):
            return b / T

        classify(L, T):
            L_ms = L_SUN * (T / T_SUN)^4
            if L < 0.1 * L_ms: return "white dwarf"
            elif L > 10.0 * L_ms: return "giant"
            else: return "main sequence"
    """

    def luminosity(self, T: float, R: float) -> float:
        """Compute the luminosity L = 4πR²σT⁴.

        Parameters
        ----------
        T : float
            Effective surface temperature (K).
        R : float
            Radius of the star (m).

        Returns
        -------
        float
            Luminosity (W).
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement luminosity(self, T, R) in "
            "StudentStars.  Use L = 4πR²σT⁴."
        )

    def radius_from_luminosity(self, L: float, T: float) -> float:
        """Compute the radius R = sqrt(L / (4πσT⁴)).

        Parameters
        ----------
        L : float
            Luminosity (W).
        T : float
            Effective surface temperature (K).

        Returns
        -------
        float
            Radius (m).
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement radius_from_luminosity(self, L, T) in "
            "StudentStars.  Use R = sqrt(L / (4πσT⁴))."
        )

    def peak_wavelength(self, T: float) -> float:
        """Compute the peak wavelength λ_max = b / T (Wien's law).

        Parameters
        ----------
        T : float
            Temperature (K).

        Returns
        -------
        float
            Peak wavelength (m).
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement peak_wavelength(self, T) in "
            "StudentStars.  Use λ_max = b / T."
        )

    def blackbody_curve(self, T, wavelengths):
        """[Stretch goal] Compute a normalised blackbody spectral curve.

        This is an advanced hook — it is NOT tested by the basic grader.
        """
        raise NotImplementedError(
            "You must implement blackbody_curve(self, T, wavelengths) in "
            "StudentStars if attempting the stretch goal."
        )

    def classify(self, L: float, T: float) -> str:
        """Classify a star into an H-R diagram region.

        Returns one of: ``"main sequence"``, ``"giant"``, ``"white dwarf"``.

        Parameters
        ----------
        L : float
            Luminosity (W).
        T : float
            Effective surface temperature (K).

        Returns
        -------
        str
            Classification.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement classify(self, L, T) in "
            "StudentStars.  Compare L to the main-sequence prediction."
        )