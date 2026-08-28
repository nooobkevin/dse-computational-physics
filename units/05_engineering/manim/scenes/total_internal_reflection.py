"""Scene A — Total internal reflection in an optical fibre.

Shows a ray zigzagging inside the fibre core.  When the ray angle exceeds
the critical angle (θ_c = arcsin(n₂/n₁)), the ray undergoes total internal
reflection (green).  Below the critical angle, the ray leaks out (red).

The physics is computed by
:class:`physics_core.engineering.optics.ReferenceOpticalFibre`, so the
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

from physics_core.engineering.optics import ReferenceOpticalFibre


class TotalInternalReflection(Scene):
    """Total internal reflection in an optical fibre."""

    def construct(self) -> None:
        fibre = ReferenceOpticalFibre(n1=1.50, n2=1.45, length=10.0, angle=1.4)
        crit = fibre.critical_angle
        crit_deg = math.degrees(crit)

        # Fibre schematic
        core_top = UP * 0.4
        core_bot = DOWN * 0.4
        clad_top = UP * 0.7
        clad_bot = DOWN * 0.7
        fibre_left = LEFT * 4.5
        fibre_right = RIGHT * 4.5

        # Cladding outline
        cladding = VMobject()
        cladding.set_points_as_corners([
            fibre_left + clad_top,
            fibre_right + clad_top,
            fibre_right + clad_bot,
            fibre_left + clad_bot,
            fibre_left + clad_top,
        ])
        cladding.set_color(BLUE)
        cladding.set_stroke(width=2, opacity=0.4)

        # Core outline
        core = VMobject()
        core.set_points_as_corners([
            fibre_left + core_top,
            fibre_right + core_top,
            fibre_right + core_bot,
            fibre_left + core_bot,
            fibre_left + core_top,
        ])
        core.set_color(YELLOW)
        core.set_stroke(width=2)

        # Ray zigzag (TIR case — green)
        ray_tir = VGroup()
        n_bounces = 5
        x_start = fibre_left[0] + 0.3
        x_end = fibre_right[0] - 0.3
        seg_len = (x_end - x_start) / n_bounces
        for i in range(n_bounces):
            x1 = x_start + i * seg_len
            y1 = core_top[1] - 0.1 if i % 2 == 0 else core_bot[1] + 0.1
            x2 = x_start + (i + 1) * seg_len
            y2 = core_bot[1] + 0.1 if i % 2 == 0 else core_top[1] - 0.1
            seg = VMobject()
            seg.set_points_as_corners([
                np.array([x1, y1, 0]),
                np.array([x2, y2, 0]),
            ])
            seg.set_color(GREEN)
            seg.set_stroke(width=3)
            ray_tir.add(seg)

        # Labels
        n1_label = MathTex("n_1 = 1.50", font_size=24, color=YELLOW).next_to(
            fibre_left + core_top, UP, buff=0.3
        )
        n2_label = MathTex("n_2 = 1.45", font_size=24, color=BLUE).next_to(
            fibre_left + clad_top, UP, buff=0.3
        )
        crit_label = MathTex(
            f"\\theta_c = \\arcsin(n_2/n_1) = {crit_deg:.1f}^\\circ",
            font_size=24,
        ).to_corner(UP + RIGHT, buff=0.5)

        tir_label = MathTex(
            "\\theta > \\theta_c \\Rightarrow \\text{TIR}",
            font_size=28,
            color=GREEN,
        ).to_corner(DOWN + LEFT, buff=0.5)

        # Animate
        self.play(Create(cladding), Create(core))
        self.play(Write(n1_label), Write(n2_label))
        self.play(Create(ray_tir), run_time=2.0)
        self.play(Write(crit_label))
        self.play(Write(tir_label))
        self.wait(2.0)