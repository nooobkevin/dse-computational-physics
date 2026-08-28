"""Scene A — Superposition of two transverse waves forming a standing wave.

Animate two counter-propagating traveling waves (one moving right, one
moving left) and their superposition, which produces a standing wave
with fixed nodes.  The standing wave is computed analytically via
ReferenceWaveSim.standing_wave().

Physics driver
--------------
ReferenceWaveSim from physics_core.waves.wave_sim provides the analytical
traveling and standing wave solutions.

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
The visible curves are ``always_redraw`` mobjects rebuilt every frame as
a single VMobject from the current simulation time.  The simulation time
is read from ``scene.time`` (the authoritative video time), NOT
accumulated from updater ``dt`` values.  This pattern is required
because submobjects appended to a mounted VGroup from inside an updater
are never re-rendered by the ManimCE cairo renderer.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Axes,
    BLUE,
    GREEN,
    GREY_D,
    LEFT,
    DOWN,
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
    always_redraw,
)

from physics_core.waves.wave_sim import ReferenceWaveSim


class SuperpositionStanding(Scene):
    """Superposition of two transverse waves → standing wave with nodes."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        A: float = 1.0
        lam: float = 4.0
        f: float = 0.5
        sim = ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f, L=12.0, nx=300)
        total_time: float = 8.0

        # Authoritative simulation time — read from scene (video) time.
        t: list[float] = [0.0]

        # ------------------------------------------------------------------
        # Axes
        # ------------------------------------------------------------------
        axes = Axes(
            x_range=[0, sim.L, 2],
            y_range=[-A * 3.5, A * 3.5, 1],
            x_length=10,
            y_length=4.5,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 20,
            },
        )
        axes.center()

        x_label = MathTex("x").next_to(axes.x_axis.get_end(), DOWN)
        y_label = MathTex("y").next_to(axes.y_axis.get_end(), LEFT)

        # ------------------------------------------------------------------
        # Legend
        # ------------------------------------------------------------------
        legend = VGroup(
            MathTex("\\text{Wave } \\rightarrow \\text{ (right)}", color=BLUE, font_size=22),
            MathTex("\\text{Wave } \\leftarrow \\text{ (left)}", color=ORANGE, font_size=22),
            MathTex("\\text{Result (standing)}", color=GREEN, font_size=22),
            MathTex("\\text{Node (fixed)}", color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(RIGHT + UP, buff=0.5)

        # ------------------------------------------------------------------
        # Node markers (static)
        # ------------------------------------------------------------------
        node_positions = [n * lam / 2.0 for n in range(int(sim.L / (lam / 2.0)) + 1)]
        node_dots = VGroup()
        for nx_pos in node_positions:
            if nx_pos <= sim.L:
                node_dots.add(
                    Line(
                        axes.c2p(nx_pos, -A * 3.0),
                        axes.c2p(nx_pos, A * 3.0),
                        color=RED, stroke_width=1, stroke_opacity=0.5,
                    )
                )

        # ------------------------------------------------------------------
        # Wave curves — always_redraw, single VMobject per curve
        # ------------------------------------------------------------------
        def curve(ys_fn, color, width: int) -> VMobject:
            """Build one wave profile as a single VMobject (fast path)."""
            ys = np.asarray(ys_fn(), dtype=float)
            pts = [axes.c2p(float(x), float(y)) for x, y in zip(sim.x, ys)]
            vm = VMobject(color=color, stroke_width=width)
            vm.set_points_as_corners(pts)
            return vm

        wave_right = always_redraw(
            lambda: curve(lambda: A * np.sin(sim.k * sim.x - sim.omega * t[0]), BLUE, 2)
        )
        wave_left = always_redraw(
            lambda: curve(lambda: A * np.sin(sim.k * sim.x + sim.omega * t[0]), ORANGE, 2)
        )
        standing = always_redraw(
            lambda: curve(
                lambda: 2 * A * np.sin(sim.k * sim.x) * np.cos(sim.omega * t[0]), GREEN, 3
            )
        )

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
        self.add(axes, x_label, y_label)
        self.add(legend)
        self.add(node_dots)
        self.add(wave_right, wave_left, standing)
        self.add(driver)

        self.wait(total_time)
