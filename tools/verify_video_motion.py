"""Verify that a Manim-rendered video actually animates.

Usage:
    uv run python tools/verify_video_motion.py <video.mp4> [video2.mp4 ...]

Gate (MOTION OK) requires ALL of:
  1. Video is decodable and has >= 30 frames.
  2. Max mean absolute pixel diff between consecutive sampled frames > 0.05
     (a completely static render measures ~0.00).
  3. The "colored content" (high-saturation pixels) changes by more than
     300 px somewhere between the first third and the last third of the
     video (catches renders where only a label fades while the main
     figure is never drawn — the "只有框架沒有線" failure mode).

With --strict (for continuous-simulation scenes), additionally:
  4. At least 5 of the ~40 sampled frame intervals show motion
     (diff > 0.05).  A single mid-video glitch (e.g. a label disappearing)
     must not pass as "animation".

Exit code 0 = all videos pass; 1 = at least one fails.
"""

from __future__ import annotations

import sys

import cv2
import numpy as np

MOTION_THRESHOLD = 0.05
CONTENT_CHANGE_THRESHOLD = 300
STRICT_MIN_MOTION_INTERVALS = 5


def colored_px(frame: np.ndarray) -> int:
    """Count high-saturation (non-grey) pixels in a BGR frame."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return int((hsv[:, :, 1] > 60).sum())


def verify(video: str, strict: bool = False) -> bool:
    cap = cv2.VideoCapture(video)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if n < 30:
        print(f"FAIL {video}: only {n} frames (need >= 30)")
        cap.release()
        return False

    # Sample ~40 frames evenly across the video.
    idxs = np.linspace(0, n - 1, 40).astype(int)
    prev = None
    max_diff = 0.0
    motion_intervals = 0
    first_colored = None
    last_colored = None
    prev_colored = None
    max_content_change = 0
    for i in idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i))
        ok, fr = cap.read()
        if not ok:
            print(f"FAIL {video}: cannot read frame {i}")
            cap.release()
            return False
        if prev is not None:
            d = float(np.mean(np.abs(fr.astype(int) - prev.astype(int))))
            max_diff = max(max_diff, d)
            if d > MOTION_THRESHOLD:
                motion_intervals += 1
        prev = fr
        c = colored_px(fr)
        if first_colored is None:
            first_colored = c
        last_colored = c
        if prev_colored is not None:
            max_content_change = max(max_content_change, abs(c - prev_colored))
        prev_colored = c
    cap.release()

    ok = True
    if max_diff <= MOTION_THRESHOLD:
        print(
            f"FAIL {video}: max consecutive-frame diff {max_diff:.3f} "
            f"(<= {MOTION_THRESHOLD}) — video is static"
        )
        ok = False
    if max_content_change <= CONTENT_CHANGE_THRESHOLD:
        print(
            f"FAIL {video}: colored content never changes "
            f"(max change {max_content_change}px, first={first_colored} "
            f"last={last_colored}) — main figure likely never drawn"
        )
        ok = False
    if strict and motion_intervals < STRICT_MIN_MOTION_INTERVALS:
        print(
            f"FAIL {video}: only {motion_intervals}/39 sampled intervals show "
            f"motion (need >= {STRICT_MIN_MOTION_INTERVALS}) — animation is not "
            f"sustained across the video"
        )
        ok = False
    if ok:
        print(
            f"PASS {video}: frames={n} max_diff={max_diff:.3f} "
            f"content_change={max_content_change}px "
            f"motion_intervals={motion_intervals}/39"
        )
    return ok


def main(argv: list[str]) -> int:
    args = argv[1:]
    strict = False
    if "--strict" in args:
        strict = True
        args.remove("--strict")
    if not args:
        print(__doc__)
        return 2
    results = [verify(v, strict=strict) for v in args]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
