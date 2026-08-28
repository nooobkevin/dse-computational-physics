"""Scene — Quantum superposition: |ψ⟩ = a|0⟩ + b|1⟩ with measurement.

Animate a qubit in a superposition state.  Probability weights |a|² and
|b|² are shown as bars.  A measurement "click" collapses the state to
|0⟩ or |1⟩ with the correct probability.  Repeated measurements build a
histogram showing the expected distribution.

Physics driver
--------------
Built-in random module (seeded for deterministic renders).

Animation pattern (IMPORTANT — see repo convention)
----------------------------------------------------
The visible elements are ``always_redraw`` mobjects rebuilt every frame
from the current simulation time.  The simulation time is read from
``scene.time`` via a driver mobject.
"""

from __future__ import annotations

import math
import random

import numpy as np
from manim import (
    BLUE,
    BLUE_D,
    DOWN,
    GRAY,
    GREEN,
    LEFT,
    Line,
    MathTex,
    Mobject,
    ORANGE,
    Rectangle,
    RED,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    VMobject,
    YELLOW,
    always_redraw,
)


class SuperpositionState(Scene):
    """Quantum superposition: |ψ⟩ = a|0⟩ + b|1⟩ with measurement."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        random.seed(42)  # deterministic render

        # Superposition amplitudes (normalised)
        a = math.sqrt(0.7)  # amplitude for |0⟩
        b = math.sqrt(0.3)  # amplitude for |1⟩
        prob_0 = a * a  # |a|² = 0.7
        prob_1 = b * b  # |b|² = 0.3

        # Measurement history
        max_measurements = 30
        measurements: list[int] = []  # 0 or 1
        next_measure_time: list[float] = [2.0]  # first measurement at t=2s
        measure_interval: float = 1.5  # seconds between measurements

        # Authoritative simulation time
        t: list[float] = [0.0]
        total_time: float = 12.0

        # ------------------------------------------------------------------
        # State vector display
        # ------------------------------------------------------------------
        state_tex = MathTex(
            "|\\psi\\rangle = a|0\\rangle + b|1\\rangle",
            font_size=28,
            color=GRAY,
        )
        state_tex.to_corner(UP + LEFT, buff=0.5)

        # Amplitude values
        a_tex = always_redraw(
            lambda: MathTex(
                f"a = {a:.3f},\\quad b = {b:.3f}",
                font_size=20,
                color=GRAY,
            ).next_to(state_tex, DOWN, buff=0.2, aligned_edge=LEFT)
        )

        norm_tex = always_redraw(
            lambda: MathTex(
                f"|a|^2 = {prob_0:.2f},\\quad |b|^2 = {prob_1:.2f}",
                font_size=20,
                color=GRAY,
            ).next_to(a_tex, DOWN, buff=0.1, aligned_edge=LEFT)
        )

        # ------------------------------------------------------------------
        # Probability bars
        # ------------------------------------------------------------------
        bar_center = UP * 1.5
        bar_width = 1.5
        bar_height_max = 2.0

        def prob_bars() -> VGroup:
            group = VGroup()
            # Bar for |0⟩
            h0 = prob_0 * bar_height_max
            bar0 = Rectangle(
                width=bar_width,
                height=h0,
                color=BLUE,
                fill_opacity=0.6,
            )
            bar0.move_to(bar_center + LEFT * 1.5, DOWN + LEFT)
            bar0.shift(UP * h0 / 2.0)
            label0 = MathTex("|0\\rangle", font_size=20, color=BLUE)
            label0.next_to(bar0, DOWN, buff=0.1)
            prob0_label = MathTex(f"{prob_0:.2f}", font_size=18, color=BLUE)
            prob0_label.next_to(bar0, UP, buff=0.05)
            group.add(bar0, label0, prob0_label)

            # Bar for |1⟩
            h1 = prob_1 * bar_height_max
            bar1 = Rectangle(
                width=bar_width,
                height=h1,
                color=ORANGE,
                fill_opacity=0.6,
            )
            bar1.move_to(bar_center + RIGHT * 1.5, DOWN + RIGHT)
            bar1.shift(UP * h1 / 2.0)
            label1 = MathTex("|1\\rangle", font_size=20, color=ORANGE)
            label1.next_to(bar1, DOWN, buff=0.1)
            prob1_label = MathTex(f"{prob_1:.2f}", font_size=18, color=ORANGE)
            prob1_label.next_to(bar1, UP, buff=0.05)
            group.add(bar1, label1, prob1_label)

            return group

        bars = always_redraw(prob_bars)

        # ------------------------------------------------------------------
        # Measurement result display
        # ------------------------------------------------------------------
        result_tex = always_redraw(
            lambda: self._build_result_text(measurements, prob_0, prob_1)
        )

        # ------------------------------------------------------------------
        # Histogram of measurement outcomes
        # ------------------------------------------------------------------
        hist_center = DOWN * 1.5
        hist_width = 2.0
        hist_height = 1.5

        def histogram() -> VGroup:
            group = VGroup()
            total = len(measurements)
            if total == 0:
                # Show empty histogram
                frame0 = Rectangle(
                    width=hist_width,
                    height=hist_height,
                    color=GRAY,
                    fill_opacity=0.0,
                    stroke_width=1,
                )
                frame0.move_to(hist_center + LEFT * 1.5, DOWN + LEFT)
                frame1 = Rectangle(
                    width=hist_width,
                    height=hist_height,
                    color=GRAY,
                    fill_opacity=0.0,
                    stroke_width=1,
                )
                frame1.move_to(hist_center + RIGHT * 1.5, DOWN + RIGHT)
                group.add(frame0, frame1)
                return group

            count_0 = measurements.count(0)
            count_1 = measurements.count(1)
            max_count = max(count_0, count_1, 1)

            # Bar for |0⟩ outcomes
            h0 = (count_0 / max_count) * hist_height
            bar0 = Rectangle(
                width=hist_width * 0.7,
                height=h0,
                color=BLUE,
                fill_opacity=0.6,
            )
            bar0.move_to(hist_center + LEFT * 1.5, DOWN + LEFT)
            bar0.shift(UP * h0 / 2.0)
            label0 = MathTex(f"|0\\rangle: {count_0}", font_size=16, color=BLUE)
            label0.next_to(bar0, DOWN, buff=0.1)
            group.add(bar0, label0)

            # Bar for |1⟩ outcomes
            h1 = (count_1 / max_count) * hist_height
            bar1 = Rectangle(
                width=hist_width * 0.7,
                height=h1,
                color=ORANGE,
                fill_opacity=0.6,
            )
            bar1.move_to(hist_center + RIGHT * 1.5, DOWN + RIGHT)
            bar1.shift(UP * h1 / 2.0)
            label1 = MathTex(f"|1\\rangle: {count_1}", font_size=16, color=ORANGE)
            label1.next_to(bar1, DOWN, buff=0.1)
            group.add(bar1, label1)

            return group

        hist = always_redraw(histogram)

        # ------------------------------------------------------------------
        # Physics driver — sets authoritative time + performs measurements
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time
            # Perform measurements at scheduled times
            while t[0] >= next_measure_time[0] and len(measurements) < max_measurements:
                outcome = 0 if random.random() < prob_0 else 1
                measurements.append(outcome)
                next_measure_time[0] += measure_interval

        driver = Mobject()
        driver.add_updater(updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        self.add(state_tex, a_tex, norm_tex)
        self.add(bars)
        self.add(result_tex)
        self.add(hist)
        self.add(driver)

        self.wait(total_time)

    # ------------------------------------------------------------------
    # Helper: build measurement result text
    # ------------------------------------------------------------------
    def _build_result_text(
        self, measurements: list[int], prob_0: float, prob_1: float
    ) -> VGroup:
        group = VGroup()
        title = Text("Measurement Results", font_size=18, color=GRAY)
        title.to_corner(UP + RIGHT, buff=0.5)
        group.add(title)

        if not measurements:
            latest = Text("(waiting...)", font_size=16, color=GRAY)
            latest.next_to(title, DOWN, buff=0.2, aligned_edge=LEFT)
            group.add(latest)
            return group

        # Show the last few outcomes
        recent = measurements[-min(8, len(measurements)):]
        outcome_str = " ".join("|0⟩" if r == 0 else "|1⟩" for r in recent)
        outcome_tex = MathTex(
            outcome_str.replace("|0⟩", "|0\\rangle").replace("|1⟩", "|1\\rangle"),
            font_size=20,
            color=GRAY,
        )
        outcome_tex.next_to(title, DOWN, buff=0.2, aligned_edge=LEFT)
        group.add(outcome_tex)

        # Statistics
        total = len(measurements)
        count_0 = measurements.count(0)
        count_1 = measurements.count(1)
        stats = Text(
            f"Total: {total}  |  |0⟩: {count_0} ({count_0/total*100:.0f}%)  "
            f"|  |1⟩: {count_1} ({count_1/total*100:.0f}%)",
            font_size=16,
            color=GRAY,
        )
        stats.next_to(outcome_tex, DOWN, buff=0.15, aligned_edge=LEFT)
        group.add(stats)

        return group