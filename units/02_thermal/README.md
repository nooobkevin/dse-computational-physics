# Unit 02: Thermal Physics

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of kinetic theory, gas laws, and random walk
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercises** (code) — coding tasks with auto-graders

All three artifacts consume the same `physics_core` engine (`src/physics_core/thermal/`),
so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map (CAF 2026)

This unit targets the following HKDSE Physics (CAF Consultation Draft) outcomes:

### a. Heat transfer — heat and internal energy

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| **Temperature as average KE of random molecular motion**: `KE_avg = 3RT/(2N_A) = (3/2)kT` | Teacher app gas mode (KE display, T_est from equipartition); questions.md (g) |
| **Specific heat capacity**: `c = Q/(mΔT)`, fit experimental data | Exercise `specific_heat_exercise.py` (data-analysis: fit Q vs ΔT → c) |
| **Zeroth law of thermodynamics** / thermal equilibrium | Questions.md (i) |
| **Internal energy** as sum of molecular KE + PE | Questions.md (g) (KE_avg relates T to KE) |

### b. Change of state — latent heat, evaporation

*Out of scope for computational physics toolkit this iteration. Calorimetry labs
(latent heat, phase change, cooling curves) are teacher-led practical activities
and are not covered by CP artifacts. See "Removed-content compliance" below.*

### c. Gases — general gas law and kinetic theory

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| **Boyle's law** (p-V), **pressure law** (p-T), **Charles' law** (V-T) | Teacher app `--mode gas_laws` (P-V curve, P-T curve with absolute-zero extrapolation) |
| **Determine absolute zero** by extrapolation of p-T | Teacher app `--mode gas_laws` (P-T graph with linear fit → absolute zero) |
| **Use Kelvin scale** | Questions.md (g)-(h); teacher app Kelvin discussion; pV = NkT formula |
| **Combine to pV/T = constant; solve problems using pV = nRT** | Teacher app `--mode gas_laws` (Boyle + pressure law verification) |
| **Random motion of molecules** | Teacher app gas mode (live MD trajectories); RandomWalkScene (diffusion model) |
| **Gas pressure from molecular bombardment** | Teacher app gas mode (live P_meas vs P_ideal); PressureStatistical scene |
| **KE_avg = 3RT/(2N_A)** relating T to microscopic KE | Teacher app (equipartition T_est); questions.md (g) |
| **Maxwell-Boltzmann distribution** (interpret temperature change) | MaxwellBoltzmann scene; teacher app MB overlay; questions.md (a) |

### Suggested computational physics activities (CAF lines 1543–1546)

| Activity | Which artifact(s) deliver it |
|---|---|
| **Simulate random walk of molecules** | RandomWalk engine + RandomWalkScene (Manim: many walkers, RMS ring) |
| **Simulate motions of gas molecules + MB distribution** | Teacher app gas mode; MaxwellBoltzmann scene; PressureStatistical scene |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Random walk (diffusion)**: `RandomWalkScene.mp4` — many walkers spread from the origin
  on a 2D grid, with an RMS-radius ring expanding as sqrt(t).  Demonstrates that
  RMS displacement grows as sqrt(N), modelling gas molecule diffusion.
- **Maxwell-Boltzmann distribution**: `MaxwellBoltzmann.mp4` — theoretical MB speed
  distribution at different temperatures, alongside measured distribution.
- **Pressure from collisions**: `PressureStatistical.mp4` — gas box with particles,
  pressure-vs-time graph converging toward the ideal gas law, MB overlay.
- **Numerical methods**: `IntegratorConvergence.mp4` — Euler vs Verlet comparison.

### Step 2: Run the teacher demo app

Open the teacher app and demonstrate the physics live:

- **Gas mode** (`--mode gas`): spawns N particles in a 2D box with velocity arrows.
  Shows speed distribution with MB overlay, live pressure vs ideal gas law, average
  and RMS speed, estimated temperature from equipartition.
- **Gas laws mode** (`--mode gas_laws`): two live graphs — Boyle's law (P vs V, isothermal)
  and pressure law (P vs T, isochoric) with absolute-zero extrapolation.

### Step 3: Complete the fill-in-the-blank exercises

**Gas exercise**: Students implement `_collide_wall` and `_collide_particle`
in `gas_exercise.py`.  The auto-grader checks pressure, energy conservation,
speed distribution, and wall bounce.

**Specific heat exercise**: Students implement `specific_heat_from_fit`,
`energy_to_heat`, and `final_temperature` in `specific_heat_exercise.py`.
The auto-grader checks the linear fit (Q vs ΔT → c), the energy formula Q = mcΔT,
and the temperature change formula.

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
uv run pytest tests/test_thermal.py -v
```

### Teacher app

```bash
# Gas mode (fully synthetic — no webcam needed)
uv run python units/02_thermal/teacher_app/main.py --mode gas

# Gas laws mode (Boyle + absolute-zero extrapolation)
uv run python units/02_thermal/teacher_app/main.py --mode gas_laws

# Headless self-check (no window, for CI)
uv run python units/02_thermal/teacher_app/main.py --mode gas --headless-selfcheck
uv run python units/02_thermal/teacher_app/main.py --mode gas_laws --headless-selfcheck
```

Options:
- `--N <count>` — number of gas particles (default: 200, gas mode only)
- `--T <temperature>` — initial temperature (default: 2.0, gas mode only)

### Manim render

```bash
# Render all scenes (requires Docker)
bash units/02_thermal/manim/render.sh

# Render a specific scene
bash units/02_thermal/manim/render.sh random_walk

# Low-quality preview (fast)
bash units/02_thermal/manim/render.sh random_walk -ql
```

Available scenes: `maxwell_boltzmann`, `integrator_convergence`, `pressure_statistical`,
`random_walk`.

### Exercise / grader

```bash
# Grade the gas exercise
uv run pytest units/02_thermal/exercises/test_exercise.py -v

# Grade the specific heat exercise
uv run pytest units/02_thermal/exercises/test_exercise.py -k TestSpecificHeat -v

# Grade against the solution file (teacher self-check)
uv run pytest units/02_thermal/exercises/test_exercise.py -v \
    --override-student=units/02_thermal/exercises/gas_solution.py

uv run pytest units/02_thermal/exercises/test_exercise.py -v \
    --override-student=units/02_thermal/exercises/specific_heat_solution.py \
    -k TestSpecificHeat

# Full self-check
uv run pytest units/02_thermal/exercises/test_exercise.py --selfcheck -v
```

---

## Key Formulas

| Formula | Context |
|---|---|
| `KE_avg = 3RT/(2N_A) = (3/2)kT` | Average kinetic energy per molecule (CAF required) |
| `C = Q/ΔT` | Heat capacity |
| `c = Q/(mΔT)` | Specific heat capacity |
| `pV = NkT` | Ideal gas law (simulation units) |
| `pV = nRT` | Ideal gas law (real-world constants) |
| `P ∝ 1/V` (Boyle), `P ∝ T` (pressure law), `V ∝ T` (Charles') | Empirical gas laws |
| `RMS = s√N` | Random walk RMS displacement |
| `f(v) = (m/kT) v exp(-mv²/2kT)` (2D) | Maxwell-Boltzmann speed distribution |
| `T(K) = T(°C) + 273.15` | Kelvin-Celsius conversion |

---

## Removed-Content Compliance (CAF Annex 3)

The following topics were **removed** from the CAF curriculum and are NOT
taught by this unit's artifacts:

- **Thermometers** — not covered (removed from CAF)
- **Transfer processes** (conduction, convection, radiation) — not covered
- **PV = (1/3)Nm⟨c²⟩** — not covered (removed from CAF)
- **Real gases** — not covered (simulation uses ideal gas model)

If any existing scene or question references these topics, the relevant code
is preserved but labelled "beyond CAF core" for reference use only.

### Out-of-scope notes

- **Calorimetry labs** (determine specific heat capacity, latent heat,
  cooling curves) are teacher-led practical activities and are out of scope
  for the computational physics toolkit.  The specific heat exercise in
  this unit is a data-analysis CP activity (fitting Q vs ΔT), not a
  calorimetry simulation.
- **Phase change** (melting, boiling, latent heat, evaporation) is not
  covered by any CP artifact this iteration.
- **2D vs 3D note**: The gas simulation uses 2D for visual clarity, but the
  CAF kinetic theory outcomes (KE_avg = 3RT/(2N_A)) are explicitly 3D.
  The Maxwell-Boltzmann distribution helpers in `equations.py` support both
  2D and 3D formulas.  Teachers should be aware of this dimensional mismatch
  when discussing the 3/2 factor in KE_avg.

---

## Architecture Notes

### Random walk engine

`physics_core.thermal.random_walk.RandomWalk` is a standalone engine (no
abstract-base / Reference pattern needed).  It provides:

- Seeded deterministic RNG for reproducibility
- 1D or 2D random walk with configurable step length
- Pre-computed position history and RMS displacement
- Final displacement histogram (for distribution analysis)

### Gas simulation engine

`physics_core.thermal.gas_sim.GasSim` is the abstract base with two
physics hooks: `_collide_wall` and `_collide_particle`.  `ReferenceGasSim`
provides the correct reference implementation.  Extended with:

- `set_volume(new_L)` — moving-wall compression/expansion
- `set_temperature(new_T)` — rescale velocities for heating/cooling
- `gas_law_isothermal_curve(V_values)` — generate P-V data (Boyle's law)
- `gas_law_isochoric_curve(T_values)` — generate P-T data (pressure law)

### Specific heat exercise

The exercise uses standalone functions (no class hierarchy needed for
data-analysis style exercises):

- `specific_heat_from_fit(Q_data, delta_T_data, mass) → (C, c, slope_err)`
- `energy_to_heat(mass, c, delta_T) → Q`
- `final_temperature(Q, mass, c, T_initial) → T_final`