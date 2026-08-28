"""Physics error / uncertainty helpers.

Provides routines for computing and formatting measurement errors and for
rounding values to a specified number of significant figures.
"""

from __future__ import annotations

import math


def absolute_error(measured: float, true: float) -> float:
    """Absolute error ``|measured - true|``."""
    return abs(measured - true)


def relative_error(measured: float, true: float) -> float:
    """Relative error ``|measured - true| / |true|``.

    Raises ZeroDivisionError if *true* is zero.
    """
    if true == 0.0:
        raise ZeroDivisionError("relative_error: true value is zero")
    return abs(measured - true) / abs(true)


def percent_error(measured: float, true: float) -> float:
    """Percent error = relative error × 100.

    Raises ZeroDivisionError if *true* is zero.
    """
    return relative_error(measured, true) * 100.0


def sig_figs(x: float, n: int) -> float:
    """Round *x* to *n* significant figures.

    Parameters
    ----------
    x : float
        Value to round.
    n : int
        Number of significant figures (must be >= 1).

    Returns
    -------
    float
        Rounded value.
    """
    if n < 1:
        raise ValueError(f"sig_figs: n must be >= 1, got {n}")
    if x == 0.0:
        return 0.0
    # Order-of-magnitude of x
    magnitude = int(math.floor(math.log10(abs(x))))
    scale = 10.0 ** (n - 1 - magnitude)
    return round(x * scale) / scale


def format_value_with_error(value: float, err: float) -> str:
    """Format ``value ± err`` with the error rounded to one significant figure.

    The value is rounded to the same decimal place as the error.

    Parameters
    ----------
    value : float
        Measured value.
    err : float
        Uncertainty (must be > 0).

    Returns
    -------
    str
        Formatted string, e.g. ``"1.23 ± 0.05"``.
    """
    if err <= 0:
        raise ValueError(f"format_value_with_error: err must be > 0, got {err}")

    # Round error to 1 significant figure
    err_rounded = sig_figs(err, 1)

    # Determine decimal places from the rounded error
    if err_rounded >= 1.0:
        decimals = 0
    else:
        # Number of decimal places to show the first significant digit
        decimals = max(0, -int(math.floor(math.log10(err_rounded))))

    value_rounded = round(value, decimals)
    err_formatted = f"{err_rounded:.{decimals}f}"
    value_formatted = f"{value_rounded:.{decimals}f}"
    return f"{value_formatted} ± {err_formatted}"