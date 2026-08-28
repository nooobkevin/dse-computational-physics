# Unit 09: Scientific Inquiry in Physics

## Overview

This unit is different from the other units in the toolkit.  Instead of a
physics simulation, it focuses on the **scientific inquiry process** —
designing experiments, collecting and analysing data, drawing evidence-based
conclusions, and evaluating results.  This maps to the HKDSE "Scientific
Inquiry and Development" strand.

The unit follows the same three-artifact pattern shared by every unit in the
toolkit, adapted for data analysis:

1. **Manim animation** (watch) — visual explanation of linearisation,
   uncertainty, and the inquiry loop
2. **Teacher demo app** (interact) — real-time OpenCV application that
   generates synthetic experimental data, fits a model, and estimates a
   physical constant with uncertainty
3. **Student fill-in-the-blank exercise** (code) — a data-analysis coding
   task with an auto-grader

All three artifacts consume the same `physics_core` engine
(`src/physics_core/inquiry/`), so the analysis is identical across every
front-end.

---

## Curriculum Learning-Outcome Map

This unit targets the following HKDSE Physics curriculum outcomes:

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Scientific inquiry** (Scientific Inquiry a) | Define a research question; identify independent, dependent, and control variables; plan a controlled experiment | Manim `Conclusion` (inquiry loop schematic); Teacher app (experiment design discussion); Concept questions (a) |
| **Data collection** (Scientific Inquiry b) | Collect and record data systematically; use appropriate instruments and measurement techniques | Teacher app (synthetic data generation); Student exercise (data input) |
| **Data analysis** (Scientific Inquiry c) | Graph data; linearise non-linear relationships; fit a best-fit line; interpret slope and intercept | Manim `Linearisation` (T² vs L); Teacher app (scatter + fit overlay); Student exercise (implement linear fit) |
| **Uncertainty and error** (Scientific Inquiry d) | Estimate measurement uncertainty; propagate errors; compute percent error; distinguish systematic vs random error | Manim `Uncertainty` (error bars, % error); Teacher app (uncertainty propagation display); Concept questions (d, e) |
| **Conclusions and evaluation** (Scientific Inquiry e) | Draw evidence-based conclusions; evaluate experimental design; suggest improvements | Manim `Conclusion` (inquiry loop); Teacher app (g estimate + % error); Concept questions (f) |
| **Building computational models** (Scientific Inquiry) | Translate a data-analysis procedure into code; modify the analysis and observe the effect | Student exercise (implement `model` method); Teacher app (different experiments) |

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Linearisation**: `Linearisation.mp4` — shows the non-linear T vs L
  relationship for a pendulum, then the linearised T² vs L plot with a
  best-fit line.  Explains why we linearise and how the slope gives a
  physical constant.
- **Uncertainty & Error**: `Uncertainty.mp4` — shows data points with error
  bars, the best-fit line, the estimated g value, and the percent error vs
  the accepted value.  Explains uncertainty propagation.
- **Conclusion**: `Conclusion.mp4` — shows the full inquiry loop as a
  schematic diagram (Question → Plan → Data → Analyse → Conclude →
  Evaluate), with the pendulum experiment as a concrete example.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the analysis live:

- **Analysis mode** (`--mode analysis`): generates synthetic pendulum data
  (T² vs L), performs a linear fit, displays the scatter plot with the
  best-fit line, and reports the estimated g with percent error.  Use this
  to discuss linearisation, slope interpretation, and error analysis.
- **Experiment mode** (`--mode experiment`): generates synthetic free-fall
  data (s vs t²), shows error bars on the data points, fits a line, and
  reports the estimated g with uncertainty propagation.  Use this to
  discuss measurement uncertainty and error propagation.

### Step 3: Complete the fill-in-the-blank exercise

Students open `inquiry_exercise.py` and implement the `model` method in
`StudentLinearFit`.  The auto-grader checks:

1. The `NotImplementedError` is replaced (immediate fail if not)
2. The slope matches the known value to within 1e-6
3. The intercept matches the known value to within 1e-6
4. R² ≈ 1 for noiseless data
5. Percent error is correctly computed from the estimated constant

The concepts from Step 2 feed directly into the concept questions in
`questions.md`: identifying variables, linearisation, best-fit vs origin,
percent error, systematic vs random error, and evaluation.

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

This runs the unit tests in `tests/` (including `test_inquiry.py`).  The
`pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Analysis mode (synthetic pendulum experiment)
uv run python units/09_inquiry/teacher_app/main.py --mode analysis

# Experiment mode (synthetic free-fall experiment with error bars)
uv run python units/09_inquiry/teacher_app/main.py --mode experiment

# Headless self-check (no window, for CI)
uv run python units/09_inquiry/teacher_app/main.py --mode analysis --headless-selfcheck
```

Both modes are fully synthetic — no camera or external hardware required.
The `--headless-selfcheck` flag runs the analysis without opening a window
and exits — useful for CI or testing.

### Manim render

```bash
# Render all three scenes (requires Docker)
bash units/09_inquiry/manim/render.sh

# Render a specific scene
bash units/09_inquiry/manim/render.sh linearisation

# Low-quality preview (fast)
bash units/09_inquiry/manim/render.sh linearisation -ql
```

The script uses the `manimcommunity/manim:stable` Docker image.  Output MP4
files land in `units/09_inquiry/manim/output/`.  The `--disable_caching`
flag is set to force re-render on every run.

Available scenes: `linearisation`, `uncertainty`, `conclusion`.

Quality flags: `-qh` (high, default), `-qm` (medium), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: inquiry_exercise.py)
uv run pytest units/09_inquiry/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/09_inquiry/exercises/test_exercise.py \
    --override-student=units/09_inquiry/exercises/inquiry_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/09_inquiry/exercises/test_exercise.py --selfcheck -v
```

The solution file (`inquiry_solution.py`) and teacher answer key
(`teacher_key.md`) are gitignored — students must not see them.

---

## Data-Analysis Tie-In

The `ReferenceLinearFit` class in `physics_core.inquiry.analysis` performs
ordinary least-squares linear regression using numpy's `polyfit`.  The
student exercise asks students to implement the same analysis themselves.

This creates a direct link:

- **Watch**: the Manim scene shows linearisation and best-fit lines
- **Do**: the student implements the linear fit, then runs it on synthetic
  data
- **Analyze**: the concept questions ask about slope interpretation, R²,
  percent error, and sources of uncertainty

### Synthetic-only note

All data in this unit is **synthetic** — generated by the teacher app or
the Manim scenes using numpy random number generators.  This ensures the
unit works without any external hardware or lab equipment.  Teachers can
replace the synthetic data with real experimental data if desired.

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render
  every time (cached frames from a previous run with different parameters
  would be stale).
- Output MP4s are flattened from the nested `videos/` directory into the
  flat `output/` directory by the script.
