"""Scene D — Random walk of molecules (gas diffusion model).

Shows many walkers starting at the origin on a 2D grid, spreading out
over time like gas molecules diffusing.  A live RMS-radius ring expands
as sqrt(t), demonstrating that RMS displacement grows as sqrt(N).

Physics driver
--------------
RandomWalk from physics_core.thermal.random_walk

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
The random walk is precomputed ONCE before the animation starts: all
walker positions at every step are stored.  Each visible element is an
``always_redraw`` mobject rebuilt every frame from the authoritative
video time ``t``, which is read from ``scene.time`` and never accumulated
from updater ``dt`` values.  The RMS ring is a SINGLE VMobject built with
``set_points_as_corners``; the walker dots are a VGroup rebuilt from
scratch each frame.  This pattern is required because submobjects
appended to a mounted VGroup from inside an updater are never re-rendered
by the ManimCE cairo renderer, and because updaters fire twice per frame
(dt accumulation would run the simulation at 2x video speed).
"""

from __future__ import annotations

import numpy as np
from manim import (
    Axes,
    BLUE,
    BLUE_D,
    DOWN,
    Dot,
    GRAY_BROWN,
    GREEN,
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

from physics_core.thermal.random_walk import RandomWalk


class RandomWalkScene(Scene):
    """Animate many random walkers spreading from the origin."""

    def construct(self) -> None:
        # ==================================================================
        # Parameters
        # ==================================================================
        n_walkers = 200
        n_steps = 150
        step_length = 0.3
        total_time = 10.0
        fps: float = 30.0
        n_frames: int = int(total_time * fps)

        # ==================================================================
        # Pre-compute the random walk
        # ==================================================================
        rw = RandomWalk(
            n_walkers=n_walkers,
            n_steps=n_steps,
            step_length=step_length,
            dim=2,
            seed=42,
        )

        # Frame → step mapping must be ceil so the LAST frame reaches step
        # N (int() truncation never displayed the final step, making the
        # on-screen √N inconsistent with the N in the info panel).
        steps_per_frame = n_steps / n_frames

        # Pre-compute walker positions for each frame
        frame_positions: list[np.ndarray] = []
        for frame in range(n_frames):
            step_idx = min(int(np.ceil(frame * steps_per_frame)), n_steps)
            frame_positions.append(rw.positions[:, step_idx, :].copy())

        # Pre-compute RMS values for each frame
        frame_rms: list[float] = []
        for frame in range(n_frames):
            step_idx = min(int(np.ceil(frame * steps_per_frame)), n_steps)
            frame_rms.append(float(rw.rms[step_idx]))

        # Theoretical RMS at final step
        rms_theoretical = float(rw.rms_theoretical[-1])

        # ==================================================================
        # Axes — the grid showing the walker area
        # ==================================================================
        # Determine display range from max RMS
        max_rms = float(rw.rms[-1])
        display_range = max_rms * 1.5
        display_range = max(display_range, 3.0)

        # Clean integer tick grid: the display range is rounded up to a whole
        # multiple of the tick step so no tick value ever needs decimals.
        tick_step = 1.0
        display_range = max(
            tick_step * int(np.ceil(max_rms * 1.5 / tick_step)), 3.0
        )

        axes = Axes(
            x_range=[-display_range, display_range, tick_step],
            y_range=[-display_range, display_range, tick_step],
            x_length=8,
            y_length=8,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 16,
                "decimal_number_config": {"num_decimal_places": 0},
            },
        )
        axes.center()

        # ==================================================================
        # Labels
        # ==================================================================
        title = MathTex(
            "\\text{Random walk — gas molecule diffusion}",
            font_size=28,
        ).to_corner(UP, buff=0.3)

        # ==================================================================
        # Legend / info panel (right side)
        # ==================================================================
        info_lines = VGroup(
            MathTex(f"N_{{\\text{{walkers}}}} = {n_walkers}", font_size=20),
            MathTex(f"N_{{\\text{{steps}}}} = {n_steps}", font_size=20),
            MathTex(f"s = {step_length}", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        info_lines.to_corner(RIGHT + UP, buff=0.5)

        # ==================================================================
        # RMS label — shows current RMS and theoretical sqrt(N) relation
        # ==================================================================
        # Authoritative simulation time — read from the scene (video) clock.
        t: list[float] = [0.0]

        rms_label = MathTex(
            "\\text{RMS} = s \\sqrt{N}",
            color=RED,
            font_size=24,
        ).to_corner(DOWN + LEFT, buff=0.5)

        # ==================================================================
        # Animated elements — rebuilt every frame from the video clock
        # ==================================================================
        def frame_index() -> int:
            """Index of the precomputed frame matching the video clock."""
            return min(max(int(t[0] * fps), 0), n_frames - 1)

        def walker_dots() -> VGroup:
            """Walker positions at the current frame."""
            idx = frame_index()
            pts = frame_positions[idx]
            return VGroup(
                *[
                    Dot(
                        axes.c2p(float(px), float(py)),
                        radius=0.015,
                        color=BLUE_D,
                        fill_opacity=0.6,
                    )
                    for px, py in pts
                ]
            )

        def rms_ring() -> VMobject:
            """RMS-radius ring at the current frame (single VMobject)."""
            idx = frame_index()
            r = frame_rms[idx]
            if r < 0.01:
                return VMobject(color=RED, stroke_width=2)

            n_pts = 80
            angles = np.linspace(0, 2 * np.pi, n_pts)
            pts = [
                axes.c2p(r * np.cos(theta), r * np.sin(theta))
                for theta in angles
            ]
            vm = VMobject(color=RED, stroke_width=3)
            vm.set_points_as_corners(pts)
            return vm

        def rms_label_text() -> MathTex:
            """RMS law plus the value measured from the walker cloud."""
            idx = frame_index()
            r = frame_rms[idx]
            n = min(int(np.ceil(idx * steps_per_frame)), n_steps)
            return MathTex(
                f"\\text{{RMS}} = s \\sqrt{{N}} \\approx {r:.2f}"
                f" \\quad (N = {n})",
                color=RED,
                font_size=22,
            ).to_corner(DOWN + LEFT, buff=0.5)

        walkers = always_redraw(walker_dots)
        ring = always_redraw(rms_ring)
        rms_formula = always_redraw(rms_label_text)

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
        self.add(axes)
        self.add(title)
        self.add(info_lines)
        self.add(walkers)
        self.add(ring)
        self.add(rms_formula)
        self.add(driver)

        self.wait(total_time)