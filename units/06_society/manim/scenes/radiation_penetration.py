"""Scene B — Alpha, beta, gamma radiation penetrating power.

Shows a schematic of alpha, beta, and gamma radiation passing through
different materials: paper, aluminium, and lead.  The key takeaway is
the inverse relationship between ionising power and penetrating power.

English labels only.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    Create,
    DOWN,
    FadeIn,
    GREEN,
    LEFT,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    Square,
    Text,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
)


class RadiationPenetration(Scene):
    """Alpha, beta, gamma penetrating power through matter."""

    def construct(self) -> None:
        # ==================================================================
        # Radiation types
        # ==================================================================
        rad_data = [
            ("Alpha (\\alpha)", "He-4 nucleus", RED, 0.3),
            ("Beta (\\beta)", "Electron", BLUE, 0.6),
            ("Gamma (\\gamma)", "EM wave / photon", YELLOW, 0.9),
        ]

        # Materials
        materials = [
            ("Paper", GREEN, 0.3),
            ("Aluminium", BLUE, 0.6),
            ("Lead", ORANGE, 0.9),
        ]

        # ==================================================================
        # Layout
        # ==================================================================
        title = Text("Penetrating Power of Radiation", font_size=30)
        title.to_corner(UP, buff=0.3)
        self.play(Write(title))

        # Draw three columns: one per radiation type
        col_x_positions = [-4.0, 0.0, 4.0]
        col_labels = []

        for i, (name, desc, color, _) in enumerate(rad_data):
            label = Text(name, font_size=22, color=color)
            label.move_to(np.array([col_x_positions[i], 2.0, 0]))
            col_labels.append(label)

        self.play(*[Write(lbl) for lbl in col_labels])

        # Draw material barriers
        barrier_y = 0.5
        barrier_h = 0.3

        for mat_idx, (mat_name, mat_color, _) in enumerate(materials):
            for col_idx in range(3):
                x = col_x_positions[col_idx]
                y = barrier_y - mat_idx * 1.2
                barrier = Square(side_length=0.8, color=mat_color, fill_opacity=0.3)
                barrier.move_to(np.array([x, y, 0]))
                self.play(Create(barrier), run_time=0.3)

                label = Text(mat_name, font_size=16, color=mat_color)
                label.next_to(barrier, DOWN, buff=0.1)
                self.play(Write(label), run_time=0.2)

        # ==================================================================
        # Show which radiation passes through which material
        # ==================================================================
        # Alpha: stopped by paper
        alpha_stop = Text("Stopped by paper", font_size=18, color=RED)
        alpha_stop.move_to(np.array([col_x_positions[0], -2.5, 0]))
        self.play(Write(alpha_stop))

        # Beta: stopped by aluminium
        beta_stop = Text("Stopped by Al", font_size=18, color=BLUE)
        beta_stop.move_to(np.array([col_x_positions[1], -2.5, 0]))
        self.play(Write(beta_stop))

        # Gamma: requires lead
        gamma_stop = Text("Requires lead / concrete", font_size=18, color=YELLOW)
        gamma_stop.move_to(np.array([col_x_positions[2], -2.5, 0]))
        self.play(Write(gamma_stop))

        # ==================================================================
        # Summary
        # ==================================================================
        summary = VGroup()
        summary_lines = [
            "Penetrating power: gamma > beta > alpha",
            "Ionising power: alpha > beta > gamma",
            "Alpha: stopped by paper / few cm of air",
            "Beta: stopped by few mm of aluminium",
            "Gamma: requires thick lead or concrete",
        ]
        for i, line in enumerate(summary_lines):
            t = Text(line, font_size=18, color=WHITE)
            t.to_corner(DOWN + LEFT, buff=0.3 + i * 0.35)
            summary.add(t)

        self.play(*[FadeIn(t) for t in summary], run_time=1.5)
        self.wait(2.0)