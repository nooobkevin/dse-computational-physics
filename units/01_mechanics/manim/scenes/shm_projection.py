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
    BLUE,
    BLUE_B,
    Circle,
    DashedLine,
    Dot,
    DOWN,
    GRAY,
    GRAY_A,
    GREEN,
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
        # Velocity panel — v(t) = -R·ω·sin(ωt)
        # ------------------------------------------------------------------
        v_axes = Axes(
            x_range=[0, int(total_time) + 1, 2],
            y_range=[-radius * omega * 1.3, radius * omega * 1.3, 1.0],
            x_length=5.5,
            y_length=1.5,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 16,
            },
        )
        v_axes.next_to(legend_text, DOWN, buff=0.3, aligned_edge=LEFT)
        v_axes.shift(RIGHT * 0.5)

        v_t_label = MathTex("t", font_size=20).next_to(
            v_axes.x_axis.get_end(), DOWN
        )
        v_label_graph = MathTex("v", color=GREEN, font_size=20).next_to(
            v_axes.y_axis.get_end(), LEFT
        )

        v_trace_scr = [
            v_axes.c2p(t_i, -radius * omega * math.sin(omega * t_i))
            for t_i in trace_ts
        ]
        v_trace = always_redraw(lambda: _build_curve(v_trace_scr, trace_ts, t, GREEN, 2.5))

        v_current_dot = always_redraw(
            lambda: Dot(
                v_axes.c2p(t[0], -radius * omega * math.sin(omega * t[0])),
                color=GREEN, radius=0.08,
            )
        )

        v_formula = MathTex(
            "v = -R\\omega\\sin(\\omega t)", font_size=18, color=GREEN,
        )
        v_formula.next_to(v_axes, DOWN, buff=0.15)

        # ------------------------------------------------------------------
        # Acceleration panel — a(t) = -R·ω²·cos(ωt)
        # ------------------------------------------------------------------
        a_axes = Axes(
            x_range=[0, int(total_time) + 1, 2],
            y_range=[-radius * omega**2 * 1.3, radius * omega**2 * 1.3, 1.0],
            x_length=5.5,
            y_length=1.5,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 16,
            },
        )
        a_axes.next_to(v_formula, DOWN, buff=0.2, aligned_edge=LEFT)
        a_axes.shift(RIGHT * 0.5)

        a_t_label = MathTex("t", font_size=20).next_to(
            a_axes.x_axis.get_end(), DOWN
        )
        a_label_graph = MathTex("a", color=BLUE, font_size=20).next_to(
            a_axes.y_axis.get_end(), LEFT
        )

        a_trace_scr = [
            a_axes.c2p(t_i, -radius * omega**2 * math.cos(omega * t_i))
            for t_i in trace_ts
        ]
        a_trace = always_redraw(lambda: _build_curve(a_trace_scr, trace_ts, t, BLUE, 2.5))

        a_current_dot = always_redraw(
            lambda: Dot(
                a_axes.c2p(t[0], -radius * omega**2 * math.cos(omega * t[0])),
                color=BLUE, radius=0.08,
            )
        )

        a_formula = MathTex(
            "a = -R\\omega^2\\cos(\\omega t)", font_size=18, color=BLUE,
        )
        a_formula.next_to(a_axes, DOWN, buff=0.15)

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
        self.add(v_axes, v_t_label, v_label_graph)
        self.add(v_trace, v_current_dot, v_formula)
        self.add(a_axes, a_t_label, a_label_graph)
        self.add(a_trace, a_current_dot, a_formula)
        self.add(driver)

        self.wait(total_time)


def _build_curve(
    scr: list[np.ndarray],
    ts: list[float],
    t_ref: list[float],
    color: str,
    width: float,
) -> VMobject:
    """Revealed prefix of a precomputed (time, value) curve."""
    vm = VMobject(color=color, stroke_width=width)
    n = bisect_right(ts, t_ref[0])
    if n >= 2:
        vm.set_points_as_corners(list(scr[:n]))
    return vm