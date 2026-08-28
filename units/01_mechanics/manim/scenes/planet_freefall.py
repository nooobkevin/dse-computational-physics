"""Scene E — Free fall on different planets (Earth, Moon, Mars).

Three objects are dropped simultaneously from the same height on
Earth (g=9.81), Moon (g=1.62), Mars (g=3.71).  Each object's position
is labelled, and a small v-t trace panel shows the linear velocity
growth with slope = g.

Physics: y(t) = y0 - ½·g·t², v(t) = -g·t.
Sanity: Moon g=1.62 m/s² ≈ 1/6 of Earth.  Mars g=3.71 m/s² ≈ 0.38× Earth.

CAF reference: CP activity "free fall on different planets".
"""

from __future__ import annotations

import math
from bisect import bisect_right

import numpy as np
from manim import (
    Axes,
    BLUE,
    DOWN,
    GRAY_BROWN,
    GREEN,
    GREY_D,
    Dot,
    LEFT,
    MathTex,
    Mobject,
    RED,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    YELLOW,
    always_redraw,
)


class PlanetFreeFall(Scene):
    """Three objects dropped simultaneously on Earth, Moon, Mars."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Physics parameters
        # ------------------------------------------------------------------
        # Planet: (name, g, colour)
        planets: list[tuple[str, float, str]] = [
            ("Earth", 9.81, BLUE),
            ("Moon", 1.62, GREY_D),
            ("Mars", 3.71, RED),
        ]
        y0: float = 4.0  # initial height (m)
        total_time: float = 2.5  # seconds

        # Pre-compute analytical trajectories
        def freefall_trajectory(
            g: float, dt: float = 0.005
        ) -> tuple[list[float], list[float], list[float]]:
            ts: list[float] = [0.0]
            ys: list[float] = [y0]
            vs: list[float] = [0.0]
            while ts[-1] < total_time:
                t_next = ts[-1] + dt
                ts.append(t_next)
                ys.append(y0 - 0.5 * g * t_next**2)
                vs.append(g * t_next)
            return ts, ys, vs

        planet_data: list[dict] = []
        for name, g, color in planets:
            ts, ys, vs = freefall_trajectory(g)
            # Clamp to ground
            clamped_ys = [max(y, 0.0) for y in ys]
            planet_data.append({
                "name": name, "g": g, "color": color,
                "ts": ts, "ys": clamped_ys, "vs": vs,
            })

        # ------------------------------------------------------------------
        # Main axes — position vs time
        # ------------------------------------------------------------------
        y_range = [0, y0 * 1.1]
        main_axes = Axes(
            x_range=[0, total_time, 0.5],
            y_range=y_range,
            x_length=6.5,
            y_length=4.5,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 20,
            },
        )
        main_axes.to_corner(UP + LEFT, buff=0.5)

        main_x_label = MathTex("t", font_size=24).next_to(
            main_axes.x_axis.get_end(), DOWN
        )
        main_y_label = MathTex("y", font_size=24).next_to(
            main_axes.y_axis.get_end(), LEFT
        )

        main_title = MathTex(
            "\\text{Position vs time}", font_size=24, color=GRAY_BROWN,
        )
        main_title.next_to(main_axes, UP, buff=0.1)

        # ------------------------------------------------------------------
        # v-t trace panel (small, bottom-right)
        # ------------------------------------------------------------------
        v_axes = Axes(
            x_range=[0, total_time, 0.5],
            y_range=[0, max(d["g"] * total_time for d in planet_data) * 1.15, 5],
            x_length=4.5,
            y_length=2.5,
            axis_config={
                "color": GREY_D,
                "include_numbers": True,
                "font_size": 16,
            },
        )
        v_axes.to_corner(DOWN + RIGHT, buff=0.5)

        v_title = MathTex(
            "\\text{Speed vs time}", font_size=20, color=GRAY_BROWN,
        )
        v_title.next_to(v_axes, UP, buff=0.1)

        v_x_label = MathTex("t", font_size=20).next_to(
            v_axes.x_axis.get_end(), DOWN
        )
        v_y_label = MathTex("|v|", font_size=20).next_to(
            v_axes.y_axis.get_end(), LEFT
        )

        # ------------------------------------------------------------------
        # Legend
        # ------------------------------------------------------------------
        legend = VGroup(
            *[
                MathTex(
                    f"\\text{{{d['name']}}} \\; (g={d['g']:.2f})",
                    color=d["color"], font_size=20,
                )
                for d in planet_data
            ]
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + RIGHT, buff=0.5)

        # ------------------------------------------------------------------
        # Progressive-reveal curves
        # ------------------------------------------------------------------
        t: list[float] = [0.0]

        def make_fall_curve(
            data: dict, ax: Axes, is_v: bool = False,
        ) -> VMobject:
            if is_v:
                scr = [ax.c2p(tt, vv) for tt, vv in zip(data["ts"], data["vs"])]
            else:
                scr = [ax.c2p(tt, yy) for tt, yy in zip(data["ts"], data["ys"])]
            def _inner() -> VMobject:
                vm = VMobject(color=data["color"], stroke_width=3)
                n = bisect_right(data["ts"], t[0])
                if n >= 2:
                    vm.set_points_as_corners(list(scr[:n]))
                return vm
            return always_redraw(_inner)

        def make_falling_dot(data: dict) -> VMobject:
            def _inner() -> Dot:
                i = bisect_right(data["ts"], t[0]) - 1
                i = max(0, min(i, len(data["ts"]) - 1))
                y = data["ys"][i]
                x_pos = main_axes.c2p(data["ts"][i], y)
                return Dot(x_pos, color=data["color"], radius=0.10)
            return always_redraw(_inner)

        def make_position_label(data: dict) -> VMobject:
            def _inner() -> MathTex:
                i = bisect_right(data["ts"], t[0]) - 1
                i = max(0, min(i, len(data["ts"]) - 1))
                y = data["ys"][i]
                lbl = MathTex(
                    f"y={y:.2f}\\;\\text{{m}}",
                    font_size=14, color=data["color"],
                )
                lbl.next_to(
                    main_axes.c2p(data["ts"][i], y),
                    RIGHT, buff=0.15,
                )
                return lbl
            return always_redraw(_inner)

        fall_curves: list[VMobject] = []
        fall_dots: list[VMobject] = []
        pos_labels: list[VMobject] = []
        v_curves: list[VMobject] = []

        for d in planet_data:
            fall_curves.append(make_fall_curve(d, main_axes))
            fall_dots.append(make_falling_dot(d))
            pos_labels.append(make_position_label(d))
            v_curves.append(make_fall_curve(d, v_axes, is_v=True))

        # ------------------------------------------------------------------
        # Physics driver
        # ------------------------------------------------------------------
        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        # ------------------------------------------------------------------
        # Assemble
        # ------------------------------------------------------------------
        self.add(main_title, main_axes, main_x_label, main_y_label)
        self.add(legend)
        self.add(v_title, v_axes, v_x_label, v_y_label)
        for fc in fall_curves:
            self.add(fc)
        for fd in fall_dots:
            self.add(fd)
        for pl in pos_labels:
            self.add(pl)
        for vc in v_curves:
            self.add(vc)
        self.add(driver)

        self.wait(total_time)