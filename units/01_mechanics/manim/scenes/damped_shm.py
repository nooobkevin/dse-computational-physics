"""Scene D — Damped SHM: underdamped, critically damped, overdamped.

Three damped harmonic oscillators simulated side by side via
ReferencePendulumSim (small_angle=True for linear damping).  Each trace
shows theta-vs-time with the analytic decay envelope A·e^(-γt).

Physics: θ'' + b·θ' + ω₀²·θ = 0, ω₀² = g/L.
Regimes: underdamped (b<2ω₀), critically damped (b=2ω₀), overdamped (b>2ω₀).

CAF: Annex 3 enrichment + CP activity "SHM with or without damping".
"""

from __future__ import annotations

import math
from bisect import bisect_right
from dataclasses import dataclass

import numpy as np
from manim import (
    Axes,
    Dot,
    DOWN,
    GRAY_BROWN,
    GREY_D,
    MathTex,
    Mobject,
    Scene,
    UP,
    VGroup,
    VMobject,
    always_redraw,
)

from physics_core.mechanics.pendulum import ReferencePendulumSim


@dataclass
class _RegimeData:
    name: str
    b: float
    color: str
    sim_ts: list[float]
    sim_thetas: list[float]
    env_ts: list[float]
    env_ys: list[float]


class DampedSHM(Scene):
    """Three damping regimes side by side with analytic decay envelopes."""

    def construct(self) -> None:
        L: float = 1.0
        g: float = 9.81
        omega0: float = math.sqrt(g / L)
        theta0: float = 0.8
        total_time: float = 6.0

        b_critical: float = 2.0 * omega0
        regimes_raw = [
            ("Underdamped", 0.5 * omega0, "#E74C3C"),
            ("Critically damped", b_critical, "#2ECC71"),
            ("Overdamped", 3.0 * omega0, "#3498DB"),
        ]

        def simulate(b: float, dt: float = 0.005) -> tuple[list[float], list[float]]:
            sim = ReferencePendulumSim(
                length=L, g=g, theta0=theta0, omega0=0.0,
                dt=dt, scheme="verlet", small_angle=True,
                damping_coefficient=b,
            )
            ts: list[float] = [0.0]
            thetas: list[float] = [theta0]
            while ts[-1] < total_time:
                sim.step()
                ts.append(sim.state["t"])
                thetas.append(sim.state["theta"])
            return ts, thetas

        def envelope(b: float, n: int = 300) -> tuple[list[float], list[float]]:
            gamma = b / 2.0
            ts = [total_time * i / (n - 1) for i in range(n)]
            ys = [theta0 * math.exp(-gamma * t) for t in ts]
            return ts, ys

        regimes: list[_RegimeData] = []
        for name, b, color in regimes_raw:
            sim_ts, sim_thetas = simulate(b)
            env_ts, env_ys = envelope(b)
            regimes.append(_RegimeData(
                name=name, b=b, color=color,
                sim_ts=sim_ts, sim_thetas=sim_thetas,
                env_ts=env_ts, env_ys=env_ys,
            ))

        margin = 0.5
        panel_w = (14.0 - 2 * margin) / 3.0
        panel_h = 4.0
        y_max = theta0 * 1.2

        panels: list[Axes] = []
        for i in range(3):
            ax = Axes(
                x_range=[0, total_time, 1],
                y_range=[-y_max, y_max, 0.5],
                x_length=panel_w,
                y_length=panel_h,
                axis_config={
                    "color": GREY_D,
                    "include_numbers": True,
                    "font_size": 16,
                },
            )
            ax.move_to(np.array([
                -14.0 / 2 + margin + panel_w / 2 + i * panel_w,
                0.5,
                0,
            ]))
            panels.append(ax)

        title = MathTex(
            "\\text{Damped SHM: } \\ddot{\\theta} + b\\dot{\\theta} + \\omega_0^2\\theta = 0",
            font_size=28, color=GREY_D,
        )
        title.to_edge(UP, buff=0.3)

        regime_labels = VGroup()
        for i, rd in enumerate(regimes):
            lbl = MathTex(
                f"\\text{{{rd.name}}}" + f"\\; b={rd.b:.2f}",
                font_size=20, color=rd.color,
            )
            lbl.next_to(panels[i], UP, buff=0.1)
            regime_labels.add(lbl)

        t: list[float] = [0.0]

        def make_trace(rd: _RegimeData, ax: Axes) -> VMobject:
            scr = [ax.c2p(tt, th) for tt, th in zip(rd.sim_ts, rd.sim_thetas)]
            def _inner() -> VMobject:
                vm = VMobject(color=rd.color, stroke_width=2.5)
                n = bisect_right(rd.sim_ts, t[0])
                if n >= 2:
                    vm.set_points_as_corners(list(scr[:n]))
                return vm
            return always_redraw(_inner)

        def make_envelope(rd: _RegimeData, ax: Axes) -> VMobject:
            pos_scr = [ax.c2p(tt, yy) for tt, yy in zip(rd.env_ts, rd.env_ys)]
            neg_scr = [ax.c2p(tt, -yy) for tt, yy in zip(rd.env_ts, rd.env_ys)]
            def _inner() -> VMobject:
                g = VGroup()
                for pts in (pos_scr, neg_scr):
                    vm = VMobject(color=rd.color, stroke_width=1.5, stroke_opacity=0.5)
                    n = bisect_right(rd.env_ts, t[0])
                    if n >= 2:
                        vm.set_points_as_corners(list(pts[:n]))
                    g.add(vm)
                return g
            return always_redraw(_inner)

        trace_mobs: list[VMobject] = []
        env_mobs: list[VMobject] = []
        dot_mobs: list[VMobject] = []
        for i, rd in enumerate(regimes):
            trace_mobs.append(make_trace(rd, panels[i]))
            # θ₀e^{-γt} bounds the motion only in the underdamped regime; the
            # critical/overdamped solutions decay slower early on and would
            # visibly break out of this envelope.
            if rd.name == "Underdamped":
                env_mobs.append(make_envelope(rd, panels[i]))
            dot_mobs.append(_make_dot(rd, panels[i], t))

        caption = MathTex(
            "\\text{Envelope (underdamped): } \\theta_0 e^{-\\gamma t}, \\; \\gamma = b/2",
            font_size=22, color=GRAY_BROWN,
        )
        caption.next_to(panels[-1], DOWN, buff=0.4)

        def updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(updater)

        self.add(title)
        self.add(regime_labels)
        for ax in panels:
            self.add(ax)
        for tm in trace_mobs:
            self.add(tm)
        for em in env_mobs:
            self.add(em)
        for dm in dot_mobs:
            self.add(dm)
        self.add(caption)
        self.add(driver)

        self.wait(total_time)


def _make_dot(rd: _RegimeData, ax: Axes, t: list[float]) -> VMobject:
    """Animated dot tracking the current position on the curve."""
    scr = [ax.c2p(tt, th) for tt, th in zip(rd.sim_ts, rd.sim_thetas)]
    def _inner() -> Dot:
        n = bisect_right(rd.sim_ts, t[0])
        idx = max(0, min(n - 1, len(scr) - 1))
        return Dot(scr[idx], color=rd.color, radius=0.08)
    return always_redraw(_inner)