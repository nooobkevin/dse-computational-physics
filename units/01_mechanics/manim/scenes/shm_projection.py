"""Scene A — SHM as the projection of uniform circular motion.

Animate a radius vector rotating at constant angular velocity; the
projection of its tip onto the horizontal axis executes simple harmonic
motion, and a displacement-vs-time cosine curve is traced in real time.
Phase-angle markers on the circle label the phase relationship with the
cosine curve.

Physics driver
--------------
CircularMotion from physics_core (read-only) supplies the radius and the
angular velocity; the on-screen angle is evaluated analytically as
θ = ω·t so that every visual is a pure function of the current time.

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
The simulation time is read from ``scene.time`` (the authoritative video
clock) and never accumulated from updater ``dt`` values, because updaters
fire twice per frame.  All time-varying visuals — including the
displacement trace, which is a SINGLE VMobject holding the prefix of a
precomputed cosine curve — are ``always_redraw`` mobjects rebuilt from
that time each frame, because submobjects appended to a mounted VGroup
from inside an updater are never re-rendered by the ManimCE cairo
renderer.
"""

from __future__ import annotations

import math
from bisect import bisect_right

import numpy as np
from manim import (
    Axes,
    BLUE_B,
    Circle,
    DashedLine,
    Dot,
    DOWN,
    GRAY,
    GRAY_A,
    GREY_D,
    LEFT,
    Line,
    MathTex,
    Mobject,
    RED_C,
    RED_D,
    RIGHT,
    Scene,
    UP,
    UR,
    VGroup,
    VMobject,
    YELLOW,
    always_redraw,
)

# Import the shared physics engine
from physics_core.mechanics.circular import CircularMotion


class ShmProjection(Scene):
    """SHM as projection of uniform circular motion — animated."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        radius: float = 2.0
        omega: float = 1.0  # rad/s — one rotation in ≈6.28 s
        circ = CircularMotion(radius=radius, omega0=omega, theta0=0.0)
        total_time: float = 10.0  # seconds of simulation time

        # Authoritative simulation time — read from the scene (video) clock.
        t: list[float] = [0.0]

        def tip_offset() -> np.ndarray:
            """Radius-vector tip relative to the centre, at θ = θ0 + ω·t."""
            theta = circ.angle + circ.omega() * t[0]
            return np.array(
                [
                    circ.radius * math.cos(theta),
                    circ.radius * math.sin(theta),
                    0.0,
                ]
            )

        # ------------------------------------------------------------------
        # Left panel — reference circle
        # ------------------------------------------------------------------
        center = LEFT * 3.2

        # Circle outline
        ref_circle = Circle(radius=radius, color=BLUE_B, stroke_width=3)
        ref_circle.move_to(center)

        # Horizontal axis through the centre (projection axis)
        axis_x = Line(
            center + LEFT * radius * 1.3,
            center + RIGHT * radius * 1.3,
            color=GRAY_A,
            stroke_width=1.5,
        )

        # Phase-angle markers at 0, π/2, π, 3π/2
        phase_labels = VGroup()
        for angle, label_str in [
            (0, "0"),
            (math.pi / 2, "\\pi/2"),
            (math.pi, "\\pi"),
            (3 * math.pi / 2, "3\\pi/2"),
        ]:
            pos = center + np.array(
                [
                    radius * 1.15 * math.cos(angle),
                    radius * 1.15 * math.sin(angle),
                    0,
                ]
            )
            lbl = MathTex(label_str, font_size=18, color=GRAY)
            lbl.move_to(pos)
            phase_labels.add(lbl)

        # Radius vector (rotates with the simulation)
        radius_line = always_redraw(
            lambda: Line(
                center,
                center + tip_offset(),
                color=YELLOW,
                stroke_width=5,
            )
        )

        # Tip dot on the circle
        tip_dot = always_redraw(
            lambda: Dot(
                center + tip_offset(),
                color=YELLOW,
                radius=0.09,
            )
        )

        # Projected dot on the horizontal axis
        proj_dot = always_redraw(
            lambda: Dot(
                center + np.array([tip_offset()[0], 0.0, 0.0]),
                color=RED_C,
                radius=0.10,
            )
        )

        # Dropline connecting the tip to the projected dot
        drop_line = always_redraw(
            lambda: Line(
                center + tip_offset(),
                center + np.array([tip_offset()[0], 0.0, 0.0]),
                color=RED_D,
                stroke_width=2,
                stroke_opacity=0.6,
            )
        )

        # "x" label on the projection axis
        x_label_circle = MathTex("x", color=RED_C, font_size=28).next_to(
            axis_x.get_end(), UR, buff=0.1
        )

        # ------------------------------------------------------------------
        # Right panel — displacement vs. time graph
        # ------------------------------------------------------------------
        axes = Axes(
            x_range=[0, int(total_time) + 1, 2],
            y_range=[-radius * 1.2, radius * 1.2, 0.5],
            x_length=5.5,
            y_length=3.0,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 20,
            },
        )
        axes.next_to(ref_circle, RIGHT, buff=1.2, aligned_edge=UP)

        t_label = MathTex("t", font_size=28).next_to(
            axes.x_axis.get_end(), DOWN
        )
        x_label_graph = MathTex("x", color=RED_C, font_size=28).next_to(
            axes.y_axis.get_end(), LEFT
        )

        # Displacement curve — precomputed once, revealed progressively
        trace_ts: list[float] = [
            float(v) for v in np.arange(0.0, total_time + 0.01, 0.01)
        ]
        trace_scr = [
            axes.c2p(t_i, radius * math.cos(omega * t_i)) for t_i in trace_ts
        ]

        def revealed_trace() -> VMobject:
            """Prefix of the exact cosine curve with time <= t[0]."""
            vm = VMobject(color=RED_C, stroke_width=3)
            n = bisect_right(trace_ts, t[0])
            if n >= 2:
                vm.set_points_as_corners(trace_scr[:n])
            return vm

        trace = always_redraw(revealed_trace)

        # Moving dot on the graph that tracks the current displacement
        current_dot = always_redraw(
            lambda: Dot(
                axes.c2p(t[0], tip_offset()[0]),
                color=RED_C,
                radius=0.10,
            )
        )

        # Alignment line connecting the projection axis on the left to the
        # current trace point on the right — shows the mapping visually
        alignment_line = always_redraw(
            lambda: DashedLine(
                center + np.array([tip_offset()[0], 0.0, 0.0]),
                axes.c2p(t[0], tip_offset()[0]),
                color=GREY_D,
                stroke_width=1.5,
                stroke_opacity=0.4,
            )
        )

        # Legend text explaining the mapping
        legend_text = MathTex(
            "x = R\\cos(\\omega t)", font_size=24, color=RED_C
        )
        legend_text.next_to(axes, DOWN, buff=0.3)

        # ------------------------------------------------------------------
        # Physics driver — publishes the authoritative video time
        # ------------------------------------------------------------------
        def physics_updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(physics_updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        self.add(ref_circle, axis_x, phase_labels)
        self.add(radius_line, tip_dot, proj_dot, drop_line, x_label_circle)
        self.add(axes, t_label, x_label_graph)
        self.add(trace, current_dot, alignment_line, legend_text)
        self.add(driver)

        self.wait(total_time)