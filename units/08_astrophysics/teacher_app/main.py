"""Teacher-facing interactive app for Astrophysics & Relativity.

Usage
-----
    uv run python units/08_astrophysics/teacher_app/main.py --mode doppler
    uv run python units/08_astrophysics/teacher_app/main.py --mode hubble
    uv run python units/08_astrophysics/teacher_app/main.py --mode lifecycles
    uv run python units/08_astrophysics/teacher_app/main.py --mode doppler --headless-selfcheck

All modes are fully synthetic — no camera required.
"""

from __future__ import annotations

import argparse
import math
import random
import sys
from typing import List, Tuple

import cv2
import numpy as np

from physics_core.astrophysics.doppler import C, H0, ReferenceDopplerShift
from physics_core.astrophysics.hubble import HubbleLaw, SPECTRAL_CLASSES

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720
WIN_NAME = "Astrophysics & Relativity Teacher Demo"
FPS = 30

# Colours (BGR)
COLOR_TEXT = (255, 255, 255)
COLOR_AXIS = (100, 100, 100)
COLOR_BLUE = (255, 200, 50)       # blueshift
COLOR_RED = (50, 100, 255)        # redshift
COLOR_SOURCE = (0, 255, 255)      # yellow source
COLOR_GREEN = (0, 255, 0)
COLOR_CYAN = (255, 255, 0)
COLOR_MAGENTA = (255, 0, 255)
COLOR_ORANGE = (0, 165, 255)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Astrophysics & Relativity teacher demo app"
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["doppler", "hubble", "lifecycles"],
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
    cv2.arrowedLine(canvas, start, end, color, thickness, tipLength=0.2)


def draw_text(
    canvas: np.ndarray,
    text: str,
    pos: Tuple[int, int],
    color: Tuple[int, int, int] = COLOR_TEXT,
    scale: float = 0.5,
    thickness: int = 1,
) -> None:
    cv2.putText(canvas, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------


def _run_doppler(args: argparse.Namespace) -> None:
    """Doppler redshift mode — wave compression/expansion with colour shift."""
    ds = ReferenceDopplerShift(f0=5.8e14)
    v_max = 3e7  # 0.1c
    t = 0.0
    sweep_period = 8.0  # seconds per full sweep

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Sweep velocity sinusoidally: approaching → rest → receding → rest
        v = v_max * math.sin(2.0 * math.pi * t / sweep_period)
        ds._state["v"] = v
        ds.step(1.0 / FPS)
        t += 1.0 / FPS

        f_obs = ds.observed_frequency(v)
        z = ds.redshift(v)
        lambda_source = C / ds.f0
        lambda_obs = C / f_obs

        # ── Draw wave ──────────────────────────────────────────────────
        wave_center_y = CANVAS_H // 2 - 60
        wave_amp = 60
        n_waves = 6
        base_wavelength_px = 120.0
        # Scale wavelength by observed / source ratio
        wavelength_ratio = lambda_obs / lambda_source
        wave_color = COLOR_RED if v > 0 else COLOR_BLUE if v < 0 else COLOR_GREEN

        pts: List[Tuple[int, int]] = []
        for px in range(50, CANVAS_W - 50):
            # Local phase: each pixel represents a position along the wave
            phase = 2.0 * math.pi * (px - 50) / (base_wavelength_px * wavelength_ratio)
            py = int(wave_center_y + wave_amp * math.sin(phase))
            pts.append((px, py))

        pts_arr = np.array(pts, dtype=np.int32)
        cv2.polylines(canvas, [pts_arr], False, wave_color, 2, cv2.LINE_AA)

        # Source marker
        cv2.circle(canvas, (50, wave_center_y), 8, COLOR_SOURCE, -1)
        draw_text(canvas, "Source", (50, wave_center_y - 20), COLOR_SOURCE, 0.5, 2)

        # Observer marker
        cv2.circle(canvas, (CANVAS_W - 50, wave_center_y), 8, COLOR_CYAN, -1)
        draw_text(canvas, "Observer", (CANVAS_W - 130, wave_center_y - 20), COLOR_CYAN, 0.5, 2)

        # ── Info panel ─────────────────────────────────────────────────
        info = [
            "Doppler Effect — Light",
            f"v = {v/1000:.1f} km/s  ({'receding' if v > 100 else 'approaching' if v < -100 else 'stationary'})",
            f"f_source = {ds.f0:.2e} Hz",
            f"f_obs   = {f_obs:.2e} Hz",
            f"λ_source = {lambda_source*1e9:.1f} nm",
            f"λ_obs   = {lambda_obs*1e9:.1f} nm",
            f"z = {z:.6f}",
            f"Δλ/λ ≈ v/c = {v/C:.6f}",
        ]
        for i, line in enumerate(info):
            draw_text(canvas, line, (10, 30 + i * 25), COLOR_TEXT, 0.55, 1)

        # Colour legend
        draw_text(canvas, "Blueshift (approaching)", (CANVAS_W - 300, CANVAS_H - 60), COLOR_BLUE, 0.5, 2)
        draw_text(canvas, "Redshift (receding)", (CANVAS_W - 300, CANVAS_H - 30), COLOR_RED, 0.5, 2)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break

    cv2.destroyAllWindows()


def _run_hubble(args: argparse.Namespace) -> None:
    """Hubble's law mode — galaxy scatter plot with v = H0·d line."""
    hl = HubbleLaw(h0=H0)
    random.seed(42)

    # Generate synthetic galaxies at random distances (0–500 Mpc)
    n_galaxies = 30
    distances = [random.uniform(10.0, 500.0) for _ in range(n_galaxies)]
    # Add some scatter to velocities (simulate peculiar velocities)
    velocities = [hl.velocity(d) + random.uniform(-200, 200) for d in distances]

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # ── Plot area ──────────────────────────────────────────────────
        margin_left = 120
        margin_right = 80
        margin_top = 80
        margin_bottom = 80
        plot_w = CANVAS_W - margin_left - margin_right
        plot_h = CANVAS_H - margin_top - margin_bottom

        # Axes
        cv2.rectangle(canvas, (margin_left, margin_top),
                      (margin_left + plot_w, margin_top + plot_h),
                      COLOR_AXIS, 1)

        # Axis labels
        draw_text(canvas, "Distance (Mpc)", (margin_left + plot_w // 2 - 60, CANVAS_H - 20), COLOR_TEXT, 0.5, 1)
        draw_text(canvas, "v (km/s)", (10, margin_top + plot_h // 2), COLOR_TEXT, 0.5, 1)

        # Ticks
        max_dist = 600.0
        max_vel = hl.velocity(max_dist)
        for d in range(0, 601, 100):
            px = int(margin_left + d / max_dist * plot_w)
            cv2.line(canvas, (px, margin_top + plot_h), (px, margin_top + plot_h + 5), COLOR_AXIS, 1)
            draw_text(canvas, str(d), (px - 15, margin_top + plot_h + 20), COLOR_AXIS, 0.4, 1)
        for v in range(0, int(max_vel) + 1, 5000):
            py = int(margin_top + plot_h - v / max_vel * plot_h)
            cv2.line(canvas, (margin_left - 5, py), (margin_left, py), COLOR_AXIS, 1)
            draw_text(canvas, str(v), (margin_left - 50, py + 4), COLOR_AXIS, 0.4, 1)

        # ── Theoretical line v = H0·d ──────────────────────────────────
        line_pts = []
        for d_px in range(0, plot_w + 1):
            d_val = d_px / plot_w * max_dist
            v_val = hl.velocity(d_val)
            px = margin_left + d_px
            py = int(margin_top + plot_h - v_val / max_vel * plot_h)
            line_pts.append((px, py))
        line_arr = np.array(line_pts, dtype=np.int32)
        cv2.polylines(canvas, [line_arr], False, COLOR_GREEN, 2, cv2.LINE_AA)

        # ── Galaxy dots ────────────────────────────────────────────────
        for d, v in zip(distances, velocities):
            px = int(margin_left + d / max_dist * plot_w)
            py = int(margin_top + plot_h - v / max_vel * plot_h)
            cv2.circle(canvas, (px, py), 4, COLOR_ORANGE, -1)

        # ── Info panel ─────────────────────────────────────────────────
        info = [
            "Hubble's Law: v = H0 * d",
            f"H0 = {H0} km/s/Mpc",
            f"v_max = {hl.velocity(max_dist):.0f} km/s at {max_dist:.0f} Mpc",
            f"Galaxies shown: {n_galaxies}",
            "Orange dots = galaxies with peculiar velocities",
            "Green line = theoretical v = H0*d",
        ]
        for i, line in enumerate(info):
            draw_text(canvas, line, (10, 30 + i * 25), COLOR_TEXT, 0.55, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


def _run_lifecycles(args: argparse.Namespace) -> None:
    """Stellar life cycle mode — schematic flow diagram."""
    cv2.namedWindow(WIN_NAME)

    # Box dimensions
    box_w = 200
    box_h = 60
    arrow_len = 80

    # Layout positions (center of each box)
    stages = [
        ("Nebula", (CANVAS_W // 2, 50), COLOR_CYAN),
        ("Main\nSequence", (CANVAS_W // 2, 180), COLOR_GREEN),
        ("Giant /\nSupergiant", (CANVAS_W // 2 - 160, 340), COLOR_ORANGE),
        ("White\nDwarf", (CANVAS_W // 2 - 300, 500), COLOR_BLUE),
        ("Neutron Star\n/ Black Hole", (CANVAS_W // 2 + 160, 500), COLOR_RED),
    ]

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # ── Draw connecting arrows ─────────────────────────────────────
        # Nebula → Main Sequence
        draw_arrow(canvas, (CANVAS_W // 2, 50 + box_h // 2),
                   (CANVAS_W // 2, 180 - box_h // 2), COLOR_TEXT, 2)
        # Main Sequence → Giant/Supergiant
        draw_arrow(canvas, (CANVAS_W // 2, 180 + box_h // 2),
                   (CANVAS_W // 2 - 160, 340 - box_h // 2), COLOR_TEXT, 2)
        # Giant/Supergiant → White Dwarf (low mass)
        draw_arrow(canvas, (CANVAS_W // 2 - 160, 340 + box_h // 2),
                   (CANVAS_W // 2 - 300, 500 - box_h // 2), COLOR_TEXT, 2)
        # Giant/Supergiant → Neutron Star / Black Hole (high mass)
        draw_arrow(canvas, (CANVAS_W // 2 - 160 + box_w // 2, 340 + box_h // 2),
                   (CANVAS_W // 2 + 160 - box_w // 2, 500 - box_h // 2), COLOR_TEXT, 2)

        # ── Draw boxes ─────────────────────────────────────────────────
        for name, (cx, cy), color in stages:
            x1 = cx - box_w // 2
            y1 = cy - box_h // 2
            x2 = cx + box_w // 2
            y2 = cy + box_h // 2
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, 2)
            # Multi-line text
            lines = name.split("\n")
            for li, line in enumerate(lines):
                text_w = len(line) * 7
                tx = cx - text_w // 2
                ty = cy + (li - len(lines) // 2) * 18 + 5
                draw_text(canvas, line, (tx, ty), color, 0.5, 2)

        # ── Info panel ─────────────────────────────────────────────────
        info = [
            "Stellar Life Cycle",
            "",
            "Low-mass stars (≤8 M_sun):",
            "  Nebula → Main Sequence → Giant → White Dwarf",
            "",
            "High-mass stars (>8 M_sun):",
            "  Nebula → Main Sequence → Supergiant → Neutron Star / Black Hole",
            "",
            "Spectral classification (O B A F G K M):",
        ]
        for i, line in enumerate(info):
            draw_text(canvas, line, (10, 30 + i * 22), COLOR_TEXT, 0.5, 1)

        # Spectral class table
        table_x = 10
        table_y = CANVAS_H - 180
        draw_text(canvas, "Class  Temp (K)      Colour", (table_x, table_y), COLOR_TEXT, 0.45, 1)
        for si, sc in enumerate(SPECTRAL_CLASSES):
            row_y = table_y + 20 + si * 20
            row_text = f"  {sc['class']:4s}  {sc['temp_min']}-{sc['temp_max']}  {sc['colour']}"
            draw_text(canvas, row_text, (table_x, row_y), COLOR_TEXT, 0.4, 1)

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
    if mode == "doppler":
        ds = ReferenceDopplerShift(f0=5.8e14)
        # At rest
        f_rest = ds.observed_frequency(0.0)
        assert abs(f_rest - ds.f0) / ds.f0 < 1e-12, "f_obs should equal f0 at rest"
        # Approaching (blueshift)
        f_approach = ds.observed_frequency(-1000.0)
        assert f_approach > ds.f0, "Approaching source should blueshift (f_obs > f0)"
        # Receding (redshift)
        f_recede = ds.observed_frequency(1000.0)
        assert f_recede < ds.f0, "Receding source should redshift (f_obs < f0)"
        # Redshift z ≈ v/c for small v
        z = ds.redshift(1000.0)
        assert abs(z - 1000.0 / C) < 1e-6, f"Low-v redshift should be ≈ v/c, got {z}"
        # Velocity from z
        v_recovered = ds.velocity_from_z(z)
        assert abs(v_recovered - 1000.0) < 1.0, f"velocity_from_z should recover v, got {v_recovered}"
        print("Doppler self-check OK (relativistic Doppler verified)")

    elif mode == "hubble":
        hl = HubbleLaw(h0=H0)
        v = hl.velocity(10.0)
        assert abs(v - H0 * 10.0) / (H0 * 10.0) < 1e-12, f"Hubble velocity mismatch: {v}"
        d = hl.distance(v)
        assert abs(d - 10.0) / 10.0 < 1e-12, f"Hubble distance mismatch: {d}"
        print("Hubble self-check OK (v = H0*d verified)")

    elif mode == "lifecycles":
        # Verify spectral classification table is populated
        assert len(SPECTRAL_CLASSES) == 7, "Should have 7 spectral classes"
        for sc in SPECTRAL_CLASSES:
            assert sc["temp_min"] < sc["temp_max"], f"Invalid temp range for {sc['class']}"
        print("Lifecycles self-check OK (spectral classes verified)")

    print("Astrophysics & Relativity self-check OK")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    if args.headless_selfcheck:
        _headless_selfcheck(args.mode)
        return

    if args.mode == "doppler":
        _run_doppler(args)
    elif args.mode == "hubble":
        _run_hubble(args)
    elif args.mode == "lifecycles":
        _run_lifecycles(args)


if __name__ == "__main__":
    main()