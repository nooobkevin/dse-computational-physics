"""Scene — Epidemic spread: S/I/R cellular automaton visualisation.

Animate the spread of a simulated epidemic on a 2-D grid using the
cellular-automaton SIR model from physics_core.  Susceptible cells are
grey, infected are red, recovered are green.  A bar chart shows the
running S/I/R counts over time.

Physics driver
--------------
ReferenceEpidemicModel from physics_core.inquiry.complex_systems provides
the CA simulation engine.

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
    GRAY,
    GREEN,
    LEFT,
    Mobject,
    RED,
    Rectangle,
    RIGHT,
    Scene,
    Square,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
    always_redraw,
)

from physics_core.inquiry.complex_systems import ReferenceEpidemicModel

# Cell colours
COLOR_SUSCEPTIBLE = GRAY
COLOR_INFECTED = RED
COLOR_RECOVERED = GREEN


class EpidemicSpread(Scene):
    """Epidemic SIR spread on a grid with a running bar chart."""

    def construct(self) -> None:
        # ------------------------------------------------------------------
        # Simulation parameters
        # ------------------------------------------------------------------
        rows: int = 25
        cols: int = 40
        p_infect: float = 0.35
        p_recover: float = 0.08
        total_steps: int = 120
        cell_size: float = 0.12

        # ------------------------------------------------------------------
        # Precompute ALL simulation frames
        # ------------------------------------------------------------------
        model = ReferenceEpidemicModel(rows, cols, p_infect, p_recover, seed=42)
        history = model.run(total_steps)  # list of (S, I, R) tuples

        # Also store the full grid at each step
        grids: list[np.ndarray] = [model.grid]  # t=0 grid is the initial
        for _ in range(total_steps):
            model.step()
            grids.append(model.grid.copy())
        # grids[i] is the grid state AFTER step i (grids[0] = initial)

        # We'll use grids indexed by step, but model.run already consumed steps.
        # Re-run from scratch for the grid snapshots.
        model2 = ReferenceEpidemicModel(rows, cols, p_infect, p_recover, seed=42)
        all_grids: list[np.ndarray] = [model2.grid.copy()]
        for _ in range(total_steps):
            model2.step()
            all_grids.append(model2.grid.copy())

        n_frames: int = len(all_grids)  # total_steps + 1
        total_time_scene: float = 16.0

        # ------------------------------------------------------------------
        # Authoritative time / frame index
        # ------------------------------------------------------------------
        t: list[float] = [0.0]

        def frame_idx() -> int:
            """Map scene time [0, total_time) to a frame index [0, n_frames)."""
            frac = t[0] / total_time_scene
            idx = int(round(frac * (n_frames - 1)))
            return max(0, min(idx, n_frames - 1))

        # ------------------------------------------------------------------
        # Layout — title + step counter share the y=3.45 band (different
        # columns); grid frame spans y[-1.2, 2.8]; legend below the frame;
        # chart bars grow from baseline y=-1.0 (max top y=1.5).
        # ------------------------------------------------------------------
        title = Text(
            "Epidemic Spread — SIR Model", font_size=28, color=YELLOW
        )
        title.move_to(UP * 3.45)
        self.add(title)

        grid_top_y: float = 2.8
        grid_origin = np.array([-5.5, grid_top_y, 0.0])

        # S/I/R bar chart (right side): bars grow upward from a fixed
        # baseline at chart_origin.y - 1.25 = -1.0, max top y = 1.5.
        chart_origin = np.array([3.0, 0.25, 0.0])
        bar_w: float = 0.6
        max_count: int = rows * cols

        # ------------------------------------------------------------------
        # Precompute cell-square mobjects (static geometry, colour per frame)
        # ------------------------------------------------------------------
        cell_colors: list[list[str]] = []  # [frame][cell_idx] = color hex
        for frame_grid in all_grids:
            frame_colors: list[str] = []
            for r in range(rows):
                for c in range(cols):
                    val = int(frame_grid[r, c])
                    if val == 0:
                        col = "#666666"  # grey
                    elif val == 1:
                        col = "#FF0000"  # red
                    else:
                        col = "#009900"  # green
                    frame_colors.append(col)
            cell_colors.append(frame_colors)

        # Build cell squares (static positions)
        cell_squares: VGroup = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(
                    side_length=cell_size,
                    fill_opacity=0.9,
                    stroke_width=0,
                )
                sq.move_to(
                    grid_origin
                    + RIGHT * c * cell_size * 1.1
                    + DOWN * r * cell_size * 1.1
                )
                cell_squares.add(sq)

        # Grid background — sized and centred on the cell group's bounding
        # box so the frame fully encloses the grid on all four edges.
        grid_bg = Rectangle(
            width=cell_squares.width + cell_size,
            height=cell_squares.height + cell_size,
            color=WHITE,
            stroke_width=1,
            fill_opacity=0.0,
        ).move_to(cell_squares.get_center())

        # Step counter: same band as the title (y=3.45) but a different
        # column (title ends near x=2.2, counter starts at x=3.0)
        step_text = always_redraw(
            lambda: Text(
                f"Step: {frame_idx()}",
                font_size=16, color=WHITE,
            ).move_to(np.array([3.0, 3.45, 0.0]), aligned_edge=LEFT)
        )

        # Legend: bottom-left, below the grid frame (frame bottom y = -1.2),
        # clear of title, grid frame and chart
        legend = VGroup(
            Text("Susceptible", font_size=12, color=GRAY),
            Text("Infected", font_size=12, color=RED),
            Text("Recovered", font_size=12, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        legend.move_to(np.array([-6.9, -1.7, 0.0]), aligned_edge=UP + LEFT)

        # ------------------------------------------------------------------
        # always_redraw grid cells
        # ------------------------------------------------------------------
        def update_cells() -> VGroup:
            fidx = frame_idx()
            colors = cell_colors[fidx]
            for sq, col in zip(cell_squares, colors):
                sq.set_fill(col, opacity=0.9)
            return cell_squares

        cells_mob = always_redraw(update_cells)

        # ------------------------------------------------------------------
        # always_redraw bar chart
        # ------------------------------------------------------------------
        def update_chart() -> VGroup:
            fidx = frame_idx()
            s, i, r_counts = history[fidx]

            chart = VGroup()
            # Susceptible bar
            s_h = (s / max_count) * 2.5
            s_bar = Rectangle(
                width=bar_w, height=s_h,
                fill_color=COLOR_SUSCEPTIBLE, fill_opacity=0.8,
                stroke_width=1, stroke_color=WHITE,
            )
            s_bar.move_to(chart_origin + DOWN * (2.5 - s_h) / 2, aligned_edge=LEFT)
            chart.add(s_bar)

            # Infected bar
            i_h = (i / max_count) * 2.5
            i_bar = Rectangle(
                width=bar_w, height=i_h,
                fill_color=COLOR_INFECTED, fill_opacity=0.8,
                stroke_width=1, stroke_color=WHITE,
            )
            i_bar.move_to(
                chart_origin + RIGHT * (bar_w + 0.15) + DOWN * (2.5 - i_h) / 2,
                aligned_edge=LEFT,
            )
            chart.add(i_bar)

            # Recovered bar
            r_h = (r_counts / max_count) * 2.5
            r_bar = Rectangle(
                width=bar_w, height=r_h,
                fill_color=COLOR_RECOVERED, fill_opacity=0.8,
                stroke_width=1, stroke_color=WHITE,
            )
            r_bar.move_to(
                chart_origin + RIGHT * 2 * (bar_w + 0.15) + DOWN * (2.5 - r_h) / 2,
                aligned_edge=LEFT,
            )
            chart.add(r_bar)

            return chart

        chart_mob = always_redraw(update_chart)

        # ------------------------------------------------------------------
        # Labels for chart
        # ------------------------------------------------------------------
        bar_baseline_y = chart_origin[1] - 1.25
        s_label = Text("S", font_size=16, color=GRAY)
        s_label.next_to(
            np.array([chart_origin[0] + bar_w / 2, bar_baseline_y, 0.0]),
            DOWN, buff=0.1,
        )
        i_label = Text("I", font_size=16, color=RED)
        i_label.next_to(
            np.array(
                [chart_origin[0] + (bar_w + 0.15) + bar_w / 2, bar_baseline_y, 0.0]
            ),
            DOWN, buff=0.1,
        )
        r_label = Text("R", font_size=16, color=GREEN)
        r_label.next_to(
            np.array(
                [
                    chart_origin[0] + 2 * (bar_w + 0.15) + bar_w / 2,
                    bar_baseline_y,
                    0.0,
                ]
            ),
            DOWN, buff=0.1,
        )

        chart_title = Text("S/I/R Counts", font_size=16, color=WHITE)
        chart_title.next_to(
            np.array([chart_origin[0], bar_baseline_y, 0.0]), DOWN, buff=0.45
        ).align_to(chart_origin, LEFT)

        # ------------------------------------------------------------------
        # Driver
        # ------------------------------------------------------------------
        def driver_updater(_mob: Mobject, dt: float) -> None:
            t[0] = self.time

        driver = Mobject()
        driver.add_updater(driver_updater)

        # ------------------------------------------------------------------
        # Assemble and run
        # ------------------------------------------------------------------
        self.add(title)
        self.add(grid_bg)
        self.add(cells_mob)
        self.add(chart_mob)
        self.add(s_label, i_label, r_label)
        self.add(chart_title)
        self.add(step_text)
        self.add(legend)
        self.add(driver)

        self.wait(total_time_scene)


