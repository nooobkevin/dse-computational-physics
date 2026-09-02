"""Scene — Resonance: steady-state amplitude vs driving frequency.

Two driven, damped oscillators are compared: light damping (tall, narrow
peak) and heavy damping (short, broad peak).  Both curves are the analytic
steady-state amplitude ``A(ω_d)`` from the engine, and a dot sweeps along the
light-damping curve while a small driven-pendulum inset visibly grows as the
sweep passes ω₀ (resonance).

Physics
-------
Driven, damped pendulum:  ``θ'' = -(g/L)·sin(θ) - b·ω + (F₀/m)·cos(ω_d·t)``
with ``ω₀ = √(g/L)``.  The linearised steady-state amplitude is

    A(ω_d) = (g/L) / sqrt((ω₀² - ω_d²)² + (b·ω_d)²)

whose peak ``A(ω₀) = ω₀/b`` sits at ``ω_d = √(ω₀² - b²/2)`` (slightly below
ω₀ for a damped oscillator).

Animation pattern (IMPORTANT — see repo convention)
---------------------------------------------------
The sweep and oscillation data are fully precomputed at scene start.  An
authoritative time ``t = [0.0]`` is driven by a driver Mobject via
``t[0] = self.time``; every time-varying visual is an ``always_redraw``
mobject rebuilt each frame.  Each curve is a single VMobject built with
``set_points_as_corners``.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    Axes,
    Create,
    DashedLine,
    Dot,
    DOWN,
    GRAY_BROWN,
    GREY_D,
    LaggedStart,
    LEFT,
    Line,
    MathTex,
    Mobject,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    always_redraw,
)

from physics_core.mechanics.pendulum import steady_state_amplitude
from manim_polish import BEAT_PRE, Attention, Reveal


class Resonance(Scene):
    """Resonance curve with two damping values and a driven-oscillation inset."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        L: float = 1.0
        g: float = 9.81
        omega0: float = math.sqrt(g / L)

        b_light: float = 0.6
        b_heavy: float = 2.0

        w_lo: float = 0.4
        w_hi: float = 7.0
        x_max: float = 8.0
        y_max: float = 5.6

        # Authoritative simulation time — read from scene (video) time.
        t: list[float] = [0.0]

        # ------------------------------------------------------------------
        # Precompute the resonance curves (analytic, from the engine)
        # ------------------------------------------------------------------
        n_curve = 320
        curve_ws = np.linspace(0.0, x_max, n_curve)
        curve_light = np.array(
            [steady_state_amplitude(float(w), g, L, b_light) for w in curve_ws]
        )
        curve_heavy = np.array(
            [steady_state_amplitude(float(w), g, L, b_heavy) for w in curve_ws]
        )

        # ------------------------------------------------------------------
        # Precompute the sweep + driven-oscillation inset data (scene start)
        # ------------------------------------------------------------------
        fps = 30
        total_time = 11.0
        n_frames = int(total_time * fps)
        times = np.linspace(0.0, total_time, n_frames)
        dt_frame = times[1] - times[0]

        sweep_w = w_lo + (w_hi - w_lo) * times / total_time
        phase = np.zeros(n_frames)
        for i in range(1, n_frames):
            phase[i] = phase[i - 1] + 0.5 * (sweep_w[i - 1] + sweep_w[i]) * dt_frame

        sweep_amp = np.array(
            [steady_state_amplitude(float(w), g, L, b_light) for w in sweep_w]
        )
        inset_scale = 0.9 / float(sweep_amp.max())
        inset_theta = inset_scale * sweep_amp * np.cos(phase)

        # ------------------------------------------------------------------
        # Axes
        # ------------------------------------------------------------------
        axes = Axes(
            x_range=[0, x_max, 1],
            y_range=[0, y_max, 1],
            x_length=7.5,
            y_length=5.0,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 18,
            },
        )
        axes.shift(LEFT * 1.4)

        x_label = MathTex("\\text{Driving frequency }\\; \\omega_d\\; \\text{(rad/s)}",
                          font_size=22).next_to(axes.x_axis.get_end(), DOWN)
        y_label = MathTex("\\text{Amplitude }\\; A", font_size=22).next_to(
            axes.y_axis.get_end(), LEFT
        )

        title = MathTex(
            "\\text{Resonance: } A(\\omega_d) = \\frac{g/L}"
            "{\\sqrt{(\\omega_0^2 - \\omega_d^2)^2 + (b\\,\\omega_d)^2}}",
            font_size=26, color=GREY_D,
        )
        title.to_edge(UP, buff=0.25)

        # ------------------------------------------------------------------
        # Static resonance curves (single VMobject each)
        # ------------------------------------------------------------------
        def build_curve(ws: np.ndarray, amps: np.ndarray, color: str) -> VMobject:
            pts = [axes.c2p(float(w), float(a)) for w, a in zip(ws, amps)]
            vm = VMobject(color=color, stroke_width=3)
            vm.set_points_as_corners(pts)
            return vm

        light_curve = build_curve(curve_ws, curve_light, "#F4A259")
        heavy_curve = build_curve(curve_ws, curve_heavy, "#4A90E2")

        omega0_line = DashedLine(
            axes.c2p(omega0, 0.0), axes.c2p(omega0, y_max * 0.98),
            color=GREY_D, stroke_width=1, dash_length=0.1,
        )
        omega0_label = MathTex("\\omega_0", font_size=22, color=GREY_D).next_to(
            omega0_line, UP, buff=0.05
        )

        # ------------------------------------------------------------------
        # Legend
        # ------------------------------------------------------------------
        legend = VGroup(
            MathTex(
                "\\text{Light damping }\\; b=" + f"{b_light:.1f}",
                color="#F4A259", font_size=20,
            ),
            MathTex(
                "\\text{Heavy damping }\\; b=" + f"{b_heavy:.1f}",
                color="#4A90E2", font_size=20,
            ),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + RIGHT, buff=0.4)

        # ------------------------------------------------------------------
        # Inset pendulum (upper-right empty region)
        # ------------------------------------------------------------------
        pivot_screen = np.array([4.6, 2.6, 0.0])
        rod_len = 1.7

        inset_title = MathTex("\\text{Driven pendulum}", font_size=18).next_to(
            pivot_screen, UP, buff=0.15
        )
        pivot_dot = Dot(pivot_screen, color=GREY_D, radius=0.09)

        def bob_screen(idx: int) -> np.ndarray:
            th = inset_theta[idx]
            return np.array([
                pivot_screen[0] + rod_len * math.sin(th),
                pivot_screen[1] - rod_len * math.cos(th),
                0.0,
            ])

        def frame_index(tval: float) -> int:
            idx = int(round(tval * fps))
            return max(0, min(idx, n_frames - 1))

        rod = always_redraw(lambda: Line(
            pivot_screen, bob_screen(frame_index(t[0])),
            color=GRAY_BROWN, stroke_width=3,
        ))
        bob = always_redraw(lambda: Dot(
            bob_screen(frame_index(t[0])), color="#2ECC71", radius=0.15,
        ))

        # ------------------------------------------------------------------
        # Sweeping dot + amplitude guide + resonance marker (always_redraw)
        # ------------------------------------------------------------------
        sweep_dot = always_redraw(lambda: Dot(
            axes.c2p(sweep_w[frame_index(t[0])], sweep_amp[frame_index(t[0])]),
            color="#E74C3C", radius=0.09,
        ))
        guide = always_redraw(lambda: Line(
            axes.c2p(sweep_w[frame_index(t[0])], 0.0),
            axes.c2p(sweep_w[frame_index(t[0])], sweep_amp[frame_index(t[0])]),
            color="#F4A259", stroke_width=1, stroke_opacity=0.6,
        ))
        reso = MathTex("\\text{Resonance!}", font_size=22, color="#E74C3C")
        resonant_idx = int(np.argmin(np.abs(sweep_w - omega0)))
        reso.move_to(axes.c2p(sweep_w[resonant_idx], sweep_amp[resonant_idx]) + UP * 0.4)
        reso.add_updater(lambda m: m.set_opacity(
            1.0 if abs(sweep_w[frame_index(t[0])] - omega0) < 0.35 else 0.0
        ))

        # ------------------------------------------------------------------
        # Physics driver — authoritative time from the scene clock
        # ------------------------------------------------------------------
        run_start: list[float] = [0.0]

        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = max(0.0, self.time - run_start[0])

        driver = Mobject()
        driver.add_updater(updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        reveal = Reveal(self)
        attention = Attention(self)

        # Staged intro: title, then axes, then the two resonance curves are
        # drawn in as a staggered sweep — the viewer meets the physics before
        # the probe starts.
        reveal.caption(title)
        reveal.draw(axes, run_time=1.4, lag=0.1)
        self.play(
            LaggedStart(
                Create(heavy_curve),
                Create(light_curve),
                lag_ratio=0.3,
            ),
            run_time=1.8,
        )
        self.wait(BEAT_PRE)
        reveal.beat(0.2)

        # Everything static is now on screen; the sweep runs from t=0.
        self.add(omega0_line, omega0_label)
        self.add(legend)
        self.add(guide, sweep_dot)
        self.add(reso)
        self.add(inset_title, pivot_dot, rod, bob)
        self.add(driver)
        run_start[0] = self.time

        self.wait(total_time)
