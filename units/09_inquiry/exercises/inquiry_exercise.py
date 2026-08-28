"""Scientific inquiry — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **data analysis** for a physics experiment by
overriding the ``model`` method in ``StudentLinearFit``.

The base class :class:`physics_core.inquiry.analysis.LinearFit` provides
everything else: the data storage, the ``step`` method, the ``state``
property, ``position()``, and ``energy()``.  You only need to supply the
model function.

Physics background
------------------
You are given a set of (x, y) data points from a physics experiment.
Your task is to fit a linear model to the data:

    y = m * x + c

where *m* is the slope and *c* is the intercept.

The data has already been **linearised** — that is, the variables have been
chosen so that the relationship is a straight line.  For example:

- Pendulum experiment: T² vs L gives a straight line with slope 4π²/g
- Free-fall experiment: s vs t² gives a straight line with slope ½g

Your job is to implement ``model(self, x)`` to return ``m * x + c``,
where ``m`` and ``c`` are the slope and intercept you compute from the data.

What to do
----------
1. Read the docstring and signature of ``model`` below.
2. Replace the ``raise NotImplementedError`` line with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/09_inquiry/exercises/test_exercise.py -v

   The grader measures the **numerical behaviour** of your analysis
   (slope, intercept, R², percent error) — it does *not* read your
   source code, so any correct implementation will pass.

Hints
-----
- The slope and intercept should be stored as ``self._slope`` and
  ``self._intercept`` (set in ``__init__`` or in a ``_fit()`` method).
- Use numpy's ``np.polyfit(x_data, y_data, 1)`` for the least-squares fit.
- The model function should return ``self._slope * x + self._intercept``.
"""

from __future__ import annotations

import numpy as np

from physics_core.inquiry.analysis import LinearFit


class StudentLinearFit(LinearFit):
    """Student implementation of linear data analysis.

    Override :meth:`model` with the correct physics.
    Everything else is inherited from :class:`LinearFit`.

    Example
    -------
    >>> x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    >>> y = 2.0 * x + 1.0
    >>> fit = StudentLinearFit(x_data=x, y_data=y)
    >>> print(fit.slope(), fit.intercept())
    """

    def __init__(
        self,
        x_data: np.ndarray,
        y_data: np.ndarray,
        model_type: str = "linear",
    ) -> None:
        super().__init__(x_data, y_data, model_type)
        # TODO: Perform the least-squares fit here.
        # Store the results in self._slope and self._intercept.
        # raise NotImplementedError(
        #     "You must implement the fit in StudentLinearFit.__init__"
        # )

    def model(self, x: float) -> float:
        """Evaluate the linear model at *x*.

        Parameters
        ----------
        x : float
            Independent variable value.

        Returns
        -------
        float
            Model prediction ``slope * x + intercept``.

        Physics (fill this in)
        ----------------------
        Replace the line below with:

            return self._slope * x + self._intercept

        (The attributes ``self._slope`` and ``self._intercept`` should be
        set in ``__init__`` by performing a least-squares fit.)
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement model(self, x) in StudentLinearFit.  "
            "See the docstring for the correct formula."
        )