# Unit 05: Physics and Engineering

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-method coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/engineering/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes:

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Total internal reflection** (Engineering a) | Critical angle θ_c = arcsin(n₂/n₁); TIR condition; optical fibres; refractive index n = c/v | Teacher app (`--mode fibre` — TIR/leak visualisation, critical angle display, ray angle control); Manim `TotalInternalReflection` (fibre zigzag ray with TIR labels) |
| **Lasers** (Engineering b) | Population inversion; stimulated vs spontaneous emission; coherence | Teacher app (`--mode laser` — energy level diagram, inversion indicator, photon count); Manim (concept overlay) |
| **Electric motors** (Engineering c) | Motor effect F = B I L; armature rotation; torque τ = N B I L r cos(θ) | Manim `MotorEffect` (B-field, current, force vectors with formula); Teacher app (concept demonstration) |
| **Transformers** (Engineering d) | Vp/Vs = Np/Ns; Ip/Is = Ns/Np; ideal power conservation; step-up/step-down | Teacher app (`--mode transformer` — turns ratio, V/I display, power conservation); Manim `TransformerScene` (schematic with numerical verification) |
| **Semiconductors and diodes** (Engineering e) | Semiconductor physics; diode/LED operation; solar cells; integrated circuits | Student exercise concept questions (semiconductor basics, LED, solar cell applications) |
| **Particle accelerators** (Engineering f) | Cyclotron; linear accelerators; principles of particle acceleration | Student exercise concept questions (cyclotron operation, LINAC principles) |
| **Building computational models** (Scientific Inquiry) | Translate physics equations into code; modify a simulation and observe the effect | Student exercise (fill in `critical_angle` and `total_internal_reflection`); Manim scenes (TIR, transformer, motor effect) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Total internal reflection**: `TotalInternalReflection.mp4` — shows a ray zigzagging inside an optical fibre core. The critical angle formula θ_c = arcsin(n₂/n₁) is displayed. The green ray indicates TIR (θ > θ_c). Pause to discuss why n₁ must be greater than n₂ and how optical fibres transmit light with minimal loss.
- **Transformer**: `TransformerScene.mp4` — shows a schematic transformer with primary and secondary coils. The turns ratio Vp/Vs = Np/Ns and power conservation are displayed numerically.
- **Motor effect**: `MotorEffect.mp4` — shows a current-carrying conductor in a uniform magnetic field. The force vector F = B I L is displayed, along with the torque formula τ = N B I L r cos(θ).

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Fibre mode** (`--mode fibre`): shows an optical fibre cross-section with a ray zigzagging inside. The critical angle is displayed. Use UP/DOWN arrows to change the ray angle — the ray turns green (TIR) when above the critical angle and red (leak) when below. Use this to discuss: what is the critical angle? Why must n₁ > n₂? How does TIR enable long-distance fibre communication?
- **Transformer mode** (`--mode transformer`): shows the turns ratio Np/Ns, primary/secondary voltages, currents, and power. Verify Vp/Vs = Np/Ns and power conservation Vp·Ip = Vs·Is by inspection. Use this to discuss: why do we use transformers? What is a step-up/step-down transformer?
- **Laser mode** (`--mode laser`): shows the energy level diagram (upper/lower levels), population inversion indicator, and laser beam intensity. The photon count builds up as the simulation runs. Use this to discuss: what is population inversion? How does stimulated emission produce coherent light?

### Step 3: Complete the fill-in-the-blank exercise

Students open `engineering_exercise.py` and implement:

1. The `critical_angle` property — return `math.asin(self.n2 / self.n1)`
2. The `total_internal_reflection(self, angle)` method — return `angle > self.critical_angle`

The auto-grader checks:

1. The `NotImplementedError` is replaced (immediate fail if not)
2. The critical angle matches `arcsin(n₂/n₁)` to within 1%
3. A ray above the critical angle undergoes TIR
4. A ray below the critical angle leaks out
5. No TIR is possible when n₁ ≤ n₂

The concept questions in `questions.md` cover critical angle calculations, TIR, n = c/v, transformer ratios, laser coherence, motor effect, and applications.

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

This runs all unit tests including `tests/test_engineering.py` (optical fibres, lasers, motors, transformers). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Fibre mode (fully synthetic — TIR visualisation)
uv run python units/05_engineering/teacher_app/main.py --mode fibre

# Transformer mode (fully synthetic)
uv run python units/05_engineering/teacher_app/main.py --mode transformer

# Laser mode (fully synthetic)
uv run python units/05_engineering/teacher_app/main.py --mode laser

# Headless self-check (no window, for CI)
uv run python units/05_engineering/teacher_app/main.py --mode fibre --headless-selfcheck
```

All modes are fully synthetic — no camera required. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all three scenes (requires Docker)
bash units/05_engineering/manim/render.sh

# Render a specific scene
bash units/05_engineering/manim/render.sh total_internal_reflection

# Low-quality preview (fast)
bash units/05_engineering/manim/render.sh total_internal_reflection -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/05_engineering/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `total_internal_reflection`, `transformer`, `motor_effect`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: engineering_exercise.py)
uv run pytest units/05_engineering/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/05_engineering/exercises/test_exercise.py \
    --override-student=units/05_engineering/exercises/engineering_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/05_engineering/exercises/test_exercise.py --selfcheck -v
```

The solution file (`engineering_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Physics Engine Architecture

The `src/physics_core/engineering/` package mirrors the `mechanics/` and `em/` packages:

```
src/physics_core/engineering/
  __init__.py           ← exports all classes
  optics.py             ← OpticalFibre (abstract) + ReferenceOpticalFibre
  lasers.py             ← Laser (abstract) + ReferenceLaser
  motors.py             ← Motor/Transformer (abstract) + ReferenceMotor/ReferenceTransformer
```

Each abstract base defines physics **hooks** (raising `NotImplementedError`) that subclasses override. The Reference subclasses provide the correct physics using the same formulas students are expected to implement.

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

All three modes in the teacher app are **fully synthetic**. There is no camera input — all physics is computed and rendered procedurally. This makes the app deterministic and ideal for classroom projection without any hardware dependency.