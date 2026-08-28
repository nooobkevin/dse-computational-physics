# Unit 08: Astrophysics and Relativity

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-class coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/astrophysics/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes:

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Doppler effect — light** (Astrophysics 8a) | Redshift/blueshift; observed frequency formula; `z = Δλ/λ`; low-velocity approximation `z ≈ v/c` | Teacher app (`--mode doppler` — live wave-compression animation with colour shift); Manim `DopplerRedshift` (rest → blueshift → redshift); Student exercise (implement `observed_frequency`, `redshift`, `velocity_from_z`) |
| **Hubble's law** (Astrophysics 8b) | `v = H₀d`; expanding universe; recession velocity proportional to distance | Teacher app (`--mode hubble` — galaxy scatter plot with theoretical line); Manim `HubbleLawScene` (axes, dots, theory line); Student exercise (implement `hubble_velocity`) |
| **Big Bang theory and evidence** (Astrophysics 8c) | CMB, galaxy redshifts, light-element abundances as evidence for the Big Bang | Concept questions in `questions.md`; Teacher app (`--mode lifecycles` — cosmic timeline discussed in class) |
| **Stellar life cycle** (Astrophysics 8d) | Nebula → main sequence → giant/supergiant → white dwarf / neutron star / black hole; spectral classification (O B A F G K M) | Manim `StellarLifecycle` (schematic flow diagram); Teacher app (`--mode lifecycles` — box-and-arrow diagram + spectral class table) |
| **Special relativity — concepts** (Relativity 8e) | Time dilation, length contraction (conceptual); twin paradox | Concept questions in `questions.md` (twin paradox, time dilation explanation) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Doppler redshift**: `DopplerRedshift.mp4` — shows a source emitting light waves at rest, then approaching (blueshift, compressed waves), then receding (redshift, stretched waves). The relativistic Doppler formula and redshift *z* are overlaid.
- **Hubble's law**: `HubbleLawScene.mp4` — shows an expanding-universe scatter plot: galaxy dots with recession velocity proportional to distance (v = H₀·d), along with a theoretical line and axis labels.
- **Stellar life cycle**: `StellarLifecycle.mp4` — shows a schematic flow diagram of stellar evolution: nebula → main sequence → giant/supergiant → white dwarf / neutron star / black hole, with mass-threshold labels.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Doppler mode** (`--mode doppler`): a sine wave representing light from a source is animated; the source's velocity sweeps sinusoidally through approaching → rest → receding. The wave compresses (blueshift, blue colour) or stretches (redshift, red colour) in real time. Observed frequency, redshift *z*, and wavelength shift are displayed numerically. Use this to discuss: why does approaching give a higher frequency? What is the relationship between `z` and `v`? At what speed is the shift noticeable?
- **Hubble mode** (`--mode hubble`): a scatter plot of synthetic galaxies at random distances is shown with the theoretical `v = H₀·d` line. Each galaxy dot includes a small peculiar-velocity scatter. Use this to discuss: what does the slope of the line represent? Why are the data points not all on the line? What is the physical meaning of H₀?
- **Lifecycles mode** (`--mode lifecycles`): a schematic flow diagram of stellar evolution shows boxes and arrows for each stage. The spectral-classification table (O B A F G K M) is displayed at the bottom. Use this to discuss: what determines a star's fate? What is a white dwarf? What happens in a supernova?

### Step 3: Complete the fill-in-the-blank exercise

Students open `astrophysics_exercise.py` and implement the four methods on `StudentDopplerShift`: `observed_frequency`, `redshift`, `velocity_from_z`, and `hubble_velocity`. The auto-grader checks:

1. The `NotImplementedError` is replaced (immediate fail if not)
2. A receding source gives a lower observed frequency (redshift, `f_obs < f0`)
3. An approaching source gives a higher observed frequency (blueshift, `f_obs > f0`)
4. The low-velocity redshift `z ≈ v/c` to within 5%
5. `velocity_from_z(redshift(v))` recovers the original velocity `v` to within 1%
6. `hubble_velocity(d)` gives `H₀ · d` to within 1%

The concept questions in `questions.md` tie the code to the broader curriculum: meaning of redshift, the `z = Δλ/λ` formula, Hubble's law and the expanding universe, evidence for the Big Bang, stellar life cycles, and time dilation.

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

This runs all unit tests including `tests/test_astrophysics.py` (Doppler shift, Hubble's law). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Doppler mode (fully synthetic)
uv run python units/08_astrophysics/teacher_app/main.py --mode doppler

# Hubble mode (fully synthetic)
uv run python units/08_astrophysics/teacher_app/main.py --mode hubble

# Life cycles mode (fully synthetic)
uv run python units/08_astrophysics/teacher_app/main.py --mode lifecycles

# Headless self-check (no window, for CI)
uv run python units/08_astrophysics/teacher_app/main.py --mode doppler --headless-selfcheck
```

All modes are fully synthetic — no camera required. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all three scenes (requires Docker)
bash units/08_astrophysics/manim/render.sh

# Render a specific scene
bash units/08_astrophysics/manim/render.sh doppler_redshift

# Low-quality preview (fast)
bash units/08_astrophysics/manim/render.sh doppler_redshift -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/08_astrophysics/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `doppler_redshift`, `hubble_law`, `stellar_lifecycle`.

Quality flags: `-qm` (medium, default), `-qh` (high), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: astrophysics_exercise.py)
uv run pytest units/08_astrophysics/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/08_astrophysics/exercises/test_exercise.py \
    --override-student=units/08_astrophysics/exercises/astrophysics_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/08_astrophysics/exercises/test_exercise.py --selfcheck \
    --override-student=units/08_astrophysics/exercises/astrophysics_solution.py -v
```

The solution file (`astrophysics_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Physics Engine Architecture

The `src/physics_core/astrophysics/` package mirrors the pattern established by `mechanics/` and `em/`:

```
src/physics_core/astrophysics/
  __init__.py           ← exports all classes
  doppler.py            ← DopplerShift (abstract) + ReferenceDopplerShift
  hubble.py             ← HubbleLaw + SPECTRAL_CLASSES table
```

The abstract base `DopplerShift` defines four physics **hooks** (raising `NotImplementedError`) that subclasses override:

- `observed_frequency(v)` — relativistic Doppler formula
- `redshift(v)` — `z = sqrt((1+β)/(1-β)) - 1`
- `velocity_from_z(z)` — relativistic inverse
- `hubble_velocity(distance, H0)` — `v = H₀ · d`

The `ReferenceDopplerShift` subclass provides the correct physics using the same formulas students are expected to implement.

---

## Synthetic-Only Note

All three modes in the teacher app are **fully synthetic**. Unlike the pendulum mode in Unit 01 (which supported real webcam tracking), there is no camera input — all physics is computed and rendered procedurally. This makes the app deterministic and ideal for classroom projection without any hardware dependency.