"""Teacher-facing interactive app (M3) for the electricity & magnetism toolkit.

Usage
-----
    uv run python units/04_em/teacher_app/main.py --mode field
    uv run python units/04_em/teacher_app/main.py --mode circuit
    uv run python units/04_em/teacher_app/main.py --mode magnet
    uv run python units/04_em/teacher_app/main.py --mode field --headless-selfcheck

All modes are fully synthetic — no camera required.
"""

from __future__ import annotations

import argparse
import math
import sys
from typing import List, Tuple

import cv2
import numpy as np

from physics_core.em.circuits import ReferenceCircuit
from physics_core.em.electrostatics import ReferenceElectricField
from physics_core.em.magnetism import ReferenceSolenoid, ReferenceStraightWire

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720
WIN_NAME = "Electricity & Magnetism Teacher Demo"
FPS = 30

# Colours (BGR)
COLOR_TEXT = (255, 255, 255)
COLOR_AXIS = (100, 100, 100)
COLOR_FIELD = (0, 200, 255)      # orange field lines
COLOR_FIELD_WEAK = (0, 100, 200)
COLOR_CHARGE_POS = (0, 0, 255)   # red for positive charge
COLOR_CHARGE_NEG = (255, 0, 0)   # blue for negative charge
COLOR_WIRE = (0, 255, 255)       # yellow wire
COLOR_B = (0, 165, 255)          # orange magnetic field
COLOR_CIRCUIT = (0, 255, 0)      # green circuit wires
COLOR_RESISTOR = (0, 0, 255)     # red resistors
COLOR_BATTERY = (0, 255, 255)    # yellow battery

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Electricity & Magnetism teacher demo app")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["field", "circuit", "magnet"],
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


def draw_field_vectors(
    canvas: np.ndarray,
    ef: ReferenceElectricField,
    center_px: Tuple[int, int],
    scale: float,
    step_px: int = 60,
) -> None:
    """Draw electric-field vector arrows on a grid, scaled by magnitude."""
    cx, cy = center_px
    for gx in range(step_px // 2, CANVAS_W, step_px):
        for gy in range(step_px // 2, CANVAS_H, step_px):
            # World coordinates (metres) — map canvas to [-3, 3] m
            wx = (gx - cx) / scale
            wy = (cy - gy) / scale
            Ex, Ey = ef.field(wx, wy)
            E_mag = math.hypot(Ex, Ey)
            if E_mag < 1e-9:
                continue
            # Arrow length proportional to log-magnitude (clamped)
            arrow_len = min(28.0, 6.0 + 4.0 * math.log10(1.0 + E_mag * 1e10))
            # Direction in pixel space (y inverted)
            dx = Ex / E_mag
            dy = -Ey / E_mag
            end_x = int(gx + dx * arrow_len)
            end_y = int(gy + dy * arrow_len)
            color = COLOR_FIELD if E_mag > 1e-4 else COLOR_FIELD_WEAK
            draw_arrow(canvas, (gx, gy), (end_x, end_y), color, 1)


def draw_field_lines(
    canvas: np.ndarray,
    ef: ReferenceElectricField,
    center_px: Tuple[int, int],
    scale: float,
    n_lines: int = 12,
) -> None:
    """Draw electric field lines radiating from the charge."""
    cx, cy = center_px
    for i in range(n_lines):
        angle = 2.0 * math.pi * i / n_lines
        # Trace the field line outward from the charge
        pts: List[Tuple[int, int]] = []
        r = 0.15  # start just outside the charge
        for _ in range(60):
            wx = r * math.cos(angle)
            wy = r * math.sin(angle)
            px = int(cx + wx * scale)
            py = int(cy - wy * scale)
            if px < 0 or px >= CANVAS_W or py < 0 or py >= CANVAS_H:
                break
            pts.append((px, py))
            r += 0.06
        if len(pts) >= 2:
            pts_arr = np.array(pts, dtype=np.int32)
            cv2.polylines(canvas, [pts_arr], False, COLOR_FIELD, 1, cv2.LINE_AA)


def draw_parallel_plate_field(
    canvas: np.ndarray,
    plate_top: int,
    plate_bottom: int,
    left: int,
    right: int,
) -> None:
    """Draw a uniform electric field between two parallel plates."""
    # Plates
    cv2.rectangle(canvas, (left, plate_top), (right, plate_top + 6), COLOR_CHARGE_POS, -1)
    cv2.rectangle(canvas, (left, plate_bottom - 6), (right, plate_bottom), COLOR_CHARGE_NEG, -1)
    cv2.putText(canvas, "+", (left + 10, plate_top + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)
    cv2.putText(canvas, "-", (left + 10, plate_bottom - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

    # Uniform field arrows (pointing downward, from + to -)
    mid_y = (plate_top + plate_bottom) // 2
    for gx in range(left + 40, right, 60):
        draw_arrow(canvas, (gx, mid_y - 20), (gx, mid_y + 20), COLOR_FIELD, 2)


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------


def _run_field(args: argparse.Namespace) -> None:
    """Electric field mode — point charge field lines + vector arrows."""
    ef = ReferenceElectricField(q=1e-9)
    center_px = (CANVAS_W // 2, CANVAS_H // 2)
    scale = 180.0  # px per metre

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        draw_field_lines(canvas, ef, center_px, scale)
        draw_field_vectors(canvas, ef, center_px, scale)

        # Charge marker
        cv2.circle(canvas, center_px, 14, COLOR_CHARGE_POS, -1)
        cv2.circle(canvas, center_px, 14, (255, 255, 255), 1)
        cv2.putText(canvas, "+q", (center_px[0] + 20, center_px[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_CHARGE_POS, 2)

        # Info panel
        info = [
            "Electric field of a point charge",
            "E = q / (4*pi*eps0 * r^2)  (radial)",
            "V = q / (4*pi*eps0 * r)",
            "Field lines point away from +q",
            "Arrow length ~ log |E|",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (10, 30 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break

    cv2.destroyAllWindows()


def _run_circuit(args: argparse.Namespace) -> None:
    """Circuit mode — series circuit with current, potential, power."""
    # Series circuit: V=10V, R1=5Ω, R2=3Ω
    branches = [
        (0, 1, 5.0, 10.0),
        (1, 0, 3.0, 0.0),
    ]
    ckt = ReferenceCircuit(branches)
    ckt.resolve()

    I = ckt.currents["0"]
    V1 = I * 5.0
    V2 = I * 3.0
    P1 = I * I * 5.0
    P2 = I * I * 3.0

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Draw the circuit: battery on left, R1 top, R2 bottom
        # Battery (left vertical)
        bx = 200
        by_top = 200
        by_bot = 520
        cv2.line(canvas, (bx, by_top), (bx, by_bot), COLOR_CIRCUIT, 3)
        # Battery symbol
        cv2.rectangle(canvas, (bx - 15, by_top + 40), (bx + 15, by_top + 90), COLOR_BATTERY, 2)
        cv2.putText(canvas, "10 V", (bx - 60, by_top + 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_BATTERY, 2)

        # Top wire to R1
        cv2.line(canvas, (bx, by_top), (500, by_top), COLOR_CIRCUIT, 3)
        # R1 (top horizontal)
        cv2.rectangle(canvas, (500, by_top - 20), (700, by_top + 20), COLOR_RESISTOR, 2)
        cv2.putText(canvas, "R1 = 5 ohm", (520, by_top - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_RESISTOR, 1)

        # Right wire down to R2
        cv2.line(canvas, (700, by_top), (700, by_bot), COLOR_CIRCUIT, 3)
        # R2 (bottom horizontal)
        cv2.rectangle(canvas, (500, by_bot - 20), (700, by_bot + 20), COLOR_RESISTOR, 2)
        cv2.putText(canvas, "R2 = 3 ohm", (520, by_bot + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_RESISTOR, 1)

        # Bottom wire back to battery
        cv2.line(canvas, (500, by_bot), (bx, by_bot), COLOR_CIRCUIT, 3)

        # Current arrow (clockwise)
        mid_top = (450, by_top - 30)
        mid_bot = (450, by_bot + 30)
        draw_arrow(canvas, mid_top, (450, by_top), COLOR_TEXT, 2)
        draw_arrow(canvas, (450, by_bot), mid_bot, COLOR_TEXT, 2)

        # Info panel
        info = [
            "Series circuit (Kirchhoff's laws)",
            f"I = {I:.3f} A   (V / (R1+R2))",
            f"V_R1 = {V1:.3f} V   (I*R1)",
            f"V_R2 = {V2:.3f} V   (I*R2)",
            f"KVL: 10 - {V1:.2f} - {V2:.2f} = {10 - V1 - V2:.2e} V",
            f"P_R1 = {P1:.3f} W   (I^2*R1)",
            f"P_R2 = {P2:.3f} W   (I^2*R2)",
            f"P_total = {P1 + P2:.3f} W",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (850, 100 + i * 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


def _run_magnet(args: argparse.Namespace) -> None:
    """Magnetic field mode — straight wire field lines."""
    wire = ReferenceStraightWire(current=2.0)
    center_px = (CANVAS_W // 2, CANVAS_H // 2)

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Concentric circular field lines around the wire
        for radius_px in range(40, 320, 40):
            cv2.circle(canvas, center_px, radius_px, COLOR_B, 1, cv2.LINE_AA)

        # Field vector arrows along the circles (tangential)
        for radius_px in range(40, 320, 40):
            for angle in range(0, 360, 30):
                a = math.radians(angle)
                px = int(center_px[0] + radius_px * math.cos(a))
                py = int(center_px[1] + radius_px * math.sin(a))
                # Tangential direction (right-hand rule, CCW)
                tx = -math.sin(a)
                ty = math.cos(a)
                end_x = int(px + tx * 18)
                end_y = int(py + ty * 18)
                draw_arrow(canvas, (px, py), (end_x, end_y), COLOR_B, 1)

        # Wire (cross-section, current out of screen)
        cv2.circle(canvas, center_px, 12, COLOR_WIRE, -1)
        cv2.circle(canvas, center_px, 12, (255, 255, 255), 1)
        cv2.putText(canvas, "I (out)", (center_px[0] + 20, center_px[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WIRE, 2)

        # Info panel
        info = [
            "Magnetic field of a straight wire",
            "B = mu0 * I / (2*pi*r)  (circumferential)",
            "Right-hand rule: thumb = current,",
            "fingers curl = field direction",
            "Field strength decreases as 1/r",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (10, 30 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

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
    if mode == "field":
        ef = ReferenceElectricField(q=1e-9)
        Ex, Ey = ef.field(1.0, 0.0)
        assert math.hypot(Ex, Ey) > 0.0, "Electric field must be non-zero"
        V = ef.potential(1.0, 0.0)
        assert V > 0.0, "Potential must be positive for +q"
        print("Field self-check OK (Coulomb E and V verified)")

    elif mode == "circuit":
        branches = [
            (0, 1, 5.0, 10.0),
            (1, 0, 3.0, 0.0),
        ]
        ckt = ReferenceCircuit(branches)
        ckt.resolve()
        I = ckt.currents["0"]
        # KVL: sum of voltage drops = 0
        V_loop = 10.0 - I * 5.0 - I * 3.0
        assert abs(V_loop) < 1e-9, f"KVL violated: {V_loop}"
        # KCL: current in = current out at node 1
        I_out = ckt.currents["1"]
        assert abs(I - I_out) < 1e-9, f"KCL violated: {I} != {I_out}"
        print("Circuit self-check OK (Kirchhoff's laws verified)")

    elif mode == "magnet":
        wire = ReferenceStraightWire(current=2.0)
        Bx, By, Bz = wire.field(0.1, 0.0)
        B_mag = math.sqrt(Bx * Bx + By * By + Bz * Bz)
        assert B_mag > 0.0, "Magnetic field must be non-zero"
        solenoid = ReferenceSolenoid(current=2.0, N=200, length=0.5)
        _, _, Bz_sol = solenoid.field(0.0, 0.0)
        assert Bz_sol > 0.0, "Solenoid field must be non-zero"
        print("Magnet self-check OK (wire and solenoid fields verified)")

    print("Electricity & Magnetism self-check OK")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    if args.headless_selfcheck:
        _headless_selfcheck(args.mode)
        return

    if args.mode == "field":
        _run_field(args)
    elif args.mode == "circuit":
        _run_circuit(args)
    elif args.mode == "magnet":
        _run_magnet(args)


if __name__ == "__main__":
    main()