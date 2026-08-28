"""Infinite square well simulation with dependency-injection hooks.

Architecture
------------
:class:`QuantumWell` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It defines framework methods (``step``, ``state``, ``position``, ``energy``)
and one physics **hook**:

    ``energy_level(self, n: int) -> float``

that raises ``NotImplementedError`` by default.  Subclasses override the
hook to supply the physics — students fill it in, while
:class:`ReferenceQuantumWell` provides the correct reference implementation.

State representation
--------------------
Internal state is a dict ``{"n": ..., "x": ..., "t": ...}``.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
H = 6.62607015e-34  # Planck constant (J·s)
HBAR = H / (2.0 * math.pi)  # reduced Planck constant (J·s)
M_E = 9.10938356e-31  # electron mass (kg)
E_CHARGE = 1.602176634e-19  # elementary charge (C)


class QuantumWell:
    """Abstract base infinite square well simulation.

    Parameters
    ----------
    L : float
        Width of the well (m).  Default 1e-10 (1 Å).
    m : float
        Particle mass (kg).  Default electron mass.
    n : int
        Quantum number (default 1 = ground state).
    dt : float
        Default time-step (s).  Default 0.01.
    """

    def __init__(
        self,
        L: float = 1e-10,
        m: float = M_E,
        n: int = 1,
        dt: float = 0.01,
    ) -> None:
        self.L = L
        self.m = m
        self.dt = dt
        self._n = n
        self._x = L / 2.0  # default position: centre of well
        self._t = 0.0

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def energy_level(self, n: int) -> float:
        """Compute the energy of the *n*-th stationary state.

        For an infinite square well: E_n = n² h² / (8 m L²)

        Parameters
        ----------
        n : int
            Quantum number (1, 2, 3, ...).

        Returns
        -------
        float
            Energy in joules.
        """
        raise NotImplementedError(
            "Subclasses must implement energy_level(self, n)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        For the quantum well, this is a no-op for stationary states
        (the wavefunction evolves by a global phase, which does not
        affect |ψ|²).  Subclasses may override for time-dependent
        phenomena.

        Parameters
        ----------
        dt : float or None
            Step size.  Uses ``self.dt`` if None.
        """
        h = dt if dt is not None else self.dt
        self._t += h

    @property
    def state(self) -> Dict[str, float | int]:
        """Current simulation state ``{"n", "x", "t"}``."""
        return {"n": self._n, "x": self._x, "t": self._t}

    @property
    def position(self) -> Tuple[float, float]:
        """Current position ``(x, 0)`` — particle position along the well."""
        return (self._x, 0.0)

    @property
    def energy(self) -> float:
        """Energy of the current stationary state (J)."""
        return self.energy_level(self._n)

    # ------------------------------------------------------------------
    # Derived helpers
    # ------------------------------------------------------------------
    def wavefunction(self, x: float, n: int | None = None) -> float:
        """Evaluate the wavefunction ψ_n(x) at position *x*.

        Parameters
        ----------
        x : float
            Position along the well (m).  Must be in [0, L].
        n : int or None
            Quantum number.  Uses ``self._n`` if None.

        Returns
        -------
        float
            ψ_n(x) — the wavefunction value.
        """
        raise NotImplementedError(
            "Subclasses must implement wavefunction(self, x, n)"
        )

    def probability_density(self, x: float, n: int | None = None) -> float:
        """Probability density |ψ_n(x)|² at position *x*.

        Parameters
        ----------
        x : float
            Position along the well (m).
        n : int or None
            Quantum number.  Uses ``self._n`` if None.

        Returns
        -------
        float
            |ψ_n(x)|².
        """
        psi = self.wavefunction(x, n)
        return psi * psi

    def transition_energy(self, n_i: int, n_f: int) -> float:
        """Energy difference between two states: ΔE = E_nf - E_ni.

        Parameters
        ----------
        n_i : int
            Initial quantum number.
        n_f : int
            Final quantum number.

        Returns
        -------
        float
            Transition energy in joules (positive if n_f > n_i).
        """
        return self.energy_level(n_f) - self.energy_level(n_i)

    def de_broglie_wavelength(self, p: float) -> float:
        """Compute the de Broglie wavelength λ = h / p.

        Parameters
        ----------
        p : float
            Momentum (kg·m/s).

        Returns
        -------
        float
            Wavelength (m).
        """
        if p == 0.0:
            raise ValueError("Momentum cannot be zero for de Broglie wavelength")
        return H / p


class ReferenceQuantumWell(QuantumWell):
    """Reference infinite square well with correct physics.

    Energy levels
    -------------
        E_n = n² h² / (8 m L²)

    Wavefunctions
    -------------
        ψ_n(x) = √(2/L) sin(nπx/L)    for 0 ≤ x ≤ L
        ψ_n(x) = 0                     otherwise

    Probability density
    -------------------
        |ψ_n(x)|² = (2/L) sin²(nπx/L)
    """

    def energy_level(self, n: int) -> float:
        """E_n = n² h² / (8 m L²)."""
        if n < 1:
            raise ValueError(f"Quantum number n must be >= 1, got {n}")
        return (n * n * H * H) / (8.0 * self.m * self.L * self.L)

    def wavefunction(self, x: float, n: int | None = None) -> float:
        """ψ_n(x) = √(2/L) sin(nπx/L) for 0 ≤ x ≤ L, else 0."""
        if n is None:
            n = self._n
        if n < 1:
            raise ValueError(f"Quantum number n must be >= 1, got {n}")
        if x < 0.0 or x > self.L:
            return 0.0
        return math.sqrt(2.0 / self.L) * math.sin(n * math.pi * x / self.L)

    def probability_density(self, x: float, n: int | None = None) -> float:
        """|ψ_n(x)|² = (2/L) sin²(nπx/L) for 0 ≤ x ≤ L, else 0."""
        if n is None:
            n = self._n
        if x < 0.0 or x > self.L:
            return 0.0
        psi = self.wavefunction(x, n)
        return psi * psi

    def transition_wavelength(self, n_i: int, n_f: int) -> float:
        """Wavelength of photon emitted/absorbed in a transition.

        ΔE = hc/λ  →  λ = hc / |ΔE|

        Parameters
        ----------
        n_i : int
            Initial quantum number.
        n_f : int
            Final quantum number.

        Returns
        -------
        float
            Photon wavelength (m).
        """
        delta_e = abs(self.transition_energy(n_i, n_f))
        if delta_e == 0.0:
            return float("inf")
        return H * 299792458.0 / delta_e
