"""3Blue1Brown-style polish helpers for our Manim scenes.

Shared palette, easing presets, staged-reveal and attention helpers so
scenes feel cohesive and "eased" like a 3b1b video without repeating
boilerplate.

Importable in Docker renders because render.sh exports PYTHONPATH=/work/src.
"""

from __future__ import annotations

from manim import (
    Flash,
    Group,
    Indicate,
    LaggedStart,
    Mobject,
    Scene,
    ShowPassingFlash,
    SurroundingRectangle,
    Create,
    FadeIn,
    Write,
    UP,
    rate_functions,
)


PALETTE = {
    "background": "#1C1C1C",
    "primary": "#58C4DD",
    "secondary": "#83C167",
    "accent": "#FFFF00",
    "warning": "#FF6666",
    "text": "#FFFFFF",
    "muted": "#A9B2C3",
    "orange": "#F4A259",
    "blue": "#4A90E2",
    "green": "#2ECC71",
    "red": "#E74C3C",
}

EASE = {
    "default": rate_functions.smooth,
    "inout": rate_functions.ease_in_out_sine,
    "out": rate_functions.ease_out_cubic,
    "pulse": rate_functions.there_and_back,
}

BEAT_PRE = 0.3
BEAT_POST = 1.0


class Reveal:
    """Staged, paced reveals — the 3b1b narrative rhythm.

    Nothing appears all at once: each beat is followed by a short pause so
    the viewer can read the frame before the next element lands.
    """

    def __init__(self, scene: Scene) -> None:
        self.scene = scene

    def caption(self, mob: Mobject, run_time: float = 1.0) -> None:
        self.scene.play(Write(mob), run_time=run_time, rate_func=EASE["default"])
        self.scene.wait(BEAT_POST)

    def group(self, *mobs: Mobject, run_time: float = 1.2, lag: float = 0.15) -> None:
        self.scene.play(
            LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in mobs], lag_ratio=lag),
            run_time=run_time,
        )
        self.scene.wait(BEAT_PRE + 0.2)

    def draw(self, *mobs: Mobject, run_time: float = 1.5, lag: float = 0.2) -> None:
        self.scene.play(
            LaggedStart(*[Create(m) for m in mobs], lag_ratio=lag),
            run_time=run_time,
        )
        self.scene.wait(BEAT_PRE)

    def beat(self, seconds: float = 0.5) -> None:
        self.scene.wait(seconds)


class Attention:
    """Direct the viewer's eye — 3b1b's signature highlight moves."""

    def __init__(self, scene: Scene) -> None:
        self.scene = scene

    def flash(self, target: Mobject, color: str = PALETTE["accent"]) -> None:
        """Radial spark at a key moment — the most 3b1b-characteristic cue."""
        self.scene.wait(BEAT_PRE)
        self.scene.play(Flash(target, color=color, line_length=0.2), run_time=0.8)
        self.scene.wait(0.25)

    def pop(self, mob: Mobject, color: str = PALETTE["accent"],
            scale: float = 1.2) -> None:
        self.scene.wait(BEAT_PRE)
        self.scene.play(Indicate(mob, color=color, scale_factor=scale),
                        run_time=0.8)

    def trace(self, path: Mobject, color: str = PALETTE["primary"],
              time_width: float = 1.5) -> None:
        """Glow travelling along a curve — 'look along this path'."""
        ghost = path.copy().set_stroke(color, width=5)
        self.scene.play(ShowPassingFlash(ghost, time_width=time_width),
                        run_time=1.5)

    def box(self, mob: Mobject, color: str = PALETTE["accent"],
            buff: float = 0.2) -> Mobject:
        rect = SurroundingRectangle(mob, color=color, buff=buff, stroke_width=2.5)
        self.scene.play(Create(rect), run_time=0.8)
        return rect
