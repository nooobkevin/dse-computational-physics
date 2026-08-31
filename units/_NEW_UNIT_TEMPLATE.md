# New Unit Template

Copy this skeleton to add a new curriculum unit. Each unit follows the same
three-artifact pattern: Manim animation, teacher demo app, and student
fill-in-the-blank exercise, all sharing one `physics_core` engine. This
template reflects the conventions established by the CAF iteration (units
07–09 are the most recent exemplars — read their READMEs before starting).

---

## Directory Layout

```
units/NN_<unit>/
  README.md              ← per-unit documentation (outcome map, lesson flow, commands)
  curriculum_alignment.md ← CAF learning-outcome map (see units/08_astrophysics/)
  manim/
    scenes/
      __init__.py
      <scene_a>.py       ← Manim scene(s) importing physics_core Reference classes
      <scene_b>.py
    render.sh             ← copy from units/08_astrophysics/manim/render.sh, update SCENE_NAMES
    output/               ← rendered MP4s (gitignored)
  teacher_app/
    main.py               ← OpenCV demo app, one --mode per topic, --headless-selfcheck
  exercises/
    __init__.py
    <topic>_exercise.py   ← student fill-in-the-blank (NotImplementedError hooks)
    <topic>_solution.py   ← hidden solution (gitignored)
    test_exercise.py      ← auto-grader (one file per exercise; e.g. test_stars_exercise.py)
    conftest.py           ← pytest fixtures (--override-student[-<exercise>], --selfcheck)
    questions.md          ← concept questions
    teacher_key.md        ← answer key (gitignored)
```

Register the unit's exercises in `units/exercises_shared/registry.py` so
`tools/grade_exercise.py` knows each test file's override flag and solution
file.

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

- The **state dict** must contain at least `"x"` and `"v"` for the generic
  integrators in `physics_core.integrators`. Add domain-specific keys as
  needed (e.g. `"y"`, `"vx"`, `"vy"` for projectile).
- The **deriv function** passed to the integrator has signature
  `deriv(x, v, t) -> float`. The base class wraps the physics hook into
  this signature.
- The **Reference** class is what the Manim scenes and teacher app use.
  The **abstract base** is what the student exercise subclasses.
- Add the new module to `src/physics_core/<domain>/` with an `__init__.py`.

---

## Steps to Add a Unit

### Step 1: Add the physics engine

Create `src/physics_core/<domain>/` with:

- `__init__.py`
- `<topic>.py` — abstract base + Reference implementation

The abstract base defines the physics hook(s) that raise
`NotImplementedError`. The Reference subclass supplies the correct physics.

**Acceptance:** `uv run pytest tests/` passes (add unit tests for the new
engine).

### Step 2: Add Manim scene(s)

Create `units/NN_<unit>/manim/scenes/<scene>.py`:

- Import the Reference class from `physics_core.<domain>`.
- Use the **proven-animation pattern** for anything that moves (see
  `units/03_waves/manim/scenes/superposition_standing.py`):

```python
t: list[float] = [0.0]

def updater(_mob: Mobject, dt: float) -> None:
    t[0] = self.time

driver = Mobject()
driver.add_updater(updater)
```

- Visible curves are `always_redraw` mobjects rebuilt every frame as a
  **single VMobject** with `set_points_as_corners` (never a VGroup of
  Lines).
- The authoritative time is `self.time` (Manim's video clock), not
  accumulated from `dt`.
- This pattern avoids the ManimCE cairo-renderer bug where submobjects
  added inside an updater are frozen.
- Copy `render.sh` from `units/08_astrophysics/manim/render.sh` and update
  the `SCENE_NAMES` array. The script mounts the repo at `/work`
  (`-v "$REPO_ROOT":/work`, `-w /work`, `PYTHONPATH=/work/src`), runs
  `manimcommunity/manim:stable` with `-qm` (default), `--disable_caching`,
  `--format mp4`, writes to `--media_dir units/NN_<unit>/manim/output`, and
  flattens nested `videos/` MP4s into the flat `output/` directory.

**Acceptance:**

```bash
bash units/NN_<unit>/manim/render.sh <scene> -ql
```

Check that an MP4 appears in `units/NN_<unit>/manim/output/`, then run the
motion gate:

```bash
uv run python tools/verify_video_motion.py units/NN_<unit>/manim/output/<Scene>.mp4 --strict
```

Every new/changed MP4 must pass the strict gate (≥ 30 frames, sustained
motion across ≥ 5 sampled intervals, coloured content changes).

### Step 3: Add the teacher app mode

Create `units/NN_<unit>/teacher_app/main.py`:

- Accept `--mode <name>` (one mode per topic).
- Accept `--headless-selfcheck` for CI: run a few frames of the mode
  without opening a window, assert the physics, print an OK message, and
  `sys.exit(0)`.
- Import the Reference class from `physics_core.<domain>`.
- Run a real-time loop calling `sim.step()` and rendering the state.

**Acceptance:**

```bash
uv run python units/NN_<unit>/teacher_app/main.py --mode <name> --headless-selfcheck
```

Should print an OK message and exit without opening a window.

### Step 4: Add the exercise

Create in `units/NN_<unit>/exercises/`:

- **`<topic>_exercise.py`** — student-facing file. Subclass the abstract
  base, leave the hook raising `NotImplementedError` with a TODO comment.
  Include a docstring explaining the physics and the formula to implement.
- **`<topic>_solution.py`** — hidden solution (add to `.gitignore`). Same
  subclass with the hook correctly implemented.
- **`test_exercise.py`** — auto-grader. Import the student class via the
  conftest fixture. Test numerical behaviour (period, energy conservation,
  stability) — do NOT read the student's source code. One test file per
  exercise (e.g. `test_stars_exercise.py` for a second exercise).
- **`conftest.py`** — copy from `units/08_astrophysics/exercises/conftest.py`.
  Provides `--override-student` (shared) plus per-exercise flags such as
  `--override-student-stars`, `--selfcheck`, and the `student_class` /
  `wrong_student_class` fixtures.
- **`questions.md`** — concept questions linking the exercise to the
  curriculum.
- **`teacher_key.md`** — answer key (add to `.gitignore`).

Register the exercise in `units/exercises_shared/registry.py`:

```python
"NN_<unit>": (
    ExerciseSpec("test_exercise.py", "--override-student", "<topic>_solution.py"),
),
```

**Acceptance:**

```bash
# Grader should fail on the unfilled exercise
uv run pytest units/NN_<unit>/exercises/test_exercise.py -v

# Grader should pass on the solution
uv run pytest units/NN_<unit>/exercises/test_exercise.py \
    --override-student=units/NN_<unit>/exercises/<topic>_solution.py -v

# Full self-check
uv run pytest units/NN_<unit>/exercises/test_exercise.py --selfcheck -v

# Scorecard CLI (partial credit)
uv run python tools/grade_exercise.py NN_<unit> --solution units/NN_<unit>/exercises/<topic>_solution.py
```

### Step 5: Write the unit README and curriculum map

Create `units/NN_<unit>/README.md` following the structure in
`units/08_astrophysics/README.md`:

- Overview of the three-artifact pattern
- Curriculum learning-outcome map (table: Sub-topic → Learning outcome(s) →
  Which artifact(s) deliver it)
- Suggested lesson flow (watch → interact → code)
- Exact commands for each artifact (engine tests, teacher app modes +
  `--headless-selfcheck`, render.sh usage, exercise/grader commands)
- Numerical-methods tie-in (if applicable)

Create `units/NN_<unit>/curriculum_alignment.md` with the detailed CAF
alignment (see `units/08_astrophysics/curriculum_alignment.md`).

---

## Checklist

| # | Artifact | Acceptance command |
|---|---|---|
| 1 | Physics engine | `uv run pytest tests/` |
| 2 | Manim scene(s) | `bash units/NN_<unit>/manim/render.sh <scene> -ql` → check output MP4 |
| 3 | Motion gate | `uv run python tools/verify_video_motion.py units/NN_<unit>/manim/output/<Scene>.mp4 --strict` |
| 4 | Teacher app | `uv run python units/NN_<unit>/teacher_app/main.py --mode <name> --headless-selfcheck` |
| 5a | Exercise (unfilled) | `uv run pytest units/NN_<unit>/exercises/test_exercise.py -v` → fails with NotImplementedError |
| 5b | Exercise (solution) | `uv run pytest units/NN_<unit>/exercises/test_exercise.py --override-student=.../solution.py -v` → passes |
| 5c | Self-check | `uv run pytest units/NN_<unit>/exercises/test_exercise.py --selfcheck -v` → both pass and fail verified |
| 5d | Scorecard CLI | `uv run python tools/grade_exercise.py NN_<unit> --solution .../solution.py` → prints 100.0% |
| 6 | Unit README + curriculum map | Written with outcome map, lesson flow, and exact commands |

---

## Gitignore Reminder

Add these patterns to `.gitignore` if not already present:

```
units/**/<topic>_solution.py
units/**/teacher_key.md
units/**/output/
```