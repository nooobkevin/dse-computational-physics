# New Unit Template

Copy this skeleton to add a new curriculum unit. Each unit follows the same three-artifact pattern: Manim animation, teacher demo app, and student fill-in-the-blank exercise, all sharing one `physics_core` engine.

---

## Directory Layout

```
units/NN_<unit>/
  README.md              ← per-unit documentation (outcome map, lesson flow, commands)
  manim/
    scenes/
      __init__.py
      <scene_a>.py       ← Manim scene(s) importing physics_core
      <scene_b>.py
    render.sh             ← copy from units/01_mechanics/manim/render.sh, update SCENE_NAMES
    output/               ← rendered MP4s (gitignored)
  teacher_app/
    main.py               ← OpenCV demo app (or add a mode to the existing app)
    ...                   ← mode-specific modules
  exercises/
    __init__.py
    <topic>_exercise.py   ← student fill-in-the-blank (NotImplementedError hooks)
    <topic>_solution.py   ← hidden solution (gitignored)
    test_exercise.py      ← auto-grader
    conftest.py           ← pytest fixtures (--override-student, --selfcheck)
    questions.md          ← concept questions
    teacher_key.md        ← answer key (gitignored)
```

---

## The `physics_core` Contract

Every simulation in `src/physics_core/<domain>/` follows this pattern:

### Abstract base class

```python
class MySim:
    """Abstract base. Framework methods are implemented; physics hooks raise NotImplementedError."""

    def __init__(self, ...):
        # Store parameters, initialise state dict
        self._state = {"x": ..., "v": ..., "t": 0.0}

    # ── Physics hook (subclass MUST override) ──
    def acceleration(self, ...) -> float:
        raise NotImplementedError("Subclasses must implement ...")

    # ── Framework methods (fully implemented) ──
    def step(self, dt=None):
        """Advance simulation by one time-step using euler_step or verlet_step."""
        h = dt if dt is not None else self.dt
        # Map domain state to integrator state {"x", "v", "t"}
        # Call euler_step or verlet_step
        # Map back to domain state

    @property
    def state(self) -> dict:
        """Current simulation state."""
        return dict(self._state)

    def position(self) -> tuple:
        """Physical position (x, y) or generalised coordinate."""

    def energy(self) -> dict:
        """Kinetic, potential, and total energy."""
```

### Reference implementation

```python
class ReferenceMySim(MySim):
    """Correct physics. Overrides the hook(s)."""

    def acceleration(self, ...) -> float:
        # Return the correct physical acceleration
        return ...
```

### Key points

- The **state dict** must contain at least `"x"` and `"v"` for the generic integrators in `physics_core.integrators`. Add domain-specific keys as needed (e.g. `"y"`, `"vx"`, `"vy"` for projectile).
- The **deriv function** passed to the integrator has signature `deriv(x, v, t) -> float`. The base class wraps the physics hook into this signature.
- The **Reference** class is what the Manim scenes and teacher app use. The **abstract base** is what the student exercise subclasses.
- Add the new module to `src/physics_core/<domain>/` with an `__init__.py`.

---

## Steps to Add a Unit

### Step 1: Add the physics engine

Create `src/physics_core/<domain>/` with:

- `__init__.py`
- `<topic>.py` — abstract base + Reference implementation

The abstract base defines the physics hook(s) that raise `NotImplementedError`. The Reference subclass supplies the correct physics.

**Acceptance:** `uv run pytest tests/` passes (add unit tests for the new engine).

### Step 2: Add Manim scene(s)

Create `units/NN_<unit>/manim/scenes/<scene>.py`:

- Import the Reference class from `physics_core.<domain>`
- Use the `h = min(dt, 1.0 / config.frame_rate)` dt-clamp in updaters
- Copy `render.sh` from `01_mechanics/manim/render.sh` and update the `SCENE_NAMES` array

**Acceptance:**

```bash
bash units/NN_<unit>/manim/render.sh <scene> -ql
```

Check that an MP4 appears in `units/NN_<unit>/manim/output/`.

### Step 3: Add the teacher app mode

Either add a new mode to the existing `units/01_mechanics/teacher_app/main.py` or create a standalone app in `units/NN_<unit>/teacher_app/main.py`.

The app should:
- Accept `--mode <name>` (if multi-mode)
- Accept `--headless-selfcheck` for CI
- Import the Reference class from `physics_core.<domain>`
- Run a real-time loop calling `sim.step()` and rendering the state

**Acceptance:**

```bash
uv run python units/NN_<unit>/teacher_app/main.py --mode <name> --headless-selfcheck
```

Should print an OK message and exit without opening a window.

### Step 4: Add the exercise

Create in `units/NN_<unit>/exercises/`:

- **`<topic>_exercise.py`** — student-facing file. Subclass the abstract base, leave the hook raising `NotImplementedError` with a TODO comment. Include a docstring explaining the physics and the formula to implement.
- **`<topic>_solution.py`** — hidden solution (add to `.gitignore`). Same subclass with the hook correctly implemented.
- **`test_exercise.py`** — auto-grader. Import the student class via the conftest fixture. Test numerical behaviour (period, energy conservation, stability) — do NOT read the student's source code.
- **`conftest.py`** — copy from `01_mechanics/exercises/conftest.py`. Provides `--override-student`, `--selfcheck`, and the `student_class` / `wrong_student_class` fixtures.
- **`questions.md`** — concept questions linking the exercise to the curriculum.
- **`teacher_key.md`** — answer key (add to `.gitignore`).

**Acceptance:**

```bash
# Grader should fail on the unfilled exercise
uv run pytest units/NN_<unit>/exercises/test_exercise.py -v

# Grader should pass on the solution
uv run pytest units/NN_<unit>/exercises/test_exercise.py \
    --override-student=units/NN_<unit>/exercises/<topic>_solution.py -v

# Full self-check
uv run pytest units/NN_<unit>/exercises/test_exercise.py --selfcheck -v
```

### Step 5: Write the unit README

Create `units/NN_<unit>/README.md` following the structure in `units/01_mechanics/README.md`:

- Overview of the three-artifact pattern
- Curriculum learning-outcome map (table: Sub-topic → Learning outcome(s) → Which artifact(s))
- Suggested lesson flow (watch → interact → code)
- Exact commands for each artifact
- Any calibration or setup notes
- Numerical-methods tie-in (if applicable)

---

## Checklist

| # | Artifact | Acceptance command |
|---|---|---|
| 1 | Physics engine | `uv run pytest tests/` |
| 2 | Manim scene(s) | `bash units/NN_<unit>/manim/render.sh <scene> -ql` → check output MP4 |
| 3 | Teacher app | `uv run python units/NN_<unit>/teacher_app/main.py --mode <name> --headless-selfcheck` |
| 4a | Exercise (unfilled) | `uv run pytest units/NN_<unit>/exercises/test_exercise.py -v` → fails with NotImplementedError |
| 4b | Exercise (solution) | `uv run pytest units/NN_<unit>/exercises/test_exercise.py --override-student=.../solution.py -v` → passes |
| 4c | Self-check | `uv run pytest units/NN_<unit>/exercises/test_exercise.py --selfcheck -v` → both pass and fail verified |
| 5 | Unit README | Written with outcome map, lesson flow, and exact commands |

---

## Gitignore Reminder

Add these patterns to `.gitignore` if not already present:

```
units/**/<topic>_solution.py
units/**/teacher_key.md
units/**/output/
```
