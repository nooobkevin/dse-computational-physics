"""Scene — Engineering Design: pendulum clock optimisation loop.

Animate the engineering design cycle (Design → Build → Test → Analyse →
Improve) for a pendulum clock.  The goal: choose pendulum length L so the
period is T = 2.0 s.  Across 3 iterations, the student guesses L,
simulates/measures the period (with small deterministic noise), fits T² vs
L, estimates g, and refines L toward the target.

Animation pattern
-----------------
All iteration data is precomputed at scene start.  A t[0] driver advances
an integer iteration index inside always_redraw mobjects.
"""

from __future__ import annotations

import math
from typing import List, Tuple

import numpy as np
from manim import (
    Axes,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
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
    Text,
    UP,
    VGroup,
    VMobject,
    Write,
    YELLOW,
    always_redraw,
)

from physics_core.inquiry.analysis import ReferenceLinearFit


class EngineeringDesign(Scene):
    """Pendulum clock design: iterate to find L for target T = 2.0 s."""

    def construct(self) -> None:
        g_true: float = 9.81
        target_T: float = 2.0
        L_optimal: float = (target_T**2) * g_true / (4.0 * math.pi**2)
        rng = np.random.default_rng(seed=42)

        # ------------------------------------------------------------------
        # Precompute 3 design iterations
        # ------------------------------------------------------------------
        L_guesses: List[float] = [0.6, 1.2, 0.95]
        n_measure: int = 6
        iterations: List[dict] = []

        for guess in L_guesses:
            L_vals = np.linspace(max(guess - 0.3, 0.2), guess + 0.3, n_measure)
            T_true = 2.0 * math.pi * np.sqrt(L_vals / g_true)
            T_measured = T_true + rng.normal(0, 0.02, size=n_measure)
            T2_data = T_measured**2
            fit = ReferenceLinearFit(x_data=L_vals, y_data=T2_data)
            slope = fit.slope()
            g_est = 4.0 * math.pi**2 / slope
            L_rec = (target_T**2) / (4.0 * math.pi**2) * g_est

            iterations.append({
                "L_guess": guess,
                "L_vals": L_vals,
                "T2_data": T2_data,
                "slope": slope,
                "g_est": g_est,
                "L_recommended": L_rec,
            })

        total_iterations: int = len(iterations)
        total_time_scene: float = 18.0

        # ------------------------------------------------------------------
        # Animation state
        # ------------------------------------------------------------------
        t: list[float] = [0.0]

        def iter_idx() -> int:
            frac = t[0] / total_time_scene
            idx = int(round(frac * (total_iterations - 1)))
            return max(0, min(idx, total_iterations - 1))

        # ------------------------------------------------------------------
        # Title
        # ------------------------------------------------------------------
        title = Text("Engineering Design: Pendulum Clock", font_size=28, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        # Target info
        target_info = Text(
            f"Target: T = {target_T:.1f} s   |   Find L so T matches target",
            font_size=18, color=GRAY,
        )
        target_info.next_to(title, DOWN, buff=0.2)
        self.play(Write(target_info), run_time=0.6)
        self.wait(0.3)

        # ------------------------------------------------------------------
        # Design loop stages (static labels)
        # ------------------------------------------------------------------
        stage_labels = [
            ("Design", ORANGE),
            ("Build", YELLOW),
            ("Test", GREEN),
            ("Analyse", GREEN),
            ("Improve", RED),
        ]
        stage_texts: VGroup = VGroup()
        for i, (label, color) in enumerate(stage_labels):
            st = Text(f"{i+1}. {label}", font_size=16, color=color)
            st.move_to(LEFT * 5.5 + UP * (1.0 - i * 0.4))
            stage_texts.add(st)

        # ------------------------------------------------------------------
        # always_redraw: axes + data + fit line
        # ------------------------------------------------------------------
        axes = Axes(
            x_range=[0, 1.8, 0.5],
            y_range=[0, 8.0, 2.0],
            x_length=5.0,
            y_length=3.5,
            axis_config={"color": GREY_D, "include_numbers": True, "font_size": 18},
        )
        axes.move_to(RIGHT * 1.5 + DOWN * 0.2)

        x_label = MathTex("L", font_size=20, color=GRAY).next_to(
            axes.x_axis.get_end(), DOWN
        )
        y_label = MathTex("T^2", font_size=20, color=GRAY).next_to(
            axes.y_axis.get_end(), LEFT
        )

        def update_graph() -> VGroup:
            idx = iter_idx()
            data = iterations[idx]
            g = VGroup()
            Lv = data["L_vals"]
            T2v = data["T2_data"]

            # Data dots
            for Li, T2i in zip(Lv, T2v):
                g.add(Dot(axes.c2p(Li, T2i), color=ORANGE, radius=0.06))

            # Fit line
            slope = data["slope"]
            intercept = 0.0
            x_fit = np.linspace(Lv.min(), Lv.max(), 100)
            y_fit = slope * x_fit + intercept
            pts = [axes.c2p(float(x), float(y)) for x, y in zip(x_fit, y_fit)]
            vm = VMobject(color=GREEN, stroke_width=2)
            vm.set_points_as_corners(pts)
            g.add(vm)

            # Optimal L marker
            L_opt_marker = DashedLine(
                axes.c2p(L_optimal, 0),
                axes.c2p(L_optimal, slope * L_optimal),
                color=GREY_D, stroke_width=1, stroke_opacity=0.5,
            )
            if hasattr(L_opt_marker, 'set_stroke_opacity'):
                L_opt_marker.set_stroke_opacity(0.5)
            g.add(L_opt_marker)

            # Recommended L marker
            L_rec = data["L_recommended"]
            if 0 < L_rec < 2.0:
                L_rec_marker = DashedLine(
                    axes.c2p(L_rec, 0),
                    axes.c2p(L_rec, slope * L_rec),
                    color=RED, stroke_width=1, stroke_opacity=0.7,
                )
                if hasattr(L_rec_marker, 'set_stroke_opacity'):
                    L_rec_marker.set_stroke_opacity(0.7)
                g.add(L_rec_marker)

            return g

        graph_mob = always_redraw(update_graph)

        # Info panel
        def update_info() -> VGroup:
            idx = iter_idx()
            data = iterations[idx]
            g = VGroup()

            lines = [
                f"Iteration {idx + 1}:",
                f"  Guess L = {data['L_guess']:.2f} m",
                f"  Slope = {data['slope']:.3f} s²/m",
                f"  g_est = {data['g_est']:.2f} m/s²",
                f"  L* (recommended) = {data['L_recommended']:.3f} m",
                f"  L_opt (true g) = {L_optimal:.3f} m",
                "",
            ]
            if idx == 0:
                lines.append("Iteration 1: Make initial guess")
            elif idx == 1:
                lines.append("Iteration 2: Refine L toward L*")
            else:
                lines.append("Iteration 3: Converge to L_opt!")
                diff = abs(data["L_recommended"] - L_optimal)
                lines.append(f"  |L* - L_opt| = {diff:.4f} m")

            for i, line in enumerate(lines):
                txt = Text(line, font_size=14, color=GRAY)
                txt.move_to(LEFT * 5.0 + DOWN * (2.8 - i * 0.35))
                g.add(txt)

            return g

        info_mob = always_redraw(update_info)

        # ------------------------------------------------------------------
        # Driver
        # ------------------------------------------------------------------
        def driver_updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(driver_updater)

        # ------------------------------------------------------------------
        # Assemble
        # ------------------------------------------------------------------
        self.add(axes, x_label, y_label)
        self.add(stage_texts)
        self.add(graph_mob)
        self.add(info_mob)
        self.add(driver)

        self.wait(total_time_scene)