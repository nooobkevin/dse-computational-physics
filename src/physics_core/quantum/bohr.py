"""Bohr hydrogen atom model — discrete energy levels and spectral transitions.

Architecture
------------
:class:`BohrHydrogen` provides the Bohr model of the hydrogen atom.
It computes energy levels, transition wavelengths, and ionisation energies
for the hydrogen atom according to the Bohr quantization rules.

This class is NOT an abstract base with dependency-injection hooks — it is
a self-contained reference implementation that the exercise's
:class:`StudentBohrHydrogen` subclasses (or a separate exercise class)
provides an override hook for.  The existing :class:`BohrHydrogen` serves
as the reference engine for the Manim scenes and the teacher app.

Physics
-------
The Bohr model of the hydrogen atom postulates quantised electron orbits.
The energy levels are given by:

    E_n = −13.6 eV / n²      for n = 1, 2, 3, ...

where n is the principal quantum number.

The photon wavelength for a transition from level n_i to n_f is:

    1 / λ = R_H · (1/n_f² − 1/n_i²)

where R_H = 1.0974 × 10⁷ m⁻¹ is the Rydberg constant, and λ is the
wavelength in vacuum.

Equivalently:  λ = hc / |E_f − E_i|  (in SI units).

The ionisation energy from level n is:

    E_ion(n) = 0 − E_n = 13.6 eV / n²

This is a classical-quantum hybrid model — it was superseded by the
full quantum-mechanical Schrödinger equation, but remains the standard
pedagogical introduction to quantised energy levels in atoms.

References
----------
- Bohr, N. "On the Constitution of Atoms and Molecules." Phil. Mag. 26, 1 (1913).
- Niels Bohr Institute: https://www.nbi.ku.dk/english/
- HKDSE Physics curriculum item c: Bohr's atomic model of hydrogen
  (lines 2730-2787 of the CAF Consultation Draft).
"""

from __future__ import annotations

import math
from typing import Dict


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
H = 6.62607015e-34  # Planck constant (J·s)
C = 299792458.0  # speed of light (m/s)
E_CHARGE = 1.602176634e-19  # elementary charge (C)


class BohrHydrogen:
    """Bohr model of the hydrogen atom.

    Provides energy levels, transition wavelengths, and ionisation energies
    all in SI units (joules for energies, metres for wavelengths).

    Parameters
    ----------
    Z : int
        Nuclear charge (default 1 for hydrogen).
    """

    def __init__(self, Z: int = 1) -> None:
        self.Z = Z
        # Ground-state energy E₁ in eV for hydrogen (Z=1)
        self._e1_eV = -13.6

    # ------------------------------------------------------------------
    # Physics methods
    # ------------------------------------------------------------------
    def energy_level(self, n: int) -> float:
        """Energy of the *n*-th stationary state.

        E_n = −13.6 eV / n²

        Parameters
        ----------
        n : int
            Principal quantum number (1, 2, 3, ...).

        Returns
        -------
        float
            Energy in eV.
        """
        if n < 1:
            raise ValueError(f"Principal quantum number n must be >= 1, got {n}")
        return self._e1_eV / (float(n) * float(n))

    def energy_joules(self, n: int) -> float:
        """Energy of the *n*-th state in joules."""
        return self.energy_level(n) * E_CHARGE

    def transition_energy(self, n_i: int, n_f: int) -> float:
        """Energy difference between two states ΔE = E_nf − E_ni.

        If n_f > n_i, the atom absorbs energy (positive ΔE, absorption).
        If n_f < n_i, the atom emits energy (|ΔE|, emission).

        Parameters
        ----------
        n_i : int
            Initial principal quantum number.
        n_f : int
            Final principal quantum number.

        Returns
        -------
        float
            Energy difference in eV (positive if n_f > n_i).
        """
        return self.energy_level(n_f) - self.energy_level(n_i)

    def transition_wavelength(self, n_i: int, n_f: int) -> float:
        """Wavelength of the photon emitted or absorbed in a transition.

        Uses the Rydberg formula:
            1/λ = R_H · |1/n_f² − 1/n_i²|

        or equivalently λ = hc / |ΔE|.

        Parameters
        ----------
        n_i : int
            Initial quantum number.
        n_f : int
            Final quantum number.

        Returns
        -------
        float
            Photon wavelength in metres.
        """
        delta_e = self.transition_energy(n_i, n_f)  # in eV
        if delta_e == 0.0:
            return float("inf")
        # Convert eV to J
        delta_e_j = abs(delta_e) * E_CHARGE
        return H * C / delta_e_j

    def ionisation_energy(self, n: int) -> float:
        """Energy required to ionise the atom from level *n*.

        E_ion(n) = 0 − E_n = 13.6 eV / n²

        Parameters
        ----------
        n : int
            Principal quantum number.

        Returns
        -------
        float
            Ionisation energy in eV (always positive).
        """
        return -self.energy_level(n)  # E_n is negative, so this gives positive

    def excitation_energy(self, n: int) -> float:
        """Energy above ground state for level *n*.

        E_exc(n) = E_n − E₁

        Parameters
        ----------
        n : int
            Principal quantum number.

        Returns
        -------
        float
            Excitation energy in eV.
        """
        return self.energy_level(n) - self.energy_level(1)

    # ------------------------------------------------------------------
    # Helper methods for the Balmer / Lyman series
    # ------------------------------------------------------------------
    def lyman_wavelength(self, n: int) -> float:
        """Wavelength for Lyman series transition (n → 1).

        Parameters
        ----------
        n : int
            Upper level (n ≥ 2).

        Returns
        -------
        float
            Wavelength in metres.
        """
        return self.transition_wavelength(n, 1)

    def balmer_wavelength(self, n: int) -> float:
        """Wavelength for Balmer series transition (n → 2).

        Parameters
        ----------
        n : int
            Upper level (n ≥ 3).

        Returns
        -------
        float
            Wavelength in metres.
        """
        return self.transition_wavelength(n, 2)

    # ------------------------------------------------------------------
    # State representation (for compatibility with physics engine pattern)
    # ------------------------------------------------------------------
    @property
    def state(self) -> Dict[str, float | int]:
        """Current state stub — tracks the last queried levels."""
        return {
            "Z": self.Z,
            "E_1": self.energy_level(1),
        }

    def step(self, dt: float | None = None) -> None:
        """No-op (static model)."""
        pass