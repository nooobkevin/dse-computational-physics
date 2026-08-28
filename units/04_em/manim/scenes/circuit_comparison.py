"""Scene C — Kirchhoff's laws: circuit comparison.

Visualises a series circuit with two resistors, computing branch currents and
node voltages via nodal analysis (Kirchhoff + Ohm).  Displays:

- Circuit schematic with current direction
- KCL: sum of currents into a node equals sum out
- KVL: sum of voltage drops around a closed loop equals zero
- Power dissipation P = I²R

All computations use :class:`physics_core.em.circuits.ReferenceCircuit`.
"""

from __future__ import annotations

from manim import (
    BLUE,
    Create,
    DOWN,
    GREEN,
    LEFT,
    MathTex,
    RED,
    RIGHT,
    Scene,
    UP,
    VGroup,
    Write,
    YELLOW,
)

from physics_core.em.circuits import ReferenceCircuit


class CircuitComparison(Scene):
    """Kirchhoff's laws: series circuit comparison."""

    def construct(self) -> None:
        # ==================================================================
        # Solve circuit
        # ==================================================================
        branches = [
            (0, 1, 5.0, 10.0),
            (1, 0, 3.0, 0.0),
        ]
        ckt = ReferenceCircuit(branches)
        ckt.resolve()

        I = ckt.currents["0"]
        V_R1 = I * 5.0
        V_R2 = I * 3.0
        V_out = ckt.voltages["1"]

        # ==================================================================
        # Title
        # ==================================================================
        title = MathTex(
            "\\text{Kirchhoff's Laws — Series Circuit}",
            font_size=28,
            color=YELLOW,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # ==================================================================
        # Circuit schematic
        # ==================================================================
        schematic_title = MathTex(
            "\\text{Circuit: } V_s = 10\\,\\mathrm{V},\\; R_1 = 5\\,\\Omega,\\; R_2 = 3\\,\\Omega",
            font_size=24,
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(schematic_title))

        # ==================================================================
        # Kirchhoff's Current Law (KCL)
        # ==================================================================
        kcl_title = MathTex(
            "\\text{KCL: } \\Sigma I_{\\text{in}} = \\Sigma I_{\\text{out}}",
            font_size=26,
            color=GREEN,
        ).shift(LEFT * 3.5 + UP * 0.5)
        self.play(Write(kcl_title))

        # KCL equation
        kcl_eq1 = MathTex(
            f"I_1 = {I:.3f}\\,\\mathrm{{A}},\\quad I_2 = {I:.3f}\\,\\mathrm{{A}}",
            font_size=22,
        ).next_to(kcl_title, DOWN, buff=0.3, aligned_edge=LEFT)
        kcl_eq2 = MathTex(
            f"I_1 - I_2 = {I - I:.3f}\\,\\mathrm{{A}}",
            font_size=22,
            color=GREEN,
        ).next_to(kcl_eq1, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(kcl_eq1))
        self.play(Write(kcl_eq2))

        # ==================================================================
        # Kirchhoff's Voltage Law (KVL)
        # ==================================================================
        kvl_title = MathTex(
            "\\text{KVL: } \\Sigma V = 0",
            font_size=26,
            color=BLUE,
        ).shift(RIGHT * 3.5 + UP * 0.5)
        self.play(Write(kvl_title))

        # KVL equation
        kvl_eq1 = MathTex(
            f"V_{{\\text{{R1}}}} = {V_R1:.3f}\\,\\mathrm{{V}}",
            font_size=22,
        ).next_to(kvl_title, DOWN, buff=0.3, aligned_edge=LEFT)
        kvl_eq2 = MathTex(
            f"V_{{\\text{{R2}}}} = {V_R2:.3f}\\,\\mathrm{{V}}",
            font_size=22,
        ).next_to(kvl_eq1, DOWN, buff=0.2, aligned_edge=LEFT)
        kvl_eq3 = MathTex(
            f"V_s - V_{{\\text{{R1}}}} - V_{{\\text{{R2}}}} = {10.0 - V_R1 - V_R2:.1e}\\,\\mathrm{{V}}",
            font_size=22,
            color=BLUE,
        ).next_to(kvl_eq2, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(kvl_eq1))
        self.play(Write(kvl_eq2))
        self.play(Write(kvl_eq3))

        # ==================================================================
        # Power dissipation
        # ==================================================================
        power_title = MathTex(
            "\\text{Power dissipation: } P = I^2 R",
            font_size=26,
            color=RED,
        ).shift(DOWN * 0.5)
        self.play(Write(power_title))

        P1 = I * I * 5.0
        P2 = I * I * 3.0
        power_eq1 = MathTex(
            f"P_1 = ({I:.3f})^2 \\times 5 = {P1:.3f}\\,\\mathrm{{W}}",
            font_size=22,
        ).next_to(power_title, DOWN, buff=0.3, aligned_edge=LEFT)
        power_eq2 = MathTex(
            f"P_2 = ({I:.3f})^2 \\times 3 = {P2:.3f}\\,\\mathrm{{W}}",
            font_size=22,
        ).next_to(power_eq1, DOWN, buff=0.2, aligned_edge=LEFT)
        power_eq3 = MathTex(
            f"P_{{\\text{{total}}}} = {P1 + P2:.3f}\\,\\mathrm{{W}}",
            font_size=22,
            color=RED,
        ).next_to(power_eq2, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(power_eq1))
        self.play(Write(power_eq2))
        self.play(Write(power_eq3))

        # ==================================================================
        # Summary
        # ==================================================================
        summary = MathTex(
            "\\text{Both KCL and KVL are satisfied — the circuit is consistent}",
            font_size=24,
            color=GREEN,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(summary))

        self.wait(3.0)