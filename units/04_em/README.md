# Unit 04: Electricity and Magnetism

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/em/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following CAF (Consultation Draft June 2026) learning outcomes for Topic 4 — Electricity and Magnetism:

| CAF item | Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|---|
| **a** | Electric current, potential, resistance | Define electric current as rate of net flow of charge; distinguish conventional vs electron flow; define p.d. as energy per unit charge; define e.m.f.; define `R = V/I` and `ρ = RA/l`; identify ohmic and non-ohmic I-V characteristics | Teacher app (`--mode vi_graph` — ohmic vs non-ohmic curves, slope = 1/R readout); Concept questions (internal resistance, e.m.f.) |
| **b** | Simple circuits and electrical power — Kirchhoff's Laws, equivalent resistance, internal resistance, power | KCL (ΣI=0) and KVL (ΣV=0); series/parallel; equivalent resistance; e.m.f. vs terminal voltage; `P = VI = I²R = V²/R` | Manim `CircuitComparison` (KCL+KVL verification); Teacher app (`--mode circuit` — series; `--mode parallel` — parallel circuit with KCL badge); Student exercise (implement `resolve()` with nodal analysis); Concept questions |
| **c** | Electrostatics — Coulomb's law, electric field, field strength | Coulomb's law `F = Q₁Q₂/(4πε₀r²)`; electric field of point charge and parallel plates; field lines; `E = F/q`; `E = Q/(4πε₀r²)`; `E = V/d` | Manim `ElectricFieldLines` (point charge + parallel plates); Manim `PotentialGradient` (equipotentials); Teacher app (`--mode field` — field lines + vector arrows); Student exercise (implement `field()` and `potential()`) |
| **d** | Magnetic fields — magnetic force, current-carrying conductor, moving charge | Field patterns (wire, coil, solenoid); `B = μ₀I/(2πr)`; `B = μ₀NI/l`; `F = BIl sinθ`; `F = BQv sinθ`; right-hand rule; circular motion `r = mv/(qB)` | Manim `MagneticForce` (charged particle in B-field, circular arc, opposite-sign contrast); Teacher app (`--mode magnet` — wire field lines; `--mode solenoid` — uniform field with current slider); Student exercise (implement `magnetic_force()` and `orbit_radius()`); Engine `ReferenceMovingCharge` + `ReferenceBarMagnet` |

### Status

| CAF item | Coverage |
|---|---|
| a — Current, potential, resistance | PARTIAL (vi_graph mode added; resistivity concept pending) |
| b — Circuits and power | COVERED (series + parallel now available) |
| c — Electrostatics | COVERED |
| d — Magnetic fields | PARTIAL (moving charge + solenoid added; coil and motor pending) |

### Removed-content compliance (Annex 3)

The following topics were **removed** from the CAF consultation draft for E&M and are **not** included in this unit:
- Variation of current with applied potential difference for **different materials** (basic ohmic vs non-ohmic identification is retained)
- Effect of temperature on resistance of metals and semiconductors
- Effect of resistance of ammeters and voltmeters on measurements
- Root-mean-square (RMS) value of alternating current

If any of these appear in discussion, they are labelled "beyond CAF core" in the materials.

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Electric field patterns**: `ElectricFieldLines.mp4` — field lines radiating from a point charge and the uniform field between parallel plates.
- **Equipotentials and gradient**: `PotentialGradient.mp4` — equipotentials (blue circles) and field vectors (yellow arrows) for a point charge.
- **Kirchhoff's laws**: `CircuitComparison.mp4` — series circuit with KCL, KVL, and power dissipation verified numerically.
- **Magnetic force on a moving charge**: `MagneticForce.mp4` — a charged particle enters a uniform B-field region; straight line outside, circular arc inside with radius `r = mv/(qB)`. A second charge with opposite sign curves in the opposite direction.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Field mode** (`--mode field`): electric field lines and vector arrows for a point charge.
- **Circuit mode** (`--mode circuit`): series circuit with current, voltage drops, and power.
- **Magnet mode** (`--mode magnet`): concentric circular field lines around a current-carrying wire.
- **Solenoid mode** (`--mode solenoid`): uniform B-field inside a solenoid with adjustable current slider. Shows `B = μ₀NI/L`.
- **V-I graph mode** (`--mode vi_graph`): ohmic (straight line) vs non-ohmic (filament lamp curve) I-V characteristics with live slope = 1/R readout.
- **Parallel circuit mode** (`--mode parallel`): two-branch parallel circuit with KCL verification badge at the junction node.

### Step 3: Complete the fill-in-the-blank exercise

Students open `em_exercise.py` and implement three classes:

1. **`StudentElectricField`** — implement `field()` and `potential()` using Coulomb's law.
2. **`StudentCircuit`** — implement `resolve()` using nodal analysis (Kirchhoff + Ohm).
3. **`StudentMagnetism`** — implement `magnetic_force()` (`F = |q|vB sinθ`) and `orbit_radius()` (`r = mv/(|q|B)`).

The auto-grader checks each implementation for numerical correctness.

### Step 4: Concept questions

Students answer the concept questions in `exercises/questions.md`:

- **Questions (a)–(c)**: Coulomb's inverse-square law, electric field vs potential, equipotential surfaces.
- **Questions (d)–(f)**: Kirchhoff's laws, series circuits, internal resistance and terminal voltage.
- **Questions (g)–(i)**: Lorentz force on a moving charge, right-hand rule, circular motion in a magnetic field (`r = mv/(qB)`, `T = 2πm/(qB)`).

The teacher key (`teacher_key.md`) is gitignored — students must not see it.

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

This runs all unit tests including `tests/test_em.py` (electrostatics, circuits, magnetism).

### Teacher app

```bash
# Electric field mode
uv run python units/04_em/teacher_app/main.py --mode field

# Circuit mode (series)
uv run python units/04_em/teacher_app/main.py --mode circuit

# Magnet mode (straight wire)
uv run python units/04_em/teacher_app/main.py --mode magnet

# Solenoid mode (with current slider)
uv run python units/04_em/teacher_app/main.py --mode solenoid

# V-I graph mode (ohmic vs non-ohmic)
uv run python units/04_em/teacher_app/main.py --mode vi_graph

# Parallel circuit mode (with KCL check)
uv run python units/04_em/teacher_app/main.py --mode parallel

# Headless self-check (no window, for CI)
uv run python units/04_em/teacher_app/main.py --mode solenoid --headless-selfcheck
```

All modes are fully synthetic — no camera required. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all scenes (requires Docker)
bash units/04_em/manim/render.sh

# Render a specific scene
bash units/04_em/manim/render.sh magnetic_force

# Low-quality preview (fast)
bash units/04_em/manim/render.sh magnetic_force -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/04_em/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `electric_field_lines`, `potential_gradient`, `circuit_comparison`, `magnetic_force`.

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

The `src/physics_core/em/` package contains four modules:

```
src/physics_core/em/
  __init__.py           ← exports all classes
  electrostatics.py     ← ElectricField (abstract) + ReferenceElectricField
  circuits.py           ← Circuit (abstract) + ReferenceCircuit (nodal solver)
  magnetism.py          ← MagneticField (abstract) + ReferenceStraightWire
                          + ReferenceSolenoid + MovingCharge (abstract)
                          + ReferenceMovingCharge + ReferenceBarMagnet
```

Each abstract base defines physics **hooks** (raising `NotImplementedError`) that subclasses override. `ReferenceMovingCharge` provides the correct Lorentz-force physics (`F = |q|vB sinθ`, `r = mv/(|q|B)`) and uses the Boris algorithm for trajectory integration. `ReferenceBarMagnet` models a bar magnet as a magnetic dipole with field `B = (μ₀/4π)[3(m·r̂)r̂ - m]/r³`.

### dt-clamp in Manim updaters

All Manim scenes use the same time pattern: a `t = [0.0]` list updated from `self.time` in the driver updater, with `always_redraw` lambdas that rebuild visuals from the current `t[0]`.

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render every time.
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.

---

## Synthetic-Only Note

All modes in the teacher app are **fully synthetic**. Unlike the pendulum mode in Unit 01 (which supported real webcam tracking), there is no camera input — all physics is computed and rendered procedurally. This makes the app deterministic and ideal for classroom projection without any hardware dependency.

---

## CAF Compliance Notes

### Kirchhoff's laws — adjusted learning outcomes

The CAF (June 2026, Annex 3 line 4358) notes that Kirchhoff's laws have "adjusted" learning outcomes. The toolkit's treatment (KCL + KVL with nodal analysis) is robust and exceeds whatever the adjustment entails. The `ReferenceCircuit` engine supports arbitrary topologies (series, parallel, mixed), and the student exercise requires implementing a general nodal solver.

### Removed content (Annex 3, lines 4290–4295)

The following topics were **removed** from the CAF for E&M and are **not** included in this unit:

- Variation of current with applied potential difference for **different materials** (basic ohmic vs non-ohmic identification is retained — see `--mode vi_graph`)
- Effect of temperature on resistance of metals and semiconductors
- Effect of resistance of ammeters and voltmeters on measurements
- Root-mean-square (RMS) value of alternating current

If any of these appear in discussion, they are labelled "beyond CAF core" in the materials.

### Integrated content (Annex 3)

- **Electromagnetic induction, AC, and transformers** were moved to Unit 05 (Physics & Engineering) per Annex 3 reorganisation (lines 4341–4345). This unit does **not** cover them.

### Out-of-scope (teacher-led activities)

The following CAF-suggested activities are hands-on/experiential and outside the computational toolkit's scope:

- Breadboard circuit construction and testing
- Electrostatic generation equipment (charging by friction, electroscopes)
- Bouncing metal ball between parallel charged plates
- Current balance measurement of magnetic field strength
- Cathode ray tube demonstration of electron-beam deflection
- Maxwell's story and the history of electromagnetism

These should be delivered as complementary teacher-led activities.

### Computational Physics alignment (CAF §2.2.2)

The CAF suggests "simulate the electric field or magnetic field patterns" (line 2078) as the CP activity for this topic. The toolkit exceeds this with:

| CP activity | Which artifact(s) deliver it |
|---|---|
| Simulate electric field patterns | Manim `ElectricFieldLines`; Teacher app `--mode field`; Student exercise `StudentElectricField` |
| Simulate magnetic field patterns | Manim `MagneticForce`; Teacher app `--mode magnet` / `--mode solenoid`; Student exercise `StudentMagnetism` |
| Build computational models: translate physics to code (line 629) | Student exercises (fill-in-the-blank hooks for Coulomb, circuit nodal analysis, Lorentz force) |
| Computer-assisted data analysis (line 659) | V-I characteristic comparison (`--mode vi_graph`); concept questions with numerical computation |