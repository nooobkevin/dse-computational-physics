"""Scene B — Hubble's law: expanding universe with galaxies receding.

Shows a scatter plot of galaxies with recession velocity proportional to
distance (v = H0 * d).  The theoretical line is drawn alongside galaxy
dots with peculiar velocity scatter.
"""

from __future__ import annotations

import math
import random

import numpy as np
from manim import (
    BLUE,
    Create,
    DEGREES,
    Dot,
    DOWN,
    LEFT,
    Line,
    MathTex,
    ORANGE,
    RIGHT,
    Scene,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from physics_core.astrophysics.hubble import HubbleLaw


class HubbleLawScene(Scene):
    """Hubble's law: v = H0 * d with galaxy scatter."""

    def construct(self) -> None:
        hl = HubbleLaw(h0=67.8)
        random.seed(42)

        # Generate synthetic galaxies
        n_galaxies = 20
        max_dist = 500.0  # Mpc
        distances = [random.uniform(10.0, max_dist) for _ in range(n_galaxies)]
        velocities = [hl.velocity(d) + random.uniform(-200, 200) for d in distances]

        max_vel = hl.velocity(max_dist)

        # ==================================================================
        # Axes
        # ==================================================================
        axes = VGroup()
        # x-axis
        x_axis = Line(
            LEFT * 5.0 + DOWN * 2.5,
            RIGHT * 5.0 + DOWN * 2.5,
            color=BLUE,
        )
        # y-axis
        y_axis = Line(
            LEFT * 5.0 + DOWN * 2.5,
            LEFT * 5.0 + UP * 2.5,
            color=BLUE,
        )
        axes.add(x_axis, y_axis)

        # Labels
        x_label = MathTex("d \\; (\\text{Mpc})", font_size=24).next_to(
            x_axis, DOWN, buff=0.3
        )
        y_label = MathTex("v \\; (\\text{km/s})", font_size=24).next_to(
            y_axis, LEFT, buff=0.3
        ).rotate(90 * DEGREES)

        # Ticks
        ticks = VGroup()
        for d in range(0, 601, 100):
            px = LEFT * 5.0 + RIGHT * (d / max_dist) * 10.0 + DOWN * 2.5
            tick = Line(px + DOWN * 0.1, px + UP * 0.1, color=BLUE)
            label = MathTex(str(d), font_size=14).next_to(tick, DOWN, buff=0.1)
            ticks.add(tick, label)
        for v in range(0, int(max_vel) + 1, 5000):
            py = DOWN * 2.5 + UP * (v / max_vel) * 5.0 + LEFT * 5.0
            tick = Line(py + LEFT * 0.1, py + RIGHT * 0.1, color=BLUE)
            label = MathTex(str(v), font_size=14).next_to(tick, LEFT, buff=0.1)
            ticks.add(tick, label)

        self.play(Create(axes), Write(x_label), Write(y_label), Create(ticks))

        # ==================================================================
        # Theoretical line v = H0 * d
        # ==================================================================
        line_start = LEFT * 5.0 + DOWN * 2.5
        line_end = LEFT * 5.0 + RIGHT * 10.0 + DOWN * 2.5 + UP * 5.0
        theory_line = Line(line_start, line_end, color=YELLOW, stroke_width=3)
        theory_label = MathTex(
            "v = H_0 \\, d", font_size=22, color=YELLOW
        ).next_to(theory_line, UP + RIGHT, buff=0.1)
        self.play(Create(theory_line), Write(theory_label))

        # ==================================================================
        # Galaxy dots
        # ==================================================================
        galaxy_dots = VGroup()
        for d, v in zip(distances, velocities):
            px = -5.0 + (d / max_dist) * 10.0
            py = -2.5 + (v / max_vel) * 5.0
            dot = Dot(np.array([px, py, 0]), color=ORANGE, radius=0.06)
            galaxy_dots.add(dot)

        self.play(Create(galaxy_dots), run_time=1.5)

        # ==================================================================
        # Title
        # ==================================================================
        title = MathTex(
            "\\text{Hubble's Law: The Expanding Universe}",
            font_size=30,
        ).to_corner(UP + LEFT, buff=0.5)
        h0_label = MathTex(
            f"H_0 = {hl.h0}\\,\\text{{km/s/Mpc}}",
            font_size=22,
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), Write(h0_label))

        self.wait(2.0)