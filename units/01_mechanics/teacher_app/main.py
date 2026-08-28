"""Teacher-facing interactive app (M3) for the mechanics toolkit.

Usage
-----
    uv run python units/01_mechanics/teacher_app/main.py --mode pendulum
    uv run python units/01_mechanics/teacher_app/main.py --mode circular
    uv run python units/01_mechanics/teacher_app/main.py --mode projectile
    uv run python units/01_mechanics/teacher_app/main.py --mode circular --headless-selfcheck
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
from collections import deque
from typing import Deque, List, Optional, Tuple

import cv2
import numpy as np

from physics_core.errors import percent_error, sig_figs
from physics_core.mechanics.circular import CircularMotion
from physics_core.mechanics.pendulum import ReferencePendulumSim
from physics_core.mechanics.projectile import ReferenceProjectileSim

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720
WIN_NAME = "Physics Teacher Demo"
FPS = 30
DT = 0.033  # ~30 fps step
MAX_DATA_POINTS = 900  # ~30 seconds at 30 fps
MAX_FAIL_FRAMES = 30

# Colours (BGR)
COLOR_TRACKED = (0, 255, 0)  # green
COLOR_IDEAL = (0, 255, 255)  # yellow
COLOR_AXIS = (100, 100, 100)
COLOR_TEXT = (255, 255, 255)
COLOR_PIVOT = (0, 0, 255)  # red
COLOR_BOB = (0, 255, 0)
COLOR_STRING = (200, 200, 200)
COLOR_VECTOR = (255, 150, 0)  # orange
COLOR_VX = (255, 0, 0)  # blue
COLOR_VY = (0, 0, 255)  # red
COLOR_TRACE = (200, 200, 0)
COLOR_CENTER = (0, 0, 255)
COLOR_RADIUS = (255, 255, 255)
COLOR_CENTRIPETAL = (0, 150, 255)
COLOR_TRAJECTORY = (0, 255, 255)
COLOR_PROJECTILE = (0, 200, 255)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Physics teacher demo app")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["pendulum", "circular", "projectile"],
        help="Demo mode",
    )
    parser.add_argument(
        "--length",
        type=float,
        default=1.0,
        help="Pendulum length / circle radius (m)",
    )
    parser.add_argument(
        "--device",
        type=int,
        default=0,
        help="Camera device index (default: 0)",
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
    """Draw a 2D graph into a rectangular region of the canvas.

    Parameters
    ----------
    canvas : np.ndarray
        The full canvas (modified in-place).
    region : (rx, ry, rw, rh)
        Rectangle in pixels.
    points : list of (x, y)
        Data points in world coordinates.
    color : (B, G, R)
        Line colour.
    """
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

    # Padding
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

    # Axes at origin if visible
    if y_min <= 0 <= y_max:
        _, ay = to_px(0, 0)
        cv2.line(canvas, (gx, ay), (gx + gw, ay), COLOR_AXIS, 1)
    if x_min <= 0 <= x_max:
        ax, _ = to_px(0, 0)
        cv2.line(canvas, (ax, gy), (ax, gy + gh), COLOR_AXIS, 1)

    # Polyline
    pts = np.array([to_px(x, y) for x, y in points], dtype=np.int32)
    if len(pts) >= 2:
        cv2.polylines(canvas, [pts], False, color, 1, cv2.LINE_AA)

    # Labels
    if title:
        cv2.putText(canvas, title, (rx + 5, ry + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
    if x_label:
        cv2.putText(canvas, x_label, (rx + rw - 100, ry + rh - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1)
    if y_label:
        cv2.putText(canvas, y_label, (rx + 4, ry + margin - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1)


# ---------------------------------------------------------------------------
# Pendulum helpers
# ---------------------------------------------------------------------------


def compute_theta(
    bob_px: Tuple[int, int], pivot_px: Tuple[int, int]
) -> float:
    """Angle from vertical (rad).  Zero = straight down, positive = right."""
    dx = bob_px[0] - pivot_px[0]
    dy = bob_px[1] - pivot_px[1]
    return math.atan2(dx, dy)


def estimate_period(
    times: List[float], thetas: List[float]
) -> Optional[float]:
    """Estimate period (s) from zero-crossings of theta."""
    zero_ts: List[float] = []
    for i in range(1, len(thetas)):
        if thetas[i - 1] * thetas[i] < 0:
            # Linear interpolation to zero
            t_frac = abs(thetas[i - 1]) / (abs(thetas[i - 1]) + abs(thetas[i]))
            zt = times[i - 1] + (times[i] - times[i - 1]) * t_frac
            zero_ts.append(zt)

    if len(zero_ts) < 3:
        return None

    intervals = [zero_ts[i + 1] - zero_ts[i] for i in range(len(zero_ts) - 1)]
    half_period = sum(intervals) / len(intervals)
    return half_period * 2.0


def draw_pendulum_scene(
    canvas: np.ndarray,
    pivot_px: Tuple[int, int],
    theta: float,
    length_px: float,
) -> None:
    """Draw a synthetic pendulum into the scene area."""
    px, py = pivot_px
    bx = int(px + length_px * math.sin(theta))
    by = int(py + length_px * math.cos(theta))
    # String
    cv2.line(canvas, (px, py), (bx, by), COLOR_STRING, 2)
    # Pivot
    cv2.circle(canvas, (px, py), 5, COLOR_PIVOT, -1)
    # Bob
    cv2.circle(canvas, (bx, by), 12, COLOR_BOB, -1)
    cv2.circle(canvas, (bx, by), 12, (255, 255, 255), 1)


# ---------------------------------------------------------------------------
# Circular motion drawing
# ---------------------------------------------------------------------------


def draw_circular_scene(
    canvas: np.ndarray,
    center_px: Tuple[int, int],
    sim: CircularMotion,
    radius_px: float,
    trace: Deque[Tuple[int, int]],
) -> None:
    """Draw the circular motion scene with vectors."""
    cx, cy = center_px
    theta = sim.angle
    r = sim.radius

    # Path circle
    cv2.circle(canvas, (cx, cy), int(radius_px), COLOR_AXIS, 1)

    # Dot position
    bx = int(cx + radius_px * math.cos(theta))
    by = int(cy - radius_px * math.sin(theta))  # y inverted

    # Trace
    trace.append((bx, by))
    trace_pts = np.array(list(trace), dtype=np.int32)
    if len(trace_pts) >= 2:
        cv2.polylines(canvas, [trace_pts], False, COLOR_TRACE, 1, cv2.LINE_AA)

    # Radius vector (center -> dot)
    cv2.line(canvas, (cx, cy), (bx, by), COLOR_RADIUS, 2)
    mid_x = (cx + bx) // 2
    mid_y = (cy + by) // 2
    cv2.putText(
        canvas, "r", (mid_x + 5, mid_y - 5),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_RADIUS, 1,
    )

    # Tangential velocity (perpendicular to radius, direction of motion)
    v = sim.tangential_speed
    v_scale = 20.0  # visual scaling
    # Direction: (-sin(theta), -cos(theta)) for CCW (y-inverted)
    vx_dir = -math.sin(theta)
    vy_dir = -math.cos(theta)
    vx_px = int(bx + vx_dir * v * v_scale)
    vy_px = int(by + vy_dir * v * v_scale)
    cv2.arrowedLine(canvas, (bx, by), (vx_px, vy_px), COLOR_VECTOR, 2, tipLength=0.3)
    cv2.putText(
        canvas, "v", (vx_px + 5, vy_px - 5),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_VECTOR, 1,
    )

    # Centripetal acceleration (toward center)
    a_c = sim.centripetal_accel
    a_scale = 5.0
    acx = int(bx - (bx - cx) / radius_px * a_c * a_scale)
    acy = int(by - (by - cy) / radius_px * a_c * a_scale)
    cv2.arrowedLine(canvas, (bx, by), (acx, acy), COLOR_CENTRIPETAL, 2, tipLength=0.3)
    cv2.putText(
        canvas, "a_c", (acx + 5, acy - 5),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_CENTRIPETAL, 1,
    )

    # Dot
    cv2.circle(canvas, (bx, by), 8, COLOR_BOB, -1)
    cv2.circle(canvas, (bx, by), 8, (255, 255, 255), 1)

    # Center
    cv2.circle(canvas, (cx, cy), 3, COLOR_CENTER, -1)


# ---------------------------------------------------------------------------
# Projectile drawing
# ---------------------------------------------------------------------------


def draw_projectile_scene(
    canvas: np.ndarray,
    traj_x: np.ndarray,
    traj_y: np.ndarray,
    traj_vx: np.ndarray,
    traj_vy: np.ndarray,
    idx: int,
    origin_px: Tuple[int, int],
    scale: float,
) -> None:
    """Draw the projectile trajectory scene with velocity vectors."""
    ox, oy = origin_px

    # Full trajectory curve
    pts = np.array(
        [(int(ox + traj_x[i] * scale), int(oy - traj_y[i] * scale)) for i in range(len(traj_x))],
        dtype=np.int32,
    )
    if len(pts) >= 2:
        cv2.polylines(canvas, [pts], False, COLOR_TRAJECTORY, 1, cv2.LINE_AA)

    # Current position
    cx = int(ox + traj_x[idx] * scale)
    cy = int(oy - traj_y[idx] * scale)
    cv2.circle(canvas, (cx, cy), 8, COLOR_PROJECTILE, -1)
    cv2.circle(canvas, (cx, cy), 8, (255, 255, 255), 1)

    # Velocity vector
    vx = traj_vx[idx]
    vy = traj_vy[idx]
    v_scale = 3.0

    # Total velocity
    vx_end = int(cx + vx * v_scale)
    vy_end = int(cy + vy * v_scale)
    cv2.arrowedLine(canvas, (cx, cy), (vx_end, vy_end), COLOR_VECTOR, 2, tipLength=0.3)

    # Horizontal component
    vx_end_h = int(cx + vx * v_scale)
    cv2.arrowedLine(canvas, (cx, cy), (vx_end_h, cy), COLOR_VX, 2, tipLength=0.2)
    cv2.putText(
        canvas, "vx", (vx_end_h + 5, cy - 5),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_VX, 1,
    )

    # Vertical component
    vy_end_v = int(cy + vy * v_scale)
    cv2.arrowedLine(canvas, (cx, cy), (cx, vy_end_v), COLOR_VY, 2, tipLength=0.2)
    cv2.putText(
        canvas, "vy", (cx + 5, vy_end_v + 5),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_VY, 1,
    )


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------


def _run_pendulum(args: argparse.Namespace) -> None:
    """Pendulum mode — real webcam with synthetic fallback."""
    from tracking import BobTracker
    from calibration import run_calibration, CalibrationData

    # Try camera
    cap = cv2.VideoCapture(args.device)
    camera_ok = cap.isOpened()
    first_frame: Optional[np.ndarray] = None
    if camera_ok:
        ret, frame = cap.read()
        if ret:
            first_frame = frame
        else:
            camera_ok = False

    # Calibration
    calib: CalibrationData
    if camera_ok and first_frame is not None:
        cv2.namedWindow(WIN_NAME)
        cv2.imshow(WIN_NAME, first_frame)
        cv2.waitKey(100)
        calib = run_calibration(first_frame, WIN_NAME, args.length)
    else:
        calib = CalibrationData(
            pivot_px=(320, 100),
            length_m=args.length,
            scale=200.0,
            calibrated=True,
        )

    cv2.namedWindow(WIN_NAME)
    tracker = BobTracker()
    tracker.create_trackbars(WIN_NAME)

    # Data buffers
    times: Deque[float] = deque(maxlen=MAX_DATA_POINTS)
    thetas: Deque[float] = deque(maxlen=MAX_DATA_POINTS)
    omegas: Deque[float] = deque(maxlen=MAX_DATA_POINTS)

    # Ideal sim for overlay
    ideal_sim = ReferencePendulumSim(
        length=calib.length_m, g=9.81, theta0=0.1, dt=DT
    )
    ideal_times: Deque[float] = deque(maxlen=MAX_DATA_POINTS)
    ideal_thetas: Deque[float] = deque(maxlen=MAX_DATA_POINTS)
    ideal_omegas: Deque[float] = deque(maxlen=MAX_DATA_POINTS)

    # Fallback state
    fallback_sim: Optional[ReferencePendulumSim] = None
    fallback_mode = not camera_ok
    fail_count = 0
    synthetic_time = 0.0

    # Error analysis
    g_est = 0.0
    g_err_pct = 0.0
    period_est = 0.0

    # Scene area for synthetic drawing
    scene_origin = (320, 100)  # pivot pixel in scene area
    length_px = calib.scale * calib.length_m

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        if fallback_mode:
            # ---- Synthetic fallback ----
            if fallback_sim is None:
                fallback_sim = ReferencePendulumSim(
                    length=calib.length_m, g=9.81, theta0=0.1, dt=DT
                )
            state = fallback_sim.state
            theta = state["theta"]
            omega = state["omega"]
            t = state["t"]
            fallback_sim.step()

            thetas.append(theta)
            times.append(t)
            omegas.append(omega)

            # Draw synthetic pendulum in left scene area
            draw_pendulum_scene(canvas, scene_origin, theta, length_px)

            # Overlay message
            cv2.putText(
                canvas,
                "SYNTHETIC MODE - Camera unavailable",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 165, 255),
                2,
            )

            # Step ideal sim in sync
            ideal_state = ideal_sim.state
            ideal_thetas.append(ideal_state["theta"])
            ideal_times.append(ideal_state["t"])
            ideal_omegas.append(ideal_state["omega"])
            ideal_sim.step()

        else:
            # ---- Camera mode ----
            assert cap is not None
            ret, frame = cap.read()
            if not ret:
                fallback_mode = True
                continue

            # Resize camera to left scene area (640x480)
            frame_resized = cv2.resize(frame, (640, 480))
            canvas[0:480, 0:640] = frame_resized

            # Read trackbars
            tracker.read_trackbars(WIN_NAME)

            # Track bob
            centroid = tracker.detect(frame_resized)
            if centroid is None:
                fail_count += 1
                if fail_count >= MAX_FAIL_FRAMES:
                    fallback_mode = True
                    continue
            else:
                fail_count = 0
                cx, cy = centroid
                theta = compute_theta((cx, cy), calib.pivot_px)

                t = synthetic_time
                times.append(t)
                thetas.append(theta)

                if len(thetas) >= 2:
                    omega = (thetas[-1] - thetas[-2]) / DT
                    omegas.append(omega)

                # Draw pivot and bob overlay
                px, py = calib.pivot_px
                cv2.circle(canvas, (px, py), 5, COLOR_PIVOT, -1)
                cv2.circle(canvas, (cx, cy), 8, COLOR_BOB, -1)
                cv2.line(canvas, (px, py), (cx, cy), COLOR_STRING, 2)

                # Step ideal sim
                ideal_state = ideal_sim.state
                ideal_thetas.append(ideal_state["theta"])
                ideal_times.append(ideal_state["t"])
                ideal_omegas.append(ideal_state["omega"])
                ideal_sim.step()

                # Error analysis
                if len(times) > 10:
                    p = estimate_period(list(times), list(thetas))
                    if p is not None and p > 0:
                        period_est = p
                        g_est = 4.0 * math.pi**2 * calib.length_m / (p**2)
                        try:
                            g_err_pct = percent_error(g_est, 9.81)
                        except ZeroDivisionError:
                            g_err_pct = 0.0

            synthetic_time += DT

        # ---- Draw graphs (right side) ----
        # s-t graph (top right)
        st_points = list(zip(times, thetas))
        draw_graph(
            canvas,
            (640, 0, 640, 360),
            st_points,
            COLOR_TRACKED,
            x_label="Time (s)",
            y_label="Theta (rad)",
            title="s-t (Tracked)",
        )

        # Overlay ideal curve on s-t graph
        ideal_st = list(zip(ideal_times, ideal_thetas))
        draw_graph(
            canvas,
            (640, 0, 640, 360),
            ideal_st,
            COLOR_IDEAL,
            title="s-t (Ideal)",
        )

        # Phase portrait (bottom right)
        phase_points = list(zip(thetas, omegas))
        draw_graph(
            canvas,
            (640, 360, 640, 360),
            phase_points,
            COLOR_TRACKED,
            x_label="Theta (rad)",
            y_label="Omega (rad/s)",
            title="Phase Portrait",
        )

        # Overlay ideal phase portrait
        ideal_phase = list(zip(ideal_thetas, ideal_omegas))
        draw_graph(
            canvas,
            (640, 360, 640, 360),
            ideal_phase,
            COLOR_IDEAL,
        )

        # ---- Error analysis display ----
        if period_est > 0:
            g_display = sig_figs(g_est, 3)
            err_display = sig_figs(g_err_pct, 2)
            period_display = sig_figs(period_est, 3)
            info_lines = [
                f"L = {calib.length_m:.2f} m",
                f"T = {period_display:.3f} s",
                f"g_est = {g_display:.3f} m/s^2",
                f"Error = {err_display:.2f} %",
            ]
            for i, line in enumerate(info_lines):
                cv2.putText(
                    canvas,
                    line,
                    (10, CANVAS_H - 100 + i * 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    COLOR_TEXT,
                    1,
                )

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:  # ESC
            break

    if camera_ok and cap is not None:
        cap.release()
    cv2.destroyAllWindows()


def _run_circular(args: argparse.Namespace) -> None:
    """Circular mode — fully synthetic."""
    radius = args.length
    omega0 = 1.5  # rad/s
    sim = CircularMotion(radius=radius, omega0=omega0, dt=DT)

    center_px = (CANVAS_W // 2, CANVAS_H // 2)
    radius_px = 250.0
    trace: Deque[Tuple[int, int]] = deque(maxlen=200)

    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        draw_circular_scene(canvas, center_px, sim, radius_px, trace)

        # Info
        info = [
            f"Radius = {radius:.2f} m",
            f"omega = {omega0:.2f} rad/s",
            f"v = {sim.tangential_speed:.2f} m/s",
            f"a_c = {sim.centripetal_accel:.2f} m/s^2",
        ]
        for i, line in enumerate(info):
            cv2.putText(
                canvas,
                line,
                (10, 30 + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                COLOR_TEXT,
                1,
            )

        sim.step()

        cv2.imshow(WIN_NAME, canvas)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


def _run_projectile(args: argparse.Namespace) -> None:
    """Projectile mode — fully synthetic."""
    from .synthetic import projectile_trajectory

    vx0 = 15.0
    vy0 = 20.0
    g = 9.81

    # Pre-compute full trajectory
    xs, ys, vxs, vys = projectile_trajectory(vx0=vx0, vy0=vy0, g=g, dt=DT)

    origin_px = (100, 600)
    scale = 15.0  # px per metre

    idx = 0
    cv2.namedWindow(WIN_NAME)

    while True:
        canvas = np.zeros((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)

        # Left: trajectory scene
        draw_projectile_scene(canvas, xs, ys, vxs, vys, idx, origin_px, scale)

        # Info
        info = [
            f"vx0 = {vx0:.1f} m/s",
            f"vy0 = {vy0:.1f} m/s",
            f"x = {xs[idx]:.2f} m",
            f"y = {ys[idx]:.2f} m",
            f"vx = {vxs[idx]:.2f} m/s",
            f"vy = {vys[idx]:.2f} m/s",
        ]
        for i, line in enumerate(info):
            cv2.putText(
                canvas,
                line,
                (10, 30 + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                COLOR_TEXT,
                1,
            )

        # Right: height vs range graph
        h_vs_r = [(xs[i], ys[i]) for i in range(idx + 1)]
        draw_graph(
            canvas,
            (640, 0, 640, 720),
            h_vs_r,
            COLOR_TRAJECTORY,
            x_label="Range (m)",
            y_label="Height (m)",
            title="Height vs Range",
        )

        idx = (idx + 1) % len(xs)

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
    from tracking import BobTracker
    from calibration import CalibrationData

    if mode == "pendulum":
        # Synthetic fallback path (no camera)
        sim = ReferencePendulumSim(length=1.0, g=9.81, theta0=0.1, dt=DT)
        tracker = BobTracker()
        _ = tracker  # unused but verifies import
        for _ in range(30):
            sim.step()
        print("Pendulum self-check OK (synthetic fallback)")

    elif mode == "circular":
        sim = CircularMotion(radius=1.0, omega0=1.5, dt=DT)
        for _ in range(30):
            sim.step()
        print("Circular self-check OK")

    elif mode == "projectile":
        from synthetic import projectile_trajectory

        xs, ys, vxs, vys = projectile_trajectory(vx0=15.0, vy0=20.0, g=9.81, dt=DT)
        assert len(xs) > 10, f"Expected >10 trajectory points, got {len(xs)}"
        print(f"Projectile self-check OK ({len(xs)} trajectory points)")

    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    if args.headless_selfcheck:
        _headless_selfcheck(args.mode)
        return

    if args.mode == "pendulum":
        _run_pendulum(args)
    elif args.mode == "circular":
        _run_circular(args)
    elif args.mode == "projectile":
        _run_projectile(args)


if __name__ == "__main__":
    main()