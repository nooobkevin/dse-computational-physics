"""Engineering Design — student fill-in-the-blank exercise.

Task
----
You are designing a pendulum clock.  Your goal is to find the pendulum
length L that produces a period of exactly T = 2.0 seconds.

You are given a set of (L, T_measured) data from a prototype test.
Your job is to:

1. Fit T² vs L to find the slope.
2. Estimate g from the slope (slope = 4π² / g).
3. Compute the recommended L for the target period.
4. Compute the iteration error: how far off is your measured T from
   the target T?

The base class :class:`physics_core.inquiry.analysis.LinearFit` provides
the data storage, and we use :class:`ReferenceLinearFit` for the fit.
You need to implement the analysis functions.

Physics background
------------------
The period of a simple pendulum is: T = 2π √(L/g)
Therefore: T² = (4π²/g) × L  — a straight line through the origin.

If you measure T for several values of L, you can:
1. Compute T²
2. Fit T² vs L → slope = 4π²/g
3. Estimate g = 4π² / slope
4. Recommended L for target T: L = (T_target² × g) / (4π²)
"""

from __future__ import annotations

import math
from typing import Tuple

import numpy as np

from physics_core.inquiry.analysis import ReferenceLinearFit


def fit_slope(T2_data: np.ndarray, L_data: np.ndarray) -> float:
    """Compute the least-squares slope of T² vs L.

    Parameters
    ----------
    T2_data : np.ndarray
        Measured period-squared values (s²).
    L_data : np.ndarray
        Corresponding pendulum lengths (m).

    Returns
    -------
    float
        Slope of the best-fit line (s²/m).

    Physics: slope = 4π² / g
    """
    # TODO: Replace the NotImplementedError below.
    # Hint: Use ReferenceLinearFit(x_data=L_data, y_data=T2_data).slope()
    raise NotImplementedError(
        "You must implement fit_slope().  "
        "Use ReferenceLinearFit to fit T² vs L and return the slope."
    )


def recommended_length(slope: float, T_target: float) -> float:
    """Compute the pendulum length L for a target period T.

    Parameters
    ----------
    slope : float
        Slope of T² vs L (s²/m), equal to 4π²/g.
    T_target : float
        Desired period (s).

    Returns
    -------
    float
        Recommended pendulum length L (m).

    Derivation:
        T² = slope × L  →  L = T² / slope

    When the slope is from a fit to measured data, this gives the
    best estimate of L for the target period.
    """
    # TODO: Replace the NotImplementedError below.
    raise NotImplementedError(
        "You must implement recommended_length().  "
        "Use L = T_target² / slope."
    )


def iteration_error(
    L_guess: float, T_target: float, T_measured: float
) -> float:
    """Compute the percent error between measured T and target T.

    Parameters
    ----------
    L_guess : float
        The pendulum length that was tested (m) — used for display only.
    T_target : float
        The target period (s).
    T_measured : float
        The measured period (s) at the given L.

    Returns
    -------
    float
        Percent error = |T_measured - T_target| / T_target × 100
    """
    # TODO: Replace the NotImplementedError below.
    raise NotImplementedError(
        "You must implement iteration_error().  "
        "Compute |T_measured - T_target| / T_target * 100."
    )