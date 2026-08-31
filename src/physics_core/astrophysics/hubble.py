"""Hubble's law and stellar classification utilities.

Provides :class:`HubbleLaw` for computing recession velocities and
distances, and the :data:`SPECTRAL_CLASSES` table for stellar
classification (O B A F G K M → temperature ranges).
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
# Hubble constant (km/s per Mpc) — Planck 2018 value
H0 = 67.8

# 1 Mpc in km (for Hubble time calculation)
MEGAPARSEC_IN_KM = 3.085677581e19


def redshift_factor(z: float) -> float:
    """Factor by which cosmic expansion stretches light of redshift ``z``.

    A photon emitted with wavelength ``λ_e`` at a source of redshift ``z``
    is observed today with wavelength ``λ_o`` given by

        λ_o = (1 + z) · λ_e

    so :func:`redshift_factor` returns ``(1 + z)``.  It is the inverse of
    the cosmic scale factor *a = 1 / (1 + z)*.

    Parameters
    ----------
    z : float
        Cosmological redshift (dimensionless).  Must be greater than -1.

    Returns
    -------
    float
        The wavelength-stretching factor ``1 + z``.

    Raises
    ------
    ValueError
        If ``z < -1`` (a physically impossible redshift — the emitted
        wavelength would be non-positive).
    """
    if z < -1.0:
        raise ValueError(f"redshift z must be >= -1, got {z}")
    return 1.0 + z


# ---------------------------------------------------------------------------
# Stellar spectral classification (O B A F G K M)
# ---------------------------------------------------------------------------
# NOTE: The CAF (Curriculum and Assessment Framework) consultation draft
# (June 2026) removes "major spectral classes OBAFGKM" from the core
# curriculum (Annex 3 lines 4309–4310).  This table is retained as
# **enrichment material** — useful for teachers who wish to discuss
# spectral classification beyond the core requirements, but no longer a
# tested outcome.  The H-R diagram (which uses temperature as its
# horizontal axis) remains a core requirement.
#
# Each entry: (min_temp_K, max_temp_K, colour_name, hex_colour, description)
SpectralClass = Tuple[int, int, str, str, str]

SPECTRAL_CLASSES: List[Dict[str, Any]] = [
    {
        "class": "O",
        "temp_min": 30000,
        "temp_max": 50000,
        "colour": "Blue",
        "hex": "#9db4ff",
        "description": "Very hot, massive blue giants",
    },
    {
        "class": "B",
        "temp_min": 10000,
        "temp_max": 30000,
        "colour": "Blue-white",
        "hex": "#aabfff",
        "description": "Hot, massive blue-white stars",
    },
    {
        "class": "A",
        "temp_min": 7500,
        "temp_max": 10000,
        "colour": "White",
        "hex": "#f8f7ff",
        "description": "White main-sequence stars (e.g. Sirius)",
    },
    {
        "class": "F",
        "temp_min": 6000,
        "temp_max": 7500,
        "colour": "Yellow-white",
        "hex": "#fff4e8",
        "description": "Yellow-white stars (e.g. Procyon)",
    },
    {
        "class": "G",
        "temp_min": 5200,
        "temp_max": 6000,
        "colour": "Yellow",
        "hex": "#ffedcc",
        "description": "Yellow dwarf stars (e.g. the Sun)",
    },
    {
        "class": "K",
        "temp_min": 3700,
        "temp_max": 5200,
        "colour": "Orange",
        "hex": "#ffd4a3",
        "description": "Orange dwarf stars (e.g. Epsilon Eridani)",
    },
    {
        "class": "M",
        "temp_min": 2400,
        "temp_max": 3700,
        "colour": "Red",
        "hex": "#ffcc99",
        "description": "Red dwarf stars (e.g. Proxima Centauri)",
    },
]


class HubbleLaw:
    """Hubble's law: *v = H₀ · d*.

    Parameters
    ----------
    h0 : float
        Hubble constant (km/s per Mpc).  Default 67.8.
    """

    def __init__(self, h0: float = H0) -> None:
        self.h0 = h0

    def velocity(self, distance: float) -> float:
        """Recession velocity *v = H₀ · d*.

        Parameters
        ----------
        distance : float
            Distance to the galaxy (Mpc).

        Returns
        -------
        float
            Recession velocity (km/s).
        """
        return self.h0 * distance

    def distance(self, velocity: float) -> float:
        """Distance from recession velocity *d = v / H₀*.

        Parameters
        ----------
        velocity : float
            Recession velocity (km/s).

        Returns
        -------
        float
            Distance (Mpc).
        """
        return velocity / self.h0

    @property
    def hubble_time(self) -> float:
        """Hubble time *1 / H₀* in seconds.

        An estimate of the age of the universe under the assumption of
        constant expansion.
        """
        # H0 in km/s/Mpc → convert Mpc to km → seconds
        return MEGAPARSEC_IN_KM / self.h0