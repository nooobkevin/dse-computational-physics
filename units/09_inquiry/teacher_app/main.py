"""Teacher-facing interactive app for Unit 09: Scientific Inquiry.

Usage
-----
    uv run python units/09_inquiry/teacher_app/main.py --mode analysis
    uv run python units/09_inquiry/teacher_app/main.py --mode experiment
    uv run python units/09_inquiry/teacher_app/main.py --mode epidemic
    uv run python units/09_inquiry/teacher_app/main.py --mode design
    uv run python units/09_inquiry/teacher_app/main.py --mode epidemic --headless-selfcheck
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

# Ensure this directory is on sys.path so sibling modules can be imported
# when the script is run directly (e.g. ``uv run python main.py``).
_THIS_DIR = str(Path(__file__).resolve().parent)
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from typing import Callable, List, Optional, Tuple

import cv2
import numpy as np

from physics_core.errors import sig_figs
from physics_core.inquiry.analysis import (
    ReferenceLinearFit,
    percent_error,
    propagate_uncertainty,
)
from physics_core.inquiry.complex_systems import ReferenceEpidemicModel

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720
WIN_NAME = "Scientific Inquiry — Teacher Demo"
FPS = 30

# Colours (BGR)
COLOR_DATA = (0, 255, 0)       # green
COLOR_FIT = (0, 255, 255)      # yellow
COLOR_AXIS = (100, 100, 100)
COLOR_TEXT = (255, 255, 255)
COLOR_ERROR_BARS = (0, 165, 255)  # orange
COLOR_ACCEPTED = (255, 100, 100)  # light red
COLOR_BG = (30, 30, 30)
COLOR_SUSCEPTIBLE = (128, 128, 128)  # grey
COLOR_INFECTED = (0, 0, 200)          # red (BGR)
COLOR_RECOVERED = (0, 180, 0)         # green (BGR)
COLOR_DESIGN_FIT = (255, 0, 255)      # magenta

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scientific inquiry teacher demo app")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["analysis", "experiment", "epidemic", "design"],
        help="Demo mode",
    )
    parser.add_argument(
        "--headless-selfcheck",
        action="store_true",
        help="Run a headless self-check without opening a window",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def _make_slider(
    canvas: np.ndarray,
    x: int, y: int, w: int,
    label: str,
    value: float,
    vmin: float, vmax: float,
) -> None:
    """Draw a horizontal slider with current value."""
    cv2.putText(
        canvas, f"{label}: {value:.2f}", (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1,
    )
    cv2.rectangle(canvas, (x, y), (x + w, y + 6), COLOR_AXIS, 1)
    frac = (value - vmin) / (vmax - vmin)
    knob_x = int(x + frac * w)
    cv2.rectangle(canvas, (knob_x - 3, y - 2), (knob_x + 3, y + 8), COLOR_FIT, -1)


# ---------------------------------------------------------------------------
# Graph drawing utility
# ---------------------------------------------------------------------------


def draw_scatter(
    canvas: np.ndarray,
    region: Tuple[int, int, int, int],
    x_data: np.ndarray,
    y_data: np.ndarray,
    color: Tuple[int, int, int],
    x_label: str = "",
    y_label: str = "",
    title: str = "",
    fit_line: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    fit_color: Tuple[int, int, int] = COLOR_FIT,
    error_bars: Optional[np.ndarray] = None,
    marker_lines: Optional[List[Tuple[float, float, Tuple[int, int, int], str]]] = None,
) -> None:
    """Draw a scatter plot with optional best-fit line, error bars, and markers."""
    rx, ry, rw, rh = region
    cv2.rectangle(canvas, (rx, ry), (rx + rw, ry + rh), COLOR_AXIS, 1)

    if len(x_data) == 0:
        return

    x_min, x_max = float(x_data.min()), float(x_data.max())
    y_min, y_max = float(y_data.min()), float(y_data.max())

    # Padding
    x_pad = max((x_max - x_min) * 0.12, 0.1)
    y_pad = max((y_max - y_min) * 0.12, 0.1)
    if x_pad < 1e-12:
        x_pad = 0.5
    if y_pad < 1e-12:
        y_pad = 0.5
    x_min -= x_pad
    x_max += x_pad
    y_min -= y_pad
    y_max += y_pad

    margin = 50
    gx = rx + margin
    gy = ry + margin
    gw = rw - 2 * margin
    gh = rh - 2 * margin

    def to_px(wx: float, wy: float) -> Tuple[int, int]:
        px = int(gx + (wx - x_min) / (x_max - x_min) * gw)
        py = int(gy + (y_max - wy) / (y_max - y_min) * gh)
        return (px, py)

    # Axes at origin if visible
    if y_min <= 0 <= y_max:
        _, ay = to_px(0, 0)
        cv2.line(canvas, (gx, ay), (gx + gw, ay), COLOR_AXIS, 1)
    if x_min <= 0 <= x_max:
        ax, _ = to_px(0, 0)
        cv2.line(canvas, (ax, gy), (ax, gy + gh), COLOR_AXIS, 1)

    # Error bars (vertical)
    if error_bars is not None:
        for i in range(len(x_data)):
            px, py = to_px(x_data[i], y_data[i])
            y_err_px = int(error_bars[i] / (y_max - y_min) * gh)
            cv2.line(
                canvas,
                (px, py - y_err_px),
                (px, py + y_err_px),
                COLOR_ERROR_BARS,
                1,
            )
            cv2.line(
                canvas,
                (px - 3, py - y_err_px),
                (px + 3, py - y_err_px),
                COLOR_ERROR_BARS,
                1,
            )
            cv2.line(
                canvas,
                (px - 3, py + y_err_px),
                (px + 3, py + y_err_px),
                COLOR_ERROR_BARS,
                1,
            )

    # Best-fit line
    if fit_line is not None:
        x_fit, y_fit = fit_line
        pts = np.array(
            [to_px(x_fit[i], y_fit[i]) for i in range(len(x_fit))],
            dtype=np.int32,
        )
        if len(pts) >= 2:
            cv2.polylines(canvas, [pts], False, fit_color, 2, cv2.LINE_AA)

    # Marker lines (vertical dashed)
    if marker_lines is not None:
        for mx, my_min, mcolor, mlabel in marker_lines:
            if mx is not None:
                mx_px, _ = to_px(mx, 0)
                cv2.line(
                    canvas,
                    (mx_px, gy),
                    (mx_px, gy + gh),
                    mcolor,
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    canvas, mlabel, (mx_px + 3, gy + 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, mcolor, 1,
                )

    # Data points
    for i in range(len(x_data)):
        px, py = to_px(x_data[i], y_data[i])
        cv2.circle(canvas, (px, py), 5, color, -1)
        cv2.circle(canvas, (px, py), 5, (255, 255, 255), 1)

    # Labels
    if title:
        cv2.putText(
            canvas, title, (rx + 5, ry + 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLOR_TEXT, 1,
        )
    if x_label:
        cv2.putText(
            canvas, x_label, (rx + rw - 120, ry + rh - 8),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_TEXT, 1,
        )
    if y_label:
        cv2.putText(
            canvas, y_label, (rx + 6, ry + margin - 6),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_TEXT, 1,
        )


# ---------------------------------------------------------------------------
# Synthetic experiment generators
# ---------------------------------------------------------------------------


def generate_pendulum_data(
    n_points: int = 10,
    length: float = 1.0,
    g_true: float = 9.81,
    noise_std: float = 0.02,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic pendulum period² vs length data."""
    rng = np.random.default_rng(seed)
    lengths = np.linspace(0.2, 1.5, n_points)
    t_sq_true = (4.0 * math.pi**2 / g_true) * lengths
    t_sq_measured = t_sq_true + rng.normal(0, noise_std, size=n_points)
    return (lengths, t_sq_measured)


def generate_freefall_data(
    n_points: int = 10,
    g_true: float = 9.81,
    noise_std: float = 0.05,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic free-fall distance vs t² data."""
    rng = np.random.default_rng(seed)
    times = np.linspace(0.1, 1.0, n_points)
    t_sq = times**2
    s_true = 0.5 * g_true * t_sq
    s_measured = s_true + rng.normal(0, noise_std, size=n_points)
    return (t_sq, s_measured)


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------


def _run_analysis(args: argparse.Namespace) -> None:
    """Analysis mode — synthetic experiment + linear fit + constant estimation."""
    cv2.namedWindow(WIN_NAME)

    # Generate synthetic pendulum data
    lengths, t_sq = generate_pendulum_data(n_points=10, noise_std=0.03)

    # Fit T² vs L: slope = 4π²/g, so g_est = 4π² / slope
    fit = ReferenceLinearFit(x_data=lengths, y_data=t_sq)
    slope = fit.slope()
    intercept = fit.intercept()
    r_sq = fit.correlation_squared()
    g_est = 4.0 * math.pi**2 / slope
    g_err = percent_error(g_est, 9.81)

    # Uncertainty propagation
    slope_err, intercept_err = propagate_uncertainty(
        slope, intercept, lengths, t_sq
    )
    # Propagate to g: g = 4π² / slope → dg = (4π² / slope²) * d_slope
    g_uncertainty = (4.0 * math.pi**2 / slope**2) * slope_err

    # Fit line for drawing
    x_fit, y_fit = fit.position()

    # Info text
    info_lines = [
        "Pendulum Experiment: T² vs L",
        f"Slope = {sig_figs(slope, 4):.4f} s²/m",
        f"Intercept = {sig_figs(intercept, 4):.4f} s²",
        f"R² = {sig_figs(r_sq, 4):.4f}",
        "",
        f"Estimated g = {sig_figs(g_est, 4):.4f} m/s²",
        f"g uncertainty = ± {sig_figs(g_uncertainty, 2):.2f} m/s²",
        f"Percent error vs 9.81 = {sig_figs(g_err, 3):.2f}%",
        "",
        "T² = (4π²/g) × L   →   slope = 4π²/g",
        "g = 4π² / slope",
    ]

    while True:
        canvas = np.full((CANVAS_H, CANVAS_W, 3), COLOR_BG, dtype=np.uint8)

        # Scatter plot + best-fit line (left side)
        draw_scatter(
            canvas,
            (20, 20, 800, 680),
            lengths,
            t_sq,
            COLOR_DATA,
            x_label="Length L (m)",
            y_label="Period² T² (s²)",
            title="Pendulum Data: T² vs L",
            fit_line=(x_fit, y_fit),
        )

        # Info panel (right side)
        for i, line in enumerate(info_lines):
            y_pos = 40 + i * 28
            cv2.putText(
                canvas,
                line,
                (850, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                COLOR_TEXT,
                1,
            )

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break

    cv2.destroyAllWindows()


def _run_experiment(args: argparse.Namespace) -> None:
    """Experiment mode — uncertainty & error-propagation workflow."""
    cv2.namedWindow(WIN_NAME)

    # Generate free-fall data
    t_sq, distances = generate_freefall_data(n_points=8, noise_std=0.08)

    # Fit s vs t²: slope = ½ g, so g_est = 2 * slope
    fit = ReferenceLinearFit(x_data=t_sq, y_data=distances)
    slope = fit.slope()
    intercept = fit.intercept()
    r_sq = fit.correlation_squared()
    g_est = 2.0 * slope
    g_err = percent_error(g_est, 9.81)

    # Uncertainty propagation
    slope_err, intercept_err = propagate_uncertainty(
        slope, intercept, t_sq, distances
    )
    g_uncertainty = 2.0 * slope_err

    # Error bars (simulated: proportional to y value)
    error_bars = 0.05 + 0.03 * distances

    x_fit, y_fit = fit.position()

    info_lines = [
        "Free-Fall Experiment: s vs t²",
        f"Slope = {sig_figs(slope, 4):.4f} m/s²",
        f"Intercept = {sig_figs(intercept, 4):.4f} m",
        f"R² = {sig_figs(r_sq, 4):.4f}",
        "",
        f"Estimated g = {sig_figs(g_est, 4):.4f} m/s²",
        f"g uncertainty = ± {sig_figs(g_uncertainty, 2):.2f} m/s²",
        f"Percent error vs 9.81 = {sig_figs(g_err, 3):.2f}%",
        "",
        "s = ½ g t²   →   slope = ½ g",
        "g = 2 × slope",
        "",
        "Error bars show ±1σ uncertainty",
        "Propagation: σ_g = 2 × σ_slope",
    ]

    while True:
        canvas = np.full((CANVAS_H, CANVAS_W, 3), COLOR_BG, dtype=np.uint8)

        draw_scatter(
            canvas,
            (20, 20, 800, 680),
            t_sq,
            distances,
            COLOR_DATA,
            x_label="Time² t² (s²)",
            y_label="Distance s (m)",
            title="Free-Fall Data: s vs t²",
            fit_line=(x_fit, y_fit),
            error_bars=error_bars,
        )

        for i, line in enumerate(info_lines):
            y_pos = 40 + i * 26
            cv2.putText(
                canvas,
                line,
                (850, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                COLOR_TEXT,
                1,
            )

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


def _run_epidemic(args: argparse.Namespace) -> None:
    """Epidemic mode — cellular-automaton SIR spread with step/play."""
    cv2.namedWindow(WIN_NAME)

    rows: int = 40
    cols: int = 60
    p_infect: float = 0.35
    p_recover: float = 0.08
    total_steps: int = 150

    model = ReferenceEpidemicModel(rows, cols, p_infect, p_recover, seed=42)

    # Precompute all frames
    all_grids: List[np.ndarray] = [model.grid.copy()]
    for _ in range(total_steps):
        model.step()
        all_grids.append(model.grid.copy())

    sir_history: List[Tuple[int, int, int]] = [(int(np.sum(g == 0)), int(np.sum(g == 1)), int(np.sum(g == 2))) for g in all_grids]

    step: int = 0
    playing: bool = False
    cell_w: int = 8
    cell_h: int = 8
    grid_offset_x: int = 20
    grid_offset_y: int = 50

    while True:
        canvas = np.full((CANVAS_H, CANVAS_W, 3), COLOR_BG, dtype=np.uint8)

        # Draw grid
        grid = all_grids[step]
        for r in range(rows):
            for c in range(cols):
                val = grid[r, c]
                if val == 0:
                    color = COLOR_SUSCEPTIBLE
                elif val == 1:
                    color = COLOR_INFECTED
                else:
                    color = COLOR_RECOVERED
                x = grid_offset_x + c * cell_w
                y = grid_offset_y + r * cell_h
                cv2.rectangle(
                    canvas,
                    (x, y), (x + cell_w - 1, y + cell_h - 1),
                    color, -1,
                )

        # S/I/R counts
        s, i, r_cnt = sir_history[step]
        total = rows * cols

        # Bar chart
        bar_x = grid_offset_x + cols * cell_w + 30
        bar_y = 60
        bar_h = 200
        bar_w = 30
        gap = 10

        for idx, (cnt, col, label) in enumerate(
            [(s, COLOR_SUSCEPTIBLE, "S"), (i, COLOR_INFECTED, "I"), (r_cnt, COLOR_RECOVERED, "R")]
        ):
            bx = bar_x + idx * (bar_w + gap)
            bh = int((cnt / total) * bar_h)
            cv2.rectangle(canvas, (bx, bar_y + bar_h - bh), (bx + bar_w, bar_y + bar_h), col, -1)
            cv2.putText(
                canvas, f"{label}: {cnt}", (bx - 5, bar_y + bar_h + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1,
            )

        # Info
        cv2.putText(
            canvas, f"Step: {step}/{total_steps}", (bar_x, bar_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1,
        )
        cv2.putText(
            canvas, f"p_infect = {p_infect:.2f}", (bar_x, bar_y - 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1,
        )
        cv2.putText(
            canvas, f"p_recover = {p_recover:.2f}", (bar_x, bar_y - 50),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1,
        )

        controls = [
            "[SPACE] Play/Pause",
            "[RIGHT] Step forward",
            "[ESC] Exit",
        ]
        for ci, ctrl in enumerate(controls):
            cv2.putText(
                canvas, ctrl, (bar_x, 400 + ci * 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_AXIS, 1,
            )

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF

        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            playing = not playing
        elif key == 83 or key == 115:  # RIGHT arrow or 's'
            if step < total_steps:
                step += 1

        if playing and step < total_steps:
            step += 1

    cv2.destroyAllWindows()


def _run_design(args: argparse.Namespace) -> None:
    """Engineering design mode — pendulum clock: find L for target T."""
    cv2.namedWindow(WIN_NAME)
    cv2.createTrackbar("L (m)", WIN_NAME, 50, 200, lambda x: None)  # 0.50 - 2.00

    g_true: float = 9.81
    target_T: float = 2.0  # seconds
    rng = np.random.default_rng(seed=42)

    while True:
        canvas = np.full((CANVAS_H, CANVAS_W, 3), COLOR_BG, dtype=np.uint8)

        track_val = cv2.getTrackbarPos("L (m)", WIN_NAME)
        L_guess: float = 0.5 + track_val * (1.5 / 200)  # 0.50 to 2.00

        # Simulated "measurements": vary L around guess, measure T
        n_measure: int = 6
        L_vals = np.linspace(max(L_guess - 0.3, 0.2), L_guess + 0.3, n_measure)
        # True period: T = 2π√(L/g)
        T_true = 2.0 * math.pi * np.sqrt(L_vals / g_true)
        # Add small deterministic noise (seeded)
        T_measured = T_true + rng.normal(0, 0.02, size=n_measure)

        # Linearise: T² vs L
        T2_data = T_measured**2
        fit = ReferenceLinearFit(x_data=L_vals, y_data=T2_data)
        slope = fit.slope()
        r_sq = fit.correlation_squared()
        g_est = 4.0 * math.pi**2 / slope

        # Recommended L for target T
        L_recommended = (target_T**2) / (4.0 * math.pi**2) * g_est

        # L for target T using true g
        L_optimal = (target_T**2) * g_true / (4.0 * math.pi**2)

        x_fit, y_fit = fit.position()

        # Draw scatter + fit (left)
        draw_scatter(
            canvas,
            (20, 20, 700, 500),
            L_vals,
            T2_data,
            COLOR_DATA,
            x_label="Length L (m)",
            y_label="Period² T² (s²)",
            title=f"Design: Pendulum Clock (target T = {target_T:.1f} s)",
            fit_line=(x_fit, y_fit),
            fit_color=COLOR_DESIGN_FIT,
            marker_lines=[
                (L_recommended, 0, COLOR_ACCEPTED, "L*"),
                (L_optimal, 0, (200, 200, 200), "L_opt"),
            ],
        )

        # Info panel (right)
        info = [
            "Engineering Design: Pendulum Clock",
            "",
            f"Target period: T = {target_T:.1f} s",
            f"Current L guess: {L_guess:.3f} m",
            f"Recommended L: {L_recommended:.3f} m",
            f"Optimal L (true g): {L_optimal:.3f} m",
            "",
            f"Measured T at current L:",
        ]
        # Show measured period at closest L
        closest_i = np.argmin(np.abs(L_vals - L_guess))
        info.append(f"  T = {T_measured[closest_i]:.4f} s")
        info.append(f"  T² = {T2_data[closest_i]:.4f} s²")
        info.append("")
        info.append(f"Fit: slope = {slope:.4f} s²/m")
        info.append(f"R² = {r_sq:.4f}")
        info.append(f"Estimated g = {g_est:.3f} m/s²")
        info.append(f"L* for T={target_T:.1f}s = {L_recommended:.3f} m")

        for i, line in enumerate(info):
            cv2.putText(
                canvas, line, (750, 40 + i * 24),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_TEXT, 1,
            )

        # Guide: iteration steps
        guide = [
            "Design Loop:",
            "1. Guess L",
            "2. Measure T (simulated)",
            "3. Fit T² vs L → g_est",
            "4. Compute L* for target T",
            "5. Adjust L toward L*",
            "",
            "Use slider: adjust L guess",
        ]
        for i, line in enumerate(guide):
            cv2.putText(
                canvas, line, (750, 460 + i * 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_AXIS, 1,
            )

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Headless self-check
# ---------------------------------------------------------------------------


def _headless_selfcheck(mode: str) -> None:
    """Run a headless self-check without opening a window.

    Used for CI / no-display testing.
    """
    if mode == "analysis":
        # Generate pendulum data with known g=9.81
        lengths, t_sq = generate_pendulum_data(
            n_points=10, g_true=9.81, noise_std=0.03, seed=42
        )
        fit = ReferenceLinearFit(x_data=lengths, y_data=t_sq)
        slope = fit.slope()
        g_est = 4.0 * math.pi**2 / slope
        g_err = percent_error(g_est, 9.81)

        # Slope should be positive and close to 4π²/9.81 ≈ 4.025
        expected_slope = 4.0 * math.pi**2 / 9.81
        assert abs(slope - expected_slope) / expected_slope < 0.05, (
            f"Slope {slope:.4f} deviates too much from expected {expected_slope:.4f}"
        )
        assert g_err < 5.0, (
            f"Percent error {g_err:.2f}% exceeds 5% threshold"
        )
        print(f"Analysis self-check OK: g_est={g_est:.3f} m/s², error={g_err:.2f}%")

    elif mode == "experiment":
        t_sq, distances = generate_freefall_data(
            n_points=8, g_true=9.81, noise_std=0.08, seed=42
        )
        fit = ReferenceLinearFit(x_data=t_sq, y_data=distances)
        slope = fit.slope()
        g_est = 2.0 * slope
        g_err = percent_error(g_est, 9.81)

        expected_slope = 0.5 * 9.81
        assert abs(slope - expected_slope) / expected_slope < 0.08, (
            f"Slope {slope:.4f} deviates too much from expected {expected_slope:.4f}"
        )
        assert g_err < 8.0, (
            f"Percent error {g_err:.2f}% exceeds 8% threshold"
        )
        print(f"Experiment self-check OK: g_est={g_est:.3f} m/s², error={g_err:.2f}%")

    elif mode == "epidemic":
        model = ReferenceEpidemicModel(50, 50, 0.35, 0.08, seed=42)
        history = model.run(200)
        # Infection should spread (peak I > 1)
        max_i = max(h[1] for h in history)
        assert max_i > 1, (
            f"Epidemic self-check FAILED: infection did not spread (max I={max_i})"
        )
        # Infection eventually saturates (R monotonically increases)
        r_counts = [h[2] for h in history]
        for i in range(1, len(r_counts)):
            assert r_counts[i] >= r_counts[i - 1], (
                f"Epidemic self-check FAILED: R decreased at step {i}"
            )
        print(f"Epidemic self-check OK: max_I={max_i}, final_R={r_counts[-1]}")

    elif mode == "design":
        g_true = 9.81
        target_T = 2.0
        rng = np.random.default_rng(seed=99)
        L_guess = 1.2
        L_vals = np.linspace(L_guess - 0.3, L_guess + 0.3, 6)
        T_true = 2.0 * math.pi * np.sqrt(L_vals / g_true)
        T_measured = T_true + rng.normal(0, 0.02, size=6)
        T2_data = T_measured**2
        fit = ReferenceLinearFit(x_data=L_vals, y_data=T2_data)
        slope = fit.slope()
        g_est = 4.0 * math.pi**2 / slope

        # Fit should recover g within ~5%
        g_err = percent_error(g_est, g_true)
        assert g_err < 5.0, (
            f"Design self-check FAILED: g error {g_err:.2f}% > 5%"
        )

        # Recommended L should give period close to target
        L_recommended = (target_T**2) / (4.0 * math.pi**2) * g_est
        T_predicted = 2.0 * math.pi * math.sqrt(L_recommended / g_true)
        T_err = abs(T_predicted - target_T) / target_T * 100.0
        assert T_err < 3.0, (
            f"Design self-check FAILED: T error {T_err:.2f}% > 3%"
        )
        print(
            f"Design self-check OK: g_est={g_est:.3f} m/s² "
            f"({g_err:.2f}%), L_recommended={L_recommended:.3f} m"
        )

    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    if args.headless_selfcheck:
        _headless_selfcheck(args.mode)
        return

    if args.mode == "analysis":
        _run_analysis(args)
    elif args.mode == "experiment":
        _run_experiment(args)
    elif args.mode == "epidemic":
        _run_epidemic(args)
    elif args.mode == "design":
        _run_design(args)


if __name__ == "__main__":
    main()