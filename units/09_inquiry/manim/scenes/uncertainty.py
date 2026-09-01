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
    RIGHT,
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
            x_length=4.4,
            y_length=3.4,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 20},
        )
        axes.center()
        axes.shift(DOWN * 0.3 + LEFT * 1.5)
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
                [px - 0.1, py + y_err_px, 0],
                [px + 0.1, py + y_err_px, 0],
                color=ORANGE,
                stroke_width=2,
            )
            cap_bot = Line(
                [px - 0.1, py - y_err_px, 0],
                [px + 0.1, py - y_err_px, 0],
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
            Text("Key Concepts:", font_size=22, color=YELLOW),
            Text("Error bars show +/-1sigma", font_size=17, color=GRAY),
            Text("measurement uncertainty", font_size=17, color=GRAY),
            Text("Best-fit line minimises", font_size=17, color=GRAY),
            Text("squared residuals", font_size=17, color=GRAY),
            Text("Slope gives g = 2 x slope", font_size=17, color=GRAY),
            Text("Percent error compares to", font_size=17, color=GRAY),
            Text("accepted value", font_size=17, color=GRAY),
            Text("Uncertainty propagates:", font_size=17, color=GRAY),
            Text("sigma_g = 2 x sigma_slope", font_size=17, color=GRAY),
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        explanation.next_to(axes, RIGHT, buff=0.5)
        explanation.align_to(axes, UP)

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


class UncertaintyRepeated(Scene):
    """Repeated measurements with outlier detection and mean±std."""

    def construct(self) -> None:
        title = Text(
            "Repeated Measurements & Outlier Detection", font_size=28, color=YELLOW
        )
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        # Simulated repeated measurements of the same quantity
        rng = np.random.default_rng(42)
        true_value = 9.81  # m/s² for g
        values = true_value + rng.normal(0, 0.15, size=5)
        values[3] = 10.45  # Introduce a clear outlier (value 4)

        # Original mean and std
        mean_orig = float(np.mean(values))
        std_orig = float(np.std(values, ddof=1))

        # IQR outlier detection
        q1 = float(np.percentile(values, 25))
        q3 = float(np.percentile(values, 75))
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        # Filter outliers
        values_clean = np.array([v for v in values if lower <= v <= upper])
        mean_clean = float(np.mean(values_clean))
        std_clean = float(np.std(values_clean, ddof=1)) if len(values_clean) > 1 else 0.0

        # Intro text
        intro = VGroup(
            Text("5 repeated measurements of g (m/s²):", font_size=20, color=GRAY),
        )
        intro.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        intro.next_to(title, DOWN, buff=0.3).align_to(LEFT, LEFT).shift(LEFT * 3.5)
        self.play(Write(intro), run_time=0.5)

        # Draw scatter of individual measurements
        axes = Axes(
            x_range=[0, 2, 1],
            y_range=[9.0, 11.0, 0.5],
            x_length=4.0,
            y_length=3.5,
            axis_config={"color": GRAY_A, "include_numbers": True, "font_size": 18},
        )
        axes.move_to(RIGHT * 0.5 + DOWN * 0.2)
        self.play(Create(axes), run_time=0.8)
        self.add(
            MathTex("\\text{Trial}", font_size=18, color=GRAY).next_to(
                axes.x_axis.get_end(), DOWN
            ),
            MathTex("g\\; (\\text{m/s}^2)", font_size=18, color=GRAY).next_to(
                axes.y_axis.get_end(), LEFT
            ),
        )

        # Plot points
        x_positions = np.linspace(0.2, 1.8, 5)
        point_group = VGroup()
        labels_group = VGroup()
        for i, (xv, yv) in enumerate(zip(x_positions, values)):
            is_outlier = not (lower <= yv <= upper)
            color = RED if is_outlier else BLUE_B
            dot = Dot(axes.c2p(xv, yv), color=color, radius=0.08)
            point_group.add(dot)
            label = MathTex(
                f"{yv:.2f}",
                font_size=14, color=color,
            )
            label.next_to(dot, UP, buff=0.1)
            labels_group.add(label)

        for d in point_group:
            self.play(FadeIn(d), run_time=0.3)
        for l in labels_group:
            self.play(Write(l), run_time=0.2)

        self.wait(0.3)

        # Show mean line and std band (before outlier removal)
        mean_line_orig = axes.get_horizontal_line(
            axes.c2p(0, mean_orig), color=ORANGE, stroke_width=2
        )
        self.play(Create(mean_line_orig), run_time=0.5)

        mean_label_orig = MathTex(
            f"\\bar{{g}} = {mean_orig:.3f}", font_size=16, color=ORANGE
        )
        mean_label_orig.next_to(mean_line_orig, LEFT, buff=0.2)
        self.play(Write(mean_label_orig), run_time=0.4)

        # Outlier flagging
        outlier_idx = np.where(
            (values < lower) | (values > upper)
        )[0]
        if len(outlier_idx) > 0:
            flag_text = Text(
                f"Outlier! IQR = [{lower:.2f}, {upper:.2f}]",
                font_size=16, color=RED,
            )
            flag_text.next_to(axes, DOWN, buff=0.3)
            self.play(Write(flag_text), run_time=0.6)

        self.wait(0.5)

        # Show corrected mean
        new_mean_line = axes.get_horizontal_line(
            axes.c2p(0, mean_clean), color=GREEN, stroke_width=3
        )
        self.play(Create(new_mean_line), run_time=0.5)

        corrected_label = MathTex(
            f"\\text{{Corrected }}\\bar{{g}} = {mean_clean:.3f}",
            font_size=18, color=GREEN,
        )
        corrected_label.next_to(new_mean_line, RIGHT, buff=0.3)
        self.play(Write(corrected_label), run_time=0.5)

        self.wait(0.5)

        # Summary info panel (right)
        summary_lines = [
            "Original:",
            f"  Mean = {mean_orig:.4f} m/s²",
            f"  Std = {std_orig:.4f} m/s²",
            "",
            "IQR method:",
            f"  Q1 = {q1:.3f}, Q3 = {q3:.3f}",
            f"  IQR = {iqr:.3f}",
            f"  Outlier < {lower:.3f} or > {upper:.3f}",
            "",
            "After outlier removal:",
            f"  N = {len(values_clean)} points",
            f"  Corrected mean = {mean_clean:.4f} m/s²",
            f"  Corrected std = {std_clean:.4f} m/s²",
            f"  True value = {true_value:.2f} m/s²",
        ]
        summary = VGroup(
            *[Text(line, font_size=14, color=GRAY) for line in summary_lines]
        )
        summary.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        summary.next_to(title, DOWN, buff=0.5).align_to(RIGHT, RIGHT).shift(LEFT * 0.5)
        for line in summary:
            self.play(Write(line), run_time=0.25)
        self.wait(1.5)