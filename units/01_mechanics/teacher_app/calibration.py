"""One-time calibration for the pendulum mode.

The teacher:
1. Clicks the pivot point on the video frame.
2. Types the pendulum length *L* (metres).
3. Optionally sets a pixel-to-metre scale by clicking two points of known
   separation, or accepts a default derived from *L*.

All calibration data is stored in a :class:`CalibrationData` dataclass for
the session.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

import cv2
import numpy as np


@dataclass
class CalibrationData:
    """Persistent calibration for one session."""

    pivot_px: Tuple[int, int] = (0, 0)  # (x, y) pixel coordinates of pivot
    length_m: float = 1.0  # pendulum length in metres
    scale: float = 100.0  # pixels per metre (px/m)
    calibrated: bool = False  # True once calibration is complete


# ---------------------------------------------------------------------------
# Interactive calibration helpers — module-level mutable state for the
# mouse callback.  Lowercase names to avoid "constant redefinition" lint.
# ---------------------------------------------------------------------------

_pivot_click: Optional[Tuple[int, int]] = None
_ref_click_a: Optional[Tuple[int, int]] = None
_ref_click_b: Optional[Tuple[int, int]] = None
_cal_step = 0  # 0 = pivot, 1 = ref-a, 2 = ref-b, 3 = done


def _mouse_callback(event: int, x: int, y: int, flags: int, param: object) -> None:
    """Record clicks during calibration."""
    global _pivot_click, _ref_click_a, _ref_click_b, _cal_step
    if event == cv2.EVENT_LBUTTONDOWN:
        if _cal_step == 0:
            _pivot_click = (x, y)
            _cal_step = 1
        elif _cal_step == 1:
            _ref_click_a = (x, y)
            _cal_step = 2
        elif _cal_step == 2:
            _ref_click_b = (x, y)
            _cal_step = 3


def run_calibration(
    frame: np.ndarray,
    window_name: str,
    length_m: float,
) -> CalibrationData:
    """Run the interactive calibration overlay on *frame*.

    The user clicks the pivot, then two reference points a known distance
    apart (or just presses a key to accept the default scale from *L*).

    Returns a populated :class:`CalibrationData`.
    """
    global _pivot_click, _ref_click_a, _ref_click_b, _cal_step
    # Reset globals
    _pivot_click = None
    _ref_click_a = None
    _ref_click_b = None
    _cal_step = 0

    cv2.setMouseCallback(window_name, _mouse_callback)

    data = CalibrationData()
    data.length_m = length_m

    overlay = frame.copy()

    while True:
        display = overlay.copy()

        if _cal_step == 0:
            cv2.putText(
                display,
                "Click the PIVOT point (top of pendulum)",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
            )
        elif _cal_step == 1:
            if _pivot_click is not None:
                cv2.circle(display, _pivot_click, 5, (0, 0, 255), -1)
            cv2.putText(
                display,
                "Click two points of known separation (or press SPACE to use L)",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )
        elif _cal_step == 2:
            if _pivot_click is not None:
                cv2.circle(display, _pivot_click, 5, (0, 0, 255), -1)
            if _ref_click_a is not None:
                cv2.circle(display, _ref_click_a, 5, (255, 0, 0), -1)
            cv2.putText(
                display,
                "Click second reference point",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
            )
        elif _cal_step >= 3:
            # Compute scale
            if _ref_click_a is not None and _ref_click_b is not None:
                ref_px = np.linalg.norm(
                    np.array(_ref_click_b, dtype=float)
                    - np.array(_ref_click_a, dtype=float)
                )
                # Assume reference distance = L (the user measured a known length)
                data.scale = ref_px / data.length_m
            else:
                # Default: assume L pixels = L metres
                data.scale = 1.0  # fallback — will be refined below

            data.pivot_px = _pivot_click if _pivot_click is not None else (0, 0)
            data.calibrated = True
            break

        cv2.imshow(window_name, display)
        key = cv2.waitKey(30) & 0xFF
        if key == 32:  # SPACE — skip reference points
            _cal_step = 3
        if key == 27:  # ESC — abort with defaults
            data.pivot_px = _pivot_click if _pivot_click is not None else (frame.shape[1] // 2, 50)
            data.calibrated = True
            break

    cv2.setMouseCallback(window_name, lambda *a: None)
    return data