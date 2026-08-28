"""Scene C — Motor effect: current-carrying conductor in a magnetic field.

Shows a current-carrying conductor (wire) in a uniform magnetic field.
The force F = B I L acts on the conductor (motor effect), causing the
armature to rotate.  The torque formula τ = N B I L r cos(θ) is displayed.

The physics is computed by
:class:`physics_core.engineering.motors.ReferenceMotor`, so the
animation uses the same engine as the teacher app and student exercise.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    Create,
    DOWN,
    GREEN,
    LEFT,
    MathTex,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    Write,
    YELLOW,
)

from physics_core.engineering.motors import ReferenceMotor


class MotorEffect(Scene):
    """Motor effect — force on a current-carrying conductor in a B-field."""

    def construct(self) -> None:
        motor = ReferenceMotor(B=0.5, I=2.0, L=0.1, N=1, radius=0.05)

        # Magnetic field arrows (uniform, pointing right)
        field_arrows = VGroup()
        for gx in np.linspace(-3, 3, 7):
            for gy in np.linspace(-1.5, 1.5, 5):
                start = np.array([gx, gy, 0])
                end = np.array([gx + 0.4, gy, 0])
                arrow = VMobject()
                arrow.set_points_as_corners([start, end])
                arrow.set_color(BLUE)
                arrow.set_stroke(width=2)
                field_arrows.add(arrow)

        field_label = MathTex("B", font_size=32, color=BLUE).to_corner(
            UP + LEFT, buff=0.5
        )

        # Conductor (vertical wire)
        wire = VMobject()
        wire.set_points_as_corners([
            np.array([0, -1.5, 0]),
            np.array([0, 1.5, 0]),
        ])
        wire.set_color(YELLOW)
        wire.set_stroke(width=6)

        # Current arrow (upward)
        current_arrow = VMobject()
        current_arrow.set_points_as_corners([
            np.array([0.3, -1.0, 0]),
            np.array([0.3, 1.0, 0]),
        ])
        current_arrow.set_color(RED)
        current_arrow.set_stroke(width=3)

        current_label = MathTex("I", font_size=28, color=RED).next_to(
            current_arrow, RIGHT, buff=0.2
        )

        # Force arrow (F = BIL, perpendicular to both B and I)
        force_arrow = VMobject()
        force_arrow.set_points_as_corners([
            np.array([0, 0, 0]),
            np.array([0, 0.8, 0]),
        ])
        force_arrow.set_color(GREEN)
        force_arrow.set_stroke(width=4)

        force_label = MathTex("F = B I L", font_size=28, color=GREEN).next_to(
            force_arrow, UP, buff=0.3
        )

        # Torque formula
        torque_formula = MathTex(
            "\\tau = N B I L r \\cos\\theta",
            font_size=28,
            color=GREEN,
        ).to_corner(DOWN + LEFT, buff=0.5)

        # Animate
        self.play(Create(field_arrows), run_time=1.5)
        self.play(Write(field_label))
        self.play(Create(wire))
        self.play(Create(current_arrow), Write(current_label))
        self.play(Create(force_arrow), Write(force_label))
        self.play(Write(torque_formula))
        self.wait(2.0)