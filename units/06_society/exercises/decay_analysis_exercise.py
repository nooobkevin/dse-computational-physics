"""Decay data analysis exercise — computer-assisted data analysis (CP.5).

Task
----
Given a hard-coded noisy count-rate dataset (simulated GM counter
measurements), implement functions to:

1. ``half_life_from_fit(t, counts)`` — estimate half-life by fitting
   an exponential decay curve (or log-linear slope).
2. ``background_subtracted_rate(counts, background)`` — subtract
   background radiation from measured count rates.
3. ``remaining_fraction(N0, N)`` — compute the fraction of nuclei
   remaining.

This is a **data-analysis** exercise: you are given real-looking
(count rate, time) data and must extract the half-life using
curve-fitting, just as physicists do with experimental data.

Physics background
------------------
Radioactive decay follows N(t) = N₀ · 2^(-t/T), where T is the
half-life.  The count rate (detected decays per second) is proportional
to the number of undecayed nuclei: C(t) = C₀ · 2^(-t/T).

Taking the natural log: ln(C) = ln(C₀) - (ln(2)/T) · t

So a plot of ln(C) vs t gives a straight line with slope -ln(2)/T,
from which we can extract T = -ln(2) / slope.

What to do
----------
1. Read the docstrings of each function below.
2. Replace the ``raise NotImplementedError`` lines with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/06_society/exercises/test_decay_analysis_exercise.py -v
"""

from __future__ import annotations

import math
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Simulated experimental data (count rate vs time)
# ---------------------------------------------------------------------------
# These data simulate GM counter measurements of a radioactive sample
# with background radiation.  Time is in seconds, counts in decays/s.
# The true half-life is approximately 5.0 s.
TIME_POINTS: List[float] = [
    0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0,
    10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0,
]

COUNT_RATES: List[float] = [
    982.0, 812.0, 702.0, 588.0, 502.0, 428.0, 362.0, 310.0,
    268.0, 230.0, 198.0, 172.0, 150.0, 130.0, 114.0, 100.0,
    88.0, 78.0, 68.0, 60.0,
]

BACKGROUND_RATE: float = 20.0  # decays/s (background radiation)


def half_life_from_fit(t: List[float], counts: List[float]) -> float:
    """Estimate half-life from count-rate data using log-linear fit.

    Performs a linear regression on ln(counts) vs t, then extracts
    the half-life from the slope.

    Parameters
    ----------
    t : list[float]
        Time points (s).
    counts : list[float]
        Count rates (decays/s) at each time point.

    Returns
    -------
    float
        Estimated half-life (s).

    Physics (fill this in)
    ----------------------
    1. Take ln of each count rate.
    2. Fit a line ln(C) = m * t + b using least squares:
       m = (n*sum(t*lnC) - sum(t)*sum(lnC)) / (n*sum(t²) - (sum(t))²)
       b = (sum(lnC) - m*sum(t)) / n
    3. Half-life T = -ln(2) / m
    """
    raise NotImplementedError(
        "You must implement half_life_from_fit(t, counts)"
    )


def background_subtracted_rate(counts: List[float], background: float) -> List[float]:
    """Subtract background radiation from measured count rates.

    Parameters
    ----------
    counts : list[float]
        Measured count rates (decays/s).
    background : float
        Background count rate (decays/s).

    Returns
    -------
    list[float]
        Background-subtracted count rates.

    Physics (fill this in)
    ----------------------
    return [max(c - background, 0.0) for c in counts]
    """
    raise NotImplementedError(
        "You must implement background_subtracted_rate(counts, background)"
    )


def remaining_fraction(N0: float, N: float) -> float:
    """Compute the fraction of nuclei remaining.

    Parameters
    ----------
    N0 : float
        Initial number of nuclei.
    N : float
        Current number of nuclei.

    Returns
    -------
    float
        Fraction remaining (N / N0).

    Physics (fill this in)
    ----------------------
    return N / N0
    """
    raise NotImplementedError(
        "You must implement remaining_fraction(N0, N)"
    )