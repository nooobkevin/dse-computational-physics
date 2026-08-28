"""Scene — Rutherford scattering: alpha particles deflected by a gold nucleus.

Animate several alpha particles approaching a gold nucleus from the left
with different impact parameters.  Each particle follows a hyperbolic
Coulomb-scattering trajectory computed by ReferenceRutherfordScattering.
A head-on particle (b ≈ 0) backscatters at 180°.

Progressive reveal: trajectories appear one-by-one with labels.

Physics driver
--------------
ReferenceRutherfordScattering from physics_core provides the scattering
angle θ(b) and trajectory points.

Animation pattern (IMPORTANT — see repo convention)
----------------------------------------------------
Each trajectory is a static VMobject revealed via Create. No
always_redraw needed since the trajectories are pre-computed and static.
"""

from __future__ import annotations

import math
import random

import numpy as np
from manim import (
    BLUE,
    Circle,
    Create,
    DOWN,
    GOLD,
    GRAY,
    GREEN,
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

from physics_core.quantum.rutherford import ReferenceRutherfordScattering


class RutherfordScattering(Scene):
    """Rutherford scattering: alpha particles deflected by a gold nucleus."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        random.seed(42)  # deterministic render

        Z1 = 2  # alpha particle
        Z2 = 79  # gold nucleus
        E = 5.0e6 * 1.602176634e-19  # 5 MeV in J
        sim = ReferenceRutherfordScattering(Z1=Z1, Z2=Z2, E=E)

        # Impact parameters: one nearly head-on, then increasing
        b_values = [1e-16, 5e-15, 1.5e-14, 3e-14, 5e-14]
        n_trajectories = len(b_values)

        # Pre-compute trajectories
        thetas: list[float] = []
        for b in b_values:
            theta = sim.scattering_angle(b, E)
            thetas.append(theta)

        scale = 1.5e13  # m → Manim units

        # ------------------------------------------------------------------
        # Gold nucleus at centre
        # ------------------------------------------------------------------
        nucleus = Circle(radius=0.15, color=GOLD, fill_opacity=0.8)
        nucleus_label = Text("Au", font_size=16, color=GOLD)
        nucleus_label.next_to(nucleus, UP, buff=0.1)

        beam_label = Text("α beam →", font_size=20, color=GRAY)
        beam_label.to_corner(LEFT + UP, buff=0.5)

        # ------------------------------------------------------------------
        # Build trajectory mobjects + labels
        # ------------------------------------------------------------------
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
        trajectory_mobs: list[VMobject] = []
        label_mobs: list[VGroup] = []

        for i in range(n_trajectories):
            b = b_values[i]
            pts = sim.trajectory_points(b, E, n_points=150, r_max=3e-13)
            manim_pts = [
                np.array([p[0] * scale, p[1] * scale, 0]) for p in pts
            ]
            vm = VMobject(color=colors[i], stroke_width=2)
            if len(manim_pts) >= 2:
                vm.set_points_as_corners(manim_pts)
            trajectory_mobs.append(vm)

            theta_deg = math.degrees(thetas[i])
            label = MathTex(
                f"b={b:.0e}\\;\\text{{m}},\\;\\theta={theta_deg:.0f}^\\circ",
                font_size=18,
                color=colors[i],
            )
            label.to_corner(RIGHT + UP, buff=0.5 + i * 0.45)
            label_mobs.append(label)

        # ------------------------------------------------------------------
        # Animation sequence
        # ------------------------------------------------------------------
        self.add(nucleus, nucleus_label, beam_label)

        # Reveal trajectories one by one with fade-in
        for i in range(n_trajectories):
            self.play(Create(trajectory_mobs[i]), run_time=1.0)
            self.play(Write(label_mobs[i]), run_time=0.5)
            self.wait(0.5)

        self.wait(2.0)