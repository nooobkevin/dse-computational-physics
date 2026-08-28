"""Scene — Orbital motion of a satellite around a central body.

Shows a satellite in circular orbit with:
- Velocity vector (tangent to orbit)
- Gravitational force vector (toward centre)
- KE / GPE / total-energy bar chart showing conservation
- v_orb and v_esc labels

Physics driver
--------------
ReferenceOrbitalBody from physics_core.engineering.orbital provides
the gravitational force, orbital velocity, escape velocity, and energy.
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

from physics_core.engineering.orbital import ReferenceOrbitalBody


class OrbitalMotion(Scene):
    """Satellite in circular orbit — vectors and energy bar chart."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        M = 5.972e24    # Earth mass (kg)
        r = 7.0e6       # orbital radius (m)
        m = 1000.0      # satellite mass (kg)
        v_orb = math.sqrt(6.67430e-11 * M / r)

        sim = ReferenceOrbitalBody(
            M=M, m=m,
            x=r, y=0.0,
            vx=0.0, vy=v_orb,
        )

        total_time: float = 12.0

        # Authoritative simulation time
        t: list[float] = [0.0]

        # Scale factor for display: 1 m = 1e-7 manim units
        scale: float = 1e-7
        orbit_radius_display: float = r * scale  # ~0.7

        # ------------------------------------------------------------------
        # Axes for orbit (centred)
        # ------------------------------------------------------------------
        origin = np.array([-2.5, 0.0, 0.0])

        # Central body (Earth)
        earth = VMobject()
        earth.set_points_as_corners([
            origin + np.array([dx, dy, 0]) * 0.2
            for dx, dy in [
                (0.2, 0), (0, 0.2), (-0.2, 0), (0, -0.2), (0.2, 0),
            ]
        ])
        earth.set_color(BLUE_D)
        earth.set_fill(BLUE_D, opacity=0.6)
        earth.set_stroke(width=1)

        earth_label = MathTex("\\text{Earth}", font_size=24, color=BLUE_D)
        earth_label.next_to(origin, DOWN, buff=0.1)

        # Orbit path (circle)
        orbit_path = VMobject(color=GRAY, stroke_width=1, stroke_opacity=0.5)
        pts = [
            origin + np.array([
                orbit_radius_display * math.cos(theta),
                orbit_radius_display * math.sin(theta),
                0,
            ])
            for theta in np.linspace(0, 2 * math.pi, 100)
        ]
        orbit_path.set_points_as_corners(pts)

        # ------------------------------------------------------------------
        # Satellite position
        # ------------------------------------------------------------------
        def satellite_pos() -> np.ndarray:
            """Satellite position in display coordinates."""
            x, y = sim.position()
            return origin + np.array([x * scale, y * scale, 0])

        # Satellite dot
        satellite_dot = always_redraw(
            lambda: VMobject().set_points_as_corners(
                [satellite_pos(), satellite_pos()]
            ).set_color(YELLOW).set_stroke(width=8)
        )

        # ------------------------------------------------------------------
        # Velocity vector (tangent)
        # ------------------------------------------------------------------
        def velocity_arrow() -> VMobject:
            pos = satellite_pos()
            vx, vy = sim.state["vx"], sim.state["vy"]
            v_mag = math.hypot(vx, vy)
            if v_mag < 1:
                v_mag = 1
            arrow_len = 1.0
            end = pos + np.array([
                vx / v_mag * arrow_len,
                vy / v_mag * arrow_len,
                0,
            ])
            vm = VMobject(color=GREEN, stroke_width=3)
            vm.set_points_as_corners([pos, end])
            return vm

        v_arrow = always_redraw(velocity_arrow)

        v_label = MathTex("v", font_size=22, color=GREEN)
        v_label.add_updater(lambda m: m.next_to(
            satellite_pos() + np.array([
                sim.state["vx"] / max(sim.speed, 1) * 1.1,
                sim.state["vy"] / max(sim.speed, 1) * 1.1,
                0,
            ]), UP, buff=0.1
        ))

        # ------------------------------------------------------------------
        # Gravitational force vector (toward centre)
        # ------------------------------------------------------------------
        def force_arrow() -> VMobject:
            pos = satellite_pos()
            dx = origin[0] - pos[0]
            dy = origin[1] - pos[1]
            d = math.hypot(dx, dy)
            if d < 0.01:
                d = 0.01
            arrow_len = 0.8
            end = pos + np.array([dx / d * arrow_len, dy / d * arrow_len, 0])
            vm = VMobject(color=RED, stroke_width=3)
            vm.set_points_as_corners([pos, end])
            return vm

        f_arrow = always_redraw(force_arrow)

        f_label = MathTex("F_g", font_size=22, color=RED)
        f_label.add_updater(lambda m: m.next_to(
            satellite_pos() + np.array([
                -(satellite_pos()[0] - origin[0]) / max(
                    math.hypot(satellite_pos()[0] - origin[0], satellite_pos()[1] - origin[1]), 0.01
                ) * 0.9,
                -(satellite_pos()[1] - origin[1]) / max(
                    math.hypot(satellite_pos()[0] - origin[0], satellite_pos()[1] - origin[1]), 0.01
                ) * 0.9,
                0,
            ]), DOWN, buff=0.1
        ))

        # ------------------------------------------------------------------
        # Energy bar chart (right side)
        # ------------------------------------------------------------------
        bar_x = 3.5
        bar_width = 0.6
        max_energy = 2.5e11  # display scale

        def energy_bars() -> VMobject:
            energy = sim.energy_components()
            ke_frac = max(energy["kinetic"] / max_energy, 0.01)
            gpe_frac = max(abs(energy["potential"]) / max_energy, 0.01)
            total_frac = max(abs(energy["total"]) / max_energy, 0.01)

            bars = VMobject()
            pts = []

            # KE bar (green) — positive
            y_top_ke = 1.5
            y_bot_ke = y_top_ke - ke_frac * 2.5
            pts += [
                np.array([bar_x - bar_width/2, y_bot_ke, 0]),
                np.array([bar_x + bar_width/2, y_bot_ke, 0]),
                np.array([bar_x + bar_width/2, y_top_ke, 0]),
                np.array([bar_x - bar_width/2, y_top_ke, 0]),
                np.array([bar_x - bar_width/2, y_bot_ke, 0]),
            ]

            # GPE bar (red) — negative (below zero)
            y_top_gpe = 0
            y_bot_gpe = -gpe_frac * 2.5
            bar_x2 = bar_x + bar_width + 0.3
            pts += [
                np.array([bar_x2 - bar_width/2, y_bot_gpe, 0]),
                np.array([bar_x2 + bar_width/2, y_bot_gpe, 0]),
                np.array([bar_x2 + bar_width/2, y_top_gpe, 0]),
                np.array([bar_x2 - bar_width/2, y_top_gpe, 0]),
                np.array([bar_x2 - bar_width/2, y_bot_gpe, 0]),
            ]

            # Total bar (blue)
            bar_x3 = bar_x + 2 * (bar_width + 0.3)
            total_y = total_frac * 2.5
            if total_y > 0:
                pts += [
                    np.array([bar_x3 - bar_width/2, 0, 0]),
                    np.array([bar_x3 + bar_width/2, 0, 0]),
                    np.array([bar_x3 + bar_width/2, -total_y, 0]),
                    np.array([bar_x3 - bar_width/2, -total_y, 0]),
                    np.array([bar_x3 - bar_width/2, 0, 0]),
                ]
            else:
                pts += [
                    np.array([bar_x3 - bar_width/2, total_y, 0]),
                    np.array([bar_x3 + bar_width/2, total_y, 0]),
                    np.array([bar_x3 + bar_width/2, 0, 0]),
                    np.array([bar_x3 - bar_width/2, 0, 0]),
                    np.array([bar_x3 - bar_width/2, total_y, 0]),
                ]

            bars.set_points_as_corners(pts)
            return bars

        e_bars = always_redraw(energy_bars)

        # Energy labels
        ke_label = MathTex("KE", font_size=20, color=GREEN).move_to(
            np.array([bar_x, 1.8, 0])
        )
        gpe_label = MathTex("GPE", font_size=20, color=RED).move_to(
            np.array([bar_x + bar_width + 0.3, -1.5, 0])
        )
        total_label = MathTex("E_{\\text{tot}}", font_size=20, color=BLUE).move_to(
            np.array([bar_x + 2 * (bar_width + 0.3), -1.5, 0])
        )

        # ------------------------------------------------------------------
        # v_orb and v_esc display
        # ------------------------------------------------------------------
        v_orb_text = always_redraw(lambda: MathTex(
            f"v_{{\\text{{orb}}}} = {sim.orbital_velocity(sim.radius)/1000:.1f}\\,\\text{{km/s}}",
            font_size=22, color=GREEN,
        ).to_corner(DOWN + LEFT, buff=0.3))

        v_esc_text = always_redraw(lambda: MathTex(
            f"v_{{\\text{{esc}}}} = {sim.escape_velocity(sim.radius)/1000:.1f}\\,\\text{{km/s}}",
            font_size=22, color=ORANGE,
        ).next_to(v_orb_text, DOWN, buff=0.1, aligned_edge=LEFT))

        # ------------------------------------------------------------------
        # Physics driver
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # Simulation step updater
        def sim_updater(_mob: Mobject, dt: float) -> None:
            h = min(dt, 1.0 / 30.0)
            sim.step(h * 100)  # scale time for visible orbit

        sim_driver = Mobject()
        sim_driver.add_updater(sim_updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        self.add(earth, earth_label, orbit_path)
        self.add(satellite_dot)
        self.add(v_arrow, f_arrow)
        self.add(v_label, f_label)
        self.add(e_bars)
        self.add(ke_label, gpe_label, total_label)
        self.add(v_orb_text, v_esc_text)
        self.add(driver, sim_driver)

        self.wait(total_time)