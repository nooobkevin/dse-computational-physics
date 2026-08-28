"""Bohr hydrogen atom — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of the Bohr hydrogen atom by
overriding the ``energy_level``, ``transition_wavelength``, and
``ionisation_energy`` methods in ``StudentBohrHydrogen``.

The parent class :class:`BohrHydrogen` provides the framework methods.

Physics background
------------------
The Bohr model describes the hydrogen atom with quantised energy levels:

    E_n = −13.6 eV / n²    for n = 1, 2, 3, ...

The Rydberg formula gives the wavelength of emitted/absorbed photons:

    1/λ = R_H · (1/n_f² − 1/n_i²)

where R_H ≈ 1.097 × 10⁷ m⁻¹ is the Rydberg constant.

Equivalently:
    λ = hc / |E_f − E_i|

The ionisation energy from level n is:
    E_ion(n) = 13.6 eV / n²

Constants you can use
---------------------
- h = 6.62607015 × 10⁻³⁴ J·s (Planck's constant)
- c = 299792458 m/s (speed of light)
- E_CHARGE = 1.602176634 × 10⁻¹⁹ C (elementary charge)
- 1 eV = E_CHARGE joules

What to do
----------
1. Implement ``energy_level(n)`` returning E_n in eV.
2. Implement ``transition_wavelength(n_i, n_f)`` returning λ in metres.
3. Implement ``ionisation_energy(n)`` returning E_ion in eV.
4. Run the auto-grader to check your work:

       uv run pytest units/07_quantum/exercises/test_exercise.py \\
           --override-student=units/07_quantum/exercises/hydrogen_exercise.py -v
"""

from __future__ import annotations

from physics_core.quantum.bohr import BohrHydrogen


class StudentBohrHydrogen(BohrHydrogen):
    """Student implementation of the Bohr hydrogen atom.

    Override the three methods below with the correct physics.
    Everything else is inherited from :class:`BohrHydrogen`.

    Example
    -------
    >>> h = StudentBohrHydrogen()
    >>> print(h.energy_level(1))
    """

    def energy_level(self, n: int) -> float:
        """Compute the energy of the *n*-th stationary state.

        E_n = −13.6 eV / n²

        Parameters
        ----------
        n : int
            Principal quantum number (1, 2, 3, ...).

        Returns
        -------
        float
            Energy in eV.

        Physics (fill this in)
        ----------------------
        Replace the line below with:

            return -13.6 / (float(n) * float(n))
        """
        raise NotImplementedError(
            "You must implement energy_level(self, n) "
            "in StudentBohrHydrogen."
        )

    def transition_wavelength(self, n_i: int, n_f: int) -> float:
        """Wavelength of the photon emitted/absorbed in a transition.

        λ = hc / |ΔE|  where ΔE = E_nf − E_ni in joules.

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

        Physics (fill this in)
        ----------------------
        Use ``self.energy_level(n)`` to get energies in eV.
        Convert to joules: 1 eV = E_CHARGE J.
        Then λ = hc / |ΔE|.
        """
        raise NotImplementedError(
            "You must implement transition_wavelength(self, n_i, n_f) "
            "in StudentBohrHydrogen."
        )

    def ionisation_energy(self, n: int) -> float:
        """Energy required to ionise the atom from level *n*.

        E_ion(n) = 13.6 eV / n²

        Parameters
        ----------
        n : int
            Principal quantum number.

        Returns
        -------
        float
            Ionisation energy in eV.
        """
        raise NotImplementedError(
            "You must implement ionisation_energy(self, n) "
            "in StudentBohrHydrogen."
        )