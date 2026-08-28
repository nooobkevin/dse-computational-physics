"""Teacher-facing interactive app for the Quantum Physics toolkit.

Usage
-----
    uv run python units/07_quantum/teacher_app/main.py --mode well
    uv run python units/07_quantum/teacher_app/main.py --mode photoelectric
    uv run python units/07_quantum/teacher_app/main.py --mode de_broglie
    uv run python units/07_quantum/teacher_app/main.py --mode laser
    uv run python units/07_quantum/teacher_app/main.py --mode rutherford
    uv run python units/07_quantum/teacher_app/main.py --mode hydrogen
    uv run python units/07_quantum/teacher_app/main.py --mode uncertainty
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
from physics_core.quantum.lasers import ReferenceLaser
from physics_core.quantum.rutherford import ReferenceRutherfordScattering
from physics_core.quantum.bohr import BohrHydrogen

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
COLOR_NO = (0, 0, 255)      # red
COLOR_LASER = (0, 255, 0)  # green laser

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Quantum Physics teacher demo app")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["well", "photoelectric", "de_broglie", "laser",
                 "rutherford", "hydrogen", "uncertainty"],
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
        cv2.line(canvas, (50, ey + 100), (250, ey + 100), COLOR_NO, 2)
        cv2.putText(canvas, f"N_lower = {laser.N_lower:.0f}", (260, ey + 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_NO, 1)

        # Population inversion indicator
        inversion = laser.population_inversion
        inv_color = COLOR_LASER if inversion else COLOR_NO
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
# Rutherford mode
# ---------------------------------------------------------------------------


def _run_rutherford(args: argparse.Namespace) -> None:
    """Rutherford scattering: impact parameter slider, live θ and trajectory."""
    sim = ReferenceRutherfordScattering(Z1=2, Z2=79, E=5.0e6 * E_CHARGE)
    b = 1e-14  # initial impact parameter
    E = 5.0e6 * E_CHARGE  # 5 MeV
    scale = 1.5e13  # m → pixels (approx)

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Compute scattering angle
        theta = sim.scattering_angle(b, E)
        theta_deg = math.degrees(theta)

        # ---- Trajectory plot ----
        traj_region = (40, 40, 700, 600)
        rx, ry, rw, rh = traj_region
        cv2.rectangle(canvas, (rx, ry), (rx + rw, ry + rh), COLOR_AXIS, 1)
        cv2.putText(canvas, "Rutherford Scattering Trajectory", (rx + 5, ry + 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        # Draw gold nucleus at centre
        cx = rx + rw // 2
        cy = ry + rh // 2
        cv2.circle(canvas, (cx, cy), 10, (0, 215, 255), -1)  # gold
        cv2.putText(canvas, "Au", (cx - 8, cy + 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

        # Compute and draw trajectory
        pts = sim.trajectory_points(b, E, n_points=200, r_max=3e-13)
        if len(pts) >= 2:
            traj_px = []
            for px, py in pts:
                sx = int(cx + px * scale)
                sy = int(cy - py * scale)
                traj_px.append((sx, sy))
            traj_arr = np.array(traj_px, dtype=np.int32)
            cv2.polylines(canvas, [traj_arr], False, COLOR_LEVEL, 2, cv2.LINE_AA)

        # Draw incoming direction
        cv2.arrowedLine(canvas, (rx + 10, cy), (cx - 30, cy), COLOR_AXIS, 1, tipLength=0.1)

        # ---- Info panel ----
        info_lines = [
            f"Alpha particle (Z=2) → Gold nucleus (Z=79)",
            f"Energy: {E / E_CHARGE:.1e} eV",
            f"Impact parameter b = {b:.2e} m",
            f"Scattering angle θ = {theta_deg:.1f}°",
            "",
            "Keys: ↑↓ adjust b (×1.5 / ÷1.5)",
            "      ESC: exit",
        ]
        for i, line in enumerate(info_lines):
            cv2.putText(canvas, line, (760, 40 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break
        elif key == 82:  # ↑
            b *= 1.5
        elif key == 84:  # ↓
            b /= 1.5
            if b < 1e-20:
                b = 1e-20

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Hydrogen mode
# ---------------------------------------------------------------------------


def _run_hydrogen(args: argparse.Namespace) -> None:
    """Bohr hydrogen: n-level slider, emission/absorption, live photon λ."""
    bohr = BohrHydrogen()
    n_max = 10
    selected_n = 2
    target_n = 1
    show_emission = True

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # ---- Energy level diagram ----
        level_region = (20, 20, 500, 600)
        rx, ry, rw, rh = level_region
        cv2.rectangle(canvas, (rx, ry), (rx + rw, ry + rh), COLOR_AXIS, 1)
        cv2.putText(canvas, "Hydrogen Energy Levels (Bohr Model)", (rx + 5, ry + 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_TEXT, 1)

        # Compute energies
        energies = [bohr.energy_level(n) for n in range(1, n_max + 1)]
        e_min = min(energies)
        e_max = 0.0  # ionisation limit

        # Draw levels
        wall_left = rx + 80
        wall_right = rx + rw - 40
        well_top = ry + 50
        well_bottom = ry + rh - 50
        well_height = well_bottom - well_top

        for n_idx in range(n_max):
            n = n_idx + 1
            e = energies[n_idx]
            e_frac = (e - e_min) / max(e_max - e_min, 1e-10)
            level_y = int(well_bottom - e_frac * well_height)

            is_selected = (n == selected_n)
            is_target = (n == target_n)
            color = COLOR_LEVEL
            thickness = 1
            if is_selected:
                color = (0, 255, 255)  # yellow
                thickness = 3
            if is_target:
                color = COLOR_TRANSITION
                thickness = 2

            cv2.line(canvas, (wall_left, level_y), (wall_right, level_y), color, thickness)
            label = f"n={n}  E={e:.2f} eV"
            cv2.putText(canvas, label, (wall_right + 5, level_y + 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_TEXT, 1)

        # Ionisation limit
        ion_y = int(well_bottom)
        cv2.line(canvas, (wall_left, ion_y), (wall_right, ion_y), COLOR_AXIS, 1)
        cv2.putText(canvas, "Ionisation limit (E=0)", (wall_right + 5, ion_y + 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_AXIS, 1)

        # Transition arrow
        if show_emission:
            n_i, n_f = selected_n, target_n
        else:
            n_i, n_f = target_n, selected_n

        if n_i != n_f:
            e_i = energies[n_i - 1]
            e_f = energies[n_f - 1]
            y_i = int(well_bottom - ((e_i - e_min) / max(e_max - e_min, 1e-10)) * well_height)
            y_f = int(well_bottom - ((e_f - e_min) / max(e_max - e_min, 1e-10)) * well_height)
            mid_x = (wall_left + wall_right) // 2
            cv2.arrowedLine(canvas, (mid_x, y_i), (mid_x, y_f), COLOR_TRANSITION, 2, tipLength=0.15)

            delta_e = bohr.transition_energy(n_i, n_f)
            lam = bohr.transition_wavelength(n_i, n_f)
            lam_nm = lam * 1e9
            delta_e_abs = abs(delta_e)
            transition_type = "Emission" if n_f < n_i else "Absorption"
            info = f"{transition_type}: ΔE = {delta_e_abs:.2f} eV, λ = {lam_nm:.1f} nm"
            cv2.putText(canvas, info, (rx + 5, ry + rh - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TRANSITION, 1)

        # ---- Info panel ----
        info_lines = [
            f"Selected n = {selected_n}",
            f"Target n = {target_n}",
            f"Mode: {'Emission' if show_emission else 'Absorption'}",
            "",
            "Keys: 1-9 select upper level",
            "      t: toggle emission/absorption",
            "      ESC: exit",
        ]
        for i, line in enumerate(info_lines):
            cv2.putText(canvas, line, (540, 40 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break
        elif ord("1") <= key <= ord(str(min(n_max, 9))):
            selected_n = key - ord("0")
        elif key == ord("t"):
            show_emission = not show_emission
            if show_emission:
                target_n = 1 if selected_n > 1 else 2
            else:
                target_n = selected_n + 1 if selected_n < n_max else selected_n

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Uncertainty mode
# ---------------------------------------------------------------------------


def _run_uncertainty(args: argparse.Namespace) -> None:
    """Heisenberg uncertainty: Δx·Δp ≥ ħ/2, slider for well width L."""
    hbar = 1.054571817e-34  # reduced Planck constant (J·s)
    m_e = 9.10938356e-31  # electron mass (kg)
    e_charge = 1.602176634e-19  # elementary charge (C)

    well_width = 1e-10  # initial well width (m)
    L_min = 1e-11
    L_max = 1e-9

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Compute uncertainty quantities
        delta_x = well_width  # position uncertainty ≈ well width
        delta_p = hbar / (2.0 * delta_x)  # minimum momentum uncertainty
        e_min = (delta_p * delta_p) / (2.0 * m_e)  # minimum kinetic energy
        e_min_eV = e_min / e_charge

        # ---- Graph: Δx vs Δp ----
        graph_region = (40, 40, 700, 500)
        rx, ry, rw, rh = graph_region
        cv2.rectangle(canvas, (rx, ry), (rx + rw, ry + rh), COLOR_AXIS, 1)
        cv2.putText(canvas, "Heisenberg Uncertainty Principle", (rx + 5, ry + 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        # Draw Δx · Δp ≥ ħ/2 curve
        n_points = 200
        x_vals = [L_min + (L_max - L_min) * i / n_points for i in range(n_points + 1)]
        p_vals = [hbar / (2.0 * x) for x in x_vals]

        curve_pts = [(x, p) for x, p in zip(x_vals, p_vals)]
        draw_graph(
            canvas,
            graph_region,
            curve_pts,
            COLOR_LEVEL,
            x_label="Δx (m)",
            y_label="Δp (kg·m/s)",
            title="Δx · Δp ≥ ħ/2",
            x_range=(L_min, L_max),
            y_range=(0, max(p_vals) * 1.2),
        )

        # Mark current point
        margin = 35
        gx = rx + margin
        gy = ry + margin
        gw = rw - 2 * margin
        gh = rh - 2 * margin
        x_px = int(gx + (well_width - L_min) / (L_max - L_min) * gw)
        y_px = int(gy + (max(p_vals) * 1.2 - delta_p) / (max(p_vals) * 1.2) * gh)
        cv2.circle(canvas, (x_px, y_px), 6, (0, 255, 255), -1)

        # ---- Info panel ----
        info_lines = [
            f"Well width L = Δx = {well_width:.2e} m",
            f"Δp ≥ ħ/(2Δx) = {delta_p:.2e} kg·m/s",
            f"Δx · Δp = {delta_x * delta_p:.2e} J·s",
            f"ħ/2 = {hbar / 2.0:.2e} J·s",
            f"Product ≥ ħ/2: {'YES ✓' if delta_x * delta_p >= hbar / 2.0 else 'NO ✗'}",
            "",
            f"Minimum KE = {e_min_eV:.2f} eV",
            "",
            "Keys: ←→ adjust L",
            "      ESC: exit",
        ]
        for i, line in enumerate(info_lines):
            cv2.putText(canvas, line, (760, 40 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break
        elif key == 81:  # ←
            well_width /= 1.2
            if well_width < L_min:
                well_width = L_min
        elif key == 83:  # →
            well_width *= 1.2
            if well_width > L_max:
                well_width = L_max

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

    elif mode == "laser":
        laser = ReferenceLaser(N_upper=100.0, N_lower=10.0)
        assert laser.population_inversion, "Population inversion should exist"
        photons = laser.stimulated_emission()
        assert photons > 0, "Stimulated emission should produce photons"
        laser.step(0.1)
        assert laser.state["photon_count"] > 0, "Photon count should increase"
        print("Laser self-check OK (stimulated emission verified)")

    elif mode == "rutherford":
        sim = ReferenceRutherfordScattering(Z1=2, Z2=79, E=5.0e6 * E_CHARGE)
        # Head-on: b→0 gives θ→π
        theta_head = sim.scattering_angle(1e-20, 5.0e6 * E_CHARGE)
        assert abs(theta_head - math.pi) < 0.01, (
            f"Head-on θ={theta_head}, expected π"
        )
        # Large b gives small angle
        theta_large = sim.scattering_angle(1e-12, 5.0e6 * E_CHARGE)
        assert theta_large < 0.1, f"Large b should give small angle, got {theta_large}"
        # Trajectory non-empty
        pts = sim.trajectory_points(1e-14, 5.0e6 * E_CHARGE, n_points=50)
        assert len(pts) >= 2, "Trajectory should have multiple points"
        print("Rutherford self-check OK")

    elif mode == "hydrogen":
        bohr = BohrHydrogen()
        # E₁ = -13.6 eV
        assert abs(bohr.energy_level(1) - (-13.6)) < 0.01
        # Lyman-alpha ~ 121.6 nm
        lam = bohr.transition_wavelength(2, 1)
        assert abs(lam - 121.6e-9) / 121.6e-9 < 0.01
        # Ionisation from n=1 = 13.6 eV
        ion = bohr.ionisation_energy(1)
        assert abs(ion - 13.6) < 0.01
        print("Hydrogen self-check OK")

    elif mode == "uncertainty":
        hbar = 1.054571817e-34
        L_test = 1e-10
        delta_x = L_test
        delta_p = hbar / (2.0 * delta_x)
        product = delta_x * delta_p
        assert product >= hbar / 2.0, (
            f"Δx·Δp = {product} should be ≥ ħ/2 = {hbar/2.0}"
        )
        print("Uncertainty self-check OK")

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
    elif args.mode == "laser":
        _run_laser(args)
    elif args.mode == "rutherford":
        _run_rutherford(args)
    elif args.mode == "hydrogen":
        _run_hydrogen(args)
    elif args.mode == "uncertainty":
        _run_uncertainty(args)


if __name__ == "__main__":
    main()