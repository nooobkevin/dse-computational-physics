# Unit 08: Astrophysics and Relativity

> **中文概覽**：本單元涵蓋天體物理與相對論的核心概念，包括都卜勒紅移、哈勃定律與宇宙膨脹、恆星演化與赫羅圖、視差測距、黑洞與中子星、時間膨脹與時空圖，以及大爆炸與宇宙微波背景輻射。所有教材均共用同一套 `physics_core` 引擎，確保動畫、教師示範程式與學生練習的物理內容完全一致。

## Overview 概覽

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-class coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/astrophysics/`), so the physics is identical across every front-end.

**中文摘要**：本單元沿用工具箱中每個單元共用的「三件教材」模式：Manim 動畫（觀看）、教師示範程式（互動）與學生填空練習（編程）。三者共用同一套 `physics_core` 引擎，因此所有介面的物理內容完全一致。

---

## Curriculum Learning-Outcome Map (CAF June 2026) 課程學習成果對照（CAF 2026 年 6 月）

This unit targets the following HKDSE Physics curriculum outcomes per the CAF Consultation Draft:

**中文摘要**：本單元對應 HKDSE 物理課程（CAF 諮詢稿）的學習成果，涵蓋觀測天空（視差測距、光年／天文單位／秒差距）、恆星與宇宙（黑體輻射、赫羅圖、史特凡-波茲曼定律、都卜勒效應、暗物質、紅移與大爆炸）、相對論（參考系、光速不變、時間膨脹、長度收縮、時空圖、衛星導航）等範疇。

### a. Observing the sky

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| **a.3** Determine distance using parallax | Teacher app (`--mode parallax` — apparent shift of near star against background, live d = 1/p); Concept questions (Q i) |
| **a.4** Light year, AU, parsec as distance units | Teacher app (`--mode parallax` — displays distance in pc and ly); Concept questions (Q i) |

### b. Stars and the universe

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| **b.1** Blackbody radiation curves — temperature, colour, luminosity | Manim `HRDiagramScene` (blackbody-curve inset with colour morphing as T sweeps); Engine `hr_diagram.py` (Planck curve, Wien's law); Student exercise `StudentStars` (`peak_wavelength`, `blackbody_curve`) |
| **b.2** H-R diagram classification | Manim `HRDiagramScene` (log L vs T, main-sequence band, giant and white-dwarf regions, sample stars); Student exercise `StudentStars` (`classify`) |
| **b.3** Stefan-Boltzmann law L = 4πR²σT⁴ | Engine `hr_diagram.py` (`luminosity`, `radius_from_luminosity`); Student exercise `StudentStars` (`luminosity`, `radius_from_luminosity`) |
| **b.4** Estimate relative size of stars using H-R diagram | Engine `hr_diagram.py` (`radius_from_luminosity`); Student exercise (radius-from-luminosity hook) |
| **b.6** Doppler effect (Δλ/λ₀ = vᵣ/c) | Manim `DopplerRedshift`; Teacher app (`--mode doppler`); Student exercise (`observed_frequency`, `redshift`, `velocity_from_z`); Engine `doppler.py` |
| **b.7** Dark matter from rotation curves | Teacher app (`--mode hubble` — rotation-curve panel with Keplerian vs flat curve, dark matter annotation) |
| **b.8** Redshift → Big Bang theory | Manim `BigBangEvidence` (two pillars of evidence: universal expansion/redshift via an inflating balloon-surface analogy `v = H₀·d`; the CMB blackbody curve at `T = 2.725 K` peaking ≈ 1.06 mm, with a faint dipole anisotropy); Concept questions (Q h) |

### c. Relativity

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| **c.1** Frames of reference / limitations of Newtonian mechanics | Manim `SpacetimeDiagram` (two observers in different inertial frames); Teacher app (`--mode relativity`) |
| **c.2** Principle of invariant light speed | Engine `relativity.py` (Lorentz transform preserves c); Teacher app self-check verifies invariance |
| **c.3** Time dilation Δt = Δt₀ / √(1 − v²/c²) | Engine `relativity.py` (`time_dilated`); Teacher app (`--mode relativity` — live gamma and dilated dt); Student exercise `StudentRelativity` (`time_dilated`) |
| **c.4** Length contraction l = l₀√(1 − v²/c²) | Engine `relativity.py` (`length_contracted`); Teacher app (`--mode relativity` — contracted length display); Student exercise `StudentRelativity` (`length_contracted`) |
| **c.5** Spacetime diagram | Manim `SpacetimeDiagram` (ct-x diagram, light cones, worldlines, relativity of simultaneity); Teacher app (`--mode relativity` — mini spacetime diagram) |
| **c.7** Satellite navigation / relativistic effects | Concept questions (Q g — GPS 38 µs/day correction) |

### Computational Physics Activities (CAF-specified)

| Activity | Artifact(s) |
|---|---|
| Simulate Doppler effect | Manim `DopplerRedshift`; Teacher app `--mode doppler`; Student exercise |
| Simulate frames of reference for simultaneity and time dilation | Manim `SpacetimeDiagram`; Teacher app `--mode relativity`; Student exercise `StudentRelativity` |

### Enrichment (beyond CAF core)

| Topic | Where it appears | Status |
|---|---|---|
| Spectral classes O B A F G K M | `SPECTRAL_CLASSES` table in `hubble.py`; Teacher app `--mode lifecycles`; Manim `StellarLifecycle` | **Enrichment** — removed from CAF core (Annex 3 lines 4309–4310); retained as teacher reference |
| Stellar life cycle (nebula → main sequence → giant → white dwarf / neutron star) | Manim `StellarLifecycle`; Teacher app `--mode lifecycles` | **Enrichment** — useful context for H-R diagram |

---

## Lesson Flow (Suggested Sequence) 教學流程（建議次序）

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Doppler redshift**: `DopplerRedshift.mp4` — shows a source emitting light waves at rest, then approaching (blueshift, compressed waves), then receding (redshift, stretched waves).
- **Hubble's law**: `HubbleLawScene.mp4` — shows an expanding-universe scatter plot with galaxy dots and the v = H₀·d line.
- **Stellar life cycle**: `StellarLifecycle.mp4` — shows a schematic flow diagram of stellar evolution (enrichment).
- **Spacetime diagram**: `SpacetimeDiagram.mp4` — shows a ct-x Minkowski diagram with light cones, two observers' worldlines, and relativity of simultaneity.
- **H-R diagram**: `HRDiagramScene.mp4` — shows log L vs T axes, main-sequence band, giant and white-dwarf regions, sample stars, and a blackbody-curve inset whose colour morphs with temperature.
- **Big Bang evidence**: `BigBangEvidence.mp4` — the two pillars of evidence for the Big Bang: an inflating balloon-surface analogy for universal expansion (galaxy dots receding, `v = H₀·d`, farther = faster), and the CMB — a nearly uniform glow whose blackbody curve peaks at `T = 2.725 K` (≈ 1.06 mm), plus a faint dipole anisotropy bar. Closes with "CMB + redshift = evidence for the Big Bang".

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Doppler mode** (`--mode doppler`): a sine wave representing light from a source is animated; the source's velocity sweeps sinusoidally through approaching → rest → receding.
- **Hubble mode** (`--mode hubble`): a scatter plot of synthetic galaxies with the theoretical v = H₀·d line, plus a rotation-curve panel showing Keplerian vs flat rotation curves (dark matter inference).
- **Lifecycles mode** (`--mode lifecycles`): a schematic flow diagram of stellar evolution with spectral-classification table (enrichment).
- **Relativity mode** (`--mode relativity`): speed slider from 0 to 0.99c; live gamma, dilated time for a 1-second proper interval, contracted length for a 1 m stick, mini spacetime diagram, and γ-vs-β plot.
- **Parallax mode** (`--mode parallax`): apparent shift of a near star against distant background as Earth moves ±1 AU; live d = 1/p (arcsec to parsec); Proxima Centauri reference.

### Step 3: Complete the fill-in-the-blank exercises

Students open the exercise files and implement the physics hooks:

1. **`astrophysics_exercise.py`** — `StudentDopplerShift`: `observed_frequency`, `redshift`, `velocity_from_z`, `hubble_velocity`.
2. **`stars_exercise.py`** — `StudentRelativity`: `lorentz_factor`, `time_dilated`, `length_contracted`. `StudentStars`: `luminosity`, `radius_from_luminosity`, `peak_wavelength`, `classify`.

The concept questions in `questions.md` tie the code to the broader curriculum.

**中文摘要**：建議教學次序為：先播放 Manim 動畫（都卜勒紅移、哈勃定律、恆星演化、時空圖、赫羅圖、大爆炸證據），再以教師示範程式即時示範（都卜勒、哈勃、恆星演化、相對論、視差等模式），最後讓學生完成填空練習（`astrophysics_exercise.py` 與 `stars_exercise.py`），並以 `questions.md` 的概念題連結課程內容。

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
uv run pytest tests/test_astrophysics.py -v
```

This runs all unit tests including Doppler shift, Hubble's law, special relativity, and H-R diagram physics.

### Teacher app

```bash
# Doppler mode (fully synthetic)
uv run python units/08_astrophysics/teacher_app/main.py --mode doppler

# Hubble mode (fully synthetic)
uv run python units/08_astrophysics/teacher_app/main.py --mode hubble

# Life cycles mode (fully synthetic)
uv run python units/08_astrophysics/teacher_app/main.py --mode lifecycles

# Relativity mode (fully synthetic)
uv run python units/08_astrophysics/teacher_app/main.py --mode relativity

# Parallax mode (fully synthetic)
uv run python units/08_astrophysics/teacher_app/main.py --mode parallax

# Headless self-check (no window, for CI)
uv run python units/08_astrophysics/teacher_app/main.py --mode doppler --headless-selfcheck
```

All modes are fully synthetic — no camera required. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all scenes (requires Docker)
bash units/08_astrophysics/manim/render.sh

# Render a specific scene
bash units/08_astrophysics/manim/render.sh spacetime_diagram

# Low-quality preview (fast)
bash units/08_astrophysics/manim/render.sh spacetime_diagram -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/08_astrophysics/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `doppler_redshift`, `hubble_law`, `stellar_lifecycle`, `spacetime_diagram`, `hr_diagram`, `big_bang_evidence`.

Quality flags: `-qm` (medium, default), `-qh` (high), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the Doppler shift exercise
uv run pytest units/08_astrophysics/exercises/test_exercise.py -v

# Grade the stars & relativity exercise
uv run pytest units/08_astrophysics/exercises/test_stars_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/08_astrophysics/exercises/test_stars_exercise.py -v \
    --override-student-stars=units/08_astrophysics/exercises/stars_solution.py

# Full self-check
uv run pytest units/08_astrophysics/exercises/test_stars_exercise.py --selfcheck \
    --override-student-stars=units/08_astrophysics/exercises/stars_solution.py -v
```

The solution files (`astrophysics_solution.py`, `stars_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

---

## Physics Engine Architecture 物理引擎架構

The `src/physics_core/astrophysics/` package mirrors the pattern established by `mechanics/` and `em/`:

```
src/physics_core/astrophysics/
  __init__.py           ← exports all classes
  doppler.py            ← DopplerShift (abstract) + ReferenceDopplerShift
  hubble.py             ← HubbleLaw + redshift_factor(z)=1+z, SPECTRAL_CLASSES table (enrichment)
  relativity.py         ← RelativityEngine (abstract) + ReferenceRelativityEngine
  hr_diagram.py         ← HRDiagram (abstract) + ReferenceHRDiagram + SAMPLE_STARS
```

Each abstract base defines physics **hooks** (raising `NotImplementedError`) that subclasses override. The `Reference*` subclasses provide the correct physics using the same formulas students are expected to implement.

**中文摘要**：`src/physics_core/astrophysics/` 套件沿用 `mechanics/` 與 `em/` 的設計模式：每個抽象基類定義物理「掛鉤」（拋出 `NotImplementedError`），由子類別覆寫；`Reference*` 子類別則以學生應實作的相同公式提供正確物理。

---

## Synthetic-Only Note 全合成模式說明

All modes in the teacher app are **fully synthetic**. Unlike the pendulum mode in Unit 01 (which supported real webcam tracking), there is no camera input — all physics is computed and rendered procedurally. This makes the app deterministic and ideal for classroom projection without any hardware dependency.

**中文摘要**：教師示範程式的所有模式均為「全合成」模式，無需攝影機輸入，所有物理皆以程序化方式計算與繪製。這使程式具確定性，適合在課堂投影使用，不依賴任何硬件。