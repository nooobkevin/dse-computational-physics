"""Unit 01 — Mechanics: auto-graded quiz (student version).

Task
----
Fill in the 10 answer hooks below.  Each method returns the answer to one
DSE-style question about mechanics (SUVAT kinematics, SHM, energy, momentum,
projectiles).  Numeric questions return a ``float``; conceptual questions
return the letter of the correct option (e.g. ``"A"``).

What to do
----------
1. Read the question in each method's docstring.
2. Replace the ``raise NotImplementedError`` line with the correct answer.
3. Run the auto-grader to check your work:

       uv run pytest units/01_mechanics/exercises/test_quiz.py

   (10 tests — one per question.  All fail until you fill in the hooks.)

CAF reference: Curriculum item b (kinematics), d (work/energy/power),
e (momentum), g (periodic motion / SHM).
"""

from __future__ import annotations

import math


class StudentQuiz:
    """Student answers to the Unit 01 mechanics quiz.

    Each method returns the answer to one question.  Numeric answers are
    returned as ``float``; multiple-choice answers are returned as the
    option letter (``"A"``, ``"B"``, ``"C"`` or ``"D"``).
    """

    # -- Numeric questions -------------------------------------------------

    def q1_suvat_distance(self) -> float:
        """Q1. A car accelerates from rest at 2.0 m/s² for 5.0 s.

        Using ``s = ut + ½at²``, how far (in metres) does it travel?
        """
        raise NotImplementedError(
            "You must implement q1_suvat_distance(self).  "
            "Use s = ut + ½at² with u = 0, a = 2.0, t = 5.0."
        )

    def q2_free_fall_speed(self) -> float:
        """Q2. A ball is dropped from rest and falls freely for 2.0 s.

        Using ``v = gt`` with g = 9.81 m/s², what is its speed (in m/s)
        just before it hits the ground?
        """
        raise NotImplementedError(
            "You must implement q2_free_fall_speed(self).  "
            "Use v = g * t with g = 9.81 and t = 2.0."
        )

    def q3_shm_period(self) -> float:
        """Q3. A simple pendulum has length L = 1.0 m.

        Using the small-angle period ``T = 2π√(L/g)`` with g = 9.81 m/s²,
        what is its period (in seconds)?
        """
        raise NotImplementedError(
            "You must implement q3_shm_period(self).  "
            "Use T = 2 * pi * sqrt(L / g) with L = 1.0 and g = 9.81."
        )

    def q4_kinetic_energy(self) -> float:
        """Q4. A 2.0 kg object moves at 3.0 m/s.

        Using ``KE = ½mv²``, what is its kinetic energy (in joules)?
        """
        raise NotImplementedError(
            "You must implement q4_kinetic_energy(self).  "
            "Use KE = 0.5 * m * v * v with m = 2.0 and v = 3.0."
        )

    def q5_momentum(self) -> float:
        """Q5. A 0.5 kg ball moves at 4.0 m/s.

        Using ``p = mv``, what is its momentum (in kg·m/s)?
        """
        raise NotImplementedError(
            "You must implement q5_momentum(self).  "
            "Use p = m * v with m = 0.5 and v = 4.0."
        )

    def q6_projectile_time(self) -> float:
        """Q6. A stone is dropped from rest from a height of 19.62 m.

        Using ``t = √(2h/g)`` with g = 9.81 m/s², how long (in seconds)
        does it take to reach the ground?
        """
        raise NotImplementedError(
            "You must implement q6_projectile_time(self).  "
            "Use t = sqrt(2 * h / g) with h = 19.62 and g = 9.81."
        )

    # -- Conceptual questions ----------------------------------------------

    def q7_vector_quantity(self) -> str:
        """Q7. Which of the following is a vector quantity?

        A) speed
        B) distance
        C) displacement
        D) mass

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q7_vector_quantity(self).  "
            "Return the letter of the correct option."
        )

    def q8_shm_acceleration(self) -> str:
        """Q8. In simple harmonic motion, the acceleration is directly
        proportional to which quantity?

        A) displacement
        B) velocity
        C) time
        D) amplitude

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q8_shm_acceleration(self).  "
            "Return the letter of the correct option."
        )

    def q9_suvat_equation(self) -> str:
        """Q9. Which SUVAT equation relates final velocity, initial
        velocity, acceleration and displacement?

        A) v = u + at
        B) s = ut + ½at²
        C) v² = u² + 2as
        D) s = ½(u + v)t

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q9_suvat_equation(self).  "
            "Return the letter of the correct option."
        )

    def q10_newton_second_law(self) -> str:
        """Q10. Newton's second law states F = ma.  If the net force on a
        body is doubled while its mass stays the same, what happens to its
        acceleration?

        A) it halves
        B) it doubles
        C) it stays the same
        D) it quadruples

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q10_newton_second_law(self).  "
            "Return the letter of the correct option."
        )