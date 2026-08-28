"""Scene C — Young's double-slit interference pattern.

Animates the double-slit interference pattern showing bright and dark
fringes on a screen.  The condition d sin(θ) = nλ is displayed, and
the fringe positions are computed analytically.

Physics driver
--------------
physics_core.waves.equations provides young_slit_angle for computing
fringe positions.

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
The animated rays (and their path-difference readout) are
``always_redraw`` mobjects rebuilt every frame from the current
simulation time.  The simulation time is read from ``scene.time`` (the
authoritative video time) via a driver mobject whose updater only does
``t[0] = self.time``; it is NEVER accumulated from updater ``dt``
values.  This pattern is required because submobjects appended to a
mounted VGroup from inside an updater are never re-rendered by the
ManimCE cairo renderer.  Static elements (screen, slits, fringes,
labels, formula) are built once and added directly.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    BLUE_D,
    DOWN,
    GRAY,
    GREEN,
    GREY_D,
    LEFT,
    Line,
    MathTex,
    Mobject,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    VMobject,
    YELLOW,
    always_redraw,
    Axes,
)

from physics_core.waves.equations import young_slit_angle, young_slit_intensity


class YoungSlit(Scene):
    """Young's double-slit interference pattern — bright/dark fringes."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        wavelength: float = 500e-9  # 500 nm
        slit_sep: float = 0.1e-3  # 0.1 mm
        screen_dist: float = 1.0  # 1 m
        n_orders: int = 5  # show orders -5 to +5

        # Fringe spacing: Δy = λD / d
        fringe_spacing = wavelength * screen_dist / slit_sep

        # Authoritative simulation time — read from scene (video) time.
        t: list[float] = [0.0]

        # ------------------------------------------------------------------
        # Scene layout
        # ------------------------------------------------------------------
        # Left: slits, Right: screen
        slit_x = -4.0
        screen_x = 4.0
        screen_half_height = 3.0

        # Slit positions (two dots)
        slit_upper = slit_x * RIGHT + 0.1 * UP
        slit_lower = slit_x * RIGHT + 0.1 * DOWN

        # Screen line
        screen_line = Line(
            screen_x * RIGHT + screen_half_height * UP,
            screen_x * RIGHT + screen_half_height * DOWN,
            color=GRAY, stroke_width=4,
        )

        # Labels
        slit_label = MathTex("\\text{Slits}", font_size=22).next_to(
            slit_x * RIGHT + 0.3 * UP, UP, buff=0.3
        )
        screen_label = MathTex("\\text{Screen}", font_size=22).next_to(
            screen_x * RIGHT + screen_half_height * UP, UP, buff=0.3
        )

        # Slit dots
        slit_dots = VGroup(
            Line(slit_upper - 0.05 * RIGHT, slit_upper + 0.05 * RIGHT, color=BLUE, stroke_width=4),
            Line(slit_lower - 0.05 * RIGHT, slit_lower + 0.05 * RIGHT, color=BLUE, stroke_width=4),
        )

        # ------------------------------------------------------------------
        # Fringe markers on screen (static)
        # ------------------------------------------------------------------
        fringes = VGroup()
        fringe_labels = VGroup()

        for n in range(-n_orders, n_orders + 1):
            # y position on screen: y = n * λD / d
            y_pos = n * fringe_spacing
            # Scale to scene coordinates
            y_scene = y_pos / (screen_half_height * 2) * screen_half_height * 2

            if abs(y_scene) > screen_half_height:
                continue

            fringe_pos = screen_x * RIGHT + y_scene * UP

            # Bright fringe (integer n)
            fringe_mark = Line(
                fringe_pos + 0.1 * LEFT,
                fringe_pos + 0.1 * RIGHT,
                color=YELLOW if n != 0 else GREEN,
                stroke_width=6,
            )
            fringes.add(fringe_mark)

            # Label
            label = Text(f"n={n}", font_size=16, color=YELLOW)
            label.next_to(fringe_pos, RIGHT, buff=0.1)
            fringe_labels.add(label)

        # Central maximum label
        central_label = Text("n=0", font_size=18, color=GREEN)
        central_label.next_to(screen_x * RIGHT, RIGHT, buff=0.1)

        # ------------------------------------------------------------------
        # Formula display (static)
        # ------------------------------------------------------------------
        formula = VGroup(
            MathTex("d \\sin(\\theta) = n \\lambda", font_size=28),
            MathTex(f"\\lambda = {wavelength*1e9:.0f} \\text{{ nm}}", font_size=22),
            MathTex(f"d = {slit_sep*1e3:.2f} \\text{{ mm}}", font_size=22),
            MathTex(f"D = {screen_dist:.1f} \\text{{ m}}", font_size=22),
            MathTex(
                f"\\Delta y = {fringe_spacing*1e3:.2f} \\text{{ mm}}",
                font_size=22,
            ),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + LEFT, buff=0.5)

        # ------------------------------------------------------------------
        # Animated rays from slits to a point sweeping across the screen
        # ------------------------------------------------------------------
        def sweep_target() -> np.ndarray:
            """Point on the screen that the rays aim at (sweeps bottom→top)."""
            sweep_fraction = (t[0] % 4.0) / 4.0  # 0 to 1 over 4 seconds
            sweep_y = -screen_half_height + sweep_fraction * 2 * screen_half_height
            return screen_x * RIGHT + sweep_y * UP

        rays = always_redraw(
            lambda: VGroup(
                Line(slit_upper, sweep_target(), color=BLUE_D,
                     stroke_width=1.5, stroke_opacity=0.4),
                Line(slit_lower, sweep_target(), color=ORANGE,
                     stroke_width=1.5, stroke_opacity=0.4),
            )
        )

        def path_difference_text() -> MathTex:
            target = sweep_target()
            path_upper = math.hypot(target[0] - slit_upper[0], target[1] - slit_upper[1])
            path_lower = math.hypot(target[0] - slit_lower[0], target[1] - slit_lower[1])
            path_diff = abs(path_upper - path_lower)
            label = MathTex(
                f"\\text{{Path diff}} = {path_diff*1e3:.2f} \\text{{ mm}}",
                font_size=18, color=YELLOW,
            )
            label.next_to(formula, DOWN, buff=0.3)
            return label

        path_label = always_redraw(path_difference_text)

        # ------------------------------------------------------------------
        # Intensity distribution panel (additive — keeps all existing content)
        # ------------------------------------------------------------------
        slit_width: float = 0.02e-3  # 0.02 mm slit width for diffraction envelope

        intensity_axes = Axes(
            x_range=[-screen_half_height, screen_half_height, 1],
            y_range=[0, 1.1, 0.2],
            x_length=3.0,
            y_length=2.0,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 12,
            },
        )
        intensity_axes.to_corner(DOWN + RIGHT, buff=0.5)

        intensity_title = MathTex(
            "\\text{Intensity } I(y)", font_size=18,
        ).next_to(intensity_axes, UP, buff=0.1)

        def intensity_curve() -> VMobject:
            """Build the I(y) curve as a single VMobject."""
            n_pts = 200
            ys = np.linspace(-screen_half_height, screen_half_height, n_pts)
            # Convert scene y to physical y: scale factor
            phys_scale = screen_half_height * 2.0  # maps scene coords to physical
            intensities = [
                young_slit_intensity(
                    y * fringe_spacing / phys_scale,
                    slit_separation=slit_sep,
                    slit_width=slit_width,
                    screen_distance=screen_dist,
                    wavelength=wavelength,
                )
                for y in ys
            ]
            pts = [
                intensity_axes.c2p(float(y), float(I))
                for y, I in zip(ys, intensities)
            ]
            vm = VMobject(color=YELLOW, stroke_width=2)
            vm.set_points_as_corners(pts)
            return vm

        intensity_curve_mob = always_redraw(intensity_curve)

        # Maxima/minima labels (static — computed once)
        max_min_labels = VGroup()
        for n in range(-n_orders, n_orders + 1):
            y_pos = n * fringe_spacing
            y_scene = y_pos / (screen_half_height * 2) * screen_half_height * 2
            if abs(y_scene) > screen_half_height:
                continue
            I_val = young_slit_intensity(
                y_pos,
                slit_separation=slit_sep,
                slit_width=slit_width,
                screen_distance=screen_dist,
                wavelength=wavelength,
            )
            if I_val > 0.5:
                label = Text(
                    f"max n={n}", font_size=10, color=YELLOW,
                )
            else:
                label = Text(
                    f"min n={n}", font_size=10, color=GRAY,
                )
            label.next_to(
                intensity_axes.c2p(float(y_scene), float(I_val)),
                UP if I_val > 0.5 else DOWN,
                buff=0.05,
            )
            max_min_labels.add(label)

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
        self.add(formula)
        self.add(slit_label, screen_label)
        self.add(slit_dots, screen_line)
        self.add(fringes, fringe_labels, central_label)
        self.add(rays, path_label)
        self.add(intensity_axes, intensity_title, intensity_curve_mob, max_min_labels)
        self.add(driver)

        self.wait(8.0)
