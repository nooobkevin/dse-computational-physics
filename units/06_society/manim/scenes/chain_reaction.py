"""Scene C — Nuclear fission chain reaction and critical mass concept.

Shows a schematic of a fission chain reaction: a neutron strikes a
fissile nucleus (e.g. U-235), causing it to split and release more
neutrons.  The neutron multiplication factor k determines whether the
chain is subcritical (k<1), critical (k=1), or supercritical (k>1).

English labels only.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLUE,
    Create,
    DOWN,
    FadeIn,
    GREEN,
    LEFT,
    ORANGE,
    RED,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
)


class ChainReaction(Scene):
    """Nuclear fission chain reaction / critical mass concept."""

    def construct(self) -> None:
        title = Text("Nuclear Fission Chain Reaction", font_size=30)
        title.to_corner(UP, buff=0.3)
        self.play(Write(title))

        # ==================================================================
        # Left panel: schematic of fission
        # ==================================================================
        panel_title = Text("Fission process", font_size=22, color=YELLOW)
        panel_title.move_to(np.array([-3.5, 1.5, 0]))
        self.play(Write(panel_title))

        # Neutron (small circle)
        neutron = Text("n", font_size=20, color=ORANGE)
        neutron.move_to(np.array([-5.0, 0.0, 0]))
        self.play(Create(neutron))

        # Nucleus (larger circle)
        nucleus = Text("U-235", font_size=20, color=RED)
        nucleus.move_to(np.array([-3.5, 0.0, 0]))
        self.play(Create(nucleus))

        # Arrow from neutron to nucleus
        arrow_text = Text("\\rightarrow", font_size=24, color=WHITE)
        arrow_text.move_to(np.array([-4.3, 0.0, 0]))
        self.play(Write(arrow_text))

        # Fission products
        fission_text = Text("Fission", font_size=18, color=GREEN)
        fission_text.move_to(np.array([-2.0, 0.0, 0]))
        self.play(Write(fission_text))

        # Released neutrons (3)
        released = VGroup()
        for i in range(3):
            n = Text("n", font_size=16, color=ORANGE)
            n.move_to(np.array([-0.5 + i * 0.5, 0.0, 0]))
            released.add(n)
        self.play(Create(released))

        # Energy release
        energy_text = Text("+ Energy", font_size=18, color=YELLOW)
        energy_text.next_to(released, RIGHT, buff=0.3)
        self.play(Write(energy_text))

        self.wait(0.5)

        # ==================================================================
        # Right panel: chain reaction generations
        # ==================================================================
        gen_title = Text("Chain reaction (k=2)", font_size=22, color=GREEN)
        gen_title.move_to(np.array([3.0, 1.5, 0]))
        self.play(Write(gen_title))

        # Draw generations
        gen_positions = [
            (3.0, 0.0),      # gen 0: 1 neutron
            (3.0, -0.8),     # gen 1: 2 neutrons
            (3.0, -1.6),     # gen 2: 4 neutrons
            (3.0, -2.4),     # gen 3: 8 neutrons
        ]

        gen_labels = [
            "Gen 0: 1 n",
            "Gen 1: 2 n",
            "Gen 2: 4 n",
            "Gen 3: 8 n",
        ]

        gen_group = VGroup()
        for i, (gx, gy) in enumerate(gen_positions):
            label = Text(gen_labels[i], font_size=16, color=ORANGE)
            label.move_to(np.array([gx, gy, 0]))
            gen_group.add(label)

        self.play(*[Write(lbl) for lbl in gen_group], run_time=1.5)

        # ==================================================================
        # Bottom: critical mass concept
        # ==================================================================
        concept_lines = [
            "Neutron multiplication factor k",
            "k = neutrons in next generation / neutrons in current generation",
            "",
            "k < 1: subcritical — chain dies out",
            "k = 1: critical — self-sustaining chain reaction",
            "k > 1: supercritical — runaway (nuclear explosion)",
            "",
            "Critical mass: minimum mass of fissile material",
            "  needed to sustain a chain reaction (k >= 1)",
            "",
            "Control rods absorb excess neutrons to keep k = 1",
            "Moderator (e.g. graphite, water) slows neutrons",
            "  to increase probability of fission",
        ]

        concept_group = VGroup()
        for i, line in enumerate(concept_lines):
            t = Text(line, font_size=16, color=WHITE)
            t.to_corner(DOWN + LEFT, buff=0.2 + i * 0.3)
            concept_group.add(t)

        self.play(*[FadeIn(t) for t in concept_group], run_time=2.0)
        self.wait(2.0)