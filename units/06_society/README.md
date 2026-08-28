# Unit 06: Physics and Society

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-method coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/society/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes:

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Radioactive decay** (Society 6a) | Exponential decay law `N = N₀·2^(-t/T)`; half-life concept; Monte Carlo simulation of decay | Teacher app (`--mode decay` — N vs t curve, analytic overlay, half-life marker); Manim `RadioactiveDecay` (decay curve + Monte Carlo dots); Student exercise (implement `decay_probability`) |
| **Alpha, beta, gamma radiation** (Society 6b) | Ionising power (α > β > γ); penetrating power (γ > β > α); absorption by paper/aluminium/lead | Teacher app (`--mode radiation` — bar charts of ionising/penetrating power); Manim `RadiationPenetration` (schematic of shielding) |
| **Nuclear fission and chain reactions** (Society 6c) | Neutron multiplication factor k; critical mass; subcritical/critical/supercritical regimes | Teacher app (`--mode reactor` — neutron population vs generation for k=0.6, 1.0, 1.5); Manim `ChainReaction` (fission schematic + chain reaction generations) |
| **Building computational models** (Scientific Inquiry) | Translate physics equations into code; use Monte Carlo methods to simulate random processes | Student exercise (fill in `decay_probability`); Manim `RadioactiveDecay` (Monte Carlo dots overlaid on analytic curve) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Radioactive decay**: `RadioactiveDecay.mp4` — shows the exponential decay curve `N = N₀·2^(-t/T)` with the analytic curve in green and Monte Carlo simulation dots in orange. The half-life is marked with red dashed lines at `N = N₀/2`. Pause to discuss: why does the Monte Carlo scatter around the analytic curve? What happens if we increase N₀?
- **Radiation penetration**: `RadiationPenetration.mp4` — shows a schematic of alpha, beta, and gamma radiation passing through paper, aluminium, and lead barriers. The key takeaway: penetrating power γ > β > α, ionising power α > β > γ.
- **Chain reaction**: `ChainReaction.mp4` — shows a fission schematic (neutron + U-235 → fission fragments + neutrons + energy) and chain reaction generations. The critical mass concept and neutron multiplication factor k are explained.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Decay mode** (`--mode decay`): shows a Monte Carlo decay simulation with the analytic curve overlaid. The N vs t graph builds in real time as nuclei decay. The estimated half-life is marked with a red dashed line. Use this to discuss: why does the Monte Carlo curve fluctuate? How does increasing N₀ reduce fluctuations? How does the estimated half-life compare to the true value?
- **Radiation mode** (`--mode radiation`): shows bar charts of penetrating power and ionising power for alpha, beta, and gamma radiation. Discuss the inverse relationship and shielding requirements.
- **Reactor mode** (`--mode reactor`): shows neutron population vs generation for three values of k (0.6, 1.0, 1.5). Discuss subcritical, critical, and supercritical regimes. Link to nuclear reactor control.

### Step 3: Complete the fill-in-the-blank exercise

Students open `society_exercise.py` and implement the single method `decay_probability(self, dt)`. The auto-grader checks:

1. The `NotImplementedError` is replaced (immediate fail if not)
2. The decay probability is in [0, 1] for all dt
3. The Monte Carlo simulation approximates the analytic curve to within 5%
4. The estimated half-life is within 10% of the true value

The Monte Carlo vs analytic discussion from Step 1 feeds directly into the concept questions in `questions.md`: why exponential decay, Monte Carlo vs analytic methods, alpha/beta/gamma properties, critical mass, and radiation safety.

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

This runs all unit tests including `tests/test_society.py` (decay simulation, radiation properties). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Decay mode (Monte Carlo simulation)
uv run python units/06_society/teacher_app/main.py --mode decay

# Radiation mode (alpha/beta/gamma properties)
uv run python units/06_society/teacher_app/main.py --mode radiation

# Reactor mode (chain reaction / critical mass)
uv run python units/06_society/teacher_app/main.py --mode reactor

# Headless self-check (no window, for CI)
uv run python units/06_society/teacher_app/main.py --mode decay --headless-selfcheck
```

All modes are fully synthetic — no camera required. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all three scenes (requires Docker)
bash units/06_society/manim/render.sh

# Render a specific scene
bash units/06_society/manim/render.sh radioactive_decay

# Low-quality preview (fast)
bash units/06_society/manim/render.sh radioactive_decay -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/06_society/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `radioactive_decay`, `radiation_penetration`, `chain_reaction`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: society_exercise.py)
uv run pytest units/06_society/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/06_society/exercises/test_exercise.py \
    --override-student=units/06_society/exercises/society_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/06_society/exercises/test_exercise.py --selfcheck -v
```

The solution file (`society_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Physics Engine Architecture

The `src/physics_core/society/` package follows the same pattern as `mechanics/` and `em/`:

```
src/physics_core/society/
  __init__.py           ← exports all classes
  decay.py              ← DecaySim (abstract) + ReferenceDecaySim
```

The abstract base `DecaySim` defines one physics **hook** (`decay_probability(self, dt)`) that raises `NotImplementedError`. The `ReferenceDecaySim` subclass provides the correct physics using both analytic and Monte Carlo methods.

### dt-clamp in Manim updaters

All Manim scenes use the same dt-clamp pattern in their updater functions:

```python
h = min(dt, 1.0 / config.frame_rate)
```

This prevents a Manim edge-case where `dt` can be 0 on frame boundaries, which would cause the simulation to stall.

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render every time.
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.

---

## Synthetic-Only Note

All three modes in the teacher app are **fully synthetic**. Unlike the pendulum mode in Unit 01 (which supported real webcam tracking), there is no camera input — all physics is computed and rendered procedurally. This makes the app deterministic and ideal for classroom projection without any hardware dependency.