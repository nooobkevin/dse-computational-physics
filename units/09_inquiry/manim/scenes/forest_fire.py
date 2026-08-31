"""Scene — Forest fire: wind-biased cellular-automaton spread.

Animate the spread of a forest fire on a 2-D grid using the cellular
automaton from physics_core.  Trees are green, burning cells are orange,
burned (consumed) cells are brown, empty cells are dark.  A wind arrow shows
the prevailing direction and a bar chart tracks the live tree / burning /
burned counts.

Physics driver
--------------
ReferenceForestFire from physics_core.inquiry.complex_systems provides the
CA simulation engine.

Animation pattern
-----------------
All frames are precomputed at scene start.  A t[0] driver advances an
integer frame index, and always_redraw mobjects rebuild from that index
every frame.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    DOWN,
    LEFT,
    Mobject,
    ORIGIN,
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

from physics_core.inquiry.complex_systems import (
    BURNED,
    BURNING,
    EMPTY,
    ReferenceForestFire,
    TREE,
)

# Cell colours
COLOR_TREE = "#2E8B57"
COLOR_EMPTY = "#404040"
COLOR_BURNING = "#FF4500"
COLOR_BURNED = "#4A2F1B"


class ForestFire(Scene):
    """Forest-fire spread on a grid with wind bias and a live counts bar."""

    def construct(self) -> None:
        rows: int = 26
        cols: int = 42
        p_ignite: float = 0.35
        wind_direction: int = 0  # east
        wind_bias: float = 0.4
        burn_duration: int = 2
        tree_density: float = 0.9
        cell_size: float = 0.07
        max_steps: int = 400

        # ------------------------------------------------------------------
        # Precompute ALL simulation frames
        # ------------------------------------------------------------------
        model = ReferenceForestFire(
            rows,
            cols,
            p_ignite=p_ignite,
            wind_direction=wind_direction,
            wind_bias=wind_bias,
            burn_duration=burn_duration,
            tree_density=tree_density,
            seed=42,
        )

        grids: list[np.ndarray] = [model.grid.copy()]
        history: list[tuple[int, int, int]] = [model.fire_counts()]
        for _ in range(max_steps):
            model.step()
            grids.append(model.grid.copy())
            history.append(model.fire_counts())
            if model.fire_counts()[1] == 0:  # fire fully burned out
                break

        n_frames: int = len(grids)
        total_time_scene: float = float(min(n_frames * 0.16, 26.0))

        # ------------------------------------------------------------------
        # Authoritative time / frame index
        # ------------------------------------------------------------------
        t: list[float] = [0.0]

        def frame_idx() -> int:
            frac = t[0] / total_time_scene
            idx = int(round(frac * (n_frames - 1)))
            return max(0, min(idx, n_frames - 1))

        # ------------------------------------------------------------------
        # Layout
        # ------------------------------------------------------------------
        title = Text("Forest Fire — Wind-Biased Spread", font_size=28, color=YELLOW)
        title.to_edge(UP, buff=0.25)
        self.add(title)

        grid_origin = np.array([-6.4, 1.0, 0.0])
        grid_bg = Rectangle(
            width=cols * cell_size * 1.1 + cell_size,
            height=rows * cell_size * 1.1 + cell_size,
            color=WHITE,
            stroke_width=1,
            fill_opacity=0.0,
        )
        grid_bg.move_to(
            grid_origin
            + RIGHT * cols * cell_size * 1.1 / 2
            - DOWN * rows * cell_size * 1.1 / 2
        )
        self.add(grid_bg)

        # Precompute cell colours per frame.
        cell_colors: list[list[str]] = []
        for frame_grid in grids:
            frame_colors: list[str] = []
            for r in range(rows):
                for c in range(cols):
                    val = int(frame_grid[r, c])
                    if val == TREE:
                        frame_colors.append(COLOR_TREE)
                    elif val == EMPTY:
                        frame_colors.append(COLOR_EMPTY)
                    elif val == BURNING:
                        frame_colors.append(COLOR_BURNING)
                    else:
                        frame_colors.append(COLOR_BURNED)
            cell_colors.append(frame_colors)

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

        def update_cells() -> VGroup:
            fidx = frame_idx()
            colors = cell_colors[fidx]
            for sq, col in zip(cell_squares, colors):
                sq.set_fill(col, opacity=0.9)
            return cell_squares

        cells_mob = always_redraw(update_cells)
        self.add(cells_mob)

        # ------------------------------------------------------------------
        # Wind arrow
        # ------------------------------------------------------------------
        wind_annot = self._wind_arrow(wind_direction)
        wind_annot.next_to(grid_bg, UP, buff=0.2).align_to(grid_bg, LEFT)
        wind_label = Text(
            "WIND", font_size=16, color=YELLOW
        )
        wind_label.next_to(wind_annot, RIGHT, buff=0.1).align_to(
            wind_annot, UP
        )
        self.add(wind_annot, wind_label)

        # ------------------------------------------------------------------
        # Live counts bar
        # ------------------------------------------------------------------
        chart_origin = np.array([2.2, 2.2, 0.0])
        bar_w: float = 0.7
        max_count: int = rows * cols

        def update_chart() -> VGroup:
            fidx = frame_idx()
            trees, burning, burned = history[fidx]
            chart = VGroup()
            for i, (cnt, colour) in enumerate(
                [(trees, COLOR_TREE), (burning, COLOR_BURNING), (burned, COLOR_BURNED)]
            ):
                h = (cnt / max_count) * 2.6
                bar = Rectangle(
                    width=bar_w,
                    height=h,
                    fill_color=colour,
                    fill_opacity=0.85,
                    stroke_width=1,
                    stroke_color=WHITE,
                )
                bar.move_to(
                    chart_origin
                    + RIGHT * i * (bar_w + 0.18)
                    + DOWN * (2.6 - h) / 2,
                    aligned_edge=LEFT,
                )
                chart.add(bar)
            return chart

        chart_mob = always_redraw(update_chart)
        self.add(chart_mob)

        # Labels for the chart
        for i, label in enumerate(["Trees", "Burning", "Burned"]):
            lbl = Text(
                label,
                font_size=14,
                color=[COLOR_TREE, COLOR_BURNING, COLOR_BURNED][i],
            )
            lbl.next_to(
                chart_origin + RIGHT * i * (bar_w + 0.18) + RIGHT * bar_w / 2,
                DOWN,
                buff=0.12,
            )
            self.add(lbl)

        chart_title = Text("Live Counts", font_size=16, color=WHITE)
        chart_title.next_to(chart_origin + UP * 2.6, DOWN, buff=0.1).align_to(
            chart_origin, LEFT
        )
        self.add(chart_title)

        step_text = always_redraw(
            lambda: Text(
                f"Step: {frame_idx()}",
                font_size=16,
                color=WHITE,
            )
            .next_to(chart_title, DOWN, buff=0.2)
            .align_to(chart_origin, LEFT)
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

    @staticmethod
    def _wind_arrow(direction: int):
        """Return an Arrow pointing in the given wind direction (0=E,1=S,2=W,3=N)."""
        vectors = {
            0: RIGHT,
            1: DOWN,
            2: LEFT,
            3: UP,
        }
        vec = vectors[direction]
        arrow = Arrow(
            start=ORIGIN,
            end=vec,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.25,
            color=YELLOW,
        )
        return arrow
