"""Scene E — The electric motor: wire force, coil torque, and a commutator.

Three-part progressive build (Engine: ``physics_core.em.motor``):

A. A single current-carrying wire in a uniform B field.  Show the current
   direction, the into-page B field, and the force ``F = B I L sin(theta)``
   given by the right-hand rule.

B. A rectangular coil between two pole pieces.  Show the forces on the two
   active sides (a couple) and the resulting torque
   ``tau = N B I A sin(phi)``, sweeping phi so students see it vanish at
   phi = 0 / 180 deg and peak at 90 deg.

C. A spinning coil with a split-ring commutator.  The coil current flips
   sign every half turn (colour-coded) so the coil keeps turning one way;
   the angular velocity is read out live.

Animation pattern (repo convention)
-----------------------------------
The visible curves are ``always_redraw`` mobjects rebuilt every frame from
``t[0]`` (set from ``self.time`` by a driver).  Each moving curve is a
single VMobject built via ``set_points_as_corners``.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    Dot,
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
    Arc,
    Arrow,
    Circle,
    DOWN,
    FadeIn,
    FadeOut,
    Rectangle,
)

from physics_core.em.motor import ReferenceDCMotorConstant

# ---------------------------------------------------------------------------
# Scene constants
# ---------------------------------------------------------------------------
PART_B_START = 4.0
PART_C_START = 9.0
TOTAL_TIME = 16.0

# When the part-B demonstration coil first appears (cumulative self.time
# after the part-A builds) and how long it stays before the commutator spin.
COIL_B_APPEAR = 6.9
COIL_B_WINDOW = 3.0

DT_ENG = 1.0 / 120.0
T_ENG = TOTAL_TIME + 2.0  # integrate a little past the timeline for slack.
N_ENG = max(1, int(round(T_ENG / DT_ENG)) + 1)

# Coil geometry (scene units).
COIL_R = 2.0
POLE_X = 4.0
POLE_Y = 1.7


class ElectricMotor(Scene):
    """Wire force -> coil couple -> spinning commutator motor."""

    def _field_symbol(self, pos: np.ndarray, into_page: bool) -> VGroup:
        """Draw a small B-field marker: cross for into-page, dot for out."""
        grp = VGroup(Circle(radius=0.12, color=BLUE, stroke_width=1.5).move_to(pos))
        d = 0.08
        if into_page:
            grp.add(
                Line(
                    pos + np.array([-d, -d, 0.0]),
                    pos + np.array([d, d, 0.0]),
                    color=BLUE, stroke_width=1.5,
                )
            )
            grp.add(
                Line(
                    pos + np.array([-d, d, 0.0]),
                    pos + np.array([d, -d, 0.0]),
                    color=BLUE, stroke_width=1.5,
                )
            )
        else:
            grp.add(Dot(pos, radius=0.05, color=BLUE))
        return grp

    def _current_marker(
        self, pos: np.ndarray, colour: object, out_of_page: bool
    ) -> VGroup:
        """Draw a current direction marker (circle out / cross in) at *pos*."""
        grp = self._field_symbol(pos, into_page=not out_of_page)
        grp.set_color(colour)
        return grp

    def _build_coil(
        self,
        phi: float,
        sign_on_a: bool,
        show_forces: bool = True,
        show_normal: bool = True,
        show_torque: bool = True,
    ) -> VGroup:
        """Build one top-down coil snapshot at normal angle *phi* (radians)."""
        grp = VGroup()
        seg_angle = phi + math.pi / 2.0
        p_a = COIL_R * np.array([math.cos(seg_angle), math.sin(seg_angle), 0.0])
        p_b = -p_a

        # Coil plane — a single polyline through the shaft (one VMobject).
        seg = VMobject(color=GREY_D, stroke_width=8)
        seg.set_points_as_corners([p_b, np.zeros(3), p_a])
        grp.add(seg)

        a_is_out = sign_on_a
        grp.add(self._current_marker(p_a, RED if a_is_out else BLUE, a_is_out))
        grp.add(self._current_marker(p_b, BLUE if a_is_out else RED, not a_is_out))

        if show_forces:
            f_a_dir = np.array([0.0, 1.0, 0.0]) if a_is_out else np.array([0.0, -1.0, 0.0])
            f_b_dir = -f_a_dir
            grp.add(Arrow(p_a, p_a + 0.9 * f_a_dir, color=ORANGE, buff=0, stroke_width=3))
            grp.add(Arrow(p_b, p_b + 0.9 * f_b_dir, color=ORANGE, buff=0, stroke_width=3))

        if show_normal:
            n_hat = np.array([math.cos(phi), math.sin(phi), 0.0])
            grp.add(Arrow(np.zeros(3), 1.3 * n_hat, color=GREEN, buff=0, stroke_width=3))

        if show_torque:
            grp.add(
                Arc(
                    radius=COIL_R + 0.4,
                    start_angle=seg_angle - 0.4,
                    angle=1.4,
                    color=YELLOW, stroke_width=3,
                )
            )

        return grp

    def construct(self) -> None:
        # ----- Physics engine + pre-integration -----
        # The constant-drive motor keeps the coil turning smoothly through
        # the commutator half-turns (the proportional model stalls at the
        # zero-torque null points of a single coil).
        self.motor = ReferenceDCMotorConstant(
            N=10, B=0.5, A=0.02, J=1e-3, current=1.0, friction=0.02,
            phi=0.1, omega=1.0,
        )
        phi_arr = np.zeros(N_ENG, dtype=np.float64)
        omega_arr = np.zeros(N_ENG, dtype=np.float64)
        sign_arr = np.zeros(N_ENG, dtype=np.float64)
        motor = self.motor
        for i in range(N_ENG):
            phi_arr[i] = motor.phi
            omega_arr[i] = motor.omega
            sign_arr[i] = motor.commutator_sign()
            motor.step(DT_ENG)

        t: list[float] = [0.0]

        def field_index(tv: float) -> int:
            return max(0, min(int(tv / DT_ENG), N_ENG - 1))

        def motor_phi(tv: float) -> float:
            return float(phi_arr[field_index(tv)])

        def motor_omega(tv: float) -> float:
            return float(omega_arr[field_index(tv)])

        def motor_sign(tv: float) -> float:
            return float(sign_arr[field_index(tv)])

        def demo_phi(tv: float) -> float:
            # Part B sweep: 90 deg -> 180 -> 90 -> 0 -> 90 over the visible
            # window, passing both null points (phi = 0 and 180 deg).
            s = math.sin(2.0 * math.pi * (tv - COIL_B_APPEAR) / COIL_B_WINDOW)
            return math.radians(90.0 + 90.0 * s)

        # Physics driver (repo convention) — added before any self.wait() so
        # t[0] tracks self.time for every always_redraw below.
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)
        self.add(driver)

        # ----- Part A — single wire in a B field -----
        region_a = Rectangle(
            width=6.4, height=3.6, color=BLUE,
            fill_color=BLUE, fill_opacity=0.06, stroke_width=1,
            stroke_opacity=0.4,
        ).move_to(np.array([0.0, 0.0, 0.0]))
        region_label_a = MathTex(
            "\\mathbf{B}\\;\\otimes", font_size=22, color=BLUE,
        ).next_to(region_a, UP, buff=0.15)

        markers_a = VGroup()
        for gx in np.linspace(-2.7, 2.7, 7):
            for gy in np.linspace(-1.5, 1.5, 4):
                markers_a.add(self._field_symbol(np.array([gx, gy, 0.0]), True))

        wire_a = Line(
            np.array([-2.7, -0.55, 0.0]), np.array([2.7, -0.55, 0.0]),
            color=YELLOW, stroke_width=6,
        )
        current_arrow_a = Arrow(
            np.array([-2.55, 0.05, 0.0]), np.array([2.55, 0.05, 0.0]),
            color=GREEN, buff=0, stroke_width=3,
        ).shift(np.array([0.0, 0.6, 0.0]))
        current_label_a = MathTex("I", font_size=24, color=GREEN).next_to(
            current_arrow_a, UP, buff=0.1
        )
        force_a = Arrow(
            np.array([0.0, -0.55, 0.0]), np.array([0.0, 1.4, 0.0]),
            color=RED, buff=0, stroke_width=4,
        )
        force_label_a = MathTex("F", font_size=26, color=RED).next_to(
            force_a.get_end(), UP, buff=0.12
        )

        info_a = VGroup(
            MathTex("\\textbf{A} \\;\\text{— Force on a wire}", font_size=24, color=GREY_D),
            MathTex("F = B I L \\sin\\theta", font_size=22, color=RED),
            MathTex("\\text{right hand rule: } I \\times B", font_size=22, color=GREEN),
            MathTex("\\theta = 90^\\circ \\Rightarrow F = BIL \\; (\\text{max})", font_size=22, color=GREY_D),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(LEFT + UP, buff=0.4)

        self.add(region_a, region_label_a, markers_a, wire_a)
        self.play(FadeIn(current_arrow_a, current_label_a, shift=UP), run_time=1.0)
        self.play(FadeIn(force_a, force_label_a, shift=DOWN), run_time=1.0)
        self.play(FadeIn(info_a), run_time=0.8)
        self.wait(1.4)

        a_group = VGroup(
            region_a, region_label_a, markers_a, wire_a,
            current_arrow_a, current_label_a, force_a, force_label_a, info_a,
        )
        self.play(FadeOut(a_group), run_time=0.6)

        # ----- Part B — coil between pole pieces, couple -> torque -----
        pole_n = Rectangle(
            width=0.5, height=2 * POLE_Y, color=RED,
            fill_color=RED, fill_opacity=0.7, stroke_width=1,
        ).move_to(np.array([-POLE_X, 0.0, 0.0]))
        pole_s = Rectangle(
            width=0.5, height=2 * POLE_Y, color=BLUE,
            fill_color=BLUE, fill_opacity=0.7, stroke_width=1,
        ).move_to(np.array([POLE_X, 0.0, 0.0]))
        n_label = MathTex("N", font_size=28, color=RED).next_to(pole_n, LEFT, buff=0.2)
        s_label = MathTex("S", font_size=28, color=BLUE).next_to(pole_s, RIGHT, buff=0.2)

        b_arrows = VGroup()
        for gx in np.linspace(-3.1, 3.1, 7):
            for gy in np.linspace(-1.2, 1.2, 3):
                b_arrows.add(
                    Arrow(
                        np.array([gx - 0.18, gy, 0.0]),
                        np.array([gx + 0.18, gy, 0.0]),
                        color=BLUE, buff=0, stroke_width=2,
                    )
                )

        shaft = Dot(np.zeros(3), radius=0.09, color=GREY_D)

        info_b = VGroup(
            MathTex("\\textbf{B} \\;\\text{— Couple on a coil}", font_size=24, color=GREY_D),
            MathTex("\\tau = N B I A \\sin\\phi", font_size=24, color=GREEN),
            MathTex("\\text{max at } \\phi = 90^\\circ", font_size=22, color=ORANGE),
            MathTex("\\text{zero at } \\phi = 0^\\circ, 180^\\circ", font_size=22, color=GREY_D),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(LEFT + UP, buff=0.4)

        torque_anchor = Dot(np.array([0.0, -2.6, 0.0])).set_opacity(0.0)
        torque_label = MathTex("\\text{live torque}", font_size=20, color=GREY_D).next_to(
            torque_anchor, LEFT, buff=0.3
        )
        torque_readout = always_redraw(
            lambda: MathTex(
                "\\tau = "
                + f"{10 * 0.5 * 1.0 * 0.02 * math.sin(demo_phi(t[0])):.3f}"
                + "\\,\\mathrm{N\\,m}",
                font_size=22, color=GREEN,
            ).next_to(torque_anchor, RIGHT, buff=0.3)
        )
        coil_b = always_redraw(
            lambda: self._build_coil(
                demo_phi(t[0]), sign_on_a=(math.sin(demo_phi(t[0])) >= 0.0)
            )
        )

        self.play(
            FadeIn(pole_n, pole_s, n_label, s_label, shift=LEFT), run_time=0.8
        )
        self.play(FadeIn(b_arrows, shaft), run_time=0.8)
        self.play(FadeIn(info_b), run_time=0.5)
        self.add(torque_anchor, torque_label, torque_readout)
        self.add(coil_b)
        self.wait(COIL_B_WINDOW)

        # Keep the poles / field for part C; clear only the demo coil and the
        # part-B labels so the spinning coil does not overlap it.  Changing
        # always_redraw mobjects are removed instantly (manim cannot
        # interpolate a family that is rebuilt every frame).
        self.remove(coil_b, torque_readout)
        self.play(FadeOut(torque_anchor, torque_label, info_b), run_time=0.5)

        # ----- Part C — spinning coil with a commutator -----
        commutator_badge = always_redraw(
            lambda: MathTex(
                "\\text{commutator: current "
                + ("reversed" if motor_sign(t[0]) < 0.0 else "forward")
                + "}",
                font_size=20,
                color=RED if motor_sign(t[0]) < 0.0 else GREEN,
            ).next_to(np.zeros(3), DOWN, buff=0.7)
        )
        omega_readout = always_redraw(
            lambda: MathTex(
                "\\omega = " + f"{motor_omega(t[0]):.2f}" + "\\,\\mathrm{rad/s}",
                font_size=22, color=YELLOW,
            ).to_corner(RIGHT + UP, buff=0.4)
        )
        coil_c = always_redraw(
            lambda: self._build_coil(
                motor_phi(t[0]),
                sign_on_a=(motor_sign(t[0]) >= 0.0),
                show_torque=False,
            )
        )
        info_c = MathTex(
            "\\textbf{C} \\;\\text{— Commutator keeps it spinning}",
            font_size=24, color=GREY_D,
        ).to_corner(LEFT + UP, buff=0.4)

        self.add(coil_c, commutator_badge, omega_readout)
        self.play(FadeIn(info_c), run_time=0.5)
        self.wait(3.9)
