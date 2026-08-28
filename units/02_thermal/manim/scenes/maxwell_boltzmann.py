"""Scene A — Maxwell-Boltzmann speed distribution with temperature dependence.

Shows the theoretical Maxwell-Boltzmann speed distribution curve for an
ideal gas at different temperatures, alongside the measured speed
distribution of simulated gas particles.  As temperature increases, the
distribution broadens and the most probable speed shifts to higher values.

Physics drivers
---------------
- maxwell_boltzmann from physics_core.thermal.equations
- ReferenceGasSim from physics_core.thermal.gas_sim

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
The gas simulation is run ONCE before the animation starts: for every
temperature in the cycle the sim is re-seeded and stepped, and the
measured speed histogram is stored per frame.  The theoretical MB curves
are likewise precomputed per temperature.  Each visible element is an
``always_redraw`` mobject that rebuilds itself every frame from the
authoritative video time ``t``, which is read from ``scene.time`` and
never accumulated from updater ``dt`` values.  Each MB curve is a SINGLE
VMobject built with ``set_points_as_corners`` (the active temperature's
curve sweeps in from the left while previously drawn temperatures stay
on screen for comparison), and the histogram is a VGroup rebuilt from
scratch each frame.  This pattern is required because submobjects
appended to a mounted VGroup from inside an updater are never
re-rendered by the ManimCE cairo renderer, and because updaters fire
twice per frame (dt accumulation would run the simulation at 2x video
speed).
"""

from __future__ import annotations

from bisect import bisect_right

import numpy as np
from manim import (
    Axes,
    BLUE,
    BLUE_D,
    DOWN,
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


class MaxwellBoltzmann(Scene):
    """Animate the MB speed distribution as temperature changes."""

    def construct(self) -> None:
        # ==================================================================
        # Parameters
        # ==================================================================
        m = 1.0
        kB = 1.0
        dim = 2
        temperatures = [0.5, 1.0, 2.0, 4.0]
        v_max_display = 5.0
        n_curve_steps = 200
        colors = [BLUE_D, BLUE, GREEN, RED]

        # Pre-compute MB curves for each temperature
        mb_curves: dict[float, list[tuple[float, float]]] = {}
        for temp_val in temperatures:
            pts: list[tuple[float, float]] = []
            for i in range(n_curve_steps):
                v = v_max_display * i / n_curve_steps
                f = maxwell_boltzmann(v, temp_val, m, kB=kB, dim=dim)
                pts.append((v, f))
            mb_curves[temp_val] = pts

        # ==================================================================
        # Axes
        # ==================================================================
        axes = (
            Axes(
                x_range=[0, v_max_display + 0.5, 1],
                y_range=[-0.05, 1.0, 0.2],
                x_length=10,
                y_length=5,
                axis_config={
                    "color": GRAY_BROWN,
                    "include_numbers": True,
                    "font_size": 24,
                },
            )
            .center()
            .shift(DOWN * 0.3)
        )

        v_label = MathTex("v").next_to(axes.x_axis.get_end(), DOWN)
        f_label = MathTex("f(v)").next_to(axes.y_axis.get_end(), LEFT)

        # ==================================================================
        # Timing — each temperature holds the stage for frames_per_T frames
        # ==================================================================
        frames_per_T: int = 150
        fps: float = 30.0
        seconds_per_T: float = frames_per_T / fps
        total_duration: float = len(temperatures) * seconds_per_T

        # ==================================================================
        # Gas simulation for measured distribution — stepped ONCE up-front
        # ==================================================================
        # For each temperature the sim is re-initialised (same seed) and
        # stepped once per video frame; the measured histogram of every
        # frame is stored so the animation only has to look it up.
        hist_frames: dict[float, list[list[tuple[float, float]]]] = {}
        for temp_val in temperatures:
            sim = ReferenceGasSim(
                N=200, L=15.0, T=temp_val, m=m, dt=0.02, dim=dim,
                particle_radius=0.05, seed=42,
            )
            per_temp: list[list[tuple[float, float]]] = []
            for _ in range(frames_per_T):
                sim.step()
                counts, bin_edges = sim.speed_distribution(bins=20)
                bars: list[tuple[float, float]] = []
                if len(counts) > 0:
                    bin_widths = bin_edges[1:] - bin_edges[:-1]
                    total = float(np.sum(counts * bin_widths))
                    if total > 0:
                        densities = counts.astype(np.float64) / total
                    else:
                        densities = counts.astype(np.float64)

                    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2.0

                    for j in range(len(bin_centres)):
                        if bin_centres[j] > v_max_display:
                            continue
                        bar_h = float(densities[j]) / 1.0 * 5.0  # scale to axes
                        if bar_h > 0.01:
                            bars.append((float(bin_centres[j]), bar_h))
                per_temp.append(bars)
            hist_frames[temp_val] = per_temp

        # ==================================================================
        # Legend
        # ==================================================================
        legend_items = VGroup()
        for i, T in enumerate(temperatures):
            item = MathTex(
                f"T = {T}", color=colors[i], font_size=22
            )
            legend_items.add(item)
        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend_items.to_corner(RIGHT + UP, buff=0.5)

        # ==================================================================
        # Temperature labels — one per temperature, shown by opacity
        # ==================================================================
        # Pre-built so no LaTeX is compiled inside the render loop.
        T_labels: list[MathTex] = [
            MathTex(
                f"T = {T:.1f}", color=colors[i], font_size=28
            ).to_corner(UP + LEFT, buff=0.5)
            for i, T in enumerate(temperatures)
        ]

        # ==================================================================
        # Animated elements — rebuilt every frame from the video clock
        # ==================================================================
        # Authoritative simulation time — read from the scene (video) clock.
        t: list[float] = [0.0]

        def active_index() -> int:
            """Index of the temperature currently on stage."""
            idx = int(t[0] / seconds_per_T)
            return min(idx, len(temperatures) - 1)

        # MB curve — progressively revealed single VMobject.
        curve_vs: dict[float, list[float]] = {
            T: [v for v, _ in mb_curves[T]] for T in temperatures
        }
        curve_pts: dict[float, list[np.ndarray]] = {
            T: [axes.c2p(v, f) for v, f in mb_curves[T]] for T in temperatures
        }

        def mb_trace() -> VGroup:
            """Curves for all temperatures shown so far, current one sweeping."""
            idx = active_index()
            local_t = t[0] - idx * seconds_per_T
            # Sweep the curve across the first 60% of this temperature's slot.
            frac = min(local_t / (0.6 * seconds_per_T), 1.0)

            curves = VGroup()
            for j in range(idx + 1):
                T_j = temperatures[j]
                vs = curve_vs[T_j]
                limit = frac * v_max_display if j == idx else v_max_display
                n = bisect_right(vs, limit)
                if n >= 2:
                    vm = VMobject(color=colors[j], stroke_width=3)
                    vm.set_points_as_corners(list(curve_pts[T_j][:n]))
                    curves.add(vm)
            return curves

        def hist_group() -> VGroup:
            """Measured speed histogram for the current frame."""
            idx = active_index()
            T_current = temperatures[idx]
            local_t = t[0] - idx * seconds_per_T
            frame = min(int(local_t * fps), frames_per_T - 1)
            frame = max(frame, 0)
            return VGroup(
                *[
                    Line(
                        axes.c2p(v, 0),
                        axes.c2p(v, h),
                        color=GREY_D,
                        stroke_width=4,
                    )
                    for v, h in hist_frames[T_current][frame]
                ]
            )

        def T_label() -> MathTex:
            """A copy of the pre-built label for the current temperature."""
            return T_labels[active_index()].copy()

        mb_curve_mob = always_redraw(mb_trace)
        hist_bars = always_redraw(hist_group)
        T_label_mob = always_redraw(T_label)

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
        self.add(axes, v_label, f_label)
        self.add(legend_items)
        self.add(T_label_mob)
        self.add(hist_bars)
        self.add(mb_curve_mob)
        self.add(driver)

        self.wait(total_duration)
