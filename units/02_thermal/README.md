# Unit 02: Thermal Physics (Kinetic Theory)

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the kinetic theory of gases
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a two-method coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/thermal/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes:

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Kinetic theory** (Thermal Physics a) | Random motion of molecules; molecular model of an ideal gas; assumptions of the kinetic theory | Teacher app (gas mode — real-time MD simulation with particle trajectories and velocity arrows); Manim `MaxwellBoltzmann` (speed distribution animation) |
| **Maxwell-Boltzmann distribution** (Thermal Physics b) | Speed distribution of gas particles; most probable speed, mean speed, RMS speed; effect of temperature on the distribution | Manim `MaxwellBoltzmann` (MB curve changing with T, measured distribution overlay); Teacher app (live histogram with theoretical MB curve) |
| **Pressure and the ideal gas law** (Thermal Physics c) | pV = NkT; pressure from wall collisions; momentum transfer | Manim `PressureStatistical` (collision frequency vs N, pressure convergence); Teacher app (computed pressure vs ideal gas law) |
| **Internal energy and equipartition** (Thermal Physics d) | Internal energy of an ideal gas; equipartition theorem; degrees of freedom | Teacher app (KE display, temperature estimation from KE); Student exercise (implement collision hooks, observe equipartition) |
| **Building computational models** (Scientific Inquiry) | Translate physics equations into code; modify a simulation and observe the effect | Student exercise (fill in `_collide_wall` and `_collide_particle`); Manim `IntegratorConvergence` (Euler vs Verlet energy drift) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Maxwell-Boltzmann distribution**: `MaxwellBoltzmann.mp4` — shows the theoretical MB speed distribution curve at different temperatures, alongside the measured distribution from a running MD simulation. As temperature increases, the distribution broadens and the peak shifts right. Pause at each temperature to discuss the most probable speed, mean speed, and RMS speed.
- **Numerical methods**: `IntegratorConvergence.mp4` — compares Euler and Verlet for a particle bouncing between walls. The energy-drift inset shows that both schemes conserve energy for free particles (no forces), but the trajectory accuracy differs.
- **Pressure from collisions**: `PressureStatistical.mp4` — shows the gas box with particles, a running pressure-vs-time graph converging toward the ideal gas law prediction, and the speed distribution histogram with MB overlay.

### Step 2: Run the teacher demo app

Open the teacher app in gas mode and demonstrate the physics live:

- **Gas mode** (`--mode gas`): spawns N particles in a 2D box with velocity arrows. The app shows:
  - The gas box with particles moving and colliding (velocity arrows indicate direction and magnitude)
  - A speed distribution histogram with the theoretical Maxwell-Boltzmann curve overlaid
  - Live computed pressure (from wall momentum transfer) compared to the ideal gas law
  - Average speed, RMS speed, and estimated temperature from equipartition
  - Use this to discuss: how pressure emerges from collisions, how the speed distribution matches theory, how temperature relates to average KE

The gas mode is fully synthetic (no webcam needed), so it always works.

### Step 3: Complete the fill-in-the-blank exercise

Students open `gas_exercise.py` and implement two methods: `_collide_wall` and `_collide_particle`. The auto-grader checks:

1. The `NotImplementedError` is replaced (immediate fail if not)
2. Pressure / kinetic energy is positive after running
3. Speed distribution is non-empty
4. Kinetic energy is conserved for a single free particle (Verlet)
5. A particle heading toward a wall bounces back

The error-analysis angle from Step 2 feeds directly into the concept questions in `questions.md`: Maxwell-Boltzmann distribution, equipartition, pressure from collisions, sources of error, Verlet vs Euler, and 2D vs 3D.

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

This runs the unit tests in `tests/` (including the new thermal tests). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Gas mode (fully synthetic — no webcam needed)
uv run python units/02_thermal/teacher_app/main.py --mode gas

# Headless self-check (no window, for CI)
uv run python units/02_thermal/teacher_app/main.py --mode gas --headless-selfcheck
```

The gas mode is fully synthetic, so it always works without a webcam. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

Additional options:
- `--N <count>` — number of gas particles (default: 200)
- `--T <temperature>` — initial temperature (default: 2.0)

### Manim render

```bash
# Render all three scenes (requires Docker)
bash units/02_thermal/manim/render.sh

# Render a specific scene
bash units/02_thermal/manim/render.sh maxwell_boltzmann

# Low-quality preview (fast)
bash units/02_thermal/manim/render.sh maxwell_boltzmann -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/02_thermal/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `maxwell_boltzmann`, `integrator_convergence`, `pressure_statistical`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: gas_exercise.py)
uv run pytest units/02_thermal/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/02_thermal/exercises/test_exercise.py \
    --override-student=units/02_thermal/exercises/gas_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/02_thermal/exercises/test_exercise.py --selfcheck -v
```

The solution file (`gas_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Numerical-Methods Tie-In

The `IntegratorConvergence` Manim scene uses the same `euler_step` and `verlet_step` functions from `physics_core.integrators` that the student exercise builds on. This creates a direct link:

- **Watch**: the Manim scene shows Euler vs Verlet trajectory and energy conservation for a bouncing particle
- **Do**: the student implements the collision hooks, then runs the simulation with both schemes
- **Analyze**: the concept questions in `questions.md` ask why both schemes conserve energy for free particles, and how collisions are handled

### dt-clamp in Manim updaters

All three Manim scenes use the same dt-clamp pattern in their updater functions:

```python
h = min(dt, 1.0 / config.frame_rate)
```

This prevents a Manim edge-case where `dt` can be 0 on frame boundaries, which would cause the simulation to stall. The clamp ensures the physics step never exceeds one frame's worth of time.

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render every time (cached frames from a previous run with different parameters would be stale).
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.

---

## Synthetic-Only Mode

Unlike Unit 01 (Mechanics), which has a webcam-based pendulum mode, the thermal unit is **fully synthetic** — no webcam is needed. The gas simulation runs entirely in software, generating particles, collisions, and thermodynamic observables computationally. This means the teacher app always works, in any environment.

The trade-off is that students cannot directly compare simulation results to a real physical experiment (as they can with the pendulum). Instead, the focus is on comparing the simulation to the **theoretical predictions** of kinetic theory: the Maxwell-Boltzmann distribution, the ideal gas law, and equipartition.