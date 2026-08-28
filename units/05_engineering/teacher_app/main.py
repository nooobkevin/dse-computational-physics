"""Teacher-facing interactive app (M3) for the Physics & Engineering toolkit.

Usage
-----
    uv run python units/05_engineering/teacher_app/main.py --mode fibre
    uv run python units/05_engineering/teacher_app/main.py --mode transformer
    uv run python units/05_engineering/teacher_app/main.py --mode laser
    uv run python units/05_engineering/teacher_app/main.py --mode fibre --headless-selfcheck

All modes are fully synthetic — no camera required.
"""

from __future__ import annotations

import argparse
import math
import sys
from typing import List, Tuple

import cv2
import numpy as np

from physics_core.engineering.lasers import ReferenceLaser
from physics_core.engineering.motors import ReferenceTransformer
from physics_core.engineering.optics import ReferenceOpticalFibre

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720
WIN_NAME = "Physics & Engineering Teacher Demo"
FPS = 30

# Colours (BGR)
COLOR_TEXT = (255, 255, 255)
COLOR_AXIS = (100, 100, 100)
COLOR_TIR = (0, 255, 0)        # green for TIR
COLOR_LEAK = (0, 0, 255)       # red for leak
COLOR_CORE = (200, 200, 0)     # yellow core
COLOR_CLAD = (100, 100, 100)   # grey cladding
COLOR_RAY = (0, 200, 255)      # orange ray
COLOR_PRIMARY = (0, 255, 255)  # yellow primary
COLOR_SECONDARY = (0, 165, 255)  # orange secondary
COLOR_LASER = (0, 255, 0)      # green laser

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Physics & Engineering teacher demo app"
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["fibre", "transformer", "laser"],
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


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------


def _run_fibre(args: argparse.Namespace) -> None:
    """Optical fibre mode — TIR ray tracing."""
    fibre = ReferenceOpticalFibre(n1=1.50, n2=1.45, length=10.0, angle=1.4)
    crit = fibre.critical_angle
    crit_deg = math.degrees(crit)

    cv2.namedWindow(WIN_NAME)

    angle_rad = 1.4  # start above critical

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)
        fibre.angle = angle_rad

        # Fibre cross-section (horizontal)
        cx, cy = CANVAS_W // 2, CANVAS_H // 2
        half_len = 400
        core_half = 30
        clad_half = 50

        # Cladding
        cv2.rectangle(canvas, (cx - half_len, cy - clad_half),
                      (cx + half_len, cy + clad_half), COLOR_CLAD, 1)
        # Core
        cv2.rectangle(canvas, (cx - half_len, cy - core_half),
                      (cx + half_len, cy + core_half), COLOR_CORE, 1)

        # Ray zigzag inside core
        tir = fibre.total_internal_reflection(angle_rad)
        ray_color = COLOR_TIR if tir else COLOR_LEAK

        # Draw zigzag ray
        n_bounces = 4
        x_start = cx - half_len + 20
        x_end = cx + half_len - 20
        seg_len = (x_end - x_start) / n_bounces
        for i in range(n_bounces):
            x1 = int(x_start + i * seg_len)
            y1 = cy - core_half + 5 if i % 2 == 0 else cy + core_half - 5
            x2 = int(x_start + (i + 1) * seg_len)
            y2 = cy + core_half - 5 if i % 2 == 0 else cy - core_half + 5
            cv2.line(canvas, (x1, y1), (x2, y2), ray_color, 2, cv2.LINE_AA)

        # Labels
        cv2.putText(canvas, f"n1 (core) = {fibre.n1}", (cx - half_len, cy - clad_half - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        cv2.putText(canvas, f"n2 (clad) = {fibre.n2}", (cx - half_len, cy - clad_half - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        # Info panel
        status = "TIR (total internal reflection)" if tir else "LEAK (ray escapes)"
        info = [
            "Optical fibre — Total Internal Reflection",
            f"Critical angle: {crit_deg:.1f} deg  (arcsin(n2/n1))",
            f"Ray angle: {math.degrees(angle_rad):.1f} deg",
            f"Status: {status}",
            "",
            "Press UP/DOWN to change ray angle",
            "Press ESC to exit",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (10, 30 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break
        elif key == 82:  # UP
            angle_rad = min(angle_rad + 0.05, math.pi / 2 - 0.01)
        elif key == 84:  # DOWN
            angle_rad = max(angle_rad - 0.05, 0.01)

    cv2.destroyAllWindows()


def _run_transformer(args: argparse.Namespace) -> None:
    """Transformer mode — turns ratio, voltage, current, power."""
    t = ReferenceTransformer(Np=100, Ns=50, Vp=230.0, load_resistance=20.0)
    t.step()

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Draw transformer schematic
        cx, cy = CANVAS_W // 2, CANVAS_H // 2

        # Primary coil (left)
        cv2.putText(canvas, "PRIMARY", (cx - 300, cy - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_PRIMARY, 2)
        for i in range(6):
            x = cx - 200 + i * 12
            cv2.arcLength(canvas, (x, cy - 40), (x + 6, cy + 40), COLOR_PRIMARY, 2)

        # Core (rectangle)
        cv2.rectangle(canvas, (cx - 120, cy - 60), (cx + 120, cy + 60), (150, 150, 150), 2)

        # Secondary coil (right)
        cv2.putText(canvas, "SECONDARY", (cx + 160, cy - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_SECONDARY, 2)
        for i in range(4):
            x = cx + 140 + i * 12
            cv2.arcLength(canvas, (x, cy - 40), (x + 6, cy + 40), COLOR_SECONDARY, 2)

        # Info panel
        Vp = t.state["Vp"]
        Vs = t.state["Vs"]
        Ip = t.state["Ip"]
        Is = t.state["Is"]
        Pp = Vp * Ip
        Ps = Vs * Is

        info = [
            "Ideal Transformer",
            f"Np = {t.Np} turns, Ns = {t.Ns} turns",
            f"Turns ratio Np/Ns = {t.Np}/{t.Ns} = {t.Np/t.Ns:.2f}",
            "",
            f"Vp = {Vp:.1f} V",
            f"Vs = Vp * Ns/Np = {Vs:.1f} V",
            f"Vp/Vs = {Vp/Vs:.2f}  (should equal Np/Ns = {t.Np/t.Ns:.2f})",
            "",
            f"Ip = {Ip:.3f} A",
            f"Is = {Is:.3f} A",
            f"Ip/Is = {Ip/Is:.4f}  (should equal Ns/Np = {t.Ns/t.Np:.4f})",
            "",
            f"Primary power = {Pp:.1f} W",
            f"Secondary power = {Ps:.1f} W",
            f"Power conserved: {Pp:.1f} ≈ {Ps:.1f} W",
            "",
            "Press ESC to exit",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (50, 50 + i * 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


def _run_laser(args: argparse.Namespace) -> None:
    """Laser mode — population inversion and stimulated emission."""
    laser = ReferenceLaser(N_upper=100.0, N_lower=10.0, pump_rate=50.0)

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Draw laser cavity
        cx, cy = CANVAS_W // 2, CANVAS_H // 2

        # Mirrors
        cv2.rectangle(canvas, (cx - 300, cy - 80), (cx - 290, cy + 80), (200, 200, 200), -1)
        cv2.rectangle(canvas, (cx + 290, cy - 80), (cx + 300, cy + 80), (200, 200, 200), -1)

        # Gain medium
        cv2.rectangle(canvas, (cx - 200, cy - 60), (cx + 200, cy + 60), (50, 50, 50), 1)

        # Laser beam (coherent light)
        photon_count = laser.state["photon_count"]
        beam_intensity = min(1.0, photon_count / 50.0)
        if beam_intensity > 0.01:
            beam_color = (0, int(255 * beam_intensity), int(255 * beam_intensity))
            cv2.line(canvas, (cx - 290, cy), (cx + 290, cy), beam_color, 3)
            # Output beam
            cv2.line(canvas, (cx + 290, cy), (cx + 350, cy), beam_color, 2)

        # Energy level diagram
        ey = 150
        # Upper level
        cv2.line(canvas, (50, ey), (250, ey), COLOR_LASER, 2)
        cv2.putText(canvas, f"N_upper = {laser.N_upper:.0f}", (260, ey + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_LASER, 1)
        # Lower level
        cv2.line(canvas, (50, ey + 100), (250, ey + 100), COLOR_LEAK, 2)
        cv2.putText(canvas, f"N_lower = {laser.N_lower:.0f}", (260, ey + 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_LEAK, 1)

        # Population inversion indicator
        inversion = laser.population_inversion
        inv_color = COLOR_TIR if inversion else COLOR_LEAK
        inv_text = "Population inversion: YES" if inversion else "Population inversion: NO"
        cv2.putText(canvas, inv_text, (50, ey + 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, inv_color, 2)

        # Info panel
        info = [
            "Laser — Stimulated Emission",
            f"Photon count: {photon_count:.1f}",
            f"Pump rate: {laser.pump_rate:.0f} atoms/s",
            "",
            "Stimulated emission requires",
            "population inversion (N_upper > N_lower).",
            "Coherent photons build up in the cavity.",
            "",
            "Press ESC to exit",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (50, 400 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

        # Step the simulation
        laser.step(0.05)

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
    if mode == "fibre":
        fibre = ReferenceOpticalFibre(n1=1.50, n2=1.45)
        crit = fibre.critical_angle
        expected_crit = math.asin(1.45 / 1.50)
        assert abs(crit - expected_crit) < 1e-6, \
            f"Critical angle mismatch: {crit} vs {expected_crit}"
        # Ray above critical should TIR
        assert fibre.total_internal_reflection(crit + 0.1), \
            "Ray above critical angle should TIR"
        # Ray below critical should leak
        assert not fibre.total_internal_reflection(max(0.01, crit - 0.1)), \
            "Ray below critical angle should leak"
        print("Fibre self-check OK (TIR physics verified)")

    elif mode == "transformer":
        t = ReferenceTransformer(Np=100, Ns=50, Vp=230.0, load_resistance=20.0)
        t.step()
        Vs = t.state["Vs"]
        Ip = t.state["Ip"]
        Is = t.state["Is"]
        # Vp/Vs = Np/Ns
        assert abs(230.0 / Vs - 100.0 / 50.0) < 1e-6, \
            f"Voltage ratio mismatch: {230.0/Vs} vs {100.0/50.0}"
        # Ip/Is = Ns/Np
        assert abs(Ip / Is - 50.0 / 100.0) < 1e-6, \
            f"Current ratio mismatch: {Ip/Is} vs {50.0/100.0}"
        # Power conservation
        Pp = 230.0 * Ip
        Ps = Vs * Is
        assert abs(Pp - Ps) < 1e-6, \
            f"Power not conserved: Pp={Pp}, Ps={Ps}"
        print("Transformer self-check OK (turns ratio and power verified)")

    elif mode == "laser":
        laser = ReferenceLaser(N_upper=100.0, N_lower=10.0)
        assert laser.population_inversion, "Population inversion should exist"
        photons = laser.stimulated_emission()
        assert photons > 0, "Stimulated emission should produce photons"
        laser.step(0.1)
        assert laser.state["photon_count"] > 0, "Photon count should increase"
        print("Laser self-check OK (stimulated emission verified)")

    print("Physics & Engineering self-check OK")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    if args.headless_selfcheck:
        _headless_selfcheck(args.mode)
        return

    if args.mode == "fibre":
        _run_fibre(args)
    elif args.mode == "transformer":
        _run_transformer(args)
    elif args.mode == "laser":
        _run_laser(args)


if __name__ == "__main__":
    main()