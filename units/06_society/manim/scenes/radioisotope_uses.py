"""Radioisotope applications — medical imaging, therapy, industrial.

Shows three applications of radioactive isotopes with progressive reveal:
1. Medical imaging (gamma camera / PET-style tracer route)
2. Radiotherapy (targeted dose)
3. Industrial (thickness gauge)

Progressive reveal per application with English labels only.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    BLUE_D,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    GREY_D,
    LEFT,
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
)


class RadioisotopeUses(Scene):
    """Radioisotope applications: medical imaging, therapy, industrial."""

    def construct(self) -> None:
        total_time: float = 14.0
        t: list[float] = [0.0]

        # ==================================================================
        # Title
        # ==================================================================
        title = Text("Uses of Radioactive Isotopes", font_size=30, color=YELLOW)
        title.to_corner(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.3)

        # ==================================================================
        # Application 1 — Medical Imaging (gamma camera / PET tracer)
        # ==================================================================
        app1_title = Text("1. Medical Imaging (Gamma Camera)", font_size=22, color=GREEN)
        app1_title.move_to(np.array([-5.0, 1.5, 0]))
        self.play(Write(app1_title))

        # Body outline (simplified as an ellipse-like shape)
        body = VGroup()
        # Head
        head = VMobject(color=WHITE, stroke_width=2)
        head.set_points_as_corners([
            np.array([-0.5, 1.0, 0]),
            np.array([0.5, 1.0, 0]),
            np.array([0.5, 1.8, 0]),
            np.array([-0.5, 1.8, 0]),
        ])
        body.add(head)
        # Torso
        torso = VMobject(color=WHITE, stroke_width=2)
        torso.set_points_as_corners([
            np.array([-1.2, -1.5, 0]),
            np.array([1.2, -1.5, 0]),
            np.array([1.2, 1.0, 0]),
            np.array([-1.2, 1.0, 0]),
        ])
        body.add(torso)

        body.move_to(np.array([-2.0, -0.3, 0]))
        self.play(Create(body), run_time=1.0)

        # Tracer injection point
        inject_label = Text("Tracer injected", font_size=14, color=ORANGE)
        inject_label.move_to(np.array([-3.5, -0.5, 0]))
        self.play(Write(inject_label))

        # Animated tracer path (dots moving through body)
        tracer_path = [
            np.array([-3.0, -0.5, 0]),
            np.array([-2.0, -0.3, 0]),
            np.array([-1.5, 0.2, 0]),
            np.array([-1.0, 0.5, 0]),
            np.array([-0.5, 0.3, 0]),
            np.array([0.0, 0.0, 0]),
        ]

        tracer_dots = VGroup()
        for pt in tracer_path:
            dot = VMobject(color=ORANGE, stroke_width=3)
            dot.set_points_as_corners([
                pt + np.array([-0.03, 0, 0]),
                pt + np.array([0.03, 0, 0]),
            ])
            tracer_dots.add(dot)

        self.play(*[Create(d) for d in tracer_dots], run_time=1.5)

        # Gamma detector
        detector = VMobject(color=YELLOW, stroke_width=2)
        detector.set_points_as_corners([
            np.array([1.5, -1.0, 0]),
            np.array([2.5, -1.0, 0]),
            np.array([2.5, 1.0, 0]),
            np.array([1.5, 1.0, 0]),
        ])
        detector.move_to(np.array([2.5, -0.3, 0]))
        det_label = Text("Gamma detector", font_size=14, color=YELLOW)
        det_label.next_to(detector, RIGHT, buff=0.2)

        self.play(Create(detector), Write(det_label))

        # Gamma rays (arrows from body to detector)
        gamma_rays = VGroup()
        for y_pos in [-0.5, 0.0, 0.5]:
            ray = VMobject(color=YELLOW, stroke_width=1)
            ray.set_points_as_corners([
                np.array([0.5, y_pos, 0]),
                np.array([2.0, y_pos, 0]),
            ])
            gamma_rays.add(ray)

        self.play(*[Create(r) for r in gamma_rays], run_time=0.5)

        # Description
        desc1 = Text(
            "Radioactive tracer accumulates in target organ;\n"
            "gamma rays detected to form image",
            font_size=14, color=WHITE
        )
        desc1.move_to(np.array([-2.0, -2.3, 0]))
        self.play(Write(desc1))
        self.wait(0.5)

        # Fade out app1
        self.play(
            FadeOut(app1_title), FadeOut(body), FadeOut(inject_label),
            FadeOut(tracer_dots), FadeOut(detector), FadeOut(det_label),
            FadeOut(gamma_rays), FadeOut(desc1),
        )

        # ==================================================================
        # Application 2 — Radiotherapy
        # ==================================================================
        app2_title = Text("2. Radiotherapy (Targeted Dose)", font_size=22, color=RED)
        app2_title.move_to(np.array([-5.0, 1.5, 0]))
        self.play(Write(app2_title))

        # Tumour (red circle)
        tumour = VMobject(color=RED, fill_opacity=0.5)
        tumour.set_points_as_corners([
            np.array([-0.5, -0.5, 0]),
            np.array([0.5, -0.5, 0]),
            np.array([0.5, 0.5, 0]),
            np.array([-0.5, 0.5, 0]),
        ])
        tumour.move_to(np.array([0.0, 0.0, 0]))
        tumour_label = Text("Tumour", font_size=14, color=RED)
        tumour_label.next_to(tumour, DOWN, buff=0.2)
        self.play(Create(tumour), Write(tumour_label))

        # Radiation beams (arrows from multiple angles)
        beams = VGroup()
        angles = [-60, -30, 0, 30, 60]
        for angle_deg in angles:
            angle_rad = np.radians(angle_deg)
            start = np.array([
                -3.0 * np.cos(angle_rad),
                3.0 * np.sin(angle_rad),
                0,
            ])
            end = np.array([
                -0.3 * np.cos(angle_rad),
                0.3 * np.sin(angle_rad),
                0,
            ])
            beam = VMobject(color=YELLOW, stroke_width=2)
            beam.set_points_as_corners([start, end])
            beams.add(beam)

        self.play(*[Create(b) for b in beams], run_time=1.5)

        # Description
        desc2 = Text(
            "Focused radiation beam destroys tumour cells;\n"
            "radioactive source (e.g. Co-60) delivers precise dose",
            font_size=14, color=WHITE
        )
        desc2.move_to(np.array([0.0, -2.3, 0]))
        self.play(Write(desc2))
        self.wait(0.5)

        # Fade out app2
        self.play(
            FadeOut(app2_title), FadeOut(tumour), FadeOut(tumour_label),
            FadeOut(beams), FadeOut(desc2),
        )

        # ==================================================================
        # Application 3 — Industrial (thickness gauge)
        # ==================================================================
        app3_title = Text("3. Industrial Thickness Gauge", font_size=22, color=BLUE)
        app3_title.move_to(np.array([-5.0, 1.5, 0]))
        self.play(Write(app3_title))

        # Source
        source = VMobject(color=ORANGE, fill_opacity=0.8)
        source.set_points_as_corners([
            np.array([-0.5, 0.8, 0]),
            np.array([0.5, 0.8, 0]),
            np.array([0.5, 1.5, 0]),
            np.array([-0.5, 1.5, 0]),
        ])
        source.move_to(np.array([-2.0, 1.0, 0]))
        source_label = Text("Radioactive source", font_size=14, color=ORANGE)
        source_label.next_to(source, UP, buff=0.1)
        self.play(Create(source), Write(source_label))

        # Material sheet
        sheet = VMobject(color=GREY_D, fill_opacity=0.5)
        sheet.set_points_as_corners([
            np.array([-3.0, -0.2, 0]),
            np.array([3.0, -0.2, 0]),
            np.array([3.0, 0.2, 0]),
            np.array([-3.0, 0.2, 0]),
        ])
        sheet.move_to(np.array([0.0, 0.0, 0]))
        sheet_label = Text("Material (paper / metal)", font_size=14, color=GREY_D)
        sheet_label.next_to(sheet, DOWN, buff=0.2)
        self.play(Create(sheet), Write(sheet_label))

        # Radiation passing through
        radiation_lines = VGroup()
        for x_pos in [-1.0, 0.0, 1.0]:
            line = VMobject(color=YELLOW, stroke_width=1)
            line.set_points_as_corners([
                np.array([x_pos, 1.0, 0]),
                np.array([x_pos, -0.2, 0]),
            ])
            radiation_lines.add(line)

        self.play(*[Create(r) for r in radiation_lines], run_time=0.5)

        # Detector below
        detector2 = VMobject(color=GREEN, stroke_width=2)
        detector2.set_points_as_corners([
            np.array([-1.0, -1.0, 0]),
            np.array([1.0, -1.0, 0]),
            np.array([1.0, -0.8, 0]),
            np.array([-1.0, -0.8, 0]),
        ])
        detector2.move_to(np.array([0.0, -1.2, 0]))
        det2_label = Text("Detector", font_size=14, color=GREEN)
        det2_label.next_to(detector2, DOWN, buff=0.1)
        self.play(Create(detector2), Write(det2_label))

        # Description
        desc3 = Text(
            "Radiation absorption depends on material thickness;\n"
            "detector measures transmitted intensity → thickness",
            font_size=14, color=WHITE
        )
        desc3.move_to(np.array([0.0, -2.3, 0]))
        self.play(Write(desc3))
        self.wait(0.5)

        # ==================================================================
        # Summary
        # ==================================================================
        summary_items = [
            "Medical imaging: tracer + gamma camera",
            "Radiotherapy: targeted radiation dose",
            "Industrial: thickness gauge, quality control",
        ]
        summary_group = VGroup()
        for i, item in enumerate(summary_items):
            t = Text(item, font_size=18, color=WHITE)
            t.move_to(np.array([0.0, 1.0 - i * 0.5, 0]))
            summary_group.add(t)

        self.play(
            FadeOut(app3_title), FadeOut(source), FadeOut(source_label),
            FadeOut(sheet), FadeOut(sheet_label), FadeOut(radiation_lines),
            FadeOut(detector2), FadeOut(det2_label), FadeOut(desc3),
        )
        self.play(*[Write(item) for item in summary_group], run_time=1.5)
        self.wait(2.0)