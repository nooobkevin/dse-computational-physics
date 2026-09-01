"""Scene B — Euler vs Velocity-Verlet for molecular dynamics.

Compares energy conservation of Euler and Verlet integration schemes for
an atom vibrating about its lattice site (harmonic restoring force
F = -k(x - x_c)).  Euler's energy grows without bound; Verlet keeps it
bounded near E0.  A force-free particle would make the two schemes
numerically identical, so the spring force is what makes the comparison
meaningful.

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
        m = 1.0
        k = 4.0  # spring constant -> omega0 = 2 rad/s, period ~ pi s
        x_c = 7.5  # lattice-site equilibrium
        amplitude = 3.0

        # ==================================================================
        # Pre-compute data: an atom bound to a lattice site by a harmonic
        # restoring force.  This is the thermal-physics context (vibrating
        # solid) and, unlike force-free motion, it makes Euler and Verlet
        # behave differently.
        # ==================================================================

        def spring_deriv(x: float, v: float, t: float) -> float:
            return -k * (x - x_c) / m

        def total_energy(x: float, v: float) -> float:
            return 0.5 * m * v * v + 0.5 * k * (x - x_c) ** 2

        x0 = x_c + amplitude
        v0 = 0.0

        # Euler trajectory
        euler_ts: list[float] = [0.0]
        euler_xs: list[float] = [x0]
        euler_vs: list[float] = [v0]
        euler_ke: list[float] = [total_energy(x0, v0)]
        state = {"x": x0, "v": v0, "t": 0.0}

        while state["t"] < total_time:
            state = euler_step(state, dt, spring_deriv)
            x, v = state["x"], state["v"]
            euler_ts.append(state["t"])
            euler_xs.append(x)
            euler_vs.append(v)
            euler_ke.append(total_energy(x, v))

        # Verlet trajectory
        verlet_ts: list[float] = [0.0]
        verlet_xs: list[float] = [x0]
        verlet_vs: list[float] = [v0]
        verlet_ke: list[float] = [total_energy(x0, v0)]
        state = {"x": x0, "v": v0, "t": 0.0}

        while state["t"] < total_time:
            state = verlet_step(state, dt, spring_deriv)
            x, v = state["x"], state["v"]
            verlet_ts.append(state["t"])
            verlet_xs.append(x)
            verlet_vs.append(v)
            verlet_ke.append(total_energy(x, v))

        # Normalise total energy to initial value
        ke0 = total_energy(x0, v0)
        euler_ke_norm = [e / ke0 for e in euler_ke]
        verlet_ke_norm = [e / ke0 for e in verlet_ke]

        # ==================================================================
        # Main axes — trajectory x(t)
        # ==================================================================
        axes = Axes(
            x_range=[0, total_time + 0.5, 2],
            y_range=[0, x_c + amplitude * 1.4, x_c / 2],
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
        # Model parameters caption (atom vibrating about a lattice site)
        # ==================================================================
        gas_caption = MathTex(
            f"m = {m},\\; k = {k},\\; F = -k(x - x_c),\\; A = {amplitude}",
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

        trace_euler = always_redraw(
            lambda: revealed(euler_ts, euler_scr, RED, 5)
        )
        trace_verlet = always_redraw(
            lambda: revealed(verlet_ts, verlet_scr, BLUE, 5)
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
