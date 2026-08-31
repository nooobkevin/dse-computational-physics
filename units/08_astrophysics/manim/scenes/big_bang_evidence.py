"""Scene G — Two pillars of evidence for the Big Bang (CAF b.8).

A progressive-reveal infographic that builds up the two lines of
observational evidence for the Big Bang:

1. **Pillar 1 — expansion / redshift** — an inflating balloon-surface
   analogy: galaxy dots on an expanding 2D surface all recede from each
   other; farther pairs recede faster (Hubble's law ``v = H0 * d``).

2. **Pillar 2 — the cosmic microwave background (CMB)** — the sky is a
   nearly uniform glow; revealing the Planck blackbody curve at
   ``T = 2.725 K`` (peak ≈ 1.06 mm, Wien), plus a faint dipole anisotropy
   bar (our motion relative to the CMB, ΔT ≈ ±3.36 mK).

The scene closes with a title card "CMB + redshift = evidence for the
Big Bang".  A tall scanning cursor sweeps the frame throughout (see how
``EMSpectrum`` in unit 03 solved the motion gate).

Physics driver
--------------
ReferenceHRDiagram from physics_core.astrophysics.hr_diagram supplies the
Planck blackbody curve at T_CMB (and Wien's law for the peak).

Animation pattern (IMPORTANT — repo convention)
-----------------------------------------------
The visible time-varying elements (balloon surface, galaxy dots,
recession arrows, scanning cursor) are ``always_redraw`` mobjects rebuilt
every frame as single VMobjects from the authoritative video time.  The
simulation time is read from ``scene.time`` (NOT accumulated from updater
``dt``) via a driver mobject whose updater only does ``t[0] = self.time``.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    Arrow,
    BLUE,
    DOWN,
    FadeIn,
    GRAY,
    GREY_D,
    LEFT,
    Line,
    MathTex,
    Mobject,
    ORANGE,
    RED,
    Scene,
    UP,
    VGroup,
    VMobject,
    WHITE,
    YELLOW,
    always_redraw,
)

from physics_core.astrophysics.hr_diagram import ReferenceHRDiagram

T_CMB: float = 2.725  # CMB temperature (K)
CLOSING_BG: str = "#14141f"


def _p(x: float, y: float) -> np.ndarray:
    return np.array([x, y, 0.0])


class BigBangEvidence(Scene):
    """Two pillars of evidence for the Big Bang: expansion/redshift + CMB."""

    def construct(self) -> None:
        hr = ReferenceHRDiagram()

        total_time: float = 18.0
        t: list[float] = [0.0]

        # ------------------------------------------------------------------
        # Shared layout
        # ------------------------------------------------------------------
        title = MathTex(
            "\\text{Two Pillars of Evidence for the Big Bang}", font_size=30,
        ).to_corner(UP + LEFT, buff=0.4)

        L_LEFT, L_RIGHT = -6.3, -0.3
        L_TOP, L_BOT = 2.9, -2.9
        L_CX = (L_LEFT + L_RIGHT) / 2.0
        R_LEFT, R_RIGHT = 0.3, 6.3
        R_TOP, R_BOT = 2.9, -2.9
        R_CX = (R_LEFT + R_RIGHT) / 2.0

        def rect(px1: float, py1: float, px2: float, py2: float,
                 color: str = GREY_D) -> VMobject:
            vm = VMobject(color=color, stroke_width=2)
            vm.set_points_as_corners([
                _p(px1, py1), _p(px2, py1), _p(px2, py2),
                _p(px1, py2), _p(px1, py1),
            ])
            return vm

        left_frame = rect(L_LEFT, L_BOT, L_RIGHT, L_TOP)
        right_frame = rect(R_LEFT, R_BOT, R_RIGHT, R_TOP)

        left_title = MathTex(
            "\\text{Pillar 1 --- Expansion / Redshift}", font_size=22,
            color=ORANGE,
        ).move_to(_p(L_CX, L_TOP - 0.35))
        right_title = MathTex(
            "\\text{Pillar 2 --- Cosmic Microwave Background}", font_size=22,
            color=YELLOW,
        ).move_to(_p(R_CX, R_TOP - 0.35))

        # ------------------------------------------------------------------
        # Pillar 1 — balloon-surface expansion
        # ------------------------------------------------------------------
        b_center = _p(L_CX, 0.35)
        R0: float = 0.85
        R_GROWTH: float = 1.1
        N_DOTS: int = 8

        def balloon_radius() -> float:
            frac: float = min(t[0] / total_time, 1.0)
            return R0 * (1.0 + R_GROWTH * frac)

        def dot_pos(idx: int, r: float) -> np.ndarray:
            theta: float = idx * 2.0 * math.pi / N_DOTS
            return _p(b_center[0] + r * math.cos(theta),
                      b_center[1] + r * math.sin(theta))

        def balloon_fn() -> VMobject:
            r: float = balloon_radius()
            pts: list[np.ndarray] = [
                _p(b_center[0] + r * math.cos(a),
                   b_center[1] + r * math.sin(a))
                for a in [i * 2.0 * math.pi / 64 for i in range(65)]
            ]
            vm = VMobject(color=ORANGE, stroke_width=3)
            vm.set_points_as_corners(pts)
            return vm

        def galaxy_dots() -> VGroup:
            r = balloon_radius()
            dots: VGroup = VGroup()
            for i in range(N_DOTS):
                px, py, _ = dot_pos(i, r)
                color = YELLOW if i == 0 else WHITE
                dots.add(Line(_p(px - 0.04, py), _p(px + 0.04, py),
                              color=color, stroke_width=5))
                dots.add(Line(_p(px, py - 0.04), _p(px, py + 0.04),
                              color=color, stroke_width=5))
            return dots

        def arrows_fn() -> VGroup:
            r = balloon_radius()
            obs = dot_pos(0, r)
            arrows: VGroup = VGroup()
            for idx in (1, 2, 3):
                far = dot_pos(idx, r)
                arrows.add(Arrow(obs, far, buff=0.0, color=RED, stroke_width=3))
            return arrows

        balloon = always_redraw(balloon_fn)
        galaxy_mob = always_redraw(galaxy_dots)
        arrow_mob = always_redraw(arrows_fn)

        left_caption = MathTex(
            "v = H_0\\,d \\quad (\\text{farther } \\Rightarrow \\text{ faster})",
            font_size=20, color=RED,
        ).move_to(_p(L_CX, L_BOT + 0.4))
        observer_note = MathTex(
            "\\text{observer: every galaxy sees the same pattern}",
            font_size=14, color=GRAY,
        ).move_to(_p(L_CX, L_BOT + 0.95))

        # ------------------------------------------------------------------
        # Pillar 2 — CMB glow + blackbody curve + dipole
        # ------------------------------------------------------------------
        peak_mm: float = hr.peak_wavelength(T_CMB) * 1e3

        glow_color: str = "#FF9E5E"
        glow = VMobject(color=glow_color, fill_color=glow_color,
                        fill_opacity=0.85, stroke_width=2)
        glow.set_points_as_corners([
            _p(1.2, 2.35), _p(5.6, 2.35), _p(5.6, 1.65), _p(1.2, 1.65),
            _p(1.2, 2.35),
        ])
        glow_caption = MathTex(
            "\\text{Sky: nearly uniform glow } (\\Delta T/T \\approx 10^{-5})",
            font_size=15, color=GRAY,
        ).move_to(_p(R_CX, 1.4))

        bb_left, bb_right = 1.1, 5.7
        bb_bot, bb_top = 0.1, 1.1
        wl_min: float = 0.05e-3
        wl_max: float = 10.0e-3

        def wl_to_x(wl: float) -> float:
            frac = (wl - wl_min) / (wl_max - wl_min)
            return bb_left + frac * (bb_right - bb_left)

        bb_x_axis = Line(_p(bb_left, bb_bot), _p(bb_right, bb_bot),
                         color=GREY_D, stroke_width=1)
        bb_y_axis = Line(_p(bb_left, bb_bot), _p(bb_left, bb_top),
                         color=GREY_D, stroke_width=1)
        bb_x_label = MathTex("\\lambda \\, (\\text{mm})", font_size=14, color=GREY_D)
        bb_x_label.next_to(_p((bb_left + bb_right) / 2, bb_bot), DOWN, buff=0.1)
        bb_y_label = MathTex("I_{\\lambda}", font_size=14, color=GREY_D)
        bb_y_label.next_to(_p(bb_left, (bb_bot + bb_top) / 2), LEFT, buff=0.1)

        wl_arr = np.linspace(wl_min, wl_max, 400)
        intensity = hr.blackbody_curve(T_CMB, wl_arr)
        curve_pts: list[np.ndarray] = [
            _p(wl_to_x(wl), bb_bot + intensity[i] * (bb_top - bb_bot))
            for i, wl in enumerate(wl_arr)
        ]
        bb_curve = VMobject(color=RED, stroke_width=2.5)
        bb_curve.set_points_as_corners(curve_pts)

        peak_x = wl_to_x(peak_mm * 1e-3)
        peak_line = Line(_p(peak_x, bb_bot), _p(peak_x, bb_top),
                         color=ORANGE, stroke_width=1, stroke_opacity=0.6)
        peak_label = MathTex(
            f"\\text{{peak }} \\approx {peak_mm:.2f}\\text{{ mm}}",
            font_size=15, color=ORANGE,
        ).move_to(_p(peak_x + 0.25, bb_bot + 0.28))
        temp_label = MathTex(
            "T = 2.725\\text{ K}", font_size=18, color=YELLOW,
        ).move_to(_p(bb_right - 0.5, bb_top + 0.2))

        dip_cy = -2.35
        dip_left, dip_right = 1.6, 5.2
        dip_cx = (dip_left + dip_right) / 2.0
        dip_base = Line(_p(dip_left, dip_cy), _p(dip_right, dip_cy),
                        color=GRAY, stroke_width=2)
        dip_tick = Line(_p(dip_cx, dip_cy - 0.12), _p(dip_cx, dip_cy + 0.12),
                        color=WHITE, stroke_width=2)
        dip_offset = Line(_p(dip_cx + 0.15, dip_cy - 0.12),
                          _p(dip_cx + 0.15, dip_cy + 0.12),
                          color=YELLOW, stroke_width=3)
        dip_arrows = VGroup(
            Arrow(_p(dip_cx, dip_cy + 0.2), _p(dip_left + 0.4, dip_cy + 0.2),
                  buff=0.0, color=BLUE, stroke_width=2),
            Arrow(_p(dip_cx, dip_cy + 0.2), _p(dip_right - 0.4, dip_cy + 0.2),
                  buff=0.0, color=BLUE, stroke_width=2),
        )
        dip_title = MathTex("\\text{anisotropy}", font_size=14, color=GRAY,
                           ).move_to(_p(R_CX, dip_cy + 0.45))
        dip_label = MathTex(
            "\\text{dipole } \\Delta T \\approx \\pm 3.36\\text{ mK}",
            font_size=15, color=YELLOW,
        ).move_to(_p(R_CX, dip_cy - 0.5))

        # ------------------------------------------------------------------
        # Closing title card
        # ------------------------------------------------------------------
        card = VMobject(color=CLOSING_BG, fill_color=CLOSING_BG,
                        fill_opacity=0.95, stroke_width=0)
        card.set_points_as_corners([
            _p(-4.4, 1.2), _p(4.4, 1.2), _p(4.4, -1.2), _p(-4.4, -1.2),
            _p(-4.4, 1.2),
        ])
        closing = MathTex(
            "\\text{CMB + redshift = evidence for the Big Bang}",
            font_size=30, color=YELLOW,
        )

        # ------------------------------------------------------------------
        # Scanning cursor (semi-transparent bar + thin line)
        # ------------------------------------------------------------------
        scan_left, scan_right = -6.3, 6.3
        scan_span = scan_right - scan_left

        def scan_x() -> float:
            frac = (t[0] % total_time) / total_time
            return scan_left + frac * scan_span

        def highlight_bar() -> VMobject:
            cx = scan_x()
            hw = 0.7
            vm = VMobject(color=YELLOW, fill_opacity=0.12, stroke_width=0)
            vm.set_points_as_corners([
                _p(cx - hw, 4.0), _p(cx + hw, 4.0), _p(cx + hw, -4.0),
                _p(cx - hw, -4.0), _p(cx - hw, 4.0),
            ])
            return vm

        def cursor() -> Line:
            cx = scan_x()
            return Line(_p(cx, 4.0), _p(cx, -4.0), color=YELLOW, stroke_width=6)

        hl_mob = always_redraw(highlight_bar)
        cursor_mob = always_redraw(cursor)

        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)
        self.add(driver)

        # ------------------------------------------------------------------
        # Progressive reveal
        # ------------------------------------------------------------------
        self.play(FadeIn(title))
        self.add(hl_mob, cursor_mob)

        self.play(FadeIn(left_frame), FadeIn(left_title))
        self.add(balloon, galaxy_mob, arrow_mob)
        self.play(FadeIn(left_caption), FadeIn(observer_note))
        self.wait(2.0)

        self.play(FadeIn(right_frame), FadeIn(right_title))
        self.play(FadeIn(glow), FadeIn(glow_caption))
        self.play(FadeIn(bb_x_axis), FadeIn(bb_y_axis),
                  FadeIn(bb_x_label), FadeIn(bb_y_label))
        self.play(FadeIn(bb_curve))
        self.play(FadeIn(peak_line), FadeIn(peak_label), FadeIn(temp_label))
        self.play(FadeIn(dip_base), FadeIn(dip_tick), FadeIn(dip_offset),
                  FadeIn(dip_arrows), FadeIn(dip_title), FadeIn(dip_label))
        self.wait(1.5)

        self.play(FadeIn(card))
        self.play(FadeIn(closing))
        self.wait(2.5)
