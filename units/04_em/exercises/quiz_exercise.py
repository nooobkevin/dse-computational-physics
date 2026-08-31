"""Unit 04 — Electricity & Magnetism: auto-graded quiz (student version).

Task
----
Fill in the 10 answer hooks below.  Each method returns the answer to one
DSE-style question about electricity and magnetism (magnetic force on a
current-carrying wire, solenoid field, Ohm's law / Kirchhoff's laws, motor
torque).  Numeric questions return a ``float``; conceptual questions return
the letter of the correct option (e.g. ``"A"``).

What to do
----------
1. Read the question in each method's docstring.
2. Replace the ``raise NotImplementedError`` line with the correct answer.
3. Run the auto-grader to check your work:

       uv run pytest units/04_em/exercises/test_quiz.py

   (10 tests — one per question.  All fail until you fill in the hooks.)

CAF reference: Curriculum item b (circuits, KCL/KVL), d (magnetic fields,
F = BIL sinθ, solenoid B = μ₀nI, motor torque τ = NBIAsinφ).
"""

from __future__ import annotations

import math


class StudentQuiz:
    """Student answers to the Unit 04 electricity & magnetism quiz.

    Each method returns the answer to one question.  Numeric answers are
    returned as ``float``; multiple-choice answers are returned as the
    option letter (``"A"``, ``"B"``, ``"C"`` or ``"D"``).
    """

    # -- Numeric questions -------------------------------------------------

    def q1_wire_force(self) -> float:
        """Q1. A straight wire of length L = 0.30 m carrying a current
        I = 2.0 A lies perpendicular to a uniform magnetic field of
        B = 0.50 T.

        Using ``F = BIL sinθ`` with θ = 90°, what is the magnetic force
        (in newtons) on the wire?
        """
        raise NotImplementedError(
            "You must implement q1_wire_force(self).  "
            "Use F = B * I * L * sin(theta) with B = 0.50, I = 2.0, "
            "L = 0.30 and theta = 90 degrees."
        )

    def q2_wire_force_angle(self) -> float:
        """Q2. The same wire (L = 0.30 m, I = 2.0 A, B = 0.50 T) is now
        tilted so the wire makes an angle θ = 30° with the magnetic field.

        Using ``F = BIL sinθ``, what is the magnetic force (in newtons)?
        """
        raise NotImplementedError(
            "You must implement q2_wire_force_angle(self).  "
            "Use F = B * I * L * sin(theta) with theta = 30 degrees."
        )

    def q3_solenoid_field(self) -> float:
        """Q3. A solenoid has n = 1000 turns per metre and carries a
        current I = 2.0 A.

        Using ``B = μ₀nI`` with μ₀ = 4π × 10⁻⁷ T·m/A, what is the magnetic
        field strength (in tesla) inside the solenoid?
        """
        raise NotImplementedError(
            "You must implement q3_solenoid_field(self).  "
            "Use B = mu0 * n * I with mu0 = 4 * pi * 1e-7, n = 1000 "
            "and I = 2.0."
        )

    def q4_ohm_law(self) -> float:
        """Q4. A resistor of resistance R = 12 Ω carries a current of
        I = 0.50 A.

        Using Ohm's law ``V = IR``, what is the potential difference
        (in volts) across the resistor?
        """
        raise NotImplementedError(
            "You must implement q4_ohm_law(self).  "
            "Use V = I * R with I = 0.50 and R = 12."
        )

    def q5_kcl_total_current(self) -> float:
        """Q5. Two resistors, R₁ = 4.0 Ω and R₂ = 6.0 Ω, are connected in
        parallel across a 12 V battery.

        Using ``I = V/R`` for each branch and Kirchhoff's current law
        (I_total = I₁ + I₂), what is the total current (in amperes) drawn
        from the battery?
        """
        raise NotImplementedError(
            "You must implement q5_kcl_total_current(self).  "
            "Use I1 = V / R1, I2 = V / R2, then return I1 + I2."
        )

    def q6_motor_torque(self) -> float:
        """Q6. A motor coil has N = 50 turns, area A = 0.010 m², and
        carries a current I = 1.5 A in a magnetic field B = 0.20 T.

        Using ``τ = NBIAsinφ`` with φ = 90°, what is the torque
        (in N·m) on the coil?
        """
        raise NotImplementedError(
            "You must implement q6_motor_torque(self).  "
            "Use tau = N * B * I * A * sin(phi) with N = 50, B = 0.20, "
            "I = 1.5, A = 0.010 and phi = 90 degrees."
        )

    # -- Conceptual questions ----------------------------------------------

    def q7_max_force_orientation(self) -> str:
        """Q7. The magnetic force on a current-carrying wire in a uniform
        magnetic field is a maximum when the wire is:

        A) parallel to the magnetic field
        B) perpendicular to the magnetic field
        C) at 45° to the magnetic field
        D) independent of the wire's orientation

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q7_max_force_orientation(self).  "
            "Return the letter of the correct option."
        )

    def q8_solenoid_field_inside(self) -> str:
        """Q8. Inside a long solenoid, away from the ends, the magnetic
        field is:

        A) uniform (constant strength and direction)
        B) strongest near the ends
        C) zero everywhere
        D) sinusoidal along the axis

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q8_solenoid_field_inside(self).  "
            "Return the letter of the correct option."
        )

    def q9_kcl_statement(self) -> str:
        """Q9. Kirchhoff's current law (KCL) states that at any junction
        in a circuit:

        A) the sum of currents entering equals the sum of currents leaving
        B) the sum of potential differences around a loop is zero
        C) the current is the same in every branch
        D) the total power is conserved

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q9_kcl_statement(self).  "
            "Return the letter of the correct option."
        )

    def q10_force_direction_rule(self) -> str:
        """Q10. The direction of the force on a current-carrying conductor
        in a magnetic field is found using:

        A) the right-hand grip rule
        B) Fleming's left-hand rule
        C) Fleming's right-hand rule
        D) Lenz's law

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q10_force_direction_rule(self).  "
            "Return the letter of the correct option."
        )