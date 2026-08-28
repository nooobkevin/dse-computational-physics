"""Teacher-facing interactive app (M3) for the thermal physics toolkit.

Usage
-----
    uv run python units/02_thermal/teacher_app/main.py --mode gas
    uv run python units/02_thermal/teacher_app/main.py --mode gas --headless-selfcheck
    uv run python units/02_thermal/teacher_app/main.py --mode gas_laws
    uv run python units/02_thermal/teacher_app/main.py --mode gas_laws --headless-selfcheck
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
        choices=["gas", "gas_laws"],
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
# Gas laws mode runner
# ---------------------------------------------------------------------------


def _run_gas_laws(args: argparse.Namespace) -> None:
    """Gas laws mode — Boyle's law (P-V) and absolute-zero extrapolation (P-T).

    Shows two live graphs:
    - Left: P vs V (Boyle's law) — isothermal compression/expansion
    - Right: P vs T (pressure law) — isochoric heating with absolute-zero
      extrapolation line
    """
    N = 100
    T_init = 2.0
    L = 15.0
    dt = 0.01

    sim = ReferenceGasSim(
        N=N, L=L, T=T_init, m=1.0, dt=dt, dim=2,
        particle_radius=0.05, seed=42,
    )

    # Pre-compute Boyle's law curve (P vs V at constant T)
    V_values = np.linspace(100.0, 350.0, 8).tolist()
    boyle_curve = sim.gas_law_isothermal_curve(
        V_values, equilibration_steps=300, sample_steps=100, seed=42
    )

    # Pre-compute pressure law curve (P vs T at constant V)
    T_sim_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    pt_curve = sim.gas_law_isochoric_curve(
        T_sim_values, equilibration_steps=300, sample_steps=100, seed=42
    )

    # Convert simulation T to Celsius for absolute-zero extrapolation
    # Map: simulation T=0 → -273.15°C, simulation T=2.0 → 0°C (arbitrary mapping)
    # We use: T_Celsius = (T_sim - 2.0) * 100.0  (so T_sim=2 → 0°C, T_sim=4 → 200°C)
    T_scale = 100.0
    T_offset = 2.0  # simulation T that maps to 0°C
    pt_celsius = [
        ((T_sim - T_offset) * T_scale, P) for T_sim, P in pt_curve
    ]

    # Linear fit to P-T data for absolute-zero extrapolation
    T_c_vals = np.array([tc for tc, _ in pt_celsius], dtype=np.float64)
    P_vals = np.array([P for _, P in pt_curve], dtype=np.float64)
    if len(T_c_vals) >= 2:
        coeffs = np.polyfit(T_c_vals, P_vals, 1)
        slope = coeffs[0]
        intercept = coeffs[1]
        # Absolute zero: P = 0 → T = -intercept / slope
        if abs(slope) > 1e-12:
            abs_zero_C = -intercept / slope
        else:
            abs_zero_C = -273.15
    else:
        slope = 0.0
        intercept = 0.0
        abs_zero_C = -273.15

    # Layout regions
    boyle_region = (50, 50, 550, 400)
    pt_region = (680, 50, 550, 400)
    info_x = 50
    info_y = 500

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Draw Boyle's law (P vs V)
        draw_graph(
            canvas, boyle_region, boyle_curve,
            color=(0, 200, 255),  # yellow-orange
            x_label="V", y_label="P",
            title="Boyle's law: P vs V (isothermal)",
        )

        # Draw pressure law (P vs T in Celsius)
        draw_graph(
            canvas, pt_region, pt_celsius,
            color=(0, 255, 255),  # yellow
            x_label="T (°C)", y_label="P",
            title="Pressure law: P vs T (isochoric)",
        )

        # Draw absolute-zero extrapolation line on P-T graph
        rx, ry, rw, rh = pt_region
        margin = 35
        gx = rx + margin
        gy = ry + margin
        gw = rw - 2 * margin
        gh = rh - 2 * margin

        # Determine visible T range
        all_tc = [tc for tc, _ in pt_celsius]
        t_min = min(all_tc) - 50.0
        t_max = max(all_tc) + 50.0
        # Extend to include absolute zero
        t_min = min(t_min, abs_zero_C - 50.0)

        all_p = [P for _, P in pt_curve]
        p_min = 0.0
        p_max = max(all_p) * 1.2 if max(all_p) > 0 else 1.0

        def to_px_celsius(tc: float, p: float) -> Tuple[int, int]:
            px = int(gx + (tc - t_min) / (t_max - t_min) * gw)
            py = int(gy + (p_max - p) / (p_max - p_min) * gh)
            return (px, py)

        # Draw extrapolation line (dashed)
        if abs(slope) > 1e-12:
            t_extrap_start = abs_zero_C
            t_extrap_end = t_max
            p_start = slope * t_extrap_start + intercept
            p_end = slope * t_extrap_end + intercept
            pt1 = to_px_celsius(t_extrap_start, p_start)
            pt2 = to_px_celsius(t_extrap_end, p_end)
            cv2.line(canvas, pt1, pt2, (100, 100, 255), 1, cv2.LINE_AA)  # red-ish dashed

        # Mark absolute zero
        abs_zero_px = to_px_celsius(abs_zero_C, 0.0)
        cv2.circle(canvas, abs_zero_px, 5, (0, 0, 255), -1)
        cv2.putText(
            canvas,
            f"Absolute zero: {abs_zero_C:.1f} °C",
            (abs_zero_px[0] - 80, abs_zero_px[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
        )

        # Info panel
        info_lines = [
            f"N = {N}",
            f"T = {T_init:.2f} (simulation units)",
            f"Boyle: P x V = constant",
            f"P-T slope = {slope:.4f}",
            f"Abs zero = {abs_zero_C:.1f} °C",
            f"Theoretical: -273.15 °C",
        ]
        for i, line in enumerate(info_lines):
            cv2.putText(
                canvas, line,
                (info_x, info_y + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1,
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
    elif mode == "gas_laws":
        sim = ReferenceGasSim(N=100, L=15.0, T=2.0, dt=0.01, dim=2, particle_radius=0.05, seed=42)
        # Test Boyle's law: P * V should be approximately constant
        V_values = [100.0, 200.0, 300.0]
        boyle = sim.gas_law_isothermal_curve(
            V_values, equilibration_steps=300, sample_steps=200, seed=42
        )
        pv_products = [P * V for V, P in boyle]
        mean_pv = float(np.mean(pv_products))
        for V, P in boyle:
            pv = P * V
            rel_err = abs(pv - mean_pv) / mean_pv
            assert rel_err < 0.35, (
                f"Boyle self-check: P*V={pv:.4f} at V={V:.1f}, mean={mean_pv:.4f}"
            )
        # Test pressure law: P / T should be approximately constant
        T_values = [1.0, 2.0, 3.0]
        pt = sim.gas_law_isochoric_curve(
            T_values, equilibration_steps=500, sample_steps=300, seed=42
        )
        pt_ratios = [P / T for T, P in pt]
        mean_ratio = float(np.mean(pt_ratios))
        for T, P in pt:
            ratio = P / T
            rel_err = abs(ratio - mean_ratio) / mean_ratio
            assert rel_err < 0.35, (
                f"Pressure law self-check: P/T={ratio:.4f} at T={T:.1f}, mean={mean_ratio:.4f}"
            )
        # Test absolute-zero extrapolation
        T_c_vals = np.array([(T_sim - 2.0) * 100.0 for T_sim, _ in pt], dtype=np.float64)
        P_vals = np.array([P for _, P in pt], dtype=np.float64)
        coeffs = np.polyfit(T_c_vals, P_vals, 1)
        slope = coeffs[0]
        intercept = coeffs[1]
        abs_zero_C = -intercept / slope
        assert abs(abs_zero_C - (-273.15)) / 273.15 < 0.5, (
            f"Absolute zero self-check: got {abs_zero_C:.1f} °C, expected -273.15 °C"
        )
        print(f"Gas laws self-check OK (abs zero = {abs_zero_C:.1f} °C)")
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
    elif args.mode == "gas_laws":
        _run_gas_laws(args)


if __name__ == "__main__":
    main()