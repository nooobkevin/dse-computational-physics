"""Color-centroid bob tracking via HSV thresholding.

The :class:`BobTracker` takes a BGR frame, converts to HSV, applies a
tunable hue/saturation/value range, finds the largest contour of the
resulting mask, and returns its centroid in pixel coordinates.

A trackbar (``create_trackbars``) lets the teacher widen or narrow the
HSV window live when lighting conditions change.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

import cv2
import numpy as np


# Default orange-ish bob — tune with the trackbars.
DEFAULT_HSV_LOW = np.array([5, 120, 80], dtype=np.uint8)
DEFAULT_HSV_HIGH = np.array([25, 255, 255], dtype=np.uint8)

# Minimum contour area (px²) — smaller blobs are rejected as noise.
MIN_CONTOUR_AREA = 50


@dataclass
class HSVRange:
    """Mutable HSV threshold range.  Trackbars write directly into here."""

    low: np.ndarray = field(default_factory=lambda: DEFAULT_HSV_LOW.copy())
    high: np.ndarray = field(default_factory=lambda: DEFAULT_HSV_HIGH.copy())

    def as_tuple(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.low, self.high


class BobTracker:
    """Track a coloured pendulum bob in a webcam frame.

    Parameters
    ----------
    hsv_range : HSVRange or None
        HSV bounds.  A fresh default range is created if None.
    min_area : int
        Minimum contour area in pixels — smaller blobs are ignored.
    """

    def __init__(
        self,
        hsv_range: Optional[HSVRange] = None,
        min_area: int = MIN_CONTOUR_AREA,
    ) -> None:
        self.hsv_range = hsv_range if hsv_range is not None else HSVRange()
        self.min_area = min_area

    def detect(self, frame: np.ndarray) -> Optional[Tuple[int, int]]:
        """Return the centroid ``(cx, cy)`` of the largest coloured blob,
        or ``None`` if no blob above ``min_area`` is found.
        """
        if frame is None or frame.size == 0:
            return None

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.hsv_range.low, self.hsv_range.high)

        # Morphological cleanup — remove specks, fill small holes.
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) < self.min_area:
            return None

        M = cv2.moments(largest)
        if M["m00"] == 0:
            return None
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy)

    # ------------------------------------------------------------------
    # Trackbar helpers
    # ------------------------------------------------------------------

    def create_trackbars(self, window_name: str) -> None:
        """Attach HSV tune trackbars to an existing OpenCV window."""
        # Placeholder callbacks — we just read the trackbar values in the loop.
        def _nothing(_: int) -> None:
            return None

        cv2.createTrackbar("H Low", window_name, int(self.hsv_range.low[0]), 179, _nothing)
        cv2.createTrackbar("H High", window_name, int(self.hsv_range.high[0]), 179, _nothing)
        cv2.createTrackbar("S Low", window_name, int(self.hsv_range.low[1]), 255, _nothing)
        cv2.createTrackbar("S High", window_name, int(self.hsv_range.high[1]), 255, _nothing)
        cv2.createTrackbar("V Low", window_name, int(self.hsv_range.low[2]), 255, _nothing)
        cv2.createTrackbar("V High", window_name, int(self.hsv_range.high[2]), 255, _nothing)

    def read_trackbars(self, window_name: str) -> None:
        """Pull the current trackbar values into ``self.hsv_range``."""
        try:
            h_low = cv2.getTrackbarPos("H Low", window_name)
            h_high = cv2.getTrackbarPos("H High", window_name)
            s_low = cv2.getTrackbarPos("S Low", window_name)
            s_high = cv2.getTrackbarPos("S High", window_name)
            v_low = cv2.getTrackbarPos("V Low", window_name)
            v_high = cv2.getTrackbarPos("V High", window_name)
        except cv2.error:
            # Window might not exist (headless / closed) — skip.
            return
        self.hsv_range.low = np.array([h_low, s_low, v_low], dtype=np.uint8)
        self.hsv_range.high = np.array([h_high, s_high, v_high], dtype=np.uint8)
