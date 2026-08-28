"""Scene B — Ideal transformer voltage ratio and power conservation.

Shows a schematic transformer with primary and secondary coils, the
turns ratio Np/Ns, and the voltage/current relationships.  Numerical
values verify Vp/Vs = Np/Ns and power conservation Vp·Ip = Vs·Is.

The physics is computed by
:class:`physics_core.engineering.motors.ReferenceTransformer`, so the
animation uses the same engine as the teacher app and student exercise.
"""

from __future__ import annotations

from manim import (
    BLUE,
    Create,
    DOWN,
    GREEN,
    LEFT,
    MathTex,
    ORANGE,
    RIGHT,
    Scene,
    UP,
    VGroup,
    VMobject,
    Write,
    YELLOW,
)

from physics_core.engineering.motors import ReferenceTransformer


class TransformerScene(Scene):
    """Ideal transformer — turns ratio and power conservation."""

    def construct(self) -> None:
        t = ReferenceTransformer(Np=100, Ns=50, Vp=230.0, load_resistance=20.0)
        t.step()

        Vp = t.state["Vp"]
        Vs = t.state["Vs"]
        Ip = t.state["Ip"]
        Is = t.state["Is"]
        Pp = Vp * Ip
        Ps = Vs * Is

        # Core (iron)
        core = VMobject()
        core.set_points_as_corners([
            LEFT * 1.5 + DOWN * 1.5,
            RIGHT * 1.5 + DOWN * 1.5,
            RIGHT * 1.5 + UP * 1.5,
            LEFT * 1.5 + UP * 1.5,
            LEFT * 1.5 + DOWN * 1.5,
        ])
        core.set_color(BLUE)
        core.set_stroke(width=2, opacity=0.3)
        core.set_fill(BLUE, opacity=0.1)

        # Primary coil (left side)
        primary_label = MathTex("\\text{Primary}", font_size=28, color=YELLOW).next_to(
            LEFT * 3.5 + UP * 1.0, LEFT, buff=0
        )
        primary_turns = MathTex(f"N_p = {t.Np}", font_size=24).next_to(
            primary_label, DOWN, buff=0.3
        )
        primary_v = MathTex(f"V_p = {Vp:.1f}\\,\\text{{V}}", font_size=24, color=YELLOW).next_to(
            primary_turns, DOWN, buff=0.3
        )
        primary_i = MathTex(f"I_p = {Ip:.3f}\\,\\text{{A}}", font_size=24).next_to(
            primary_v, DOWN, buff=0.3
        )

        # Secondary coil (right side)
        secondary_label = MathTex("\\text{Secondary}", font_size=28, color=ORANGE).next_to(
            RIGHT * 3.5 + UP * 1.0, RIGHT, buff=0
        )
        secondary_turns = MathTex(f"N_s = {t.Ns}", font_size=24).next_to(
            secondary_label, DOWN, buff=0.3
        )
        secondary_v = MathTex(f"V_s = {Vs:.1f}\\,\\text{{V}}", font_size=24, color=ORANGE).next_to(
            secondary_turns, DOWN, buff=0.3
        )
        secondary_i = MathTex(f"I_s = {Is:.3f}\\,\\text{{A}}", font_size=24).next_to(
            secondary_v, DOWN, buff=0.3
        )

        # Formulas
        ratio_formula = MathTex(
            f"\\frac{{V_p}}{{V_s}} = \\frac{{N_p}}{{N_s}} = {t.Np/t.Ns:.2f}",
            font_size=28,
            color=GREEN,
        ).to_corner(DOWN + LEFT, buff=0.5)

        power_formula = MathTex(
            f"V_p I_p = {Pp:.1f}\\,\\text{{W}} \\quad V_s I_s = {Ps:.1f}\\,\\text{{W}}",
            font_size=28,
            color=GREEN,
        ).next_to(ratio_formula, DOWN, buff=0.3)

        # Animate
        self.play(Create(core))
        self.play(
            Write(primary_label),
            Write(primary_turns),
            Write(primary_v),
            Write(primary_i),
        )
        self.play(
            Write(secondary_label),
            Write(secondary_turns),
            Write(secondary_v),
            Write(secondary_i),
        )
        self.play(Write(ratio_formula))
        self.play(Write(power_formula))
        self.wait(2.0)