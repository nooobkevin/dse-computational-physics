"""Scene A — Linearisation: turning a non-linear relationship into a straight line.

Animate the concept of linearisation using the pendulum period example:
T = 2π √(L/g) is a non-linear relationship between T and L, but T² vs L
is a straight line through the origin.  The scene shows both graphs side
by side, then highlights the best-fit line on the linearised plot.

Physics driver
--------------
ReferenceLinearFit from physics_core.inquiry.analysis provides the
least-squares fit for the linearised data.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    Axes,
    BLUE_B,
    BLUE_D,
    Create,
    Dot,
    DOWN,
    FadeIn,
    GRAY,
    GRAY_A,
    GRAY_B,
    GREEN,
    GREEN_C,
    LaggedStart,
    LEFT,
    MathTex,
    RED_C,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from physics_core.inquiry.analysis import ReferenceLinearFit


class Linearisation(Scene):
    """Linearising a non-linear relationship — pendulum T² vs L."""

    def construct(self) -> None:
        g = 9.81
        lengths = np.linspace(0.2, 1.5, 10)
        periods = 2.0 * math.pi * np.sqrt(lengths / g)
        t_sq = periods**2

        fit = ReferenceLinearFit(x_data=lengths, y_data=t_sq)
        r_sq = fit.correlation_squared()

        title = Text("Linearisation: Making Data Linear", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.0)
        self.wait(0.3)

        left_label = Text("Non-linear: T vs L", font_size=24, color=RED_C)
        left_label.move_to(LEFT * 3.5 + UP * 2.5)
        self.play(Write(left_label), run_time=0.7)

        axes_left = Axes(
            x_range=[0, 1.8, 0.5],
            y_range=[0, 2.8, 0.5],
            x_length=4.0,
            y_length=3.0,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 18},
        )
        axes_left.move_to(LEFT * 3.5 + DOWN * 0.5)
        self.play(Create(axes_left), run_time=1.0)

        x_label_left = MathTex("L", font_size=22, color=GRAY).next_to(
            axes_left.x_axis.get_end(), DOWN
        )
        y_label_left = MathTex("T", font_size=22, color=GRAY).next_to(
            axes_left.y_axis.get_end(), LEFT
        )
        self.play(Write(x_label_left), Write(y_label_left), run_time=0.5)

        dots_left = VGroup()
        for L, T in zip(lengths, periods):
            dots_left.add(Dot(axes_left.c2p(L, T), color=BLUE_B, radius=0.06))
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_left], lag_ratio=0.15),
            run_time=2.0,
        )

        L_curve = np.linspace(0.2, 1.5, 100)
        T_curve = 2.0 * math.pi * np.sqrt(L_curve / g)
        curve_left = axes_left.plot_line_graph(
            x_values=L_curve,
            y_values=T_curve,
            line_color=BLUE_D,
            stroke_width=2,
            add_vertex_dots=False,
        )
        self.play(Create(curve_left), run_time=1.2)
        self.wait(0.3)

        arrow = MathTex(r"\Rightarrow", font_size=48, color=YELLOW)
        arrow.move_to(RIGHT * 0.5)
        self.play(Write(arrow), run_time=0.5)

        right_label = Text("Linearised: T\u00b2 vs L", font_size=24, color=GREEN)
        right_label.move_to(RIGHT * 3.5 + UP * 2.5)
        self.play(Write(right_label), run_time=0.7)

        axes_right = Axes(
            x_range=[0, 1.8, 0.5],
            y_range=[0, 7.0, 1.0],
            x_length=4.0,
            y_length=3.0,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 18},
        )
        axes_right.move_to(RIGHT * 3.5 + DOWN * 0.5)
        self.play(Create(axes_right), run_time=1.0)

        x_label_right = MathTex("L", font_size=22, color=GRAY).next_to(
            axes_right.x_axis.get_end(), DOWN
        )
        y_label_right = MathTex("T^2", font_size=22, color=GRAY).next_to(
            axes_right.y_axis.get_end(), LEFT
        )
        self.play(Write(x_label_right), Write(y_label_right), run_time=0.5)

        dots_right = VGroup()
        for L, T2 in zip(lengths, t_sq):
            dots_right.add(Dot(axes_right.c2p(L, T2), color=GREEN_C, radius=0.06))
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_right], lag_ratio=0.15),
            run_time=2.0,
        )

        x_fit, y_fit = fit.position()
        fit_line = axes_right.plot_line_graph(
            x_values=x_fit,
            y_values=y_fit,
            line_color=GREEN,
            stroke_width=3,
            add_vertex_dots=False,
        )
        self.play(Create(fit_line), run_time=1.2)

        eq_text = MathTex(
            r"T^2 = \frac{4\pi^2}{g}\,L",
            font_size=28,
            color=GREEN,
        )
        eq_text.next_to(axes_right, DOWN, buff=0.3)
        self.play(Write(eq_text), run_time=0.8)

        r_sq_text = MathTex(
            f"R^2 = {r_sq:.4f}",
            font_size=22,
            color=GRAY_B,
        )
        r_sq_text.next_to(eq_text, DOWN, buff=0.15)
        self.play(Write(r_sq_text), run_time=0.6)
        self.wait(0.3)

        explanation = VGroup(
            Text("Why linearise?", font_size=28, color=YELLOW),
            Text("Easier to identify trends", font_size=22, color=GRAY),
            Text("Best-fit line gives slope = 4pi^2/g", font_size=22, color=GRAY),
            Text("Estimate g from the slope", font_size=22, color=GRAY),
            Text("R^2 quantifies goodness of fit", font_size=22, color=GRAY),
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation.next_to(title, DOWN, buff=0.5)
        explanation.shift(LEFT * 0.5)

        for line in explanation:
            self.play(Write(line), run_time=0.55)
        self.wait(1.5)


class LinearisationShort(Scene):
    """Shorter version of Linearisation for quick previews."""

    def construct(self) -> None:
        g = 9.81
        lengths = np.linspace(0.2, 1.5, 10)
        t_sq = (4.0 * math.pi**2 / g) * lengths

        fit = ReferenceLinearFit(x_data=lengths, y_data=t_sq)

        title = Text("Linearisation", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.add(title)

        axes = Axes(
            x_range=[0, 1.8, 0.5],
            y_range=[0, 7.0, 1.0],
            x_length=6.0,
            y_length=4.0,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 20},
        )
        axes.center()

        dots = VGroup()
        for L, T2 in zip(lengths, t_sq):
            dots.add(Dot(axes.c2p(L, T2), color=GREEN_C, radius=0.07))

        x_fit, y_fit = fit.position()
        fit_line = axes.plot_line_graph(
            x_values=x_fit,
            y_values=y_fit,
            line_color=GREEN,
            stroke_width=3,
            add_vertex_dots=False,
        )

        eq_text = MathTex(
            r"T^2 = \frac{4\pi^2}{g}\,L",
            font_size=30,
            color=GREEN,
        )
        eq_text.next_to(axes, DOWN, buff=0.4)

        self.add(axes, dots, fit_line, eq_text)
        self.wait(3.0)