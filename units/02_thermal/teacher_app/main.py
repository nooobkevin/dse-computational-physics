"""Teacher-facing interactive app (M3) for the thermal physics toolkit.

Usage
-----
    uv run python units/02_thermal/teacher_app/main.py --mode gas
    uv run python units/02_thermal/teacher_app/main.py --mode gas --headless-selfcheck
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np

from physics_core.errors import sig_figs
from physics_core.thermal.equations import maxwell_boltzmann, rms_speed as mb_rms_speed
from physics_core.thermal.gas_sim import ReferenceGasSim

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720
WIN_NAME = "Physics Teacher Demo - Thermal"
FPS = 30
DT = 0.02  # ~50 fps step
MAX_DATA_POINTS = 900

# Colours (BGR)
COLOR_BOX = (100, 100, 100)
COLOR_PARTICLE = (0, 255, 0)  # green
COLOR_VECTOR = (255, 150, 0)  # orange
COLOR_TEXT = (255, 255, 255)
COLOR_HIST = (0, 200, 255)  # yellow-orange
COLOR_MB_CURVE = (0, 255, 255)  # yellow
COLOR_AXIS = (100, 100, 100)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Thermal physics teacher demo app")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["gas"],
        help="Demo mode",
    )
    parser.add_argument(
        "--N",
        type=int,
        default=200,
        help="Number of gas particles (default: 200)",
    )
    parser.add_argument(
        "--T",
        type=float,
        default=2.0,
        help="Initial temperature (default: 2.0)",
    )
    parser.add_argument(
        "--headless-selfcheck",
        action="store_true",
        help="Run a few frames without opening a window, then exit",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Graph drawing utility (mirrors Unit 01)
# ---------------------------------------------------------------------------


def draw_graph(
    canvas: np.ndarray,
    region: Tuple[int, int, int, int],
    points: List[Tuple[float, float]],
    color: Tuple[int, int, int],
    x_label: str = "",
    y_label: str = "",
    title: str = "",
    x_range: Optional[Tuple[float, float]] = None,
    y_range: Optional[Tuple[float, float]] = None,
) -> None:
    """Draw a 2D graph into a rectangular region of the canvas."""
    rx, ry, rw, rh = region
    cv2.rectangle(canvas, (rx, ry), (rx + rw, ry + rh), COLOR_AXIS, 1)

    if not points:
        return

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    if x_range is not None:
        x_min, x_max = x_range
    else:
        x_min, x_max = min(xs), max(xs)
        if abs(x_max - x_min) < 1e-12:
            x_min -= 0.5
            x_max += 0.5

    if y_range is not None:
        y_min, y_max = y_range
    else:
        y_min, y_max = min(ys), max(ys)
        if abs(y_max - y_min) < 1e-12:
            y_min -= 0.5
            y_max += 0.5

    x_pad = max((x_max - x_min) * 0.08, 0.01)
    y_pad = max((y_max - y_min) * 0.08, 0.01)
    x_min -= x_pad
    x_max += x_pad
    y_min -= y_pad
    y_max += y_pad

    margin = 35
    gx = rx + margin
    gy = ry + margin
    gw = rw - 2 * margin
    gh = rh - 2 * margin

    def to_px(wx: float, wy: float) -> Tuple[int, int]:
        px = int(gx + (wx - x_min) / (x_max - x_min) * gw)
        py = int(gy + (y_max - wy) / (y_max - y_min) * gh)
        return (px, py)

    if y_min <= 0 <= y_max:
        _, ay = to_px(0, 0)
        cv2.line(canvas, (gx, ay), (gx + gw, ay), COLOR_AXIS, 1)
    if x_min <= 0 <= x_max:
        ax, _ = to_px(0, 0)
        cv2.line(canvas, (ax, gy), (ax, gy + gh), COLOR_AXIS, 1)

    pts = np.array([to_px(x, y) for x, y in points], dtype=np.int32)
    if len(pts) >= 2:
        cv2.polylines(canvas, [pts], False, color, 1, cv2.LINE_AA)

    if title:
        cv2.putText(canvas, title, (rx + 5, ry + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
    if x_label:
        cv2.putText(canvas, x_label, (rx + rw - 100, ry + rh - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1)
    if y_label:
        cv2.putText(canvas, y_label, (rx + 4, ry + margin - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1)


# ---------------------------------------------------------------------------
# Gas scene drawing
# ---------------------------------------------------------------------------


def draw_gas_scene(
    canvas: np.ndarray,
    sim: ReferenceGasSim,
    box_origin: Tuple[int, int],
    box_size_px: float,
) -> None:
    """Draw the gas box with particles and velocity arrows."""
    ox, oy = box_origin
    scale = box_size_px / sim.L

    # Draw box
    cv2.rectangle(canvas, (ox, oy), (int(ox + box_size_px), int(oy + box_size_px)), COLOR_BOX, 2)

    # Draw particles
    positions = sim._positions
    velocities = sim._velocities

    for i in range(sim.N):
        px = int(ox + positions[i, 0] * scale)
        py = int(oy + positions[i, 1] * scale)

        # Particle dot
        cv2.circle(canvas, (px, py), 3, COLOR_PARTICLE, -1)

        # Velocity arrow (scaled for visibility)
        vx = int(velocities[i, 0] * scale * 0.3)
        vy = int(velocities[i, 1] * scale * 0.3)
        if abs(vx) > 1 or abs(vy) > 1:
            cv2.arrowedLine(canvas, (px, py), (px + vx, py + vy), COLOR_VECTOR, 1, tipLength=0.3)


# ---------------------------------------------------------------------------
# Speed distribution histogram with MB overlay
# ---------------------------------------------------------------------------


def draw_speed_distribution(
    canvas: np.ndarray,
    region: Tuple[int, int, int, int],
    sim: ReferenceGasSim,
    bins: int = 30,
) -> None:
    """Draw the measured speed distribution with theoretical MB curve overlay."""
    rx, ry, rw, rh = region
    counts, bin_edges = sim.speed_distribution(bins=bins)

    if len(counts) == 0:
        return

    # Normalise counts to probability density
    bin_widths = bin_edges[1:] - bin_edges[:-1]
    total = float(np.sum(counts * bin_widths))
    if total > 0:
        densities = counts.astype(np.float64) / total
    else:
        densities = counts.astype(np.float64)

    # Bin centres
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    # Theoretical MB curve
    v_max = float(np.max(bin_edges)) * 1.2
    mb_pts: List[Tuple[float, float]] = []
    n_steps = 200
    for i in range(n_steps):
        v = v_max * i / n_steps
        f = maxwell_boltzmann(v, sim.T, sim.m, kB=sim.kB, dim=sim.dim)
        mb_pts.append((v, f))

    # Determine y range from both histogram and MB curve
    max_density = max(float(np.max(densities)), max((p[1] for p in mb_pts), default=0.0))
    y_max = max_density * 1.2 if max_density > 0 else 1.0

    # Draw histogram bars
    margin = 35
    gx = rx + margin
    gy = ry + margin
    gw = rw - 2 * margin
    gh = rh - 2 * margin

    def to_px(wx: float, wy: float) -> Tuple[int, int]:
        px = int(gx + wx / v_max * gw)
        py = int(gy + (y_max - wy) / y_max * gh)
        return (px, py)

    # Axes
    cv2.rectangle(canvas, (rx, ry), (rx + rw, ry + rh), COLOR_AXIS, 1)

    # Bars
    for i in range(len(bin_centres)):
        x = bin_centres[i]
        d = densities[i]
        px = to_px(x, 0)[0]
        bar_w = max(int(bin_widths[i] / v_max * gw), 2)
        bar_h = int(d / y_max * gh)
        cv2.rectangle(canvas, (px - bar_w // 2, gy + gh - bar_h), (px + bar_w // 2, gy + gh), COLOR_HIST, -1)

    # MB curve
    mb_pixels = [to_px(v, f) for v, f in mb_pts]
    mb_arr = np.array(mb_pixels, dtype=np.int32)
    if len(mb_arr) >= 2:
        cv2.polylines(canvas, [mb_arr], False, COLOR_MB_CURVE, 2, cv2.LINE_AA)

    # Labels
    cv2.putText(canvas, "Speed distribution", (rx + 5, ry + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
    cv2.putText(canvas, "Speed", (rx + rw - 60, ry + rh - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1)
    cv2.putText(canvas, "f(v)", (rx + 4, ry + margin - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1)
    cv2.putText(canvas, "Measured", (rx + 5, ry + rh - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_HIST, 1)
    cv2.putText(canvas, "MB theory", (rx + 5, ry + rh - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_MB_CURVE, 1)


# ---------------------------------------------------------------------------
# Gas mode runner
# ---------------------------------------------------------------------------


def _run_gas(args: argparse.Namespace) -> None:
    """Gas mode — fully synthetic molecular dynamics demo."""
    N = args.N
    T_init = args.T
    L = 15.0
    dt = DT

    sim = ReferenceGasSim(N=N, L=L, T=T_init, m=1.0, dt=dt, dim=2, particle_radius=0.05)

    # Layout
    box_origin = (30, 30)
    box_size_px = 500.0
    hist_region = (560, 30, 690, 340)
    info_x = 560
    info_y_start = 400

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Step simulation
        sim.step()

        # Draw gas box
        draw_gas_scene(canvas, sim, box_origin, box_size_px)

        # Draw speed distribution
        draw_speed_distribution(canvas, hist_region, sim, bins=25)

        # Info panel
        p = sim.pressure()
        p_ideal = sim.ideal_gas_pressure()
        v_avg = sim.average_speed
        v_rms_val = sim.rms_speed
        T_est = sim.temperature_from_ke()
        ke = sim.energy()["kinetic"]

        info_lines = [
            f"N = {N}",
            f"T_input = {T_init:.2f}",
            f"T_est = {sig_figs(T_est, 3):.3f}",
            f"KE = {sig_figs(ke, 4):.4f}",
            f"P_meas = {sig_figs(p, 4):.4f}",
            f"P_ideal = {sig_figs(p_ideal, 4):.4f}",
            f"v_avg = {sig_figs(v_avg, 3):.3f}",
            f"v_rms = {sig_figs(v_rms_val, 3):.3f}",
            f"t = {sig_figs(sim._t, 4):.4f} s",
        ]
        for i, line in enumerate(info_lines):
            cv2.putText(
                canvas,
                line,
                (info_x, info_y_start + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                COLOR_TEXT,
                1,
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
    """Run a few frames of the given mode without opening a window.

    This is used for CI / no-display testing.
    """
    if mode == "gas":
        sim = ReferenceGasSim(N=100, L=15.0, T=2.0, dt=0.02, dim=2, particle_radius=0.05, seed=42)
        for _ in range(500):
            sim.step()
        p = sim.pressure()
        assert p > 0.0, f"Pressure should be positive, got {p}"
        counts, bin_edges = sim.speed_distribution(bins=10)
        assert len(counts) > 0, "Speed distribution should be non-empty"
        assert len(bin_edges) > 0, "Speed distribution bin edges should be non-empty"
        T_est = sim.temperature_from_ke()
        rel_err = abs(T_est - 2.0) / 2.0
        assert rel_err < 0.15, (
            f"Estimated T={T_est:.4f} too far from input T=2.0 "
            f"(error {rel_err*100:.2f}%)"
        )
        print(f"Thermal self-check OK ({sim.N} particles)")
    else:
        print(f"No self-check for mode '{mode}'")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    if args.headless_selfcheck:
        _headless_selfcheck(args.mode)
        return

    if args.mode == "gas":
        _run_gas(args)


if __name__ == "__main__":
    main()