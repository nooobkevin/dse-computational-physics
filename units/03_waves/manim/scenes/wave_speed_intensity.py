"""Scene B — Wave speed and intensity relationships.

Shows the relationship between wave speed, frequency, and wavelength
(v = fλ) and the intensity-amplitude relationship (I ∝ A²).  Three
traveling waves with different amplitudes are displayed side by side,
and a bar chart shows the corresponding intensities.

Physics driver
--------------
ReferenceWaveSim from physics_core.waves.wave_sim provides the analytical
traveling wave solution.  physics_core.waves.equations provides the
intensity helper.

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
The visible wave profiles are ``always_redraw`` mobjects rebuilt every
frame as a single VMobject each from the current simulation time.  The
simulation time is read from ``scene.time`` (the authoritative video
time) via a driver mobject whose updater only does ``t[0] =
self.time``; it is NEVER accumulated from updater ``dt`` values.  This
pattern is required because submobjects appended to a mounted VGroup
from inside an updater are never re-rendered by the ManimCE cairo
renderer.  Static elements (axes, labels, legend, intensity bars) are
built once and added directly.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Axes,
    BLUE,
    DOWN,
    GREEN,
    GREY_D,
    LEFT,
    Line,
    MathTex,
    Mobject,
    RED,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    always_redraw,
)

from physics_core.waves.equations import intensity
from physics_core.waves.wave_sim import ReferenceWaveSim


class WaveSpeedIntensity(Scene):
    """Wave speed formula v = fλ and intensity I ∝ A²."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters — three waves with different amplitudes
        # ------------------------------------------------------------------
        amplitudes = [0.5, 1.0, 1.5]
        lam = 4.0
        f = 0.5
        sims = [
            ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f, L=12.0, nx=200)
            for A in amplitudes
        ]
        total_time: float = 6.0

        # Authoritative simulation time — read from scene (video) time.
        t: list[float] = [0.0]
        colors = [BLUE, GREEN, RED]

        # ------------------------------------------------------------------
        # Left panel — three traveling waves
        # ------------------------------------------------------------------
        wave_axes = Axes(
            x_range=[0, sims[0].L, 2],
            y_range=[-2.0, 2.0, 1],
            x_length=7,
            y_length=3.5,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 18,
            },
        )
        wave_axes.to_corner(UP + LEFT, buff=0.5)

        wave_title = MathTex(
            "\\text{Traveling waves: } y = A \\sin(kx - \\omega t)",
            font_size=22,
        ).next_to(wave_axes, UP, buff=0.1)

        # Legend
        wave_legend = VGroup(
            MathTex(f"\\text{{A = {amplitudes[0]:.1f}}}", color=BLUE, font_size=18),
            MathTex(f"\\text{{A = {amplitudes[1]:.1f}}}", color=GREEN, font_size=18),
            MathTex(f"\\text{{A = {amplitudes[2]:.1f}}}", color=RED, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(wave_axes, RIGHT, buff=0.3)

        # Wave curves — always_redraw, one single VMobject per wave
        def wave_curve(sim: ReferenceWaveSim, color) -> VMobject:
            ys = sim.field(sim.x, t[0])
            pts = [wave_axes.c2p(float(x), float(y)) for x, y in zip(sim.x, ys)]
            vm = VMobject(color=color, stroke_width=2)
            vm.set_points_as_corners(pts)
            return vm

        traces = [
            always_redraw(lambda s=s, c=colors[i]: wave_curve(s, c))
            for i, s in enumerate(sims)
        ]

        # ------------------------------------------------------------------
        # Right panel — intensity bar chart (static: I depends only on A)
        # ------------------------------------------------------------------
        bar_axes = Axes(
            x_range=[-0.5, 2.5, 1],
            y_range=[0, 2.8, 0.5],
            x_length=3.5,
            y_length=3.5,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 16,
            },
        )
        bar_axes.next_to(wave_axes, DOWN, buff=0.8, aligned_edge=LEFT)
        bar_axes.shift(RIGHT * 1.5)

        bar_title = MathTex(
            "\\text{Intensity } I \\propto A^2",
            font_size=22,
        ).next_to(bar_axes, UP, buff=0.1)

        # Bar labels
        bar_labels = VGroup()
        for i, A in enumerate(amplitudes):
            lbl = MathTex(f"A={A:.1f}", font_size=16)
            lbl.next_to(bar_axes.c2p(float(i), 0), DOWN, buff=0.15)
            bar_labels.add(lbl)

        # Bars — static, built once
        bars = VGroup()
        max_I = intensity(max(amplitudes))
        for i, A in enumerate(amplitudes):
            I_val = intensity(A)
            bar_height = I_val / max_I * 2.5  # scale to fit axes
            bar = Line(
                bar_axes.c2p(float(i), 0),
                bar_axes.c2p(float(i), bar_height),
                color=colors[i], stroke_width=40,
            )
            bars.add(bar)

            # Intensity value label
            val_label = MathTex(f"{I_val:.2f}", font_size=14, color=colors[i])
            val_label.next_to(bar_axes.c2p(float(i), bar_height), UP, buff=0.1)
            bars.add(val_label)

        # ------------------------------------------------------------------
        # Physics driver — sets authoritative time from the scene clock
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        self.add(wave_axes, wave_title, wave_legend)
        self.add(bar_axes, bar_title, bar_labels)
        self.add(bars)
        for tr in traces:
            self.add(tr)
        self.add(driver)

        self.wait(total_time)
