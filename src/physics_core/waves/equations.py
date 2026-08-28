"""Wave equation helpers for the HKDSE Physics toolkit.

Provides utility functions for wave-related physics calculations:
dispersion relations, wave speed, intensity, Young's double-slit,
and diffraction grating equations.
"""

from __future__ import annotations

import math


def wave_speed(frequency: float, wavelength: float) -> float:
    """Compute wave speed from frequency and wavelength: v = f λ.

    Parameters
    ----------
    frequency : float
        Wave frequency (Hz).
    wavelength : float
        Wavelength (m).

    Returns
    -------
    float
        Wave speed (m/s).
    """
    return frequency * wavelength


def angular_frequency(frequency: float) -> float:
    """Convert frequency to angular frequency: ω = 2πf.

    Parameters
    ----------
    frequency : float
        Frequency (Hz).

    Returns
    -------
    float
        Angular frequency (rad/s).
    """
    return 2.0 * math.pi * frequency


def wave_number(wavelength: float) -> float:
    """Compute wave number: k = 2π / λ.

    Parameters
    ----------
    wavelength : float
        Wavelength (m).

    Returns
    -------
    float
        Wave number (rad/m).
    """
    return 2.0 * math.pi / wavelength


def intensity(amplitude: float) -> float:
    """Wave intensity proportional to amplitude squared: I ∝ A².

    Parameters
    ----------
    amplitude : float
        Wave amplitude (m).

    Returns
    -------
    float
        Relative intensity (arbitrary units).
    """
    return amplitude**2


def intensity_inverse_square(distance: float, reference_intensity: float = 1.0) -> float:
    """Intensity at a distance from a point source: I ∝ 1/r².

    Parameters
    ----------
    distance : float
        Distance from the source (m).  Must be > 0.
    reference_intensity : float
        Intensity at unit distance (default 1.0).

    Returns
    -------
    float
        Intensity at the given distance.
    """
    if distance <= 0.0:
        raise ValueError(f"distance must be > 0, got {distance}")
    return reference_intensity / (distance**2)


def young_slit_dsin(
    slit_separation: float, angle: float, order: int = 1
) -> float:
    """Young's double-slit condition: d sin(θ) = n λ.

    Given slit separation *d*, angle *θ*, and order *n*, returns the
    wavelength λ that produces a bright fringe at that angle.

    Parameters
    ----------
    slit_separation : float
        Distance between the two slits (m).
    angle : float
        Angle from the central axis (rad).
    order : int
        Fringe order n (default 1).

    Returns
    -------
    float
        Wavelength λ (m).
    """
    return slit_separation * math.sin(angle) / order


def young_slit_angle(
    wavelength: float, slit_separation: float, order: int = 1
) -> float:
    """Young's double-slit: angle for the n-th bright fringe.

    Given wavelength λ, slit separation *d*, and order *n*,
    returns the angle θ for a bright fringe: sin(θ) = n λ / d.

    Parameters
    ----------
    wavelength : float
        Wavelength (m).
    slit_separation : float
        Distance between the two slits (m).
    order : int
        Fringe order n (default 1).

    Returns
    -------
    float
        Angle θ (rad).
    """
    ratio = order * wavelength / slit_separation
    if ratio > 1.0:
        raise ValueError(
            f"order * wavelength / d = {ratio} > 1 — no solution for this order"
        )
    return math.asin(ratio)


def diffraction_grating_angle(
    wavelength: float, grating_spacing: float, order: int = 1
) -> float:
    """Diffraction grating: angle for the n-th order maximum.

    Given wavelength λ, grating spacing *d*, and order *n*,
    returns the angle θ: d sin(θ) = n λ.

    Parameters
    ----------
    wavelength : float
        Wavelength (m).
    grating_spacing : float
        Distance between adjacent grating lines (m).
    order : int
        Diffraction order n (default 1).

    Returns
    -------
    float
        Angle θ (rad).
    """
    return young_slit_angle(wavelength, grating_spacing, order)
