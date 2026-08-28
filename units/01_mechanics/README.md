# Unit 01: Mechanics

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-method coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/mechanics/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes:

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Kinematics** (Mechanics b) | v = Δs/Δt, a = Δv/Δt; interpret motion graphs; uniformly-accelerated equations; vertical motion under gravity | Teacher app (pendulum mode — real-time θ-t and phase-portrait graphs); Manim `IntegratorConvergence` (trajectory comparison) |
| **Projectile motion** (Mechanics f) | Independence of horizontal/vertical motion; parabolic trajectory | Teacher app (projectile mode — height vs range graph, velocity vector decomposition); Manim `ProjectileDt` (exact vs numerical dt convergence) |
| **Periodic motion** (Mechanics g) | SHM as projection of uniform circular motion; period/frequency; ω = 2π/T; displacement as a trig function | Manim `ShmProjection` (rotating radius vector → cosine trace); Teacher app (circular mode — centripetal acceleration vectors) |
| **Building computational models** (Scientific Inquiry) | Translate physics equations into code; modify a simulation and observe the effect | Student exercise (fill in `angular_acceleration`); Manim `IntegratorConvergence` (Euler vs Verlet energy drift) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **SHM / circular motion**: `ShmProjection.mp4` — shows the radius vector rotating, the projected dot on the x-axis, and the cosine trace building in real time. Pause on the phase-angle markers (0, π/2, π, 3π/2) to link the circle geometry to the displacement graph.
- **Numerical methods**: `IntegratorConvergence.mp4` — compares Euler, Verlet, and the exact analytical solution for a simple harmonic oscillator. The energy-drift inset shows Euler's systematic energy gain; the convergence inset shows that reducing dt makes Euler collapse onto the exact curve.
- **Projectile motion**: `ProjectileDt.mp4` — shows the exact parabola alongside coarse-dt and fine-dt Euler trajectories. Three dots animate simultaneously so students see how step size affects accuracy.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Pendulum mode** (`--mode pendulum`): wave a real pendulum (or use the synthetic fallback). The app tracks the bob, plots θ-t and phase-portrait graphs, overlays the ideal curve, and computes an estimate of *g* from the measured period. Use this to discuss error analysis: compare the estimated *g* to 9.81, compute percent error, consider significant figures, and identify sources of error (air resistance, pixel-tracking noise, small-angle approximation).
- **Circular mode** (`--mode circular`): shows a dot moving on a circle with radius, tangential velocity, and centripetal acceleration vectors drawn. Link the x-projection to the SHM animation students just watched.
- **Projectile mode** (`--mode projectile`): launches a projectile with velocity-vector decomposition (vx, vy, total v). The height-vs-range graph builds in real time.

### Step 3: Complete the fill-in-the-blank exercise

Students open `pendulum_exercise.py` and implement the single method `angular_acceleration(self, theta, omega)`. The auto-grader checks:

1. The `NotImplementedError` is replaced (immediate fail if not)
2. The measured period matches `2π√(L/g)` to within 1%
3. Total energy drifts less than 2% over 2000 steps (Verlet)
4. Amplitude stays bounded (wrong sign causes blow-up)

The error-analysis angle from Step 2 feeds directly into the concept questions in `questions.md`: estimating *g* from period, sources of error, Euler vs Verlet energy drift, and the small-angle approximation.

---

## How to Run Each Artifact

### Prerequisites

- Python 3.11+ with `uv` installed
- Docker (for Manim rendering only)

```bash
# Install dependencies
uv sync
```

### Engine tests

```bash
uv run pytest
```

This runs the unit tests in `tests/` (pendulum, projectile, circular, integrators, errors). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Pendulum mode (real webcam or synthetic fallback)
uv run python units/01_mechanics/teacher_app/main.py --mode pendulum

# Circular motion mode (fully synthetic)
uv run python units/01_mechanics/teacher_app/main.py --mode circular

# Projectile motion mode (fully synthetic)
uv run python units/01_mechanics/teacher_app/main.py --mode projectile

# Headless self-check (no window, for CI)
uv run python units/01_mechanics/teacher_app/main.py --mode pendulum --headless-selfcheck
```

The pendulum mode requires a webcam for real capture; if no camera is available it falls back to a synthetic pendulum automatically. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

Additional options:
- `--length <metres>` — pendulum length or circle radius (default: 1.0)
- `--device <index>` — camera device index (default: 0)

### Manim render

```bash
# Render all three scenes (requires Docker)
bash units/01_mechanics/manim/render.sh

# Render a specific scene
bash units/01_mechanics/manim/render.sh shm_projection

# Low-quality preview (fast)
bash units/01_mechanics/manim/render.sh shm_projection -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/01_mechanics/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `shm_projection`, `integrator_convergence`, `projectile_dt`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: pendulum_exercise.py)
uv run pytest units/01_mechanics/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/01_mechanics/exercises/test_exercise.py \
    --override-student=units/01_mechanics/exercises/pendulum_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/01_mechanics/exercises/test_exercise.py --selfcheck -v
```

The solution file (`pendulum_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Pendulum Calibration Guide

When you run the teacher app in pendulum mode with a webcam, the app prompts you to calibrate:

1. **Click the pivot point** — click on the point where the pendulum string is fixed (top of the pendulum). A red dot marks your click.
2. **Enter the pendulum length** — pass `--length <L>` on the command line (in metres). The app uses this value for the physics calculations.
3. **Set the pixel scale** — the app asks you to click two reference points of known separation (or press SPACE to accept a default scale derived from *L*). This maps pixels to metres for the overlay graphics.

The calibration data is stored in a `CalibrationData` dataclass for the session. If no camera is available, the app uses default calibration values and runs in synthetic mode.

After calibration, the app displays:
- The tracked bob position overlaid on the video
- Real-time θ-t and phase-portrait graphs
- An ideal (reference) curve for comparison
- An estimate of *g* computed from the measured period, with percent error vs 9.81

---

## Numerical-Methods Tie-In

The `IntegratorConvergence` Manim scene uses the same `euler_step` and `verlet_step` functions from `physics_core.integrators` that the student exercise builds on. This creates a direct link:

- **Watch**: the Manim scene shows Euler's energy drift and Verlet's stability
- **Do**: the student implements the pendulum's angular acceleration, then runs the simulation with both schemes
- **Analyze**: the concept questions in `questions.md` ask why Euler drifts and Verlet does not

### dt-clamp in Manim updaters

All three Manim scenes use the same dt-clamp pattern in their updater functions:

```python
h = min(dt, 1.0 / config.frame_rate)
```

This prevents a Manim edge-case where `dt` can be 0 on frame boundaries, which would cause the simulation to stall. The clamp ensures the physics step never exceeds one frame's worth of time.

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render every time (cached frames from a previous run with different parameters would be stale).
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.