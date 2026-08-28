# DSE Computational Physics Toolkit

A curriculum-aligned toolkit for teaching HKDSE Physics through computation. Each unit delivers three artifacts that share one physics engine: a **Manim animation** (watch), a **teacher demo app** (interact), and a **student fill-in-the-blank exercise** (code).

---

## Core Concepts

### Three artifacts, one engine

```
src/physics_core/          ← shared physics engine
  integrators.py             Euler / Verlet ODE steppers
  errors.py                  percent error, sig figs, uncertainty formatting
  mechanics/
    pendulum.py              PendulumSim (abstract) + ReferencePendulumSim
    projectile.py            ProjectileSim (abstract) + ReferenceProjectileSim
    circular.py              CircularMotion (uniform circular kinematics)

units/01_mechanics/
  manim/scenes/              ← Manim animations (watch)
  teacher_app/               ← OpenCV demo app (interact)
  exercises/                 ← Student fill-in exercise + auto-grader (code)
```

### PhysicsEngine.step(dt) design

Every simulation class follows the same pattern:

- An **abstract base** (e.g. `PendulumSim`) defines framework methods (`step(dt)`, `state`, `position`, `energy`) and one or more **physics hooks** that raise `NotImplementedError` (e.g. `angular_acceleration(self, theta, omega)`).
- A **Reference subclass** (e.g. `ReferencePendulumSim`) overrides the hooks with the correct physics.
- All three front-ends — Manim updater, OpenCV app loop, student exercise — import and call the same base class. The student exercise is the only one that subclasses the base directly; the Manim scenes and teacher app use the Reference implementation.

This means the physics is identical across every artifact. A student who completes the exercise has written code that the Manim renderer and teacher app also use.

---

## Quickstart for Teachers

### Prerequisites

- Python 3.11 or later
- [`uv`](https://docs.astral.sh/uv/) (package manager)
- Docker (for Manim rendering only)

### Setup

```bash
# Install dependencies
uv sync

# Run the engine unit tests
uv run pytest
```

### Run the teacher demo app

```bash
# Pendulum mode (webcam or synthetic fallback)
uv run python units/01_mechanics/teacher_app/main.py --mode pendulum

# Circular motion mode
uv run python units/01_mechanics/teacher_app/main.py --mode circular

# Projectile motion mode
uv run python units/01_mechanics/teacher_app/main.py --mode projectile

# Headless self-check (no window, for CI)
uv run python units/01_mechanics/teacher_app/main.py --mode pendulum --headless-selfcheck
```

### Render Manim animations

```bash
# Render all scenes (requires Docker)
bash units/01_mechanics/manim/render.sh

# Low-quality preview
bash units/01_mechanics/manim/render.sh shm_projection -ql
```

Output MP4 files land in `units/01_mechanics/manim/output/`.

### Run the exercise grader

```bash
# Grade the student's exercise
uv run pytest units/01_mechanics/exercises/test_exercise.py -v

# Teacher self-check against the solution
uv run pytest units/01_mechanics/exercises/test_exercise.py \
    --override-student=units/01_mechanics/exercises/pendulum_solution.py -v
```

---

## Unit Index

Aligned to the **CAF (Secondary 4–6) Consultation Draft (June 2026)** — each unit's README carries the detailed learning-outcome map and curriculum-alignment notes.

| Unit | Directory | Topics |
|---|---|---|
| 01 — Mechanics | `units/01_mechanics/` | Kinematics, projectile (with drag), SHM + damping & resonance, circular motion, free fall on different planets, numerical integration |
| 02 — Thermal Physics | `units/02_thermal/` | Kinetic theory, Maxwell-Boltzmann distribution, gas laws + absolute zero, molecular random walk, specific heat (data analysis) |
| 03 — Waves | `units/03_waves/` | Superposition, standing waves, Young's double-slit + intensity, polarisation (Malus), EM spectrum, ultrasound ranging, inverse-square data analysis |
| 04 — Electricity & Magnetism | `units/04_em/` | Electric field, series/parallel circuits + KCL, I-V characteristics, magnetic force on moving charges, solenoid & field patterns |
| 05 — Physics & Engineering | `units/05_engineering/` | Orbital motion of celestial bodies, Bernoulli & pitot tube, electromagnetic induction, transformers, domestic electricity, (beyond-core: TIR/fibres, semiconductors) |
| 06 — Physics & Society | `units/06_society/` | Radioactivity & half-life, Monte Carlo decay, fission chain reactions, energy sources (fission/fusion/solar/wind), radioisotope uses |
| 07 — Quantum Physics | `units/07_quantum/` | Rutherford scattering, Bohr hydrogen model (primary) + line spectra, photoelectric effect, de Broglie wavelength, square well, superposition & uncertainty, laser |
| 08 — Astrophysics & Relativity | `units/08_astrophysics/` | Doppler redshift, Hubble's law + rotation curves (dark matter), stellar life cycle, H-R diagram & black-body radiation, parallax, time dilation & spacetime diagrams, Big Bang |
| 09 — Scientific Inquiry | `units/09_inquiry/` | Data analysis, linearisation, uncertainty & outliers, curve fitting, complex systems (epidemic model), engineering design loop |

Each unit follows the layout convention:

```
units/NN_<unit>/
  README.md          ← per-unit documentation (outcome map, lesson flow, commands)
  manim/
    scenes/            ← Manim scene Python files
    render.sh          ← Docker-based render script
    output/            ← rendered MP4 files (gitignored)
  teacher_app/
    main.py            ← OpenCV demo app entry point
    ...                ← mode-specific modules
  exercises/
    <topic>_exercise.py   ← student fill-in-the-blank (NotImplementedError hooks)
    <topic>_solution.py   ← hidden solution (gitignored)
    test_exercise.py      ← auto-grader
    conftest.py           ← pytest fixtures (--override-student, --selfcheck)
    questions.md          ← concept questions
    teacher_key.md        ← answer key (gitignored)
```

---

## HKDSE Curriculum Coverage

The toolkit maps to the Computational Physics activities proposed in the **CAF (Secondary 4–6) Consultation Draft (June 2026)**. All nine topics below are implemented as units.

### 1. Mechanics ✓ unit 01

- Use motion video analysis software or applications to analyze different motions.
- Use computer programming and simulation to model various motions (e.g., free fall on different planets, projectile motion with or without air resistance, simple harmonic motion with or without damping).

### 2. Thermal Physics ✓ unit 02

- Simulate random motion of molecules.
- Simulate the motion of gas molecules in a container to demonstrate the Maxwell-Boltzmann distribution.

### 3. Wave Motion ✓ unit 03

- Simulate the superposition of transverse waves.
- Simulate the formation of standing waves.

### 4. Electricity and Magnetism ✓ unit 04

- Simulate electric and magnetic field patterns.

### 5. Physics and Engineering ✓ unit 05

- Simulate orbital motion of celestial bodies.

### 6. Physics and Society ✓ unit 06

- Conduct dice-throwing/computational physics experiments to simulate the radioactive decay of isotopes.
- Simulate nuclear decay processes.

### 7. Quantum Physics ✓ unit 07

- Simulate Rutherford's scattering experiment.

### 8. Astrophysics and Relativity ✓ unit 08

- Simulate the Doppler effect.
- Simulate simultaneity and time dilation in different frames of reference.

### 9. Scientific Inquiry in Physics ✓ unit 09

- Write a program to simulate simple harmonic motion and investigate the damping coefficient.
- Write a program to simulate complex systems to demonstrate societal processes, such as forest fires, disease transmission, and crowd control.

---

## Adding a New Unit

See `units/_NEW_UNIT_TEMPLATE.md` for the step-by-step replication template. The template covers:

1. Adding a new domain under `src/physics_core/<domain>/` (DI hooks + Reference implementation)
2. Creating Manim scenes that import the engine
3. Adding a teacher app mode
4. Writing the student exercise with auto-grader
5. Writing the unit README with outcome map and lesson flow

---

## Project Structure

```
.
├── pyproject.toml          # uv / hatchling config (pythonpath = ["src"])
├── src/
│   └── physics_core/       # shared physics engine (one domain per topic)
│       ├── integrators.py  # euler_step, verlet_step
│       ├── errors.py       # percent_error, sig_figs, etc.
│       ├── mechanics/      # pendulum, projectile, circular
│       ├── thermal/        # gas simulation, Maxwell-Boltzmann, random walk
│       ├── waves/          # superposition, standing waves, intensity
│       ├── em/             # fields, circuits, magnetism
│       ├── engineering/    # fibres, transformers, orbital, fluid, induction
│       ├── society/        # decay, reactor, energy sources
│       ├── quantum/        # wavefunctions, photoelectric, rutherford, bohr, lasers
│       ├── astrophysics/   # doppler, hubble, relativity, hr_diagram
│       └── inquiry/        # linearisation, uncertainty, complex systems
├── tests/                  # engine unit tests
├── units/                  # per-unit artifacts (01..09)
│   ├── 01_mechanics/
│   └── _NEW_UNIT_TEMPLATE.md
├── tools/
│   └── verify_video_motion.py  # strict motion gate for rendered MP4s
└── docs/
```
