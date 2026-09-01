"""Scene — Bernoulli's principle and pitot tube visualisation.

Shows a horizontal tube with a constriction:
- Streamlines speed up in the throat (continuity)
- Pressure drops where velocity increases (Bernoulli)
- A pitot tube shows stagnation pressure → speed readout

Physics driver
--------------
ReferenceFluidFlow from physics_core.engineering.fluid provides
continuity velocity, Bernoulli pressure, and pitot speed.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
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
    VGroup,
    VMobject,
    YELLOW,
    always_redraw,
)

from physics_core.engineering.fluid import ReferenceFluidFlow


class BernoulliPitot(Scene):
    """Horizontal tube with constriction — Bernoulli effect and pitot tube."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics
        # ------------------------------------------------------------------
        A1 = 0.1          # m²
        A2 = 0.04         # m² (constriction)
        v1 = 1.5          # m/s
        P1 = 101325.0     # Pa (atmospheric)
        rho = 1000.0      # kg/m³ (water)
        h1 = h2 = 0.0     # horizontal

        sim = ReferenceFluidFlow(A1=A1, A2=A2, v1=v1, P1=P1, h1=h1, h2=h2, rho=rho)
        sim.step()
        v2 = sim.state["v2"]
        P2 = sim.state["P2"]
        # Venturi: pressure drop between the two different cross-sections.
        delta_P = P1 - P2
        # Pitot: stagnation minus static pressure at the SAME point (wide
        # section), so the recovered speed is exactly v1.
        delta_P_stag = 0.5 * rho * v1 * v1
        pitot_v = sim.pitot_speed(delta_P_stag, rho)

        t: list[float] = [0.0]
        total_time: float = 8.0

        # ------------------------------------------------------------------
        # Tube geometry (display units)
        # ------------------------------------------------------------------
        cx, cy = 0.0, 0.0
        tube_half_len = 4.0
        tube_h1 = 0.6  # wide section half-height
        tube_h2 = 0.3  # narrow section half-height
        throat_start = -0.8
        throat_end = 0.8

        def tube_profile(x: float) -> float:
            """Tube half-height at position x."""
            if x < throat_start:
                return tube_h1
            elif x > throat_end:
                return tube_h1
            else:
                # Linear taper
                frac = (x - throat_start) / (throat_end - throat_start)
                return tube_h1 - frac * (tube_h1 - tube_h2)

        # Tube outline (static)
        tube_top = VMobject(color=GRAY, stroke_width=2)
        tube_bot = VMobject(color=GRAY, stroke_width=2)
        xs = np.linspace(-tube_half_len, tube_half_len, 200)
        top_pts = [np.array([x, tube_profile(x), 0]) for x in xs]
        bot_pts = [np.array([x, -tube_profile(x), 0]) for x in xs]
        tube_top.set_points_as_corners(top_pts)
        tube_bot.set_points_as_corners(bot_pts)

        # Labels for wide / narrow sections
        wide_label = MathTex("A_1", font_size=24, color=BLUE).move_to(
            np.array([-2.5, tube_h1 + 0.3, 0])
        )
        narrow_label = MathTex("A_2", font_size=24, color=BLUE).move_to(
            np.array([0.0, tube_h2 + 0.3, 0])
        )

        # ------------------------------------------------------------------
        # Streamlines — animated particles
        # ------------------------------------------------------------------
        n_streams = 7
        stream_positions: list[list[float]] = [
            [np.random.uniform(-tube_half_len, throat_start)]
            for _ in range(n_streams)
        ]

        def streamlines() -> VMobject:
            vm = VMobject(color=BLUE, stroke_width=1.5, stroke_opacity=0.6)
            pts = []
            for spos in stream_positions:
                x = spos[0]
                # Update position based on speed
                if x < throat_start:
                    dx = 0.02 * v1
                elif x > throat_end:
                    dx = 0.02 * v1
                else:
                    frac = (x - throat_start) / (throat_end - throat_start)
                    local_v = v1 + frac * (v2 - v1)
                    dx = 0.02 * local_v
                spos[0] += dx
                if spos[0] > tube_half_len:
                    spos[0] = -tube_half_len
                y = tube_profile(spos[0]) * 0.6 * (
                    1.0 - 2.0 * (stream_positions.index(spos) / n_streams)
                )
                pts.append(np.array([spos[0], y, 0]))
            vm.set_points_as_corners(pts)
            return vm

        stream_vis = always_redraw(streamlines)

        # ------------------------------------------------------------------
        # Pressure display (manometer-style columns)
        # ------------------------------------------------------------------
        def manometer() -> VMobject:
            vm = VMobject(color=RED, stroke_width=3)
            # P1 column (left)
            p1_height = P1 / 101325.0 * 1.0
            # P2 column (right, throat)
            p2_height = P2 / 101325.0 * 1.0
            pts = [
                np.array([-2.5, -tube_h1 - p1_height - 0.2, 0]),
                np.array([-2.5, -tube_h1, 0]),
                np.array([0.0, -tube_h1, 0]),
                np.array([0.0, -tube_h2 - p2_height - 0.2, 0]),
            ]
            vm.set_points_as_corners(pts)
            return vm

        manometer_vis = always_redraw(manometer)

        # ------------------------------------------------------------------
        # Pitot tube display (right side)
        # ------------------------------------------------------------------
        pitot_label = MathTex(
            f"\\text{{Pitot: }} v_1 = {pitot_v:.2f}\\,\\text{{m/s}}",
            font_size=22, color=GREEN,
        ).to_corner(DOWN + RIGHT, buff=0.5)

        pitot_info = MathTex(
            f"\\Delta P_{{\\text{{stag}}}} = \\tfrac{{1}}{{2}}\\rho v_1^2"
            f" = {delta_P_stag:.0f}\\,\\text{{Pa}}",
            font_size=20, color=ORANGE,
        ).next_to(pitot_label, UP, buff=0.2)

        venturi_info = MathTex(
            f"\\text{{Venturi: }} \\Delta P = P_1 - P_2 = {delta_P:.0f}\\,\\text{{Pa}}",
            font_size=20, color=GRAY,
        ).next_to(pitot_info, UP, buff=0.2)

        # ------------------------------------------------------------------
        # Formula display
        # ------------------------------------------------------------------
        continuity_formula = MathTex(
            f"A_1 v_1 = A_2 v_2 \\quad ({A1})({v1}) = ({A2})({v2:.3f})",
            font_size=20, color=GREEN,
        )

        bernoulli_formula = MathTex(
            f"P_1 + \\frac{{1}}{{2}}\\rho v_1^2 = P_2 + \\frac{{1}}{{2}}\\rho v_2^2",
            font_size=20, color=YELLOW,
        )

        VGroup(continuity_formula, bernoulli_formula).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1
        ).to_corner(DOWN + LEFT, buff=0.3)

        # ------------------------------------------------------------------
        # Physics driver
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        self.add(tube_top, tube_bot)
        self.add(wide_label, narrow_label)
        self.add(stream_vis)
        self.add(manometer_vis)
        self.add(continuity_formula, bernoulli_formula)
        self.add(pitot_label, pitot_info, venturi_info)
        self.add(driver)

        self.wait(total_time)