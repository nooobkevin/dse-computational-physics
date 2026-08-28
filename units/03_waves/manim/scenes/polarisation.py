"""Scene D — Polarisation of transverse waves (Annex 3 enrichment).

Animates a transverse wave passing through a polariser slit at angle θ.
The transmitted amplitude is A cos(θ), and Malus's law I = I₀ cos²(θ)
is shown live as the angle changes.  A second crossed polariser
demonstrates extinction.

Physics driver
--------------
physics_core.waves.equations.malus_law provides the intensity calculation.

Animation pattern (IMPORTANT — see repo convention)
--------------------------------------------------
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
    UP,
    VGroup,
    VMobject,
    YELLOW,
    always_redraw,
)

from physics_core.waves.equations import malus_law


class Polarisation(Scene):
    """Transverse wave passing through a polariser — Malus's law."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        A: float = 1.5  # incident amplitude
        I0: float = A**2  # incident intensity
        lam: float = 4.0
        f: float = 0.5
        k: float = 2.0 * math.pi / lam
        omega: float = 2.0 * math.pi * f
        total_time: float = 12.0

        # Authoritative simulation time
        t: list[float] = [0.0]

        # Polariser angle (rad) — sweeps from 0 to π over the animation
        def theta() -> float:
            return (t[0] / total_time) * math.pi

        # ------------------------------------------------------------------
        # Axes for the wave display (left side)
        # ------------------------------------------------------------------
        wave_axes = VGroup(
            Line(LEFT * 4.5, RIGHT * 4.5, color=GREY_D, stroke_width=1),
            Line(UP * 2.5, DOWN * 2.5, color=GREY_D, stroke_width=1),
        )
        wave_axes.move_to(LEFT * 2.5 + DOWN * 0.5)

        # ------------------------------------------------------------------
        # Polariser slit visual (static)
        # ------------------------------------------------------------------
        # A vertical slit at x=0 that rotates with theta
        polariser_center = LEFT * 2.5 + DOWN * 0.5

        def polariser_slit() -> VMobject:
            th = theta()
            half_len = 2.5
            dx = half_len * math.sin(th)
            dy = half_len * math.cos(th)
            slit = VMobject(color=GRAY, stroke_width=3)
            slit.set_points_as_corners([
                polariser_center + dx * LEFT + dy * DOWN,
                polariser_center + dx * RIGHT + dy * UP,
            ])
            return slit

        slit_mob = always_redraw(polariser_slit)

        # ------------------------------------------------------------------
        # Incident wave (before polariser) — always vertical polarisation
        # ------------------------------------------------------------------
        def incident_wave() -> VMobject:
            xs = np.linspace(-4.5, 0.0, 100)
            ys = A * np.sin(k * xs - omega * t[0])
            pts = [
                polariser_center + float(x) * RIGHT + float(y) * UP
                for x, y in zip(xs, ys)
            ]
            vm = VMobject(color=BLUE, stroke_width=2)
            vm.set_points_as_corners(pts)
            return vm

        incident = always_redraw(incident_wave)

        # ------------------------------------------------------------------
        # Transmitted wave (after polariser) — amplitude = A cos(θ)
        # ------------------------------------------------------------------
        def transmitted_wave() -> VMobject:
            th = theta()
            A_trans = A * abs(math.cos(th))
            xs = np.linspace(0.0, 4.5, 100)
            ys = A_trans * np.sin(k * xs - omega * t[0])
            pts = [
                polariser_center + float(x) * RIGHT + float(y) * UP
                for x, y in zip(xs, ys)
            ]
            vm = VMobject(color=GREEN, stroke_width=2)
            vm.set_points_as_corners(pts)
            return vm

        transmitted = always_redraw(transmitted_wave)

        # ------------------------------------------------------------------
        # Second polariser (crossed) — appears later in the animation
        # ------------------------------------------------------------------
        def second_slit() -> VMobject:
            # Second polariser at x=3.0, rotated 90° from first
            th = theta() + math.pi / 2.0
            center = polariser_center + 3.0 * RIGHT
            half_len = 2.5
            dx = half_len * math.sin(th)
            dy = half_len * math.cos(th)
            slit = VMobject(color=RED, stroke_width=3)
            slit.set_points_as_corners([
                center + dx * LEFT + dy * DOWN,
                center + dx * RIGHT + dy * UP,
            ])
            return slit

        second_slit_mob = always_redraw(second_slit)

        # ------------------------------------------------------------------
        # Wave after second polariser
        # ------------------------------------------------------------------
        def after_second() -> VMobject:
            th = theta()
            # First polariser: A₁ = A cos(θ)
            A1 = A * abs(math.cos(th))
            # Second polariser at θ + 90°: A₂ = A₁ cos(θ + 90°) = A₁ sin(θ)
            A2 = A1 * abs(math.cos(th + math.pi / 2.0))
            xs = np.linspace(3.0, 4.5, 50)
            ys = A2 * np.sin(k * xs - omega * t[0])
            center = polariser_center + 3.0 * RIGHT
            pts = [
                center + float(x - 3.0) * RIGHT + float(y) * UP
                for x, y in zip(xs, ys)
            ]
            vm = VMobject(color=RED, stroke_width=2)
            vm.set_points_as_corners(pts)
            return vm

        after_second_mob = always_redraw(after_second)

        # ------------------------------------------------------------------
        # Labels and formula display (right side)
        # ------------------------------------------------------------------
        title = MathTex(
            "\\text{Polarisation — Malus's Law}",
            font_size=28,
        ).to_corner(UP + RIGHT, buff=0.5)

        def formula_group() -> VGroup:
            th = theta()
            I_trans = malus_law(I0, th)
            A_trans = A * abs(math.cos(th))
            # Second polariser
            I_after_second = malus_law(I_trans, math.pi / 2.0)

            lines = VGroup(
                MathTex(f"\\theta = {math.degrees(th):.0f}^\\circ", font_size=22),
                MathTex(
                    f"A_{{\\text{{trans}}}} = A \\cos(\\theta) = {A_trans:.2f}",
                    font_size=22,
                ),
                MathTex(
                    f"I_{{\\text{{trans}}}} = I_0 \\cos^2(\\theta) = {I_trans:.2f}",
                    font_size=22,
                    color=GREEN,
                ),
                MathTex(
                    f"I_{{\\text{{crossed}}}} = I_{{\\text{{trans}}}} \\cos^2(90^\\circ)"
                    f" = {I_after_second:.2f}",
                    font_size=20,
                    color=RED,
                ),
            )
            lines.arrange(DOWN, aligned_edge=LEFT)
            lines.next_to(title, DOWN, buff=0.5, aligned_edge=LEFT)
            return lines

        formulas = always_redraw(formula_group)

        # ------------------------------------------------------------------
        # Labels
        # ------------------------------------------------------------------
        incident_label = MathTex(
            "\\text{Incident (vertical)}", color=BLUE, font_size=18
        ).next_to(polariser_center + LEFT * 2.0 + UP * 2.5, UP)

        transmitted_label = MathTex(
            "\\text{Transmitted}", color=GREEN, font_size=18
        ).next_to(polariser_center + RIGHT * 2.0 + UP * 2.5, UP)

        polariser_label = MathTex(
            "\\text{Polariser}", color=GRAY, font_size=18
        ).next_to(polariser_center + UP * 3.0, UP)

        second_label = MathTex(
            "\\text{Crossed}", color=RED, font_size=18
        ).next_to(polariser_center + RIGHT * 3.0 + UP * 3.0, UP)

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
        self.add(title)
        self.add(wave_axes)
        self.add(slit_mob, second_slit_mob)
        self.add(incident, transmitted, after_second_mob)
        self.add(incident_label, transmitted_label, polariser_label, second_label)
        self.add(formulas)
        self.add(driver)

        self.wait(total_time)