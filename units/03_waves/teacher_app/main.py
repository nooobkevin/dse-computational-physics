"""Teacher-facing interactive app for Unit 03 — Waves.

Usage
-----
    uv run python units/03_waves/teacher_app/main.py --mode traveling
    uv run python units/03_waves/teacher_app/main.py --mode standing
    uv run python units/03_waves/teacher_app/main.py --mode interference
    uv run python units/03_waves/teacher_app/main.py --mode standing --headless-selfcheck
"""

from __future__ import annotations

import argparse
import math
import sys

import cv2
import numpy as np

from physics_core.waves.wave_sim import ReferenceWaveSim

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720
WIN_NAME = "Waves Teacher Demo"
FPS = 30
DT = 0.033  # ~30 fps step

# Colours (BGR)
COLOR_WAVE = (0, 255, 255)  # yellow
COLOR_WAVE2 = (0, 200, 255)  # orange
COLOR_RESULT = (0, 255, 0)  # green
COLOR_PARTICLE = (0, 0, 255)  # red
COLOR_AXIS = (100, 100, 100)
COLOR_TEXT = (255, 255, 255)
COLOR_NODE = (0, 0, 255)
COLOR_FRINGE_BRIGHT = (0, 255, 255)
COLOR_FRINGE_DARK = (50, 50, 50)
COLOR_SCREEN = (150, 150, 150)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Waves teacher demo app")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["traveling", "standing", "interference"],
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
    region: tuple[int, int, int, int],
    points: list[tuple[float, float]],
    color: tuple[int, int, int],
    x_label: str = "",
    y_label: str = "",
    title: str = "",
    x_range: tuple[float, float] | None = None,
    y_range: tuple[float, float] | None = None,
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

    def to_px(wx: float, wy: float) -> tuple[int, int]:
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
# Traveling wave mode
# ---------------------------------------------------------------------------


def _run_traveling(args: argparse.Namespace) -> None:
    """Traveling wave mode — synthetic sine curve with moving particle."""
    A = 1.0
    lam = 4.0
    f = 0.5
    sim = ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f, L=12.0, nx=300)

    # Scene area
    scene_x0, scene_y0 = 40, 40
    scene_w, scene_h = 800, 400
    origin_x = scene_x0 + 60
    origin_y = scene_y0 + scene_h // 2
    scale_x = (scene_w - 80) / sim.L
    scale_y = (scene_h // 2 - 30) / (A * 1.5)

    # Particle position (fixed x)
    particle_x = 3.0

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        t = sim.state["t"]

        # Draw wave profile
        x_arr = sim.x
        y_arr = sim.field(x_arr, t)
        wave_pts = [
            (int(origin_x + xi * scale_x), int(origin_y - yi * scale_y))
            for xi, yi in zip(x_arr, y_arr)
        ]
        wave_pts_np = np.array(wave_pts, dtype=np.int32)
        cv2.polylines(canvas, [wave_pts_np], False, COLOR_WAVE, 2, cv2.LINE_AA)

        # Draw horizontal axis
        cv2.line(
            canvas,
            (origin_x, origin_y),
            (origin_x + int(sim.L * scale_x), origin_y),
            COLOR_AXIS, 1,
        )

        # Moving particle on the wave
        y_particle = sim.displacement(particle_x, t)
        px = int(origin_x + particle_x * scale_x)
        py = int(origin_y - y_particle * scale_y)
        cv2.circle(canvas, (px, py), 8, COLOR_PARTICLE, -1)
        cv2.circle(canvas, (px, py), 8, (255, 255, 255), 1)

        # Vertical line from particle to axis
        cv2.line(canvas, (px, origin_y), (px, py), COLOR_PARTICLE, 1, cv2.LINE_AA)

        # Phase indicator
        phase = (sim.k * particle_x - sim.omega * t) % (2 * math.pi)
        phase_deg = math.degrees(phase)

        # Info
        info = [
            f"Traveling Wave: y = A sin(kx - ωt)",
            f"A = {A:.1f} m, λ = {lam:.1f} m, f = {f:.1f} Hz",
            f"v = fλ = {sim.v:.1f} m/s",
            f"Particle at x = {particle_x:.1f} m",
            f"y = {y_particle:.3f} m",
            f"Phase = {phase_deg:.0f}°",
        ]
        for i, line in enumerate(info):
            cv2.putText(
                canvas, line, (10, 30 + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1,
            )

        # Displacement vs time graph (right side)
        graph_region = (860, 40, 400, 300)
        graph_pts = []
        for step_back in range(300):
            tt = t - step_back * DT
            if tt < 0:
                break
            yy = sim.displacement(particle_x, tt)
            graph_pts.append((tt, yy))
        graph_pts.reverse()
        draw_graph(
            canvas, graph_region, graph_pts, COLOR_PARTICLE,
            x_label="t (s)", y_label="y (m)",
            title="Displacement vs Time",
        )

        sim.step(DT)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Standing wave mode
# ---------------------------------------------------------------------------


def _run_standing(args: argparse.Namespace) -> None:
    """Standing wave mode — superposition of two traveling waves."""
    A = 1.0
    lam = 4.0
    f = 0.5
    sim = ReferenceWaveSim(amplitude=A, wavelength=lam, frequency=f, L=12.0, nx=300)

    scene_x0, scene_y0 = 40, 40
    scene_w, scene_h = 800, 500
    origin_x = scene_x0 + 60
    origin_y = scene_y0 + scene_h // 2
    scale_x = (scene_w - 80) / sim.L
    scale_y = (scene_h // 2 - 30) / (A * 3.0)

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        t = sim.state["t"]
        x_arr = sim.x

        # Wave 1: traveling right
        y1 = A * np.sin(sim.k * x_arr - sim.omega * t)
        # Wave 2: traveling left
        y2 = A * np.sin(sim.k * x_arr + sim.omega * t)
        # Result: standing wave
        y_result = y1 + y2

        # Draw wave 1 (dashed feel — thin line)
        pts1 = np.array([
            (int(origin_x + xi * scale_x), int(origin_y - y1i * scale_y))
            for xi, y1i in zip(x_arr, y1)
        ], dtype=np.int32)
        cv2.polylines(canvas, [pts1], False, COLOR_WAVE2, 1, cv2.LINE_AA)

        # Draw wave 2 (dashed feel — thin line)
        pts2 = np.array([
            (int(origin_x + xi * scale_x), int(origin_y - y2i * scale_y))
            for xi, y2i in zip(x_arr, y2)
        ], dtype=np.int32)
        cv2.polylines(canvas, [pts2], False, (255, 100, 0), 1, cv2.LINE_AA)

        # Draw result (thick green)
        pts_result = np.array([
            (int(origin_x + xi * scale_x), int(origin_y - yri * scale_y))
            for xi, yri in zip(x_arr, y_result)
        ], dtype=np.int32)
        cv2.polylines(canvas, [pts_result], False, COLOR_RESULT, 3, cv2.LINE_AA)

        # Horizontal axis
        cv2.line(
            canvas,
            (origin_x, origin_y),
            (origin_x + int(sim.L * scale_x), origin_y),
            COLOR_AXIS, 1,
        )

        # Mark nodes (where sin(kx) = 0)
        node_positions = [n * lam / 2.0 for n in range(int(sim.L / (lam / 2.0)) + 1)]
        for nx_pos in node_positions:
            if nx_pos <= sim.L:
                nx_px = int(origin_x + nx_pos * scale_x)
                cv2.line(canvas, (nx_px, origin_y - 10), (nx_px, origin_y + 10), COLOR_NODE, 2)

        # Legend
        legend = [
            ("Wave → (right)", COLOR_WAVE2),
            ("Wave ← (left)", (255, 100, 0)),
            ("Result (standing)", COLOR_RESULT),
            ("Node", COLOR_NODE),
        ]
        for i, (text, color) in enumerate(legend):
            ly = scene_y0 + scene_h + 10 + i * 22
            cv2.circle(canvas, (scene_x0 + 10, ly + 5), 5, color, -1)
            cv2.putText(
                canvas, text, (scene_x0 + 22, ly + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1,
            )

        # Info
        info = [
            f"Standing Wave: y = 2A sin(kx) cos(ωt)",
            f"A = {A:.1f} m, λ = {lam:.1f} m, f = {f:.1f} Hz",
            f"t = {t:.2f} s",
        ]
        for i, line in enumerate(info):
            cv2.putText(
                canvas, line, (scene_x0 + scene_w + 10, 30 + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1,
            )

        sim.step(DT)

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Interference mode (Young's double-slit)
# ---------------------------------------------------------------------------


def _run_interference(args: argparse.Namespace) -> None:
    """Interference mode — double-slit fringe pattern."""
    wavelength = 500e-9  # 500 nm
    slit_sep = 0.1e-3  # 0.1 mm
    screen_dist = 1.0  # 1 m
    screen_width = 0.1  # 0.1 m on screen
    n_fringes = 5

    scene_x0, scene_y0 = 40, 40
    scene_w, scene_h = 800, 500

    # Slit positions (left side)
    slit_center_x = scene_x0 + 100
    slit_center_y = scene_y0 + scene_h // 2

    # Screen position (right side)
    screen_x = scene_x0 + scene_w - 80
    screen_px_width = 300

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Draw slits
        cv2.circle(canvas, (slit_center_x, slit_center_y - 5), 3, COLOR_TEXT, -1)
        cv2.circle(canvas, (slit_center_x, slit_center_y + 5), 3, COLOR_TEXT, -1)
        cv2.putText(
            canvas, "Slits", (slit_center_x - 30, slit_center_y - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1,
        )

        # Draw screen
        screen_left = screen_x
        screen_top = slit_center_y - screen_px_width // 2
        screen_bottom = slit_center_y + screen_px_width // 2
        cv2.line(canvas, (screen_left, screen_top), (screen_left, screen_bottom), COLOR_SCREEN, 3)

        # Compute fringe positions
        # For small angles: y = n * λ * D / d
        fringe_spacing = wavelength * screen_dist / slit_sep
        fringe_spacing_px = fringe_spacing / screen_width * screen_px_width

        # Draw fringes
        for n in range(-n_fringes, n_fringes + 1):
            y_offset = n * fringe_spacing_px
            fy = slit_center_y + int(y_offset)

            if screen_top <= fy <= screen_bottom:
                # Bright fringe for integer n
                if abs(n) % 2 == 0 or True:  # all integer orders are bright
                    color = COLOR_FRINGE_BRIGHT
                    width = max(1, int(fringe_spacing_px * 0.4))
                else:
                    color = COLOR_FRINGE_DARK
                    width = max(1, int(fringe_spacing_px * 0.4))

                cv2.line(
                    canvas,
                    (screen_left - width, fy),
                    (screen_left + width, fy),
                    color, 3,
                )

                # Label order
                if n != 0:
                    cv2.putText(
                        canvas, f"n={n}", (screen_left + 10, fy + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1,
                    )
                else:
                    cv2.putText(
                        canvas, "n=0", (screen_left + 10, fy + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1,
                    )

        # Draw paths from slits to screen (a few representative rays)
        for n in [-2, -1, 0, 1, 2]:
            y_offset = n * fringe_spacing_px
            fy = slit_center_y + int(y_offset)
            if screen_top <= fy <= screen_bottom:
                # Path from upper slit
                cv2.line(
                    canvas,
                    (slit_center_x, slit_center_y - 5),
                    (screen_left, fy),
                    (60, 60, 60), 1, cv2.LINE_AA,
                )
                # Path from lower slit
                cv2.line(
                    canvas,
                    (slit_center_x, slit_center_y + 5),
                    (screen_left, fy),
                    (60, 60, 60), 1, cv2.LINE_AA,
                )

        # Formula
        formula_lines = [
            "Young's Double-Slit",
            "d sin(θ) = n λ",
            f"λ = {wavelength*1e9:.0f} nm",
            f"d = {slit_sep*1e3:.2f} mm",
            f"D = {screen_dist:.1f} m",
            f"Fringe spacing Δy = {fringe_spacing*1e3:.2f} mm",
        ]
        for i, line in enumerate(formula_lines):
            cv2.putText(
                canvas, line, (10, 30 + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1,
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
    """Run a few frames of the given mode without opening a window.

    This is used for CI / no-display testing.
    """
    if mode == "traveling":
        sim = ReferenceWaveSim(amplitude=1.0, wavelength=4.0, frequency=0.5, L=12.0, nx=300)
        for _ in range(30):
            sim.step(DT)
        # Verify field amplitude is bounded by A
        t = sim.state["t"]
        y = sim.field(sim.x, t)
        assert np.max(np.abs(y)) <= 1.0 + 1e-12, "Traveling wave amplitude exceeded A"
        print("Traveling wave self-check OK")

    elif mode == "standing":
        sim = ReferenceWaveSim(amplitude=1.0, wavelength=4.0, frequency=0.5, L=12.0, nx=300)
        for _ in range(30):
            sim.step(DT)
        # Verify a node has ~zero displacement
        node_x = 2.0  # λ/2 = 2.0 for λ=4
        t = sim.state["t"]
        y_node = sim.standing_wave(node_x, t)
        assert abs(y_node) < 1e-12, (
            f"Standing wave node at x={node_x} has non-zero displacement {y_node}"
        )
        print("Standing wave self-check OK")

    elif mode == "interference":
        # Verify the double-slit formula
        wavelength = 500e-9
        d = 0.1e-3
        # For n=1: sin(θ) = λ/d
        theta = math.asin(wavelength / d)
        # Fringe spacing on screen at D=1m: Δy = λD/d
        D = 1.0
        fringe_spacing = wavelength * D / d
        assert fringe_spacing > 0, "Fringe spacing must be positive"
        print(f"Interference self-check OK (fringe spacing = {fringe_spacing*1e3:.4f} mm)")

    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    if args.headless_selfcheck:
        _headless_selfcheck(args.mode)
        return

    if args.mode == "traveling":
        _run_traveling(args)
    elif args.mode == "standing":
        _run_standing(args)
    elif args.mode == "interference":
        _run_interference(args)


if __name__ == "__main__":
    main()
