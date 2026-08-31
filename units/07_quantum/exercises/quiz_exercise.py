"""Unit 07 — Quantum Physics: auto-graded quiz (student version).

Task
----
Fill in the 10 answer hooks below.  Each method returns the answer to one
DSE-style question about quantum physics (Bohr energy levels, Balmer
wavelengths, photoelectric effect, superposition probabilities, de Broglie
wavelength).  Numeric questions return a ``float``; conceptual questions
return the letter of the correct option (e.g. ``"A"``).

What to do
----------
1. Read the question in each method's docstring.
2. Replace the ``raise NotImplementedError`` line with the correct answer.
3. Run the auto-grader to check your work:

       uv run pytest units/07_quantum/exercises/test_quiz.py

   (10 tests — one per question.  All fail until you fill in the hooks.)

CAF reference: Curriculum item b (photoelectric effect), c (Bohr hydrogen
model / line spectra), d (wave-particle duality), e (superposition and
uncertainty).
"""

from __future__ import annotations

import math


class StudentQuiz:
    """Student answers to the Unit 07 quantum physics quiz.

    Each method returns the answer to one question.  Numeric answers are
    returned as ``float``; multiple-choice answers are returned as the
    option letter (``"A"``, ``"B"``, ``"C"`` or ``"D"``).
    """

    # -- Numeric questions -------------------------------------------------

    def q1_bohr_energy_level(self) -> float:
        """Q1. In the Bohr model of hydrogen, the energy of level n is
        ``E_n = -13.6 / n²`` eV.

        What is the energy (in eV) of the n = 2 level?
        """
        raise NotImplementedError(
            "You must implement q1_bohr_energy_level(self).  "
            "Use E_n = -13.6 / n**2 with n = 2."
        )

    def q2_balmer_wavelength(self) -> float:
        """Q2. The Balmer-alpha line is the transition n = 3 → n = 2 in
        hydrogen.

        Using ``ΔE = 13.6 × (1/2² − 1/3²)`` eV and ``λ = hc / ΔE`` with
        ``hc = 1240 eV·nm``, what is the wavelength (in nm) of this line?
        """
        raise NotImplementedError(
            "You must implement q2_balmer_wavelength(self).  "
            "Use dE = 13.6 * (1/4 - 1/9) then lambda = 1240 / dE."
        )

    def q3_photoelectric_ke_max(self) -> float:
        """Q3. Light of frequency f = 1.0 × 10¹⁵ Hz shines on a metal with
        work function φ = 3.0 × 10⁻¹⁹ J.

        Using ``K_max = hf − φ`` with h = 6.63 × 10⁻³⁴ J·s, what is the
        maximum kinetic energy (in joules) of the emitted electrons?
        """
        raise NotImplementedError(
            "You must implement q3_photoelectric_ke_max(self).  "
            "Use K_max = h * f - phi with h = 6.63e-34, f = 1.0e15, "
            "phi = 3.0e-19."
        )

    def q4_threshold_frequency(self) -> float:
        """Q4. A metal has work function φ = 3.0 × 10⁻¹⁹ J.

        Using ``f₀ = φ / h`` with h = 6.63 × 10⁻³⁴ J·s, what is the
        threshold frequency (in Hz) below which no electrons are emitted?
        """
        raise NotImplementedError(
            "You must implement q4_threshold_frequency(self).  "
            "Use f0 = phi / h with phi = 3.0e-19 and h = 6.63e-34."
        )

    def q5_superposition_probability(self) -> float:
        """Q5. A qubit is prepared in the superposition
        ``|ψ⟩ = 0.6|0⟩ + 0.8|1⟩``.

        Using ``P(|0⟩) = |a|²``, what is the probability of measuring the
        state ``|0⟩``?
        """
        raise NotImplementedError(
            "You must implement q5_superposition_probability(self).  "
            "Use P = a * a with a = 0.6."
        )

    def q6_de_broglie_wavelength(self) -> float:
        """Q6. An electron of mass m = 9.11 × 10⁻³¹ kg moves at
        v = 1.0 × 10⁶ m/s.

        Using ``λ = h / (mv)`` with h = 6.63 × 10⁻³⁴ J·s, what is its
        de Broglie wavelength (in metres)?
        """
        raise NotImplementedError(
            "You must implement q6_de_broglie_wavelength(self).  "
            "Use lam = h / (m * v) with h = 6.63e-34, m = 9.11e-31, "
            "v = 1.0e6."
        )

    # -- Conceptual questions ----------------------------------------------

    def q7_photoelectric_frequency(self) -> str:
        """Q7. In the photoelectric effect, which statement is correct?

        A) increasing the light intensity increases the maximum kinetic
           energy of the emitted electrons
        B) the maximum kinetic energy of the emitted electrons depends on
           the frequency of the incident light
        C) electrons are emitted for any frequency of incident light
        D) the number of emitted electrons depends only on the frequency

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q7_photoelectric_frequency(self).  "
            "Return the letter of the correct option."
        )

    def q8_bohr_level_spacing(self) -> str:
        """Q8. In the Bohr model, the energy levels E_n = -13.6/n² eV are:

        A) equally spaced
        B) closer together as n increases
        C) further apart as n increases
        D) continuous (any energy allowed)

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q8_bohr_level_spacing(self).  "
            "Return the letter of the correct option."
        )

    def q9_superposition_measurement(self) -> str:
        """Q9. A quantum system in the superposition |ψ⟩ = a|0⟩ + b|1⟩ is
        measured.  What happens?

        A) it remains in the superposition
        B) it collapses to |0⟩ or |1⟩ with probabilities |a|² and |b|²
        C) it always collapses to |0⟩
        D) it collapses to a new superposition of both states

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q9_superposition_measurement(self).  "
            "Return the letter of the correct option."
        )

    def q10_heisenberg_uncertainty(self) -> str:
        """Q10. The Heisenberg uncertainty principle for position and
        momentum states that:

        A) Δx · Δp ≥ ħ/2
        B) Δx · Δp ≤ ħ/2
        C) Δx · Δp = 0
        D) Δx · Δp = ħ

        Return the letter of the correct option.
        """
        raise NotImplementedError(
            "You must implement q10_heisenberg_uncertainty(self).  "
            "Return the letter of the correct option."
        )