"""Hertzsprung-Russell diagram and stellar physics simulation.

Architecture
------------
:class:`HRDiagram` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines five physics **hooks**:

    ``luminosity(self, T, R) -> float``
    ``radius_from_luminosity(self, L, T) -> float``
    ``peak_wavelength(self, T) -> float``
    ``blackbody_curve(self, T, wavelengths) -> np.ndarray``
    ``classify(self, L, T) -> str``

that raise ``NotImplementedError`` by default.  Subclasses override the
hooks to supply the physics — students fill them in, while
:class:`ReferenceHRDiagram` provides the correct reference implementation.

Physical constants
------------------
``SIGMA`` — Stefan-Boltzmann constant (5.670374419e-8 W m⁻² K⁻⁴).
``B`` — Wien displacement constant (2.897771955e-3 m·K).
``L_SUN`` — Solar luminosity (3.828e26 W).
``R_SUN`` — Solar radius (6.9634e8 m).
"""

from __future__ import annotations

import math
from typing import List

import numpy as np

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
SIGMA: float = 5.670374419e-8  # Stefan-Boltzmann constant (W m⁻² K⁻⁴)
B: float = 2.897771955e-3       # Wien displacement constant (m·K)
H: float = 6.62607015e-34       # Planck constant (J·s)
C: float = 2.99792458e8         # speed of light (m/s)
K_B: float = 1.380649e-23       # Boltzmann constant (J/K)
L_SUN: float = 3.828e26         # Solar luminosity (W)
R_SUN: float = 6.9634e8         # Solar radius (m)
T_SUN: float = 5772.0           # Solar effective temperature (K)


class HRDiagram:
    """Abstract base H-R diagram and stellar physics simulation.

    Parameters
    ----------
    sigma : float
        Stefan-Boltzmann constant.  Default 5.670374419e-8.
    b : float
        Wien displacement constant.  Default 2.897771955e-3.
    """

    def __init__(
        self,
        sigma: float = SIGMA,
        b: float = B,
    ) -> None:
        self.sigma: float = sigma
        self.b: float = b

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------

    def luminosity(self, T: float, R: float) -> float:
        """Compute the luminosity of a spherical blackbody.

        L = 4π R² σ T⁴

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
        raise NotImplementedError(
            "Subclasses must implement luminosity(self, T, R)"
        )

    def radius_from_luminosity(self, L: float, T: float) -> float:
        """Compute the radius of a star from its luminosity and temperature.

        R = sqrt(L / (4π σ T⁴))

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
        raise NotImplementedError(
            "Subclasses must implement radius_from_luminosity(self, L, T)"
        )

    def peak_wavelength(self, T: float) -> float:
        """Compute the peak wavelength of blackbody radiation (Wien's law).

        λ_max = b / T

        Parameters
        ----------
        T : float
            Temperature (K).

        Returns
        -------
        float
            Peak wavelength (m).
        """
        raise NotImplementedError(
            "Subclasses must implement peak_wavelength(self, T)"
        )

    def blackbody_curve(
        self, T: float, wavelengths: np.ndarray
    ) -> np.ndarray:
        """Compute a normalised blackbody spectral curve (Planck's law).

        B(λ, T) = (2hc²/λ⁵) * 1 / (exp(hc / λkT) - 1)

        The result is normalised so the peak value is 1.0.

        Parameters
        ----------
        T : float
            Temperature (K).
        wavelengths : np.ndarray
            Array of wavelengths (m) at which to evaluate the spectrum.

        Returns
        -------
        np.ndarray
            Normalised spectral intensity (peak = 1.0).
        """
        raise NotImplementedError(
            "Subclasses must implement blackbody_curve(self, T, wavelengths)"
        )

    def classify(self, L: float, T: float) -> str:
        """Classify a star into a region of the H-R diagram.

        Uses simple luminosity-temperature boundaries:

        - ``"main sequence"`` — L within a factor of 10 of the
          Stefan-Boltzmann prediction for a solar-radius star.
        - ``"giant"`` — L more than 10× the main-sequence prediction.
        - ``"white dwarf"`` — L less than 0.1× the main-sequence prediction.

        Parameters
        ----------
        L : float
            Luminosity (W).
        T : float
            Effective surface temperature (K).

        Returns
        -------
        str
            One of ``"main sequence"``, ``"giant"``, ``"white dwarf"``.
        """
        raise NotImplementedError(
            "Subclasses must implement classify(self, L, T)"
        )


class ReferenceHRDiagram(HRDiagram):
    """Reference H-R diagram implementation with correct physics."""

    def luminosity(self, T: float, R: float) -> float:
        return 4.0 * math.pi * R * R * self.sigma * T ** 4

    def radius_from_luminosity(self, L: float, T: float) -> float:
        return math.sqrt(L / (4.0 * math.pi * self.sigma * T ** 4))

    def peak_wavelength(self, T: float) -> float:
        return self.b / T

    def blackbody_curve(
        self, T: float, wavelengths: np.ndarray
    ) -> np.ndarray:
        hc: float = H * C
        kT: float = K_B * T
        # Avoid division by zero at λ = 0
        intensity: np.ndarray = np.where(
            wavelengths > 0,
            (2.0 * hc / wavelengths ** 5)
            * 1.0 / (np.exp(hc / (wavelengths * kT)) - 1.0),
            0.0,
        )
        peak: float = float(np.max(intensity))
        if peak > 0.0:
            intensity = intensity / peak
        return intensity

    def classify(self, L: float, T: float) -> str:
        # Main-sequence reference: L ∝ T⁴ for a solar-radius star
        L_ms: float = L_SUN * (T / T_SUN) ** 4
        if L < 0.1 * L_ms:
            return "white dwarf"
        elif L > 10.0 * L_ms:
            return "giant"
        else:
            return "main sequence"


# ---------------------------------------------------------------------------
# Convenience: sample stars for H-R diagram plotting
# ---------------------------------------------------------------------------

SampleStar = tuple[str, float, float, str]  # (name, L/L_sun, T/K, region)


SAMPLE_STARS: List[SampleStar] = [
    ("Sun", 1.0, 5772, "main sequence"),
    ("Betelgeuse", 1.26e5, 3500, "giant"),
    ("Sirius A", 25.4, 9940, "main sequence"),
    ("Proxima Centauri", 0.0017, 3042, "main sequence"),
    ("Rigel", 1.2e5, 12100, "giant"),
    ("Sirius B", 0.026, 25000, "white dwarf"),
    ("Van Maanen's Star", 0.00017, 6000, "white dwarf"),
    ("Aldebaran", 425, 3900, "giant"),
]