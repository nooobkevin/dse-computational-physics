# Unit 09: Scientific Inquiry in Physics

> **中文概覽**：本單元對應 CAF 主題 9「物理中的科學探究」，涵蓋數據分析、線性化、不確定度與誤差處理、複雜系統（流行病模型、森林火災、人群疏散）以及工程設計循環。所有教材均共用同一套 `physics_core` 引擎，確保動畫、教師示範程式與學生練習的分析內容完全一致。

## Overview 概覽

This unit maps to the **NEW CAF Topic 9 — Scientific Inquiry in Physics**
(June 2026 Consultation Draft), which replaces the former "Investigative
Study."  The unit covers **16 lesson hours** with at least **8 hands-on
practical tasks** and at least **1 scientific investigation or engineering
design activity**.

The unit follows the same three-artifact pattern shared by every unit in
the toolkit, adapted for data analysis and computational modelling:

1. **Manim animation** (watch) — visual explanation of linearisation,
   uncertainty, the inquiry loop, complex systems (epidemic, forest fire,
   crowd control), and the engineering design cycle
2. **Teacher demo app** (interact) — real-time OpenCV application with
   multiple modes for data analysis, experiment design, epidemic
   simulation, and engineering design
3. **Student fill-in-the-blank exercises** (code) — coding tasks with
   auto-graders

All artifacts consume the same `physics_core` engine
(`src/physics_core/inquiry/`), so the analysis is identical across every
front-end.

**中文摘要**：本單元對應新的 CAF 主題 9「物理中的科學探究」，取代以往的「研習」。單元涵蓋 16 課時，包括至少 8 項動手實作任務及至少 1 項科學探究或工程設計活動。沿用「三件教材」模式並針對數據分析與計算建模調整：Manim 動畫（線性化、不確定度、探究循環、複雜系統、工程設計循環）、教師示範程式（多種數據分析與模擬模式）與學生填空練習（自動評分）。

---

## CAF Curriculum Alignment 課程對照

### Learning Targets (16 hours)

| Domain | Sub-skills | Artifacts |
|---|---|---|
| **Scientific Inquiry** | Laboratory Technique, Data Analysis, Order of Accuracy and Error Treatment, Awareness of Safety | Manim scenes, Teacher app, Exercises, Questions |
| **Computational Physics** | Building Computational Models, Computer-Assisted Data Analysis | `complex_systems.py` engine, Epidemic scene, Data analysis exercise |

### Process Outcomes

| Activity | Outcomes | Artifacts |
|---|---|---|
| **Practical tasks** (8+, ~80 min each) | Prepare experiment, Use apparatus/computational tools, Complete assignments/reports | Teacher app (all modes), Exercises |
| **Scientific investigation** (~240 min) | Develop/justify plan, Implement, Analyse/refine, Report | Report template, Data analysis exercise, Questions |
| **Engineering design** (~240 min) | Define problem/design, Prototype/test, Analyse/optimise, Improve | `--mode design`, EngineeringDesign scene, Design exercise |

### Suggested Investigation Topics Covered

- **Programming complex systems (disease spread)**: `EpidemicSpread` scene,
  `--mode epidemic`, `ReferenceEpidemicModel` engine
- **Programming complex systems (forest fires)**: `ForestFire` scene,
  `--mode fire`, `ReferenceForestFire` engine
- **Programming complex systems (crowd control)**: `CrowdControl` scene,
  `--mode crowd`, `ReferenceCrowdModel` engine
- **Programming SHM simulation with damping**: see Unit 01 `damped_shm`
  scene (cross-reference)
- **Data linearisation** (1/x, 1/x²): `LinearisationTransforms` scene
- **Repeated measurements / outlier detection**: `UncertaintyRepeated` scene
- **Engineering design — pendulum clock**: `EngineeringDesign` scene,
  `--mode design`, `design_exercise.py`

---

## Lesson Flow (Suggested Sequence) 教學流程（建議次序）

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Linearisation**: `Linearisation.mp4` — T² vs L pendulum linearisation
- **More linearisation transforms**: `LinearisationTransforms.mp4` — 1/x
  and 1/x² transforms
- **Uncertainty & Error**: `Uncertainty.mp4` — error bars, best-fit line,
  percent error
- **Repeated measurements**: `UncertaintyRepeated.mp4` — outlier detection
  with IQR, mean±std
- **Conclusion**: `Conclusion.mp4` — the full inquiry loop
- **Epidemic spread**: `EpidemicSpread.mp4` — SIR cellular automaton on a
  grid with running bar chart
- **Forest fire**: `ForestFire.mp4` — wind-biased fire spread on a grid
  with live counts bar
- **Crowd control**: `CrowdControl.mp4` — agent-based evacuation through a
  single exit with congestion and live metrics
- **Engineering design**: `EngineeringDesign.mp4` — pendulum clock design
  loop (Design, Build, Test, Analyse, Improve)

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate live:

- **Analysis mode** (`--mode analysis`): pendulum T² vs L, linear fit,
  g estimation
- **Experiment mode** (`--mode experiment`): free-fall s vs t², error
  bars, uncertainty propagation
- **Epidemic mode** (`--mode epidemic`): SIR grid simulation with
  step/play controls
- **Fire mode** (`--mode fire`): forest-fire grid with p_ignite / wind_bias
  sliders + step/play controls
- **Crowd mode** (`--mode crowd`): agent evacuation with panic / n_agents
  sliders + step/play controls
- **Design mode** (`--mode design`): pendulum clock engineering design
  with L slider, fit, optimal L marker

### Step 3: Complete the fill-in-the-blank exercises

Students open the exercise files and implement the analysis functions.
Auto-graders check numerical behaviour (not source-code matching).

1. **`inquiry_exercise.py`** — implement `StudentLinearFit.model()`
2. **`design_exercise.py`** — implement `fit_slope()`,
   `recommended_length()`, `iteration_error()`
3. **`data_analysis_exercise.py`** — implement `to_si()`,
   `remove_outliers()`, `fit_slope()`, `estimate_g()`,
   `percent_uncertainty()`

### Step 4: Concept questions

Answer the questions in `questions.md`, including the new AI evaluation
and safety assessment questions.

### Step 5: Investigation report

Use `report_template.md` to structure a full scientific investigation
report.

**中文摘要**：建議教學次序為：先播放 Manim 動畫（線性化、不確定度、探究循環、流行病、森林火災、人群疏散、工程設計），再以教師示範程式即時示範（分析、實驗、流行病、火災、人群、設計等模式），然後讓學生完成填空練習（`inquiry_exercise.py`、`design_exercise.py`、`data_analysis_exercise.py`），接著回答 `questions.md` 的概念題（包括 AI 評估與安全評估題），最後以 `report_template.md` 撰寫完整的科學探究報告。

---

## How to Run Each Artifact 如何執行各項教材

### Prerequisites

- Python 3.11+ with `uv` installed
- Docker (for Manim rendering only)

```bash
uv sync
```

### Engine tests

```bash
uv run pytest tests/test_inquiry.py -v
```

### Teacher app

```bash
uv run python units/09_inquiry/teacher_app/main.py --mode analysis
uv run python units/09_inquiry/teacher_app/main.py --mode experiment
uv run python units/09_inquiry/teacher_app/main.py --mode epidemic
uv run python units/09_inquiry/teacher_app/main.py --mode fire
uv run python units/09_inquiry/teacher_app/main.py --mode crowd
uv run python units/09_inquiry/teacher_app/main.py --mode design
uv run python units/09_inquiry/teacher_app/main.py --mode epidemic --headless-selfcheck
uv run python units/09_inquiry/teacher_app/main.py --mode fire --headless-selfcheck
uv run python units/09_inquiry/teacher_app/main.py --mode crowd --headless-selfcheck
```

### Manim render

```bash
bash units/09_inquiry/manim/render.sh
bash units/09_inquiry/manim/render.sh epidemic
bash units/09_inquiry/manim/render.sh forest_fire
bash units/09_inquiry/manim/render.sh crowd_control
bash units/09_inquiry/manim/render.sh epidemic -ql
```

Available scenes: `linearisation`, `linearisation_transforms`,
`uncertainty`, `uncertainty_repeated`, `conclusion`, `epidemic`,
`engineering_design`, `forest_fire`, `crowd_control`.

### Exercise / grader

```bash
uv run pytest units/09_inquiry/exercises/test_exercise.py -v
uv run pytest units/09_inquiry/exercises/test_design.py -v
uv run pytest units/09_inquiry/exercises/test_data_analysis.py -v
```

---

## New in This CAF Iteration 本版 CAF 新增內容

| Item | Description | Files |
|---|---|---|
| **Epidemic CA engine** | Deterministic SIR cellular automaton on NxM grid | `src/physics_core/inquiry/complex_systems.py` |
| **Epidemic scene** | Grid of S/I/R cells with running bar chart | `manim/scenes/epidemic.py` |
| **Epidemic app mode** | Step/play controls for SIR simulation | `teacher_app/main.py` (`--mode epidemic`) |
| **Forest-fire CA engine** | Deterministic forest-fire CA with wind bias, per-step counts | `src/physics_core/inquiry/complex_systems.py` |
| **Forest-fire scene** | Tree grid, ignition, wind arrow, live counts bar | `manim/scenes/forest_fire.py` |
| **Fire app mode** | p_ignite / wind_bias sliders, step/play, burns out | `teacher_app/main.py` (`--mode fire`) |
| **Crowd CA engine** | Deterministic agent-based exit evacuation with panic | `src/physics_core/inquiry/complex_systems.py` |
| **Crowd scene** | Hall + exit, agents congest at the door, live traces | `manim/scenes/crowd_control.py` |
| **Crowd app mode** | panic / n_agents sliders, step/play, all exit | `teacher_app/main.py` (`--mode crowd`) |
| **Engineering design scene** | Pendulum clock design loop (3 iterations) | `manim/scenes/engineering_design.py` |
| **Design app mode** | L slider, T² vs L fit, optimal L marker | `teacher_app/main.py` (`--mode design`) |
| **Design exercise** | fit_slope, recommended_length, iteration_error | `exercises/design_exercise.py` + grader |
| **1/x, 1/x² linearisation** | Additional linearisation transforms scene | `manim/scenes/linearisation.py` (extended) |
| **Repeated measurements** | Outlier detection with IQR, mean±std | `manim/scenes/uncertainty.py` (extended) |
| **Data analysis exercise** | Unit conversion, outlier removal, fit, g estimate | `exercises/data_analysis_exercise.py` + grader |
| **Report template** | Structured investigation report scaffold | `exercises/report_template.md` |
| **AI evaluation questions** | Critical evaluation of AI-generated analysis | `exercises/questions.md` (g) |
| **Safety assessment questions** | Hazard identification in experiment design | `exercises/questions.md` (h) |

### Cross-reference: SHM damping investigation 交叉參考：簡諧運動阻尼探究

The CAF suggests "programming a simulation of simple harmonic motion and
study the damping factor" as an investigation topic.  This is delivered
by **Unit 01** (`units/01_mechanics/manim/scenes/damped_shm.py`) in the
same CAF iteration.  See Unit 01's README for details.

**中文摘要**：CAF 建議以「編寫簡諧運動模擬並研究阻尼係數」作為探究主題。此主題由同一 CAF 版本的 **單元 01**（`units/01_mechanics/manim/scenes/damped_shm.py`）提供，詳情見單元 01 的 README。
