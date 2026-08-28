"""Scene B — Equipotential lines and field vectors (E = -grad V).

Shows equipotential contours around a point charge alongside the electric
field vector arrows.  Because E = -∇V, the field vectors are everywhere
perpendicular to the equipotential lines — a core concept in electrostatics.

This is a static-annotation scene: all geometry is pre-computed using
:class:`physics_core.em.electrostatics.ReferenceElectricField` (Coulomb's law).
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    Arrow,
    BLUE,
    Circle,
    Create,
    DOWN,
    Dot,
    GRAY,
    LEFT,
    MathTex,
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


class PotentialGradient(Scene):
    """Equipotential lines + field vectors: E = -grad V."""

    def construct(self) -> None:
        # ==================================================================
        # Physics setup — point charge at centre
        # ==================================================================
        ef = ReferenceElectricField(q=1e-9)

        # ==================================================================
        # Display area
        # ==================================================================
        origin = np.array([0.0, 0.0, 0.0])
        scale = 1.6  # mapping from world coords to scene coords

        # Charge dot
        charge_dot = Dot(origin, color=RED, radius=0.12)
        charge_label = MathTex("+q", font_size=24, color=RED).next_to(
            charge_dot, UP, buff=0.15
        )

        # ==================================================================
        # Equipotential circles
        # ==================================================================
        equipotentials = VGroup()
        radii = [0.5, 0.8, 1.1, 1.4, 1.8]
        for r in radii:
            circle = Circle(radius=r * scale, color=BLUE, stroke_width=2)
            circle.move_to(origin)
            equipotentials.add(circle)

        # ==================================================================
        # Field vector arrows (perpendicular to equipotentials)
        # ==================================================================
        field_arrows = VGroup()
        for angle in range(0, 360, 30):
            a = math.radians(angle)
            for r in (0.6, 1.0, 1.5):
                wx = r * math.cos(a)
                wy = r * math.sin(a)
                Ex, Ey = ef.field(wx, wy)
                E_mag = math.hypot(Ex, Ey)
                if E_mag < 1e-9:
                    continue
                start = origin + np.array([wx * scale, wy * scale, 0])
                arrow_len = 0.3
                direction = np.array([Ex / E_mag, Ey / E_mag, 0])
                end = start + direction * arrow_len
                arr = Arrow(start, end, color=YELLOW, stroke_width=2, buff=0)
                field_arrows.add(arr)

        # ==================================================================
        # Annotations
        # ==================================================================
        title = MathTex(
            "E = -\\nabla V", font_size=30, color=YELLOW
        ).to_corner(UP + LEFT, buff=0.5)

        eq_label = MathTex(
            "\\text{Equipotential lines (blue)}", font_size=20, color=BLUE
        ).to_corner(DOWN + LEFT, buff=0.3)

        field_label = MathTex(
            "\\text{Field vectors (yellow)}", font_size=20, color=YELLOW
        ).to_corner(DOWN + RIGHT, buff=0.3)

        note = MathTex(
            "\\text{Field is always } \\perp \\text{ equipotential}",
            font_size=22,
            color=GRAY,
        ).to_corner(DOWN, buff=0.3)

        # ==================================================================
        # Assemble
        # ==================================================================
        self.play(Create(charge_dot), Write(charge_label))
        self.play(Create(equipotentials), run_time=2.0)
        self.play(Create(field_arrows), run_time=2.0)
        self.play(Write(title))
        self.play(Write(eq_label), Write(field_label))
        self.play(Write(note))

        self.wait(2.0)