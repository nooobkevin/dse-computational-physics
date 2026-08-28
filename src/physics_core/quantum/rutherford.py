"""Rutherford (Coulomb) scattering simulation with dependency-injection hooks.

Architecture
------------
:class:`RutherfordScattering` is the **abstract base** that defines the
framework for simulating alpha-particle scattering by a gold nucleus via
Coulomb repulsion.  It defines one physics **hook**:

    ``scattering_angle(self, b: float, E: float) -> float``

that raises ``NotImplementedError`` by default.  Subclasses override the
hook to supply the physics, while :class:`ReferenceRutherfordScattering`
provides the correct reference implementation.

Physics
-------
For a point charge *q₁* (alpha particle, Z₁ = 2) of kinetic energy *E*
approaching a stationary target charge *q₂* (gold nucleus, Z₂ = 79) at
impact parameter *b*, the classical Rutherford scattering angle is:

    θ(b) = 2 · atan( k / (E · b) )

where k = Z₁ Z₂ e² / (4 π ε₀).  This is the standard Coulomb scattering
formula derived from the two-body problem with the target mass >> projectile
mass (gold nucleus ~197 amu, alpha ~4 amu → effectively stationary target).

In the centre-of-mass frame, the exact closed-form result is:

    θ = 2 · atan( (Z₁ Z₂ e²) / (16 π ε₀ E b) )

when the projectile mass is negligible compared to the target mass, and
with the factor-of-2 difference depending on whether one uses the reduced
mass or the laboratory scattering angle.  Here we use the lab-frame result
directly in the small-angle Rutherford form.

    θ(b) = 2 · atan( k / (2 · E · b) )

with the conventional factor such that the head-on (b → 0) limit gives
θ → π (180° backscattering).

References
----------
- Rutherford, E. "The Scattering of α and β Particles by Matter and the
  Structure of the Atom." Phil. Mag. 21, 669 (1911).
- Standard textbook derivation: θ = 2 arctan(Z₁ Z₂ e² / (8 π ε₀ E b))
  for the laboratory scattering angle when target mass >> projectile mass.

State representation
--------------------
Internal state tracks ``{"b", "E", "theta", "t"}``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
K_COULOMB = 8.987551787e9  # 1/(4 π ε₀) in N·m²/C²
E_CHARGE = 1.602176634e-19  # elementary charge (C)


class RutherfordScattering:
    """Abstract base Rutherford scattering simulation.

    Parameters
    ----------
    Z1 : int
        Atomic number of the projectile (default 2 for alpha particle).
    Z2 : int
        Atomic number of the target (default 79 for gold).
    b : float
        Impact parameter (m).  Default 1e-14.
    E : float
        Kinetic energy of the projectile (J).  Default 5 MeV in J.
    """

    def __init__(
        self,
        Z1: int = 2,
        Z2: int = 79,
        b: float = 1e-14,
        E: float = 5.0e6 * E_CHARGE,  # 5 MeV in J
    ) -> None:
        self.Z1 = Z1
        self.Z2 = Z2
        self._b = b
        self._E = E
        self._t = 0.0

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def scattering_angle(self, b: float, E: float) -> float:
        """Compute the Rutherford scattering angle for given impact
        parameter and energy.

        Parameters
        ----------
        b : float
            Impact parameter (m).
        E : float
            Projectile kinetic energy (J).

        Returns
        -------
        float
            Scattering angle θ in radians (0 ≤ θ ≤ π).
        """
        raise NotImplementedError(
            "Subclasses must implement scattering_angle(self, b, E)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step (no-op for static calc)."""
        h = dt if dt is not None else 0.01
        self._t += h

    @property
    def state(self) -> Dict[str, float | int]:
        """Current simulation state ``{"b", "E", "theta", "t"}``."""
        return {
            "b": self._b,
            "E": self._E,
            "theta": self.scattering_angle(self._b, self._E),
            "t": self._t,
        }

    @property
    def energy(self) -> float:
        """Projectile kinetic energy (J)."""
        return self._E

    # ------------------------------------------------------------------
    # Derived helpers
    # ------------------------------------------------------------------
    def impact_parameters(self, n: int, b_max: float | None = None) -> List[float]:
        """Generate a sequence of impact parameters for visualisation.

        Parameters
        ----------
        n : int
            Number of impact parameters.
        b_max : float or None
            Maximum impact parameter (default 10× current b).

        Returns
        -------
        list[float]
            Impact parameters in metres, including a very small value
            for the nearly-head-on case.
        """
        if b_max is None:
            b_max = self._b * 10.0
        # Include b=0 (head-on) approximately by starting at a tiny value
        b_min = b_max * 1e-6
        return [b_min + (b_max - b_min) * i / max(n - 1, 1) for i in range(n)]

    def coulomb_constant(self) -> float:
        """Compute k = Z₁ Z₂ e² / (4 π ε₀).

        Returns
        -------
        float
            Coulomb constant product in N·m².
        """
        return K_COULOMB * self.Z1 * self.Z2 * E_CHARGE * E_CHARGE

    def trajectory_points(
        self, b: float, E: float, n_points: int = 200, r_max: float = 5e-13
    ) -> List[Tuple[float, float]]:
        """Generate (x, y) trajectory points for the alpha particle path.

        Uses the analytical Rutherford scattering hyperbola.  The incoming
        asymptote approaches from y = b (the impact parameter) and the
        outgoing asymptote is rotated by the scattering angle θ.

        Parameters
        ----------
        b : float
            Impact parameter (m).
        E : float
            Projectile kinetic energy (J).
        n_points : int
            Number of points to generate.
        r_max : float
            Maximum distance from origin (m) for the trajectory extent.

        Returns
        -------
        list[(float, float)]
            List of (x, y) trajectory points.
        """
        theta = self.scattering_angle(b, E)
        if theta >= math.pi - 1e-12:
            # Head-on: straight in and straight back
            pts: List[Tuple[float, float]] = []
            for i in range(n_points):
                frac = -1.0 + 2.0 * i / max(n_points - 1, 1)
                x = frac * r_max
                y = 0.0
                pts.append((x, y))
            return pts

        # For non-head-on, compute the hyperbolic trajectory using the
        # Rutherford formula.  The eccentricity e_hyp = 1 / sin(θ/2).
        sin_half = math.sin(theta / 2.0)
        if sin_half < 1e-12:
            sin_half = 1e-12
        eccentricity = 1.0 / sin_half

        # Closest approach distance (distance of closest approach for
        # head-on would be k/E; here we use the standard result)
        k = self.coulomb_constant()
        d_min = k / max(E, 1e-30)  # distance of closest approach for head-on
        a_hyp = d_min / 2.0  # semi-major axis of hyperbola

        pts = []
        # Parameter sweep: angle from -π + δ to π - δ (avoid asymptotes)
        delta = 0.05
        angles = [
            -math.pi + delta + (2.0 * math.pi - 2.0 * delta) * i / max(n_points - 1, 1)
            for i in range(n_points)
        ]

        for phi in angles:
            # Polar form of hyperbola: r = a·(e² - 1) / (1 + e·cos(φ))
            denom = 1.0 + eccentricity * math.cos(phi)
            if abs(denom) < 1e-15:
                continue
            r = a_hyp * (eccentricity * eccentricity - 1.0) / denom
            if r > r_max:
                continue

            # Rotate so the scattering plane is correct: incoming from
            # the left (x < 0), outgoing deflected by θ
            # phi ranges from -(π-δ) to +(π-δ), so the particle
            # comes from the right of the hyperbola and goes to the left
            x = r * math.cos(phi + math.pi - theta / 2.0)
            y = r * math.sin(phi + math.pi - theta / 2.0) + b

            pts.append((x, y))

        return pts


class ReferenceRutherfordScattering(RutherfordScattering):
    """Reference Rutherford scattering with correct physics.

    The scattering angle is given by the classical Coulomb formula:

        θ(b) = 2 · atan( (Z₁ Z₂ e²) / (8 π ε₀ E b) )

    In the head-on limit (b → 0), θ → π (180° backscattering).
    For large impact parameters, θ → 0 (no deflection).
    """

    def scattering_angle(self, b: float, E: float) -> float:
        """θ(b) = 2 · atan( k / (2 · E · b) )

        where k = Z₁ Z₂ e² / (4 π ε₀).

        Parameters
        ----------
        b : float
            Impact parameter (m).
        E : float
            Projectile kinetic energy (J).

        Returns
        -------
        float
            Scattering angle in radians [0, π].
        """
        if b <= 0.0:
            return math.pi
        if E <= 0.0:
            return math.pi

        k = self.coulomb_constant()
        # The lab-frame Rutherford formula:
        # θ = 2·atan(k / (2 · E · b))
        arg = k / (2.0 * E * b)
        return 2.0 * math.atan(arg)