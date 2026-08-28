"""Scene F — Ideal parabola vs trajectory with linear drag.

Two projectiles launched with identical initial conditions: one under
ideal gravity (no drag) and one with linear air resistance (drag
coefficient b > 0).  The drag trajectory shows range reduction and
a terminal-velocity hint in the vertical component.

Physics: ax = -b·vx/m, ay = -g - b·vy/m.
Terminal velocity (vertical): v_term = -m·g / b.

CAF reference: CP activity "projectile motion with or without air resistance".
"""

from __future__ import annotations

from bisect import bisect_right

import numpy as np
from manim import (
    Axes,
    BLUE,
    DOWN,
    GRAY_BROWN,
    GREEN,
    GREY_D,
    Dot,
    LEFT,
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

from physics_core.mechanics.projectile import ReferenceProjectileSim


class ProjectileDrag(Scene):
    """Ideal parabola vs trajectory with linear drag."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        vx0: float = 8.0
        vy0: float = 6.0
        g: float = 9.81
        mass: float = 1.0
        drag_coeff: float = 0.5  # b value — noticeable but not extreme
        total_time: float = 2.0 * vy0 / g  # ideal time of flight ~1.22s
        total_time_actual: float = total_time * 2.0  # drag extends flight time

        # Ideal trajectory (analytical parabola)
        ideal_ts = [float(t) for t in np.linspace(0.0, total_time, 200)]
        ideal_xs = [vx0 * t for t in ideal_ts]
        ideal_ys = [vy0 * t - 0.5 * g * t * t for t in ideal_ts]

        # Drag trajectory (numerical)
        def simulate_drag(
            b: float, dt: float = 0.005,
        ) -> tuple[list[float], list[float], list[float]]:
            sim = ReferenceProjectileSim(
                vx0=vx0, vy0=vy0, dt=dt, scheme="verlet",
                drag_coefficient=b, mass=mass,
            )
            ts: list[float] = [0.0]
            xs: list[float] = [0.0]
            ys: list[float] = [0.0]
            while sim.state.t < total_time_actual and sim.state.y >= 0:
                sim.step()
                ts.append(sim.state.t)
                xs.append(sim.state.x)
                ys.append(max(sim.state.y, 0.0))
            return ts, xs, ys

        drag_ts, drag_xs, drag_ys = simulate_drag(drag_coeff)
        no_drag_ts, no_drag_xs, no_drag_ys = simulate_drag(0.0)

        # Terminal velocity (vertical fall under drag)
        v_term = mass * g / drag_coeff  # ≈ 19.62 m/s

        x_max = max(max(ideal_xs), max(drag_xs)) * 1.15
        y_max = max(max(ideal_ys), max(drag_ys)) * 1.2

        # ------------------------------------------------------------------
        # Axes
        # ------------------------------------------------------------------
        axes = Axes(
            x_range=[0, x_max, 2],
            y_range=[0, y_max, 2],
            x_length=8,
            y_length=4.5,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 20,
            },
        )
        axes.center().shift(UP * 0.3)

        x_label = MathTex("x", font_size=24).next_to(axes.x_axis.get_end(), DOWN)
        y_label = MathTex("y", font_size=24).next_to(axes.y_axis.get_end(), LEFT)

        title = MathTex(
            "\\text{Projectile: ideal vs with air resistance}",
            font_size=26,
            color=GRAY_BROWN,
        )
        title.to_edge(UP, buff=0.3)

        # ------------------------------------------------------------------
        # Legend
        # ------------------------------------------------------------------
        v_term_label = MathTex(
            f"b={drag_coeff},\\; v_{{\\text{{term}}}}\\approx{v_term:.1f}\\;\\text{{m/s}}",
            font_size=18,
            color=GRAY_BROWN,
        )

        legend = VGroup(
            MathTex("\\text{Ideal (no drag)}", color=GREEN, font_size=22),
            MathTex(
                f"\\text{{Drag }} b={drag_coeff}",
                color=RED, font_size=22,
            ),
            v_term_label,
        )
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.to_corner(UP + RIGHT, buff=0.5)

        # ------------------------------------------------------------------
        # Progressive-reveal curves
        # ------------------------------------------------------------------
        t: list[float] = [0.0]

        def make_curve(
            ts: list[float], xs: list[float], ys: list[float],
            ax: Axes, color: str, width: float,
        ) -> VMobject:
            scr = [ax.c2p(x_i, y_i) for x_i, y_i in zip(xs, ys)]
            def _inner() -> VMobject:
                vm = VMobject(color=color, stroke_width=width)
                n = bisect_right(ts, t[0])
                if n >= 2:
                    vm.set_points_as_corners(list(scr[:n]))
                return vm
            return always_redraw(_inner)

        trace_ideal = make_curve(ideal_ts, ideal_xs, ideal_ys, axes, GREEN, 3)
        trace_nodrag = make_curve(
            no_drag_ts, no_drag_xs, no_drag_ys, axes, BLUE, 2,
        )
        trace_drag = make_curve(
            drag_ts, drag_xs, drag_ys, axes, RED, 3,
        )

        # Projectile dots
        def make_dot(
            ts: list[float], xs: list[float], ys: list[float],
            ax: Axes, color: str,
        ) -> VMobject:
            def _inner() -> Dot:
                i = bisect_right(ts, t[0]) - 1
                i = max(0, min(i, len(ts) - 1))
                pt = ax.c2p(xs[i], ys[i])
                return Dot(pt, color=color, radius=0.09)
            return always_redraw(_inner)

        dot_ideal = make_dot(ideal_ts, ideal_xs, ideal_ys, axes, GREEN)
        dot_nodrag = make_dot(
            no_drag_ts, no_drag_xs, no_drag_ys, axes, BLUE,
        )
        dot_drag = make_dot(drag_ts, drag_xs, drag_ys, axes, RED)

        # Range labels
        ideal_range = max(ideal_xs)
        drag_range = max(drag_xs)

        range_label_ideal = always_redraw(
            lambda: MathTex(
                f"R_{{\\text{{ideal}}}}={ideal_range:.2f}",
                font_size=16, color=GREEN,
            ).next_to(axes.c2p(ideal_range, 0), DOWN, buff=0.15)
        )
        range_label_drag = always_redraw(
            lambda: MathTex(
                f"R_{{\\text{{drag}}}}={drag_range:.2f}",
                font_size=16, color=RED,
            ).next_to(axes.c2p(drag_range, 0), DOWN, buff=0.15)
        )

        # ------------------------------------------------------------------
        # Physics driver
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # ------------------------------------------------------------------
        # Assemble
        # ------------------------------------------------------------------
        self.add(title)
        self.add(axes, x_label, y_label)
        self.add(legend)
        self.add(trace_ideal, trace_nodrag, trace_drag)
        self.add(dot_ideal, dot_nodrag, dot_drag)
        self.add(range_label_ideal, range_label_drag)
        self.add(driver)

        self.wait(total_time_actual)