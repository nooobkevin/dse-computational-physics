"""Scene A — Radioactive decay curve and half-life concept.

Shows the exponential decay N = N0 * (1/2)^(t/T) with both the analytic
curve and a Monte Carlo simulation overlay.  The half-life is marked at
the point where N = N0/2.

Uses :class:`physics_core.society.decay.ReferenceDecaySim` so the
animation uses the same physics engine as the teacher app and the
student exercise.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    Create,
    Dot,
    DOWN,
    GREEN,
    LEFT,
    MathTex,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    VMobject,
    Write,
    YELLOW,
)

from physics_core.society.decay import ReferenceDecaySim


class RadioactiveDecay(Scene):
    """Radioactive decay curve: N = N0 * (1/2)^(t/T)."""

    def construct(self) -> None:
        # Simulation parameters
        N0 = 50000
        T = 1.0
        dt = 0.02
        n_steps = 150  # 3 half-lives

        sim = ReferenceDecaySim(N0=N0, half_life=T, dt=dt, seed=42)

        # Pre-compute analytic curve
        analytic_curve = sim.analytic_curve(n_steps)

        # Axes
        axes = VGroup()
        x_axis = VMobject()
        x_axis.set_points_as_corners([
            np.array([-4.5, -2.5, 0]),
            np.array([4.5, -2.5, 0]),
        ])
        x_axis.set_color(BLUE)
        x_axis.set_stroke(width=2)
        axes.add(x_axis)

        y_axis = VMobject()
        y_axis.set_points_as_corners([
            np.array([-4.5, -2.5, 0]),
            np.array([-4.5, 2.5, 0]),
        ])
        y_axis.set_color(BLUE)
        y_axis.set_stroke(width=2)
        axes.add(y_axis)

        # Axis labels
        t_label = MathTex("t", font_size=28, color=BLUE).next_to(
            np.array([4.5, -2.5, 0]), RIGHT, buff=0.15
        )
        n_label = MathTex("N", font_size=28, color=BLUE).next_to(
            np.array([-4.5, 2.5, 0]), UP, buff=0.15
        )

        # Scale factors
        scale_x = 9.0 / (3.0 * T)  # 3 half-lives across 9 units
        scale_y = 5.0 / float(N0)

        # Draw analytic curve (green)
        analytic_dots = VGroup()
        for t_val, n_val in analytic_curve:
            x = -4.5 + t_val * scale_x
            y = -2.5 + n_val * scale_y
            dot = Dot(np.array([x, y, 0]), color=GREEN, radius=0.02)
            analytic_dots.add(dot)

        # Half-life marker
        half_x = -4.5 + T * scale_x
        half_y = -2.5 + (N0 / 2.0) * scale_y
        half_marker = VGroup()
        # Vertical dashed line
        for i in range(10):
            y_start = -2.5 + i * (half_y + 2.5) / 10
            y_end = y_start + (half_y + 2.5) / 20
            seg = VMobject()
            seg.set_points_as_corners([
                np.array([half_x, y_start, 0]),
                np.array([half_x, y_end, 0]),
            ])
            seg.set_color(RED)
            seg.set_stroke(width=1)
            half_marker.add(seg)
        # Horizontal dashed line
        for i in range(10):
            x_start = -4.5 + i * (half_x + 4.5) / 10
            x_end = x_start + (half_x + 4.5) / 20
            seg = VMobject()
            seg.set_points_as_corners([
                np.array([x_start, half_y, 0]),
                np.array([x_end, half_y, 0]),
            ])
            seg.set_color(RED)
            seg.set_stroke(width=1)
            half_marker.add(seg)

        # Labels
        title = MathTex(
            "\\text{Radiocative Decay: } N = N_0 \\cdot 2^{-t/T}",
            font_size=30,
        ).to_corner(UP + RIGHT, buff=0.5)

        half_label = MathTex("T_{1/2}", font_size=24, color=RED).next_to(
            np.array([half_x, -2.8, 0]), DOWN, buff=0.1
        )
        n0_label = MathTex("N_0", font_size=24, color=GREEN).next_to(
            np.array([-4.5, -2.5 + N0 * scale_y, 0]), LEFT, buff=0.15
        )
        n0_2_label = MathTex(
            "N_0/2", font_size=24, color=RED
        ).next_to(
            np.array([-4.8, half_y, 0]), LEFT, buff=0.1
        )

        # Monte Carlo simulation (animated)
        mc_dots = VGroup()

        # Animate
        self.play(Create(axes), Write(t_label), Write(n_label))
        self.wait(0.3)

        self.play(Write(title))
        self.wait(0.3)

        # Draw analytic curve
        self.play(Create(analytic_dots), run_time=2.0)
        self.play(Write(n0_label))
        self.wait(0.5)

        # Draw half-life markers
        self.play(
            Create(half_marker),
            Write(half_label),
            Write(n0_2_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # Run Monte Carlo simulation and animate
        sim.reset()
        mc_curve_text = Text(
            "Monte Carlo simulation", font_size=22, color=ORANGE
        ).to_corner(DOWN + RIGHT, buff=0.5)

        self.play(Write(mc_curve_text))

        for step in range(n_steps):
            sim.step()
            t_val = sim.state["t"]
            n_val = sim.nuclei_remaining()
            x = -4.5 + t_val * scale_x
            y = -2.5 + n_val * scale_y
            dot = Dot(np.array([x, y, 0]), color=ORANGE, radius=0.025)
            mc_dots.add(dot)
            self.play(Create(dot), run_time=0.02)

        self.wait(2.0)