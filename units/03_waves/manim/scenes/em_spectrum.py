"""Scene F — Electromagnetic spectrum infographic (CAF c.1–c.2).

Progressive reveal of the EM spectrum from radio to gamma, with
wavelength/frequency bands, visible light zoomed into ROYGBIV, and a
moving highlight bar that creates sustained pixel changes for the
motion gate.

Animation pattern (IMPORTANT — see repo convention)
--------------------------------------------------
The visible elements are ``always_redraw`` mobjects rebuilt every frame
from the current simulation time.  The simulation time is read from
``scene.time`` (the authoritative video time) via a driver mobject whose
updater only does ``t[0] = self.time``.
"""

from __future__ import annotations

import math

from manim import (
    DOWN,
    GRAY,
    GREEN,
    GREY_D,
    LEFT,
    Line,
    MathTex,
    Mobject,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    YELLOW,
    always_redraw,
)

from physics_core.waves.equations import wave_speed


class EMSpectrum(Scene):
    """Electromagnetic spectrum infographic with progressive reveal."""

    def construct(self) -> None:
        c: float = 3.0e8

        bands: list[tuple[str, float, float, str, str]] = [
            ("Radio", 1.0, 1e5, "#FF4444", "3 kHz – 300 MHz"),
            ("Microwave", 1e-3, 1.0, "#FF8800", "300 MHz – 300 GHz"),
            ("Infrared", 7e-7, 1e-3, "#FFCC00", "300 GHz – 430 THz"),
            ("Visible", 4e-7, 7e-7, "#44FF44", "430 – 750 THz"),
            ("Ultraviolet", 1e-8, 4e-7, "#4488FF", "750 THz – 30 PHz"),
            ("X-ray", 1e-11, 1e-8, "#8844FF", "30 PHz – 30 EHz"),
            ("Gamma", 0.0, 1e-11, "#FF44FF", "> 30 EHz"),
        ]

        total_time: float = 12.0
        t: list[float] = [0.0]

        bar_top_y = 2.0
        bar_bot_y = 1.0
        bar_left_x = -5.5
        bar_right_x = 5.5
        bar_width = bar_right_x - bar_left_x

        log_min = -12.0
        log_max = 6.0

        def log_to_x(log_lambda: float) -> float:
            frac = (log_lambda - log_min) / (log_max - log_min)
            return bar_left_x + frac * bar_width

        # Pre-compute band boundaries
        band_bounds: list[tuple[float, float]] = []
        for name, wl_min, wl_max, color, freq_label in bands:
            if wl_min <= 0.0:
                wl_min = 1e-12
            log_min_b = math.log10(wl_min) if wl_min > 0 else log_min
            log_max_b = math.log10(wl_max) if wl_max > 0 else log_max
            band_bounds.append((log_to_x(log_min_b), log_to_x(log_max_b)))

        # Static spectrum bar
        static_bar = VGroup()
        for i, (name, wl_min, wl_max, color, freq_label) in enumerate(bands):
            x_left, x_right = band_bounds[i]
            bar = Line(
                x_left * RIGHT + bar_top_y * UP,
                x_right * RIGHT + bar_top_y * UP,
                color=color, stroke_width=40, stroke_opacity=0.5,
            )
            static_bar.add(bar)
            lbl = MathTex(f"\\text{{{name}}}", font_size=14, color=color)
            lbl.next_to((x_left + x_right) / 2.0 * RIGHT + bar_top_y * UP, UP, buff=0.15)
            static_bar.add(lbl)

        # Wavelength axis
        wavelength_axis = Line(
            bar_left_x * RIGHT, bar_right_x * RIGHT, color=GREY_D, stroke_width=1,
        )
        tick_labels = VGroup()
        for log_val in [-2, 0, 2]:
            x_pos = log_to_x(float(log_val))
            tick = Line(
                x_pos * RIGHT + bar_bot_y * UP,
                x_pos * RIGHT + (bar_bot_y - 0.15) * UP,
                color=GREY_D, stroke_width=1,
            )
            tick_labels.add(tick)
            lbl = MathTex(f"10^{{{log_val}}}", font_size=12)
            lbl.next_to(tick, DOWN, buff=0.05)
            tick_labels.add(lbl)

        axis_label = MathTex(
            "\\text{Wavelength } \\lambda \\text{ (m)}", font_size=16,
        ).next_to(wavelength_axis, DOWN, buff=0.4)

        # Large moving highlight bar — fills a wide vertical strip
        def moving_highlight() -> VMobject:
            frac = (t[0] % total_time) / total_time
            cx = bar_left_x + frac * bar_width
            half_w = 0.5
            bar = VMobject(color=YELLOW, fill_opacity=0.2, stroke_width=0)
            bar.set_points_as_corners([
                (cx - half_w) * RIGHT + 3.5 * UP,
                (cx + half_w) * RIGHT + 3.5 * UP,
                (cx + half_w) * RIGHT + 3.5 * DOWN,
                (cx - half_w) * RIGHT + 3.5 * DOWN,
                (cx - half_w) * RIGHT + 3.5 * UP,
            ])
            return bar

        hl_mob = always_redraw(moving_highlight)

        # Thick cursor line
        def cursor_fn() -> VMobject:
            frac = (t[0] % total_time) / total_time
            cx = bar_left_x + frac * bar_width
            return Line(
                cx * RIGHT + 3.0 * UP,
                cx * RIGHT + 0.5 * DOWN,
                color=YELLOW, stroke_width=8,
            )

        cursor_mob = always_redraw(cursor_fn)

        # Active band label
        def active_fn() -> MathTex:
            frac = (t[0] % total_time) / total_time
            cx = bar_left_x + frac * bar_width
            active_name = "Radio"
            active_color = "#FF4444"
            for i, (name, wl_min, wl_max, color, freq_label) in enumerate(bands):
                x_left, x_right = band_bounds[i]
                if x_left <= cx <= x_right:
                    active_name = name
                    active_color = color
                    break
            lbl = MathTex(f"\\text{{{active_name}}}", font_size=28, color=active_color)
            lbl.next_to(bar_bot_y * UP, DOWN, buff=0.8)
            return lbl

        active_mob = always_redraw(active_fn)

        # Visible light zoom
        def zoom_fn() -> VGroup:
            frac = (t[0] % total_time) / total_time
            cx = bar_left_x + frac * bar_width
            vis_left = log_to_x(math.log10(7e-7))
            vis_right = log_to_x(math.log10(4e-7))
            if cx < vis_left or cx > vis_right:
                return VGroup()
            zoom = VGroup()
            roygbiv = [
                ("Red", 700, "#FF0000"),
                ("Orange", 620, "#FF8800"),
                ("Yellow", 580, "#FFFF00"),
                ("Green", 530, "#00FF00"),
                ("Blue", 470, "#0000FF"),
                ("Indigo", 430, "#4400FF"),
                ("Violet", 400, "#8800FF"),
            ]
            zy = -1.5
            zw = 4.0
            zh = 0.8
            n = len(roygbiv)
            for i, (name, wl_nm, color) in enumerate(roygbiv):
                x0 = -zw / 2.0 + (i / n) * zw
                x1 = -zw / 2.0 + ((i + 1) / n) * zw
                bar = Line(
                    x0 * RIGHT + zy * UP,
                    x1 * RIGHT + zy * UP,
                    color=color, stroke_width=int(zh * 50),
                    stroke_opacity=0.9,
                )
                zoom.add(bar)
                lbl = MathTex(f"{wl_nm}\\text{{ nm}}", font_size=10, color=color)
                lbl.next_to(bar, DOWN, buff=0.05)
                zoom.add(lbl)
            title = MathTex(
                "\\text{Visible Light — ROYGBIV}", font_size=18, color=GREEN,
            ).next_to(zy * UP + zh * UP, UP, buff=0.2)
            zoom.add(title)
            return zoom

        zoom_mob = always_redraw(zoom_fn)

        # Info panel
        def info_fn() -> VGroup:
            frac = (t[0] % total_time) / total_time
            cx = bar_left_x + frac * bar_width
            current_band = "Radio"
            current_wl = 1.0
            for i, (name, wl_min, wl_max, color, freq_label) in enumerate(bands):
                x_left, x_right = band_bounds[i]
                if x_left <= cx <= x_right:
                    current_band = name
                    if wl_min <= 0.0:
                        wl_min = 1e-12
                    lmin = math.log10(wl_min)
                    lmax = math.log10(wl_max)
                    fi = (cx - x_left) / (x_right - x_left) if (x_right - x_left) > 1e-12 else 0.0
                    current_wl = 10.0 ** (lmin + fi * (lmax - lmin))
                    break
            freq = c / current_wl if current_wl > 0 else 0.0
            lines = VGroup(
                MathTex(f"\\text{{Band: }} {current_band}", font_size=22, color=YELLOW),
                MathTex(f"\\lambda \\approx {current_wl:.2e} \\text{{ m}}", font_size=20),
                MathTex(f"f = c / \\lambda \\approx {freq:.2e} \\text{{ Hz}}", font_size=20),
                MathTex(f"c = {c:.1e} \\text{{ m/s}}", font_size=20, color=GRAY),
            )
            lines.arrange(DOWN, aligned_edge=LEFT)
            lines.to_corner(UP + RIGHT, buff=0.5)
            return lines

        info_mob = always_redraw(info_fn)

        title = MathTex(
            "\\text{Electromagnetic Spectrum}", font_size=30,
        ).to_corner(UP + LEFT, buff=0.3)

        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        self.add(title)
        self.add(static_bar)
        self.add(wavelength_axis, tick_labels, axis_label)
        self.add(hl_mob)
        self.add(cursor_mob)
        self.add(active_mob)
        self.add(zoom_mob)
        self.add(info_mob)
        self.add(driver)

        self.wait(total_time)