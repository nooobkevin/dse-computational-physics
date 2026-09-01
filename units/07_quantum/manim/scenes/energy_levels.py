"""Scene A — Energy levels in an infinite square well.

Animate the quantised energy levels E_n ∝ n² of a particle in a 1D
infinite square well.  Show the wavefunctions ψ_n(x) and probability
densities |ψ_n(x)|² for the first few levels.  A transition arrow
illustrates photon emission when the particle drops from n=2 to n=1.

Physics driver
--------------
ReferenceQuantumWell from physics_core provides the energy levels,
wavefunctions, and transition energies.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    BLUE_B,
    BLUE_D,
    Create,
    DOWN,
    FadeOut,
    GRAY,
    GREEN,
    GREEN_B,
    LEFT,
    Line,
    MathTex,
    Mobject,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    Square,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
    always_redraw,
    config,
)

from physics_core.quantum.wavefunctions import M_E, ReferenceQuantumWell


class EnergyLevels(Scene):
    """Quantised energy levels in an infinite square well — animated."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        L = 1e-10  # 1 Å
        well = ReferenceQuantumWell(L=L, m=M_E)
        n_max = 5
        energies = [well.energy_level(n) for n in range(1, n_max + 1)]
        e_max = max(energies) * 1.15

        # ------------------------------------------------------------------
        # Well representation
        # ------------------------------------------------------------------
        well_left = LEFT * 3.0
        well_width = 3.0
        well_top = UP * 2.5
        well_bottom = DOWN * 2.5
        well_height = well_top[1] - well_bottom[1]

        # Well walls
        left_wall = Line(
            well_left + DOWN * 2.5,
            well_left + UP * 2.5,
            color=GRAY,
            stroke_width=4,
        )
        right_wall = Line(
            well_left + RIGHT * well_width + DOWN * 2.5,
            well_left + RIGHT * well_width + UP * 2.5,
            color=GRAY,
            stroke_width=4,
        )
        floor = Line(
            well_left + DOWN * 2.5,
            well_left + RIGHT * well_width + DOWN * 2.5,
            color=GRAY,
            stroke_width=2,
        )

        # Labels
        well_label = Text("Infinite Square Well", font_size=24, color=GRAY)
        well_label.next_to(left_wall, UP, buff=0.3)

        # Pedagogical framing: this is a simplified model, NOT the hydrogen
        # atom (see HydrogenSpectra for the Bohr hydrogen levels).
        well_subtitle = Text(
            "simplified model - not the hydrogen atom",
            font_size=16, color=GRAY,
        )
        well_subtitle.next_to(well_label, DOWN, buff=0.15)

        # ------------------------------------------------------------------
        # Energy levels and wavefunctions
        # ------------------------------------------------------------------
        level_lines: list[Line] = []
        level_labels: list[MathTex] = []
        wf_curves: list[VGroup] = []
        prob_curves: list[VGroup] = []

        for n_idx in range(n_max):
            n = n_idx + 1
            e_frac = energies[n_idx] / e_max
            y_pos = well_bottom[1] + e_frac * well_height

            # Energy level line
            level_line = Line(
                well_left + RIGHT * 0.2 + UP * (y_pos - well_bottom[1]),
                well_left + RIGHT * (well_width - 0.2) + UP * (y_pos - well_bottom[1]),
                color=BLUE_B,
                stroke_width=2,
            )
            level_lines.append(level_line)

            # Label
            label = MathTex(f"E_{{{n}}}", font_size=22, color=BLUE_B)
            label.next_to(level_line, RIGHT, buff=0.15)
            level_labels.append(label)

            # Wavefunction curve (scaled for visibility)
            wf_group = VGroup()
            prob_group = VGroup()
            n_steps = 100
            dx = L / n_steps
            wf_scale = 0.8  # scale factor for visualisation
            wf_points = []
            prob_points = []

            for i in range(n_steps + 1):
                x = i * dx
                psi = well.wavefunction(x, n)
                prob = well.probability_density(x, n)

                # Map x to screen
                sx = well_left[0] + (x / L) * well_width
                # Wavefunction: centre at level line, scale amplitude
                sy_wf = y_pos + psi * wf_scale * 1e5
                sy_prob = y_pos + prob * wf_scale * 2e10

                wf_points.append([sx, sy_wf, 0])
                prob_points.append([sx, sy_prob, 0])

            # Convert to line segments
            for i in range(1, len(wf_points)):
                wf_group.add(
                    Line(
                        wf_points[i - 1],
                        wf_points[i],
                        color=GREEN if n % 2 == 0 else YELLOW,
                        stroke_width=2,
                    )
                )
                prob_group.add(
                    Line(
                        prob_points[i - 1],
                        prob_points[i],
                        color=GREEN_B if n % 2 == 0 else ORANGE,
                        stroke_width=2,
                    )
                )

            wf_curves.append(wf_group)
            prob_curves.append(prob_group)

        # ------------------------------------------------------------------
        # Transition arrow (n=2 -> n=1)
        # ------------------------------------------------------------------
        e1_y = well_bottom[1] + (energies[0] / e_max) * well_height
        e2_y = well_bottom[1] + (energies[1] / e_max) * well_height
        transition_arrow = Line(
            well_left + RIGHT * (well_width / 2) + UP * (e2_y - well_bottom[1]),
            well_left + RIGHT * (well_width / 2) + UP * (e1_y - well_bottom[1]),
            color=RED,
            stroke_width=3,
        )
        transition_arrow.add_tip(tip_length=0.15)

        delta_e = well.transition_energy(1, 2)
        lam = well.transition_wavelength(1, 2)
        transition_label = MathTex(
            f"\\Delta E = {delta_e:.2e}\\,\\text{{J}}",
            font_size=20,
            color=RED,
        )
        transition_label.next_to(transition_arrow, RIGHT, buff=0.3)

        # ------------------------------------------------------------------
        # Legend
        # ------------------------------------------------------------------
        legend = VGroup()
        legend_items = [
            ("Wavefunction ψ(x)", GREEN),
            ("Probability |ψ|²", GREEN_B),
        ]
        for i, (text, color) in enumerate(legend_items):
            line = Line(
                LEFT * 0.5 + DOWN * 2.8 + DOWN * i * 0.3,
                RIGHT * 0.5 + DOWN * 2.8 + DOWN * i * 0.3,
                color=color,
                stroke_width=3,
            )
            label = Text(text, font_size=16, color=color)
            label.next_to(line, RIGHT, buff=0.15)
            legend.add(line, label)

        # ------------------------------------------------------------------
        # Animation
        # ------------------------------------------------------------------
        # Draw well
        self.play(
            Create(left_wall),
            Create(right_wall),
            Create(floor),
            Write(well_label),
            Write(well_subtitle),
        )
        self.wait(0.5)

        # Draw energy levels one by one
        for n_idx in range(n_max):
            self.play(
                Create(level_lines[n_idx]),
                Write(level_labels[n_idx]),
                run_time=0.5,
            )

        self.wait(0.5)

        # Show wavefunctions and probabilities for each level
        for n_idx in range(n_max):
            n = n_idx + 1
            # Fade in wavefunction
            self.play(
                Create(wf_curves[n_idx]),
                run_time=0.8,
            )
            self.wait(0.3)
            # Fade in probability density
            self.play(
                Create(prob_curves[n_idx]),
                run_time=0.8,
            )
            self.wait(0.5)
            # Fade out both before next level
            if n_idx < n_max - 1:
                self.play(
                    FadeOut(wf_curves[n_idx]),
                    FadeOut(prob_curves[n_idx]),
                    run_time=0.3,
                )

        # Show transition
        self.play(
            Create(transition_arrow),
            Write(transition_label),
        )
        self.wait(1.0)

        # Show legend
        self.play(Write(legend))
        self.wait(1.0)