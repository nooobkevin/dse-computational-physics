"""Scene A — Doppler redshift: wave compression and colour shift.

Shows a source emitting light waves.  As the source moves toward the
observer the waves compress (blueshift); as it moves away they stretch
(redshift).  The observed wavelength is computed by
:class:`physics_core.astrophysics.doppler.ReferenceDopplerShift`.
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
    FadeOut,
    LEFT,
    MathTex,
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
)

from physics_core.astrophysics.doppler import C, ReferenceDopplerShift


class DopplerRedshift(Scene):
    """Doppler effect: approaching source (blueshift) and receding source (redshift)."""

    def construct(self) -> None:
        ds = ReferenceDopplerShift(f0=5.8e14)
        v_approach = -3e7  # 0.1c approaching
        v_recede = 3e7     # 0.1c receding

        # ==================================================================
        # Part 1 — Source at rest
        # ==================================================================
        rest_label = MathTex(
            "\\text{Source at rest: } \\lambda_{\\text{source}}",
            font_size=28,
        ).to_corner(UP + LEFT, buff=0.5)
        self.play(Write(rest_label))

        # Draw rest wave
        wave_center = np.array([0.0, 0.0, 0.0])
        wave_amp = 0.8
        n_waves = 5
        base_wavelength = 1.2
        rest_wave = self._draw_wave(wave_center, wave_amp, base_wavelength, n_waves, YELLOW)
        self.play(Create(rest_wave), run_time=1.5)

        source_dot = Dot(LEFT * 4.0, color=ORANGE, radius=0.1)
        source_label = MathTex("\\text{Source}", font_size=20, color=ORANGE).next_to(
            source_dot, UP, buff=0.1
        )
        obs_dot = Dot(RIGHT * 4.0, color=BLUE, radius=0.1)
        obs_label = MathTex("\\text{Observer}", font_size=20, color=BLUE).next_to(
            obs_dot, UP, buff=0.1
        )
        self.play(Create(source_dot), Write(source_label))
        self.play(Create(obs_dot), Write(obs_label))

        self.wait(1.0)

        # ==================================================================
        # Part 2 — Approaching (blueshift)
        # ==================================================================
        self.play(FadeOut(rest_wave), FadeOut(rest_label))

        approach_label = MathTex(
            "\\text{Approaching: } \\lambda_{\\text{obs}} < \\lambda_{\\text{source}} \\quad (\\text{Blueshift})",
            font_size=28,
            color=BLUE,
        ).to_corner(UP + LEFT, buff=0.5)
        self.play(Write(approach_label))

        # Compute observed wavelength for approaching
        f_obs_approach = ds.observed_frequency(v_approach)
        lambda_ratio_approach = C / f_obs_approach / (C / ds.f0)
        approach_wave = self._draw_wave(
            wave_center, wave_amp, base_wavelength * lambda_ratio_approach,
            n_waves, BLUE
        )
        self.play(Create(approach_wave), run_time=1.5)

        # Formula
        formula_approach = MathTex(
            "f_{\\text{obs}} = f_{\\text{source}} \\sqrt{\\frac{1 - \\beta}{1 + \\beta}}",
            font_size=24,
        ).to_corner(DOWN + LEFT, buff=0.5)
        beta_approach = MathTex(
            f"\\beta = v/c = {v_approach / C:.3f}",
            font_size=20,
        ).next_to(formula_approach, DOWN, buff=0.2)
        self.play(Write(formula_approach), Write(beta_approach))

        self.wait(2.0)

        # ==================================================================
        # Part 3 — Receding (redshift)
        # ==================================================================
        self.play(
            FadeOut(approach_wave),
            FadeOut(approach_label),
            FadeOut(formula_approach),
            FadeOut(beta_approach),
        )

        recede_label = MathTex(
            "\\text{Receding: } \\lambda_{\\text{obs}} > \\lambda_{\\text{source}} \\quad (\\text{Redshift})",
            font_size=28,
            color=RED,
        ).to_corner(UP + LEFT, buff=0.5)
        self.play(Write(recede_label))

        f_obs_recede = ds.observed_frequency(v_recede)
        lambda_ratio_recede = C / f_obs_recede / (C / ds.f0)
        recede_wave = self._draw_wave(
            wave_center, wave_amp, base_wavelength * lambda_ratio_recede,
            n_waves, RED
        )
        self.play(Create(recede_wave), run_time=1.5)

        formula_recede = MathTex(
            "z = \\frac{\\lambda_{\\text{obs}} - \\lambda_{\\text{source}}}{\\lambda_{\\text{source}}}",
            font_size=24,
        ).to_corner(DOWN + LEFT, buff=0.5)
        z_val = MathTex(
            f"z = {ds.redshift(v_recede):.3f}",
            font_size=20,
        ).next_to(formula_recede, DOWN, buff=0.2)
        self.play(Write(formula_recede), Write(z_val))

        self.wait(2.0)

    def _draw_wave(
        self,
        center: np.ndarray,
        amplitude: float,
        wavelength: float,
        n_waves: float,
        color,
    ) -> VMobject:
        """Draw a sine wave as a continuous curve."""
        pts = []
        total_length = n_waves * wavelength
        n_points = 200
        for i in range(n_points + 1):
            x = -total_length / 2 + total_length * i / n_points
            y = amplitude * math.sin(2.0 * math.pi * x / wavelength)
            pts.append(center + np.array([x, y, 0]))
        wave = VMobject()
        wave.set_points_as_corners(pts)
        wave.set_color(color)
        wave.set_stroke(width=3)
        return wave