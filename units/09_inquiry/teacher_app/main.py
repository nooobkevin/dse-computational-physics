"""Teacher-facing interactive app for Unit 09: Scientific Inquiry.

Usage
-----
    uv run python units/09_inquiry/teacher_app/main.py --mode analysis
    uv run python units/09_inquiry/teacher_app/main.py --mode experiment
    uv run python units/09_inquiry/teacher_app/main.py --mode analysis --headless-selfcheck
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

from typing import List, Optional, Tuple

import cv2
import numpy as np

from physics_core.errors import sig_figs
from physics_core.inquiry.analysis import (
    ReferenceLinearFit,
    percent_error,
    propagate_uncertainty,
)

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

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scientific inquiry teacher demo app")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["analysis", "experiment"],
        help="Demo mode",
    )
    parser.add_argument(
        "--headless-selfcheck",
        action="store_true",
        help="Run a headless self-check without opening a window",
    )
    return parser.parse_args()


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
) -> None:
    """Draw a scatter plot with optional best-fit line and error bars."""
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
    """Generate synthetic pendulum period² vs length data.

    The period of a simple pendulum is T = 2π √(L/g), so T² = (4π²/g) * L.
    This generates (L, T²) data with a bit of noise added to T².

    Returns
    -------
    tuple
        ``(lengths, t_squared)`` — both 1-D numpy arrays.
    """
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
    """Generate synthetic free-fall distance vs t² data.

    For free fall from rest: s = ½ g t², so s vs t² is a straight line
    through the origin with slope ½ g.

    Returns
    -------
    tuple
        ``(t_squared, distance)`` — both 1-D numpy arrays.
    """
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


if __name__ == "__main__":
    main()