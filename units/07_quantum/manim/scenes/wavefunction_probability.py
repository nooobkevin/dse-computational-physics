"""Scene C — Wavefunction ψ and probability density |ψ|².

Animate the wavefunction ψ_n(x) and probability density |ψ_n(x)|² for a
particle in an infinite square well.  Show the standing-wave pattern,
nodes, and the interpretation of |ψ|² as the probability of finding the
particle at position x.  Cycle through quantum numbers n=1,2,3,4.

Physics driver
--------------
ReferenceQuantumWell from physics_core provides the wavefunctions and
probability densities.
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
    ReplacementTransform,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
    always_redraw,
    config,
)

from physics_core.quantum.wavefunctions import M_E, ReferenceQuantumWell


class WavefunctionProbability(Scene):
    """Wavefunction ψ and |ψ|² probability density — animated."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        L = 1e-10  # 1 Å
        well = ReferenceQuantumWell(L=L, m=M_E)
        n_max = 4
        current_n = 1

        # ------------------------------------------------------------------
        # Well representation
        # ------------------------------------------------------------------
        well_left = LEFT * 3.5
        well_width = 3.0
        well_top = UP * 2.5
        well_bottom = DOWN * 2.5

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

        # Axis line through centre
        axis = Line(
            well_left + RIGHT * 0.1,
            well_left + RIGHT * (well_width - 0.1),
            color=GRAY,
            stroke_width=1,
            stroke_opacity=0.5,
        )

        # ------------------------------------------------------------------
        # Labels
        # ------------------------------------------------------------------
        title = Text("Wavefunction & Probability Density", font_size=28, color=GRAY)
        title.to_edge(UP, buff=0.3)

        n_label = MathTex("n = 1", font_size=32, color=YELLOW)
        n_label.next_to(left_wall, UP, buff=0.5)

        # ------------------------------------------------------------------
        # Wavefunction and probability curves (always redrawn)
        # ------------------------------------------------------------------
        n_steps = 200
        dx = L / n_steps
        psi_si_peak = math.sqrt(2.0 / L)
        prob_si_peak = 2.0 / L

        def get_wf_curve(n: int) -> VGroup:
            group = VGroup()
            points = []
            for i in range(n_steps + 1):
                x = i * dx
                psi = well.wavefunction(x, n)
                sx = well_left[0] + (x / L) * well_width
                sy = (psi / psi_si_peak) * 1.5
                points.append([sx, sy, 0])
            for i in range(1, len(points)):
                group.add(
                    Line(
                        points[i - 1],
                        points[i],
                        color=GREEN,
                        stroke_width=3,
                    )
                )
            return group

        def get_prob_curve(n: int) -> VGroup:
            group = VGroup()
            points = []
            for i in range(n_steps + 1):
                x = i * dx
                prob = well.probability_density(x, n)
                sx = well_left[0] + (x / L) * well_width
                sy = (prob / prob_si_peak) * 2.0
                points.append([sx, sy, 0])
            for i in range(1, len(points)):
                group.add(
                    Line(
                        points[i - 1],
                        points[i],
                        color=ORANGE,
                        stroke_width=3,
                    )
                )
            return group

        # ------------------------------------------------------------------
        # Legend
        # ------------------------------------------------------------------
        legend = VGroup()
        legend_items = [
            ("ψ(x) — wavefunction", GREEN),
            ("|ψ(x)|² — probability", ORANGE),
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
        # Physics explanation text
        # ------------------------------------------------------------------
        explanations = {
            1: "Ground state: one antinode, no nodes",
            2: "First excited: one node at centre",
            3: "Second excited: two nodes",
            4: "Third excited: three nodes",
        }

        explanation_text = Text(
            explanations[1], font_size=20, color=GRAY
        )
        explanation_text.next_to(legend, DOWN, buff=0.3)

        # ------------------------------------------------------------------
        # Assemble initial scene
        # ------------------------------------------------------------------
        self.add(left_wall, right_wall, floor, axis)
        self.add(title)
        self.add(n_label)

        # Initial curves for n=1
        wf_curve = get_wf_curve(1)
        prob_curve = get_prob_curve(1)
        self.add(wf_curve, prob_curve)
        self.add(legend)
        self.add(explanation_text)

        self.wait(1.5)

        # ------------------------------------------------------------------
        # Cycle through quantum numbers
        # ------------------------------------------------------------------
        for n in range(2, n_max + 1):
            # Fade out old curves
            self.play(
                FadeOut(wf_curve),
                FadeOut(prob_curve),
                run_time=0.3,
            )

            # Update to new n
            current_n = n
            wf_curve = get_wf_curve(n)
            prob_curve = get_prob_curve(n)

            # Update label
            new_n_label = MathTex(f"n = {n}", font_size=32, color=YELLOW)
            new_n_label.next_to(left_wall, UP, buff=0.5)

            # Update explanation
            new_explanation = Text(explanations[n], font_size=20, color=GRAY)
            new_explanation.next_to(legend, DOWN, buff=0.3)

            # Animate transition
            self.play(
                ReplacementTransform(n_label, new_n_label),
                ReplacementTransform(explanation_text, new_explanation),
                Create(wf_curve),
                Create(prob_curve),
                run_time=1.0,
            )
            n_label = new_n_label
            explanation_text = new_explanation

            self.wait(1.5)

        # ------------------------------------------------------------------
        # Final summary
        # ------------------------------------------------------------------
        summary = Text(
            "|ψ|² dx = probability of finding particle in [x, x+dx]",
            font_size=22,
            color=GRAY,
        )
        summary.next_to(explanation_text, DOWN, buff=0.5)
        self.play(Write(summary))
        self.wait(1.0)