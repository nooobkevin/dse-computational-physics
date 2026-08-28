"""Data Analysis — student fill-in-the-blank exercise.

Task
----
You are given a noisy dataset of pendulum measurements.  Your job is to:

1. Convert units (if needed) so they are in SI base units.
2. Identify and remove outliers using the IQR method.
3. Fit a line to the cleaned data (T² vs L).
4. Estimate the gravitational acceleration g from the slope.
5. Compute the percent uncertainty.

The dataset is hard-coded in this file — no CSV import needed.

Physics background
------------------
T = 2π √(L/g)  →  T² = (4π²/g) × L

The slope of T² vs L is 4π²/g, so g = 4π² / slope.
"""

from __future__ import annotations

import math
from typing import Optional, Tuple

import numpy as np

from physics_core.inquiry.analysis import ReferenceLinearFit, percent_error


# ── Dataset ──────────────────────────────────────────────────────────────────
# Pendulum data: L in cm, T in seconds (one trial per length)
# NOTE: L is in CENTIMETRES — you need to convert to metres!

L_cm: np.ndarray = np.array([
    20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0,
])
T_s: np.ndarray = np.array([
    0.92, 1.12, 1.28, 1.43, 1.56, 1.69, 1.80, 1.98, 2.01, 2.12,
])
# Note: measurement at L=90 cm (T=1.98 s) is suspicious — check if it's an outlier.


# ── Student hooks ────────────────────────────────────────────────────────────


def to_si(L_cm: np.ndarray) -> np.ndarray:
    """Convert lengths from centimetres to metres.

    Parameters
    ----------
    L_cm : np.ndarray
        Pendulum lengths in centimetres.

    Returns
    -------
    np.ndarray
        Pendulum lengths in metres.
    """
    # TODO: Replace the NotImplementedError below.
    raise NotImplementedError(
        "You must implement to_si().  Convert cm to m: L_m = L_cm / 100."
    )


def remove_outliers(
    L_m: np.ndarray, T_s: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """Remove outlier data points using the IQR method on T_s.

    A point is an outlier if T_s is below Q1 - 1.5×IQR or above Q3 + 1.5×IQR.

    Parameters
    ----------
    L_m : np.ndarray
        Pendulum lengths in metres.
    T_s : np.ndarray
        Measured periods in seconds.

    Returns
    -------
    tuple
        ``(L_clean, T_clean)`` — data with outliers removed.
    """
    # TODO: Replace the NotImplementedError below.
    raise NotImplementedError(
        "You must implement remove_outliers().  "
        "Use np.percentile to compute Q1, Q3, IQR, then filter."
    )


def fit_slope(T_s: np.ndarray, L_m: np.ndarray) -> float:
    """Fit T² vs L and return the slope.

    Parameters
    ----------
    T_s : np.ndarray
        Measured periods (s).
    L_m : np.ndarray
        Pendulum lengths (m).

    Returns
    -------
    float
        Slope of T² vs L (s²/m).
    """
    # TODO: Replace the NotImplementedError below.
    raise NotImplementedError(
        "You must implement fit_slope().  "
        "Compute T² = T_s**2, then use ReferenceLinearFit."
    )


def estimate_g(slope: float) -> float:
    """Estimate g from the slope of T² vs L.

    Parameters
    ----------
    slope : float
        Slope of T² vs L (s²/m).

    Returns
    -------
    float
        Estimated gravitational acceleration (m/s²).
    """
    # TODO: Replace the NotImplementedError below.
    raise NotImplementedError(
        "You must implement estimate_g().  "
        "g = 4π² / slope."
    )


def percent_uncertainty(g_est: float, g_accepted: float = 9.81) -> float:
    """Compute the percent error of the estimated g.

    Parameters
    ----------
    g_est : float
        Estimated gravitational acceleration (m/s²).
    g_accepted : float
        Accepted gravitational acceleration (m/s²).

    Returns
    -------
    float
        Percent error.
    """
    # TODO: Replace the NotImplementedError below.
    raise NotImplementedError(
        "You must implement percent_uncertainty().  "
        "Use physics_core.inquiry.analysis.percent_error."
    )


# ── Questions ────────────────────────────────────────────────────────────────

QUESTIONS = """
Data Analysis Exercise — Questions

1. Why is it necessary to convert L from cm to m before fitting?  What
   would happen to the slope value if you forgot to convert?

2. The measurement at L = 90 cm (T = 1.98 s) — was it flagged as an outlier?
   Explain why or why not, in terms of the IQR.

3. What physical constant does the slope of T² vs L represent?
   Show the derivation.

4. How does removing the outlier change g_est?  Is the change significant?

5. Using percent_uncertainty, is your estimated g within 5% of the accepted
   value?  What does this tell you about the accuracy of the measurements?
"""