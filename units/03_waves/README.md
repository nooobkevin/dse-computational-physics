# Unit 03: Waves

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of the wave physics concept
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercise** (code) — a single-method coding task with an auto-grader

All three artifacts consume the same `physics_core` engine (`src/physics_core/waves/`), so the physics is identical across every front-end.

**Note:** The teacher app is fully synthetic (no webcam required) — it always works out of the box.

---

## 中文概覽

本單元涵蓋香港中學文憑（HKDSE）物理科「波動」主題，透過三個互相配合的教材元件教授：**Manim 動畫**（觀看）、**教師示範應用程式**（互動）及**學生填空練習**（編程）。核心概念包括波的疊加與駐波、波速與強度（I ∝ A²）、楊氏雙縫干涉、偏振（馬呂斯定律）、電磁波譜、超聲波測距及反平方定律。教師應用程式為全合成（無需網絡攝影機），開箱即用。課堂流程建議：先觀看動畫建立直觀概念，再以教師應用程式即場示範，最後讓學生完成填空練習。

---

## Curriculum Learning-Outcome Map (CAF Consultation Draft alignment)

This unit targets the following HKDSE Physics curriculum outcomes per the June 2026 CAF Consultation Draft (lines 1563–1842):

| Item | Content | Learning outcome(s) | Artifact(s) |
|------|---------|---------------------|-------------|
| **a. Nature of waves** | Wave motion and propagation; Traveling and stationary waves | Amplitude, wavelength, frequency, wave speed v = fλ; transverse vs longitudinal; energy ∝ A²; superposition → standing waves; interpret d-t graphs | Manim `SuperpositionStanding`, `WaveSpeedIntensity`; Teacher app (traveling, standing modes) |
| **b. Properties of waves** | Reflection, refraction, diffraction, interference; Young's double-slit; intensity distribution | d sin θ = n λ; bright/dark fringes; fringe spacing Δy = λD/d; I(y) double-slit intensity profile; path difference | Manim `YoungSlit` (fringe pattern + intensity panel); Teacher app (interference mode) |
| **c. Light waves / EM spectrum** | EM spectrum; speed of light; polarisation; intensity concepts; inverse-square law | c = 3.0×10⁸ m/s; EM spectrum bands (radio → gamma); visible ROYGBIV (400–700 nm); polarisation as transverse-wave evidence; Malus's law I = I₀ cos²θ; intensity ∝ 1/r²; data analysis on log-log plot | Manim `EMSpectrum`, `Polarisation`; Teacher app (inverse-square mode) |
| **d. Sound waves** | Ultrasound; musical notes; resonance | Pulse-echo ranging d = v×t/2; ultrasound imaging; frequency → pitch; amplitude → loudness; resonance | Manim `UltrasoundRanging` (pulse-echo + medical imaging strip); Student exercise concept questions |

### Removed content (CAF Annex 3 compliance)

- **Geometrical optics** (ray diagrams, lenses, lens formula) — REMOVED from core. No artifacts cover this topic. If any existing code references ray diagrams, it is labelled "beyond CAF core" and kept for reference only.
- **Noise** — REMOVED from core. No artifacts cover this topic.
- **Longitudinal wave d-t/d-d graphs** — REMOVED for traveling waves. The unit's d-t graph is transverse-only, which remains in the curriculum.

### Cross-unit references

- **Total internal reflection / optical fibres** — now live in **Unit 05 (Physics & Engineering)**. The wave nature of TIR is introduced conceptually in Unit 03 (c.5) and applied in Unit 05.

### 學習成果對應（中文摘要）

本單元對應 CAF 課程「波動」的學習成果：**a. 波的性質**（振幅、波長、頻率、波速 v = fλ、橫波與縱波、能量 ∝ A²、疊加形成駐波）；**b. 波的特性**（反射、折射、衍射、干涉、楊氏雙縫、d sin θ = nλ、條紋間距 Δy = λD/d）；**c. 光波／電磁波譜**（c = 3.0×10⁸ m/s、電磁波譜波段、可見光 ROYGBIV、偏振與馬呂斯定律 I = I₀ cos²θ、反平方定律 I ∝ 1/r²）；**d. 聲波**（脈衝回聲測距 d = v×t/2、超聲波成像、頻率→音高、振幅→響度、共振）。已刪除內容（CAF Annex 3）：幾何光學（光線圖、透鏡）、噪音、縱波的 d-t/d-d 圖。全內反射／光纖現於單元 05 教授。

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Superposition / standing waves**: `SuperpositionStanding.mp4` — two counter-propagating traveling waves (blue and orange) and their superposition (green) forming a standing wave with fixed nodes (red markers).
- **Wave speed and intensity**: `WaveSpeedIntensity.mp4` — three traveling waves with different amplitudes, bar chart showing I ∝ A².
- **Young's double-slit**: `YoungSlit.mp4` — double-slit geometry with bright fringes labelled by order n, formula d sin θ = n λ, animated rays sweeping the screen, and an I(y) intensity-distribution panel with maxima/minima labelled.
- **Polarisation**: `Polarisation.mp4` — transverse wave passing through a polariser slit at angle θ, transmitted amplitude A cos(θ), Malus's law I = I₀ cos²(θ) shown live; two crossed polarisers go to zero.
- **Ultrasound ranging**: `UltrasoundRanging.mp4` — pulse emitted from a transducer, reflects off a target at distance d, echo returns; d = v×t/2 live readout; medical imaging strip at the end.
- **EM Spectrum**: `EMSpectrum.mp4` — electromagnetic spectrum infographic (radio → gamma) with wavelength/frequency bands, progressive reveal left to right, visible light zoomed into ROYGBIV, scanning cursor.

### Step 2: Run the teacher demo app

Open the teacher app in the relevant mode and demonstrate the physics live:

- **Traveling wave mode** (`--mode traveling`): sine wave with moving particle, displacement-vs-time graph builds in real time. Discuss amplitude, wavelength, frequency, phase, wave speed.
- **Standing wave mode** (`--mode standing`): two counter-propagating waves (thin lines) and their superposition (thick green) forming a standing wave. Nodes marked in red.
- **Interference mode** (`--mode interference`): Young's double-slit geometry with bright fringes labelled by order n, formula d sin θ = n λ displayed.
- **Inverse-square law mode** (`--mode inverse_square`): point source + detector at distance r; live I vs r plot building data points as r changes; log-log inset showing the straight line of slope -2. Designed as a data-analysis CP activity matching CAF §2.2.2.

### Step 3: Complete the fill-in-the-blank exercise

Students open `wave_exercise.py` and implement the single method `displacement(self, x, t)`. The auto-grader checks:

1. The `NotImplementedError` is replaced (immediate fail if not)
2. The field values match `A sin(kx - ωt)` to within 1e-10 tolerance
3. Superposition behaviour is correct (standing wave node check)
4. Intensity scales as amplitude squared (I ∝ A²)

The concept questions in `questions.md` cover superposition, standing vs traveling waves, intensity, inverse-square law, interference, polarisation, and ultrasound.

### 課堂流程（中文摘要）

建議課堂順序分三步：**第一步**播放 Manim 動畫（`SuperpositionStanding.mp4` 疊加／駐波、`WaveSpeedIntensity.mp4` 波速與強度、`YoungSlit.mp4` 楊氏雙縫、`Polarisation.mp4` 偏振、`UltrasoundRanging.mp4` 超聲波測距、`EMSpectrum.mp4` 電磁波譜）；**第二步**以教師應用程式即場示範（行波、駐波、干涉、反平方定律四種模式，全合成無需攝影機）；**第三步**讓學生完成填空練習（實作 `displacement(self, x, t)`），並以自動評分器核對。`questions.md` 的概念題涵蓋疊加、駐波對行波、強度、反平方定律、干涉、偏振及超聲波。

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

This runs the unit tests in `tests/` (including `test_waves.py`). The `pyproject.toml` sets `pythonpath = ["src"]` so `physics_core` is importable.

### Teacher app

```bash
# Traveling wave mode (synthetic — always works)
uv run python units/03_waves/teacher_app/main.py --mode traveling

# Standing wave mode (synthetic)
uv run python units/03_waves/teacher_app/main.py --mode standing

# Interference / Young's double-slit mode (synthetic)
uv run python units/03_waves/teacher_app/main.py --mode interference

# Inverse-square law mode (synthetic) — CAF-named data-analysis CP activity
uv run python units/03_waves/teacher_app/main.py --mode inverse_square

# Headless self-check (no window, for CI)
uv run python units/03_waves/teacher_app/main.py --mode inverse_square --headless-selfcheck
```

The teacher app is fully synthetic — no webcam is needed. The `--headless-selfcheck` flag runs a few frames without opening a window and exits — useful for CI or testing.

### Manim render

```bash
# Render all scenes (requires Docker)
bash units/03_waves/manim/render.sh

# Render a specific scene
bash units/03_waves/manim/render.sh polarisation

# Low-quality preview (fast)
bash units/03_waves/manim/render.sh polarisation -ql
```

The script uses the `manimcommunity/manim:stable` Docker image. Output MP4 files land in `units/03_waves/manim/output/`. The `--disable_caching` flag is set to force re-render on every run.

Available scenes: `superposition_standing`, `wave_speed_intensity`, `young_slit`, `polarisation`, `ultrasound_ranging`, `em_spectrum`.

Quality flags: `-qh` (high, default), `-ql` (low, fast preview), `-qk` (4K).

### Exercise / grader

```bash
# Grade the student's exercise (default: wave_exercise.py)
uv run pytest units/03_waves/exercises/test_exercise.py -v

# Grade against the solution file (teacher self-check)
uv run pytest units/03_waves/exercises/test_exercise.py \
    --override-student=units/03_waves/exercises/wave_solution.py -v

# Full self-check: verify grader passes correct answer AND catches wrong one
uv run pytest units/03_waves/exercises/test_exercise.py --selfcheck -v
```

The solution file (`wave_solution.py`) and teacher answer key (`teacher_key.md`) are gitignored — students must not see them.

### 執行方法（中文摘要）

先以 `uv sync` 安裝依賴。引擎測試用 `uv run pytest`。教師應用程式以 `uv run python units/03_waves/teacher_app/main.py --mode traveling|standing|interference|inverse_square` 執行（全合成，無需網絡攝影機）。Manim 動畫以 `bash units/03_waves/manim/render.sh` 渲染（需 Docker），輸出 MP4 存放於 `manim/output/`。評分以 `uv run pytest units/03_waves/exercises/test_exercise.py -v` 執行，教師可加 `--override-student=...wave_solution.py` 自行核對。解答檔與教師答案檔（`teacher_key.md`）已加入 gitignore，學生不得查閱。

---

## Numerical-Methods Tie-In

The wave simulation in this unit is **analytical** rather than numerical — the traveling wave `y(x,t) = A sin(kx - ωt)` is a closed-form solution of the wave equation. This means:

- No ODE integration is needed (no Euler/Verlet steps)
- The solution is exact at every point in space and time
- Students can verify the wave equation `∂²y/∂t² = v² ∂²y/∂x²` analytically

The `WaveSpeedIntensity` Manim scene demonstrates the relationship between amplitude and intensity (I ∝ A²), which is a key concept for understanding wave energy transport.

### dt-clamp in Manim updaters

All Manim scenes use the same pattern in their updater functions — reading `self.time` rather than accumulating `dt`. This prevents a Manim edge-case where `dt` can be 0 on frame boundaries, which would cause the simulation to stall.

### Rendering notes

- The `render.sh` script passes `--disable_caching` to force a fresh render every time (cached frames from a previous run with different parameters would be stale).
- Output MP4s are flattened from the nested `videos/` directory into the flat `output/` directory by the script.

### 數值方法連結（中文摘要）

本單元的波動模擬屬**解析**而非數值：行波 `y(x,t) = A sin(kx - ωt)` 是波動方程的閉式解，無需 ODE 積分（無 Euler/Verlet 步驟），解在空間與時間的每一點均精確，學生可解析地驗證波動方程 `∂²y/∂t² = v² ∂²y/∂x²`。`WaveSpeedIntensity` 動畫示範振幅與強度的關係（I ∝ A²），是理解波動能量傳輸的關鍵概念。所有 Manim 場景的更新函數均讀取 `self.time` 而非累積 `dt`，以避免 Manim 在幀邊界 `dt` 為 0 的邊緣情況。

---

## Engine API Reference (`src/physics_core/waves/`)

### equations.py

| Function | Description |
|----------|-------------|
| `wave_speed(f, λ)` | v = fλ |
| `angular_frequency(f)` | ω = 2πf |
| `wave_number(λ)` | k = 2π/λ |
| `intensity(A)` | I ∝ A² |
| `intensity_inverse_square(r, I₀)` | I = I₀ / r² |
| `young_slit_dsin(d, θ, n)` | d sin θ = nλ → λ |
| `young_slit_angle(λ, d, n)` | d sin θ = nλ → θ |
| `diffraction_grating_angle(λ, d, n)` | d sin θ = nλ for grating |
| `malus_law(I₀, θ)` | I = I₀ cos²θ |
| `ultrasound_echo_distance(v, t)` | d = v×t/2 |
| `young_slit_intensity(y, d, a, D, λ)` | I(y) = I₀ cos²(πdy/λD) · sinc²(πay/λD) |

### wave_sim.py

| Class / Method | Description |
|----------------|-------------|
| `WaveSim` | Abstract base with `displacement()` hook |
| `ReferenceWaveSim` | Correct analytical physics: `y = A sin(kx - ωt)` |
| `.displacement(x, t)` | Single-point displacement |
| `.field(x_arr, t)` | Array displacement |
| `.standing_wave(x, t)` | Standing wave via superposition |
| `.step(dt)` | Advance time |
| `.energy()` | Returns `{"total": A²}` |

### 引擎 API 摘要（中文）

`equations.py` 提供波動常用函數：`wave_speed(f, λ)`（v = fλ）、`angular_frequency(f)`（ω = 2πf）、`wave_number(λ)`（k = 2π/λ）、`intensity(A)`（I ∝ A²）、`intensity_inverse_square(r, I₀)`（I = I₀/r²）、`young_slit_dsin`／`young_slit_angle`／`diffraction_grating_angle`（d sin θ = nλ）、`malus_law(I₀, θ)`（I = I₀ cos²θ）、`ultrasound_echo_distance(v, t)`（d = v×t/2）、`young_slit_intensity`（雙縫強度分佈）。`wave_sim.py` 中 `WaveSim` 為抽象基底（含 `displacement()` 鉤子），`ReferenceWaveSim` 提供正確解析物理 `y = A sin(kx - ωt)`，並提供 `.field`、`.standing_wave`、`.step`、`.energy` 等方法。