"""Physics & Engineering simulation — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of total internal reflection in
an optical fibre by overriding the hooks in ``StudentOpticalFibre``.

The base class (:class:`OpticalFibre`) provides everything else: the
``step`` method, properties like ``state``, ``position``, ``energy``,
and ``acceptance_condition``.  You only need to supply the physics.

---

## Physics background

For an optical fibre with core index *n₁* and cladding index *n₂* (n₁ > n₂),
total internal reflection (TIR) occurs when the ray angle *θ* exceeds the
critical angle:

    θ_c = arcsin(n₂ / n₁)

When θ > θ_c, the ray undergoes TIR and stays inside the core.
When θ < θ_c, the ray leaks out through the cladding.

The refractive index of a medium is related to the speed of light in that
medium: n = c / v, where c is the speed of light in vacuum and v is the
speed in the medium.

Constants
---------
``self.n1`` — core refractive index
``self.n2`` — cladding refractive index
``self.length`` — fibre length (m)
``self.angle`` — ray incidence angle (rad)

What to do
----------
1. Read the docstring of ``total_internal_reflection(self, angle)``.
2. Replace the ``raise NotImplementedError`` line with the correct physics.
3. Implement the ``critical_angle`` property.
4. Run the auto-grader to check your work:

       uv run pytest units/05_engineering/exercises/test_exercise.py -v
"""

from __future__ import annotations

import math
from typing import Any, Dict, Tuple

from physics_core.engineering.optics import OpticalFibre


class StudentOpticalFibre(OpticalFibre):
    """Student implementation of optical fibre TIR.

    Override :meth:`total_internal_reflection` and the
    :attr:`critical_angle` property with the correct physics.
    Everything else is inherited from :class:`OpticalFibre`.

    Physics (fill this in):
        critical_angle:
            return math.asin(self.n2 / self.n1)

        total_internal_reflection(angle):
            return angle > self.critical_angle
    """

    @property
    def critical_angle(self) -> float:
        """Critical angle for TIR: θ_c = arcsin(n₂ / n₁).

        Replace NotImplementedError with the correct formula.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement critical_angle in StudentOpticalFibre. "
            "See the docstring for the correct formula."
        )

    def total_internal_reflection(self, angle: float) -> bool:
        """Determine whether a ray at *angle* undergoes TIR.

        Replace NotImplementedError with the correct physics.

        Parameters
        ----------
        angle : float
            Incidence angle (rad).

        Returns
        -------
        bool
            True if the ray undergoes total internal reflection.
        """
        # TODO: Replace this NotImplementedError with the correct physics.
        raise NotImplementedError(
            "You must implement total_internal_reflection(self, angle) "
            "in StudentOpticalFibre.  See the docstring for the correct logic."
        )