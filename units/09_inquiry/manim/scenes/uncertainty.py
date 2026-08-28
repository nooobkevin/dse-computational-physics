"""Scene B — Uncertainty & Error: error bars, best-fit line, percent error.

Animate the concept of measurement uncertainty using the free-fall example:
s = 1/2 g t^2.  Show data points with error bars, the best-fit line, the
estimated g value, and the percent error vs the accepted value.

Physics driver
--------------
ReferenceLinearFit from physics_core.inquiry.analysis provides the
least-squares fit and uncertainty propagation.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Axes,
    BLUE_B,
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
    Line,
    MathTex,
    ORANGE,
    RED,
    Scene,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from physics_core.inquiry.analysis import (
    ReferenceLinearFit,
    percent_error,
)


class Uncertainty(Scene):
    """Uncertainty & error — error bars, best-fit line, percent error."""

    def construct(self) -> None:
        g_true = 9.81
        rng = np.random.default_rng(42)
        times = np.linspace(0.1, 1.0, 8)
        t_sq = times**2
        s_true = 0.5 * g_true * t_sq
        noise = rng.normal(0, 0.08, size=len(t_sq))
        s_measured = s_true + noise

        fit = ReferenceLinearFit(x_data=t_sq, y_data=s_measured)
        slope = fit.slope()
        r_sq = fit.correlation_squared()
        g_est = 2.0 * slope
        g_err = percent_error(g_est, g_true)

        error_bars = 0.05 + 0.03 * s_measured

        title = Text("Uncertainty & Error Analysis", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.0)
        self.wait(0.3)

        axes = Axes(
            x_range=[0, 1.2, 0.2],
            y_range=[0, 5.5, 1.0],
            x_length=6.0,
            y_length=4.0,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 20},
        )
        axes.center()
        axes.shift(DOWN * 0.3)
        self.play(Create(axes), run_time=1.2)

        x_label = MathTex("t^2", font_size=24, color=GRAY).next_to(
            axes.x_axis.get_end(), DOWN
        )
        y_label = MathTex("s", font_size=24, color=GRAY).next_to(
            axes.y_axis.get_end(), LEFT
        )
        self.play(Write(x_label), Write(y_label), run_time=0.5)

        dots = VGroup()
        error_lines = VGroup()

        for i in range(len(t_sq)):
            point = axes.c2p(t_sq[i], s_measured[i])
            px, py = point[0], point[1]
            dot = Dot(point, color=BLUE_B, radius=0.07)
            dots.add(dot)

            y_err = error_bars[i]
            y_err_px = axes.c2p(0, y_err)[1] - axes.c2p(0, 0)[1]
            err_line = Line(
                [px, py - y_err_px, 0],
                [px, py + y_err_px, 0],
                color=ORANGE,
                stroke_width=2,
            )
            cap_top = Line(
                [px - 3, py + y_err_px, 0],
                [px + 3, py + y_err_px, 0],
                color=ORANGE,
                stroke_width=2,
            )
            cap_bot = Line(
                [px - 3, py - y_err_px, 0],
                [px + 3, py - y_err_px, 0],
                color=ORANGE,
                stroke_width=2,
            )
            error_lines.add(err_line, cap_top, cap_bot)

        point_groups = VGroup()
        for i in range(len(t_sq)):
            point_groups.add(VGroup(dots[i], *error_lines[3 * i:3 * i + 3]))
        self.play(
            LaggedStart(*[FadeIn(g) for g in point_groups], lag_ratio=0.2),
            run_time=3.0,
        )
        self.wait(0.3)

        x_fit, y_fit = fit.position()
        fit_line = axes.plot_line_graph(
            x_values=x_fit,
            y_values=y_fit,
            line_color=GREEN,
            stroke_width=3,
            add_vertex_dots=False,
        )
        self.play(Create(fit_line), run_time=1.5)
        self.wait(0.3)

        results = VGroup(
            MathTex(
                f"g_{{\\text{{est}}}} = {g_est:.3f}\\,\\text{{m/s}}^2",
                font_size=28, color=GREEN,
            ),
            MathTex(
                f"\\text{{Percent error}} = {g_err:.2f}\\%",
                font_size=28,
                color=RED if g_err > 1 else GREEN,
            ),
            MathTex(f"R^2 = {r_sq:.4f}", font_size=28, color=GRAY_B),
        )
        results.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        results.next_to(axes, DOWN, buff=0.5)

        for line in results:
            self.play(Write(line), run_time=0.6)
        self.wait(0.3)

        explanation = VGroup(
            Text("Key Concepts:", font_size=24, color=YELLOW),
            Text("Error bars show +/-1sigma measurement uncertainty", font_size=20, color=GRAY),
            Text("Best-fit line minimises squared residuals", font_size=20, color=GRAY),
            Text("Slope gives g = 2 x slope", font_size=20, color=GRAY),
            Text("Percent error compares to accepted value", font_size=20, color=GRAY),
            Text("Uncertainty propagates: sigma_g = 2 x sigma_slope", font_size=20, color=GRAY),
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        explanation.next_to(title, DOWN, buff=0.5)
        explanation.shift(LEFT * 0.5)

        for line in explanation:
            self.play(Write(line), run_time=0.55)
        self.wait(1.5)


class UncertaintyShort(Scene):
    """Shorter version of Uncertainty for quick previews."""

    def construct(self) -> None:
        g_true = 9.81
        rng = np.random.default_rng(42)
        times = np.linspace(0.1, 1.0, 8)
        t_sq = times**2
        s_true = 0.5 * g_true * t_sq
        s_measured = s_true + rng.normal(0, 0.08, size=len(t_sq))

        fit = ReferenceLinearFit(x_data=t_sq, y_data=s_measured)
        g_est = 2.0 * fit.slope()
        g_err = percent_error(g_est, g_true)

        title = Text("Uncertainty & Error", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.add(title)

        axes = Axes(
            x_range=[0, 1.2, 0.2],
            y_range=[0, 5.5, 1.0],
            x_length=6.0,
            y_length=4.0,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 20},
        )
        axes.center()
        axes.shift(DOWN * 0.3)

        dots = VGroup()
        for i in range(len(t_sq)):
            point = axes.c2p(t_sq[i], s_measured[i])
            dots.add(Dot(point, color=BLUE_B, radius=0.07))

        x_fit, y_fit = fit.position()
        fit_line = axes.plot_line_graph(
            x_values=x_fit,
            y_values=y_fit,
            line_color=GREEN,
            stroke_width=3,
            add_vertex_dots=False,
        )

        result = MathTex(
            f"g = {g_est:.3f}\\ \\text{{m/s}}^2,\\ \\text{{error}} = {g_err:.2f}\\%",
            font_size=28,
            color=GREEN,
        )
        result.next_to(axes, DOWN, buff=0.4)

        self.add(axes, dots, fit_line, result)
        self.wait(3.0)