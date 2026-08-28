"""Kinematics (SUVAT) — student fill-in-the-blank exercise.

Task
----
Your job is to implement the SUVAT equations of uniformly accelerated
motion in the ``StudentKinematics`` class.  The base class provides
the framework; you fill in the physics hooks.

SUVAT equations (for constant acceleration a):
    v = u + at
    s = ½(u+v)t
    s = ut + ½at²
    v² = u² + 2as

Where:
    u = initial velocity (m/s)
    v = final velocity (m/s)
    a = acceleration (m/s²)
    t = time (s)
    s = displacement (m)

What to do
----------
1. Read the docstrings of each method below.
2. Replace each ``raise NotImplementedError`` line with the correct
   SUVAT formula using the class attributes ``self.u``, ``self.a``.
3. Run the auto-grader to check your work:

       uv run pytest units/01_mechanics/exercises/test_kinematics_exercise.py -v

CAF reference: Curriculum item b (Kinematics), equations of uniformly
accelerated motion; s–t, v–t, a–t graph interpretation.
"""

from __future__ import annotations

import math


class StudentKinematics:
    """Student implementation of SUVAT kinematics.

    The attributes ``self.u`` (initial velocity, m/s) and
    ``self.a`` (acceleration, m/s²) are set by the constructor.

    Parameters
    ----------
    u : float
        Initial velocity (m/s).
    a : float
        Constant acceleration (m/s²).
    """

    def __init__(self, u: float = 0.0, a: float = 9.81) -> None:
        self.u = u
        self.a = a

    def velocity_after(self, t: float) -> float:
        """Compute velocity after time *t*: ``v = u + at``.

        Parameters
        ----------
        t : float
            Time elapsed (s).

        Returns
        -------
        float
            Velocity at time *t* (m/s).

        Physics
        -------
        Replace the line below with::

            return self.u + self.a * t
        """
        raise NotImplementedError(
            "You must implement velocity_after(self, t).  "
            "Use the formula v = u + at."
        )

    def displacement(self, t: float) -> float:
        """Compute displacement after time *t*: ``s = ut + ½at²``.

        Parameters
        ----------
        t : float
            Time elapsed (s).

        Returns
        -------
        float
            Displacement at time *t* (m).

        Physics
        -------
        Replace the line below with::

            return self.u * t + 0.5 * self.a * t * t
        """
        raise NotImplementedError(
            "You must implement displacement(self, t).  "
            "Use the formula s = ut + ½at²."
        )

    def displacement_from_uv(self, v: float, t: float) -> float:
        """Compute displacement from initial and final velocity:
        ``s = ½(u+v)t``.

        Parameters
        ----------
        v : float
            Final velocity (m/s).
        t : float
            Time elapsed (s).

        Returns
        -------
        float
            Displacement (m).

        Physics
        -------
        Replace the line below with::

            return 0.5 * (self.u + v) * t
        """
        raise NotImplementedError(
            "You must implement displacement_from_uv(self, v, t).  "
            "Use the formula s = ½(u+v)t."
        )

    def final_velocity_sq(self, s: float) -> float:
        """Compute squared final velocity from displacement:
        ``v² = u² + 2as``.

        Parameters
        ----------
        s : float
            Displacement (m).

        Returns
        -------
        float
            Square of final velocity (m²/s²).

        Physics
        -------
        Replace the line below with::

            return self.u * self.u + 2.0 * self.a * s
        """
        raise NotImplementedError(
            "You must implement final_velocity_sq(self, s).  "
            "Use the formula v² = u² + 2as."
        )

    def acceleration_from_graph(
        self, v1: float, v2: float, t1: float, t2: float
    ) -> float:
        """Estimate acceleration from a v–t graph segment:
        ``a = (v2 - v1) / (t2 - t1)``.

        Parameters
        ----------
        v1 : float
            Velocity at time *t1* (m/s).
        v2 : float
            Velocity at time *t2* (m/s).
        t1 : float
            Start time (s).
        t2 : float
            End time (s).

        Returns
        -------
        float
            Acceleration (m/s²).

        Physics
        -------
        Replace the line below with::

            return (v2 - v1) / (t2 - t1)
        """
        raise NotImplementedError(
            "You must implement acceleration_from_graph(self, v1, v2, t1, t2).  "
            "Use the formula a = Δv / Δt."
        )