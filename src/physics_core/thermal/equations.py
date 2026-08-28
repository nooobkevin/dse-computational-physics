"""Maxwell-Boltzmann distribution helpers for kinetic theory.

Provides analytical formulas for the Maxwell-Boltzmann speed distribution
and related quantities (most probable speed, mean speed, RMS speed) in
2D and 3D.

All functions use simulation units where kB = 1.0 by default.
"""

from __future__ import annotations

import math

from physics_core.thermal.gas_sim import KB


def maxwell_boltzmann(
    speed: float, T: float, m: float, kB: float = KB, dim: int = 2
) -> float:
    """Maxwell-Boltzmann speed distribution *f(v)*.

    For 2D (dim=2):
        f(v) = (m / kB*T) * v * exp(-m*v² / (2*kB*T))

    For 3D (dim=3):
        f(v) = 4π * (m / (2π*kB*T))^(3/2) * v² * exp(-m*v² / (2*kB*T))

    Parameters
    ----------
    speed : float
        Speed *v* (must be >= 0).
    T : float
        Temperature.
    m : float
        Particle mass.
    kB : float
        Boltzmann constant.  Default 1.0 (simulation units).
    dim : int
        Number of spatial dimensions (2 or 3).  Default 2.

    Returns
    -------
    float
        Probability density *f(v)*.
    """
    if speed < 0.0:
        return 0.0
    if T <= 0.0:
        return 0.0

    beta = m / (kB * T)
    exp_factor = math.exp(-0.5 * beta * speed * speed)

    if dim == 2:
        return beta * speed * exp_factor
    elif dim == 3:
        prefactor = 4.0 * math.pi * (beta / (2.0 * math.pi)) ** 1.5
        return prefactor * speed * speed * exp_factor
    else:
        raise ValueError(f"Unsupported dimension: {dim}")


def most_probable_speed(
    T: float, m: float, kB: float = KB, dim: int = 2
) -> float:
    """Most probable speed *v_p*.

    For 2D: v_p = sqrt(kB*T / m)
    For 3D: v_p = sqrt(2*kB*T / m)

    Parameters
    ----------
    T : float
        Temperature.
    m : float
        Particle mass.
    kB : float
        Boltzmann constant.  Default 1.0.
    dim : int
        Number of dimensions (2 or 3).  Default 2.

    Returns
    -------
    float
        Most probable speed.
    """
    if dim == 2:
        return math.sqrt(kB * T / m)
    elif dim == 3:
        return math.sqrt(2.0 * kB * T / m)
    else:
        raise ValueError(f"Unsupported dimension: {dim}")


def mean_speed(T: float, m: float, kB: float = KB, dim: int = 2) -> float:
    """Mean (average) speed *<v>*.

    For 2D: <v> = sqrt(π*kB*T / (2*m))
    For 3D: <v> = sqrt(8*kB*T / (π*m))

    Parameters
    ----------
    T : float
        Temperature.
    m : float
        Particle mass.
    kB : float
        Boltzmann constant.  Default 1.0.
    dim : int
        Number of dimensions (2 or 3).  Default 2.

    Returns
    -------
    float
        Mean speed.
    """
    if dim == 2:
        return math.sqrt(math.pi * kB * T / (2.0 * m))
    elif dim == 3:
        return math.sqrt(8.0 * kB * T / (math.pi * m))
    else:
        raise ValueError(f"Unsupported dimension: {dim}")


def rms_speed(T: float, m: float, kB: float = KB, dim: int = 2) -> float:
    """Root-mean-square speed *v_rms*.

    For 2D: v_rms = sqrt(2*kB*T / m)
    For 3D: v_rms = sqrt(3*kB*T / m)

    Parameters
    ----------
    T : float
        Temperature.
    m : float
        Particle mass.
    kB : float
        Boltzmann constant.  Default 1.0.
    dim : int
        Number of dimensions (2 or 3).  Default 2.

    Returns
    -------
    float
        RMS speed.
    """
    if dim == 2:
        return math.sqrt(2.0 * kB * T / m)
    elif dim == 3:
        return math.sqrt(3.0 * kB * T / m)
    else:
        raise ValueError(f"Unsupported dimension: {dim}")