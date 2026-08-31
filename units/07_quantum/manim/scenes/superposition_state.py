"""Scene — Quantum superposition: |ψ⟩ = a|0⟩ + b|1⟩ with measurement.

Animate a qubit in a superposition state.  Probability weights |a|² and
|b|² are shown as bars.  A measurement "click" collapses the state to
|0⟩ or |1⟩ with the correct probability.  Repeated measurements build a
histogram showing the expected distribution.  A probability-wave panel
shows |ψ(x,t)|² of the superposition oscillating continuously, with a
scanning measurement cursor sweeping across it.

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
    ORIGIN,
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
        bar_center = UP * 2.3
        bar_width = 1.5
        bar_height_max = 1.2

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
            bar0.move_to(bar_center + LEFT * 1.5)
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
            bar1.move_to(bar_center + RIGHT * 1.5)
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
        hist_center = DOWN * 2.3
        hist_width = 2.0
        hist_height = 1.0

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
        # Probability wave panel — |ψ(x,t)|² of the superposition state
        # ------------------------------------------------------------------
        # Basis states of a 1-D well: ψ₀ = √2 sin(πx), ψ₁ = √2 sin(2πx).
        # Time evolution of |ψ⟩ = a|0⟩ + b|1⟩ gives
        #   |ψ(x,t)|² = a²ψ₀² + b²ψ₁² + 2ab ψ₀ψ₁ cos(ωt),
        # which oscillates at the Bohr frequency (shown schematically).
        wave_center = UP * 0.8
        wave_width = 9.0
        wave_height = 1.4
        wave_n = 200
        wave_omega = 2.0 * math.pi * 1.0  # ~1 oscillation per second

        wave_title = MathTex(
            "|\\psi(x,t)|^2 \\text{ — superposition oscillates}",
            font_size=16,
            color=GREEN,
        )
        wave_title.move_to(wave_center + UP * (wave_height / 2.0 + 0.2))

        wave_baseline = Line(
            wave_center + LEFT * (wave_width / 2.0),
            wave_center + RIGHT * (wave_width / 2.0),
            color=GRAY,
            stroke_width=1,
        )

        def wave_curve() -> VMobject:
            xs = np.linspace(0.0, 1.0, wave_n)
            psi0 = math.sqrt(2.0) * np.sin(math.pi * xs)
            psi1 = math.sqrt(2.0) * np.sin(2.0 * math.pi * xs)
            phase = wave_omega * t[0]
            prob = (
                prob_0 * psi0**2
                + prob_1 * psi1**2
                + 2.0 * a * b * psi0 * psi1 * math.cos(phase)
            )
            peak = float(prob.max())
            ys = wave_center[1] + (prob / peak) * (wave_height / 2.0)
            top_pts = [
                np.array(
                    [
                        wave_center[0] - wave_width / 2.0 + x * wave_width,
                        float(y),
                        0.0,
                    ]
                )
                for x, y in zip(xs, ys)
            ]
            bottom_pts = [
                np.array(
                    [
                        wave_center[0] - wave_width / 2.0 + x * wave_width,
                        wave_center[1] - wave_height / 2.0,
                        0.0,
                    ]
                )
                for x in xs[::-1]
            ]
            vm = VMobject(color=GREEN, fill_color=GREEN, fill_opacity=0.35, stroke_width=3)
            vm.set_points_as_corners(top_pts + bottom_pts)
            return vm

        wave = always_redraw(wave_curve)

        # ------------------------------------------------------------------
        # Scanning measurement cursor — sweeps across the wave panel
        # ------------------------------------------------------------------
        scan_period = 2.5  # seconds per full sweep

        def scan_cursor() -> Line:
            frac = (t[0] % scan_period) / scan_period
            x = wave_center[0] - wave_width / 2.0 + frac * wave_width
            return Line(
                np.array([x, wave_center[1] - wave_height / 2.0 - 0.1, 0.0]),
                np.array([x, wave_center[1] + wave_height / 2.0 + 0.1, 0.0]),
                color=YELLOW,
                stroke_width=2,
            )

        scan = always_redraw(scan_cursor)

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
        self.add(wave_title, wave_baseline, wave, scan)
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