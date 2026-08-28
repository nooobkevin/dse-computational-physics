"""Photoelectric effect simulation.

Provides :class:`PhotoElectric` for computing photoelectric effect
quantities: work function, threshold frequency, stopping potential,
and maximum kinetic energy of emitted electrons.

Physics
-------
    E = hf                     (photon energy)
    K_max = hf - φ             (maximum kinetic energy of photoelectrons)
    f_0 = φ / h                (threshold frequency)
    V_0 = (hf - φ) / e         (stopping potential)
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
H = 6.62607015e-34  # Planck constant (J·s)
E_CHARGE = 1.602176634e-19  # elementary charge (C)


class PhotoElectric:
    """Photoelectric effect calculator.

    Parameters
    ----------
    work_function : float
        Work function φ of the metal (J).  Default 2.0 eV converted to J.
    """

    def __init__(self, work_function: float = 2.0 * E_CHARGE) -> None:
        self.phi = work_function

    # ------------------------------------------------------------------
    # Physics methods
    # ------------------------------------------------------------------
    def photon_energy(self, f: float) -> float:
        """Energy of a photon: E = hf.

        Parameters
        ----------
        f : float
            Frequency (Hz).

        Returns
        -------
        float
            Photon energy (J).
        """
        return H * f

    def threshold_frequency(self) -> float:
        """Threshold frequency: f_0 = φ / h.

        Returns
        -------
        float
            Minimum frequency (Hz) required to eject electrons.
        """
        return self.phi / H

    def max_kinetic_energy(self, f: float) -> float:
        """Maximum kinetic energy of photoelectrons: K_max = hf - φ.

        Parameters
        ----------
        f : float
            Incident photon frequency (Hz).

        Returns
        -------
        float
            Maximum kinetic energy (J).  Returns 0 if f < f_0.
        """
        ke = H * f - self.phi
        return max(ke, 0.0)

    def stopping_potential(self, f: float) -> float:
        """Stopping potential: V_0 = (hf - φ) / e.

        Parameters
        ----------
        f : float
            Incident photon frequency (Hz).

        Returns
        -------
        float
            Stopping potential (V).  Returns 0 if f < f_0.
        """
        ke = self.max_kinetic_energy(f)
        return ke / E_CHARGE

    def work_function_eV(self) -> float:
        """Work function in electronvolts."""
        return self.phi / E_CHARGE

    def max_ke_eV(self, f: float) -> float:
        """Maximum kinetic energy in electronvolts."""
        return self.max_kinetic_energy(f) / E_CHARGE
