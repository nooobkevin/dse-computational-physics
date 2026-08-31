"""Unit 09 — Scientific Inquiry: auto-graded quiz (student version).

Task
----
Fill in the 10 answer hooks below.  Each method returns the answer to one
DSE-style question about scientific inquiry (linearisation, uncertainty
propagation, epidemic R₀ and thresholds, complex-system properties).
Numeric questions return a ``float``; conceptual questions return the
letter of the correct option (e.g. ``"A"``).

What to do
----------
1. Read the question in each method's docstring.
2. Replace the ``raise NotImplementedError`` line with the correct answer.
3. Run the auto-grader to check your work:

       uv run pytest units/09_inquiry/exercises/test_quiz.py

   (10 tests — one per question.  All fail until you fill in the hooks.)

CAF reference: Curriculum item on data analysis (linearisation, order of
accuracy and error treatment) and computational modelling of complex
systems (epidemic spread).
"""

from __future__ import annotations

import math


class StudentQuiz:
    """Student answers to the Unit 09 scientific inquiry quiz.

    Each method returns the answer to one question.  Numeric answers are
    returned as ``float``; multiple-choice answers are returned as the
    option letter (``"A"``, ``"B"``, ``"C"`` or ``"D"``).
    """

    # -- Numeric questions -------------------------------------------------

    def q1_linearisation_slope(self) -> float:
        """Q1. A pendulum of length L has period T = 2π√(L/g).  A student
        plots T² against L.

        Using ``slope = 4π² / g`` with g = 9.81 m/s², what is the slope of
        the straight line (in s²/m)?
        """
        raise NotImplementedError(
            "You must implement q1_linearisation_slope(self).  "
            "Use slope = 4 * pi**2 / g with g = 9.81."
        )

    def q2_linearisation_constant(self) -> float:
        """Q2. Data follow the relation ``y = k / x²``.  At x = 2.0 the
        measured value is y = 1.25.

        Using ``k = y · x²``, what is the constant k?
        """
        raise NotImplementedError(
            "You must implement q2_linearisation_constant(self).  "
            "Use k = y * x * x with y = 1.25 and x = 2.0."
        )

    def q3_uncertainty_propagation(self) -> float:
        """Q3. A quantity z is the sum z = x + y with x = 10.0 ± 0.5 and
        y = 20.0 ± 0.5.

        Using ``Δz = √(Δx² + Δy²)``, what is the uncertainty in z?
        """
        raise NotImplementedError(
            "You must implement q3_uncertainty_propagation(self).  "
            "Use dz = sqrt(dx*dx + dy*dy) with dx = 0.5 and dy = 0.5."
        )

    def q4_percent_uncertainty(self) -> float:
        """Q4. An experiment measures g = 9.81 ± 0.20 m/s².

        Using ``percent uncertainty = (Δg / g) × 100``, what is the
        percent uncertainty (in %)?
        """
        raise NotImplementedError(
            "You must implement q4_percent_uncertainty(self).  "
            "Use pct = (0.20 / 9.81) * 100."
        )

    def q5_epidemic_r0(self) -> float:
        """Q5. In an SIR epidemic model, the infection rate is
        β = 0.3 per day and the recovery rate is γ = 0.1 per day.

        Using ``R₀ = β / γ``, what is the basic reproduction number?
        """
        raise NotImplementedError(
            "You must implement q5_epidemic_r0(self).  "
            "Use R0 = beta / gamma with beta = 0.3 and gamma = 0.1."
        )

    def q6_herd_immunity_threshold(self) -> float:
        """Q6. A disease has basic reproduction number R₀ = 4.0.

        Using the herd-immunity threshold ``1 − 1/R₀``, what fraction of
        the population must be immune to stop the epidemic?
        """
        raise NotImplementedError(
            "You must implement q6_herd_immunity_threshold(self).  "
            "Use h = 1.0 - 1.0 / R0 with R0 = 4.0."
        )

    # -- Conceptual questions ----------------------------------------------

    def q7_linearisation_purpose(self) -> str:
        """Q7. Why do we linearise data (e.g. plot T² against L instead of
        T against L)?

        A) to make the graph look prettier
        B) to turn a power-law relationship into a straight line whose
           slope is a constant
        C) to reduce the number of data points
        D) to eliminate all experimental error

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q7_linearisation_purpose(self).  "
            "Return the letter of the correct option."
        )

    def q8_uncertainty_reduction(self) -> str:
        """Q8. Which practice best reduces the random uncertainty of a
        measured quantity?

        A) taking a single careful measurement
        B) taking repeated measurements and averaging them
        C) rounding the value to fewer significant figures
        D) using a smaller measuring instrument

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q8_uncertainty_reduction(self).  "
            "Return the letter of the correct option."
        )

    def q9_epidemic_threshold(self) -> str:
        """Q9. In the SIR model, an epidemic will spread (the number of
        infected people grows) when:

        A) R₀ < 1
        B) R₀ = 1
        C) R₀ > 1
        D) R₀ = 0

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q9_epidemic_threshold(self).  "
            "Return the letter of the correct option."
        )

    def q10_complex_system_property(self) -> str:
        """Q10. Which statement best describes a complex system such as an
        epidemic or a forest fire?

        A) its global behaviour is always predictable from a single agent
        B) global patterns emerge from many simple local interactions
        C) its agents never interact with one another
        D) it is always in equilibrium

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q10_complex_system_property(self).  "
            "Return the letter of the correct option."
        )