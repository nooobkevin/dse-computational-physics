# Unit 07: Quantum Physics

> **中文概覽**：本單元涵蓋量子物理的核心概念，包括盧瑟福散射、光電效應、波耳氫原子模型、德布羅意波長、無限方阱、量子疊加與海森堡不確定原理，以及雷射。所有教材均共用同一套 `physics_core` 引擎，確保動畫、教師示範程式與學生練習的物理內容完全一致。

## Overview 概覽

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of quantum physics concepts
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — coding tasks with auto-graders

All three artifacts consume the same `physics_core` engine (`src/physics_core/quantum/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map 課程學習成果對照

This unit targets the following HKDSE Physics curriculum outcomes (CAF 2026 Consultation Draft):

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **a. Atomic Model** | Rutherford's atomic model from scattering experiments; limitations for line spectra | Engine `RutherfordScattering`; Manim `RutherfordScattering`; Teacher app (`--mode rutherford`); Student exercise |
| **b. Photoelectric effect** | E = hf, work function φ, threshold frequency f₀, stopping potential V₀; photons as light quanta | Teacher app (`--mode photoelectric` — K_max vs f graph, threshold marker); Manim `Photoelectric` (K_max vs f linear graph, energy balance) |
| **c. Bohr's atomic model of hydrogen (PRIMARY CAF model)** | Discrete energy levels E_n = -13.6/n² eV; line spectra; transition wavelengths (Lyman, Balmer); ionisation vs excitation | Engine `BohrHydrogen`; Manim `HydrogenSpectra` (energy-level diagram + Balmer series wavelength axis); Teacher app (`--mode hydrogen` — level selector, emission/absorption, photon λ); Student `StudentBohrHydrogen` exercise |
| **d. Wave-particle duality** | de Broglie wavelength λ = h/p; electron diffraction; wave/particle evidence | Teacher app (`--mode de_broglie` — λ vs v for different particles); Concept questions |
| **d. Wave-particle duality (infinite square well)** | Quantised energy levels E_n ∝ n²h²/(8mL²) as a simplified pedagogical model; wavefunctions ψ_n(x); probability density | Manim `EnergyLevels` (E_n levels, wavefunctions, transition); Teacher app (`--mode well` — energy level diagram, |ψ_n|² overlay, transition arrows); Student `StudentQuantumWell` exercise |
| **e. Probabilistic nature & Heisenberg UP** | |ψ(x)|² as probability density; quantum superposition |ψ⟩ = a|0⟩ + b|1⟩; measurement collapse; Δx·Δp ≥ ħ/2 | Manim `WavefunctionProbability` (ψ and |ψ|² for n=1..4); Manim `SuperpositionState` (bars, measurement, histogram); Teacher app (`--mode uncertainty` — Δx·Δp slider, minimum energy); Concept questions |
| **Laser (moved from Unit 05)** | Population inversion, stimulated emission, coherent light | Engine `Laser`/`ReferenceLaser`; Teacher app (`--mode laser` — cavity, inversion display, photon count) |
| **Building computational models** (Scientific Inquiry) | Translate physics equations into code; modify a simulation and observe the effect | Student exercises (fill in energy_level, transition_wavelength, ionisation_energy); Manim scenes (all use reference engines) |

---

## Lesson Flow (Suggested Sequence) 教學流程（建議次序）

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Rutherford scattering**: `RutherfordScattering.mp4` — alpha particles with different impact parameters approach a gold nucleus; trajectories show how b determines the scattering angle θ; the head-on particle backscatters at 180°. Use this to introduce the nuclear model of the atom.
- **Hydrogen spectra**: `HydrogenSpectra.mp4` — Bohr energy levels n=1..5 with ionisation limit; transition arrows for the Balmer series; the visible Balmer lines (Hα 656 nm red, Hβ 486 nm cyan, Hγ 434 nm blue, Hδ 410 nm violet) drawn to scale on a wavelength axis.
- **Superposition and measurement**: `SuperpositionState.mp4` — |ψ⟩ = a|0⟩ + b|1⟩ with probability-weight bars; a measurement "click" collapses the state to |0⟩ or |1⟩; repeated measurements build a histogram that converges to the expected distribution.
- **Energy levels** (square well): `EnergyLevels.mp4` — shows the infinite square well with quantised energy levels E_n ∝ n², wavefunctions ψ_n(x), probability densities |ψ_n(x)|², and transition arrows.
- **Photoelectric effect**: `Photoelectric.mp4` — shows the linear K_max vs f graph, the threshold frequency f₀, and the energy balance hf = K_max + φ.
- **Wavefunction and probability**: `WavefunctionProbability.mp4` — cycles through n=1..4 showing ψ(x) and |ψ(x)|², with node counts.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Rutherford mode** (`--mode rutherford`): shows the gold nucleus at centre, alpha particle trajectory computed from the impact parameter b. ↑/↓ adjusts b and the scattering angle θ updates in real time. Use this to demonstrate the Rutherford formula θ(b).
- **Hydrogen mode** (`--mode hydrogen`): shows the Bohr energy levels n=1..10. Select a level and a target level; the app shows the transition arrow, ΔE in eV, and the photon wavelength. Toggle between emission and absorption.
- **Well mode** (`--mode well`): shows energy levels for n=1..6 with probability density overlay. Keys 1-6 switch levels, 't' toggles a transition arrow with ΔE and λ values.
- **Photoelectric mode** (`--mode photoelectric`): shows the K_max vs frequency graph with threshold frequency marked.
- **de Broglie mode** (`--mode de_broglie`): shows λ = h/p as a function of velocity for electrons, protons, and neutrons.
- **Laser mode** (`--mode laser`): shows cavity, population inversion, and photon count building up via stimulated emission.
- **Uncertainty mode** (`--mode uncertainty`): shows Δx·Δp ≥ ħ/2 graphically with a slider for well width L. The minimum kinetic energy from confinement is displayed.

### Step 3: Complete the fill-in-the-blank exercises

Students complete up to two exercises:

**Exercise 1 — Bohr hydrogen atom (`hydrogen_exercise.py`)**
Students implement three methods:
1. `energy_level(self, n)`: E_n = -13.6 eV / n²
2. `transition_wavelength(self, n_i, n_f)`: λ = hc / |ΔE|
3. `ionisation_energy(self, n)`: E_ion = 13.6 eV / n²

The auto-grader checks numerical values: E₁, n² scaling, Lyman-alpha wavelength, Balmer-alpha wavelength, and ionisation energies.

**Exercise 2 — Infinite square well (`quantum_exercise.py`)**
Students implement `energy_level(self, n)`: E_n = n²h²/(8mL²).

---

## How to Run Each Artifact 如何執行各項教材

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

This runs all unit tests in `tests/` (including `test_quantum.py` with 61+ tests). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Infinite square well mode (energy levels + probability densities)
uv run python units/07_quantum/teacher_app/main.py --mode well

# Photoelectric effect mode (K_max vs f graph)
uv run python units/07_quantum/teacher_app/main.py --mode photoelectric

# de Broglie wavelength mode (λ vs v for different particles)
uv run python units/07_quantum/teacher_app/main.py --mode de_broglie

# Laser mode (population inversion and stimulated emission)
uv run python units/07_quantum/teacher_app/main.py --mode laser

# Rutherford scattering mode (impact parameter slider, live trajectory)
uv run python units/07_quantum/teacher_app/main.py --mode rutherford

# Bohr hydrogen mode (energy level diagram, transitions)
uv run python units/07_quantum/teacher_app/main.py --mode hydrogen

# Heisenberg uncertainty mode (Δx·Δp slider)
uv run python units/07_quantum/teacher_app/main.py --mode uncertainty

# Headless self-check (no window, for CI)
uv run python units/07_quantum/teacher_app/main.py --mode well --headless-selfcheck
```

All modes are fully synthetic (no camera required). The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all six scenes (requires Docker)
bash units/07_quantum/manim/render.sh

# Render a specific scene
bash units/07_quantum/manim/render.sh rutherford_scattering

# Low-quality preview (fast)
bash units/07_quantum/manim/render.sh rutherford_scattering -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/07_quantum/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `energy_levels`, `photoelectric`, `wavefunction_probability`, `rutherford_scattering`, `hydrogen_spectra`, `superposition_state`.

Quality flags: `-qh` (high), `-qm` (medium, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the Bohr hydrogen exercise
uv run pytest units/07_quantum/exercises/test_exercise.py -v -k Bohr \
    --override-student=units/07_quantum/exercises/hydrogen_solution.py

# Grade the quantum well exercise
uv run pytest units/07_quantum/exercises/test_exercise.py -v -k QuantumWell \
    --override-student=units/07_quantum/exercises/quantum_solution.py

# Grade the default exercise (quantum_exercise.py)
uv run pytest units/07_quantum/exercises/test_exercise.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/07_quantum/exercises/test_exercise.py --selfcheck -v
```

Solution files (`quantum_solution.py`, `hydrogen_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Quantum Physics Content Summary 量子物理內容摘要

### a. Atomic Model — Rutherford scattering

| Concept | Formula | Notes |
|---|---|---|
| Coulomb repulsion | F = k Z₁ Z₂ e² / r² | k = 1/(4πϵ₀) |
| Scattering angle | θ(b) = 2·atan(k/(2·E·b)) | k = Z₁Z₂e²/(4πϵ₀) |
| Head-on (b→0) | θ → π (180°) | Full backscattering |
| Large b | θ → 0 | No deflection |

### b. Photoelectric effect

| Concept | Formula | Notes |
|---|---|---|
| Photon energy | E = hf | h = 6.63 × 10⁻³⁴ J·s |
| Work function | φ | Minimum energy to eject electron |
| Threshold frequency | f₀ = φ / h | Below f₀: no emission |
| Max KE | K_max = hf - φ | Linear in f |
| Stopping potential | V₀ = K_max / e | Measured in volts |

### c. Bohr's atomic model of hydrogen (PRIMARY CAF model)

| Quantity | Formula | Notes |
|---|---|---|
| Energy levels | E_n = -13.6 eV / n² | n = 1, 2, 3, ... |
| Ground state | E₁ = -13.6 eV | Binding energy |
| Transition wavelength | 1/λ = R_H (1/n_f² − 1/n_i²) | R_H = 1.097×10⁷ m⁻¹ |
| Lyman-alpha | λ ≈ 121.6 nm (UV) | n=2 → n=1 |
| Balmer-alpha (Hα) | λ ≈ 656.3 nm (red) | n=3 → n=2 |
| Balmer-beta (Hβ) | λ ≈ 486.1 nm (cyan) | n=4 → n=2 |
| Balmer-gamma (Hγ) | λ ≈ 434.0 nm (blue) | n=5 → n=2 |
| Balmer-delta (Hδ) | λ ≈ 410.2 nm (violet) | n=6 → n=2 |
| Ionisation energy | E_ion = 13.6 eV / n² | From level n |

### d. Wave-particle duality & Infinite square well

| Quantity | Formula | Notes |
|---|---|---|
| de Broglie wavelength | λ = h / p | p = mv |
| Square well energy | E_n = n²h² / (8mL²) | n = 1, 2, 3, ... |
| Wavefunction | ψ_n(x) = √(2/L) sin(nπx/L) | 0 ≤ x ≤ L |
| Probability density | |ψ_n(x)|² = (2/L) sin²(nπx/L) | ∫₀ᴸ |ψ|² dx = 1 |

### e. Heisenberg uncertainty principle

| Concept | Formula | Notes |
|---|---|---|
| Position-momentum | Δx · Δp ≥ ħ/2 | ħ = h/(2π) |
| Minimum KE from confinement | E_min ≈ (Δp)²/(2m) ≈ ħ²/(8mΔx²) | Link to square well E₁ |

### Laser (moved from Unit 05)

| Concept | Notes |
|---|---|
| Population inversion | N_upper > N_lower required for lasing |
| Stimulated emission | Coherent photons, proportional to (N_upper − N_lower) |
| Pump rate | Rate of atoms promoted to upper level |

---

## Physics Engines 物理引擎

| Module | Engine class | Reference class | Purpose |
|---|---|---|---|
| `quantum/wavefunctions.py` | `QuantumWell` | `ReferenceQuantumWell` | Infinite square well (pedagogical model) |
| `quantum/photoelectric.py` | `PhotoElectric` | (no abstract base needed) | Photoelectric effect calculator |
| `quantum/lasers.py` | `Laser` | `ReferenceLaser` | Population inversion, stimulated emission |
| `quantum/rutherford.py` | `RutherfordScattering` | `ReferenceRutherfordScattering` | Coulomb scattering θ(b), trajectories |
| `quantum/bohr.py` | `BohrHydrogen` | (self-contained) | Bohr hydrogen: E_n, transitions, ionisation |

---

## Numerical-Methods Tie-In 數值方法關聯

The quantum simulation engines provide analytic solutions (no ODE integration is needed):

- **Rutherford scattering**: The scattering angle θ(b) = 2·atan(k/(2·E·b)) is a closed-form result from the Coulomb deflection integral. The trajectory is the analytical hyperbola.
- **Bohr hydrogen**: Energy levels are given by the closed-form formula E_n = -13.6 eV / n². No numerical integration is required.
- **Square well**: All quantities are analytic — energy levels, wavefunctions, probability densities, and transition wavelengths are computed from closed-form expressions.
- **Superposition**: The probabilistic measurement model uses a random number generator seeded for deterministic Manim renders.

### Manim animation patterns

All Manim scenes use the same proven pattern (see `units/03_waves/manim/scenes/superposition_standing.py`):

```python
t: list[float] = [0.0]
def updater(_mob: Mobject, dt: float) -> None:
    t[0] = self.time
driver = Mobject()
driver.add_updater(updater)
```

- Visible curves are `always_redraw` mobjects rebuilt every frame as a single VMobject with `set_points_as_corners` (never VGroup of Lines).
- The authoritative time is `self.time` (Manim's video clock), not accumulated from `dt`.
- This pattern avoids the ManimCE cairo-renderer bug where submobjects added inside an updater are frozen.

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render every time.
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.
- Every new/changed MP4 must pass `uv run python tools/verify_video_motion.py <mp4> --strict`.
