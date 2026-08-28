"""Scene C — From Data to Conclusion: the full inquiry loop.

Animate the scientific inquiry process as a schematic diagram:
Question -> Plan -> Data -> Analyse -> Conclude -> Evaluate.
Show how evidence-based conclusions are drawn from data analysis,
using the pendulum experiment as a concrete example.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    Arrow,
    BLUE_B,
    BLUE_D,
    Create,
    FadeIn,
    GREEN,
    GREEN_C,
    DOWN,
    GRAY,
    GRAY_A,
    GRAY_B,
    Indicate,
    LEFT,
    MathTex,
    ORANGE,
    RED,
    RED_C,
    RIGHT,
    Scene,
    Square,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from physics_core.inquiry.analysis import ReferenceLinearFit, percent_error


class Conclusion(Scene):
    """From data to conclusion — the full inquiry loop."""

    def construct(self) -> None:
        title = Text("The Scientific Inquiry Loop", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.2)
        self.wait(0.4)

        stages = [
            ("Question", BLUE_B),
            ("Plan", BLUE_D),
            ("Data", GREEN_C),
            ("Analyse", GREEN),
            ("Conclude", ORANGE),
            ("Evaluate", RED_C),
        ]

        center = np.array([0.0, 1.05, 0.0])
        radius = 1.5
        boxes = VGroup()
        labels = VGroup()
        arrows = VGroup()

        for i, (label_text, color) in enumerate(stages):
            angle = -math.pi / 2 + i * 2 * math.pi / len(stages)
            pos = center + radius * np.array([math.cos(angle), math.sin(angle), 0])

            box = Square(
                side_length=1.15, color=color,
                fill_opacity=0.15, fill_color=color,
            )
            box.move_to(pos)
            label = Text(label_text, font_size=18, color=color)
            label.move_to(pos)
            boxes.add(box)
            labels.add(label)

            next_angle = -math.pi / 2 + (i + 1) * 2 * math.pi / len(stages)
            next_pos = center + radius * np.array(
                [math.cos(next_angle), math.sin(next_angle), 0]
            )
            arrow = Arrow(
                pos, next_pos,
                color=GRAY_A,
                stroke_width=2,
                buff=0.6,
            )
            arrows.add(arrow)

        for i in range(len(stages)):
            self.play(
                FadeIn(boxes[i], shift=DOWN * 0.2),
                Write(labels[i]),
                run_time=0.5,
            )
            self.play(Create(arrows[i]), run_time=0.35)
        self.wait(0.5)

        example_title = Text(
            "Example: Pendulum Experiment", font_size=26, color=YELLOW
        )
        example_title.next_to(boxes, DOWN, buff=0.35)
        self.play(Write(example_title), run_time=0.9)
        self.wait(0.3)

        example_steps = VGroup(
            Text("Question: How does period depend on length?", font_size=17, color=GRAY),
            Text("Plan: Vary L, measure T, control mass and angle", font_size=17, color=GRAY),
            Text("Data: Collect (L, T) pairs with a stopwatch", font_size=17, color=GRAY),
            Text("Analyse: Linearise T^2 vs L, fit straight line", font_size=17, color=GRAY),
            Text("Conclude: T^2 prop to L, estimate g = 4pi^2/slope", font_size=17, color=GRAY),
            Text("Evaluate: % error vs 9.81, identify sources of error", font_size=17, color=GRAY),
        )
        example_steps.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        example_steps.next_to(example_title, DOWN, buff=0.2, aligned_edge=LEFT)

        for step in example_steps:
            self.play(Write(step), run_time=0.55)
        self.wait(0.4)

        g_true = 9.81
        lengths = np.linspace(0.2, 1.5, 10)
        periods = 2.0 * math.pi * np.sqrt(lengths / g_true)
        t_sq = periods**2
        rng = np.random.default_rng(42)
        t_sq_noisy = t_sq + rng.normal(0, 0.03, size=len(t_sq))

        fit = ReferenceLinearFit(x_data=lengths, y_data=t_sq_noisy)
        g_est = 4.0 * math.pi**2 / fit.slope()
        g_err = percent_error(g_est, g_true)

        result_box = Square(
            side_length=1.9, color=GREEN, fill_opacity=0.1, fill_color=GREEN
        )
        result_box.next_to(example_steps, DOWN, buff=0.25).align_to(
            example_steps, LEFT
        ).shift(RIGHT * 0.1)

        result_text = VGroup(
            MathTex(
                f"g_{{\\text{{est}}}} = {g_est:.3f}\\,\\text{{m/s}}^2",
                font_size=24, color=GREEN,
            ),
            MathTex(
                f"\\%\\ \\text{{error}} = {g_err:.2f}\\%",
                font_size=24,
                color=GREEN if g_err < 5 else RED,
            ),
            MathTex(
                f"R^2 = {fit.correlation_squared():.4f}",
                font_size=24, color=GRAY_B,
            ),
        )
        result_text.arrange(DOWN, buff=0.1)
        result_text.move_to(result_box)

        self.play(FadeIn(result_box), run_time=0.5)
        for line in result_text:
            self.play(Write(line), run_time=0.5)
        self.play(Indicate(result_box, color=GREEN, scale_factor=1.05), run_time=0.8)
        self.wait(0.3)

        final_msg = Text(
            "Evidence-based conclusion: data supports the model",
            font_size=22,
            color=YELLOW,
        )
        final_msg.next_to(result_box, RIGHT, buff=0.4)

        self.play(Write(final_msg), run_time=1.0)
        self.wait(1.5)


class ConclusionShort(Scene):
    """Shorter version of Conclusion for quick previews."""

    def construct(self) -> None:
        title = Text("Scientific Inquiry Loop", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.add(title)

        stages = ["Question", "Plan", "Data", "Analyse", "Conclude", "Evaluate"]
        colors = [BLUE_B, BLUE_D, GREEN_C, GREEN, ORANGE, RED_C]

        stage_objs = VGroup()
        for i, (label, color) in enumerate(zip(stages, colors)):
            angle = -math.pi / 2 + i * 2 * math.pi / len(stages)
            pos = np.array([math.cos(angle), math.sin(angle), 0]) * 2.5
            box = Square(side_length=1.3, color=color, fill_opacity=0.15, fill_color=color)
            box.move_to(pos)
            text = Text(label, font_size=18, color=color)
            text.move_to(pos)
            stage_objs.add(box, text)

        self.add(stage_objs)
        self.wait(3.0)