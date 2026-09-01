"""Scene A — Electric field lines around a point charge and parallel plates.

Shows the electric field pattern for two configurations:
1. A single point charge — field lines radiate radially outward (positive q).
2. Two parallel plates — a uniform field between them.

The field vectors are computed by
:class:`physics_core.em.electrostatics.ReferenceElectricField` (Coulomb's
law), so the animation uses the same physics engine as the teacher app and
the student exercise.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    Arrow,
    BLUE,
    Create,
    DOWN,
    Dot,
    LEFT,
    MathTex,
    ORANGE,
    Rectangle,
    RED,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    Write,
    YELLOW,
)

from physics_core.em.electrostatics import ReferenceElectricField


class ElectricFieldLines(Scene):
    """Electric field lines: point charge + parallel plates."""

    def construct(self) -> None:
        # ==================================================================
        # Left panel — point charge
        # ==================================================================
        charge_center = LEFT * 3.2
        ef = ReferenceElectricField(q=1e-9)

        charge_dot = Dot(charge_center, color=RED, radius=0.12)
        charge_label = MathTex("+q", font_size=24, color=RED).next_to(
            charge_dot, UP, buff=0.15
        )

        # Field lines radiating outward (traced from the charge)
        field_lines = VGroup()
        n_lines = 12
        for i in range(n_lines):
            angle = 2.0 * math.pi * i / n_lines
            pts = []
            r = 0.15
            for _ in range(50):
                wx = r * math.cos(angle)
                wy = r * math.sin(angle)
                px = charge_center[0] + wx * 1.4
                py = charge_center[1] + wy * 1.4
                pts.append(np.array([px, py, 0]))
                r += 0.07
            curve = VMobject()
            curve.set_points_as_corners(pts)
            curve.set_color(YELLOW)
            curve.set_stroke(width=2)
            field_lines.add(curve)

        # Field vector arrows at a few sample points
        field_arrows = VGroup()
        for angle in range(0, 360, 45):
            a = math.radians(angle)
            for r in (0.8, 1.6):
                wx = r * math.cos(a)
                wy = r * math.sin(a)
                Ex, Ey = ef.field(wx, wy)
                E_mag = math.hypot(Ex, Ey)
                if E_mag < 1e-9:
                    continue
                start = charge_center + np.array([wx * 1.4, wy * 1.4, 0])
                # Arrow length encodes |E| ∝ 1/r² : halved at r=0.8 → quarter
                # at r=1.6, so the inverse-square falloff is visible.
                arrow_len = 0.55 * (0.8 / r) ** 2
                direction = np.array([Ex / E_mag, Ey / E_mag, 0])
                end = start + direction * arrow_len
                arr = Arrow(start, end, color=ORANGE, stroke_width=3, buff=0)
                field_arrows.add(arr)

        title_left = MathTex(
            "\\text{Point charge: } E = \\frac{q}{4\\pi\\varepsilon_0 r^2}",
            font_size=22,
        ).to_corner(UP + LEFT, buff=0.5)

        # ==================================================================
        # Right panel — parallel plates
        # ==================================================================
        plate_left = RIGHT * 0.8
        plate_width = 3.0
        plate_gap = 2.4

        top_plate = Rectangle(
            width=plate_width,
            height=0.12,
            color=RED,
            fill_color=RED,
            fill_opacity=0.8,
        )
        top_plate.move_to(plate_left + UP * (plate_gap / 2))
        bottom_plate = Rectangle(
            width=plate_width,
            height=0.12,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.8,
        )
        bottom_plate.move_to(plate_left + DOWN * (plate_gap / 2))

        plus_label = MathTex("+", font_size=24, color=RED).next_to(
            top_plate, UP, buff=0.1
        )
        minus_label = MathTex("-", font_size=24, color=BLUE).next_to(
            bottom_plate, DOWN, buff=0.1
        )

        # Uniform field arrows between plates
        plate_arrows = VGroup()
        for gx in np.linspace(-1.2, 1.2, 7):
            start = plate_left + np.array([gx, plate_gap / 2 - 0.25, 0])
            end = plate_left + np.array([gx, -plate_gap / 2 + 0.25, 0])
            arr = Arrow(start, end, color=YELLOW, stroke_width=3, buff=0)
            plate_arrows.add(arr)

        title_right = MathTex(
            "\\text{Parallel plates: uniform } E = V/d",
            font_size=22,
        ).to_corner(UP + RIGHT, buff=0.5)

        # ==================================================================
        # Assemble and animate
        # ==================================================================
        self.play(Create(charge_dot), Write(charge_label))
        self.play(Create(field_lines), run_time=2.0)
        self.play(Create(field_arrows), run_time=1.5)
        self.play(Write(title_left))

        self.play(
            Create(top_plate),
            Create(bottom_plate),
            Write(plus_label),
            Write(minus_label),
        )
        self.play(Create(plate_arrows), run_time=1.5)
        self.play(Write(title_right))

        self.wait(2.0)