"""Scene B — Explicit Euler vs velocity-Verlet vs exact SHM solution.

Plots the trajectory of a simple harmonic oscillator for three methods
and shows the energy drift of Euler (unstable at large dt) compared to
the symplectic Verlet scheme.  A convergence inset demonstrates that
reducing dt causes the numerical solution to collapse onto the exact
one.

Physics drivers
---------------
- euler_step / verlet_step from physics_core.integrators (the same
  functions the student fill-in exercise targets).
- The exact solution is the closed-form x(t) = A·cos(ω·t).

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
Every curve is precomputed ONCE into a (time, value) array pair.  Each
visible curve is an ``always_redraw`` mobject that rebuilds itself every
frame as a SINGLE VMobject holding the prefix of its data with
``time <= t``, where ``t`` is read from ``scene.time`` (the authoritative
video clock) and never accumulated from updater ``dt`` values.  This
pattern is required because submobjects appended to a mounted VGroup
from inside an updater are never re-rendered by the ManimCE cairo
renderer, and because updaters fire twice per frame (dt accumulation
would run the simulation at 2× video speed).
"""

from __future__ import annotations

import math
from bisect import bisect_right
from collections.abc import Callable, Sequence

import numpy as np
from manim import (
    Axes,
    BLUE,
    BLUE_D,
    DOWN,
    GRAY_BROWN,
    GREEN,
    GREEN_D,
    GREY_D,
    LEFT,
    MathTex,
    Mobject,
    RED,
    RED_D,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    always_redraw,
)

from physics_core.integrators import euler_step, verlet_step


class IntegratorConvergence(Scene):
    """Compare Euler, Verlet, and exact SHM — trajectory + energy drift."""

    def construct(self) -> None:
        # ==================================================================
        # Physical system — unit-mass simple harmonic oscillator
        # ==================================================================
        omega_sq: float = 10.0  # k / m
        omega: float = math.sqrt(omega_sq)
        amplitude: float = 2.0
        total_time: float = 8.0  # seconds of simulation time

        def spring_deriv(x: float, v: float, t: float) -> float:
            """Acceleration for a unit-mass spring: a = -ω²·x."""
            return -omega_sq * x

        def exact_x(t: float) -> float:
            return amplitude * math.cos(omega * t)

        def total_energy(x: float, v: float) -> float:
            """E = ½·m·v² + ½·k·x²  (m=1, k=ω²)."""
            return 0.5 * v * v + 0.5 * omega_sq * x * x

        e0 = total_energy(amplitude, 0.0)

        # ==================================================================
        # Pre-compute all datasets ONCE (R9)
        # ==================================================================
        dt_euler = 0.1  # coarse — will show drift
        dt_verlet = 0.1  # same resolution, symplectic → stable

        Stepper = Callable[
            [dict[str, float], float, Callable[[float, float, float], float]],
            dict[str, float],
        ]

        def integrate(
            stepper: Stepper, h: float
        ) -> tuple[list[float], list[float], list[float]]:
            """Return (times, positions, energy ratios) for one scheme."""
            ts: list[float] = [0.0]
            xs: list[float] = [amplitude]
            es: list[float] = [1.0]
            state = {"x": amplitude, "v": 0.0, "t": 0.0}
            while state["t"] < total_time:
                state = stepper(state, h, spring_deriv)
                ts.append(state["t"])
                xs.append(state["x"])
                es.append(total_energy(state["x"], state["v"]) / e0)
            return ts, xs, es

        # Exact: high resolution for a smooth curve
        exact_ts: list[float] = [
            float(t) for t in np.arange(0.0, total_time + 0.01, 0.01)
        ]
        exact_xs: list[float] = [exact_x(t) for t in exact_ts]

        euler_ts, euler_xs, euler_es = integrate(euler_step, dt_euler)
        verlet_ts, verlet_xs, verlet_es = integrate(verlet_step, dt_verlet)

        # Euler energy is clipped so a blow-up stays inside the inset frame
        euler_en_xs = [min(e, 5.0) for e in euler_es]
        verlet_en_xs = verlet_es

        # Euler with two finer step sizes (convergence inset)
        half_ts, half_xs, _ = integrate(euler_step, dt_euler / 2.0)
        fine_ts, fine_xs, _ = integrate(euler_step, dt_euler / 10.0)

        # ==================================================================
        # Main axes — trajectory x(t)
        # ==================================================================
        axes = Axes(
            x_range=[0, total_time + 0.5, 1],
            y_range=[-amplitude * 1.3, amplitude * 1.3, 0.5],
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
            MathTex("\\text{Exact (analytical)}", color=GREEN, font_size=22),
            MathTex(
                "\\text{Euler (dt=" + str(dt_euler) + ")}",
                color=RED,
                font_size=22,
            ),
            MathTex(
                "\\text{Verlet (dt=" + str(dt_verlet) + ")}",
                color=BLUE,
                font_size=22,
            ),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(RIGHT + UP, buff=0.5)

        # ==================================================================
        # Insets
        # ==================================================================
        en_axes = Axes(
            x_range=[0, total_time, 2],
            y_range=[-0.1, 3.5, 1],
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

        conv_axes = Axes(
            x_range=[0, total_time, 2],
            y_range=[-amplitude * 1.2, amplitude * 1.2, 0.5],
            x_length=3.5,
            y_length=2.0,
            axis_config={
                "color": GREY_D,
                "include_numbers": False,
                "font_size": 14,
            },
        )
        conv_axes.next_to(en_axes, LEFT, buff=0.4, aligned_edge=DOWN)

        conv_title = (
            MathTex("\\text{dt convergence (Euler)}", font_size=16)
            .next_to(conv_axes, UP, buff=0.1)
            .shift(LEFT * 0.3)
        )

        conv_labels = VGroup(
            MathTex("\\text{dt}=" + str(dt_euler), color=RED_D, font_size=14),
            MathTex(
                "\\text{dt}=" + str(dt_euler / 10.0),
                color=BLUE_D,
                font_size=14,
            ),
            MathTex("\\text{exact}", color=GREEN_D, font_size=14),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        conv_labels.next_to(conv_axes, DOWN, buff=0.15).shift(RIGHT * 0.3)

        # ==================================================================
        # Progressive-reveal curves — one VMobject per curve per frame
        # ==================================================================
        # Authoritative simulation time — read from the scene (video) clock.
        t: list[float] = [0.0]

        def screen_points(
            plot: Axes, ts: Sequence[float], ys: Sequence[float]
        ) -> list[np.ndarray]:
            """Map a whole dataset to scene coordinates ONCE (R9)."""
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

        exact_scr = screen_points(axes, exact_ts, exact_xs)
        euler_scr = screen_points(axes, euler_ts, euler_xs)
        verlet_scr = screen_points(axes, verlet_ts, verlet_xs)
        euler_en_scr = screen_points(en_axes, euler_ts, euler_en_xs)
        verlet_en_scr = screen_points(en_axes, verlet_ts, verlet_en_xs)
        conv_exact_scr = screen_points(conv_axes, exact_ts, exact_xs)
        conv_half_scr = screen_points(conv_axes, half_ts, half_xs)
        conv_fine_scr = screen_points(conv_axes, fine_ts, fine_xs)

        trace_exact = always_redraw(
            lambda: revealed(exact_ts, exact_scr, GREEN, 3)
        )
        trace_euler = always_redraw(
            lambda: revealed(euler_ts, euler_scr, RED, 3)
        )
        trace_verlet = always_redraw(
            lambda: revealed(verlet_ts, verlet_scr, BLUE, 3)
        )

        en_trace_euler = always_redraw(
            lambda: revealed(euler_ts, euler_en_scr, RED, 2)
        )
        en_trace_verlet = always_redraw(
            lambda: revealed(verlet_ts, verlet_en_scr, BLUE, 2)
        )

        conv_trace_exact = always_redraw(
            lambda: revealed(exact_ts, conv_exact_scr, GREEN_D, 2)
        )
        conv_trace_half = always_redraw(
            lambda: revealed(half_ts, conv_half_scr, RED_D, 2)
        )
        conv_trace_fine = always_redraw(
            lambda: revealed(fine_ts, conv_fine_scr, BLUE_D, 2)
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
        self.add(legend)
        self.add(conv_axes, conv_title, conv_labels)
        self.add(en_axes, en_title)
        self.add(conv_trace_exact, conv_trace_half, conv_trace_fine)
        self.add(en_trace_euler, en_trace_verlet)
        self.add(trace_exact, trace_euler, trace_verlet)
        self.add(driver)

        self.wait(total_time)
