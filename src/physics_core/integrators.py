"""Generic ODE steppers for first- and second-order systems.

All steppers operate on a **state dict** with at least the keys ``"x"``
(position / generalised coordinate) and ``"v"`` (velocity / first derivative).
The *deriv* callable has the signature ``deriv(x, v, t) -> float`` and returns
the acceleration (second derivative) at the given state.

Example
-------
>>> def spring(x, v, t):
...     return -x          # unit mass, unit stiffness
>>> state = {"x": 1.0, "v": 0.0}
>>> for _ in range(100):
...     state = euler_step(state, 0.01, spring)
"""

from __future__ import annotations

import copy
from typing import Callable, Dict

# A state dict must contain at least "x" and "v".
# Consumers may also store "t" (time); steppers update it if present.
State = Dict[str, float]
DerivFn = Callable[[float, float, float], float]


def euler_step(state: State, dt: float, deriv: DerivFn) -> State:
    """Forward-Euler integration step.

    Parameters
    ----------
    state : dict
        Must contain ``"x"`` and ``"v"``.  May contain ``"t"`` (time).
    dt : float
        Time-step size.
    deriv : callable
        ``deriv(x, v, t) -> acceleration``.

    Returns
    -------
    dict
        Updated state after one step.
    """
    x, v, t = state["x"], state["v"], state.get("t", 0.0)
    a = deriv(x, v, t)
    x_new = x + dt * v
    v_new = v + dt * a
    new: State = {"x": x_new, "v": v_new}
    if "t" in state:
        new["t"] = t + dt
    return new


def verlet_step(state: State, dt: float, deriv: DerivFn) -> State:
    """Velocity-Verlet integration step (symplectic, energy-stable).

    For conservative systems (e.g. simple harmonic oscillator) the total
    energy is conserved to O(dt²) and does not drift over long integrations.

    Algorithm
    ---------
    1. v(t + dt/2) = v(t) + (dt/2) * a(x(t), v(t), t)
    2. x(t + dt)   = x(t) + dt * v(t + dt/2)
    3. a_new       = a(x(t+dt), v(t+dt/2), t+dt)
    4. v(t + dt)   = v(t + dt/2) + (dt/2) * a_new

    Parameters
    ----------
    state : dict
        Must contain ``"x"`` and ``"v"``.  May contain ``"t"`` (time).
    dt : float
        Time-step size.
    deriv : callable
        ``deriv(x, v, t) -> acceleration``.

    Returns
    -------
    dict
        Updated state after one step.
    """
    x, v, t = state["x"], state["v"], state.get("t", 0.0)

    # Half-step velocity
    a_half = deriv(x, v, t)
    v_half = v + 0.5 * dt * a_half

    # Full-step position
    x_new = x + dt * v_half

    # Full-step acceleration, then full-step velocity
    a_new = deriv(x_new, v_half, t + dt)
    v_new = v_half + 0.5 * dt * a_new

    new: State = {"x": x_new, "v": v_new}
    if "t" in state:
        new["t"] = t + dt
    return new