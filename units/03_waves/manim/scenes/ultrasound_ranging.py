"""Scene E — Ultrasound pulse-echo ranging (integrated-in from Medical Physics).

Animates a pulse emitted from a transducer, reflecting off a target at
distance d, and returning as an echo.  The distance is computed live as
d = v × t / 2.  At the end, a medical imaging strip shows layered depths.

Physics driver
--------------
physics_core.waves.equations.ultrasound_echo_distance provides the
distance calculation.

Animation pattern (IMPORTANT — see repo convention)
--------------------------------------------------
The visible curves are ``always_redraw`` mobjects rebuilt every frame as
a single VMobject from the current simulation time.  The simulation time
is read from ``scene.time`` (the authoritative video time), NOT
accumulated from updater ``dt`` values.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    BLUE_D,
    DOWN,
    GRAY,
    GREEN,
    GREY_D,
    LEFT,
    Line,
    MathTex,
    Mobject,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    YELLOW,
    always_redraw,
)

from physics_core.waves.equations import ultrasound_echo_distance


class UltrasoundRanging(Scene):
    """Pulse-echo ultrasound ranging — d = v × t / 2."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        speed: float = 1540.0  # speed of sound in tissue (m/s)
        target_distance: float = 0.1  # 10 cm
        total_time: float = 10.0

        # Round-trip time
        round_trip = 2.0 * target_distance / speed

        # Authoritative simulation time
        t: list[float] = [0.0]

        # ------------------------------------------------------------------
        # Scene layout
        # ------------------------------------------------------------------
        # Transducer at left, target at right
        transducer_x = -5.0
        target_x = 3.0
        scale_y = 2.0

        # Transducer visual
        transducer = VGroup(
            Line(
                transducer_x * RIGHT + 1.5 * UP,
                transducer_x * RIGHT + 1.5 * DOWN,
                color=GRAY, stroke_width=6,
            ),
            MathTex("\\text{Transducer}", font_size=18).next_to(
                transducer_x * RIGHT + 1.5 * UP, UP, buff=0.1
            ),
        )

        # Target visual
        target = VGroup(
            Line(
                target_x * RIGHT + 1.5 * UP,
                target_x * RIGHT + 1.5 * DOWN,
                color=RED, stroke_width=4,
            ),
            MathTex("\\text{Target}", font_size=18, color=RED).next_to(
                target_x * RIGHT + 1.5 * UP, UP, buff=0.1
            ),
        )

        # Distance label (static)
        distance_label_static = MathTex(
            f"d = {target_distance*100:.0f} \\text{{ cm}}", font_size=22
        ).next_to((transducer_x + target_x) / 2.0 * RIGHT + 1.8 * UP, UP)

        # ------------------------------------------------------------------
        # Pulse animation — a Gaussian-envelope wave packet
        # ------------------------------------------------------------------
        def pulse() -> VMobject:
            """Gaussian wave packet travelling from transducer to target and back."""
            elapsed = t[0]

            # Pulse position: goes out and back
            if elapsed <= round_trip:
                # Outgoing: x goes from transducer to target
                frac = elapsed / round_trip
                pulse_x = transducer_x + (target_x - transducer_x) * frac
                direction = 1.0  # rightward
            else:
                # Return: x goes from target back to transducer
                frac = (elapsed - round_trip) / round_trip
                pulse_x = target_x - (target_x - transducer_x) * frac
                direction = -1.0  # leftward

            # Gaussian envelope
            xs = np.linspace(-0.5, 0.5, 80)
            carrier = np.sin(2.0 * math.pi * 20.0 * xs)
            envelope = np.exp(-((xs / 0.15) ** 2))
            ys = envelope * carrier * scale_y

            pts = [
                (pulse_x + float(x)) * RIGHT + float(y) * UP
                for x, y in zip(xs, ys)
            ]
            vm = VMobject(color=BLUE, stroke_width=3)
            vm.set_points_as_corners(pts)
            return vm

        pulse_mob = always_redraw(pulse)

        # ------------------------------------------------------------------
        # Echo pulse (reflected, shown on return)
        # ------------------------------------------------------------------
        def echo() -> VMobject:
            """Reflected pulse (shown only on return journey)."""
            elapsed = t[0]
            if elapsed <= round_trip:
                # No echo yet
                return VMobject()

            # Echo position: returning from target to transducer
            frac = (elapsed - round_trip) / round_trip
            echo_x = target_x - (target_x - transducer_x) * frac

            xs = np.linspace(-0.5, 0.5, 80)
            carrier = np.sin(2.0 * math.pi * 20.0 * xs)
            envelope = np.exp(-((xs / 0.15) ** 2))
            ys = envelope * carrier * scale_y * 0.7  # attenuated

            pts = [
                (echo_x + float(x)) * RIGHT + float(y) * UP
                for x, y in zip(xs, ys)
            ]
            vm = VMobject(color=ORANGE, stroke_width=3)
            vm.set_points_as_corners(pts)
            return vm

        echo_mob = always_redraw(echo)

        # ------------------------------------------------------------------
        # Live readout
        # ------------------------------------------------------------------
        def readout() -> VGroup:
            elapsed = t[0]
            if elapsed <= round_trip:
                # Outgoing: compute distance so far
                frac = elapsed / round_trip
                current_d = target_distance * frac
                status = "Pulse outgoing..."
            else:
                # Returning
                frac = (elapsed - round_trip) / round_trip
                current_d = target_distance * (1.0 - frac)
                status = "Echo returning..."

            d_calc = ultrasound_echo_distance(speed, elapsed)

            lines = VGroup(
                MathTex(f"\\text{{{status}}}", font_size=22, color=YELLOW),
                MathTex(f"v = {speed:.0f} \\text{{ m/s}}", font_size=22),
                MathTex(f"t = {elapsed*1000:.1f} \\text{{ ms}}", font_size=22),
                MathTex(
                    f"d = v \\times t / 2 = {d_calc*100:.1f} \\text{{ cm}}",
                    font_size=22, color=GREEN,
                ),
            )
            lines.arrange(DOWN, aligned_edge=LEFT)
            lines.to_corner(UP + LEFT, buff=0.5)
            return lines

        readout_mob = always_redraw(readout)

        # ------------------------------------------------------------------
        # Medical imaging strip (appears at the end)
        # ------------------------------------------------------------------
        def imaging_strip() -> VGroup:
            """Layered depth strip simulating a medical ultrasound image."""
            elapsed = t[0]
            if elapsed < total_time - 2.0:
                return VGroup()

            strip = VGroup()

            # Background
            strip_bg = Line(
                LEFT * 4.5 + DOWN * 1.5,
                RIGHT * 4.5 + DOWN * 1.5,
                color=GRAY, stroke_width=60, stroke_opacity=0.3,
            )
            strip.add(strip_bg)

            # Tissue layers at different depths
            layers = [
                (0.02, 0.6, BLUE_D),   # skin
                (0.05, 0.4, GREEN),     # fat
                (0.08, 0.7, ORANGE),    # muscle
                (0.12, 0.5, RED),       # organ boundary
                (0.15, 0.3, BLUE),      # deeper tissue
            ]

            for depth, brightness, color in layers:
                # Scale depth to screen position
                x_pos = -4.5 + (depth / 0.2) * 9.0
                layer_line = Line(
                    x_pos * RIGHT + 0.5 * DOWN,
                    x_pos * RIGHT + 2.5 * DOWN,
                    color=color, stroke_width=3, stroke_opacity=brightness,
                )
                strip.add(layer_line)

                # Depth label
                depth_label = MathTex(
                    f"{depth*100:.0f} \\text{{ cm}}", font_size=12, color=color,
                ).next_to(layer_line, DOWN, buff=0.05)
                strip.add(depth_label)

            strip_title = MathTex(
                "\\text{Ultrasound Imaging Strip}", font_size=20, color=YELLOW,
            ).next_to(strip_bg, UP, buff=0.3)
            strip.add(strip_title)

            return strip

        strip_mob = always_redraw(imaging_strip)

        # ------------------------------------------------------------------
        # Physics driver
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        self.add(transducer, target, distance_label_static)
        self.add(pulse_mob, echo_mob)
        self.add(readout_mob)
        self.add(strip_mob)
        self.add(driver)

        self.wait(total_time)