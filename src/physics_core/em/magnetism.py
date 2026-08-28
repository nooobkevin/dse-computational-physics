"""Magnetic field simulation with dependency-injection hooks.

Architecture
-----------
:class:`MagneticField` is the **abstract base**.  It defines one physics
**hook**:

    ``field(self, x, y, z) -> tuple[float, float, float]``

that raises ``NotImplementedError`` by default.  Reference implementations
provide the correct physics for a straight wire and a solenoid.

:class:`MovingCharge` is the **abstract base** for a charged particle
moving through a magnetic field.  Its hooks cover the Lorentz force
magnitude, orbital radius, and trajectory stepping.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
MU_0 = 4.0 * math.pi * 1e-7  # vacuum permeability (T·m/A)


class MagneticField:
    """Abstract base magnetic-field simulation.

    Parameters
    ----------
    position : tuple[float, float]
        Position of the source (m).  Default (0.0, 0.0).
    """

    def __init__(self, position: Tuple[float, float] = (0.0, 0.0)) -> None:
        self._position = position

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def field(self, x: float, y: float, z: float = 0.0) -> Tuple[float, float, float]:
        """Compute magnetic field ``(Bx, By, Bz)`` at point ``(x, y, z)``.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        x : float
            x-coordinate (m).
        y : float
            y-coordinate (m).
        z : float
            z-coordinate (m).  Default 0.0.

        Returns
        -------
        tuple[float, float, float]
            Magnetic field components ``(Bx, By, Bz)`` (T).
        """
        raise NotImplementedError(
            "Subclasses must implement field(self, x, y, z)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """No-op for static fields."""
        pass

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @property
    def state(self) -> Dict[str, float | Tuple[float, float]]:
        return {"position": self._position}


class ReferenceStraightWire(MagneticField):
    """Magnetic field around a long straight current-carrying wire.

    The wire lies along the z-axis.  The field at a radial distance *r*
    is circumferential (right-hand rule):

        B = μ₀ I / (2 π r)

    Parameters
    ----------
    current : float
        Current in the wire (A).  Default 1.0.
    mu0 : float
        Vacuum permeability (T·m/A).  Default 4π × 10⁻⁷.
    """

    def __init__(
        self,
        current: float = 1.0,
        mu0: float = MU_0,
        position: Tuple[float, float] = (0.0, 0.0),
    ) -> None:
        super().__init__(position=position)
        self.I = current
        self.mu0 = mu0

    def field(self, x: float, y: float, z: float = 0.0) -> Tuple[float, float, float]:
        # Displacement from wire position
        dx = x - self._position[0]
        dy = y - self._position[1]
        r = math.sqrt(dx * dx + dy * dy)
        if r < 1e-12:
            return (0.0, 0.0, 0.0)
        B_mag = self.mu0 * self.I / (2.0 * math.pi * r)
        # Circumferential direction (right-hand rule): B ⟂ r̂
        Bx = -B_mag * dy / r
        By = B_mag * dx / r
        return (Bx, By, 0.0)


class ReferenceSolenoid(MagneticField):
    """Magnetic field inside an ideal solenoid.

    The field is uniform inside and approximately zero outside:

        B = μ₀ N I / L   (inside, along the axis)

    Parameters
    ----------
    current : float
        Current in the solenoid (A).  Default 1.0.
    N : int
        Number of turns.  Default 100.
    length : float
        Length of the solenoid (m).  Default 0.5.
    mu0 : float
        Vacuum permeability (T·m/A).  Default 4π × 10⁻⁷.
    """

    def __init__(
        self,
        current: float = 1.0,
        N: int = 100,
        length: float = 0.5,
        mu0: float = MU_0,
        position: Tuple[float, float] = (0.0, 0.0),
    ) -> None:
        super().__init__(position=position)
        self.I = current
        self.N = N
        self.L = length
        self.mu0 = mu0

    def field(self, x: float, y: float, z: float = 0.0) -> Tuple[float, float, float]:
        # Uniform field along the z-axis inside the solenoid
        B_mag = self.mu0 * self.N * self.I / self.L
        return (0.0, 0.0, B_mag)


# ===========================================================================
# Moving charge in a magnetic field
# ===========================================================================


class MovingCharge:
    """Abstract base for a charged particle moving in a magnetic field.

    Defines physics **hooks** for the Lorentz force magnitude, orbital
    radius, trajectory stepping, and the right-hand rule direction.

    Parameters
    ----------
    m : float
        Particle mass (kg).  Default 1.67e-27 (proton mass).
    q : float
        Charge (C).  Default 1.602e-19 (elementary charge).
    """

    def __init__(self, m: float = 1.6726219e-27, q: float = 1.602176634e-19) -> None:
        self.m = m
        self.q = q

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------

    def magnetic_force(self, B: float, q: float, v: float, theta_degrees: float) -> float:
        """Magnitude of the Lorentz force ``F = |q| v B sinθ``.

        Parameters
        ----------
        B : float
            Magnetic field strength (T).
        q : float
            Charge (C).
        v : float
            Speed (m/s).
        theta_degrees : float
            Angle between velocity and B field (degrees).

        Returns
        -------
        float
            Force magnitude (N).
        """
        raise NotImplementedError(
            "Subclasses must implement magnetic_force(self, B, q, v, theta_degrees)"
        )

    def orbit_radius(self, m: float, v: float, q: float, B: float) -> float:
        """Orbital radius ``r = m v / (|q| B)`` for circular motion in uniform B.

        Parameters
        ----------
        m : float
            Particle mass (kg).
        v : float
            Speed perpendicular to B (m/s).
        q : float
            Charge (C).
        B : float
            Magnetic field strength (T).

        Returns
        -------
        float
            Radius of circular motion (m).
        """
        raise NotImplementedError(
            "Subclasses must implement orbit_radius(self, m, v, q, B)"
        )

    def trajectory_step(
        self,
        pos: Tuple[float, float],
        vel: Tuple[float, float],
        B: float,
        q: float,
        m: float,
        dt: float,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Advance a charged particle by one time-step in a uniform B field.

        Uses the Lorentz force ``F = q (v × B)`` with a semi-implicit
        Euler integration.  The B field is assumed uniform along +z
        (out of the page), so the force in the xy-plane is:

            a_x = (q / m) * v_y * B
            a_y = (q / m) * (-v_x) * B

        Parameters
        ----------
        pos : tuple[float, float]
            Current position ``(x, y)`` (m).
        vel : tuple[float, float]
            Current velocity ``(vx, vy)`` (m/s).
        B : float
            Magnetic field strength along +z (T).
        q : float
            Charge (C).
        m : float
            Particle mass (kg).
        dt : float
            Time step (s).

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            ``(new_pos, new_vel)`` — updated position and velocity.
        """
        raise NotImplementedError(
            "Subclasses must implement trajectory_step(self, pos, vel, B, q, m, dt)"
        )

    def right_hand_rule(
        self, v_direction: str, B_direction: str
    ) -> str:
        """Return the force direction label for a positive charge.

        Parameters
        ----------
        v_direction : str
            Velocity direction (e.g. ``"+x"``, ``"+y"``).
        B_direction : str
            Magnetic field direction (e.g. ``"+z"``).

        Returns
        -------
        str
            Force direction label (e.g. ``"+y"``, ``"-y"``).
        """
        raise NotImplementedError(
            "Subclasses must implement right_hand_rule(self, v_direction, B_direction)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------

    @property
    def state(self) -> Dict[str, float]:
        return {"m": self.m, "q": self.q}


class ReferenceMovingCharge(MovingCharge):
    """Reference implementation of a moving charge in a uniform B field.

    Physics
    -------
    - Lorentz force magnitude: ``F = |q| v B sinθ``
    - Orbital radius: ``r = m v / (|q| B)``
    - Trajectory: semi-implicit Euler integration of ``F = q(v × B)``
    - Right-hand rule: for ``v × B`` with positive q
    """

    def magnetic_force(self, B: float, q: float, v: float, theta_degrees: float) -> float:
        theta = math.radians(theta_degrees)
        return abs(q) * v * B * math.sin(theta)

    def orbit_radius(self, m: float, v: float, q: float, B: float) -> float:
        return m * v / (abs(q) * B)

    def trajectory_step(
        self,
        pos: Tuple[float, float],
        vel: Tuple[float, float],
        B: float,
        q: float,
        m: float,
        dt: float,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        # Boris algorithm for charged particle in uniform B field (B along +z).
        # This is the standard numerical integrator for Lorentz-force motion
        # and conserves the gyro-radius to machine precision.
        #
        # Step 1: half acceleration from E field (none here — v_minus = vel)
        vx_minus = vel[0]
        vy_minus = vel[1]

        # Step 2: rotation by angle 2*arctan(t) where t = (q*B/m)*(dt/2)
        t_rot = (q * B / m) * (dt / 2.0)
        # v' = v_minus + v_minus × t_hat  (t_hat = (0, 0, t_rot))
        vx_prime = vx_minus + vy_minus * t_rot
        vy_prime = vy_minus - vx_minus * t_rot
        s = 2.0 * t_rot / (1.0 + t_rot * t_rot)
        # v_plus = v_minus + v' × s_hat  (s_hat = (0, 0, s))
        vx_plus = vx_minus + vy_prime * s
        vy_plus = vy_minus - vx_prime * s

        # Step 3: half acceleration from E field (none here — v_new = v_plus)
        vx_new = vx_plus
        vy_new = vy_plus

        # Position update
        x_new = pos[0] + vx_new * dt
        y_new = pos[1] + vy_new * dt
        return (x_new, y_new), (vx_new, vy_new)

    def right_hand_rule(
        self, v_direction: str, B_direction: str
    ) -> str:
        # Cross-product lookup table for v × B
        # Returns the direction of F = q(v × B) for positive q
        cross: Dict[Tuple[str, str], str] = {
            ("+x", "+z"): "+y",
            ("+x", "-z"): "-y",
            ("-x", "+z"): "-y",
            ("-x", "-z"): "+y",
            ("+y", "+z"): "-x",
            ("+y", "-z"): "+x",
            ("-y", "+z"): "+x",
            ("-y", "-z"): "-x",
        }
        return cross.get((v_direction, B_direction), "?")


# ===========================================================================
# Bar-magnet dipole field
# ===========================================================================


class ReferenceBarMagnet(MagneticField):
    """Magnetic dipole field of a bar magnet aligned along the x-axis.

    The field is modelled as a point magnetic dipole with moment *M*
    pointing in the +x direction:

        B = (μ₀ / 4π) [3 (m·r̂) r̂ - m] / r³

    where *m* = (M, 0, 0) is the dipole moment.

    Parameters
    ----------
    moment : float
        Magnetic dipole moment (A·m²).  Default 1.0.
    mu0 : float
        Vacuum permeability (T·m/A).  Default 4π × 10⁻⁷.
    """

    def __init__(
        self,
        moment: float = 1.0,
        mu0: float = MU_0,
        position: Tuple[float, float] = (0.0, 0.0),
    ) -> None:
        super().__init__(position=position)
        self.M = moment
        self.mu0 = mu0

    def field(self, x: float, y: float, z: float = 0.0) -> Tuple[float, float, float]:
        dx = x - self._position[0]
        dy = y - self._position[1]
        r2 = dx * dx + dy * dy
        if r2 < 1e-12:
            return (0.0, 0.0, 0.0)
        r = math.sqrt(r2)
        r5 = r2 * r2 * r
        # Dipole field: Bx = (μ₀/4π) * M * (3x² - r²) / r⁵
        #             By = (μ₀/4π) * M * 3xy / r⁵
        pref = self.mu0 * self.M / (4.0 * math.pi)
        Bx = pref * (3.0 * dx * dx - r2) / r5
        By = pref * (3.0 * dx * dy) / r5
        return (Bx, By, 0.0)