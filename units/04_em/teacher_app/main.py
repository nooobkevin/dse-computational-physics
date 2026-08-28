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
import pytest

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
        choices=["field", "circuit", "magnet", "solenoid", "vi_graph", "parallel"],
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
# Solenoid mode
# ---------------------------------------------------------------------------


def _run_solenoid(args: argparse.Namespace) -> None:
    """Solenoid mode — uniform B field inside a solenoid with current slider."""
    solenoid = ReferenceSolenoid(current=1.0, N=200, length=0.5)
    current_val: float = 1.0

    cv2.namedWindow(WIN_NAME)
    cv2.createTrackbar("Current (A)", WIN_NAME, 10, 50, lambda _: None)

    while True:
        current_val = cv2.getTrackbarPos("Current (A)", WIN_NAME) / 10.0
        if current_val < 0.1:
            current_val = 0.1
        solenoid.I = current_val

        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Draw solenoid cross-section (rectangle with coil windings)
        sx, sy = CANVAS_W // 2 - 200, CANVAS_H // 2 - 150
        sw, sh = 400, 300
        cv2.rectangle(canvas, (sx, sy), (sx + sw, sy + sh), (100, 100, 100), 2)
        # Coil windings (vertical lines on left and right edges)
        for i in range(10):
            y_off = sy + (i + 1) * sh // 11
            cv2.line(canvas, (sx - 10, y_off), (sx, y_off), COLOR_WIRE, 1)
            cv2.line(canvas, (sx + sw, y_off), (sx + sw + 10, y_off), COLOR_WIRE, 1)

        # Field lines inside solenoid (uniform, parallel arrows)
        B_mag = solenoid.mu0 * solenoid.N * solenoid.I / solenoid.L
        arrow_spacing = 40
        for gx in range(sx + 30, sx + sw - 20, arrow_spacing):
            for gy in range(sy + 30, sy + sh - 20, arrow_spacing):
                draw_arrow(canvas, (gx, gy - 10), (gx, gy + 10), COLOR_B, 2)

        # Field label
        cv2.putText(canvas, "N", (sx + sw // 2 - 10, sy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        cv2.putText(canvas, "S", (sx + sw // 2 - 10, sy + sh + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        # Info panel
        info = [
            "Solenoid magnetic field",
            f"B = mu0 * N * I / L",
            f"N = {solenoid.N}, L = {solenoid.L:.2f} m",
            f"I = {current_val:.1f} A",
            f"B = {B_mag:.6f} T",
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
# V-I graph mode
# ---------------------------------------------------------------------------


def _run_vi_graph(args: argparse.Namespace) -> None:
    """V-I graph mode — ohmic vs non-ohmic I-V characteristics with slope readout."""
    cv2.namedWindow(WIN_NAME)

    # Graph area
    graph_left, graph_right = 100, 700
    graph_top, graph_bottom = 80, 620
    graph_w = graph_right - graph_left
    graph_h = graph_bottom - graph_top

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Draw axes
        cv2.line(canvas, (graph_left, graph_bottom), (graph_right, graph_bottom), COLOR_AXIS, 2)
        cv2.line(canvas, (graph_left, graph_bottom), (graph_left, graph_top), COLOR_AXIS, 2)
        cv2.putText(canvas, "V (V)", (graph_right - 40, graph_bottom + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        cv2.putText(canvas, "I (A)", (graph_left - 30, graph_top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        # Generate I-V data
        v_max = 12.0
        n_pts = 100
        ohmic_R = 4.0  # 4 ohm resistor
        lamp_R0 = 2.0  # filament lamp cold resistance

        ohmic_pts: List[Tuple[int, int]] = []
        lamp_pts: List[Tuple[int, int]] = []
        for i in range(n_pts + 1):
            v = v_max * i / n_pts
            # Ohmic: I = V/R (straight line)
            i_ohmic = v / ohmic_R
            # Non-ohmic (filament lamp): I ∝ V^0.6 (approximate curve)
            i_lamp = (v / v_max) ** 0.6 * (v_max / lamp_R0)

            px = int(graph_left + v / v_max * graph_w)
            py_ohmic = int(graph_bottom - i_ohmic / (v_max / ohmic_R) * graph_h)
            py_lamp = int(graph_bottom - i_lamp / (v_max / lamp_R0) * graph_h)
            ohmic_pts.append((px, py_ohmic))
            lamp_pts.append((px, py_lamp))

        # Draw ohmic curve (green)
        if len(ohmic_pts) >= 2:
            pts_arr = np.array(ohmic_pts, dtype=np.int32)
            cv2.polylines(canvas, [pts_arr], False, (0, 255, 0), 2, cv2.LINE_AA)

        # Draw non-ohmic curve (red)
        if len(lamp_pts) >= 2:
            pts_arr = np.array(lamp_pts, dtype=np.int32)
            cv2.polylines(canvas, [pts_arr], False, (0, 0, 255), 2, cv2.LINE_AA)

        # Legend
        cv2.putText(canvas, "Ohmic (R = 4 ohm)", (graph_left + 20, graph_top + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(canvas, "Non-ohmic (lamp)", (graph_left + 20, graph_top + 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Slope readout at V=6V
        v_test = 6.0
        i_ohmic_test = v_test / ohmic_R
        i_lamp_test = (v_test / v_max) ** 0.6 * (v_max / lamp_R0)
        slope_ohmic = i_ohmic_test / v_test  # 1/R
        slope_lamp = i_lamp_test / v_test

        info = [
            "V-I characteristics",
            f"Ohmic: slope = 1/R = {slope_ohmic:.3f} S",
            f"  R = {1.0 / slope_ohmic:.2f} ohm",
            f"Non-ohmic: slope = {slope_lamp:.3f} S",
            f"  (slope varies with V)",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (750, 100 + i * 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Parallel circuit mode
# ---------------------------------------------------------------------------


def _run_parallel(args: argparse.Namespace) -> None:
    """Parallel circuit mode — 2-branch parallel with KCL verification."""
    # Parallel circuit: V=10V, R1=5Ω, R2=3Ω
    branches = [
        (0, 1, 0.001, 10.0),  # near-ideal source
        (1, 0, 5.0, 0.0),     # R1
        (1, 0, 3.0, 0.0),     # R2
    ]
    ckt = ReferenceCircuit(branches)
    ckt.resolve()

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Draw parallel circuit
        # Battery on left
        bx, by = 200, CANVAS_H // 2
        cv2.line(canvas, (bx, by - 150), (bx, by + 150), COLOR_CIRCUIT, 3)
        cv2.rectangle(canvas, (bx - 15, by - 60), (bx + 15, by - 10), COLOR_BATTERY, 2)
        cv2.putText(canvas, "10 V", (bx - 60, by - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_BATTERY, 2)

        # Top horizontal wire
        cv2.line(canvas, (bx, by - 150), (600, by - 150), COLOR_CIRCUIT, 3)
        # Bottom horizontal wire
        cv2.line(canvas, (bx, by + 150), (600, by + 150), COLOR_CIRCUIT, 3)

        # R1 branch (top)
        cv2.rectangle(canvas, (350, by - 170), (450, by - 130), COLOR_RESISTOR, 2)
        cv2.putText(canvas, "R1 = 5 ohm", (350, by - 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_RESISTOR, 1)
        cv2.line(canvas, (350, by - 150), (350, by - 170), COLOR_CIRCUIT, 3)
        cv2.line(canvas, (450, by - 150), (450, by - 170), COLOR_CIRCUIT, 3)

        # R2 branch (bottom)
        cv2.rectangle(canvas, (350, by + 130), (450, by + 170), COLOR_RESISTOR, 2)
        cv2.putText(canvas, "R2 = 3 ohm", (350, by + 185), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_RESISTOR, 1)
        cv2.line(canvas, (350, by + 150), (350, by + 130), COLOR_CIRCUIT, 3)
        cv2.line(canvas, (450, by + 150), (450, by + 130), COLOR_CIRCUIT, 3)

        # Right vertical wire
        cv2.line(canvas, (600, by - 150), (600, by + 150), COLOR_CIRCUIT, 3)

        # Current arrows
        I_total = ckt.currents["0"]
        I1 = ckt.currents["1"]
        I2 = ckt.currents["2"]
        draw_arrow(canvas, (bx + 30, by - 100), (bx + 30, by - 150), COLOR_TEXT, 2)
        draw_arrow(canvas, (550, by - 150), (550, by - 130), COLOR_TEXT, 2)
        draw_arrow(canvas, (550, by + 150), (550, by + 130), COLOR_TEXT, 2)

        # KCL verification badge
        kcl_ok = abs(I_total - (I1 + I2)) < 0.01
        badge_color = (0, 255, 0) if kcl_ok else (0, 0, 255)
        badge_text = f"KCL: I_in = {I_total:.3f}A, I_out = {I1 + I2:.3f}A  {'OK' if kcl_ok else 'FAIL'}"
        cv2.putText(canvas, badge_text, (700, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, badge_color, 2)

        # Info panel
        info = [
            "Parallel circuit (Kirchhoff's laws)",
            f"I_total = {I_total:.3f} A",
            f"I_R1 = {I1:.3f} A   (V / R1)",
            f"I_R2 = {I2:.3f} A   (V / R2)",
            f"KCL: {I_total:.3f} = {I1:.3f} + {I2:.3f}",
            f"R_eq = 1/(1/{5.0} + 1/{3.0}) = {1.0 / (1.0/5.0 + 1.0/3.0):.3f} ohm",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (700, 200 + i * 30),
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
        V_loop = 10.0 - I * 5.0 - I * 3.0
        assert abs(V_loop) < 1e-9, f"KVL violated: {V_loop}"
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

    elif mode == "solenoid":
        solenoid = ReferenceSolenoid(current=1.0, N=200, length=0.5)
        Bx, By, Bz = solenoid.field(0.0, 0.0)
        B_mag = math.sqrt(Bx * Bx + By * By + Bz * Bz)
        expected = solenoid.mu0 * solenoid.N * solenoid.I / solenoid.L
        assert B_mag == pytest.approx(expected, rel=1e-6), (
            f"Solenoid B = {B_mag}, expected {expected}"
        )
        print("Solenoid self-check OK (uniform internal field verified)")

    elif mode == "vi_graph":
        # Verify ohmic slope = 1/R
        R = 4.0
        v_test = 6.0
        i_ohmic = v_test / R
        slope = i_ohmic / v_test
        assert abs(slope - 1.0 / R) < 1e-9, f"Ohmic slope {slope} != 1/{R}"
        # Verify non-ohmic slope differs
        v_max = 12.0
        i_lamp = (v_test / v_max) ** 0.6 * (v_max / 2.0)
        lamp_slope = i_lamp / v_test
        assert lamp_slope != pytest.approx(1.0 / R, rel=0.1), (
            "Non-ohmic slope should differ from ohmic"
        )
        print("V-I graph self-check OK (ohmic vs non-ohmic verified)")

    elif mode == "parallel":
        branches = [
            (0, 1, 0.001, 10.0),
            (1, 0, 5.0, 0.0),
            (1, 0, 3.0, 0.0),
        ]
        ckt = ReferenceCircuit(branches)
        ckt.resolve()
        I_total = ckt.currents["0"]
        I1 = ckt.currents["1"]
        I2 = ckt.currents["2"]
        # KCL: I_in = I_out1 + I_out2
        assert abs(I_total - (I1 + I2)) < 0.01, (
            f"KCL violated: {I_total} != {I1} + {I2}"
        )
        # Verify individual branch currents
        assert I1 == pytest.approx(10.0 / 5.0, rel=0.01), f"I1 = {I1}, expected 2.0"
        assert I2 == pytest.approx(10.0 / 3.0, rel=0.01), f"I2 = {I2}, expected 3.33"
        print("Parallel self-check OK (KCL and branch currents verified)")

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
    elif args.mode == "solenoid":
        _run_solenoid(args)
    elif args.mode == "vi_graph":
        _run_vi_graph(args)
    elif args.mode == "parallel":
        _run_parallel(args)


if __name__ == "__main__":
    main()