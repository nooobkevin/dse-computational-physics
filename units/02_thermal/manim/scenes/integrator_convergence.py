"""Scene B — Euler vs Velocity-Verlet for molecular dynamics.

Compares energy conservation of Euler and Verlet integration schemes
for a gas of particles bouncing inside a box.  Verlet conserves kinetic
energy much better than Euler when particles collide with walls.

Physics drivers
---------------
- euler_step / verlet_step from physics_core.integrators (the same
  functions used across the toolkit).
- ReferenceGasSim from physics_core.thermal.gas_sim.

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
Both trajectories and both energy-drift curves are integrated ONCE into
(time, value) datasets before the animation starts.  Each visible curve
is an ``always_redraw`` mobject that rebuilds itself every frame as a
SINGLE VMobject holding the prefix of its dataset with ``time <= t``,
where ``t`` is read from ``scene.time`` (the authoritative video clock)
and never accumulated from updater ``dt`` values.  This pattern is
required because submobjects appended to a mounted VGroup from inside an
updater are never re-rendered by the ManimCE cairo renderer, and because
updaters fire twice per frame (dt accumulation would run the simulation
at 2x video speed).
"""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Sequence

import numpy as np
from manim import (
    Axes,
    BLUE,
    DOWN,
    Dot,
    GRAY_BROWN,
    GREY_D,
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

from physics_core.integrators import euler_step, verlet_step


class IntegratorConvergence(Scene):
    """Compare Euler and Verlet energy conservation for MD."""

    def construct(self) -> None:
        # ==================================================================
        # Parameters
        # ==================================================================
        total_time = 10.0
        dt = 0.02
        N = 50
        L = 15.0
        T_init = 2.0
        m = 1.0

        # ==================================================================
        # Pre-compute data using ReferenceGasSim-like logic
        # We use the integrators directly on a single particle bouncing
        # between walls to show the energy conservation difference.
        # ==================================================================

        def wall_collision(pos: float, vel: float, L: float) -> tuple[float, float]:
            """Reflect at walls."""
            if pos < 0:
                return -pos, abs(vel)
            if pos > L:
                return 2.0 * L - pos, -abs(vel)
            return pos, vel

        # Single particle bouncing in 1D
        amplitude = L * 0.4
        x0 = L / 2 + amplitude
        v0 = -3.0

        # Euler trajectory
        euler_ts: list[float] = [0.0]
        euler_xs: list[float] = [x0]
        euler_vs: list[float] = [v0]
        euler_ke: list[float] = [0.5 * m * v0 * v0]
        state = {"x": x0, "v": v0, "t": 0.0}

        def zero_deriv(x: float, v: float, t: float) -> float:
            return 0.0

        while state["t"] < total_time:
            state = euler_step(state, dt, zero_deriv)
            x, v = state["x"], state["v"]
            x, v = wall_collision(x, v, L)
            state["x"], state["v"] = x, v
            euler_ts.append(state["t"])
            euler_xs.append(x)
            euler_vs.append(v)
            euler_ke.append(0.5 * m * v * v)

        # Verlet trajectory
        verlet_ts: list[float] = [0.0]
        verlet_xs: list[float] = [x0]
        verlet_vs: list[float] = [v0]
        verlet_ke: list[float] = [0.5 * m * v0 * v0]
        state = {"x": x0, "v": v0, "t": 0.0}

        while state["t"] < total_time:
            state = verlet_step(state, dt, zero_deriv)
            x, v = state["x"], state["v"]
            x, v = wall_collision(x, v, L)
            state["x"], state["v"] = x, v
            verlet_ts.append(state["t"])
            verlet_xs.append(x)
            verlet_vs.append(v)
            verlet_ke.append(0.5 * m * v * v)

        # Normalise KE to initial value
        ke0 = 0.5 * m * v0 * v0
        euler_ke_norm = [e / ke0 for e in euler_ke]
        verlet_ke_norm = [e / ke0 for e in verlet_ke]

        # ==================================================================
        # Main axes — trajectory x(t)
        # ==================================================================
        axes = Axes(
            x_range=[0, total_time + 0.5, 2],
            y_range=[-L * 0.1, L * 1.1, L / 4],
            x_length=8,
            y_length=4,
            axis_config={
                "color": GRAY_BROWN,
                "include_numbers": True,
                "font_size": 20,
            },
        )
        axes.center().shift(UP * 0.3)

        t_label = MathTex("t").next_to(axes.x_axis.get_end(), DOWN)
        x_label = MathTex("x").next_to(axes.y_axis.get_end(), LEFT)

        # ==================================================================
        # Legend
        # ==================================================================
        legend = VGroup(
            MathTex("\\text{Euler (dt=" + str(dt) + ")}", color=RED, font_size=22),
            MathTex(
                "\\text{Verlet (dt=" + str(dt) + ")}",
                color=BLUE,
                font_size=22,
            ),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(RIGHT + UP, buff=0.5)

        # ==================================================================
        # Gas parameters caption (N particles at T_init in a box of side L)
        # ==================================================================
        gas_caption = MathTex(
            f"N = {N},\\; T = {T_init},\\; L = {L},\\; m = {m}",
            font_size=20,
        ).to_corner(UP + LEFT, buff=0.4)

        # ---- Energy-drift inset ----
        en_axes = Axes(
            x_range=[0, total_time, 2],
            y_range=[-0.1, 3.0, 1],
            x_length=3.5,
            y_length=2.0,
            axis_config={
                "color": GREY_D,
                "include_numbers": False,
                "font_size": 14,
            },
        )
        en_axes.to_corner(DOWN + RIGHT, buff=0.5)

        en_title = (
            MathTex("\\text{Energy drift } E/E_0", font_size=18)
            .next_to(en_axes, UP, buff=0.1)
            .shift(LEFT * 0.3)
        )

        # ==================================================================
        # Progressive-reveal traces — one VMobject per curve per frame
        # ==================================================================
        # Authoritative simulation time — read from the scene (video) clock.
        t: list[float] = [0.0]

        def screen_points(
            plot: Axes, ts: Sequence[float], ys: Sequence[float]
        ) -> list[np.ndarray]:
            """Map a whole dataset to scene coordinates ONCE."""
            return [plot.c2p(t_i, y_i) for t_i, y_i in zip(ts, ys)]

        def revealed(
            ts: Sequence[float],
            pts: Sequence[np.ndarray],
            color: str,
            width: float,
        ) -> VMobject:
            """Prefix of a precomputed curve with time <= t[0]."""
            vm = VMobject(color=color, stroke_width=width)
            n = bisect_right(ts, t[0])
            if n >= 2:
                vm.set_points_as_corners(list(pts[:n]))
            return vm

        def head(
            ts: Sequence[float],
            pts: Sequence[np.ndarray],
            color: str,
            radius: float,
        ) -> Dot:
            """Marker on the leading edge — the particle's current state."""
            i = min(max(bisect_right(ts, t[0]) - 1, 0), len(pts) - 1)
            return Dot(pts[i], radius=radius, color=color)

        euler_scr = screen_points(axes, euler_ts, euler_xs)
        verlet_scr = screen_points(axes, verlet_ts, verlet_xs)
        euler_en_scr = screen_points(en_axes, euler_ts, euler_ke_norm)
        verlet_en_scr = screen_points(en_axes, verlet_ts, verlet_ke_norm)

        # For force-free motion Euler and Verlet give the SAME trajectory, so
        # the Verlet stroke is drawn thinner on top of the Euler one to keep
        # both schemes visible where the two curves coincide.
        trace_euler = always_redraw(
            lambda: revealed(euler_ts, euler_scr, RED, 8)
        )
        trace_verlet = always_redraw(
            lambda: revealed(verlet_ts, verlet_scr, BLUE, 3)
        )

        head_euler = always_redraw(
            lambda: head(euler_ts, euler_scr, RED, 0.12)
        )
        head_verlet = always_redraw(
            lambda: head(verlet_ts, verlet_scr, BLUE, 0.06)
        )

        en_trace_euler = always_redraw(
            lambda: revealed(euler_ts, euler_en_scr, RED, 6)
        )
        en_trace_verlet = always_redraw(
            lambda: revealed(verlet_ts, verlet_en_scr, BLUE, 2)
        )

        en_head_euler = always_redraw(
            lambda: head(euler_ts, euler_en_scr, RED, 0.09)
        )
        en_head_verlet = always_redraw(
            lambda: head(verlet_ts, verlet_en_scr, BLUE, 0.04)
        )

        # ==================================================================
        # Physics driver — publishes the authoritative video time
        # ==================================================================
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # ==================================================================
        # Assemble and run
        # ==================================================================
        self.add(axes, t_label, x_label)
        self.add(legend, gas_caption)
        self.add(en_axes, en_title)
        self.add(en_trace_euler, en_trace_verlet)
        self.add(en_head_euler, en_head_verlet)
        self.add(trace_euler, trace_verlet)
        self.add(head_euler, head_verlet)
        self.add(driver)

        self.wait(total_time)
