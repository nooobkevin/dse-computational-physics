"""Scene B — Photoelectric effect.

Animate the photoelectric effect: photon energy E = hf, work function φ,
stopping potential V₀, and the linear relationship between K_max and
frequency.  Show a graph of K_max vs f with the threshold frequency f₀
marked, and illustrate the energy balance hf = K_max + φ.

Physics driver
--------------
PhotoElectric from physics_core provides the photoelectric calculations.

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
The K_max vs f curve is revealed progressively: the full (frequency,
K_max) arrays are precomputed once, and each frame the visible trace is
the prefix whose precomputed reveal time is <= the current simulation
time.  The trace is an ``always_redraw`` VMobject (single curve built
with set_points_as_corners) and the moving dot is an ``always_redraw``
Dot.  The simulation time is read from ``scene.time`` (the
authoritative video time) via a driver mobject whose updater only does
``t[0] = self.time``; it is NEVER accumulated from updater ``dt``
values.  This pattern is required because submobjects appended to a
mounted VGroup from inside an updater are never re-rendered by the
ManimCE cairo renderer.  The closing energy-balance panel is a genuine
discrete animation and remains a ``self.play(Write(...))``.
"""

from __future__ import annotations

from bisect import bisect_right

import numpy as np
from manim import (
    Axes,
    BLUE,
    Dot,
    DOWN,
    GRAY,
    GREEN,
    LEFT,
    Line,
    MathTex,
    Mobject,
    RED,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    VMobject,
    Write,
    YELLOW,
    always_redraw,
)

from physics_core.quantum.photoelectric import E_CHARGE, PhotoElectric


class Photoelectric(Scene):
    """Photoelectric effect: K_max vs frequency — animated."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        phi_eV = 2.0
        phi = phi_eV * E_CHARGE
        pe = PhotoElectric(work_function=phi)
        f0 = pe.threshold_frequency()

        # Frequency scale: the axis is drawn in units of 1e14 Hz so tick
        # labels are small integers rather than 1e14-scale floats.
        f0_THz14 = f0 / 1e14

        # Frequency range
        f_min = 0.0
        f_max = 3.0 * f0
        n_points = 200

        # Pre-compute curve (once) and its reveal schedule: point i is
        # visible once the video time reaches reveal_time[i].
        freqs = np.array(
            [f_min + (f_max - f_min) * i / n_points for i in range(n_points + 1)]
        )
        ke_vals = np.array([pe.max_ke_eV(f) for f in freqs])
        trace_duration: float = 6.0
        reveal_times = np.linspace(0.0, trace_duration, n_points + 1)

        # Authoritative simulation time — read from scene (video) time.
        t: list[float] = [0.0]

        # ------------------------------------------------------------------
        # Axes — x in units of 10^14 Hz
        # ------------------------------------------------------------------
        unit = 1e14
        axes = Axes(
            x_range=[0, f_max / unit, 2.0],
            y_range=[0, max(ke_vals) * 1.2, 1],
            x_length=8.0,
            y_length=5.0,
            axis_config={
                "color": GRAY,
                "include_numbers": True,
                "font_size": 20,
                "decimal_number_config": {"num_decimal_places": 0},
            },
        )
        axes.center()

        # Labels
        x_label = MathTex(
            "f", "\\ (\\times 10^{14}\\ \\text{Hz})", font_size=28
        ).next_to(axes.c2p(f_max / unit * 0.5, 0), DOWN, buff=0.4)
        y_label = MathTex("K_\\text{max}", "\\text{ (eV)}", font_size=28).next_to(
            axes.y_axis.get_end(), LEFT
        )

        # ------------------------------------------------------------------
        # Threshold frequency marker (static)
        # ------------------------------------------------------------------
        f0_line = Line(
            axes.c2p(f0_THz14, 0),
            axes.c2p(f0_THz14, max(ke_vals) * 1.2),
            color=RED,
            stroke_width=2,
            stroke_opacity=0.7,
        )
        f0_label = MathTex(
            f"f_0 = {f0_THz14:.2f} \\times 10^{{14}}\\ \\text{{Hz}}",
            font_size=20,
            color=RED,
        )
        f0_label.next_to(f0_line, UP, buff=0.1)

        # ------------------------------------------------------------------
        # KE vs frequency curve — progressive reveal, always_redraw
        # ------------------------------------------------------------------
        def visible_count() -> int:
            return max(1, int(bisect_right(reveal_times, t[0])))

        def draw_trace() -> VMobject:
            k = visible_count()
            pts = [
                axes.c2p(float(freqs[i]) / unit, float(ke_vals[i]))
                for i in range(k)
            ]
            vm = VMobject(color=GREEN, stroke_width=3)
            vm.set_points_as_corners(pts)
            return vm

        trace = always_redraw(draw_trace)

        # Moving dot at the tip of the revealed trace
        current_dot = always_redraw(
            lambda: Dot(
                axes.c2p(
                    float(freqs[min(visible_count() - 1, n_points)]) / unit,
                    float(ke_vals[min(visible_count() - 1, n_points)]),
                ),
                color=GREEN,
                radius=0.08,
            )
        )

        # ------------------------------------------------------------------
        # Energy balance illustration
        # ------------------------------------------------------------------
        # Show at a specific frequency (2 * f0)
        f_demo = 2.0 * f0
        ke_demo = pe.max_ke_eV(f_demo)
        hf_demo = pe.photon_energy(f_demo) / E_CHARGE  # in eV

        energy_balance = VGroup()
        balance_title = Text("Energy Balance", font_size=22, color=GRAY)
        balance_title.to_corner(UP, buff=0.5)

        hf_eq = MathTex(f"hf = {hf_demo:.2f}\\,\\text{{eV}}", font_size=24, color=BLUE)
        hf_eq.next_to(balance_title, DOWN, buff=0.3)

        phi_eq = MathTex(f"\\phi = {phi_eV:.1f}\\,\\text{{eV}}", font_size=24, color=RED)
        phi_eq.next_to(hf_eq, DOWN, buff=0.2)

        ke_eq = MathTex(f"K_\\text{{max}} = {ke_demo:.2f}\\,\\text{{eV}}", font_size=24, color=GREEN)
        ke_eq.next_to(phi_eq, DOWN, buff=0.2)

        formula = MathTex("K_\\text{max} = hf - \\phi", font_size=26, color=YELLOW)
        formula.next_to(ke_eq, DOWN, buff=0.3)

        energy_balance.add(balance_title, hf_eq, phi_eq, ke_eq, formula)

        # ------------------------------------------------------------------
        # Physics driver — sets authoritative time from the scene clock
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        self.add(axes, x_label, y_label)
        self.add(f0_line, f0_label)
        self.add(trace, current_dot)
        self.add(driver)

        self.wait(trace_duration)

        # Freeze the fully drawn trace, then show the energy balance panel.
        driver.clear_updaters()
        self.play(Write(energy_balance))
        self.wait(2.0)
