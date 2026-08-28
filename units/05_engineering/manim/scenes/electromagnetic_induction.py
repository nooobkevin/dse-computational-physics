"""Scene — Electromagnetic induction: bar magnet moving toward/away from a coil.

Shows:
- Bar magnet approaching/receding from a coil
- Magnetic flux graph (Φ vs t)
- Induced emf graph (ε vs t) with positive/negative peaks
- Lenz direction arrows on the coil current

Physics driver
--------------
ReferenceInductionCoil from physics_core.engineering.induction provides
magnetic flux, Faraday's law, and Lenz's law.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    BLUE_D,
    DOWN,
    GRAY,
    GREEN,
    GREY_D,
    LEFT,
    MathTex,
    Mobject,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    UP,
    VMobject,
    YELLOW,
    always_redraw,
)

from physics_core.engineering.induction import ReferenceInductionCoil


class ElectromagneticInduction(Scene):
    """Bar magnet and coil — flux, induced emf, Lenz's law."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        coil = ReferenceInductionCoil(B=1.0, A=0.01, magnet_position=-3.0)
        total_time: float = 14.0

        t: list[float] = [0.0]

        # Data arrays for graphing
        times: list[float] = []
        fluxes: list[float] = []
        emfs: list[float] = []

        # ------------------------------------------------------------------
        # Coil (schematic)
        # ------------------------------------------------------------------
        coil_x = 0.0
        coil_half = 0.5

        coil_display = VMobject(color=ORANGE, stroke_width=3)
        coil_pts = []
        for i in range(6):
            x = coil_x - 0.3 + i * 0.12
            coil_pts.append(np.array([x, coil_half, 0]))
            coil_pts.append(np.array([x + 0.06, -coil_half, 0]))
        coil_display.set_points_as_corners(coil_pts)

        coil_label = MathTex("\\text{Coil}", font_size=20, color=ORANGE).next_to(
            np.array([coil_x, coil_half + 0.2, 0]), UP, buff=0.1
        )

        # ------------------------------------------------------------------
        # Magnet (moves along x-axis)
        # ------------------------------------------------------------------
        def magnet() -> VMobject:
            pos = coil.state["magnet_position"]
            vm = VMobject(color=RED, stroke_width=2)
            vm.set_fill(RED, opacity=0.6)
            vm.set_points_as_corners([
                np.array([pos - 0.3, -0.3, 0]),
                np.array([pos + 0.3, -0.3, 0]),
                np.array([pos + 0.3, 0.3, 0]),
                np.array([pos - 0.3, 0.3, 0]),
                np.array([pos - 0.3, -0.3, 0]),
            ])
            return vm

        magnet_vis = always_redraw(magnet)

        magnet_label = always_redraw(lambda: MathTex(
            "\\text{Magnet}", font_size=18, color=RED,
        ).next_to(
            np.array([coil.state["magnet_position"], 0.5, 0]), UP, buff=0.1
        ))

        # ------------------------------------------------------------------
        # Lenz direction indicator
        # ------------------------------------------------------------------
        def lenz_arrow() -> VMobject:
            vm = VMobject(color=YELLOW, stroke_width=3)
            if len(times) >= 2:
                direction = coil.lenz_direction(times[-2], times[-1])
            else:
                direction = "CW"
            # Arrow around coil
            if direction == "CCW":
                pts = [
                    np.array([-0.4, -0.6, 0]),
                    np.array([-0.4, 0.6, 0]),
                ]
            else:
                pts = [
                    np.array([0.4, 0.6, 0]),
                    np.array([0.4, -0.6, 0]),
                ]
            vm.set_points_as_corners(pts)
            return vm

        lenz_vis = always_redraw(lenz_arrow)

        lenz_label = always_redraw(lambda: MathTex(
            "I_{\\text{ind}}", font_size=18, color=YELLOW,
        ).next_to(np.array([0.6, 0.7, 0]), UP, buff=0.1))

        # ------------------------------------------------------------------
        # Graphs (right side)
        # ------------------------------------------------------------------
        graph_x0 = 3.0
        graph_y0 = 1.5
        graph_w = 3.5
        graph_h = 1.2

        # Flux graph (top)
        flux_axes_label = MathTex("\\Phi", font_size=18, color=BLUE).next_to(
            np.array([graph_x0 + graph_w + 0.2, graph_y0, 0]), RIGHT, buff=0.1
        )

        def flux_graph() -> VMobject:
            vm = VMobject(color=BLUE, stroke_width=2)
            if len(times) < 2:
                return vm
            pts = []
            for i, ti in enumerate(times):
                x = graph_x0 + (ti - times[0]) / (times[-1] - times[0] + 1e-9) * graph_w
                y = graph_y0 + fluxes[i] / (max(abs(f) for f in fluxes) + 1e-9) * graph_h * 0.8
                pts.append(np.array([x, y, 0]))
            if pts:
                vm.set_points_as_corners(pts)
            return vm

        flux_curve = always_redraw(flux_graph)

        # Emf graph (bottom)
        emf_graph_y0 = -1.8
        emf_axes_label = MathTex("\\varepsilon", font_size=18, color=RED).next_to(
            np.array([graph_x0 + graph_w + 0.2, emf_graph_y0, 0]), RIGHT, buff=0.1
        )

        def emf_graph() -> VMobject:
            vm = VMobject(color=RED, stroke_width=2)
            if len(times) < 2:
                return vm
            pts = []
            for i, ti in enumerate(times):
                x = graph_x0 + (ti - times[0]) / (times[-1] - times[0] + 1e-9) * graph_w
                y = emf_graph_y0 + emfs[i] / (max(abs(e) for e in emfs) + 1e-9) * graph_h * 0.8
                pts.append(np.array([x, y, 0]))
            if pts:
                vm.set_points_as_corners(pts)
            return vm

        emf_curve = always_redraw(emf_graph)

        # Zero lines
        flux_zero = VMobject(color=GREY_D, stroke_width=1, stroke_opacity=0.5)
        flux_zero.set_points_as_corners([
            np.array([graph_x0, graph_y0, 0]),
            np.array([graph_x0 + graph_w, graph_y0, 0]),
        ])

        emf_zero = VMobject(color=GREY_D, stroke_width=1, stroke_opacity=0.5)
        emf_zero.set_points_as_corners([
            np.array([graph_x0, emf_graph_y0, 0]),
            np.array([graph_x0 + graph_w, emf_graph_y0, 0]),
        ])

        # ------------------------------------------------------------------
        # Info display
        # ------------------------------------------------------------------
        flux_val = always_redraw(lambda: MathTex(
            f"\\Phi = {coil.state['flux']:.6f}\\,\\text{{Wb}}",
            font_size=18, color=BLUE,
        ).to_corner(UP + RIGHT, buff=0.3))

        emf_val = always_redraw(lambda: MathTex(
            f"\\varepsilon = {coil.state['emf']:.4f}\\,\\text{{V}}",
            font_size=18, color=RED,
        ).next_to(flux_val, DOWN, buff=0.1, aligned_edge=LEFT))

        lenz_dir = always_redraw(lambda: MathTex(
            f"\\text{{Lenz: }} "
            f"{coil.lenz_direction(max(coil.state['flux_prev'], 1e-9), max(coil.state['flux'], 1e-9))}",
            font_size=18, color=YELLOW,
        ).next_to(emf_val, DOWN, buff=0.1, aligned_edge=LEFT))

        # ------------------------------------------------------------------
        # Physics driver
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # Simulation step
        def sim_updater(_mob: Mobject, dt: float) -> None:
            h = min(dt, 1.0 / 30.0)
            # Oscillate the magnet back and forth
            speed = 0.3
            coil.magnet_position = -2.0 + 4.0 * abs(
                math.sin(self.time * speed * math.pi)
            )
            coil.step(h)
            times.append(self.time)
            fluxes.append(coil.state["flux"])
            emfs.append(coil.state["emf"])
            # Keep data manageable
            if len(times) > 500:
                times.pop(0)
                fluxes.pop(0)
                emfs.pop(0)

        sim_driver = Mobject()
        sim_driver.add_updater(sim_updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        self.add(coil_display, coil_label)
        self.add(magnet_vis, magnet_label)
        self.add(lenz_vis, lenz_label)
        self.add(flux_zero, emf_zero)
        self.add(flux_curve, flux_axes_label)
        self.add(emf_curve, emf_axes_label)
        self.add(flux_val, emf_val, lenz_dir)
        self.add(driver, sim_driver)

        self.wait(total_time)