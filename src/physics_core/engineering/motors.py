"""Motor and transformer simulations with dependency-injection hooks.

Architecture
------------
:class:`Motor` is the **abstract base** for a DC motor simulation.
:class:`Transformer` is the **abstract base** for an ideal transformer.
Both define physics hooks that raise ``NotImplementedError`` by default.
Reference implementations provide the correct physics.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple


# ===========================================================================
# Motor
# ===========================================================================


class Motor:
    """Abstract base DC motor simulation.

    Parameters
    ----------
    B : float
        Magnetic field strength (T).  Default 0.5.
    I : float
        Current in the armature (A).  Default 2.0.
    L : float
        Length of conductor in the field (m).  Default 0.1.
    N : int
        Number of turns.  Default 1.
    """

    def __init__(
        self,
        B: float = 0.5,
        I: float = 2.0,
        L: float = 0.1,
        N: int = 1,
    ) -> None:
        self.B = B
        self.I = I
        self.L = L
        self.N = N
        self._state: Dict[str, float] = {
            "B": B,
            "I": I,
            "L": L,
            "theta": 0.0,
            "omega": 0.0,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def torque(self) -> float:
        """Compute the torque on the armature.

        Override this in subclasses to supply the physics.

        Returns
        -------
        float
            Torque (N·m).
        """
        raise NotImplementedError(
            "Subclasses must implement torque(self)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the motor simulation by one time-step."""
        h = dt if dt is not None else 0.01
        tau = self.torque()
        # Simple rotational dynamics: τ = I α, ω += α dt, θ += ω dt
        inertia = 0.01  # kg·m²
        alpha = tau / inertia
        self._state["omega"] += alpha * h
        self._state["theta"] += self._state["omega"] * h
        self._state["t"] += h

    @property
    def state(self) -> Dict[str, Any]:
        """Current simulation state."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Armature position (schematic)."""
        theta = self._state["theta"]
        return (math.cos(theta), math.sin(theta))

    def energy(self) -> Dict[str, float]:
        """Kinetic energy of the armature."""
        omega = self._state["omega"]
        return {"kinetic": 0.5 * 0.01 * omega * omega}


class ReferenceMotor(Motor):
    """Reference DC motor with correct torque physics.

    The force on a current-carrying conductor in a magnetic field is:

        F = B I L

    The torque on a coil of N turns is:

        τ = N B I L r  (where r is the coil radius)
    """

    def __init__(
        self,
        B: float = 0.5,
        I: float = 2.0,
        L: float = 0.1,
        N: int = 1,
        radius: float = 0.05,
    ) -> None:
        super().__init__(B=B, I=I, L=L, N=N)
        self.radius = radius

    def torque(self) -> float:
        theta = self._state["theta"]
        # τ = N B I L r cos(θ) — torque varies with armature angle
        return self.N * self.B * self.I * self.L * self.radius * math.cos(theta)


# ===========================================================================
# Transformer
# ===========================================================================


class Transformer:
    """Abstract base ideal transformer simulation.

    Parameters
    ----------
    Np : int
        Number of turns on the primary coil.  Default 100.
    Ns : int
        Number of turns on the secondary coil.  Default 50.
    Vp : float
        Primary voltage (V).  Default 230.0.
    Rp : float
        Primary-side resistance (Ω).  Default 10.0.
    """

    def __init__(
        self,
        Np: int = 100,
        Ns: int = 50,
        Vp: float = 230.0,
        Rp: float = 10.0,
    ) -> None:
        self.Np = Np
        self.Ns = Ns
        self.Vp = Vp
        self.Rp = Rp
        self._state: Dict[str, float] = {
            "Np": float(Np),
            "Ns": float(Ns),
            "Vp": Vp,
            "Vs": 0.0,
            "Ip": 0.0,
            "Is": 0.0,
            "t": 0.0,
        }

    # ------------------------------------------------------------------
    # Physics hooks — subclasses MUST override
    # ------------------------------------------------------------------
    def secondary_voltage(self) -> float:
        """Compute the secondary voltage.

        Override this in subclasses to supply the physics.

        Returns
        -------
        float
            Secondary voltage (V).
        """
        raise NotImplementedError(
            "Subclasses must implement secondary_voltage(self)"
        )

    def primary_current(self) -> float:
        """Compute the primary current.

        Override this in subclasses to supply the physics.

        Returns
        -------
        float
            Primary current (A).
        """
        raise NotImplementedError(
            "Subclasses must implement primary_current(self)"
        )

    # ------------------------------------------------------------------
    # Framework methods
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the transformer simulation by one time-step."""
        self._state["Vs"] = self.secondary_voltage()
        self._state["Ip"] = self.primary_current()

    @property
    def state(self) -> Dict[str, Any]:
        """Current simulation state."""
        return dict(self._state)

    def position(self) -> Tuple[float, float]:
        """Placeholder."""
        return (0.0, 0.0)

    def energy(self) -> Dict[str, float]:
        """Power in the transformer."""
        Vp = self._state["Vp"]
        Ip = self._state["Ip"]
        Vs = self._state["Vs"]
        Is = self._state.get("Is", 0.0)
        return {
            "primary_power": Vp * Ip,
            "secondary_power": Vs * Is,
        }


class ReferenceTransformer(Transformer):
    """Reference ideal transformer with correct physics.

    For an ideal transformer:

        Vp / Vs = Np / Ns
        Ip / Is = Ns / Np
        Vp * Ip = Vs * Is  (power conservation)
    """

    def __init__(
        self,
        Np: int = 100,
        Ns: int = 50,
        Vp: float = 230.0,
        Rp: float = 10.0,
        load_resistance: float = 20.0,
    ) -> None:
        super().__init__(Np=Np, Ns=Ns, Vp=Vp, Rp=Rp)
        self.load_resistance = load_resistance

    def secondary_voltage(self) -> float:
        """Vs = Vp * Ns / Np."""
        if self.Np == 0:
            return 0.0
        return self.Vp * self.Ns / self.Np

    def primary_current(self) -> float:
        """Ip = Vs / (load_R * (Np/Ns))  (reflected load)."""
        Vs = self.secondary_voltage()
        if self.load_resistance <= 0:
            return 0.0
        Is = Vs / self.load_resistance
        self._state["Is"] = Is
        # Ip = Is * Ns / Np
        if self.Np == 0:
            return 0.0
        return Is * self.Ns / self.Np