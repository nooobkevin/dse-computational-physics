"""Unit 03 — Waves: auto-graded quiz (student version).

Task
----
Fill in the 10 answer hooks below.  Each method returns the answer to one
DSE-style question about waves (v = fλ, diffraction grating, Malus's law,
intensity, ultrasound, polarisation).  Numeric questions return a ``float``;
conceptual questions return the letter of the correct option (e.g. ``"A"``).

What to do
----------
1. Read the question in each method's docstring.
2. Replace the ``raise NotImplementedError`` line with the correct answer.
3. Run the auto-grader to check your work:

       uv run pytest units/03_waves/exercises/test_quiz.py

   (10 tests — one per question.  All fail until you fill in the hooks.)

CAF reference: Curriculum item a (nature of waves), b (properties of waves),
c (light waves / EM spectrum), d (sound waves).
"""

from __future__ import annotations

import math


class StudentQuiz:
    """Student answers to the Unit 03 waves quiz.

    Each method returns the answer to one question.  Numeric answers are
    returned as ``float``; multiple-choice answers are returned as the
    option letter (``"A"``, ``"B"``, ``"C"`` or ``"D"``).
    """

    # -- Numeric questions -------------------------------------------------

    def q1_wave_speed(self) -> float:
        """Q1. A sound wave has frequency 500 Hz and wavelength 0.68 m.

        Using ``v = fλ``, what is the wave speed (in m/s)?
        """
        raise NotImplementedError(
            "You must implement q1_wave_speed(self).  "
            "Use v = f * lam with f = 500 and lam = 0.68."
        )

    def q2_diffraction_grating(self) -> float:
        """Q2. Light of wavelength 500 nm hits a diffraction grating with
        slit spacing d = 1.0 × 10⁻⁶ m.

        Using ``d sinθ = nλ`` with n = 1, what is the angle θ of the first
        order maximum (in degrees)?
        """
        raise NotImplementedError(
            "You must implement q2_diffraction_grating(self).  "
            "Use sin(theta) = n * lam / d, then convert to degrees."
        )

    def q3_malus_law(self) -> float:
        """Q3. Unpolarised light of intensity 100 W/m² passes through a
        polariser and then an analyser rotated 60° from the polariser.

        Using Malus's law ``I = I₀ cos²θ``, what is the transmitted
        intensity (in W/m²)?
        """
        raise NotImplementedError(
            "You must implement q3_malus_law(self).  "
            "Use I = I0 * cos(theta)**2 with I0 = 100 and theta = 60 degrees."
        )

    def q4_ultrasound_echo(self) -> float:
        """Q4. An ultrasound pulse travels at 1500 m/s in tissue and the
        echo returns after 0.004 s.

        Using ``d = vt/2``, how far away (in metres) is the reflecting
        surface?
        """
        raise NotImplementedError(
            "You must implement q4_ultrasound_echo(self).  "
            "Use d = v * t / 2 with v = 1500 and t = 0.004."
        )

    def q5_inverse_square(self) -> float:
        """Q5. The intensity of a point source is 90 W/m² at a distance of
        1 m.

        Using the inverse-square law ``I ∝ 1/r²``, what is the intensity
        (in W/m²) at a distance of 3 m?
        """
        raise NotImplementedError(
            "You must implement q5_inverse_square(self).  "
            "Use I = I0 / r**2 with I0 = 90 and r = 3."
        )

    def q6_fringe_spacing(self) -> float:
        """Q6. In Young's double-slit experiment, light of wavelength
        500 nm passes through slits separated by 1.0 × 10⁻³ m onto a screen
        2.0 m away.

        Using ``Δy = λD/d``, what is the fringe spacing (in metres)?
        """
        raise NotImplementedError(
            "You must implement q6_fringe_spacing(self).  "
            "Use delta_y = lam * D / d with lam = 500e-9, D = 2.0, "
            "d = 1.0e-3."
        )

    # -- Conceptual questions ----------------------------------------------

    def q7_transverse_wave(self) -> str:
        """Q7. Which of the following is a transverse wave?

        A) sound in air
        B) light
        C) both sound in air and light
        D) neither sound in air nor light

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q7_transverse_wave(self).  "
            "Return the letter of the correct option."
        )

    def q8_crossed_polarisers(self) -> str:
        """Q8. Two polarisers are crossed (their transmission axes are
        perpendicular).  What is the intensity of light transmitted through
        the second polariser?

        A) I₀
        B) I₀/2
        C) zero
        D) I₀/4

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q8_crossed_polarisers(self).  "
            "Return the letter of the correct option."
        )

    def q9_standing_wave_wavelength(self) -> str:
        """Q9. A standing wave is set up on a string of length L fixed at
        both ends.  Which expression gives the allowed wavelengths?

        A) λ = 2L/n
        B) λ = L/n
        C) λ = nL
        D) λ = 4L/n

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q9_standing_wave_wavelength(self).  "
            "Return the letter of the correct option."
        )

    def q10_sound_polarisation(self) -> str:
        """Q10. Sound waves in air cannot be polarised because they are
        which type of wave?

        A) transverse
        B) longitudinal
        C) electromagnetic
        D) stationary

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q10_sound_polarisation(self).  "
            "Return the letter of the correct option."
        )