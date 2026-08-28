"""Data-analysis engine for scientific inquiry.

Architecture
------------
:class:`LinearFit` is the **abstract base** that follows the same pattern as
the simulation engines in ``physics_core.mechanics``, ``physics_core.thermal``,
etc.  It defines framework methods (``step``, ``state``, ``position``,
``energy``) for API compatibility, and one physics **hook**:

    ``model(self, x: float) -> float``

that raises ``NotImplementedError`` by default.  Subclasses override the hook
to supply the model function — students fill it in, while
:class:`ReferenceLinearFit` provides the correct least-squares linear
regression.

Unlike the simulation engines, this is an **analysis** engine: it does not
simulate a physical process over time.  Instead it fits a model to data.
The ``step(dt)`` method is a no-op (for duck-type compatibility with the
simulation engines), and ``state`` returns the fit parameters.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple

import numpy as np


class LinearFit:
    """Abstract base for linear (or linearised) data analysis.

    Parameters
    ----------
    x_data : np.ndarray
        Independent-variable data (1-D).
    y_data : np.ndarray
        Dependent-variable data (1-D).
    model : str
        Model type.  Default ``'linear'``.  Subclasses may support other
        models (e.g. ``'quadratic'``, ``'power'``).
    """

    def __init__(
        self,
        x_data: np.ndarray,
        y_data: np.ndarray,
        model_type: str = "linear",
    ) -> None:
        self.x_data = np.asarray(x_data, dtype=float)
        self.y_data = np.asarray(y_data, dtype=float)
        self.model_type = model_type

        if self.x_data.shape != self.y_data.shape:
            raise ValueError(
                f"x_data and y_data must have the same shape, "
                f"got {self.x_data.shape} vs {self.y_data.shape}"
            )
        if len(self.x_data) < 2:
            raise ValueError(
                f"Need at least 2 data points, got {len(self.x_data)}"
            )

        # Fit results (populated by _fit())
        self._slope: float = 0.0
        self._intercept: float = 0.0
        self._r_squared: float = 0.0
        self._residuals_arr: np.ndarray = np.array([])
        self._fitted: bool = False

    # ------------------------------------------------------------------
    # Physics hook — subclasses MUST override
    # ------------------------------------------------------------------
    def model(self, x: float) -> float:
        """Evaluate the model function at *x*.

        Override this in subclasses to supply the physics.

        Parameters
        ----------
        x : float
            Independent variable value.

        Returns
        -------
        float
            Model prediction at *x*.
        """
        raise NotImplementedError(
            "Subclasses must implement model(self, x)"
        )

    # ------------------------------------------------------------------
    # Framework methods (fully implemented)
    # ------------------------------------------------------------------
    def step(self, dt: float | None = None) -> None:
        """Advance the analysis by one step.

        For the analysis engine this is a no-op (the fit is computed once
        in ``__init__``).  The method exists for duck-type compatibility
        with the simulation engines.
        """
        return

    @property
    def state(self) -> Dict[str, float]:
        """Current analysis state (fit parameters).

        Returns
        -------
        dict
            ``{"slope": ..., "intercept": ..., "r_squared": ...}``
        """
        return {
            "slope": self._slope,
            "intercept": self._intercept,
            "r_squared": self._r_squared,
        }

    def position(self) -> Tuple[np.ndarray, np.ndarray]:
        """Return the fitted line as ``(x_fit, y_fit)`` arrays.

        The x values span the range of the input data; the y values are
        the model evaluated at those x values.
        """
        x_min, x_max = float(self.x_data.min()), float(self.x_data.max())
        x_fit = np.linspace(x_min, x_max, 200)
        y_fit = np.array([self.model(x) for x in x_fit])
        return (x_fit, y_fit)

    def energy(self) -> Dict[str, float]:
        """Return goodness-of-fit metrics.

        Returns
        -------
        dict
            ``{"r_squared": ..., "residual_sum_squares": ...}``
        """
        return {
            "r_squared": self._r_squared,
            "residual_sum_squares": float(np.sum(self._residuals_arr**2)),
        }

    # ------------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------------
    def slope(self) -> float:
        """Return the fitted slope."""
        return self._slope

    def intercept(self) -> float:
        """Return the fitted intercept."""
        return self._intercept

    def correlation_squared(self) -> float:
        """Return the coefficient of determination (R²)."""
        return self._r_squared

    def residuals(self) -> np.ndarray:
        """Return the residuals ``y_data - model(x_data)``."""
        return self._residuals_arr.copy()


class ReferenceLinearFit(LinearFit):
    """Reference linear least-squares fit.

    Performs ordinary least-squares linear regression using the standard
    formulas (numpy ``polyfit`` under the hood).  The ``model`` hook is
    implemented as ``slope * x + intercept``.

    Parameters
    ----------
    x_data : np.ndarray
        Independent-variable data (1-D).
    y_data : np.ndarray
        Dependent-variable data (1-D).
    model : str
        Model type (default ``'linear'``).  Currently only ``'linear'``
        is supported.
    """

    def __init__(
        self,
        x_data: np.ndarray,
        y_data: np.ndarray,
        model_type: str = "linear",
    ) -> None:
        super().__init__(x_data, y_data, model_type)
        self._fit()

    def _fit(self) -> None:
        """Perform the least-squares linear fit."""
        if self.model_type == "linear":
            coeffs = np.polyfit(self.x_data, self.y_data, 1)
            self._slope = float(coeffs[0])
            self._intercept = float(coeffs[1])
        else:
            raise ValueError(f"Unsupported model_type: {self.model_type!r}")

        # Compute R²
        y_pred = self._slope * self.x_data + self._intercept
        self._residuals_arr = self.y_data - y_pred
        ss_res = np.sum(self._residuals_arr**2)
        ss_tot = np.sum((self.y_data - np.mean(self.y_data))**2)
        if ss_tot == 0.0:
            self._r_squared = 1.0  # perfect fit (all data points identical)
        else:
            self._r_squared = 1.0 - ss_res / ss_tot

    def model(self, x: float) -> float:
        """Evaluate the linear model ``slope * x + intercept``."""
        return self._slope * x + self._intercept


# ---------------------------------------------------------------------------
# Standalone helpers
# ---------------------------------------------------------------------------


def propagate_uncertainty(
    slope: float,
    intercept: float,
    x_data: np.ndarray,
    y_data: np.ndarray,
) -> Tuple[float, float]:
    """Propagate uncertainty to estimate errors in slope and intercept.

    Uses the standard formulas for ordinary least-squares linear regression:

        n = number of data points
        s² = Σ (y_i - ŷ_i)² / (n - 2)   (variance of residuals)
        Δ = n Σ x_i² - (Σ x_i)²

        σ_m = s * √(n / Δ)              (uncertainty in slope)
        σ_c = s * √(Σ x_i² / Δ)         (uncertainty in intercept)

    Parameters
    ----------
    slope : float
        Fitted slope.
    intercept : float
        Fitted intercept (unused in calculation, kept for API symmetry).
    x_data : np.ndarray
        Independent-variable data.
    y_data : np.ndarray
        Dependent-variable data.

    Returns
    -------
    tuple
        ``(slope_uncertainty, intercept_uncertainty)``
    """
    n = len(x_data)
    if n < 3:
        raise ValueError(
            f"Need at least 3 data points for uncertainty propagation, "
            f"got {n}"
        )

    y_pred = slope * x_data + intercept
    residuals = y_data - y_pred
    s_sq = np.sum(residuals**2) / (n - 2)

    sum_x = np.sum(x_data)
    sum_x_sq = np.sum(x_data**2)
    delta = n * sum_x_sq - sum_x**2

    if delta <= 0:
        raise ValueError(
            "Delta (n Σx² - (Σx)²) is non-positive — data points may be "
            "collinear or identical"
        )

    slope_err = math.sqrt(s_sq * n / delta)
    intercept_err = math.sqrt(s_sq * sum_x_sq / delta)

    return (slope_err, intercept_err)


def percent_error(estimated: float, accepted: float) -> float:
    """Compute the percent error of an estimated value vs an accepted value.

    Parameters
    ----------
    estimated : float
        The measured or estimated value.
    accepted : float
        The accepted (true) value.

    Returns
    -------
    float
        Percent error = ``|estimated - accepted| / |accepted| * 100``.

    Raises
    ------
    ZeroDivisionError
        If *accepted* is zero.
    """
    if accepted == 0.0:
        raise ZeroDivisionError("percent_error: accepted value is zero")
    return abs(estimated - accepted) / abs(accepted) * 100.0