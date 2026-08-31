"""Scene — Crowd control: agents evacuating through a single exit.

Animate an agent-based crowd evacuation in a rectangular hall with a single
exit in the middle of one wall.  Agents (dots) stream toward the door,
slowing as they crowd, and pile up at the bottleneck.  A live panel tracks
the exited count (with a progress bar) and the mean-speed trace over time.

Physics driver
--------------
ReferenceCrowdModel from physics_core.inquiry.complex_systems provides the
agent-based evacuation engine.

Animation pattern
-----------------
All frames are precomputed at scene start.  A t[0] driver advances an
integer frame index, and always_redraw mobjects rebuild from that index
every frame.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    Dot,
    GREY,
    LEFT,
    Line,
    Mobject,
    Rectangle,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    VMobject,
    WHITE,
    YELLOW,
    always_redraw,
)

from physics_core.inquiry.complex_systems import ReferenceCrowdModel

COLOR_HALL = "#2A2A2A"
COLOR_DOOR = "#2E7D32"
COLOR_AGENT = "#1E90FF"
COLOR_TRACE = "#FFD700"


class CrowdControl(Scene):
    """Agent-based crowd evacuation with a live exited + speed trace."""

    def construct(self) -> None:
        n_agents: int = 50
        hall_width: float = 10.0
        hall_height: float = 6.0
        exit_size: float = 1.0
        base_speed: float = 0.9
        panic: float = 0.6
        max_steps: int = 600
        scale: float = 0.6
        origin = np.array([-5.5, -0.7, 0.0])

        # ------------------------------------------------------------------
        # Precompute ALL simulation frames
        # ------------------------------------------------------------------
        model = ReferenceCrowdModel(
            n_agents=n_agents,
            hall_width=hall_width,
            hall_height=hall_height,
            exit_size=exit_size,
            base_speed=base_speed,
            panic=panic,
            seed=42,
        )

        position_frames: list[np.ndarray] = [model.positions.copy()]
        exited_frames: list[np.ndarray] = [model.exited.copy()]
        metric_frames: list[tuple[float, int, int]] = [model.crowd_metrics()]
        for _ in range(max_steps):
            model.step()
            position_frames.append(model.positions.copy())
            exited_frames.append(model.exited.copy())
            metric_frames.append(model.crowd_metrics())
            if metric_frames[-1][1] == n_agents:  # everyone evacuated
                break

        n_frames: int = len(position_frames)
        total_time_scene: float = float(min(n_frames * 0.16, 32.0))

        # ------------------------------------------------------------------
        # Authoritative time / frame index
        # ------------------------------------------------------------------
        t: list[float] = [0.0]

        def frame_idx() -> int:
            frac = t[0] / total_time_scene
            idx = int(round(frac * (n_frames - 1)))
            return max(0, min(idx, n_frames - 1))

        def to_m(p: np.ndarray) -> np.ndarray:
            return np.array(
                [
                    origin[0] + p[0] * scale,
                    origin[1] + p[1] * scale,
                    0.0,
                ]
            )

        # ------------------------------------------------------------------
        # Title
        # ------------------------------------------------------------------
        title = Text("Crowd Control — Single-Exit Evacuation", font_size=28, color=YELLOW)
        title.to_edge(UP, buff=0.22)
        self.add(title)

        # ------------------------------------------------------------------
        # Hall + exit
        # ------------------------------------------------------------------
        hall = Rectangle(
            width=hall_width * scale,
            height=hall_height * scale,
            fill_color=COLOR_HALL,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=2,
        )
        hall.move_to(
            np.array(
                [
                    origin[0] + hall_width * scale / 2,
                    origin[1] + hall_height * scale / 2,
                    0.0,
                ]
            )
        )
        self.add(hall)

        # Exit opening (right wall, centred)
        exit_top = to_m(
            np.array([hall_width, hall_height / 2 + exit_size / 2])
        )
        exit_bottom = to_m(
            np.array([hall_width, hall_height / 2 - exit_size / 2])
        )
        exit_marker = Rectangle(
            width=0.08,
            height=abs(exit_top[1] - exit_bottom[1]),
            fill_color=COLOR_DOOR,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1,
        )
        exit_marker.move_to((exit_top + exit_bottom) / 2)
        self.add(exit_marker)

        exit_label = Text("EXIT", font_size=12, color=COLOR_DOOR)
        exit_label.move_to(exit_marker.get_center() + RIGHT * 0.5 + UP * 0.3)
        self.add(exit_label)

        # ------------------------------------------------------------------
        # Agents (pre-created dots, repositioned per frame)
        # ------------------------------------------------------------------
        agents: VGroup = VGroup()
        for _ in range(n_agents):
            dot = Dot(radius=0.09, color=COLOR_AGENT)
            agents.add(dot)

        def update_agents() -> VGroup:
            fidx = frame_idx()
            positions = position_frames[fidx]
            exited = exited_frames[fidx]
            for i, dot in enumerate(agents):
                dot.move_to(to_m(positions[i]))
                if exited[i]:
                    dot.set_opacity(0.0)
                else:
                    dot.set_opacity(1.0)
            return agents

        agents_mob = always_redraw(update_agents)
        self.add(agents_mob)

        # ------------------------------------------------------------------
        # Right panel: exited counter + progress bar
        # ------------------------------------------------------------------
        panel_x = 1.6
        exited_text = always_redraw(
            lambda: Text(
                f"Exited: {metric_frames[frame_idx()][1]} / {n_agents}",
                font_size=20,
                color=WHITE,
            ).move_to(np.array([panel_x + 2.2, 2.8, 0.0]))
        )
        self.add(exited_text)

        progress_bg = Rectangle(
            width=3.6, height=0.28,
            fill_color=GREY, fill_opacity=0.4,
            stroke_color=WHITE, stroke_width=1,
        )
        progress_bg.move_to(np.array([panel_x + 2.2, 2.4, 0.0]))
        self.add(progress_bg)

        def update_progress() -> Rectangle:
            frac = metric_frames[frame_idx()][1] / n_agents
            fill = Rectangle(
                width=3.6 * max(frac, 0.02),
                height=0.28,
                fill_color=COLOR_DOOR,
                fill_opacity=1.0,
                stroke_width=0,
            )
            fill.move_to(
                np.array([panel_x + 2.2 - (3.6 * (1.0 - frac)) / 2, 2.4, 0.0])
            )
            return fill

        progress_mob = always_redraw(update_progress)
        self.add(progress_mob)

        # ------------------------------------------------------------------
        # Right panel: mean-speed trace
        # ------------------------------------------------------------------
        plot_origin = np.array([panel_x, -0.6, 0.0])
        plot_w: float = 6.2
        plot_h: float = 2.2
        speed_max: float = base_speed * (1.0 + panic) * 1.15

        x_axis = Line(
            plot_origin,
            plot_origin + RIGHT * plot_w,
            color=WHITE,
            stroke_width=1,
        )
        y_axis = Line(
            plot_origin,
            plot_origin + UP * plot_h,
            color=WHITE,
            stroke_width=1,
        )
        self.add(x_axis, y_axis)

        speed_label = Text("mean speed", font_size=12, color=WHITE)
        speed_label.move_to(plot_origin + UP * plot_h + LEFT * 0.05)
        self.add(speed_label)

        def update_trace() -> VMobject:
            fidx = frame_idx()
            pts: list[np.ndarray] = []
            for k in range(fidx + 1):
                ms = metric_frames[k][0]
                x = plot_origin[0] + (k / max(n_frames - 1, 1)) * plot_w
                y = plot_origin[1] + (ms / speed_max) * plot_h
                pts.append(np.array([x, y, 0.0]))
            vm = VMobject(color=COLOR_TRACE, stroke_width=2)
            if len(pts) > 1:
                vm.set_points_as_corners(pts)
            return vm

        trace_mob = always_redraw(update_trace)
        self.add(trace_mob)

        step_text = always_redraw(
            lambda: Text(
                f"Step: {frame_idx()}",
                font_size=14,
                color=WHITE,
            ).move_to(np.array([panel_x + 2.2, -1.3, 0.0]))
        )
        self.add(step_text)

        # ------------------------------------------------------------------
        # Driver
        # ------------------------------------------------------------------
        def driver_updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(driver_updater)
        self.add(driver)

        self.wait(total_time_scene)
