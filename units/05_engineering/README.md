# Unit 05: Physics and Engineering

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/engineering/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map (CAF June 2026)

This unit targets the following HKDSE Physics - Physics and Engineering curriculum outcomes:

### a. Electricity generation and power transmission

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| Electromagnetic induction; magnetic flux Φ = BAcosθ; Faraday's Law ε = −ΔΦ/Δt; Lenz's law | Manim `ElectromagneticInduction` (flux graph, induced emf, Lenz arrows); Teacher app (`--mode induction` — magnet position slider, live Φ and ε graphs, Lenz direction) |
| Structure of a simple d.c. motor, d.c. generators and a.c. generators | Manim `MotorEffect` (F = BIL, torque τ = NBILr cosθ) |
| Eddy currents — occurrence and practical uses | Concept questions (eddy currents in transformer cores, regenerative braking) |
| Distinguish operating voltage/current and their peak values of an a.c. system (√2 relationship) | Concept questions (no RMS formula — numerical √2 relationship only) |
| Working principle of a simple transformer; Vp/Vs = Np/Ns | Teacher app (`--mode transformer` — turns ratio, V/I display, power conservation); Manim `TransformerScene` (schematic with numerical verification) |
| Methods for improving transformer efficiency (laminated core, eddy current reduction) | Concept questions |
| Advantages of high-voltage AC transmission; grid system stages (step-up/step-down) | Concept questions |

### b. Domestic electricity and smart living

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| Power rating of electrical appliances; operating current I = P/V; fuse selection (3A, 5A, 13A) | Student exercise `power_rating_exercise.py` (I = P/V, fuse rating, kWh, cost) |
| Kilowatt-hour as a unit of electrical energy; cost of running appliances | Student exercise `power_rating_exercise.py` (E = Pt, cost = E × rate) |
| Basic working principle of common sensors (temperature, light, motion) | Concept questions (thermistor, LDR, PIR — ADJUSTED outcome per Annex 3) |
| Applications of sensing devices for smart living | Concept questions |
| LED light emission (energy change in atomic level, efficiency, endurance) | Concept questions |

### c. Aerospace Science and Engineering

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| Continuity equation vA = constant | Manim `BernoulliPitot` (streamlines speed up in constriction); Teacher app (continuity formula) |
| Bernoulli's principle and Coanda effect for lift | Manim `BernoulliPitot` (pressure drop in throat, pitot tube) |
| Bernoulli's equation P + ρgh + ½ρv² = constant (pitot tube) | Manim `BernoulliPitot` (pitot stagnation → speed readout) |
| Newton's law of gravitation for circular orbits; F = GMm/r² | Manim `OrbitalMotion` (satellite orbit with force/velocity vectors); Teacher app (`--mode orbital`); Engine `ReferenceOrbitalBody` |
| Gravitational potential energy U = −GMm/r; conservation of mechanical energy | Manim `OrbitalMotion` (KE/GPE/total energy bar chart showing conservation) |
| Orbital velocity v_orb = √(GM/r); escape velocity v_esc = √(2GM/r) | Manim `OrbitalMotion` (v_orb and v_esc labels); Student exercise `orbital_exercise.py` |
| Satellite applications (communication, navigation, Earth observation, scientific) | Concept questions |
| Nation's contributions to aerospace technology (Long March, Tiangong, Beidou, etc.) | Concept questions (STSE) |

---

### Items beyond CAF core — enrichment only

The following sub-topics were present in the previous curriculum but are **not in the CAF (June 2026) Unit 05**. Existing code, scenes, and app modes are preserved for reference and enrichment:

| Sub-topic | Status | Artifacts |
|---|---|---|
| **Total internal reflection / optical fibres** | Beyond CAF core — enrichment only | Teacher app (`--mode fibre`); Manim `TotalInternalReflection`; Student exercise (existing `engineering_exercise.py`) |
| **Semiconductors and diodes** | Beyond CAF core — enrichment only | Student exercise concept questions (existing) |
| **Particle accelerators** | Beyond CAF core — enrichment only | Student exercise concept questions (existing) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Orbital motion**: `OrbitalMotion.mp4` — shows a satellite orbiting Earth with velocity and gravitational force vectors, plus an energy bar chart (KE/GPE/total) demonstrating conservation. v_orb and v_esc are displayed.
- **Bernoulli / pitot tube**: `BernoulliPitot.mp4` — shows a horizontal tube with a constriction. Streamlines speed up in the throat, pressure drops, and a pitot tube shows stagnation pressure → speed.
- **Electromagnetic induction**: `ElectromagneticInduction.mp4` — shows a bar magnet moving toward/away from a coil. Magnetic flux and induced emf graphs build in real time. Lenz direction arrows show the induced current.
- **Transformer**: `TransformerScene.mp4` — schematic transformer with turns ratio and power conservation verification.
- **Motor effect**: `MotorEffect.mp4` — current-carrying conductor in a magnetic field with force and torque formulas.

### Step 2: Run the teacher demo app

```bash
# Fibre mode (TIR visualisation — enrichment)
uv run python units/05_engineering/teacher_app/main.py --mode fibre

# Transformer mode (turns ratio, voltage/current, power conservation)
uv run python units/05_engineering/teacher_app/main.py --mode transformer

# Orbital mode (satellite orbit with energy display, altitude slider)
uv run python units/05_engineering/teacher_app/main.py --mode orbital

# Induction mode (magnet position slider, live flux and emf graphs)
uv run python units/05_engineering/teacher_app/main.py --mode induction
```

### Step 3: Complete the fill-in-the-blank exercises

- **Orbital mechanics**: Open `orbital_exercise.py` — implement `gravitational_force`, `orbital_velocity`, `escape_velocity`, `gravitational_potential_energy`, `total_energy`.
- **Power rating**: Open `power_rating_exercise.py` — implement `operating_current`, `fuse_rating`, `energy_kwh`, `cost`.
- **Optical fibre** (enrichment): Open `engineering_exercise.py` — implement `critical_angle`, `total_internal_reflection`.

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
uv run pytest tests/test_engineering.py -v
```

### Teacher app — headless self-check (CI-friendly)

```bash
uv run python units/05_engineering/teacher_app/main.py --mode orbital --headless-selfcheck
uv run python units/05_engineering/teacher_app/main.py --mode induction --headless-selfcheck
uv run python units/05_engineering/teacher_app/main.py --mode fibre --headless-selfcheck
uv run python units/05_engineering/teacher_app/main.py --mode transformer --headless-selfcheck
```

### Manim render

```bash
# Render all scenes (requires Docker)
bash units/05_engineering/manim/render.sh

# Render a specific scene
bash units/05_engineering/manim/render.sh orbital_motion

# Low-quality preview (fast)
bash units/05_engineering/manim/render.sh orbital_motion -ql
```

Available scenes: `total_internal_reflection`, `transformer`, `motor_effect`, `orbital_motion`, `bernoulli_pitot`, `electromagnetic_induction`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercises / grader

```bash
# Grade existing optical fibre exercise
uv run pytest units/05_engineering/exercises/test_exercise.py -v

# Grade orbital exercise
uv run pytest units/05_engineering/exercises/test_orbital_exercise.py -v

# Grade power rating exercise
uv run pytest units/05_engineering/exercises/test_power_rating_exercise.py -v

# Full self-check (all exercises)
uv run pytest units/05_engineering/exercises/ --selfcheck -v

# Grade orbital against solution (teacher)
uv run pytest units/05_engineering/exercises/test_orbital_exercise.py -v \
    --override-student=units/05_engineering/exercises/orbital_solution.py
```

---

## Physics Engine Architecture

The `src/physics_core/engineering/` package reflects the new CAF structure:

```
src/physics_core/engineering/
  __init__.py           ← exports all classes
  optics.py             ← OpticalFibre (abstract) + ReferenceOpticalFibre
  motors.py             ← Motor/Transformer (abstract) + ReferenceMotor/ReferenceTransformer
  orbital.py            ← OrbitSim (abstract) + ReferenceOrbitalBody (NEW — CAF Aerospace c)
  fluid.py              ← FluidFlow (abstract) + ReferenceFluidFlow (NEW — CAF Aerospace c)
  induction.py          ← InductionCoil (abstract) + ReferenceInductionCoil (NEW — CAF Electricity a)
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

All modes in the teacher app are **fully synthetic**. There is no camera input — all physics is computed and rendered procedurally. This makes the app deterministic and ideal for classroom projection without any hardware dependency.