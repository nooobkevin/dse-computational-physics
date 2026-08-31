"""Unit 05 — Physics & Engineering: auto-graded quiz (student version).

Task
----
Fill in the 10 answer hooks below.  Each method returns the answer to one
DSE-style question about physics and engineering (mechanical power P = Fv,
Bernoulli's principle, orbital velocity, electromagnetic induction, power
rating / transformers).  Numeric questions return a ``float``; conceptual
questions return the letter of the correct option (e.g. ``"A"``).

What to do
----------
1. Read the question in each method's docstring.
2. Replace the ``raise NotImplementedError`` line with the correct answer.
3. Run the auto-grader to check your work:

       uv run pytest units/05_engineering/exercises/test_quiz.py

   (10 tests — one per question.  All fail until you fill in the hooks.)

CAF reference: Curriculum item a (induction, transformers), b (power
rating), c (Bernoulli, orbital velocity v = √(GM/r)).
"""

from __future__ import annotations

import math


class StudentQuiz:
    """Student answers to the Unit 05 physics & engineering quiz.

    Each method returns the answer to one question.  Numeric answers are
    returned as ``float``; multiple-choice answers are returned as the
    option letter (``"A"``, ``"B"``, ``"C"`` or ``"D"``).
    """

    # -- Numeric questions -------------------------------------------------

    def q1_mechanical_power(self) -> float:
        """Q1. A car engine pushes the car forward with a constant force
        F = 1500 N while the car moves at a steady speed v = 20 m/s.

        Using ``P = Fv``, what is the mechanical power output
        (in watts) of the engine?
        """
        raise NotImplementedError(
            "You must implement q1_mechanical_power(self).  "
            "Use P = F * v with F = 1500 and v = 20."
        )

    def q2_pitot_speed(self) -> float:
        """Q2. A pitot tube measures a pressure difference ΔP = 500 Pa
        between the stagnation point and the static port.  The air density
        is ρ = 1.2 kg/m³.

        Using ``v = √(2ΔP/ρ)``, what is the air speed (in m/s)?
        """
        raise NotImplementedError(
            "You must implement q2_pitot_speed(self).  "
            "Use v = sqrt(2 * dP / rho) with dP = 500 and rho = 1.2."
        )

    def q3_orbital_velocity(self) -> float:
        """Q3. A satellite orbits a planet of mass M = 6.0 × 10²⁴ kg at a
        distance r = 6.0 × 10⁶ m from the planet's centre.
        G = 6.67 × 10⁻¹¹ N·m²/kg².

        Using ``v = √(GM/r)``, what is the orbital speed (in m/s)?
        """
        raise NotImplementedError(
            "You must implement q3_orbital_velocity(self).  "
            "Use v = sqrt(G * M / r) with G = 6.67e-11, M = 6.0e24 "
            "and r = 6.0e6."
        )

    def q4_induced_emf(self) -> float:
        """Q4. A metal rod of length L = 0.20 m moves at speed v = 4.0 m/s
        perpendicular to a uniform magnetic field B = 0.50 T.

        Using ``ε = B L v``, what is the induced e.m.f. (in volts) across
        the ends of the rod?
        """
        raise NotImplementedError(
            "You must implement q4_induced_emf(self).  "
            "Use emf = B * L * v with B = 0.50, L = 0.20 and v = 4.0."
        )

    def q5_appliance_current(self) -> float:
        """Q5. An electric kettle is rated at P = 2200 W and is designed
        for the mains voltage V = 220 V.

        Using ``I = P/V``, what is the operating current (in amperes)?
        """
        raise NotImplementedError(
            "You must implement q5_appliance_current(self).  "
            "Use I = P / V with P = 2200 and V = 220."
        )

    def q6_transformer_voltage(self) -> float:
        """Q6. An ideal transformer has N_p = 1000 turns on the primary
        and N_s = 100 turns on the secondary.  The primary is connected to
        V_p = 220 V.

        Using ``V_s = V_p × N_s / N_p``, what is the secondary voltage
        (in volts)?
        """
        raise NotImplementedError(
            "You must implement q6_transformer_voltage(self).  "
            "Use Vs = Vp * Ns / Np with Vp = 220, Ns = 100 and Np = 1000."
        )

    # -- Conceptual questions ----------------------------------------------

    def q7_bernoulli_pressure(self) -> str:
        """Q7. According to Bernoulli's principle, where the speed of a
        fluid is higher, the pressure is:

        A) higher
        B) lower
        C) unchanged
        D) zero

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q7_bernoulli_pressure(self).  "
            "Return the letter of the correct option."
        )

    def q8_orbit_speed_vs_radius(self) -> str:
        """Q8. For a satellite in a circular orbit, if the orbital radius
        is increased (while the central mass stays the same), the orbital
        speed:

        A) increases
        B) decreases
        C) stays the same
        D) becomes zero

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q8_orbit_speed_vs_radius(self).  "
            "Return the letter of the correct option."
        )

    def q9_lenz_law(self) -> str:
        """Q9. Lenz's law states that the direction of an induced current
        is such that it opposes:

        A) the change in magnetic flux that produces it
        B) the applied voltage of the circuit
        C) the weight of the conductor
        D) the magnetic field of the Earth

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q9_lenz_law(self).  "
            "Return the letter of the correct option."
        )

    def q10_step_up_transformer(self) -> str:
        """Q10. A step-up transformer (N_s > N_p) increases which quantity
        on the secondary side?

        A) voltage
        B) power
        C) frequency
        D) current

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q10_step_up_transformer(self).  "
            "Return the letter of the correct option."
        )