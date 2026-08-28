"""Scene C — Pressure from wall collisions: statistical view.

Shows how pressure emerges from the cumulative effect of individual
particle-wall collisions.  A histogram of collision frequency vs particle
speed is displayed alongside the computed pressure, which converges to
the ideal gas law prediction as the number of particles increases.

Physics drivers
---------------
- ReferenceGasSim from physics_core.thermal.gas_sim
- maxwell_boltzmann from physics_core.thermal.equations

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
The molecular-dynamics simulation is stepped ONCE before the animation
starts, one step per video frame, and every frame's observables (particle
positions, pressure, speed histogram, info-panel numbers) are recorded.
Each visible element is then an ``always_redraw`` mobject rebuilt every
frame from the authoritative video time ``t``, which is read from
``scene.time`` and never accumulated from updater ``dt`` values.  The
pressure trace and the MB overlay are SINGLE VMobjects built with
``set_points_as_corners``; the particles and the histogram are VGroups
rebuilt from scratch each frame.  This pattern is required because
submobjects appended to a mounted VGroup from inside an updater are never
re-rendered by the ManimCE cairo renderer, and because updaters fire
twice per frame (dt accumulation would run the simulation at 2x video
speed).
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
    Line,
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

from physics_core.thermal.equations import maxwell_boltzmann
from physics_core.thermal.gas_sim import ReferenceGasSim


class PressureStatistical(Scene):
    """Statistical view of pressure from wall collisions."""

    def construct(self) -> None:
        # ==================================================================
        # Parameters
        # ==================================================================
        N = 150
        L = 15.0
        T_init = 2.0
        dt = 0.02
        total_time = 12.0
        fps: float = 30.0
        n_frames: int = int(total_time * fps)

        # ==================================================================
        # Gas simulation
        # ==================================================================
        sim = ReferenceGasSim(
            N=N, L=L, T=T_init, m=1.0, dt=dt, dim=2,
            particle_radius=0.05, seed=42,
        )

        # ==================================================================
        # Axes — main: box visualisation
        # ==================================================================
        box_size = 4.0
        box_axes = Axes(
            x_range=[-1, L + 1, L / 2],
            y_range=[-1, L + 1, L / 2],
            x_length=box_size,
            y_length=box_size,
            axis_config={"color": GREY_D, "include_numbers": False},
        )
        box_axes.to_corner(UP + LEFT, buff=0.3)

        box_title = MathTex(
            "\\text{Gas box}", font_size=22
        ).next_to(box_axes, UP, buff=0.1)

        # ==================================================================
        # Axes — pressure vs time
        # ==================================================================
        p_axes = Axes(
            x_range=[0, total_time + 1, 2],
            y_range=[-0.5, 5.0, 1],
            x_length=5,
            y_length=3,
            axis_config={
                "color": GRAY_BROWN,
                "include_numbers": True,
                "font_size": 18,
            },
        )
        p_axes.next_to(box_axes, RIGHT, buff=0.5).shift(DOWN * 0.3)

        p_title = MathTex(
            "\\text{Pressure vs time}", font_size=20
        ).next_to(p_axes, UP, buff=0.1)

        p_t_label = MathTex("t").next_to(p_axes.x_axis.get_end(), DOWN)
        p_val_label = MathTex("P").next_to(p_axes.y_axis.get_end(), LEFT)

        # Ideal gas line (horizontal)
        P_ideal = sim.ideal_gas_pressure()
        ideal_line = Line(
            p_axes.c2p(0, P_ideal),
            p_axes.c2p(total_time, P_ideal),
            color=GREEN,
            stroke_width=2,
        )

        ideal_label = MathTex(
            "P_{\\text{ideal}} = " + f"{P_ideal:.2f}",
            color=GREEN,
            font_size=16,
        ).next_to(ideal_line, RIGHT, buff=0.1)

        # ==================================================================
        # Axes — speed distribution (right side)
        # ==================================================================
        s_axes = Axes(
            x_range=[0, 5.0, 1],
            y_range=[-0.05, 1.0, 0.2],
            x_length=3.5,
            y_length=2.5,
            axis_config={
                "color": GREY_D,
                "include_numbers": False,
                "font_size": 14,
            },
        )
        s_axes.to_corner(DOWN + RIGHT, buff=0.3)

        s_title = MathTex(
            "\\text{Speed distribution}", font_size=18
        ).next_to(s_axes, UP, buff=0.1)

        s_x_label = MathTex("v").next_to(s_axes.x_axis.get_end(), DOWN)
        s_y_label = MathTex("f(v)").next_to(s_axes.y_axis.get_end(), LEFT)

        # ==================================================================
        # Pre-compute the whole run — one sim step per video frame
        # ==================================================================
        frame_dots: list[list[np.ndarray]] = []
        frame_hist: list[list[tuple[float, float]]] = []
        p_times: list[float] = []
        p_screen: list[np.ndarray] = []
        frame_stats: list[tuple[float, float, float, float, float]] = []

        hist_stride: int = 5  # refresh the histogram every 5 frames
        last_hist: list[tuple[float, float]] = []

        for frame in range(n_frames):
            t_frame = (frame + 1) / fps
            sim.step()

            # ---- Particle positions mapped into the box axes ----
            frame_dots.append(
                [box_axes.c2p(float(px), float(py)) for px, py in sim._positions]
            )

            # ---- Pressure sample ----
            p = sim.pressure()
            p_times.append(t_frame)
            p_screen.append(p_axes.c2p(t_frame, p))

            # ---- Speed distribution (refreshed every hist_stride frames) ----
            if frame % hist_stride == 0:
                bars: list[tuple[float, float]] = []
                counts, bin_edges = sim.speed_distribution(bins=15)
                if len(counts) > 0:
                    bin_widths = bin_edges[1:] - bin_edges[:-1]
                    total = float(np.sum(counts * bin_widths))
                    if total > 0:
                        densities = counts.astype(np.float64) / total
                    else:
                        densities = counts.astype(np.float64)

                    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2.0

                    for j in range(len(bin_centres)):
                        v = float(bin_centres[j])
                        if v > 5.0:
                            continue
                        bar_h = float(densities[j]) / 1.0 * 2.5
                        if bar_h > 0.01:
                            bars.append((v, bar_h))
                last_hist = bars
            frame_hist.append(last_hist)

            # ---- Info-panel numbers ----
            frame_stats.append(
                (
                    t_frame,
                    p,
                    sim.temperature_from_ke(),
                    sim.average_speed,
                    sim.rms_speed,
                )
            )

        # MB overlay curve (temperature is constant, so compute it once)
        mb_pts: list[tuple[float, float]] = []
        for i in range(100):
            v = 5.0 * i / 100
            f = maxwell_boltzmann(v, sim.T, sim.m, kB=sim.kB, dim=sim.dim)
            mb_pts.append((v, f))
        mb_curve = VMobject(color=RED, stroke_width=2)
        mb_curve.set_points_as_corners([s_axes.c2p(v, f) for v, f in mb_pts])

        # ==================================================================
        # Info panel — pre-render one MathTex block per sampled frame
        # ==================================================================
        # LaTeX compilation is far too slow to run inside the render loop,
        # so the panel is only refreshed every info_stride frames and each
        # variant is built up-front.
        info_stride: int = 15

        def info_block(
            stats: tuple[float, float, float, float, float]
        ) -> VGroup:
            """One info panel for a sampled frame."""
            t_val, p_val, T_est, v_avg, v_rms_val = stats
            info_lines = [
                f"N = {sim.N}",
                f"t = {t_val:.2f}\\,\\text{{s}}",
                f"P = {p_val:.3f}",
                f"P_{{\\text{{ideal}}}} = {P_ideal:.3f}",
                f"T_{{\\text{{est}}}} = {T_est:.3f}",
                f"v_{{\\text{{avg}}}} = {v_avg:.3f}",
                f"v_{{\\text{{rms}}}} = {v_rms_val:.3f}",
            ]
            block = VGroup()
            for i, line in enumerate(info_lines):
                tex = MathTex(line, font_size=18)
                tex.to_corner(DOWN + LEFT, buff=0.3 + i * 0.3)
                block.add(tex)
            return block

        info_blocks: list[VGroup] = [
            info_block(frame_stats[frame])
            for frame in range(0, n_frames, info_stride)
        ]

        # ==================================================================
        # Animated elements — rebuilt every frame from the video clock
        # ==================================================================
        # Authoritative simulation time — read from the scene (video) clock.
        t: list[float] = [0.0]

        def frame_index() -> int:
            """Index of the precomputed frame matching the video clock."""
            return min(max(int(t[0] * fps), 0), n_frames - 1)

        def particles() -> VGroup:
            """Gas particles at the current frame."""
            return VGroup(
                *[
                    Dot(point, radius=0.025, color=BLUE_D)
                    for point in frame_dots[frame_index()]
                ]
            )

        def pressure_trace() -> VMobject:
            """Pressure history up to the current frame (single VMobject)."""
            n = frame_index() + 1
            vm = VMobject(color=BLUE, stroke_width=2)
            if n >= 2:
                vm.set_points_as_corners(p_screen[:n])
            return vm

        def speed_hist() -> VGroup:
            """Measured speed histogram at the current frame."""
            return VGroup(
                *[
                    Line(
                        s_axes.c2p(v, 0),
                        s_axes.c2p(v, h),
                        color=BLUE_D,
                        stroke_width=5,
                    )
                    for v, h in frame_hist[frame_index()]
                ]
            )

        def info_panel() -> VGroup:
            """Pre-rendered info panel for the current frame."""
            return info_blocks[frame_index() // info_stride].copy()

        particle_dots = always_redraw(particles)
        p_trace = always_redraw(pressure_trace)
        s_hist = always_redraw(speed_hist)
        info_text = always_redraw(info_panel)

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
        self.add(box_axes, box_title)
        self.add(p_axes, p_title, p_t_label, p_val_label)
        self.add(ideal_line, ideal_label)
        self.add(s_axes, s_title, s_x_label, s_y_label)
        self.add(mb_curve)
        self.add(particle_dots, p_trace, s_hist, info_text)
        self.add(driver)

        self.wait(total_time)
