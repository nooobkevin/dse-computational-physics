# Unit 07: Quantum Physics

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of quantum physics concepts
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-method coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/quantum/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes:

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Wave-particle duality** (Quantum b) | Photoelectric effect: E = hf, work function φ, threshold frequency f₀, stopping potential V₀; Compton effect; de Broglie wavelength λ = h/p | Teacher app (photoelectric mode — K_max vs f graph, threshold marker; de Broglie mode — λ vs v for different particles); Manim `Photoelectric` (K_max vs f linear graph, energy balance) |
| **Quantised energy levels** (Quantum c) | Discrete energy levels in atoms; E_n ∝ n² for infinite square well; photon emission/absorption via transitions | Teacher app (well mode — energy level diagram, |ψ_n|² overlay, transition arrows); Manim `EnergyLevels` (E_n levels, wavefunctions, transition) |
| **Wavefunctions and probability** (Quantum d) | ψ as probability amplitude; |ψ|² as probability density; standing-wave picture; nodes and antinodes | Manim `WavefunctionProbability` (ψ and |ψ|² for n=1..4, node visualisation); Teacher app (well mode — probability density curves) |
| **Heisenberg uncertainty principle** (Quantum e) | Δx·Δp ≥ ħ/2; confinement leads to minimum energy | Student exercise (concept questions); Teacher app (well mode — energy level spacing) |
| **Building computational models** (Scientific Inquiry) | Translate physics equations into code; modify a simulation and observe the effect | Student exercise (fill in `energy_level`); Manim scenes (all use `ReferenceQuantumWell`) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Energy levels**: `EnergyLevels.mp4` — shows the infinite square well with quantised energy levels E_n ∝ n², wavefunctions ψ_n(x), probability densities |ψ_n(x)|², and a transition arrow from n=2 to n=1 with photon emission. Pause on the n² spacing to discuss why higher levels are farther apart.
- **Photoelectric effect**: `Photoelectric.mp4` — shows the linear K_max vs f graph, the threshold frequency f₀, and the energy balance hf = K_max + φ. Use this to introduce the photon model and the failure of classical wave theory.
- **Wavefunction and probability**: `WavefunctionProbability.mp4` — cycles through n=1..4 showing ψ(x) and |ψ(x)|², with node counts and the interpretation of |ψ|² as probability density.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Well mode** (`--mode well`): shows energy levels for n=1..6 with probability density overlay on the selected level. Press keys 1-6 to switch levels, 't' to toggle a transition arrow with ΔE and λ values. Use this to discuss quantisation, the n² scaling, and photon emission wavelengths.
- **Photoelectric mode** (`--mode photoelectric`): shows the K_max vs frequency graph with the threshold frequency marked. The energy balance panel shows hf, φ, and K_max values. Use this to discuss the photon model, work function, and stopping potential.
- **de Broglie mode** (`--mode de_broglie`): shows λ = h/p as a function of velocity for electrons, protons, and neutrons. Press 'e', 'p', 'n' to switch particles. Use this to discuss why heavier particles have shorter wavelengths.

### Step 3: Complete the fill-in-the-blank exercise

Students open `quantum_exercise.py` and implement the single method `energy_level(self, n)`. The auto-grader checks:

1. The `NotImplementedError` is replaced (immediate fail if not)
2. E₁ matches h²/(8mL²) to within 0.1%
3. E₂/E₁ = 4 (n² scaling) to within 1%
4. Wavefunction ψ₁(L/2) matches √(2/L) (if overridden)
5. Probability density integrates to ~1 (if wavefunction overridden)

The concept questions in `questions.md` cover photon energy, wave-particle duality, de Broglie wavelength, quantised levels, probability density, and the uncertainty principle.

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

This runs the unit tests in `tests/` (including `test_quantum.py`). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Infinite square well mode (energy levels + probability densities)
uv run python units/07_quantum/teacher_app/main.py --mode well

# Photoelectric effect mode (K_max vs f graph)
uv run python units/07_quantum/teacher_app/main.py --mode photoelectric

# de Broglie wavelength mode (λ vs v for different particles)
uv run python units/07_quantum/teacher_app/main.py --mode de_broglie

# Headless self-check (no window, for CI)
uv run python units/07_quantum/teacher_app/main.py --mode well --headless-selfcheck
```

All modes are fully synthetic (no camera required). The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all three scenes (requires Docker)
bash units/07_quantum/manim/render.sh

# Render a specific scene
bash units/07_quantum/manim/render.sh energy_levels

# Low-quality preview (fast)
bash units/07_quantum/manim/render.sh energy_levels -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/07_quantum/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `energy_levels`, `photoelectric`, `wavefunction_probability`.

Quality flags: `-qh` (high), `-qm` (medium, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: quantum_exercise.py)
uv run pytest units/07_quantum/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/07_quantum/exercises/test_exercise.py \
    --override-student=units/07_quantum/exercises/quantum_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/07_quantum/exercises/test_exercise.py --selfcheck -v
```

The solution file (`quantum_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Quantum Physics Content Summary

### Wave-particle duality

| Concept | Formula | Notes |
|---|---|---|
| Photon energy | E = hf | h = 6.63 × 10⁻³⁴ J·s |
| Work function | φ | Minimum energy to eject electron |
| Threshold frequency | f₀ = φ / h | Below f₀: no emission |
| Max KE | K_max = hf - φ | Linear in f |
| Stopping potential | V₀ = K_max / e | Measured in volts |
| de Broglie wavelength | λ = h / p | p = mv |

### Infinite square well

| Quantity | Formula | Notes |
|---|---|---|
| Energy levels | E_n = n²h² / (8mL²) | n = 1, 2, 3, ... |
| Wavefunction | ψ_n(x) = √(2/L) sin(nπx/L) | 0 ≤ x ≤ L |
| Probability density | \|ψ_n(x)\|² = (2/L) sin²(nπx/L) | ∫₀ᴸ \|ψ\|² dx = 1 |
| Transition energy | ΔE = E_f - E_i | Photon: λ = hc/ΔE |

### Heisenberg uncertainty principle

Δx · Δp ≥ ħ/2

---

## Numerical-Methods Tie-In

The `ReferenceQuantumWell` class in `physics_core.quantum.wavefunctions` provides the exact analytic solutions for the infinite square well. The student exercise asks students to implement the `energy_level` formula, which is then used by all three front-ends:

- **Watch**: the Manim scenes show the wavefunctions and probability densities computed from the engine
- **Do**: the student implements `energy_level(n) = n²h²/(8mL²)`
- **Analyze**: the concept questions explore the n² scaling, transition energies, and the uncertainty principle

### dt-clamp in Manim updaters

All Manim scenes use the same dt-clamp pattern in their updater functions:

```python
h = min(dt, 1.0 / config.frame_rate)
```

This prevents a Manim edge-case where `dt` can be 0 on frame boundaries, which would cause the simulation to stall.

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render every time.
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.
