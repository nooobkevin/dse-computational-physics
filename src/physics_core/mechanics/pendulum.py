"""Pendulum simulation with dependency-injection hooks.

Architecture
------------
:class:`PendulumSim` is the **abstract base** that all three front-ends
(Manim visualizer, OpenCV teacher app, student fill-in exercise) share.
It implements framework methods (``step``, ``state``, ``position``,
``energy``, ``period_from_formula``, ``steady_state_amplitude``) and
defines one physics **hook**:

    ``angular_acceleration(self, theta, omega) -> float``

that raises ``NotImplementedError`` by default.  Subclasses override the
hook to supply the physics — students fill it in, while
:class:`ReferencePendulumSim` provides the correct reference implementation.

The base classes also support a harmonic **driving force**
``(F0/m)·cos(ω_d·t)`` via the ``driving_amplitude`` (F0) and
``driving_frequency`` (ω_d) parameters.  The ``_deriv`` adapter keeps the
internal clock (``self._state["t"]``) in sync with the integrator time so
the hook can read it; :class:`ReferencePendulumSim` applies the driven term
in its ``angular_acceleration`` while keeping the hook signature
``(theta, omega)`` unchanged, so the di-hook design stays consistent.

State representation
--------------------
Internal state is a dict ``{"theta": ..., "omega": ..., "t": ...}`` consumed
by the generic integrators in :mod:`physics_core.integrators`.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple

from physics_core.integrators import euler_step, verlet_step

# ---------------------------------------------------------------------------
# Default physical constants
# ---------------------------------------------------------------------------
G = 9.81  # gravitational acceleration (m/s²)


# ---------------------------------------------------------------------------
# Steady-state amplitude of a linearised driven, damped oscillator
# ---------------------------------------------------------------------------
def steady_state_amplitude(
    omega_d: float,
    g: float,
    length: float,
    damping_coefficient: float,
) -> float:
    """Linearised steady-state amplitude ``A(ω_d)`` of a driven oscillator.

    For the small-angle (linearised) equation
    ``θ'' + b·θ' + ω₀²·θ = (F₀/m)·cos(ω_d·t)`` with ``ω₀ = √(g/L)``, the
    steady-state response amplitude is

        A(ω_d) = (g/L) / sqrt((ω₀² - ω_d²)² + (b·ω_d)²)

    This is a **normalised** resonance response curve (the driving-strength
    factor has been folded into the ``g/L`` normalisation).  Its peak value
    ``A(ω₀) = ω₀/b`` sits at ``ω_d = √(ω₀² - b²/2)`` for a damped oscillator
    (slightly *below* ``ω₀``); as ``ω_d → ∞`` the amplitude falls to zero.

    Parameters
    ----------
    omega_d : float
        Driving angular frequency (rad/s).
    g : float
        Gravitational acceleration (m/s²).
    length : float
        Pendulum length (m).
    damping_coefficient : float
        Linear damping coefficient ``b`` (s⁻¹).

    Returns
    -------
    float
        Steady-state response amplitude (dimensionless).
    """
    omega0 = math.sqrt(g / length)
    denom_sq = (omega0**2 - omega_d**2) ** 2 + (damping_coefficient * omega_d) ** 2
    return (g / length) / math.sqrt(denom_sq)


class PendulumSim:
    """Abstract base pendulum simulation.

    Parameters
    ----------
    length : float
        Pendulum length (m).
    g : float
        Gravitational acceleration (m/s²).  Default 9.81.
    mass : float
        Bob mass (kg).  Default 1.0.
    theta0 : float
        Initial angular displacement (rad).  Default 0.1.
    omega0 : float
        Initial angular velocity (rad/s).  Default 0.0.
    dt : float
        Default time-step (s).  Default 0.01.
    scheme : str
        Integration scheme — ``"euler"`` or ``"verlet"`` (default).
    small_angle : bool
        If True, use the small-angle approximation sin(θ) ≈ θ in the
        reference implementation.  Default False.
    damping_coefficient : float
        Linear damping coefficient ``b`` — the ``-b·ω`` term.  Default 0.0
        (undamped, backward compatible).
    driving_amplitude : float
        Amplitude ``F0`` of the sinusoidal driving force (N).  The driving
        term is ``(F0/m)·cos(ω_d·t)``.  Default 0.0 (no driving,
        backward compatible).
    driving_frequency : float
        Angular frequency ``ω_d`` of the driving force (rad/s).  Default 0.0.
        Only relevant when *driving_amplitude* > 0.
    """

    def __init__(
        self,
        length: float = 1.0,
        g: float = G,
        mass: float = 1.0,
        theta0: float = 0.1,
        omega0: float = 0.0,
        dt: float = 0.01,
        scheme: str = "verlet",
        small_angle: bool = False,
        damping_coefficient: float = 0.0,
        driving_amplitude: float = 0.0,
        driving_frequency: float = 0.0,
    ) -> None:
        self.length = length
        self.g = g
        self.mass = mass
        self.dt = dt
        self.small_angle = small_angle
        self.damping_coefficient = damping_coefficient
        self.driving_amplitude = driving_amplitude
        self.driving_frequency = driving_frequency

        if scheme not in ("euler", "verlet"):
            raise ValueError(f"scheme must be 'euler' or 'verlet', got {scheme!r}")
        self._scheme = scheme

        # Internal state dict
        self._state: Dict[str, float] = {
            "theta": theta0,
            "omega": omega0,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def angular_acceleration(self, theta: float, omega: float) -> float:
        """Compute angular acceleration ``d²θ/dt²``.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        theta : float
            Current angular displacement (rad).
        omega : float
            Current angular velocity (rad/s).

        Returns
        -------
        float
            Angular acceleration (rad/s²).
        """
        raise NotImplementedError(
            "Subclasses must implement angular_acceleration(self, theta, omega)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def _deriv(self, theta: float, omega: float, t: float) -> float:
        """Adapter that calls the hook.

        The hook signature is ``angular_acceleration(theta, omega)``, but the
        driven reference implementation needs the current time *t* for the
        ```(F0/m)·cos(ω_d·t)`` term.  We sync the internal clock to *t* so the
        hook can read ``self._state["t"]``.  The mutation is transient: ``step``
        reassigns ``self._state`` from the integrator result immediately after.
        """
        self._state["t"] = t
        return self.angular_acceleration(theta, omega)

    def step(self, dt: float | None = None) -> None:
        """Advance the simulation by one time-step.

        Parameters
        ----------
        dt : float or None
            Step size.  Uses ``self.dt`` if None.
        """
        h = dt if dt is not None else self.dt
        stepper = verlet_step if self._scheme == "verlet" else euler_step

        # Map pendulum state (theta, omega) to integrator state (x, v)
        int_state = {
            "x": self._state["theta"],
            "v": self._state["omega"],
            "t": self._state["t"],
        }
        int_result = stepper(int_state, h, self._deriv)
        self._state = {
            "theta": int_result["x"],
            "omega": int_result["v"],
            "t": int_result["t"],
        }

    @property
    def state(self) -> Dict[str, float]:
        """Current simulation state ``{"theta", "omega", "t"}``."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Cartesian coordinates ``(x, y)`` of the bob.

        The pivot is at ``(0, 0)``; y points upward.
        """
        theta = self._state["theta"]
        x = self.length * math.sin(theta)
        y = -self.length * math.cos(theta)
        return (x, y)

    def energy(self) -> Dict[str, float]:
        """Kinetic and potential energy at the current state.

        Kinetic energy: ½ m L² ω²
        Gravitational PE: m g (L - y)  — zero at the bottom (θ = 0).

        Returns
        -------
        dict
            ``{"kinetic": ..., "potential": ..., "total": ...}``
        """
        omega = self._state["omega"]
        _, y = self.position()
        ke = 0.5 * self.mass * self.length**2 * omega**2
        pe = self.mass * self.g * (y + self.length)  # zero at bottom (y = -L)
        return {"kinetic": ke, "potential": pe, "total": ke + pe}

    @property
    def period_from_formula(self) -> float:
        """Small-angle period ``T = 2π √(L/g)``."""
        return 2.0 * math.pi * math.sqrt(self.length / self.g)

    @property
    def omega0(self) -> float:
        """Natural angular frequency ``ω₀ = √(g/L)`` (rad/s)."""
        return math.sqrt(self.g / self.length)

    def steady_state_amplitude(self, omega_d: float) -> float:
        """Linearised steady-state response amplitude at driving frequency
        ``ω_d`` using this pendulum's ``g``, ``length`` and damping.

        See :func:`steady_state_amplitude` for the analytic formula.
        """
        return steady_state_amplitude(
            omega_d, self.g, self.length, self.damping_coefficient
        )


class ReferencePendulumSim(PendulumSim):
    """Reference pendulum with the correct physics.

    The angular acceleration is the exact non-linear expression
    ``-(g/L) sin(θ)``, or ``-(g/L) θ`` when *small_angle* is True.
    When *damping_coefficient* > 0, a linear damping term ``-b·ω``
    is added: ``α = -(g/L) sin(θ) - b·ω``.  When *driving_amplitude* > 0, a
    sinusoidal driving term ``(F0/m)·cos(ω_d·t)`` is added, enabling forced
    oscillations and resonance.  The current time is read from the internal
    state (kept in sync by ``_deriv``).
    """

    def angular_acceleration(self, theta: float, omega: float) -> float:
        if self.small_angle:
            a = -(self.g / self.length) * theta
        else:
            a = -(self.g / self.length) * math.sin(theta)
        # Linear damping: -b * omega
        a -= self.damping_coefficient * omega
        # Sinusoidal driving force: (F0/m) * cos(omega_d * t)
        if self.driving_amplitude != 0.0:
            t = self._state["t"]
            a += (self.driving_amplitude / self.mass) * math.cos(
                self.driving_frequency * t
            )
        return a