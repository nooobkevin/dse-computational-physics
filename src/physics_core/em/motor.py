"""Electric-motor physics: force on a conductor and torque on a rotating coil.

Architecture
------------
:class:`WireForce` is the **abstract base** for the force on a straight
current-carrying conductor.  It defines one physics **hook**:

    ``force(self, B, I, L, theta_degrees) -> float``

that raises ``NotImplementedError`` by default.

:class:`CoilTorque` is the **abstract base** for the torque on a
rectangular coil.  Its hook:

    ``torque(self, N, B, I, A, phi_degrees) -> float``

returns the *signed* torque (positive when it drives the coil normal
toward the field), matching ``tau = N B I A sin(phi)``.

:class:`DCMotor` is the **abstract base** for a simple DC motor with a
split-ring commutator.  It carries the coil state (angle ``phi``, angular
velocity ``omega``) and advances it with ``step(dt)``.  Its hooks cover the
signed coil torque, the commutator current direction, and the resulting
unidirectional drive torque.

Reference implementations provide the DSE-physics correct results.  All
classes are fully deterministic: the motor response is a pure function of
the supplied parameters and the initial state.
"""

from __future__ import annotations

import math
from typing import Dict

# Supporting the docstring physics: torque on a coil is measured in N·m,
# force on a conductor in N.  The commutator references a half-turn of pi
# radians, i.e. it flips the observed current direction every 180 degrees.


# ---------------------------------------------------------------------------
# Force on a straight current-carrying conductor
# ---------------------------------------------------------------------------


class WireForce:
    """Abstract base for the force on a current-carrying conductor.

    The force on a straight wire of length *L* carrying current *I* in a
    uniform field *B* is ``F = B I L sin(theta)``, where *theta* is the
    angle between the current direction and the field (right-hand rule
    ``F = I (L x B)``).
    """

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def force(
        self, B: float, I: float, L: float, theta_degrees: float
    ) -> float:
        """Magnitude of the force ``F = B I L sin(theta)``.

        Parameters
        ----------
        B : float
            Magnetic field strength (T).
        I : float
            Current (A).
        L : float
            Conductor length inside the field (m).
        theta_degrees : float
            Angle between the current direction and the field (degrees).

        Returns
        -------
        float
            Force magnitude (N).
        """
        raise NotImplementedError(
            "Subclasses must implement force(self, B, I, L, theta_degrees)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    @property
    def state(self) -> Dict[str, float]:
        return {}


class ReferenceWireForce(WireForce):
    """Reference implementation of the conductor force.

    Physics: ``F = B I L sin(theta)``, zero when the wire is parallel to
    the field and maximum when it is perpendicular.
    """

    def force(
        self, B: float, I: float, L: float, theta_degrees: float
    ) -> float:
        theta = math.radians(theta_degrees)
        return B * I * L * math.sin(theta)


# ---------------------------------------------------------------------------
# Torque on a rectangular coil
# ---------------------------------------------------------------------------


class CoilTorque:
    """Abstract base for the torque on a rectangular current-carrying coil.

    A rectangular coil of *N* turns, area *A*, carrying current *I* in a
    uniform field *B* experiences ``tau = N B I A sin(phi)``, where *phi*
    is the angle between the coil normal and the field.  The torque is
    zero when the normal is parallel to the field (phi = 0 or 180 deg) and
    maximum when it is perpendicular (phi = 90 deg).
    """

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def torque(
        self, N: int, B: float, I: float, A: float, phi_degrees: float
    ) -> float:
        """Signed torque ``tau = N B I A sin(phi)``.

        The sign encodes the handedness of the coil (positive drives the
        coil normal toward the field).

        Parameters
        ----------
        N : int
            Number of turns.
        B : float
            Magnetic field strength (T).
        I : float
            Current (A).
        A : float
            Coil area (m²).
        phi_degrees : float
            Angle between the coil normal and the field (degrees).

        Returns
        -------
        float
            Torque (N·m), signed.
        """
        raise NotImplementedError(
            "Subclasses must implement torque(self, N, B, I, A, phi_degrees)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    def torque_magnitude(
        self, N: int, B: float, I: float, A: float, phi_degrees: float
    ) -> float:
        """Absolute value of the torque (N·m), always non-negative."""
        return abs(self.torque(N, B, I, A, phi_degrees))

    @property
    def state(self) -> Dict[str, float]:
        return {}


class ReferenceCoilTorque(CoilTorque):
    """Reference implementation of the coil torque.

    Physics: ``tau = N B I A sin(phi)`` (signed).  Zero at phi=0 and
    phi=180, maximum magnitude at phi=90.
    """

    def torque(
        self, N: int, B: float, I: float, A: float, phi_degrees: float
    ) -> float:
        phi = math.radians(phi_degrees)
        return float(N) * B * I * A * math.sin(phi)


# ---------------------------------------------------------------------------
# Simple DC motor with a split-ring commutator
# ---------------------------------------------------------------------------


class DCMotor:
    """Abstract base for a simple DC motor with a split-ring commutator.

    State
    -----
    ``phi`` : float
        Coil angle (radians), i.e. the angle between the coil normal and
        the field.
    ``omega`` : float
        Angular velocity (rad/s).  Positive = the coil spins in the drive
        direction.

    Parameters
    ----------
    N : int
        Number of coil turns.
    B : float
        Magnetic field strength (T).
    A : float
        Coil area (m²).
    J : float
        Moment of inertia of the rotor (kg·m²).
    current : float
        Supply current magnitude (A), always >= 0.  The commutator decides
        the direction actually seen by the coil each half turn.
    friction : float
        Viscous friction coefficient (N·m·s/rad).  Default 0.0.
    phi : float
        Initial coil angle (radians).
    omega : float
        Initial angular velocity (rad/s).

    The three hooks — ``coil_torque()``, ``commutator_sign()`` and
    ``drive_torque()`` — are subclasses MUST override.
    """

    def __init__(
        self,
        N: int = 1,
        B: float = 1.0,
        A: float = 0.02,
        J: float = 1e-3,
        current: float = 1.0,
        friction: float = 0.0,
        phi: float = 0.0,
        omega: float = 0.0,
    ) -> None:
        self.N = N
        self.B = B
        self.A = A
        self.J = J
        self.I = abs(current)
        self.friction = friction
        self._phi: float = phi
        self._omega: float = omega

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------
    def coil_torque(self) -> float:
        """Signed coil torque ``N B I A sin(phi)`` at the current angle.

        Uses the *supply* current magnitude ``I`` (positive), so the value
        encodes the handedness of the winding with a fixed current
        direction.  The commutator rectifies this in :meth:`drive_torque`.
        """
        raise NotImplementedError(
            "Subclasses must implement coil_torque(self)"
        )

    def commutator_sign(self) -> float:
        """Current direction seen by the coil: ``+1`` or ``-1``.

        The split-ring commutator flips the current direction every half
        turn (every pi radians of ``phi``).
        """
        raise NotImplementedError(
            "Subclasses must implement commutator_sign(self)"
        )

    def drive_torque(self) -> float:
        """Unidirectional drive torque delivered to the shaft.

        ``sign(phi) * coil_torque`` — for positive supply current this is
        the always non-negative ``N B I A |sin(phi)|``.
        """
        raise NotImplementedError(
            "Subclasses must implement drive_torque(self)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    def step(self, dt: float) -> None:
        """Advance the motor by ``dt`` seconds (semi-implicit Euler).

        ``omega += (tau - friction * omega) / J * dt``
        ``phi += omega * dt``
        """
        raise NotImplementedError(
            "Subclasses must implement step(self, dt)"
        )

    def reset(self, phi: float | None = None, omega: float | None = None) -> None:
        """Reset the motor state to an optional new angle/velocity."""
        if phi is not None:
            self._phi = phi
        if omega is not None:
            self._omega = omega

    @property
    def phi(self) -> float:
        return self._phi

    @property
    def omega(self) -> float:
        return self._omega

    @property
    def current_in_coil(self) -> float:
        """Effective current seen by the coil (sign from the commutator)."""
        return self.commutator_sign() * self.I

    @property
    def state(self) -> Dict[str, float]:
        return {
            "phi": self._phi,
            "omega": self._omega,
            "commutator": self.commutator_sign(),
            "drive_torque": self.drive_torque(),
        }


class ReferenceDCMotor(DCMotor):
    """Reference DC motor with correct coil torque and commutator physics.

    Physics
    -------
    - ``coil_torque = N B I A sin(phi)`` (signed, supply current).
    - The split-ring commutator reverses the coil current every half turn:
      ``sign(phi) = +1`` for ``phi mod 2*pi in [0, pi)`` and ``-1``
      otherwise.
    - ``drive_torque = sign(phi) * coil_torque`` is therefore the
      non-negative quantity ``N B I A |sin phi|`` for positive supply
      current, which keeps the rotor turning one way.
    - A viscous friction term bounds the angular speed at a deterministic
      terminal value ``omega_max = drive_torque / friction`` when
      ``friction > 0``.
    """

    def coil_torque(self) -> float:
        return float(self.N) * self.B * self.I * self.A * math.sin(self._phi)

    def commutator_sign(self) -> float:
        # Python's modulo yields a value in [0, 2*pi) even for negative
        # phi, so the half-turn test is well defined for any angle.
        return 1.0 if (self._phi % (2.0 * math.pi)) < math.pi else -1.0

    def drive_torque(self) -> float:
        # Rectified by the commutator: for positive supply current the
        # unidirectional drive is N B I A |sin phi| (>= 0, no reversal).
        return (
            float(self.N) * self.B * self.I * self.A * abs(math.sin(self._phi))
        )

    def step(self, dt: float) -> None:
        tau = self.drive_torque()
        self._omega += (tau - self.friction * self._omega) / self.J * dt
        self._phi += (self._omega * dt)


class ReferenceDCMotorConstant(DCMotor):
    """Reference DC motor using a constant-torque model per half turn.

    .. note::
        This variant is provided as a simple, always-rotating model.  The
        Manim scene ``ElectricMotor`` uses it (a constant drive keeps the
        coil turning smoothly through the zero-torque null points of a
        single coil), while the teacher app uses :class:`ReferenceDCMotor`
        for its live ``tau = N B I A sin(phi)`` readout.
    """

    def coil_torque(self) -> float:
        # A stylised square-wave torque: full magnitude from the supply
        # current (signed).
        return float(self.N) * self.B * self.I * self.A

    def commutator_sign(self) -> float:
        return 1.0 if (self._phi % (2.0 * math.pi)) < math.pi else -1.0

    def drive_torque(self) -> float:
        # Constant magnitude, always positive for I >= 0.
        return float(self.N) * self.B * self.I * self.A

    def step(self, dt: float) -> None:
        tau = self.drive_torque()
        self._omega += (tau - self.friction * self._omega) / self.J * dt
        self._phi += (self._omega * dt)
