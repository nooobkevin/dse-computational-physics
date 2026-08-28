"""Domestic electricity exercise — student fill-in-the-blank exercise.

Task
----
Your job is to implement the **physics** of domestic electricity by
implementing the hooks in ``StudentPowerRating``.

Physics
-------
- Power: P = V I
- Operating current: I = P / V
- Fuse choice: select the smallest standard fuse rating (3 A, 5 A, 13 A)
  that is greater than the operating current.
- Energy in kWh: E = P t  (where t is in hours)
- Cost: cost = E × rate_per_kWh

What to do
----------
1. Implement ``operating_current(self, power, voltage)``
2. Implement ``fuse_rating(self, current)``
3. Implement ``energy_kwh(self, power_watts, hours)``
4. Implement ``cost(self, energy_kwh, rate_per_kwh)``
5. Run the auto-grader:

       uv run pytest units/05_engineering/exercises/test_power_rating_exercise.py -v
"""

from __future__ import annotations

from typing import List


class StudentPowerRating:
    """Student implementation of domestic electricity calculations."""

    STANDARD_FUSE_RATINGS: List[float] = [3.0, 5.0, 13.0]

    def operating_current(self, power: float, voltage: float) -> float:
        """Compute the operating current I = P / V.

        Parameters
        ----------
        power : float
            Power rating (W).
        voltage : float
            Operating voltage (V).

        Returns
        -------
        float
            Current (A).
        """
        raise NotImplementedError(
            "You must implement operating_current(self, power, voltage). "
            "Use: return power / voltage"
        )

    def fuse_rating(self, current: float) -> float:
        """Select the appropriate fuse rating.

        Choose the smallest standard rating (3, 5, 13 A) that is
        greater than *current*.

        Parameters
        ----------
        current : float
            Operating current (A).

        Returns
        -------
        float
            Fuse rating (A).
        """
        raise NotImplementedError(
            "You must implement fuse_rating(self, current). "
            "Select the smallest standard fuse rating > current."
        )

    def energy_kwh(self, power_watts: float, hours: float) -> float:
        """Compute electrical energy in kWh.

        Parameters
        ----------
        power_watts : float
            Power (W).
        hours : float
            Time (h).

        Returns
        -------
        float
            Energy (kWh).
        """
        raise NotImplementedError(
            "You must implement energy_kwh(self, power_watts, hours). "
            "Use: return power_watts / 1000.0 * hours"
        )

    def cost(self, energy_kwh: float, rate_per_kwh: float) -> float:
        """Compute the cost of running an appliance.

        Parameters
        ----------
        energy_kwh : float
            Energy consumed (kWh).
        rate_per_kwh : float
            Electricity rate ($ per kWh).

        Returns
        -------
        float
            Total cost ($).
        """
        raise NotImplementedError(
            "You must implement cost(self, energy_kwh, rate_per_kwh). "
            "Use: return energy_kwh * rate_per_kwh"
        )