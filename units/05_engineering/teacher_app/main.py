"""Teacher-facing interactive app (M3) for the Physics & Engineering toolkit.

Usage
-----
    uv run python units/05_engineering/teacher_app/main.py --mode fibre
    uv run python units/05_engineering/teacher_app/main.py --mode transformer
    uv run python units/05_engineering/teacher_app/main.py --mode orbital
    uv run python units/05_engineering/teacher_app/main.py --mode induction
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

from physics_core.engineering.induction import ReferenceInductionCoil
from physics_core.engineering.motors import ReferenceTransformer
from physics_core.engineering.optics import ReferenceOpticalFibre
from physics_core.engineering.orbital import ReferenceOrbitalBody

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
COLOR_SAT = (0, 255, 0)         # green satellite
COLOR_ORBIT = (200, 200, 200)   # light grey orbit
COLOR_KE = (0, 255, 0)          # green KE
COLOR_GPE = (0, 0, 255)         # red GPE
COLOR_TOTAL = (255, 255, 0)     # cyan total
COLOR_FLUX = (255, 200, 0)      # yellow flux
COLOR_EMF = (0, 200, 255)       # orange emf
COLOR_COIL = (0, 165, 255)      # orange coil
COLOR_MAGNET = (0, 0, 200)      # dark red magnet

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
        choices=["fibre", "transformer", "orbital", "induction"],
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


def _run_orbital(args: argparse.Namespace) -> None:
    """Orbital mode — satellite orbit with energy display."""
    M = 5.972e24
    r = 7.0e6
    m = 1000.0
    v_orb = math.sqrt(6.67430e-11 * M / r)
    sim = ReferenceOrbitalBody(M=M, m=m, x=r, y=0.0, vx=0.0, vy=v_orb)
    scale = 1e-7
    cx, cy = CANVAS_W // 3, CANVAS_H // 2
    orbit_r = int(r * scale)
    altitude = 400.0  # km (display)
    show_esc = False

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Earth (centre)
        cv2.circle(canvas, (cx, cy), 20, (200, 100, 0), -1)
        cv2.circle(canvas, (cx, cy), int(orbit_r), COLOR_ORBIT, 1, cv2.LINE_AA)

        # Satellite
        sx = cx + int(sim.state["x"] * scale)
        sy = cy - int(sim.state["y"] * scale)
        cv2.circle(canvas, (sx, sy), 5, COLOR_SAT, -1)

        # Velocity vector (tangent)
        vx, vy = sim.state["vx"], sim.state["vy"]
        v_mag = math.hypot(vx, vy)
        if v_mag > 1:
            v_len = 60
            cv2.arrowedLine(
                canvas, (sx, sy),
                (sx + int(vx / v_mag * v_len), sy - int(vy / v_mag * v_len)),
                COLOR_KE, 2, tipLength=0.3,
            )

        # Force vector (toward centre)
        dx = cx - sx
        dy = cy - sy
        d = math.hypot(dx, dy)
        if d > 1:
            f_len = 50
            cv2.arrowedLine(
                canvas, (sx, sy),
                (sx + int(dx / d * f_len), sy + int(dy / d * f_len)),
                COLOR_GPE, 2, tipLength=0.3,
            )

        # Energy bar chart (right side)
        bar_x = CANVAS_W * 3 // 4
        energy = sim.energy_components()
        max_e = 2.5e11
        ke_h = int(energy["kinetic"] / max_e * 150)
        gpe_h = int(abs(energy["potential"]) / max_e * 150)
        total_h = int(abs(energy["total"]) / max_e * 150)

        cv2.rectangle(canvas, (bar_x - 20, 250 - ke_h), (bar_x, 250), COLOR_KE, -1)
        cv2.rectangle(canvas, (bar_x + 10, 250), (bar_x + 30, 250 + gpe_h), COLOR_GPE, -1)
        total_y = 250 - total_h if energy["total"] < 0 else 250 + total_h
        cv2.rectangle(canvas, (bar_x + 40, min(250, total_y)), (bar_x + 60, max(250, total_y)), COLOR_TOTAL, -1)

        # Info panel
        r_km = sim.radius / 1000
        v_orb_val = sim.orbital_velocity(sim.radius)
        v_esc_val = sim.escape_velocity(sim.radius)
        info = [
            "Orbital Motion",
            f"Altitude: {r_km - 6371:.0f} km  (r = {r_km:.0f} km)",
            f"v = {sim.speed/1000:.2f} km/s  |  v_orb = {v_orb_val/1000:.2f} km/s",
            f"v_esc = {v_esc_val/1000:.2f} km/s",
            "",
            f"KE = {energy['kinetic']/1e9:.2f} GJ",
            f"GPE = {energy['potential']/1e9:.2f} GJ",
            f"Total = {energy['total']/1e9:.2f} GJ",
            "",
            "Press E to toggle escape velocity comparison",
            "Press ESC to exit",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (10, 30 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

        if show_esc:
            cv2.putText(canvas,
                        f"v_esc / v_orb = {v_esc_val/v_orb_val:.2f} = sqrt(2)",
                        (10, 30 + len(info) * 25 + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TIR, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord("e") or key == ord("E"):
            show_esc = not show_esc

        # Step the simulation
        sim.step(50.0)

    cv2.destroyAllWindows()


def _run_induction(args: argparse.Namespace) -> None:
    """Induction mode — magnet and coil with flux and emf display."""
    coil = ReferenceInductionCoil(B=1.0, A=0.01, magnet_position=-3.0)
    cx, cy = CANVAS_W * 1 // 4, CANVAS_H // 2 - 50

    flux_history: list[float] = []
    emf_history: list[float] = []

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Coil (schematic)
        coil_x = cx
        for i in range(6):
            x = coil_x - 30 + i * 12
            cv2.line(canvas, (x, cy - 40), (x + 6, cy + 40), COLOR_COIL, 2)
        cv2.putText(canvas, "Coil", (coil_x - 20, cy - 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_COIL, 1)

        # Magnet
        magnet_x = cx + int(coil.state["magnet_position"] * 50)
        cv2.rectangle(canvas, (magnet_x - 20, cy - 25), (magnet_x + 20, cy + 25), COLOR_MAGNET, -1)
        cv2.putText(canvas, "N", (magnet_x - 6, cy + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv2.putText(canvas, "Magnet", (magnet_x - 25, cy - 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_MAGNET, 1)

        # Flux graph
        graph_x0 = CANVAS_W // 2 + 50
        graph_y0 = 150
        flux = coil.state["flux"]
        emf = coil.state["emf"]
        flux_history.append(flux)
        emf_history.append(emf)
        if len(flux_history) > 200:
            flux_history.pop(0)
            emf_history.pop(0)

        # Flux curve
        if len(flux_history) > 1:
            pts_flux = [(graph_x0 + int(i * 200 / len(flux_history)),
                         graph_y0 - int(f / max(abs(f) for f in flux_history + [1e-9]) * 60))
                        for i, f in enumerate(flux_history)]
            for i in range(len(pts_flux) - 1):
                cv2.line(canvas, pts_flux[i], pts_flux[i + 1], COLOR_FLUX, 2)

        cv2.putText(canvas, "Flux (Wb)", (graph_x0, graph_y0 - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_FLUX, 1)

        # EMF graph
        emf_y0 = 350
        if len(emf_history) > 1:
            max_emf = max(abs(e) for e in emf_history + [1e-9])
            pts_emf = [(graph_x0 + int(i * 200 / len(emf_history)),
                        emf_y0 - int(e / max_emf * 60))
                       for i, e in enumerate(emf_history)]
            for i in range(len(pts_emf) - 1):
                cv2.line(canvas, pts_emf[i], pts_emf[i + 1], COLOR_EMF, 2)

        cv2.putText(canvas, "EMF (V)", (graph_x0, emf_y0 - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_EMF, 1)

        # Lenz direction
        if len(flux_history) >= 2:
            direction = coil.lenz_direction(flux_history[-2], flux_history[-1])
        else:
            direction = "CW"
        cv2.putText(canvas, f"Lenz: {direction} current",
                    (graph_x0, emf_y0 + 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TIR, 1)

        # Info
        info = [
            "Electromagnetic Induction",
            f"Magnet position: {coil.magnet_position:.2f} m",
            f"Flux: {flux:.6f} Wb",
            f"EMF: {emf:.4f} V",
            "",
            "Press ESC to exit",
        ]
        for i, line in enumerate(info):
            cv2.putText(canvas, line, (10, 30 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

        # Oscillate magnet
        coil.magnet_position += 0.02
        if coil.magnet_position > 3.0:
            coil.magnet_position = -3.0
        coil.step(0.05)

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

    elif mode == "orbital":
        sim = ReferenceOrbitalBody(M=5.972e24, m=1000.0)
        r = sim.radius
        v_orb = sim.orbital_velocity(r)
        v_esc = sim.escape_velocity(r)
        # v_orb = sqrt(GM/r)
        expected_v_orb = math.sqrt(6.67430e-11 * 5.972e24 / r)
        assert abs(v_orb - expected_v_orb) / expected_v_orb < 1e-6, \
            f"Orbital velocity mismatch: {v_orb} vs {expected_v_orb}"
        # v_esc = sqrt(2) * v_orb
        assert abs(v_esc / v_orb - math.sqrt(2)) < 1e-6, \
            f"Escape velocity ratio mismatch: {v_esc/v_orb} vs sqrt(2)"
        # Energy conserved over a step
        initial_e = sim.total_energy(sim.radius, sim.speed)
        for _ in range(10):
            sim.step(10.0)
        final_e = sim.total_energy(sim.radius, sim.speed)
        assert abs(final_e - initial_e) / abs(initial_e) < 0.001, \
            f"Energy not conserved: {initial_e} -> {final_e}"
        print("Orbital self-check OK (v_orb, v_esc, energy conservation verified)")

    elif mode == "induction":
        coil = ReferenceInductionCoil(B=0.5, A=0.01)
        # Flux = B A cos(theta)
        flux = coil.magnetic_flux(0.5, 0.01, 0.0)
        assert abs(flux - 0.005) < 1e-6, \
            f"Flux mismatch: {flux}"
        # EMF = -delta_flux / delta_t
        emf = coil.induced_emf(0.01, 0.02, 0.01)
        assert abs(emf - (-1.0)) < 1e-6, \
            f"EMF mismatch: {emf} vs -1.0"
        # Lenz direction
        assert coil.lenz_direction(0.01, 0.02) == "CCW", \
            "Lenz direction should be CCW for increasing flux"
        assert coil.lenz_direction(0.02, 0.01) == "CW", \
            "Lenz direction should be CW for decreasing flux"
        # Step updates state
        coil.magnet_position = -0.1
        coil.step(0.01)
        assert coil.state["flux"] != 0.0, "Flux should be non-zero after step"
        assert coil.state["emf"] != 0.0, "EMF should be non-zero after step"
        print("Induction self-check OK (flux, EMF, Lenz direction verified)")

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
    elif args.mode == "orbital":
        _run_orbital(args)
    elif args.mode == "induction":
        _run_induction(args)


if __name__ == "__main__":
    main()