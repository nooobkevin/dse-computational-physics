"""Ideal-curve overlay helpers using ``physics_core`` reference simulations.

Provides functions that run the reference simulators and return arrays of
data points that can be drawn into the OpenCV frame with ``cv2.polylines``.
"""

from __future__ import annotations

import math
from typing import List, Tuple

import numpy as np

from physics_core.mechanics.pendulum import ReferencePendulumSim
from physics_core.mechanics.circular import CircularMotion
from physics_core.mechanics.projectile import ReferenceProjectileSim


def pendulum_ideal_trace(
    length: float,
    theta0: float,
    g: float = 9.81,
    duration: float = 10.0,
    dt: float = 0.01,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run the reference pendulum and return time, theta, omega arrays.

    Returns
    -------
    t_arr : np.ndarray
        Time values (s).
    theta_arr : np.ndarray
        Angular displacement (rad).
    omega_arr : np.ndarray
        Angular velocity (rad/s).
    """
    sim = ReferencePendulumSim(length=length, g=g, theta0=theta0, dt=dt)
    steps = int(duration / dt)
    t_vals = np.empty(steps)
    theta_vals = np.empty(steps)
    omega_vals = np.empty(steps)
    for i in range(steps):
        s = sim.state
        t_vals[i] = s["t"]
        theta_vals[i] = s["theta"]
        omega_vals[i] = s["omega"]
        sim.step()
    return t_vals, theta_vals, omega_vals


def circular_trace(
    radius: float,
    omega0: float,
    duration: float = 10.0,
    dt: float = 0.01,
) -> Tuple[np.ndarray, np.ndarray]:
    """Run circular motion and return x, y position arrays."""
    sim = CircularMotion(radius=radius, omega0=omega0, dt=dt)
    steps = int(duration / dt)
    xs = np.empty(steps)
    ys = np.empty(steps)
    for i in range(steps):
        x, y = sim.position
        xs[i] = x
        ys[i] = y
        sim.step()
    return xs, ys


def projectile_trajectory(
    vx0: float,
    vy0: float,
    g: float = 9.81,
    dt: float = 0.01,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Run projectile sim until y < 0 and return x, y, vx, vy arrays."""
    sim = ReferenceProjectileSim(vx0=vx0, vy0=vy0, dt=dt)
    xs: List[float] = []
    ys: List[float] = []
    vxs: List[float] = []
    vys: List[float] = []
    while True:
        pos = sim.position
        v = sim.velocity
        xs.append(pos[0])
        ys.append(pos[1])
        vxs.append(v[0])
        vys.append(v[1])
        if pos[1] < 0 and len(xs) > 2:
            break
        sim.step()
    return (
        np.array(xs),
        np.array(ys),
        np.array(vxs),
        np.array(vys),
    )


# ---------------------------------------------------------------------------
# Drawing helpers — map physics coordinates to pixel space
# ---------------------------------------------------------------------------


def world_to_pixel(
    x_world: float,
    y_world: float,
    origin_px: Tuple[int, int],
    scale: float,
    invert_y: bool = True,
) -> Tuple[int, int]:
    """Convert a physics-coordinate point to pixel coordinates.

    Parameters
    ----------
    x_world, y_world : float
        Physics coordinates (metres).
    origin_px : (int, int)
        Pixel location of the world origin.
    scale : float
        Pixels per metre.
    invert_y : bool
        If True (default), negate y so that upward physics = downward screen.

    Returns
    -------
    (int, int)
        Pixel ``(col, row)``.
    """
    ox, oy = origin_px
    px = int(ox + x_world * scale)
    py = int(oy + (-y_world if invert_y else y_world) * scale)
    return (px, py)