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


class LinearisationTransforms(Scene):
    """Additional linearisation transforms: 1/x and 1/x².

    Panel 1: y = k/x (hyperbola) — linearise as y vs 1/x.
    Panel 2: y = k/x² (inverse square) — linearise as y vs 1/x².
    """

    def construct(self) -> None:
        title = Text(
            "More Linearisation Transforms", font_size=28, color=YELLOW
        )
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        # ------------------------------------------------------------------
        # Panel 1: y = 8 / x  →  y vs 1/x (straight)
        # ------------------------------------------------------------------
        label1 = Text("y = k / x  →  y vs 1/x", font_size=18, color=BLUE_D)
        label1.move_to(LEFT * 3.5 + UP * 2.0)
        self.play(Write(label1), run_time=0.5)

        x_vals1 = np.linspace(0.5, 4.0, 12)
        k1 = 8.0
        y_curved1 = k1 / x_vals1
        y_linearised1 = y_curved1  # y vs 1/x — same y, but x axis is 1/x
        inv_x1 = 1.0 / x_vals1

        # Curved plot
        ax_curved1 = Axes(
            x_range=[0, 4.5, 1.0],
            y_range=[0, 18, 5],
            x_length=2.8,
            y_length=2.0,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 14},
        )
        ax_curved1.move_to(LEFT * 3.5 + DOWN * 0.8)
        self.play(Create(ax_curved1), run_time=0.6)
        self.add(
            MathTex("x", font_size=16, color=GRAY).next_to(
                ax_curved1.x_axis.get_end(), DOWN
            ),
            MathTex("y", font_size=16, color=GRAY).next_to(
                ax_curved1.y_axis.get_end(), LEFT
            ),
        )

        dots_c1 = VGroup()
        for xv, yv in zip(x_vals1, y_curved1):
            dots_c1.add(Dot(ax_curved1.c2p(xv, yv), color=RED_C, radius=0.05))
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_c1], lag_ratio=0.1),
            run_time=1.2,
        )

        curve_c1 = ax_curved1.plot_line_graph(
            x_values=x_vals1, y_values=y_curved1,
            line_color=RED_C, stroke_width=2, add_vertex_dots=False,
        )
        self.play(Create(curve_c1), run_time=0.7)

        # Arrow
        arrow1 = MathTex(r"\Rightarrow", font_size=30, color=YELLOW)
        arrow1.move_to(LEFT * 0.1)
        self.play(Write(arrow1), run_time=0.3)

        # Linearised plot
        ax_lin1 = Axes(
            x_range=[0, 2.2, 0.5],
            y_range=[0, 18, 5],
            x_length=2.8,
            y_length=2.0,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 14},
        )
        ax_lin1.move_to(RIGHT * 3.5 + DOWN * 0.8)
        self.play(Create(ax_lin1), run_time=0.6)
        self.add(
            MathTex("1/x", font_size=16, color=GRAY).next_to(
                ax_lin1.x_axis.get_end(), DOWN
            ),
            MathTex("y", font_size=16, color=GRAY).next_to(
                ax_lin1.y_axis.get_end(), LEFT
            ),
        )

        dots_l1 = VGroup()
        for xv, yv in zip(inv_x1, y_linearised1):
            dots_l1.add(Dot(ax_lin1.c2p(xv, yv), color=GREEN_C, radius=0.05))
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_l1], lag_ratio=0.1),
            run_time=1.2,
        )

        # Fit line
        fit1 = ReferenceLinearFit(x_data=inv_x1, y_data=y_linearised1)
        xf1, yf1 = fit1.position()
        line1 = ax_lin1.plot_line_graph(
            x_values=xf1, y_values=yf1,
            line_color=GREEN, stroke_width=2, add_vertex_dots=False,
        )
        self.play(Create(line1), run_time=0.7)

        eq1 = MathTex(
            r"y = k \cdot (1/x), \; k = 8.0",
            font_size=18, color=GREEN,
        )
        eq1.next_to(ax_lin1, DOWN, buff=0.2)
        self.play(Write(eq1), run_time=0.5)

        self.wait(0.3)

        # ------------------------------------------------------------------
        # Panel 2: y = 10 / x²  →  y vs 1/x² (straight)
        # ------------------------------------------------------------------
        label2 = Text("y = k / x²  →  y vs 1/x²", font_size=18, color=BLUE_D)
        label2.move_to(LEFT * 3.5 + DOWN * 3.2)
        self.play(Write(label2), run_time=0.5)

        x_vals2 = np.linspace(0.5, 3.5, 10)
        k2 = 10.0
        y_curved2 = k2 / x_vals2**2
        inv_x2_sq = 1.0 / x_vals2**2

        # Curved plot
        ax_curved2 = Axes(
            x_range=[0, 4.0, 1.0],
            y_range=[0, 42, 10],
            x_length=2.8,
            y_length=2.0,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 14},
        )
        ax_curved2.move_to(LEFT * 3.5 + DOWN * 4.0)
        self.play(Create(ax_curved2), run_time=0.6)
        self.add(
            MathTex("x", font_size=16, color=GRAY).next_to(
                ax_curved2.x_axis.get_end(), DOWN
            ),
            MathTex("y", font_size=16, color=GRAY).next_to(
                ax_curved2.y_axis.get_end(), LEFT
            ),
        )

        dots_c2 = VGroup()
        for xv, yv in zip(x_vals2, y_curved2):
            dots_c2.add(Dot(ax_curved2.c2p(xv, yv), color=RED_C, radius=0.05))
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_c2], lag_ratio=0.1),
            run_time=1.2,
        )

        curve_c2 = ax_curved2.plot_line_graph(
            x_values=x_vals2, y_values=y_curved2,
            line_color=RED_C, stroke_width=2, add_vertex_dots=False,
        )
        self.play(Create(curve_c2), run_time=0.7)

        # Arrow
        arrow2 = MathTex(r"\Rightarrow", font_size=30, color=YELLOW)
        arrow2.move_to(LEFT * 0.1 + DOWN * 3.2)
        self.play(Write(arrow2), run_time=0.3)

        # Linearised plot
        ax_lin2 = Axes(
            x_range=[0, 4.5, 1.0],
            y_range=[0, 42, 10],
            x_length=2.8,
            y_length=2.0,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 14},
        )
        ax_lin2.move_to(RIGHT * 3.5 + DOWN * 4.0)
        self.play(Create(ax_lin2), run_time=0.6)
        self.add(
            MathTex("1/x^2", font_size=16, color=GRAY).next_to(
                ax_lin2.x_axis.get_end(), DOWN
            ),
            MathTex("y", font_size=16, color=GRAY).next_to(
                ax_lin2.y_axis.get_end(), LEFT
            ),
        )

        dots_l2 = VGroup()
        for xv, yv in zip(inv_x2_sq, y_curved2):
            dots_l2.add(Dot(ax_lin2.c2p(xv, yv), color=GREEN_C, radius=0.05))
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_l2], lag_ratio=0.1),
            run_time=1.2,
        )

        fit2 = ReferenceLinearFit(x_data=inv_x2_sq, y_data=y_curved2)
        xf2, yf2 = fit2.position()
        line2 = ax_lin2.plot_line_graph(
            x_values=xf2, y_values=yf2,
            line_color=GREEN, stroke_width=2, add_vertex_dots=False,
        )
        self.play(Create(line2), run_time=0.7)

        eq2 = MathTex(
            r"y = k \cdot (1/x^2), \; k = 10.0",
            font_size=18, color=GREEN,
        )
        eq2.next_to(ax_lin2, DOWN, buff=0.2)
        self.play(Write(eq2), run_time=0.5)

        self.wait(1.0)