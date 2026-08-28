"""Hertzsprung-Russell diagram: log L vs T with stellar regions and blackbody inset.

Shows:
- Axes: log₁₀(L/L☉) vs T (reversed, decreasing to the right)
- Main-sequence band (grey shaded region)
- Red-giant region (orange shaded)
- White-dwarf region (blue shaded)
- Sample stars placed as labelled dots
- A blackbody-curve inset whose colour morphs as temperature sweeps

Animation pattern (proven — see repo convention)
---------------------------------------------------
The visible curves are ``always_redraw`` mobjects rebuilt every frame as
a single VMobject from the current simulation time.  The simulation time
is read from ``scene.time`` (the authoritative video time), NOT
accumulated from updater ``dt`` values.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    BLUE_D,
    Create,
    DOWN,
    GREEN,
    GREY,
    LEFT,
    Line,
    MathTex,
    Mobject,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    Write,
    YELLOW,
    always_redraw,
)

from physics_core.astrophysics.hr_diagram import (
    L_SUN,
    ReferenceHRDiagram,
    SAMPLE_STARS,
    T_SUN,
)


class HRDiagramScene(Scene):
    """Hertzsprung-Russell diagram: log L vs T with stellar regions and blackbody inset."""

    def construct(self) -> None:
        hr = ReferenceHRDiagram()

        # ------------------------------------------------------------------
        # Axes limits
        # ------------------------------------------------------------------
        logL_min: float = -4.0  # log10(L/L_sun)
        logL_max: float = 6.0
        T_min: float = 3000.0   # K
        T_max: float = 30000.0  # K

        # Manim coordinate mapping
        def to_mcoord(logL: float, T: float) -> np.ndarray:
            """Map (logL, T) to Manim coordinates. T axis is reversed."""
            x: float = (T_max - T) / (T_max - T_min) * 8.0 - 4.0
            y: float = (logL - logL_min) / (logL_max - logL_min) * 5.0 - 2.5
            return np.array([x, y, 0.0])

        # ------------------------------------------------------------------
        # Axes
        # ------------------------------------------------------------------
        x_axis = Line(
            to_mcoord(logL_min, T_min), to_mcoord(logL_min, T_max), color=BLUE_D
        )
        y_axis = Line(
            to_mcoord(logL_min, logL_min), to_mcoord(logL_max, logL_min), color=BLUE_D
        )

        # Ticks and labels for T axis (reversed)
        T_ticks: list[float] = [3000, 5000, 8000, 12000, 20000, 30000]
        tick_group = VMobject()
        for T_val in T_ticks:
            pos = to_mcoord(logL_min, T_val)
            tick = Line(pos + LEFT * 0.1, pos + RIGHT * 0.1, color=BLUE_D, stroke_width=1)
            tick_group.add(tick)
        # Labels
        T_label = MathTex("T \\; (\\text{K})", font_size=22, color=BLUE_D).next_to(
            to_mcoord(logL_min, T_min), DOWN, buff=0.3
        )
        logL_label = MathTex(
            "\\log_{10}(L / L_\\odot)", font_size=22, color=BLUE_D
        ).next_to(to_mcoord(logL_max, logL_min), RIGHT, buff=0.1)

        # T temperature labels
        T_labels = VGroup()
        for T_val in T_ticks:
            pos = to_mcoord(logL_min, T_val)
            lbl = MathTex(str(T_val), font_size=14, color=BLUE_D).next_to(pos, LEFT, buff=0.15)
            T_labels.add(lbl)

        # logL labels
        logL_vals: list[float] = [-4, -2, 0, 2, 4, 6]
        logL_labels = VGroup()
        for lv in logL_vals:
            pos = to_mcoord(lv, T_min)
            lbl = MathTex(str(lv), font_size=14, color=BLUE_D).next_to(pos, DOWN, buff=0.1)
            logL_labels.add(lbl)

        # ------------------------------------------------------------------
        # Stellar regions (static shaded bands)
        # ------------------------------------------------------------------
        # Main sequence: L ≈ L_sun * (T/T_sun)^4, with factor-of-10 spread
        ms_pts: list[np.ndarray] = []
        T_vals_ms: np.ndarray = np.linspace(T_min, T_max, 100)
        for T_val in T_vals_ms:
            logL_ms: float = math.log10(L_SUN * (T_val / T_SUN) ** 4 / L_SUN)
            logL_low: float = logL_ms - 1.0
            logL_high: float = logL_ms + 1.0
            ms_pts.append(to_mcoord(logL_low, T_val))
        for T_val in reversed(T_vals_ms):
            logL_ms = math.log10(L_SUN * (T_val / T_SUN) ** 4 / L_SUN)
            logL_high = logL_ms + 1.0
            ms_pts.append(to_mcoord(logL_high, T_val))
        ms_region = VMobject(color=GREY, fill_color=GREY, fill_opacity=0.15, stroke_width=0)
        ms_region.set_points_as_corners(ms_pts)

        # Giant region: high L, low T
        giant_pts: list[np.ndarray] = [
            to_mcoord(2.0, 3000.0),
            to_mcoord(6.0, 3000.0),
            to_mcoord(6.0, 6000.0),
            to_mcoord(2.0, 6000.0),
        ]
        giant_region = VMobject(
            color=ORANGE, fill_color=ORANGE, fill_opacity=0.15, stroke_width=0
        )
        giant_region.set_points_as_corners(giant_pts)

        # White dwarf region: low L, high T
        wd_pts: list[np.ndarray] = [
            to_mcoord(-4.0, 8000.0),
            to_mcoord(0.0, 8000.0),
            to_mcoord(0.0, 30000.0),
            to_mcoord(-4.0, 30000.0),
        ]
        wd_region = VMobject(
            color=BLUE, fill_color=BLUE, fill_opacity=0.15, stroke_width=0
        )
        wd_region.set_points_as_corners(wd_pts)

        # ------------------------------------------------------------------
        # Region labels
        # ------------------------------------------------------------------
        ms_label = MathTex(
            "\\text{Main Sequence}", font_size=18, color=GREY
        ).move_to(to_mcoord(0.0, 10000.0))
        giant_label = MathTex(
            "\\text{Giants}", font_size=18, color=ORANGE
        ).move_to(to_mcoord(4.0, 4000.0))
        wd_label = MathTex(
            "\\text{White Dwarfs}", font_size=18, color=BLUE
        ).move_to(to_mcoord(-2.0, 20000.0))

        # ------------------------------------------------------------------
        # Sample stars
        # ------------------------------------------------------------------
        star_dots = VGroup()
        star_names = VGroup()
        for name, L_rel, T, region in SAMPLE_STARS:
            logL_val: float = math.log10(L_rel)
            pos = to_mcoord(logL_val, T)
            color = (
                GREEN if region == "main sequence"
                else ORANGE if region == "giant"
                else BLUE
            )
            dot = Line(pos + DOWN * 0.06, pos + UP * 0.06, color=color, stroke_width=3)
            star_dots.add(dot)
            lbl = MathTex(
                "\\text{" + name.replace(" ", "\\,") + "}",
                font_size=14, color=color,
            ).next_to(pos, UP if T > 15000 else DOWN, buff=0.05)
            star_names.add(lbl)

        # ------------------------------------------------------------------
        # Blackbody-curve inset (time-varying)
        # ------------------------------------------------------------------
        t: list[float] = [0.0]

        # Inset axes
        inset_x = 3.5
        inset_y = 2.0
        inset_w = 2.5
        inset_h = 1.5

        inset_x_axis = Line(
            np.array([inset_x, inset_y, 0.0]),
            np.array([inset_x + inset_w, inset_y, 0.0]),
            color=GREY, stroke_width=1,
        )
        inset_y_axis = Line(
            np.array([inset_x, inset_y, 0.0]),
            np.array([inset_x, inset_y + inset_h, 0.0]),
            color=GREY, stroke_width=1,
        )
        inset_label = MathTex(
            "\\text{Blackbody spectrum}", font_size=12, color=GREY
        ).next_to(np.array([inset_x + inset_w / 2, inset_y + inset_h + 0.1, 0.0]), UP, buff=0.0)

        # Temperature sweeps from 3000 K to 20000 K over the animation
        def blackbody_curve_fn() -> VMobject:
            T_curve: float = 3000.0 + (20000.0 - 3000.0) * (0.5 + 0.5 * math.sin(t[0] * 0.5))
            wl: np.ndarray = np.linspace(100e-9, 2000e-9, 200)
            intensity: np.ndarray = hr.blackbody_curve(T_curve, wl)
            # Map to inset coordinates
            wl_min: float = 100e-9
            wl_max: float = 2000e-9
            pts: list[np.ndarray] = []
            for i in range(len(wl)):
                ix: float = inset_x + (wl[i] - wl_min) / (wl_max - wl_min) * inset_w
                iy: float = inset_y + intensity[i] * inset_h
                pts.append(np.array([ix, iy, 0.0]))
            vm = VMobject(stroke_width=2)
            # Colour based on temperature
            if T_curve < 5000:
                vm.set_color(RED)
            elif T_curve < 8000:
                vm.set_color(ORANGE)
            elif T_curve < 12000:
                vm.set_color(YELLOW)
            else:
                vm.set_color(BLUE)
            vm.set_points_as_corners(pts)
            return vm

        # Temperature display
        def temp_label_fn() -> MathTex:
            T_curve = 3000.0 + (20000.0 - 3000.0) * (0.5 + 0.5 * math.sin(t[0] * 0.5))
            return MathTex(
                f"T = {T_curve:.0f}\\,\\text{{K}}",
                font_size=14,
            ).next_to(np.array([inset_x + inset_w, inset_y + inset_h, 0.0]), UP + RIGHT, buff=0.0)

        bb_curve = always_redraw(blackbody_curve_fn)
        bb_temp = always_redraw(temp_label_fn)

        # ------------------------------------------------------------------
        # Physics driver
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # ------------------------------------------------------------------
        # Assemble and animate
        # ------------------------------------------------------------------
        # Phase 1: axes and regions
        self.play(Create(x_axis), Create(y_axis))
        self.play(Write(T_label), Write(logL_label))
        self.play(Write(T_labels), Write(logL_labels))
        self.play(Create(ms_region), Create(giant_region), Create(wd_region))
        self.play(Write(ms_label), Write(giant_label), Write(wd_label))
        self.wait(0.5)

        # Phase 2: sample stars
        self.play(Create(star_dots), Write(star_names))
        self.wait(0.5)

        # Phase 3: blackbody inset
        self.play(
            Create(inset_x_axis), Create(inset_y_axis), Write(inset_label),
        )
        self.add(bb_curve, bb_temp)
        self.add(driver)
        self.wait(8.0)