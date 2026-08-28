"""Scene C — Stellar life cycle: schematic flow diagram.

Shows the life cycle of stars: nebula → main sequence → giant/supergiant
→ white dwarf / neutron star / black hole.  Uses Manim shapes and text
for a clean schematic diagram.
"""

from __future__ import annotations

from manim import (
    Arrow,
    BLUE,
    Create,
    DOWN,
    LEFT,
    ORANGE,
    RED,
    Rectangle,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
)


class StellarLifecycle(Scene):
    """Stellar life cycle flow diagram."""

    def construct(self) -> None:
        # ==================================================================
        # Stage boxes
        # ==================================================================
        box_w = 2.0
        box_h = 0.8

        # Positions (center of each box)
        nebula_pos = UP * 3.0
        ms_pos = UP * 1.0
        giant_pos = LEFT * 2.0 + DOWN * 1.0
        wd_pos = LEFT * 3.5 + DOWN * 3.0
        ns_pos = RIGHT * 3.5 + DOWN * 3.0

        # Nebula
        nebula_box = Rectangle(
            width=box_w, height=box_h, color=YELLOW,
            fill_color=YELLOW, fill_opacity=0.15,
        ).move_to(nebula_pos)
        nebula_text = Text("Nebula", font_size=24).move_to(nebula_pos)

        # Main Sequence
        ms_box = Rectangle(
            width=box_w, height=box_h, color=ORANGE,
            fill_color=ORANGE, fill_opacity=0.15,
        ).move_to(ms_pos)
        ms_text = Text("Main Sequence", font_size=24).move_to(ms_pos)

        # Giant / Supergiant
        giant_box = Rectangle(
            width=box_w, height=box_h, color=RED,
            fill_color=RED, fill_opacity=0.15,
        ).move_to(giant_pos)
        giant_text = Text("Giant / Supergiant", font_size=22).move_to(giant_pos)

        # White Dwarf
        wd_box = Rectangle(
            width=box_w, height=box_h, color=BLUE,
            fill_color=BLUE, fill_opacity=0.15,
        ).move_to(wd_pos)
        wd_text = Text("White Dwarf", font_size=24).move_to(wd_pos)

        # Neutron Star / Black Hole
        ns_box = Rectangle(
            width=box_w, height=box_h, color=RED,
            fill_color=RED, fill_opacity=0.15,
        ).move_to(ns_pos)
        ns_text = Text("Neutron Star\n/ Black Hole", font_size=20).move_to(ns_pos)

        # ==================================================================
        # Arrows
        # ==================================================================
        arrow1 = Arrow(nebula_pos + DOWN * box_h / 2, ms_pos + UP * box_h / 2, color=WHITE)
        arrow2 = Arrow(ms_pos + DOWN * box_h / 2, giant_pos + UP * box_h / 2, color=WHITE)
        arrow3 = Arrow(
            giant_pos + DOWN * box_h / 2 + LEFT * box_w / 4,
            wd_pos + UP * box_h / 2 + RIGHT * box_w / 4,
            color=WHITE,
        )
        arrow4 = Arrow(
            giant_pos + DOWN * box_h / 2 + RIGHT * box_w / 4,
            ns_pos + UP * box_h / 2 + LEFT * box_w / 4,
            color=WHITE,
        )

        # Labels on arrows
        low_mass_label = Text("Low mass\n(≤8 M☉)", font_size=16, color=BLUE).move_to(
            (giant_pos + wd_pos) / 2 + LEFT * 0.5
        )
        high_mass_label = Text("High mass\n(>8 M☉)", font_size=16, color=RED).move_to(
            (giant_pos + ns_pos) / 2 + RIGHT * 0.5
        )

        # ==================================================================
        # Title
        # ==================================================================
        title = Text("Stellar Life Cycle", font_size=32).to_corner(UP + LEFT, buff=0.5)

        # ==================================================================
        # Animate
        # ==================================================================
        self.play(Write(title))

        self.play(Create(nebula_box), Write(nebula_text))
        self.play(Create(arrow1))
        self.play(Create(ms_box), Write(ms_text))
        self.play(Create(arrow2))
        self.play(Create(giant_box), Write(giant_text))

        self.play(Create(arrow3), Create(arrow4))
        self.play(Write(low_mass_label), Write(high_mass_label))

        self.play(Create(wd_box), Write(wd_text))
        self.play(Create(ns_box), Write(ns_text))

        self.wait(2.0)