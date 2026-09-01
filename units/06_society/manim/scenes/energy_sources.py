"""Energy sources comparison — fission/fusion, solar, wind.

Shows:
1. Nuclear fission/fusion with ΔE = Δmc² annotation
2. Solar panel with solar constant
3. Wind turbine with P ∝ v³ curve
4. Bar chart comparing output magnitudes

Uses :class:`physics_core.society.energy.ReferenceEnergySim` for all
physics calculations.

Animation pattern (proven)
--------------------------
t = [0.0] driver with dt-named updater; always_redraw for time-varying
elements; single VMobject curves with set_points_as_corners.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    BLUE_D,
    Create,
    DOWN,
    FadeIn,
    GREEN,
    GREY_D,
    LEFT,
    MathTex,
    Mobject,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    VMobject,
    WHITE,
    Write,
    YELLOW,
    always_redraw,
)

from physics_core.society.energy import ReferenceEnergySim


class EnergySources(Scene):
    """Energy sources: fission/fusion, solar, wind — comparison."""

    def construct(self) -> None:
        sim = ReferenceEnergySim()
        total_time: float = 16.0

        # Authoritative simulation time
        t: list[float] = [0.0]

        # ==================================================================
        # Title
        # ==================================================================
        title = Text("Energy Sources Comparison", font_size=30, color=YELLOW)
        title.to_corner(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.3)

        # ==================================================================
        # Part 1 — Nuclear fission / fusion (ΔE = Δmc²)
        # ==================================================================
        fission_title = Text("Nuclear Fission / Fusion", font_size=24, color=ORANGE)
        fission_title.move_to(np.array([-5.0, 1.8, 0]))
        self.play(Write(fission_title))

        # Mass-energy formula
        formula = MathTex(
            "\\Delta E = \\Delta m \\, c^2", font_size=28, color=YELLOW
        )
        formula.move_to(np.array([-5.0, 1.0, 0]))
        self.play(Write(formula))

        # 1 amu example
        _, energy_MeV = sim.mass_energy_delta(1.0, in_amu=True)
        amu_example = Text(
            f"1 amu mass defect → {energy_MeV:.0f} MeV", font_size=20, color=WHITE
        )
        amu_example.move_to(np.array([-5.0, 0.2, 0]))
        self.play(Write(amu_example))

        # Fission example: 0.1 amu
        _, fission_MeV = sim.mass_energy_delta(0.1, in_amu=True)
        fission_example = Text(
            f"Fission: 0.1 amu → {fission_MeV:.1f} MeV", font_size=18, color=GREEN
        )
        fission_example.move_to(np.array([-5.0, -0.4, 0]))
        self.play(Write(fission_example))

        self.wait(0.5)

        # ==================================================================
        # Part 2 — Solar power
        # ==================================================================
        solar_title = Text("Solar Power", font_size=24, color=YELLOW)
        solar_title.move_to(np.array([0.0, 1.8, 0]))
        self.play(Write(solar_title))

        solar_formula = MathTex(
            "P = S \\, A \\, \\eta", font_size=28, color=YELLOW
        )
        solar_formula.move_to(np.array([0.0, 1.0, 0]))
        self.play(Write(solar_formula))

        # Solar constant
        sc_text = Text(
            "Solar constant S = 1000 W/m²", font_size=18, color=WHITE
        )
        sc_text.move_to(np.array([0.0, 0.2, 0]))
        self.play(Write(sc_text))

        # Example: 1 m² panel at 20% efficiency
        p_solar = sim.solar_power(area=1.0, solar_constant=1000.0, efficiency=0.20)
        solar_example = Text(
            f"1 m² panel (20% eff.) → {p_solar:.0f} W", font_size=18, color=GREEN
        )
        solar_example.move_to(np.array([0.0, -0.4, 0]))
        self.play(Write(solar_example))

        self.wait(0.5)

        # ==================================================================
        # Part 3 — Wind turbine (P vs v³ curve)
        # ==================================================================
        wind_title = Text("Wind Turbine Power", font_size=24, color=BLUE)
        wind_title.move_to(np.array([5.0, 1.8, 0]))
        self.play(Write(wind_title))

        wind_formula = MathTex(
            "P = \\frac{1}{2} \\eta \\rho A v^3", font_size=26, color=YELLOW
        )
        wind_formula.move_to(np.array([5.0, 1.0, 0]))
        self.play(Write(wind_formula))

        # Axes for P vs v curve
        wind_axes = VGroup()
        wx_axis = VMobject()
        wx_axis.set_points_as_corners([
            np.array([2.5, -1.5, 0]),
            np.array([7.5, -1.5, 0]),
        ])
        wx_axis.set_color(GREY_D)
        wx_axis.set_stroke(width=2)
        wind_axes.add(wx_axis)

        wy_axis = VMobject()
        wy_axis.set_points_as_corners([
            np.array([2.5, -1.5, 0]),
            np.array([2.5, 1.2, 0]),
        ])
        wy_axis.set_color(GREY_D)
        wy_axis.set_stroke(width=2)
        wind_axes.add(wy_axis)

        w_label_x = MathTex("v", font_size=20, color=GREY_D).next_to(
            np.array([7.5, -1.5, 0]), RIGHT, buff=0.1
        )
        w_label_y = MathTex("P", font_size=20, color=GREY_D).next_to(
            np.array([2.5, 1.2, 0]), UP, buff=0.1
        )

        self.play(Create(wind_axes), Write(w_label_x), Write(w_label_y))

        # Wind speed range: 0 to 15 m/s
        v_max = 15.0
        r = 5.0  # rotor radius
        v_pts = np.linspace(0.01, v_max, 100)
        p_vals = [sim.wind_power(r=r, wind_speed=float(v), air_density=1.2, efficiency=0.4) / 1000.0 for v in v_pts]
        p_max = max(p_vals)

        # Scale: x: 2.5..7.5 for 0..v_max, y: -1.5..1.2 for 0..p_max
        def v_to_x(v: float) -> float:
            return 2.5 + (v / v_max) * 5.0

        def p_to_y(p_kw: float) -> float:
            return -1.5 + (p_kw / p_max) * 2.7

        # Build the cubic curve as a single VMobject
        curve_pts = [
            np.array([v_to_x(float(v)), p_to_y(float(p)), 0])
            for v, p in zip(v_pts, p_vals)
        ]
        wind_curve = VMobject(color=BLUE_D, stroke_width=3)
        wind_curve.set_points_as_corners(curve_pts)

        # Animate the curve being drawn
        self.play(Create(wind_curve), run_time=2.0)

        # Animate a dot moving along the curve to show cubic scaling
        dot = Mobject()

        def dot_updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(dot_updater)

        # Moving dot along curve
        moving_dot = VMobject(color=RED)
        moving_dot.set_points_as_corners([np.array([2.5, -1.5, 0])])

        # We'll use always_redraw for the moving dot
        def moving_dot_fn() -> VMobject:
            # Cycle wind speed from 0 to v_max over time
            cycle_t = t[0] % 4.0  # 4-second cycle
            v_cycle = (cycle_t / 4.0) * v_max
            idx = min(int(v_cycle / v_max * 99), 98)
            x = v_to_x(v_cycle)
            y = p_to_y(p_vals[idx])
            dot_vm = VMobject(color=RED, stroke_width=4)
            dot_vm.set_points_as_corners([
                np.array([x - 0.05, y, 0]),
                np.array([x + 0.05, y, 0]),
            ])
            return dot_vm

        moving_dot_redraw = always_redraw(moving_dot_fn)

        # Label showing cubic scaling
        cubic_label = Text(
            "P ∝ v³: double v → 8× power", font_size=16, color=BLUE_D
        )
        cubic_label.move_to(np.array([5.0, -2.0, 0]))

        self.add(driver)
        self.add(moving_dot_redraw)
        self.play(Write(cubic_label))
        self.wait(2.0)

        # Remove moving dot and driver for next section
        self.remove(moving_dot_redraw)
        self.remove(driver)

        # ==================================================================
        # Part 4 — Bar chart comparing output magnitudes
        # ==================================================================
        bar_title = Text("Power Output Comparison (log scale)", font_size=22, color=YELLOW)
        bar_title.move_to(np.array([0.0, -2.5, 0]))
        self.play(Write(bar_title))

        # Every bar is computed from its own physics:
        #   fission: 1 kg U-235, mass defect ~0.09% -> ΔE = Δmc², per day
        #   solar:   P = S·A·η for a 1 m² panel
        #   wind:    P = ½ηρπr²v³ for r = 5 m at 10 m/s
        fission_E_J, _ = sim.mass_energy_delta(0.0009, in_amu=False)
        p_fission = fission_E_J / 86400.0
        p_solar = sim.solar_power(area=1.0, solar_constant=1000.0, efficiency=0.20)
        p_wind = sim.wind_power(r=5.0, wind_speed=10.0, air_density=1.2, efficiency=0.4)

        def fmt_power(p: float) -> str:
            if p >= 1e6:
                return f"{p/1e6:.0f} MW"
            if p >= 1e3:
                return f"{p/1e3:.1f} kW"
            return f"{p:.0f} W"

        # Spans ~10^2 W to ~10^9 W, so heights use log10(P).
        log_lo, log_hi = 1.0, 9.0
        bar_data = [
            ("Fission (1 kg/day)", p_fission, ORANGE),
            ("Solar (1 m²)", p_solar, YELLOW),
            ("Wind (r=5m, v=10)", p_wind, BLUE),
        ]

        bars = VGroup()
        bar_labels = VGroup()
        bar_values = VGroup()

        for i, (name, val, color) in enumerate(bar_data):
            x_pos = -3.0 + i * 3.0
            bar_h = (math.log10(val) - log_lo) / (log_hi - log_lo) * 3.0
            bar = VMobject(color=color, fill_opacity=0.8)
            bar.set_points_as_corners([
                np.array([x_pos - 0.3, -1.5, 0]),
                np.array([x_pos + 0.3, -1.5, 0]),
                np.array([x_pos + 0.3, -1.5 + bar_h, 0]),
                np.array([x_pos - 0.3, -1.5 + bar_h, 0]),
            ])
            bars.add(bar)

            label = Text(name, font_size=14, color=color)
            label.move_to(np.array([x_pos, -1.8, 0]))
            bar_labels.add(label)

            val_text = Text(fmt_power(val), font_size=14, color=WHITE)
            val_text.move_to(np.array([x_pos, -1.5 + bar_h + 0.2, 0]))
            bar_values.add(val_text)

        self.play(
            *[Create(b) for b in bars],
            *[Write(l) for l in bar_labels],
            *[Write(v) for v in bar_values],
            run_time=2.0,
        )

        self.wait(2.0)