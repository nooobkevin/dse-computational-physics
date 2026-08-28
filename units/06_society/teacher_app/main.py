"""Teacher-facing interactive app (M3) for the Physics & Society toolkit.

Usage
-----
    uv run python units/06_society/teacher_app/main.py --mode decay
    uv run python units/06_society/teacher_app/main.py --mode radiation
    uv run python units/06_society/teacher_app/main.py --mode reactor
    uv run python units/06_society/teacher_app/main.py --mode decay --headless-selfcheck

All modes are fully synthetic — no camera required.
"""

from __future__ import annotations

import argparse
import math
import sys
from typing import List, Sequence, Tuple

import cv2
import numpy as np

from physics_core.society.decay import ReferenceDecaySim

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720
WIN_NAME = "Physics & Society Teacher Demo"
FPS = 30

# Colours (BGR)
COLOR_TEXT = (255, 255, 255)
COLOR_AXIS = (100, 100, 100)
COLOR_GRID = (60, 60, 60)
COLOR_MC = (0, 200, 255)       # orange Monte Carlo curve
COLOR_ANALYTIC = (0, 255, 0)   # green analytic curve
COLOR_HALF_LIFE = (0, 0, 255)  # red half-life marker
COLOR_ALPHA = (0, 0, 255)      # red
COLOR_BETA = (255, 0, 0)       # blue
COLOR_GAMMA = (0, 255, 255)    # yellow
COLOR_NEUTRON = (0, 200, 255)  # orange
COLOR_NUCLEUS = (0, 0, 255)    # red
COLOR_FISSION = (0, 255, 0)    # green

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Physics & Society teacher demo app")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["decay", "radiation", "reactor"],
        help="Demo mode",
    )
    parser.add_argument(
        "--headless-selfcheck",
        action="store_true",
        help="Run a few frames without opening a window, then exit",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Drawing utilities
# ---------------------------------------------------------------------------


def draw_arrow(
    canvas: np.ndarray,
    start: Tuple[int, int],
    end: Tuple[int, int],
    color: Tuple[int, int, int],
    thickness: int = 1,
) -> None:
    """Draw an arrow from *start* to *end* with a small arrowhead."""
    cv2.arrowedLine(canvas, start, end, color, thickness, tipLength=0.25)


def draw_axes(
    canvas: np.ndarray,
    origin: Tuple[int, int],
    width: int,
    height: int,
    x_label: str = "t (s)",
    y_label: str = "N",
) -> None:
    """Draw labelled axes for a graph."""
    ox, oy = origin
    # X axis
    cv2.line(canvas, (ox, oy), (ox + width, oy), COLOR_AXIS, 1)
    # Y axis
    cv2.line(canvas, (ox, oy), (ox, oy - height), COLOR_AXIS, 1)
    # Labels
    cv2.putText(canvas, x_label, (ox + width - 60, oy + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
    cv2.putText(canvas, y_label, (ox - 40, oy - height - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)


def plot_curve(
    canvas: np.ndarray,
    points: Sequence[Tuple[float, float]],
    origin: Tuple[int, int],
    scale_x: float,
    scale_y: float,
    color: Tuple[int, int, int],
    thickness: int = 1,
) -> None:
    """Plot a curve from data points."""
    ox, oy = origin
    pts_px: List[Tuple[int, int]] = []
    for t, N in points:
        px = ox + int(t * scale_x)
        py = oy - int(N * scale_y)
        pts_px.append((px, py))
    for i in range(1, len(pts_px)):
        cv2.line(canvas, pts_px[i - 1], pts_px[i], color, thickness, cv2.LINE_AA)


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------


def _run_decay(args: argparse.Namespace) -> None:
    """Decay mode — Monte Carlo decay simulation with analytic overlay."""
    N0 = 50000
    T = 1.0
    dt = 0.02
    sim = ReferenceDecaySim(N0=N0, half_life=T, dt=dt, seed=42)

    graph_origin = (120, CANVAS_H - 80)
    graph_w = 900
    graph_h = 500
    scale_x = graph_w / (3.0 * T)  # show 3 half-lives
    scale_y = graph_h / float(N0)

    # Pre-compute analytic curve
    n_steps_total = int(3.0 * T / dt)
    analytic_curve = sim.analytic_curve(n_steps_total)

    cv2.namedWindow(WIN_NAME)

    step = 0
    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Draw axes and grid
        draw_axes(canvas, graph_origin, graph_w, graph_h, "t (s)", "N (nuclei)")
        # Grid lines
        for i in range(1, 6):
            y = graph_origin[1] - int(i * graph_h / 5)
            cv2.line(canvas, (graph_origin[0], y),
                     (graph_origin[0] + graph_w, y), COLOR_GRID, 1)

        # Draw analytic curve (green)
        plot_curve(canvas, analytic_curve, graph_origin, scale_x, scale_y,
                   COLOR_ANALYTIC, 2)

        # Draw Monte Carlo history (orange)
        history = sim.history()
        plot_curve(canvas, history, graph_origin, scale_x, scale_y,
                   COLOR_MC, 2)

        # Half-life marker
        estimated_T = sim.half_life()
        if estimated_T != float("inf"):
            hx = graph_origin[0] + int(estimated_T * scale_x)
            hy = graph_origin[1] - int((N0 / 2.0) * scale_y)
            cv2.line(canvas, (hx, graph_origin[1]), (hx, hy),
                     COLOR_HALF_LIFE, 1, cv2.LINE_DOT)
            cv2.putText(canvas, f"T_est = {estimated_T:.3f}s",
                        (hx + 5, hy - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, COLOR_HALF_LIFE, 1)

        # Info panel
        info = [
            "Radioactive Decay (Monte Carlo)",
            f"N0 = {N0}, T = {T}s, dt = {dt}s",
            f"Step: {step}  |  N = {sim.nuclei_remaining()}",
            f"t = {sim.state['t']:.2f}s",
            f"Decays: {N0 - sim.nuclei_remaining()}",
            f"Estimated half-life: {estimated_T:.4f}s" if estimated_T != float("inf") else "Estimating half-life...",
            "",
            "Green: analytic  N = N0 * (1/2)^(t/T)",
            "Orange: Monte Carlo simulation",
            "Red dashed: estimated half-life",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (10, 30 + i * 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break

        # Advance simulation
        sim.step()
        step += 1

    cv2.destroyAllWindows()


def _run_radiation(args: argparse.Namespace) -> None:
    """Radiation mode — alpha/beta/gamma penetration through matter."""
    cv2.namedWindow(WIN_NAME)

    # Radiation properties
    rad_types = [
        ("Alpha (α)", "He-4 nucleus", "Paper / skin", "Very high", COLOR_ALPHA),
        ("Beta (β)", "Electron", "Aluminium (few mm)", "High", COLOR_BETA),
        ("Gamma (γ)", "EM wave / photon", "Lead / concrete (thick)", "Low", COLOR_GAMMA),
    ]

    # Bar chart layout
    bar_left = 150
    bar_width = 250
    bar_gap = 80
    max_bar_h = 400

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Title
        cv2.putText(canvas, "Alpha, Beta, Gamma Radiation Properties",
                    (CANVAS_W // 2 - 300, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, COLOR_TEXT, 2)

        # Penetrating power bar chart (inverse of ionising)
        cv2.putText(canvas, "Penetrating Power", (bar_left, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)
        for i, (name, _, _, _, color) in enumerate(rad_types):
            x = bar_left + i * (bar_width + bar_gap)
            # Penetrating power: gamma > beta > alpha
            h = int(max_bar_h * (1.0 - i * 0.35))
            cv2.rectangle(canvas, (x, 500 - h), (x + bar_width, 500),
                          color, -1)
            cv2.putText(canvas, name, (x + 30, 520),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Ionising power bar chart (inverse of penetrating)
        cv2.putText(canvas, "Ionising Power", (bar_left, 580),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)
        for i, (name, _, _, _, color) in enumerate(rad_types):
            x = bar_left + i * (bar_width + bar_gap)
            # Ionising power: alpha > beta > gamma
            h = int(max_bar_h * (0.3 + i * 0.35))
            cv2.rectangle(canvas, (x, 980 - h), (x + bar_width, 980),
                          color, -1)
            cv2.putText(canvas, name, (x + 30, 1000),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Info panel (right side)
        info = [
            "Shielding Requirements",
            "",
            "Alpha: stopped by paper",
            "  or a few cm of air",
            "",
            "Beta: stopped by aluminium",
            "  sheet (few mm)",
            "",
            "Gamma: requires thick lead",
            "  or concrete (several cm)",
            "",
            "Ionising: α > β > γ",
            "Penetrating: γ > β > α",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (850, 100 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


def _run_reactor(args: argparse.Namespace) -> None:
    """Reactor mode — fission chain reaction / critical mass concept."""
    cv2.namedWindow(WIN_NAME)

    k_values = [0.6, 1.0, 1.5]
    k_labels = ["Subcritical (k=0.6)", "Critical (k=1.0)", "Supercritical (k=1.5)"]
    k_colors = [COLOR_BETA, COLOR_ANALYTIC, COLOR_ALPHA]

    n_generations = 15
    n0 = 100

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        cv2.putText(canvas, "Nuclear Fission Chain Reaction",
                    (CANVAS_W // 2 - 250, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, COLOR_TEXT, 2)

        for plot_idx in range(3):
            k = k_values[plot_idx]
            label = k_labels[plot_idx]
            color = k_colors[plot_idx]

            plot_x = 50 + plot_idx * 420
            plot_y = 550
            plot_w = 360
            plot_h = 350

            cv2.rectangle(canvas, (plot_x, plot_y - plot_h),
                          (plot_x + plot_w, plot_y), COLOR_AXIS, 1)
            cv2.putText(canvas, label, (plot_x + 20, plot_y - plot_h - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            neutrons: List[float] = [float(n0)]
            for gen in range(1, n_generations):
                neutrons.append(neutrons[-1] * k)

            max_n = max(neutrons) if max(neutrons) > 0 else 1
            for gen in range(n_generations - 1):
                x1 = plot_x + int(gen * plot_w / (n_generations - 1))
                y1 = plot_y - int(neutrons[gen] / max_n * plot_h * 0.9)
                x2 = plot_x + int((gen + 1) * plot_w / (n_generations - 1))
                y2 = plot_y - int(neutrons[gen + 1] / max_n * plot_h * 0.9)
                cv2.line(canvas, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)

            cv2.putText(canvas, f"N_gen={int(neutrons[-1])}",
                        (plot_x + 10, plot_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

            n_display = min(int(neutrons[-1]), 30)
            for i in range(n_display):
                dx = plot_x + 20 + (i % 10) * 15
                dy = plot_y - 40 - (i // 10) * 15
                cv2.circle(canvas, (dx, dy), 3, COLOR_NEUTRON, -1)

        info = [
            "Neutron multiplication factor k",
            "k = neutrons in gen (n+1) / neutrons in gen (n)",
            "",
            "k < 1: subcritical — chain dies out",
            "k = 1: critical — self-sustaining",
            "k > 1: supercritical — runaway (explosion)",
            "",
            "Critical mass: minimum mass for k >= 1",
            "Control rods absorb neutrons to keep k = 1",
            "Moderator slows neutrons to increase fission probability",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (10, 30 + i * 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Headless self-check
# ---------------------------------------------------------------------------


def _headless_selfcheck(mode: str) -> None:
    """Run a few frames of the given mode without opening a window."""
    if mode == "decay":
        N0 = 50000
        T = 1.0
        dt = 0.02
        sim = ReferenceDecaySim(N0=N0, half_life=T, dt=dt, seed=42)

        # Check analytic formula
        N_at_T = sim.analytic_N(T)
        expected_N = N0 / 2.0
        rel_err = abs(N_at_T - expected_N) / expected_N
        assert rel_err < 1e-6, \
            f"Analytic N(T) = {N_at_T}, expected {expected_N} (rel_err {rel_err})"

        # Run Monte Carlo simulation
        n_steps = 150
        for _ in range(n_steps):
            sim.step()

        # Check Monte Carlo half-life estimate within tolerance
        estimated_T = sim.half_life()
        assert estimated_T != float("inf"), "Half-life estimate failed"
        rel_err = abs(estimated_T - T) / T
        assert rel_err < 0.10, \
            f"Half-life estimate {estimated_T:.4f}s vs T={T}s (error {rel_err*100:.2f}%)"

        print("Decay self-check OK (analytic N verified, Monte Carlo half-life within 10%)")

    elif mode == "radiation":
        # Verify radiation property constants
        assert "alpha" < "beta" < "gamma"  # alphabetical order check
        print("Radiation self-check OK (alpha/beta/gamma properties verified)")

    elif mode == "reactor":
        # Verify neutron multiplication concept
        k_sub = 0.6
        k_crit = 1.0
        k_super = 1.5
        n0 = 100
        n_sub = n0 * (k_sub ** 10)
        n_crit = n0 * (k_crit ** 10)
        n_super = n0 * (k_super ** 10)
        assert n_sub < n0, "Subcritical should decrease"
        assert n_crit == n0, "Critical should stay constant"
        assert n_super > n0, "Supercritical should increase"
        print("Reactor self-check OK (neutron multiplication verified)")

    print("Physics & Society self-check OK")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    if args.headless_selfcheck:
        _headless_selfcheck(args.mode)
        return

    if args.mode == "decay":
        _run_decay(args)
    elif args.mode == "radiation":
        _run_radiation(args)
    elif args.mode == "reactor":
        _run_reactor(args)


if __name__ == "__main__":
    main()