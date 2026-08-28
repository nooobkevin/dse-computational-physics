# Unit 04: Electricity and Magnetism

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/em/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes:

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Electrostatics** (Electricity 4a) | Coulomb's law `F = k q₁q₂/r²`; electric field `E = F/q`; field lines for point charges and parallel plates; electric potential `V = k q/r` | Teacher app (`--mode field` — field lines + vector arrows); Manim `ElectricFieldLines` (point charge + parallel plates); Manim `PotentialGradient` (equipotentials ⊥ field); Student exercise (implement `field()` and `potential()`) |
| **Simple circuits** (Electricity 4b) | Current, p.d., resistance, Ohm's law `V = IR`; series/parallel; equivalent resistance | Manim `CircuitComparison` (Kirchhoff laws); Teacher app (`--mode circuit` — current, voltage, power display); Student exercise (implement `resolve()` with nodal analysis) |
| **Kirchhoff's laws** (Electricity 4c) | KCL (ΣI_in = ΣI_out); KVL (ΣV = 0 around loop); internal resistance; power dissipation `P = I²R = V²/R = VI` | Teacher app (circuit mode shows KVL/KCL verification); Manim `CircuitComparison` (numerical validation); Concept questions (internal resistance calculation) |
| **Magnetic fields** (Electricity 4d) | Field of straight wire `B = μ₀I/2πr`; solenoid `B = μ₀NI/l`; force on current-carrying conductor `F = BIl sinθ`; force on moving charge `F = BQv sinθ` | Teacher app (`--mode magnet` — wire field lines with right-hand rule) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Electric field patterns**: `ElectricFieldLines.mp4` — shows field lines radiating from a point charge and the uniform field between parallel plates. Pause on the radial vs uniform field comparison.
- **Equipotentials and gradient**: `PotentialGradient.mp4` — shows equipotential lines (blue circles) and field vectors (yellow arrows) for a point charge. The key takeaway: field vectors are everywhere perpendicular to equipotentials.
- **Kirchhoff's laws**: `CircuitComparison.mp4` — shows a series circuit with computed currents, voltages, and power. Both KCL and KVL are verified numerically.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Field mode** (`--mode field`): shows electric field lines radiating from a point charge. Field-vector arrows are overlaid on a grid with arrow length proportional to log-magnitude. Discuss: why do field lines point away from +q? Why are they closer together near the charge? Where is the field strongest?
- **Circuit mode** (`--mode circuit`): shows a series circuit with a 10V battery and two resistors. Current, voltage drops, and power dissipation are calculated and displayed in real time. Verify KVL and KCL by inspection of the numbers.
- **Magnet mode** (`--mode magnet`): shows concentric circular field lines around a current-carrying wire (current coming out of the screen). Tangential arrows show the right-hand rule direction. Discuss: why is the field strongest near the wire?

### Step 3: Complete the fill-in-the-blank exercise

Students open `em_exercise.py` and implement two classes:

1. **`StudentElectricField`** — implement `field(self, x, y)` and `potential(self, x, y)` using Coulomb's law. The auto-grader checks:
   - The `NotImplementedError` is replaced (immediate fail if not)
   - The field magnitude matches `q/(4πε₀ r²)` to within 1%
   - The potential matches `q/(4πε₀ r)` to within 1%
   - The field direction is radially outward for positive q

2. **`StudentCircuit`** — implement `resolve(self)` using nodal analysis (Kirchhoff's laws + Ohm's law). The auto-grader checks:
   - The `NotImplementedError` is replaced
   - KCL holds at nodes (ΣI_in = ΣI_out)
   - KVL holds around loops (ΣV = 0)
   - Power `P = I²R` is consistent

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

This runs all unit tests including `tests/test_em.py` (electrostatics, circuits, magnetism). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Electric field mode (fully synthetic)
uv run python units/04_em/teacher_app/main.py --mode field

# Circuit mode (fully synthetic)
uv run python units/04_em/teacher_app/main.py --mode circuit

# Magnet mode (fully synthetic)
uv run python units/04_em/teacher_app/main.py --mode magnet

# Headless self-check (no window, for CI)
uv run python units/04_em/teacher_app/main.py --mode field --headless-selfcheck
```

All modes are fully synthetic — no camera required. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all three scenes (requires Docker)
bash units/04_em/manim/render.sh

# Render a specific scene
bash units/04_em/manim/render.sh electric_field_lines

# Low-quality preview (fast)
bash units/04_em/manim/render.sh electric_field_lines -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/04_em/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `electric_field_lines`, `potential_gradient`, `circuit_comparison`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: em_exercise.py)
uv run pytest units/04_em/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/04_em/exercises/test_exercise.py \
    --override-student=units/04_em/exercises/em_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/04_em/exercises/test_exercise.py --selfcheck -v
```

The solution file (`em_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Physics Engine Architecture

The `src/physics_core/em/` package mirrors the `mechanics/` package:

```
src/physics_core/em/
  __init__.py           ← exports all classes
  electrostatics.py     ← ElectricField (abstract) + ReferenceElectricField
  circuits.py           ← Circuit (abstract) + ReferenceCircuit (nodal solver)
  magnetism.py          ← MagneticField (abstract) + ReferenceStraightWire + ReferenceSolenoid
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

All three modes in the teacher app are **fully synthetic**. Unlike the pendulum mode in Unit 01 (which supported real webcam tracking), there is no camera input — all physics is computed and rendered procedurally. This makes the app deterministic and ideal for classroom projection without any hardware dependency.