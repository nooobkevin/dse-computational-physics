"""Unit 08 — Astrophysics and Relativity: auto-graded quiz (student version).

Task
----
Fill in the 10 answer hooks below.  Each method returns the answer to one
DSE-style question about astrophysics and relativity (Hubble's law,
parallax, Wien's law, time dilation, Doppler redshift, H-R diagram).
Numeric questions return a ``float``; conceptual questions return the
letter of the correct option (e.g. ``"A"``).

What to do
----------
1. Read the question in each method's docstring.
2. Replace the ``raise NotImplementedError`` line with the correct answer.
3. Run the auto-grader to check your work:

       uv run pytest units/08_astrophysics/exercises/test_quiz.py

   (10 tests — one per question.  All fail until you fill in the hooks.)

CAF reference: Curriculum item a.3 (parallax), b.1 (blackbody radiation),
b.2 (H-R diagram), b.6 (Doppler effect), b.8 (redshift / Big Bang),
c.3 (time dilation).
"""

from __future__ import annotations

import math


class StudentQuiz:
    """Student answers to the Unit 08 astrophysics quiz.

    Each method returns the answer to one question.  Numeric answers are
    returned as ``float``; multiple-choice answers are returned as the
    option letter (``"A"``, ``"B"``, ``"C"`` or ``"D"``).
    """

    # -- Numeric questions -------------------------------------------------

    def q1_hubble_velocity(self) -> float:
        """Q1. A galaxy is at distance d = 100 Mpc.

        Using Hubble's law ``v = H₀·d`` with H₀ = 70 km/s/Mpc, what is its
        recession velocity (in km/s)?
        """
        raise NotImplementedError(
            "You must implement q1_hubble_velocity(self).  "
            "Use v = H0 * d with H0 = 70 and d = 100."
        )

    def q2_parallax_distance(self) -> float:
        """Q2. A star has a parallax of p = 0.1 arcseconds.

        Using ``d = 1 / p``, what is its distance (in parsecs)?
        """
        raise NotImplementedError(
            "You must implement q2_parallax_distance(self).  "
            "Use d = 1.0 / p with p = 0.1."
        )

    def q3_wien_peak_wavelength(self) -> float:
        """Q3. The Sun's surface temperature is T = 5800 K.

        Using Wien's law ``λ_max = b / T`` with b = 2.898 × 10⁻³ m·K, what
        is the peak wavelength of its blackbody radiation (in metres)?
        """
        raise NotImplementedError(
            "You must implement q3_wien_peak_wavelength(self).  "
            "Use lam = b / T with b = 2.898e-3 and T = 5800."
        )

    def q4_time_dilation(self) -> float:
        """Q4. A spaceship moves at v = 0.6c relative to Earth.  A clock on
        board measures a proper time Δt₀ = 1.0 s.

        Using ``Δt = Δt₀ / √(1 − v²/c²)``, what dilated time (in seconds)
        does an Earth observer measure?
        """
        raise NotImplementedError(
            "You must implement q4_time_dilation(self).  "
            "Use dt = dt0 / sqrt(1 - v*v) with v = 0.6 and dt0 = 1.0."
        )

    def q5_lorentz_factor(self) -> float:
        """Q5. A particle travels at v = 0.8c.

        Using ``γ = 1 / √(1 − v²/c²)``, what is its Lorentz factor?
        """
        raise NotImplementedError(
            "You must implement q5_lorentz_factor(self).  "
            "Use gamma = 1.0 / sqrt(1 - v*v) with v = 0.8."
        )

    def q6_doppler_redshift(self) -> float:
        """Q6. A galaxy recedes from Earth at v = 3000 km/s.

        Using the non-relativistic redshift ``z = v / c`` with
        c = 3.0 × 10⁵ km/s, what is its redshift z?
        """
        raise NotImplementedError(
            "You must implement q6_doppler_redshift(self).  "
            "Use z = v / c with v = 3000 and c = 3.0e5."
        )

    # -- Conceptual questions ----------------------------------------------

    def q7_hr_diagram_sun(self) -> str:
        """Q7. On the H-R diagram, in which region does the Sun lie?

        A) white dwarfs
        B) main sequence
        C) red giants
        D) supergiants

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q7_hr_diagram_sun(self).  "
            "Return the letter of the correct option."
        )

    def q8_hr_diagram_temperature(self) -> str:
        """Q8. On the H-R diagram, where are the hottest stars located?

        A) on the left-hand side
        B) on the right-hand side
        C) at the top
        D) at the bottom

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q8_hr_diagram_temperature(self).  "
            "Return the letter of the correct option."
        )

    def q9_parallax_units(self) -> str:
        """Q9. A star has a parallax of 0.5 arcseconds.  Its distance is:

        A) 0.5 pc
        B) 2 pc
        C) 5 pc
        D) 20 pc

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q9_parallax_units(self).  "
            "Return the letter of the correct option."
        )

    def q10_time_dilation_concept(self) -> str:
        """Q10. According to special relativity, a clock moving relative to
        a stationary observer:

        A) runs faster than a stationary clock
        B) runs slower than a stationary clock
        C) runs at exactly the same rate
        D) stops completely

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q10_time_dilation_concept(self).  "
            "Return the letter of the correct option."
        )