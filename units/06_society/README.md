# Unit 06: Physics and Society 社會與能源

## Overview 單元概覽

本單元涵蓋物理與社會的核心課題，包括輻射與放射性（半衰期、放射性強度、蓋革計數器、電離輻射、裂變與聚變）、能源與可持續發展（可再生能源、太陽能、風能），以及放射性同位素的應用。學生透過觀看動畫、操作教師示範程式及完成填空式編程練習，掌握半衰期、放射性強度、裂變、聚變與可再生能源等概念。

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-method coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/society/`), so the physics is identical across every front-end.

---

## Curriculum Learning-Outcome Map 課程學習成果對照

This unit targets the following HKDSE Physics curriculum outcomes (CAF Consultation Draft June 2026):

下表對應 CAF（2026 年 6 月諮詢稿）主題六「物理與社會」的學習成果，涵蓋輻射與放射性、能源與可持續發展，以及物理與未來科技三大範疇。

### 6a. Radiation and radioactivity 輻射與放射性

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Radioactive decay** (6a.7–6a.10) | Random nature of decay; activity A ∝ N; half-life definition (factor of one-half); determine half-life from decay graph or numerical data | Teacher app (`--mode decay` — N vs t curve, analytic overlay, half-life marker, activity display); Manim `RadioactiveDecay` (decay curve + Monte Carlo dots); Student exercise (implement `decay_probability`); Decay analysis exercise (fit decay data → half-life) |
| **Alpha, beta, gamma radiation** (6a.4–6a.5) | Origin and nature; compare penetrating power, ranges, ionising power | Teacher app (`--mode radiation` — bar charts of ionising/penetrating power); Manim `RadiationPenetration` (schematic of shielding) |
| **Radioactive isotopes — uses** (6a.19) | Radiotherapy, thickness inspection, tracers, medical imaging | Manim `RadioisotopeUses` (gamma camera, radiotherapy, thickness gauge) |
| **Nuclear fission and chain reactions** (6a.20) | Neutron multiplication factor k; critical mass; subcritical/critical/supercritical regimes | Teacher app (`--mode reactor` — neutron population vs generation for k=0.6, 1.0, 1.5); Manim `ChainReaction` (fission schematic + chain reaction generations) |

### 6b. Energy sources and sustainable development 能源與可持續發展

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Mass-energy relationship** (6b.3–6b.5) | ΔE = Δmc²; electron-volt and atomic mass unit; apply to nuclear reactions | Engine `energy.py` (`mass_energy_delta`); Manim `EnergySources` (ΔE = Δmc² annotation); Teacher app (`--mode energy` — fission mass-defect panel); Student exercise (implement `mass_energy_delta`) |
| **Solar power** (6b.9–6b.10) | Solar constant definition; photovoltaic effect; P = S·A·η | Engine `energy.py` (`solar_power`, `photovoltaic_power`); Manim `EnergySources` (solar panel); Teacher app (`--mode energy` — solar info); Student exercise (implement `solar_power`) |
| **Wind turbine power** (6b.11) | P = ½ηρAv³; solve problems | Engine `energy.py` (`wind_power`); Manim `EnergySources` (P vs v³ curve); Teacher app (`--mode energy` — interactive sliders, cubic curve); Student exercise (implement `wind_power`) |
| **Nuclear fission and fusion** (6b.2, 6b.8) | Energy release in fission and fusion; fusion as source of solar energy | Manim `EnergySources` (fission/fusion comparison); Teacher app (`--mode energy` — mass-defect readout) |
| **Carbon neutrality** (6b.13) | Daily habits; climate change mitigation; HK energy consumption | Concept questions in `questions.md` (STSE carbon-neutrality trade-offs) |

### 6c. Physics for recent and future 物理與未來科技

| Sub-topic | Learning outcome(s) | Which artifact(s) deliver it |
|---|---|---|
| **Physics-related careers** (6c.1–6c.2) | Role of physicists and engineers in sustainable society; professions applying physical models | Concept questions in `questions.md`; README notes |
| **Physics and I&T** (6c.3) | Impact of physics discoveries on modern technologies | Manim `RadioisotopeUses` (medical imaging, industrial applications) |

### Computational Physics (per §2.2.2) 計算物理（按 §2.2.2）

| CP activity | Which artifact(s) deliver it |
|---|---|
| Simulate radioactive decay process (line 2621) | Teacher app (`--mode decay`); Manim `RadioactiveDecay`; Student exercise (Monte Carlo) |
| Monte Carlo method for probabilistic phenomena (line 642) | Decay simulation (Monte Carlo step) |
| Build computational models: translate physics to code (line 629) | Student exercises (fill-in-the-blank hooks) |
| Computer-assisted data analysis (line 659) | Decay analysis exercise (fit decay curve → half-life) |

---

## Lesson Flow (Suggested Sequence) 教學流程

以下為建議的教學順序：先觀看 Manim 動畫建立直觀概念，再以教師示範程式即時演示物理現象，最後讓學生完成填空式編程練習並回答概念問題。

### Step 1: Watch the Manim scene(s) 第一步：觀看 Manim 動畫

Play the rendered MP4 for the topic you are about to teach:

- **Radioactive decay**: `RadioactiveDecay.mp4` — shows the decay curve `N = N₀·2^(-t/T)` with the analytic curve in green and Monte Carlo simulation dots in orange. The half-life is marked with red dashed lines at `N = N₀/2`. Pause to discuss: why does the Monte Carlo scatter around the analytic curve? What happens if we increase N₀?
- **Radiation penetration**: `RadiationPenetration.mp4` — shows a schematic of alpha, beta, and gamma radiation passing through paper, aluminium, and lead barriers.
- **Chain reaction**: `ChainReaction.mp4` — shows a fission schematic and chain reaction generations with the critical mass concept.
- **Energy sources**: `EnergySources.mp4` — compares fission/fusion (ΔE = Δmc²), solar power (P = S·A·η), and wind power (P ∝ v³) with a bar chart comparison.
- **Radioisotope uses**: `RadioisotopeUses.mp4` — shows three applications: medical imaging (gamma camera), radiotherapy, and industrial thickness gauge.

### Step 2: Run the teacher demo app 第二步：執行教師示範程式

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Decay mode** (`--mode decay`): shows a Monte Carlo decay simulation with the analytic curve overlaid. The N vs t graph builds in real time. Activity (A = λN) is displayed. The estimated half-life is marked with a red dashed line.
- **Radiation mode** (`--mode radiation`): shows bar charts of penetrating power and ionising power for alpha, beta, and gamma radiation.
- **Reactor mode** (`--mode reactor`): shows neutron population vs generation for three values of k (0.6, 1.0, 1.5).
- **Energy mode** (`--mode energy`): interactive wind turbine with radius and wind-speed sliders, live P = ½ηρAv³ with the P-vs-v cubic curve; fission panel with mass-defect readout; solar power reference.

### Step 3: Complete the fill-in-the-blank exercises 第三步：完成填空式練習

Students complete one or more of the following exercises:

1. **Society exercise** (`society_exercise.py`): implement `decay_probability`.
2. **Energy exercise** (`energy_exercise.py`): implement `mass_energy_delta`, `solar_power`, `wind_power`, `photovoltaic_power`.
3. **Decay analysis exercise** (`decay_analysis_exercise.py`): implement `half_life_from_fit` (log-linear fit), `background_subtracted_rate`, `remaining_fraction`.

Each auto-grader measures numerical behaviour — any correct implementation passes.

---

## How to Run Each Artifact 如何執行各項工具

以下指令說明如何執行引擎測試、教師示範程式、Manim 渲染及練習評分器。所有示範模式均為全合成（synthetic），無需攝影機即可在課堂投影。

### Prerequisites 前置要求

- Python 3.11+ with `uv` installed
- Docker (for Manim rendering only)

```bash
# Install dependencies
uv sync
```

### Engine tests 引擎測試

```bash
uv run pytest tests/test_society.py -v
```

This runs all unit tests for the society domain (decay simulation, radiation properties, energy sources).

### Teacher app 教師示範程式

```bash
# Decay mode (Monte Carlo simulation + activity display)
uv run python units/06_society/teacher_app/main.py --mode decay

# Radiation mode (alpha/beta/gamma properties)
uv run python units/06_society/teacher_app/main.py --mode radiation

# Reactor mode (chain reaction / critical mass)
uv run python units/06_society/teacher_app/main.py --mode reactor

# Energy mode (wind turbine + fission mass-defect)
uv run python units/06_society/teacher_app/main.py --mode energy

# Headless self-check (no window, for CI)
uv run python units/06_society/teacher_app/main.py --mode decay --headless-selfcheck
```

All modes are fully synthetic — no camera required. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render Manim 渲染

```bash
# Render all scenes (requires Docker)
bash units/06_society/manim/render.sh

# Render a specific scene
bash units/06_society/manim/render.sh energy_sources

# Low-quality preview (fast)
bash units/06_society/manim/render.sh energy_sources -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/06_society/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `radioactive_decay`, `radiation_penetration`, `chain_reaction`, `energy_sources`, `radioisotope_uses`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader 練習／評分器

```bash
# Grade the decay exercise (default: society_exercise.py)
uv run pytest units/06_society/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/06_society/exercises/test_exercise.py -v \
    --override-student=units/06_society/exercises/society_solution.py

# Grade the energy exercise
uv run pytest units/06_society/exercises/test_energy_exercise.py -v \
    --override-student-energy=units/06_society/exercises/energy_solution.py

# Grade the decay analysis exercise
uv run pytest units/06_society/exercises/test_decay_analysis_exercise.py -v \
    --override-student-decay-analysis=units/06_society/exercises/decay_analysis_solution.py

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/06_society/exercises/test_exercise.py --selfcheck -v
```

Solution files (`society_solution.py`, `energy_solution.py`, `decay_analysis_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Physics Engine Architecture 物理引擎架構

The `src/physics_core/society/` package follows the same pattern as `mechanics/` and `em/`:

`src/physics_core/society/` 套件與 `mechanics/` 及 `em/` 採用相同模式：

```
src/physics_core/society/
  __init__.py           ← exports all classes
  decay.py              ← DecaySim (abstract) + ReferenceDecaySim
  energy.py             ← EnergySim (abstract) + ReferenceEnergySim
```

The abstract base defines physics **hooks** that raise `NotImplementedError`. The `Reference` subclass provides the correct physics. All three front-ends import the Reference implementation; the student exercise subclasses the base directly.

### Physics hooks 物理鉤子

| Engine | Hook(s) | Physics |
|---|---|---|
| `DecaySim` | `decay_probability(dt)` | p = 1 − exp(−λ dt), λ = ln(2)/T |
| `EnergySim` | `mass_energy_delta(dm)` | ΔE = Δm·c², 1 amu ≈ 931.5 MeV |
| `EnergySim` | `solar_power(area, S, η)` | P = S·A·η |
| `EnergySim` | `wind_power(r, v, ρ, η)` | P = ½ηρπr²v³ |
| `EnergySim` | `photovoltaic_power(area, S, η)` | P = S·A·η (default η = 0.20) |

### dt-clamp in Manim updaters Manim 更新器中的 dt 限制

All Manim scenes use the same dt-clamp pattern in their updater functions:

```python
h = min(dt, 1.0 / config.frame_rate)
```

This prevents a Manim edge-case where `dt` can be 0 on frame boundaries, which would cause the simulation to stall.

### Rendering notes 渲染說明

- The `render.sh` script passes `--disable_caching` to force a fresh render every time.
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.

---

## Synthetic-Only Note 全合成模式說明

All modes in the teacher app are **fully synthetic**. Unlike the pendulum mode in Unit 01 (which supported real webcam tracking), there is no camera input — all physics is computed and rendered procedurally. This makes the app deterministic and ideal for classroom projection without any hardware dependency.

教師示範程式的所有模式均為**全合成**。不像單元 01 的單擺模式（支援真實視訊追蹤），這裡沒有攝影機輸入，所有物理均由程式計算並程序化渲染，因此結果確定，適合無需任何硬體依賴的課堂投影。

---

## CAF Compliance Notes CAF 合規說明

### Half-life wording 半衰期的表述

The CAF (June 2026) removes the formal "exponential decay law" as named content. The current unit uses `N = N₀·2^(-t/T)` (powers of two) rather than the natural exponential form `N = N₀·e^(-λt)`. This is consistent with the CAF: half-life is presented as the quantity read from the decay curve, not derived from an exponential law. The `decay_probability` hook uses `p = 1 − exp(−λ dt)` internally, which is a computational implementation detail, not a curriculum outcome.

### Removed content 已刪除內容

- **Exponential law of decay**: Removed per Annex 3, line 4296–4297. The unit uses the half-life form `N = N₀·2^(-t/T)` which is consistent.
- **Transmutation**: Removed per Annex 3, line 4303. Not covered in this unit.

### Integrated content (Annex 3) 整合內容（附錄 3）

- **Medical imaging applications of radioisotopes** (from Medical Physics): Covered by `RadioisotopeUses` Manim scene.
- **Energy sources and sustainable development** (from Energy and Use of Energy): Covered by `energy.py` engine, `EnergySources` scene, `--mode energy` app, and `energy_exercise.py`.

### Out-of-scope (teacher-led activities) 範圍外（教師主導活動）

The following CAF-suggested activities are hands-on/experiential and outside the computational toolkit's scope:
- GM counter measurements of background radiation
- Radon concentration investigation
- Smoke detector specification review
- Radioactive waste handling research
- Power plant visits and guest talks

These should be delivered as complementary teacher-led activities.