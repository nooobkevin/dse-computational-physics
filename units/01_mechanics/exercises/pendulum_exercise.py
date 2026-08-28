"""Pendulum simulation — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of a simple pendulum by overriding
the ``angular_acceleration`` method in ``StudentPendulum``.

The base class :class:`physics_core.mechanics.pendulum.PendulumSim` provides
everything else: the integration loop (``step``), the ``state`` property,
``position()``, ``energy()``, and ``period_from_formula``.  You only need to
supply the equation of motion.

Physics background
------------------
For a simple pendulum of length *L* under gravity *g*:

    torque = - m g L sin(θ)      (restoring torque)
    I = m L²                     (moment of inertia of point mass)
    α = torque / I = -(g/L) sin(θ)

So the angular acceleration is:

    d²θ/dt² = -(g / L) * sin(θ)

For small angles (θ ≪ 1 rad) you may use the approximation sin(θ) ≈ θ,
giving the simple harmonic form:

    d²θ/dt² ≈ -(g / L) * θ

Your implementation should use the **full non-linear** expression
``-(g/L) * sin(θ)`` so that the simulation is accurate even for larger
amplitudes.

Units
-----
- theta (θ) : radians
- omega (ω) : rad/s
- return value : rad/s²

Period formula (small-angle)
----------------------------
    T = 2π √(L / g)

This is available as ``sim.period_from_formula``.

What to do
----------
1. Read the docstring and signature of ``angular_acceleration`` below.
2. Replace the ``raise NotImplementedError`` line with the correct physics.
3. Run the auto-grader to check your work:

       uv run pytest units/01_mechanics/exercises/test_exercise.py -v

   The grader measures the **numerical behaviour** of your simulation
   (period, energy conservation, stability) — it does *not* read your
   source code, so any correct implementation will pass.
"""

from __future__ import annotations

import math

from physics_core.mechanics.pendulum import PendulumSim


class StudentPendulum(PendulumSim):
    """Student implementation of the simple pendulum.

    Override :meth:`angular_acceleration` with the correct physics.
    Everything else is inherited from :class:`PendulumSim`.

    Example
    -------
    >>> sim = StudentPendulum(length=1.0, g=9.81, theta0=0.1, dt=0.01)
    >>> for _ in range(1000):
    ...     sim.step()
    >>> print(sim.state["theta"])
    """

    def angular_acceleration(self, theta: float, omega: float) -> float:
        """Compute the angular acceleration of the pendulum.

        Parameters
        ----------
        theta : float
            Current angular displacement from vertical (rad).
        omega : float
            Current angular velocity (rad/s).

        Returns
        -------
        float
            Angular acceleration d²θ/dt² (rad/s²).

        Physics (fill this in)
        ----------------------
        Replace the line below with:

            return -(self.g / self.length) * math.sin(theta)

        (The attributes ``self.g`` and ``self.length`` are set by the
        base-class constructor.)
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement angular_acceleration(self, theta, omega) "
            "in StudentPendulum.  See the docstring for the correct formula."
        )