"""Scene D — Charged particle in a uniform magnetic field.

Shows a charged particle entering a uniform B-field region (out of the
page).  Outside the field the particle moves in a straight line; inside
it follows a circular arc with radius r = mv/(qB).  A second particle
with opposite charge is shown curving in the opposite direction.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    Dot,
    GREEN,
    MathTex,
    ORANGE,
    Rectangle,
    RED,
    RIGHT,
    Scene,
    UP,
    VMobject,
    YELLOW,
)

from physics_core.em.magnetism import ReferenceMovingCharge


class MagneticForce(Scene):
    """Charged particle in uniform B field — circular motion."""

    def construct(self) -> None:
        m: float = 1.6726219e-27
        q: float = 1.602176634e-19
        B: float = 0.5
        v: float = 2e6

        mc = ReferenceMovingCharge(m=m, q=q)
        r_orbit: float = mc.orbit_radius(m, v, q, B)
        # Orbit radius r=0.0209m should span ~1.5 scene units
        scale: float = 1.5 / r_orbit  # ~72

        field_left_su: float = -1.8  # scene units
        field_right_su: float = 1.8
        dt: float = 5e-10
        n_steps: int = 800

        # Convert scene-unit coordinate to physics (meters)
        def su_to_phys(val: float) -> float:
            return val / scale

        pos_phys = su_to_phys(-5.0)  # start left of screen
        vel_phys = v
        y_offset_pos = 0.0
        y_offset_neg = -1.2

        def _compute_traj(y_offset: float, charge: float) -> list[np.ndarray]:
            traj: list[np.ndarray] = []
            px = pos_phys
            py = su_to_phys(y_offset)
            vx = vel_phys
            vy = 0.0
            fl = su_to_phys(field_left_su)
            fr = su_to_phys(field_right_su)
            for _ in range(n_steps):
                traj.append(np.array([px * scale, py * scale, 0.0]))
                if fl <= px <= fr:
                    (px, py), (vx, vy) = mc.trajectory_step(
                        (px, py), (vx, vy), B, charge, m, dt
                    )
                else:
                    px += vx * dt
                    py += vy * dt
            return traj

        traj_pos = _compute_traj(y_offset_pos, q)
        traj_neg = _compute_traj(y_offset_neg, -q)

        # B-field region background
        bg = Rectangle(
            width=field_right_su - field_left_su,
            height=6.0,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.08,
            stroke_width=1,
            stroke_opacity=0.3,
        ).move_to(np.array([(field_left_su + field_right_su) / 2.0, 0.0, 0.0]))
        bg_label = MathTex(
            "\\mathbf{B}\\;\\odot", font_size=22, color=BLUE
        ).next_to(bg, UP, buff=0.15)

        self.add(bg, bg_label)

        radius_label = MathTex(
            f"r = mv/(|q|B) = {r_orbit:.4f}\\,\\mathrm{{m}}",
            font_size=22, color=GREEN,
        ).to_corner(RIGHT + UP, buff=0.5)
        self.add(radius_label)

        label_pos = MathTex("+q", font_size=20, color=YELLOW).move_to(
            traj_pos[20] + np.array([0.0, 0.3, 0.0])
        )
        label_neg = MathTex("-q", font_size=20, color=ORANGE).move_to(
            traj_neg[20] + np.array([0.0, -0.3, 0.0])
        )
        self.add(label_pos, label_neg)

        # Initial dots
        dot_p = Dot(traj_pos[0], color=RED, radius=0.08)
        dot_n = Dot(traj_neg[0], color=ORANGE, radius=0.08)
        self.add(dot_p, dot_n)

        # Trajectory curves (start empty, grow during animation)
        curve_p = VMobject(color=YELLOW, stroke_width=3)
        curve_n = VMobject(color=ORANGE, stroke_width=3)
        self.add(curve_p, curve_n)

        batch_size: int = 10
        for batch_start in range(0, n_steps, batch_size):
            batch_end = min(batch_start + batch_size, n_steps)

            pts_p = traj_pos[:batch_end]
            if len(pts_p) >= 2:
                new_p = VMobject(color=YELLOW, stroke_width=3)
                new_p.set_points_as_corners(pts_p)
                self.remove(curve_p)
                curve_p = new_p
                self.add(curve_p)

            pts_n = traj_neg[:batch_end]
            if len(pts_n) >= 2:
                new_n = VMobject(color=ORANGE, stroke_width=3)
                new_n.set_points_as_corners(pts_n)
                self.remove(curve_n)
                curve_n = new_n
                self.add(curve_n)

            dot_p.move_to(traj_pos[batch_end - 1])
            dot_n.move_to(traj_neg[batch_end - 1])
            self.wait(0.1)