# Unit 03: Waves

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the wave physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-method coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/waves/`), so the physics is identical across every front-end.

**Note:** The teacher app is fully synthetic (no webcam required) — it always works out of the box.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes:

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Nature of waves** (Wave Motion a) | Amplitude, wavelength, frequency, wave speed v = fλ; transverse vs longitudinal waves; energy ∝ amplitude² | Teacher app (traveling mode — sine curve with moving particle, phase display); Manim `WaveSpeedIntensity` (three amplitudes, intensity bar chart) |
| **Superposition and interference** (Wave Motion b) | Principle of superposition; constructive/destructive interference; standing/stationary waves (transverse only) | Manim `SuperpositionStanding` (two counter-propagating waves → standing wave with nodes); Teacher app (standing mode — two waves + result overlay) |
| **Young's double-slit** (Wave Motion c) | d sin θ = n λ; bright/dark fringes; fringe spacing Δy = λD/d | Manim `YoungSlit` (fringe pattern with order labels); Teacher app (interference mode — slit geometry, fringe positions, formula display) |
| **Diffraction and polarisation** (Wave Motion d) | Diffraction grating; polarisation as evidence for transverse waves | Student exercise concept questions (polarisation, diffraction grating) |
| **Wave phenomena** (Wave Motion e) | Reflection, refraction, diffraction; intensity and inverse-square law | Teacher app (traveling mode — displacement vs time graph); Manim `WaveSpeedIntensity` (I ∝ A² bar chart) |
| **Sound waves** (Wave Motion f) | Musical notes, resonance, standing waves on strings | Student exercise concept questions (standing waves on strings, harmonics) |
| **Building computational models** (Scientific Inquiry) | Translate physics equations into code; modify a simulation and observe the effect | Student exercise (fill in `displacement`); Manim scenes (analytical wave solutions) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Superposition / standing waves**: `SuperpositionStanding.mp4` — shows two counter-propagating traveling waves (blue and orange) and their superposition (green) forming a standing wave with fixed nodes (red markers). Pause to identify node and anti-node positions.
- **Wave speed and intensity**: `WaveSpeedIntensity.mp4` — shows three traveling waves with different amplitudes side by side, with a bar chart showing the corresponding intensities (I ∝ A²). Use this to discuss the relationship between amplitude and energy.
- **Young's double-slit**: `YoungSlit.mp4` — shows the double-slit geometry with bright fringes labelled by order n, the formula d sin θ = n λ, and animated rays sweeping across the screen to show the path difference.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Traveling wave mode** (`--mode traveling`): shows a sine wave with a moving particle on it. The particle oscillates vertically as the wave passes. The displacement-vs-time graph builds in real time. Use this to discuss amplitude, wavelength, frequency, phase, and wave speed.
- **Standing wave mode** (`--mode standing`): shows two counter-propagating waves (thin lines) and their superposition (thick green line) forming a standing wave. Nodes are marked in red. Use this to discuss superposition, nodes, anti-nodes, and how standing waves form.
- **Interference mode** (`--mode interference`): shows Young's double-slit geometry with bright fringes on the screen labelled by order n. The formula d sin θ = n λ is displayed. Use this to discuss interference conditions, fringe spacing, and the wave nature of light.

### Step 3: Complete the fill-in-the-blank exercise

Students open `wave_exercise.py` and implement the single method `displacement(self, x, t)`. The auto-grader checks:

1. The `NotImplementedError` is replaced (immediate fail if not)
2. The field values match `A sin(kx - ωt)` to within 1e-10 tolerance
3. Superposition behaviour is correct (standing wave node check)
4. Intensity scales as amplitude squared (I ∝ A²)

The concept questions in `questions.md` cover superposition, standing vs traveling waves, intensity, inverse-square law, interference, and polarisation.

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

This runs the unit tests in `tests/` (including the new `test_waves.py`). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Traveling wave mode (synthetic — always works)
uv run python units/03_waves/teacher_app/main.py --mode traveling

# Standing wave mode (synthetic)
uv run python units/03_waves/teacher_app/main.py --mode standing

# Interference / Young's double-slit mode (synthetic)
uv run python units/03_waves/teacher_app/main.py --mode interference

# Headless self-check (no window, for CI)
uv run python units/03_waves/teacher_app/main.py --mode standing --headless-selfcheck
```

The teacher app is fully synthetic — no webcam is needed. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all three scenes (requires Docker)
bash units/03_waves/manim/render.sh

# Render a specific scene
bash units/03_waves/manim/render.sh superposition_standing

# Low-quality preview (fast)
bash units/03_waves/manim/render.sh superposition_standing -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/03_waves/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `superposition_standing`, `wave_speed_intensity`, `young_slit`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: wave_exercise.py)
uv run pytest units/03_waves/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/03_waves/exercises/test_exercise.py \
    --override-student=units/03_waves/exercises/wave_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/03_waves/exercises/test_exercise.py --selfcheck -v
```

The solution file (`wave_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Numerical-Methods Tie-In

The wave simulation in this unit is **analytical** rather than numerical — the traveling wave `y(x,t) = A sin(kx - ωt)` is a closed-form solution of the wave equation. This means:

- No ODE integration is needed (no Euler/Verlet steps)
- The solution is exact at every point in space and time
- Students can verify the wave equation `∂²y/∂t² = v² ∂²y/∂x²` analytically

The `WaveSpeedIntensity` Manim scene demonstrates the relationship between amplitude and intensity (I ∝ A²), which is a key concept for understanding wave energy transport.

### dt-clamp in Manim updaters

All three Manim scenes use the same dt-clamp pattern in their updater functions:

```python
h = min(dt, 1.0 / config.frame_rate)
```

This prevents a Manim edge-case where `dt` can be 0 on frame boundaries, which would cause the simulation to stall. The clamp ensures the physics step never exceeds one frame's worth of time.

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render every time (cached frames from a previous run with different parameters would be stale).
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.
