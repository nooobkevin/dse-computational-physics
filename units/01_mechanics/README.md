# Unit 01: Mechanics

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-method coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/mechanics/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes (June 2026 CAF Consultation Draft, Topic "1. Mechanics"):

| CAF item | Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|---|
| **a** | Vector and scalar | Distance vs displacement; vector vs scalar quantities | Student exercise concept questions |
| **b** | Kinematics | v = Δs/Δt, a = Δv/Δt; interpret s–t, v–t, a–t graphs; SUVAT equations; vertical motion under gravity; effect of air resistance | Teacher app (pendulum mode — real-time θ-t and phase-portrait graphs); Manim `IntegratorConvergence` (trajectory comparison); Manim `PlanetFreeFall` (free fall on Earth/Moon/Mars); Manim `ProjectileDrag` (ideal vs drag trajectory); Student exercise `kinematics_exercise.py` |
| **c** | Force and motion | Free-body diagrams; vector addition/resolution of forces; Newton's Laws; moment of force, torque, equilibrium, centre of gravity | Teacher app (projectile mode — velocity vector decomposition as proxy) |
| **d** | Work, energy and power | W = Fs cosθ; KE = ½mv², PE = mgh; P = W/t; conservation of energy; efficiency | Teacher app pendulum mode (energy display); Manim `IntegratorConvergence` (energy drift inset); Student pendulum exercise (energy conservation) |
| **e** | Momentum | p = mv; impulse; conservation of momentum; elastic/inelastic collisions | — (planned for future iteration) |
| **f** | Projectile motion | Parabolic path; independence of horizontal/vertical motion | Teacher app (projectile mode — height vs range, vx/vy decomposition); Manim `ProjectileDt` (dt convergence); Manim `ProjectileDrag` (drag comparison) |
| **g** | Periodic motion | Angular displacement/velocity; centripetal force; SHM kinematics (x, v, a vs t); SHM as projection of uniform circular motion; period/frequency; forced oscillation, damping, resonance *(Annex 3 enrichment)* | Manim `ShmProjection` (radius vector → x(t), v(t), a(t) traces); Manim `DampedSHM` (underdamped/critical/overdamped regimes with envelopes); Teacher app (circular mode — centripetal acceleration vectors) |
| **h** | Gravitation | Newton's law of universal gravitation; gravitational field strength g = F/m | Student exercise concept questions |
| — | Building computational models (Scientific Inquiry) | Translate physics equations into code; modify a simulation and observe the effect | Student pendulum exercise (fill in `angular_acceleration`); student kinematics exercise (fill in SUVAT hooks); Manim `IntegratorConvergence` (Euler vs Verlet energy drift) |

### Motion Video Analysis (MVA) framing

The teacher app's **pendulum mode** (`--mode pendulum`) performs real-time webcam tracking of a swinging pendulum — this *is* the CAF's suggested "motion video analysis (MVA)" activity (line 1316 of the CAF consultation draft).  The app tracks the bob, plots θ-t and phase-portrait graphs, overlays the ideal curve, and estimates *g* from the measured period.  For classrooms without a physical pendulum, the synthetic fallback mode demonstrates the same concepts.

### Damping and resonance coverage

The CAF Annex 3 enrichment "forced oscillation, damping, and resonance" (lines 4377–4380) is covered by:
- **Manim `DampedSHM`** — visual comparison of underdamped, critically damped, and overdamped oscillators with analytic decay envelopes
- **Engine damping support** — `ReferencePendulumSim` accepts a `damping_coefficient` parameter (default 0, backward compatible); the damping term `-b·ω` is added to the angular acceleration
- **Suggested activities** — discuss damping applications (car shock absorbers, door dampers) and the Tacoma Narrows Bridge collapse (lack of damping against forced oscillations)

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **SHM / circular motion**: `ShmProjection.mp4` — shows the radius vector rotating, the projected dot on the x-axis, and three stacked traces building in real time: x(t) = R cos(ωt), v(t) = −Rω sin(ωt), a(t) = −Rω² cos(ωt). Pause on the phase-angle markers (0, π/2, π, 3π/2) to link the circle geometry to all three graphs.
- **Damped SHM**: `DampedSHM.mp4` — three panels side by side showing underdamped, critically damped, and overdamped oscillators with the analytic decay envelope A·e^(−γt) overlaid. Discuss the critical damping condition b = 2√(g/L) and applications (car suspension, door closers).
- **Numerical methods**: `IntegratorConvergence.mp4` — compares Euler, Verlet, and the exact analytical solution for a simple harmonic oscillator. The energy-drift inset shows Euler's systematic energy gain; the convergence inset shows that reducing dt makes Euler collapse onto the exact curve.
- **Projectile motion (dt)**: `ProjectileDt.mp4` — shows the exact parabola alongside coarse-dt and fine-dt Euler trajectories. Three dots animate simultaneously so students see how step size affects accuracy.
- **Projectile motion (drag)**: `ProjectileDrag.mp4` — ideal parabola vs trajectory with linear drag. Shows range reduction and terminal-velocity hint in the vertical component. Use this to discuss air resistance effects on real projectiles.
- **Free fall on different planets**: `PlanetFreeFall.mp4` — three objects dropped simultaneously from the same height on Earth (g=9.81), Moon (g=1.62), and Mars (g=3.71). Position labels update in real time; a v-t trace panel shows linear velocity growth with slope = g. Illustrates that g varies by planet while the constant-acceleration model holds.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Pendulum mode** (`--mode pendulum`): wave a real pendulum (or use the synthetic fallback). The app tracks the bob, plots θ-t and phase-portrait graphs, overlays the ideal curve, and computes an estimate of *g* from the measured period. Use this to discuss error analysis: compare the estimated *g* to 9.81, compute percent error, consider significant figures, and identify sources of error (air resistance, pixel-tracking noise, small-angle approximation).
- **Circular mode** (`--mode circular`): shows a dot moving on a circle with radius, tangential velocity, and centripetal acceleration vectors drawn. Link the x-projection to the SHM animation students just watched.
- **Projectile mode** (`--mode projectile`): launches a projectile with velocity-vector decomposition (vx, vy, total v). The height-vs-range graph builds in real time.

### Step 3: Complete the fill-in-the-blank exercises

Two exercises are available; assign the one that matches the topic:

**Pendulum exercise** (`pendulum_exercise.py`): implement `angular_acceleration(self, theta, omega)`. The auto-grader checks:
1. The `NotImplementedError` is replaced (immediate fail if not)
2. The measured period matches `2π√(L/g)` to within 1%
3. Total energy drifts less than 2% over 2000 steps (Verlet)
4. Amplitude stays bounded (wrong sign causes blow-up)

**Kinematics exercise** (`kinematics_exercise.py`): implement five SUVAT hooks (`velocity_after`, `displacement`, `displacement_from_uv`, `final_velocity_sq`, `acceleration_from_graph`). The auto-grader checks each formula with multiple test cases.

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
# Render all scenes (requires Docker)
bash units/01_mechanics/manim/render.sh

# Render a specific scene
bash units/01_mechanics/manim/render.sh damped_shm

# Low-quality preview (fast)
bash units/01_mechanics/manim/render.sh damped_shm -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/01_mechanics/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `shm_projection`, `integrator_convergence`, `projectile_dt`, `damped_shm`, `planet_freefall`, `projectile_drag`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the pendulum exercise
uv run pytest units/01_mechanics/exercises/test_exercise.py -v

# Grade against the pendulum solution file (teacher self-check)
uv run pytest units/01_mechanics/exercises/test_exercise.py \
    --override-student=units/01_mechanics/exercises/pendulum_solution.py -v

# Full pendulum self-check
uv run pytest units/01_mechanics/exercises/test_exercise.py --selfcheck -v

# Grade the kinematics exercise
uv run pytest units/01_mechanics/exercises/test_kinematics_exercise.py -v

# Grade against the kinematics solution file (teacher self-check)
uv run pytest units/01_mechanics/exercises/test_kinematics_exercise.py \
    --override-student=units/01_mechanics/exercises/kinematics_solution.py -v
```

The solution files (`pendulum_solution.py`, `kinematics_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

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

All Manim scenes use the proven animation pattern: an authoritative time `t = [0.0]` read from `scene.time` via a driver Mobject, with all time-varying visuals rebuilt every frame as `always_redraw` lambdas. Each curve is a single VMobject built with `set_points_as_corners` (never a VGroup of Lines).

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render every time (cached frames from a previous run with different parameters would be stale).
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.
- Each new/changed scene is verified with `tools/verify_video_motion.py --strict` to ensure motion is present in ≥5 of 39 sampled intervals.