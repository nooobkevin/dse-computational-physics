"""Specific heat capacity — data-analysis exercise.

Students are given (Q, delta_T) data pairs for a substance and must
implement functions to determine the specific heat capacity from a
linear fit, compute the energy required to heat a substance, and
compute the final temperature after adding heat.

Data-analysis background
------------------------
The heat capacity C of a substance is defined as:

    C = Q / delta_T

where Q is the heat added and delta_T is the temperature change.
The specific heat capacity c (per unit mass) is:

    c = C / m = Q / (m * delta_T)

When we have multiple (Q, delta_T) data points, the heat capacity C
is the slope of the best-fit line Q = C * delta_T (through the origin,
since Q = 0 should give delta_T = 0).

All temperatures are assumed to be in Kelvin.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np


def specific_heat_from_fit(
    Q_data: np.ndarray, delta_T_data: np.ndarray, mass: float
) -> Tuple[float, float, float]:
    """Determine specific heat capacity from (Q, delta_T) data.

    Fits a line Q = C * delta_T (through the origin) to the data
    to find the heat capacity C, then computes c = C / m.

    Parameters
    ----------
    Q_data : ndarray, shape (n,)
        Heat added (J).
    delta_T_data : ndarray, shape (n,)
        Temperature change (K).
    mass : float
        Mass of the substance (kg).

    Returns
    -------
    C : float
        Heat capacity (J/K).
    c : float
        Specific heat capacity (J/(kg·K)).
    slope_err : float
        Standard error of the slope.
    """
    # TODO: Replace NotImplementedError with the correct computation.
    raise NotImplementedError(
        "Implement specific_heat_from_fit. "
        "Fit Q = C * delta_T through the origin."
    )


def energy_to_heat(mass: float, c: float, delta_T: float) -> float:
    """Compute the energy required to heat a substance.

    Q = m * c * delta_T

    Parameters
    ----------
    mass : float
        Mass (kg).
    c : float
        Specific heat capacity (J/(kg·K)).
    delta_T : float
        Temperature change (K).

    Returns
    -------
    float
        Heat energy (J).
    """
    # TODO: Replace NotImplementedError with the correct formula.
    raise NotImplementedError(
        "Implement energy_to_heat. "
        "Use Q = m * c * delta_T."
    )


def final_temperature(
    Q: float, mass: float, c: float, T_initial: float
) -> float:
    """Compute the final temperature after adding heat Q.

    delta_T = Q / (m * c), so T_final = T_initial + Q / (m * c).

    Parameters
    ----------
    Q : float
        Heat added (J).
    mass : float
        Mass (kg).
    c : float
        Specific heat capacity (J/(kg·K)).
    T_initial : float
        Initial temperature (K).

    Returns
    -------
    float
        Final temperature (K).
    """
    # TODO: Replace NotImplementedError with the correct computation.
    raise NotImplementedError(
        "Implement final_temperature. "
        "Use T_final = T_initial + Q / (m * c)."
    )