"""Scene — Hydrogen spectra: energy-level diagram and Balmer series.

Animate the Bohr hydrogen energy levels (n=1..5 + ionisation limit),
transition arrows for the Balmer series (n≥3 → n=2), and the visible
Balmer lines (Hα 656 nm red, Hβ 486 nm cyan, Hγ 434 nm blue, Hδ 410 nm
violet) drawn to scale on a wavelength axis.

Physics driver
--------------
BohrHydrogen from physics_core provides the energy levels and transition
wavelengths.

Animation pattern (IMPORTANT — see repo convention)
----------------------------------------------------
The visible elements are ``always_redraw`` mobjects rebuilt every frame
from the current simulation time.  The simulation time is read from
``scene.time`` via a driver mobject.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    BLUE_B,
    Create,
    DOWN,
    GRAY,
    LEFT,
    Line,
    MathTex,
    PURPLE,
    RED,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    Write,
)

from physics_core.quantum.bohr import BohrHydrogen


class HydrogenSpectra(Scene):
    """Bohr hydrogen energy levels and Balmer series — animated."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        bohr = BohrHydrogen()
        n_max = 6
        energies = [bohr.energy_level(n) for n in range(1, n_max + 1)]
        e_ion = 0.0  # ionisation limit

        # Balmer series: n=3..6 → n=2
        # (n_i, n_f, latex_name, plain_name, wavelength, color)
        balmer_lines = [
            (3, 2, "H\\\\alpha", "Hα", 656.3e-9, RED),
            (4, 2, "H\\\\beta", "Hβ", 486.1e-9, "#00FFFF"),
            (5, 2, "H\\\\gamma", "Hγ", 434.0e-9, BLUE),
            (6, 2, "H\\\\delta", "Hδ", 410.2e-9, PURPLE),
        ]

        # Authoritative simulation time
        t: list[float] = [0.0]
        total_time: float = 10.0

        # ------------------------------------------------------------------
        # Energy level diagram (left side)
        # ------------------------------------------------------------------
        diagram_center = LEFT * 3.5 + UP * 0.5
        level_height = 3.5  # total height in Manim units
        e_min = energies[-1]  # most negative (n=5)
        e_max = e_ion  # 0 eV

        def e_to_y(e: float) -> float:
            frac = (e - e_min) / max(e_max - e_min, 1e-10)
            return diagram_center[1] - level_height / 2.0 + frac * level_height

        # Draw energy levels
        level_lines = VGroup()
        level_labels = VGroup()
        for n_idx in range(n_max):
            n = n_idx + 1
            y = e_to_y(energies[n_idx])
            line = Line(
                diagram_center + LEFT * 1.5 + UP * (y - diagram_center[1]),
                diagram_center + RIGHT * 1.5 + UP * (y - diagram_center[1]),
                color=BLUE_B,
                stroke_width=2,
            )
            level_lines.add(line)
            label = MathTex(f"n={n}", font_size=20, color=BLUE_B)
            label.next_to(line, LEFT, buff=0.15)
            level_labels.add(label)

        # Ionisation limit
        ion_y = e_to_y(e_ion)
        ion_line = Line(
            diagram_center + LEFT * 1.5 + UP * (ion_y - diagram_center[1]),
            diagram_center + RIGHT * 1.5 + UP * (ion_y - diagram_center[1]),
            color=GRAY,
            stroke_width=1,
            stroke_opacity=0.5,
        )
        ion_label = Text("Ionisation limit", font_size=16, color=GRAY)
        ion_label.next_to(ion_line, RIGHT, buff=0.15)

        # Title
        diagram_title = Text("Hydrogen Energy Levels", font_size=22, color=GRAY)
        diagram_title.next_to(diagram_center + UP * (level_height / 2.0 + 0.3), UP)

        # ------------------------------------------------------------------
        # Transition arrows (Balmer series)
        # ------------------------------------------------------------------
        arrow_group = VGroup()
        for n_i, n_f, latex_name, plain_name, lam, color in balmer_lines:
            y_i = e_to_y(energies[n_i - 1])
            y_f = e_to_y(energies[n_f - 1])
            arrow = Line(
                diagram_center + RIGHT * 0.3 + UP * (y_i - diagram_center[1]),
                diagram_center + RIGHT * 0.3 + UP * (y_f - diagram_center[1]),
                color=color,
                stroke_width=2,
            )
            arrow.add_tip(tip_length=0.1)
            arrow_group.add(arrow)

            # Label
            lam_nm = lam * 1e9
            arrow_label = MathTex(
                f"{latex_name}\\;{lam_nm:.0f}\\,\\text{{nm}}",
                font_size=16,
                color=color,
            )
            arrow_label.next_to(arrow, RIGHT, buff=0.1)
            arrow_group.add(arrow_label)

        # ------------------------------------------------------------------
        # Wavelength axis (right side) — Balmer lines to scale
        # ------------------------------------------------------------------
        axis_center = RIGHT * 3.5 + UP * 0.5
        axis_length = 5.0
        lam_min = 380e-9  # 380 nm (violet)
        lam_max = 700e-9  # 700 nm (red)

        # Axis line
        axis_line = Line(
            axis_center + LEFT * (axis_length / 2.0),
            axis_center + RIGHT * (axis_length / 2.0),
            color=GRAY,
            stroke_width=2,
        )
        axis_title = Text("Balmer Series (visible)", font_size=18, color=GRAY)
        axis_title.next_to(axis_line, UP, buff=2.0)

        # Wavelength labels
        lam_labels = VGroup()
        for lam_val, label_text in [(400e-9, "400"), (500e-9, "500"),
                                     (600e-9, "600"), (700e-9, "700")]:
            frac = (lam_val - lam_min) / (lam_max - lam_min)
            x = axis_center[0] - axis_length / 2.0 + frac * axis_length
            label = Text(f"{label_text} nm", font_size=12, color=GRAY)
            label.next_to(np.array([x, axis_center[1], 0]), DOWN, buff=0.1)
            lam_labels.add(label)

        # Spectral lines (vertical lines at correct wavelengths)
        spectral_lines = VGroup()
        for line_idx, (n_i, n_f, latex_name, plain_name, lam, color) in enumerate(balmer_lines):
            if lam < lam_min or lam > lam_max:
                continue
            frac = (lam - lam_min) / (lam_max - lam_min)
            x = axis_center[0] - axis_length / 2.0 + frac * axis_length
            line = Line(
                np.array([x, axis_center[1] - 0.3, 0]),
                np.array([x, axis_center[1] + 0.3, 0]),
                color=color,
                stroke_width=4,
            )
            spectral_lines.add(line)

            # Alternate label heights (two rows) so neighbours in the
            # crowded 400–520 nm region never collide with each other.
            lam_nm = lam * 1e9
            buff = 0.30 + 0.55 * (line_idx % 2)
            label = Text(f"{plain_name} {lam_nm:.0f} nm", font_size=14, color=color)
            label.next_to(
                np.array([x, axis_center[1], 0]),
                UP,
                buff=buff,
            )
            spectral_lines.add(label)

        # ------------------------------------------------------------------
        # Animation sequence (progressive reveal)
        # ------------------------------------------------------------------
        self.play(Write(diagram_title))

        # Reveal energy levels one by one
        for n_idx in range(n_max):
            self.play(
                Create(level_lines[n_idx]),
                Write(level_labels[n_idx]),
                run_time=0.4,
            )
        self.play(Create(ion_line), Write(ion_label))

        # Reveal transition arrows one by one
        for arrow_mob in arrow_group:
            self.play(Create(arrow_mob), run_time=0.5)

        # Reveal wavelength axis
        self.play(Create(axis_line), Write(axis_title))
        for lam_label in lam_labels:
            self.play(Write(lam_label), run_time=0.15)
        for spectral_mob in spectral_lines:
            self.play(Create(spectral_mob), run_time=0.3)

        self.wait(2.0)