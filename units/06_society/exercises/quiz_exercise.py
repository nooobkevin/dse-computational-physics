"""Unit 06 — Physics & Society: auto-graded quiz (student version).

Task
----
Fill in the 10 answer hooks below.  Each method returns the answer to one
DSE-style question about physics and society (radioactive decay and
half-life, activity, decay data, energy sources, radioisotope uses).
Numeric questions return a ``float``; conceptual questions return the
letter of the correct option (e.g. ``"A"``).

What to do
----------
1. Read the question in each method's docstring.
2. Replace the ``raise NotImplementedError`` line with the correct answer.
3. Run the auto-grader to check your work:

       uv run pytest units/06_society/exercises/test_quiz.py

   (10 tests — one per question.  All fail until you fill in the hooks.)

CAF reference: Curriculum item 6a (radioactivity, half-life, activity,
radioisotope uses), 6b (energy sources: solar and wind power).
"""

from __future__ import annotations

import math


class StudentQuiz:
    """Student answers to the Unit 06 physics & society quiz.

    Each method returns the answer to one question.  Numeric answers are
    returned as ``float``; multiple-choice answers are returned as the
    option letter (``"A"``, ``"B"``, ``"C"`` or ``"D"``).
    """

    # -- Numeric questions -------------------------------------------------

    def q1_half_life_remaining(self) -> float:
        """Q1. A radioactive sample initially contains N₀ = 800 undecayed
        nuclei.  Its half-life is τ = 10 days.

        Using ``N = N₀(1/2)^(t/τ)``, how many nuclei remain after
        t = 30 days?
        """
        raise NotImplementedError(
            "You must implement q1_half_life_remaining(self).  "
            "Use N = N0 * (0.5) ** (t / tau) with N0 = 800, t = 30 "
            "and tau = 10."
        )

    def q2_fraction_remaining(self) -> float:
        """Q2. A sample has decayed for exactly 3 half-lives.

        Using ``N/N₀ = (1/2)^(t/τ)``, what fraction of the original
        nuclei remains?
        """
        raise NotImplementedError(
            "You must implement q2_fraction_remaining(self).  "
            "Use fraction = (0.5) ** 3."
        )

    def q3_activity(self) -> float:
        """Q3. A sample contains N = 5.0 × 10⁶ undecayed nuclei and its
        decay constant is λ = 0.020 s⁻¹.

        Using ``A = λN``, what is the activity (in becquerel)?
        """
        raise NotImplementedError(
            "You must implement q3_activity(self).  "
            "Use A = lam * N with lam = 0.020 and N = 5.0e6."
        )

    def q4_half_life_from_data(self) -> float:
        """Q4. The count rate of a radioactive source falls from
        800 counts/min to 100 counts/min in 60 minutes.

        Each half-life halves the count rate (800 → 400 → 200 → 100),
        so 3 half-lives pass in 60 minutes.  What is the half-life
        (in minutes)?
        """
        raise NotImplementedError(
            "You must implement q4_half_life_from_data(self).  "
            "Use tau = 60 / 3."
        )

    def q5_wind_power(self) -> float:
        """Q5. A wind turbine has a swept area A = 100 m², efficiency
        η = 0.50, and faces wind of speed v = 10 m/s.  Air density is
        ρ = 1.2 kg/m³.

        Using ``P = ½ηρAv³``, what is the power output (in watts)?
        """
        raise NotImplementedError(
            "You must implement q5_wind_power(self).  "
            "Use P = 0.5 * eta * rho * A * v ** 3 with eta = 0.50, "
            "rho = 1.2, A = 100 and v = 10."
        )

    def q6_solar_power(self) -> float:
        """Q6. A solar panel of area A = 2.0 m² receives sunlight of
        intensity S = 1000 W/m² and has efficiency η = 0.20.

        Using ``P = S·A·η``, what is the electrical power output
        (in watts)?
        """
        raise NotImplementedError(
            "You must implement q6_solar_power(self).  "
            "Use P = S * A * eta with S = 1000, A = 2.0 and eta = 0.20."
        )

    # -- Conceptual questions ----------------------------------------------

    def q7_most_penetrating(self) -> str:
        """Q7. Which type of radiation is the most penetrating?

        A) alpha
        B) beta
        C) gamma
        D) all are equally penetrating

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q7_most_penetrating(self).  "
            "Return the letter of the correct option."
        )

    def q8_medical_imaging(self) -> str:
        """Q8. Which application of a radioisotope relies on gamma
        emission to image inside the human body?

        A) thickness gauge in a factory
        B) medical tracer / gamma camera
        C) smoke detector
        D) carbon dating of fossils

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q8_medical_imaging(self).  "
            "Return the letter of the correct option."
        )

    def q9_chain_reaction_regime(self) -> str:
        """Q9. In a nuclear fission chain reaction, if the neutron
        multiplication factor is k = 1.0, the reaction is:

        A) subcritical (dies out)
        B) critical (self-sustaining at constant rate)
        C) supercritical (grows rapidly)
        D) impossible to sustain

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q9_chain_reaction_regime(self).  "
            "Return the letter of the correct option."
        )

    def q10_renewable_source(self) -> str:
        """Q10. Which of the following is a renewable energy source?

        A) coal
        B) natural gas
        C) solar
        D) nuclear fission

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q10_renewable_source(self).  "
            "Return the letter of the correct option."
        )