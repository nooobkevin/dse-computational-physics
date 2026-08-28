"""Teacher-facing interactive app for the Quantum Physics toolkit.

Usage
-----
    uv run python units/07_quantum/teacher_app/main.py --mode well
    uv run python units/07_quantum/teacher_app/main.py --mode photoelectric
    uv run python units/07_quantum/teacher_app/main.py --mode de_broglie
    uv run python units/07_quantum/teacher_app/main.py --mode well --headless-selfcheck
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

from physics_core.quantum.wavefunctions import (
    H,
    M_E,
    ReferenceQuantumWell,
)
from physics_core.quantum.photoelectric import E_CHARGE, PhotoElectric

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720
WIN_NAME = "Quantum Physics Teacher Demo"
FPS = 30

# Colours (BGR)
COLOR_AXIS = (100, 100, 100)
COLOR_TEXT = (255, 255, 255)
COLOR_LEVEL = (0, 200, 255)  # cyan
COLOR_LEVEL_FILL = (0, 100, 150)
COLOR_PROB = (0, 255, 100)  # green
COLOR_TRANSITION = (0, 100, 255)  # orange
COLOR_PHOTON = (0, 200, 255)
COLOR_KE = (0, 255, 100)
COLOR_STOPPING = (0, 100, 255)
COLOR_DE_BROGLIE = (0, 200, 255)
COLOR_GRID = (50, 50, 50)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Quantum Physics teacher demo app")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["well", "photoelectric", "de_broglie"],
        help="Demo mode",
    )
    parser.add_argument(
        "--headless-selfcheck",
        action="store_true",
        help="Run a few frames without opening a window, then exit",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Graph drawing utility
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
# Well mode
# ---------------------------------------------------------------------------


def _run_well(args: argparse.Namespace) -> None:
    """Infinite square well: energy levels, probability densities, transitions."""
    L = 1e-10  # 1 Å
    well = ReferenceQuantumWell(L=L, m=M_E)

    # Pre-compute energy levels for n=1..6
    n_max = 6
    energies = [well.energy_level(n) for n in range(1, n_max + 1)]
    e_max = max(energies) * 1.2

    # Pre-compute probability density curves
    n_steps = 200
    dx = L / n_steps
    prob_curves: List[List[Tuple[float, float]]] = []
    for n in range(1, n_max + 1):
        curve: List[Tuple[float, float]] = []
        for i in range(n_steps + 1):
            x = i * dx
            curve.append((x, well.probability_density(x, n)))
        prob_curves.append(curve)

    selected_n = 1
    show_transition = False
    transition_from = 1
    transition_to = 2

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # ---- Left: energy level diagram ----
        level_region = (20, 20, 500, 680)
        rx, ry, rw, rh = level_region
        cv2.rectangle(canvas, (rx, ry), (rx + rw, ry + rh), COLOR_AXIS, 1)
        cv2.putText(canvas, "Energy Levels", (rx + 5, ry + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        # Draw well walls
        wall_left = rx + 80
        wall_right = rx + rw - 40
        well_top = ry + 40
        well_bottom = ry + rh - 40
        well_height = well_bottom - well_top

        # Well walls
        cv2.line(canvas, (wall_left, well_top), (wall_left, well_bottom), COLOR_TEXT, 2)
        cv2.line(canvas, (wall_right, well_top), (wall_right, well_bottom), COLOR_TEXT, 2)
        cv2.line(canvas, (wall_left, well_bottom), (wall_right, well_bottom), COLOR_TEXT, 1)

        # Energy levels
        for n_idx in range(n_max):
            n = n_idx + 1
            e_frac = energies[n_idx] / e_max
            level_y = int(well_bottom - e_frac * well_height)

            is_selected = (n == selected_n)
            color = COLOR_LEVEL if not is_selected else (0, 255, 255)
            thickness = 3 if is_selected else 1

            cv2.line(canvas, (wall_left, level_y), (wall_right, level_y), color, thickness)
            label = f"n={n}  E={energies[n_idx]:.2e}J"
            cv2.putText(canvas, label, (wall_right + 5, level_y + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1)

            # Probability density overlay for selected level
            if is_selected:
                prob_curve = prob_curves[n_idx]
                max_prob = max(p[1] for p in prob_curve)
                if max_prob > 0:
                    prob_width = wall_right - wall_left
                    prob_pts = []
                    for px, p_val in prob_curve:
                        px_screen = int(wall_left + (px / L) * prob_width)
                        p_norm = p_val / max_prob
                        py_screen = int(level_y - p_norm * 40)
                        prob_pts.append((px_screen, py_screen))
                    pts_arr = np.array(prob_pts, dtype=np.int32)
                    if len(pts_arr) >= 2:
                        cv2.polylines(canvas, [pts_arr], False, COLOR_PROB, 2, cv2.LINE_AA)

        # Transition arrow
        if show_transition:
            t_from_y = int(well_bottom - (energies[transition_from - 1] / e_max) * well_height)
            t_to_y = int(well_bottom - (energies[transition_to - 1] / e_max) * well_height)
            mid_x = (wall_left + wall_right) // 2
            cv2.arrowedLine(canvas, (mid_x, t_from_y), (mid_x, t_to_y), COLOR_TRANSITION, 2, tipLength=0.15)
            delta_e = well.transition_energy(transition_from, transition_to)
            lam = well.transition_wavelength(transition_from, transition_to)
            info = f"ΔE = {abs(delta_e):.2e} J, λ = {lam:.2e} m"
            cv2.putText(canvas, info, (rx + 5, ry + rh - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TRANSITION, 1)

        # ---- Right: probability density graph ----
        graph_region = (540, 20, 720, 680)
        prob_points = prob_curves[selected_n - 1]
        draw_graph(
            canvas,
            graph_region,
            prob_points,
            COLOR_PROB,
            x_label="x (m)",
            y_label="|ψ|²",
            title=f"|ψ_{selected_n}(x)|²",
        )

        # ---- Info ----
        info_lines = [
            f"L = {L:.1e} m, m = {M_E:.2e} kg",
            f"Selected n = {selected_n}",
            f"E_{selected_n} = {energies[selected_n-1]:.2e} J",
            "",
            "Keys: 1-6 select level",
            "t: toggle transition arrow",
            "ESC: exit",
        ]
        for i, line in enumerate(info_lines):
            cv2.putText(canvas, line, (10, CANVAS_H - 160 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break
        elif ord("1") <= key <= ord(str(n_max)):
            selected_n = key - ord("0")
        elif key == ord("t"):
            show_transition = not show_transition
            if show_transition:
                transition_from = selected_n
                transition_to = min(selected_n + 1, n_max)

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Photoelectric mode
# ---------------------------------------------------------------------------


def _run_photoelectric(args: argparse.Namespace) -> None:
    """Photoelectric effect: E=hf, work function, stopping potential."""
    phi_eV = 2.0  # work function in eV
    phi = phi_eV * E_CHARGE
    pe = PhotoElectric(work_function=phi)
    f0 = pe.threshold_frequency()

    # Frequency range for display
    f_min = 0.0
    f_max = 3.0 * f0
    n_points = 300

    # Pre-compute curves
    freqs = [f_min + (f_max - f_min) * i / n_points for i in range(n_points + 1)]
    ke_curve = [(f, pe.max_ke_eV(f)) for f in freqs]
    stopping_curve = [(f, pe.stopping_potential(f)) for f in freqs]

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # ---- KE vs frequency graph ----
        graph_region = (40, 40, 800, 600)
        draw_graph(
            canvas,
            graph_region,
            ke_curve,
            COLOR_KE,
            x_label="Frequency f (Hz)",
            y_label="K_max (eV)",
            title="Photoelectric Effect: K_max vs f",
            x_range=(f_min, f_max),
            y_range=(0, max(p[1] for p in ke_curve) * 1.1),
        )

        # Mark threshold frequency
        rx, ry, rw, rh = graph_region
        margin = 35
        gx = rx + margin
        gy = ry + margin
        gw = rw - 2 * margin
        gh = rh - 2 * margin
        y_range_vals = (0, max(p[1] for p in ke_curve) * 1.1)
        y_min_g, y_max_g = y_range_vals
        f0_px = int(gx + (f0 - f_min) / (f_max - f_min) * gw)
        cv2.line(canvas, (f0_px, gy), (f0_px, gy + gh), COLOR_AXIS, 1, cv2.LINE_AA)
        cv2.putText(canvas, f"f0 = {f0:.2e} Hz", (f0_px + 5, gy + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1)

        # ---- Info panel ----
        info_lines = [
            f"Work function φ = {phi_eV:.1f} eV",
            f"Threshold f0 = {f0:.2e} Hz",
            f"Planck constant h = {H:.2e} J·s",
            "",
            "Physics: K_max = hf - φ",
            "Stopping potential V0 = K_max / e",
            "",
            "ESC: exit",
        ]
        for i, line in enumerate(info_lines):
            cv2.putText(canvas, line, (860, 40 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# de Broglie mode
# ---------------------------------------------------------------------------


def _run_de_broglie(args: argparse.Namespace) -> None:
    """de Broglie wavelength: λ = h/p, λ vs velocity."""
    well = ReferenceQuantumWell()

    # Mass options
    masses = {
        "electron": M_E,
        "proton": 1.6726219e-27,
        "neutron": 1.6749275e-27,
    }
    selected_particle = "electron"
    m = masses[selected_particle]

    # Velocity range
    v_min = 0.0
    v_max = 1.0e7  # m/s
    n_points = 300

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Compute curve
        velocities = [v_min + (v_max - v_min) * i / n_points for i in range(n_points + 1)]
        wavelengths = []
        for v in velocities:
            if v > 0:
                p = m * v
                lam = well.de_broglie_wavelength(p)
                wavelengths.append(lam)
            else:
                wavelengths.append(0.0)

        curve = [(v, lam) for v, lam in zip(velocities, wavelengths) if lam > 0]

        # ---- λ vs v graph ----
        graph_region = (40, 40, 800, 600)
        draw_graph(
            canvas,
            graph_region,
            curve,
            COLOR_DE_BROGLIE,
            x_label="Velocity v (m/s)",
            y_label="Wavelength λ (m)",
            title=f"de Broglie Wavelength: λ = h/p  ({selected_particle})",
        )

        # ---- Info panel ----
        info_lines = [
            f"Particle: {selected_particle}",
            f"Mass: {m:.2e} kg",
            f"h = {H:.2e} J·s",
            "",
            "λ = h / p = h / (mv)",
            "",
            "Keys: e=electron, p=proton, n=neutron",
            "ESC: exit",
        ]
        for i, line in enumerate(info_lines):
            cv2.putText(canvas, line, (860, 40 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break
        elif key == ord("e"):
            selected_particle = "electron"
            m = masses["electron"]
        elif key == ord("p"):
            selected_particle = "proton"
            m = masses["proton"]
        elif key == ord("n"):
            selected_particle = "neutron"
            m = masses["neutron"]

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Headless self-check
# ---------------------------------------------------------------------------


def _headless_selfcheck(mode: str) -> None:
    """Run a few frames of the given mode without opening a window.

    This is used for CI / no-display testing.
    """
    if mode == "well":
        well = ReferenceQuantumWell(L=1e-10, m=M_E)
        # Check energy levels
        e1 = well.energy_level(1)
        e2 = well.energy_level(2)
        assert e2 == 4.0 * e1, f"E2 should be 4*E1: E1={e1}, E2={e2}"
        # Check wavefunction at centre
        psi = well.wavefunction(well.L / 2.0, 1)
        expected = math.sqrt(2.0 / well.L)
        assert abs(psi - expected) < 1e-10, f"ψ_1(L/2)={psi}, expected={expected}"
        # Check probability density integrates to ~1
        n_steps = 500
        dx = well.L / n_steps
        total = sum(well.probability_density((i + 0.5) * dx, 1) * dx for i in range(n_steps))
        assert abs(total - 1.0) < 0.02, f"∫|ψ|² dx = {total}, expected ~1"
        print("Quantum Well self-check OK")

    elif mode == "photoelectric":
        phi = 2.0 * E_CHARGE
        pe = PhotoElectric(work_function=phi)
        f0 = pe.threshold_frequency()
        assert f0 == phi / H, f"f0={f0}, expected {phi/H}"
        f_above = f0 * 2.0
        ke = pe.max_kinetic_energy(f_above)
        assert ke > 0, f"KE should be positive above threshold, got {ke}"
        f_below = f0 * 0.5
        ke_below = pe.max_kinetic_energy(f_below)
        assert ke_below == 0.0, f"KE should be zero below threshold, got {ke_below}"
        print("Photoelectric self-check OK")

    elif mode == "de_broglie":
        well = ReferenceQuantumWell()
        p = 1.0e-24
        lam = well.de_broglie_wavelength(p)
        assert lam == H / p, f"λ={lam}, expected {H/p}"
        # Check that heavier particle -> shorter wavelength
        p2 = 2.0e-24
        lam2 = well.de_broglie_wavelength(p2)
        assert lam2 < lam, "Higher momentum should give shorter wavelength"
        print("de Broglie self-check OK")

    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    if args.headless_selfcheck:
        _headless_selfcheck(args.mode)
        return

    if args.mode == "well":
        _run_well(args)
    elif args.mode == "photoelectric":
        _run_photoelectric(args)
    elif args.mode == "de_broglie":
        _run_de_broglie(args)


if __name__ == "__main__":
    main()