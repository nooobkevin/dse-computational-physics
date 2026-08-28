"""Scene C — Projectile trajectory with dt convergence.

Shows an exact parabolic trajectory alongside numerical trajectories
computed with coarse and fine time steps using Euler integration.
The moving projectile dots animate along each path simultaneously,
illustrating how dt affects numerical accuracy.

Physics drivers
---------------
- ReferenceProjectileSim from physics_core.mechanics.projectile provides
  the reference (0, -g) acceleration.
- The exact kinematic parabola serves as the ground truth.

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
All three trajectories are precomputed ONCE as (time, x, y) arrays.  Each
visible trace is an ``always_redraw`` mobject rebuilt every frame as a
SINGLE VMobject holding the prefix of its data with ``time <= t``, and the
three projectile dots are rebuilt each frame from the positions at ``t``.
``t`` is read from ``scene.time`` (the authoritative video clock) and is
never accumulated from updater ``dt`` values.  This pattern is required
because submobjects appended to a mounted VGroup from inside an updater
are never re-rendered by the ManimCE cairo renderer, and because updaters
fire twice per frame (dt accumulation would run the simulation at 2×
video speed).
"""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Sequence

import numpy as np
from manim import (
    Axes,
    BLUE,
    Dot,
    DOWN,
    GREEN,
    GRAY_BROWN,
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


class ProjectileDt(Scene):
    """Projectile trajectory: exact vs coarse-dt vs fine-dt Euler."""

    def construct(self) -> None:
        # ==================================================================
        # Physical parameters
        # ==================================================================
        vx0: float = 5.0
        vy0: float = 7.0
        g: float = 9.81
        total_time: float = 2.0 * vy0 / g  # time of flight ≈ 1.43 s

        # Pre-compute exact parabola
        exact_ts = [float(t) for t in np.linspace(0.0, total_time, 200)]
        exact_xs = [vx0 * t for t in exact_ts]
        exact_ys = [vy0 * t - 0.5 * g * t * t for t in exact_ts]

        # Axes range
        x_max = vx0 * total_time * 1.2
        y_max = vy0 * vy0 / (2.0 * g) * 1.3

        # ==================================================================
        # Numerical simulations (Euler integration)
        # ==================================================================
        dt_coarse = 0.06
        dt_fine = 0.01

        def simulate_euler(
            dt: float, max_t: float
        ) -> tuple[list[float], list[float], list[float]]:
            """Return (times, xs, ys) for Euler integration."""
            sim = ReferenceProjectileSim(
                vx0=vx0,
                vy0=vy0,
                dt=dt,
                scheme="euler",
            )
            ts: list[float] = [0.0]
            xs: list[float] = [0.0]
            ys: list[float] = [0.0]
            while sim.state.t < max_t:
                sim.step()
                pos = sim.position
                ts.append(sim.state.t)
                xs.append(pos[0])
                ys.append(pos[1])
            return ts, xs, ys

        coarse_ts, coarse_xs, coarse_ys = simulate_euler(dt_coarse, total_time)
        fine_ts, fine_xs, fine_ys = simulate_euler(dt_fine, total_time)

        # ==================================================================
        # Axes — position (x horizontally, y vertically)
        # ==================================================================
        axes = Axes(
            x_range=[0, x_max, 1],
            y_range=[0, y_max, 1],
            x_length=8,
            y_length=4.5,
            axis_config={
                "color": GRAY_BROWN,
                "include_numbers": True,
                "font_size": 20,
            },
        )
        axes.center().shift(UP * 0.2)

        x_label = MathTex("x").next_to(axes.x_axis.get_end(), DOWN)
        y_label = MathTex("y").next_to(axes.y_axis.get_end(), LEFT)

        # ==================================================================
        # Legend
        # ==================================================================
        legend = VGroup(
            MathTex("\\text{Exact (parabola)}", color=GREEN, font_size=22),
            MathTex(
                "\\text{Euler coarse dt}=" + str(dt_coarse),
                color=RED,
                font_size=22,
            ),
            MathTex(
                "\\text{Euler fine dt}=" + str(dt_fine),
                color=BLUE,
                font_size=22,
            ),
        )
        legend.arrange(DOWN, aligned_edge=LEFT).to_corner(
            UP + RIGHT, buff=0.5
        )

        # ==================================================================
        # Precomputed screen points (R9) + progressive-reveal curves
        # ==================================================================
        # Authoritative simulation time — read from the scene (video) clock.
        t: list[float] = [0.0]

        def screen_points(
            xs: Sequence[float], ys: Sequence[float]
        ) -> list[np.ndarray]:
            """Map a whole dataset to scene coordinates ONCE."""
            return [axes.c2p(x_i, y_i) for x_i, y_i in zip(xs, ys)]

        exact_scr = screen_points(exact_xs, exact_ys)
        coarse_scr = screen_points(coarse_xs, coarse_ys)
        fine_scr = screen_points(fine_xs, fine_ys)

        def revealed_count(ts: Sequence[float]) -> int:
            """How many samples of a dataset are visible at time t[0]."""
            return bisect_right(ts, t[0])

        def revealed(
            ts: Sequence[float],
            pts: Sequence[np.ndarray],
            color: str,
            width: float,
        ) -> VMobject:
            """Prefix of a precomputed trajectory with time <= t[0]."""
            vm = VMobject(color=color, stroke_width=width)
            n = revealed_count(ts)
            if n >= 2:
                vm.set_points_as_corners(list(pts[:n]))
            return vm

        trace_exact = always_redraw(
            lambda: revealed(exact_ts, exact_scr, GREEN, 3)
        )
        trace_coarse = always_redraw(
            lambda: revealed(coarse_ts, coarse_scr, RED, 3)
        )
        trace_fine = always_redraw(
            lambda: revealed(fine_ts, fine_scr, BLUE, 3)
        )

        # ==================================================================
        # Animated projectile dots — rebuilt each frame from t[0]
        # ==================================================================
        def dots() -> VGroup:
            """One dot per scheme at its current trajectory position."""
            group = VGroup()
            for ts, pts, color in (
                (exact_ts, exact_scr, GREEN),
                (coarse_ts, coarse_scr, RED),
                (fine_ts, fine_scr, BLUE),
            ):
                i = min(max(revealed_count(ts) - 1, 0), len(pts) - 1)
                group.add(Dot(pts[i], color=color, radius=0.08))
            return group

        projectiles = always_redraw(dots)

        # ==================================================================
        # Physics driver — publishes the authoritative video time
        # ==================================================================
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # ==================================================================
        # Assemble the scene
        # ==================================================================
        self.add(axes, x_label, y_label)
        self.add(legend)
        self.add(trace_exact, trace_coarse, trace_fine)
        self.add(projectiles)
        self.add(driver)

        self.wait(total_time)
