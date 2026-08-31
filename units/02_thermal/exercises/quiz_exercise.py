"""Unit 02 — Thermal Physics: auto-graded quiz (student version).

Task
----
Fill in the 10 answer hooks below.  Each method returns the answer to one
DSE-style question about thermal physics (ideal gas law, specific heat,
absolute zero, kinetic theory).  Numeric questions return a ``float``;
conceptual questions return the letter of the correct option (e.g. ``"A"``).

What to do
----------
1. Read the question in each method's docstring.
2. Replace the ``raise NotImplementedError`` line with the correct answer.
3. Run the auto-grader to check your work:

       uv run pytest units/02_thermal/exercises/test_quiz.py

   (10 tests — one per question.  All fail until you fill in the hooks.)

CAF reference: Curriculum item a (heat and internal energy), c (gases and
kinetic theory), g (average kinetic energy and the Kelvin scale).
"""

from __future__ import annotations


class StudentQuiz:
    """Student answers to the Unit 02 thermal physics quiz.

    Each method returns the answer to one question.  Numeric answers are
    returned as ``float``; multiple-choice answers are returned as the
    option letter (``"A"``, ``"B"``, ``"C"`` or ``"D"``).
    """

    # -- Numeric questions -------------------------------------------------

    def q1_ideal_gas_pressure(self) -> float:
        """Q1. One mole of an ideal gas occupies 0.0224 m³ at 273 K.

        Using ``pV = nRT`` with R = 8.314 J/(mol·K), what is the pressure
        (in Pa)?
        """
        raise NotImplementedError(
            "You must implement q1_ideal_gas_pressure(self).  "
            "Use p = n * R * T / V with n = 1.0, R = 8.314, "
            "T = 273, V = 0.0224."
        )

    def q2_specific_heat_energy(self) -> float:
        """Q2. 2.0 kg of water (c = 4200 J/(kg·K)) is heated by 10 K.

        Using ``Q = mcΔT``, how much heat (in joules) is absorbed?
        """
        raise NotImplementedError(
            "You must implement q2_specific_heat_energy(self).  "
            "Use Q = m * c * delta_T with m = 2.0, c = 4200, delta_T = 10."
        )

    def q3_kelvin_conversion(self) -> float:
        """Q3. Convert 25 °C to the Kelvin scale.

        Using ``T(K) = T(°C) + 273.15``, what is the temperature in kelvin?
        """
        raise NotImplementedError(
            "You must implement q3_kelvin_conversion(self).  "
            "Use T = 25 + 273.15."
        )

    def q4_average_ke(self) -> float:
        """Q4. The average kinetic energy of a gas molecule at temperature
        T is ``KE_avg = (3/2)kT``.

        With k = 1.38 × 10⁻²³ J/K and T = 300 K, what is KE_avg (in joules)?
        """
        raise NotImplementedError(
            "You must implement q4_average_ke(self).  "
            "Use KE = 1.5 * k * T with k = 1.38e-23 and T = 300."
        )

    def q5_charles_law(self) -> float:
        """Q5. A gas occupies 2.0 L at 300 K at constant pressure.

        Using Charles' law ``V/T = constant``, what volume (in litres) does
        it occupy at 450 K?
        """
        raise NotImplementedError(
            "You must implement q5_charles_law(self).  "
            "Use V2 = V1 * T2 / T1 with V1 = 2.0, T1 = 300, T2 = 450."
        )

    def q6_boyles_law(self) -> float:
        """Q6. A gas at 100 kPa occupies 2.0 L.  It is compressed to 1.0 L
        at constant temperature.

        Using Boyle's law ``p₁V₁ = p₂V₂``, what is the new pressure (in kPa)?
        """
        raise NotImplementedError(
            "You must implement q6_boyles_law(self).  "
            "Use p2 = p1 * V1 / V2 with p1 = 100, V1 = 2.0, V2 = 1.0."
        )

    # -- Conceptual questions ----------------------------------------------

    def q7_absolute_zero(self) -> str:
        """Q7. What is absolute zero on the Celsius scale?

        A) 0 °C
        B) -273.15 °C
        C) -100 °C
        D) 273.15 °C

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q7_absolute_zero(self).  "
            "Return the letter of the correct option."
        )

    def q8_boyles_law_identify(self) -> str:
        """Q8. Which gas law states that, at constant temperature, the
        pressure of a fixed mass of gas is inversely proportional to its
        volume?

        A) Charles' law
        B) Boyle's law
        C) the pressure law
        D) Avogadro's law

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q8_boyles_law_identify(self).  "
            "Return the letter of the correct option."
        )

    def q9_temperature_measure(self) -> str:
        """Q9. Temperature is a measure of which microscopic quantity?

        A) the average kinetic energy of the molecules
        B) the total internal energy of the gas
        C) the number of molecules in the gas
        D) the speed of the fastest molecule

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q9_temperature_measure(self).  "
            "Return the letter of the correct option."
        )

    def q10_mb_distribution(self) -> str:
        """Q10. When the temperature of a gas increases, what happens to
        its Maxwell-Boltzmann speed distribution?

        A) it narrows and the peak shifts to a lower speed
        B) it broadens and the peak shifts to a higher speed
        C) it is unchanged
        D) it narrows and the peak shifts to a higher speed

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q10_mb_distribution(self).  "
            "Return the letter of the correct option."
        )