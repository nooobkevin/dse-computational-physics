"""Spacetime diagram: light cones, worldlines, and relativity of simultaneity.

Shows a ct-x Minkowski diagram with:
- Light cones at 45 degrees (x = ±ct)
- Worldline of a stationary observer (vertical, x = 0)
- Worldline of a moving observer (v = 0.6c, tilted)
- Two events A and B simultaneous in the rest frame
- Lines of constant t (rest frame) and constant t' (moving frame)
  cutting the two events differently — relativity of simultaneity.

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
    FadeOut,
    GREEN,
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

from physics_core.astrophysics.relativity import ReferenceRelativityEngine


class SpacetimeDiagram(Scene):
    """ct-x Minkowski diagram with light cones, worldlines, and relativity of simultaneity."""

    def construct(self) -> None:
        re = ReferenceRelativityEngine()
        v: float = 0.6 * re.c  # moving observer speed
        gamma: float = re.lorentz_factor(v)

        # ------------------------------------------------------------------
        # Axes limits
        # ------------------------------------------------------------------
        ct_max: float = 5.0  # light-seconds
        x_max: float = 5.0   # light-seconds

        # Scale: 1 unit = 1 light-second
        # Manim coordinates: -5 to +5 in x, -3 to +5 in ct
        def to_mcoord(x_ls: float, ct_ls: float) -> np.ndarray:
            """Map (x, ct) in light-seconds to Manim coordinates."""
            return np.array([x_ls / x_max * 4.0, ct_ls / ct_max * 4.0 - 1.0, 0.0])

        # ------------------------------------------------------------------
        # Axes
        # ------------------------------------------------------------------
        x_axis = Line(
            to_mcoord(-x_max, 0.0), to_mcoord(x_max, 0.0), color=BLUE_D
        )
        ct_axis = Line(
            to_mcoord(0.0, -0.5), to_mcoord(0.0, ct_max), color=BLUE_D
        )

        x_label = MathTex("x", font_size=24, color=BLUE_D).next_to(
            to_mcoord(x_max, 0.0), RIGHT, buff=0.1
        )
        ct_label = MathTex("ct", font_size=24, color=BLUE_D).next_to(
            to_mcoord(0.0, ct_max), UP, buff=0.1
        )

        # ------------------------------------------------------------------
        # Light cones (static)
        # ------------------------------------------------------------------
        light_cone_right = Line(
            to_mcoord(0.0, 0.0), to_mcoord(x_max, x_max), color=YELLOW, stroke_width=2
        )
        light_cone_left = Line(
            to_mcoord(0.0, 0.0), to_mcoord(-x_max, x_max), color=YELLOW, stroke_width=2
        )
        light_label = MathTex(
            "x = ct", font_size=16, color=YELLOW
        ).next_to(to_mcoord(x_max * 0.7, x_max * 0.7), RIGHT + UP, buff=0.05)

        # ------------------------------------------------------------------
        # Worldlines (static)
        # ------------------------------------------------------------------
        # Rest observer: x = 0 (vertical)
        rest_worldline = Line(
            to_mcoord(0.0, 0.0), to_mcoord(0.0, ct_max), color=GREEN, stroke_width=3
        )
        rest_label = MathTex(
            "\\text{Rest}", font_size=18, color=GREEN
        ).next_to(to_mcoord(0.0, ct_max), UP, buff=0.05)

        # Moving observer: x = v * t = β * ct, so x/ct = β = 0.6
        moving_worldline = Line(
            to_mcoord(0.0, 0.0),
            to_mcoord(v / re.c * ct_max, ct_max),
            color=ORANGE,
            stroke_width=3,
        )
        moving_label = MathTex(
            "v = 0.6c", font_size=18, color=ORANGE
        ).next_to(to_mcoord(v / re.c * ct_max * 0.8, ct_max * 0.8), LEFT, buff=0.05)

        # ------------------------------------------------------------------
        # Events A and B (static)
        # ------------------------------------------------------------------
        # Two events simultaneous in rest frame at t=0, x = ±1.5 ls
        event_A_pos = to_mcoord(-1.5, 0.0)
        event_B_pos = to_mcoord(1.5, 0.0)

        event_A_dot = Line(
            event_A_pos + DOWN * 0.08, event_A_pos + UP * 0.08, color=RED, stroke_width=3
        )
        event_B_dot = Line(
            event_B_pos + DOWN * 0.08, event_B_pos + UP * 0.08, color=RED, stroke_width=3
        )
        event_A_label = MathTex("A", font_size=20, color=RED).next_to(
            event_A_pos, DOWN + LEFT, buff=0.1
        )
        event_B_label = MathTex("B", font_size=20, color=RED).next_to(
            event_B_pos, DOWN + RIGHT, buff=0.1
        )

        # ------------------------------------------------------------------
        # Time-varying: simultaneity lines
        # ------------------------------------------------------------------
        t: list[float] = [0.0]

        # Rest-frame line of constant t (horizontal through A and B)
        def rest_simul_line() -> VMobject:
            ct_val: float = t[0] * 0.5  # sweep slowly
            p_left = to_mcoord(-x_max, ct_val)
            p_right = to_mcoord(x_max, ct_val)
            vm = VMobject(color=GREEN, stroke_width=2, stroke_opacity=0.6)
            vm.set_points_as_corners([p_left, p_right])
            return vm

        # Moving-frame line of constant t' (tilted)
        # In the moving frame, t' = γ(t - βx/c).  For constant t' = 0:
        # t = βx/c → ct = βx
        def moving_simul_line() -> VMobject:
            ct_val: float = t[0] * 0.5
            # Line of constant t' in moving frame: ct = βx + ct'_offset
            # We want it to pass through the origin at t=0 and sweep
            beta: float = v / re.c
            offset: float = ct_val
            x_left: float = -x_max
            ct_left: float = beta * x_left + offset
            x_right: float = x_max
            ct_right: float = beta * x_right + offset
            # Clamp to visible range
            ct_left = max(ct_left, -0.5)
            ct_right = max(ct_right, -0.5)
            ct_left = min(ct_left, ct_max)
            ct_right = min(ct_right, ct_max)
            p_left = to_mcoord(x_left if ct_left > -0.5 else (offset - ct_val) / beta, ct_left)
            p_right = to_mcoord(x_right if ct_right > -0.5 else (offset - ct_val) / beta, ct_right)
            vm = VMobject(color=ORANGE, stroke_width=2, stroke_opacity=0.6)
            vm.set_points_as_corners([p_left, p_right])
            return vm

        rest_simul = always_redraw(rest_simul_line)
        moving_simul = always_redraw(moving_simul_line)

        # ------------------------------------------------------------------
        # Labels for simultaneity lines
        # ------------------------------------------------------------------
        simultaneity_label_rest = MathTex(
            "t = \\text{const}", font_size=16, color=GREEN
        ).to_corner(UP + LEFT, buff=0.3)
        simultaneity_label_moving = MathTex(
            "t' = \\text{const}", font_size=16, color=ORANGE
        ).to_corner(UP + RIGHT, buff=0.3)

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
        # Phase 1: axes and light cones
        self.play(Create(x_axis), Create(ct_axis), Write(x_label), Write(ct_label))
        self.play(Create(light_cone_right), Create(light_cone_left), Write(light_label))
        self.wait(0.5)

        # Phase 2: worldlines
        self.play(Create(rest_worldline), Write(rest_label))
        self.play(Create(moving_worldline), Write(moving_label))
        self.wait(0.5)

        # Phase 3: events A and B
        self.play(
            Create(event_A_dot), Create(event_B_dot),
            Write(event_A_label), Write(event_B_label),
        )
        self.wait(0.5)

        # Phase 4: simultaneity lines (animated)
        self.play(
            Write(simultaneity_label_rest),
            Write(simultaneity_label_moving),
        )
        self.add(rest_simul, moving_simul)
        self.add(driver)
        self.wait(6.0)

        # Phase 5: final explanation
        self.play(
            FadeOut(rest_simul),
            FadeOut(moving_simul),
            FadeOut(simultaneity_label_rest),
            FadeOut(simultaneity_label_moving),
        )

        explanation = MathTex(
            "\\text{Events A and B are simultaneous in the rest frame}",
            font_size=22,
        ).to_corner(UP + LEFT, buff=0.3)
        explanation2 = MathTex(
            "\\text{but NOT simultaneous in the moving frame}",
            font_size=22,
            color=ORANGE,
        ).next_to(explanation, DOWN, buff=0.2)

        # Show rest simultaneity line through A and B
        rest_final = Line(
            to_mcoord(-x_max, 0.0), to_mcoord(x_max, 0.0),
            color=GREEN, stroke_width=2, stroke_opacity=0.8,
        )
        # Show moving simultaneity line through A (t'=0 at A)
        # For event A at x=-1.5, t=0: t'_A = γ(0 - β*(-1.5)/c) = γ*β*1.5/c
        # For event B at x=+1.5, t=0: t'_B = γ(0 - β*1.5/c) = -γ*β*1.5/c
        # So A and B have different t' — they are NOT simultaneous in moving frame
        beta = v / re.c
        t_prime_A = gamma * (0.0 - beta * (-1.5) / re.c)
        t_prime_B = gamma * (0.0 - beta * 1.5 / re.c)
        # Line of constant t' through A: ct = βx + ct'_offset
        # t'_A = γ(t - βx/c) → for constant t' = t'_A: t = βx/c + t'_A/γ
        # ct = βx + c*t'_A/γ
        offset_A = re.c * t_prime_A / gamma
        ct_left_A = beta * (-x_max) + offset_A
        ct_right_A = beta * x_max + offset_A
        moving_final = Line(
            to_mcoord(-x_max, ct_left_A),
            to_mcoord(x_max, ct_right_A),
            color=ORANGE, stroke_width=2, stroke_opacity=0.8,
        )

        self.play(
            Create(rest_final),
            Create(moving_final),
            Write(explanation),
            Write(explanation2),
        )
        self.wait(3.0)