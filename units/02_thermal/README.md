# Unit 02: Thermal Physics

## Overview

This unit follows the three-artifact pattern shared by every unit in the toolkit:

1. **Manim animation** (watch) — visual explanation of kinetic theory, gas laws, and random walk
2. **Teacher demo app** (interact) — real-time OpenCV application for classroom demonstration
3. **Student fill-in-the-blank exercises** (code) — coding tasks with auto-graders

All three artifacts consume the same `physics_core` engine (`src/physics_core/thermal/`),
so the physics is identical across every front-end.

---

## 中文概覽

本單元涵蓋香港中學文憑（HKDSE）物理科「熱學」主題，透過三個互相配合的教材元件教授：**Manim 動畫**（觀看）、**教師示範應用程式**（互動）及**學生填空練習**（編程）。核心概念包括分子動力論、麥克斯韋-玻爾茲曼（Maxwell-Boltzmann）速率分佈、氣體定律與絕對零度、分子隨機行走（擴散）、比熱容（數據分析）及能量均分定理。課堂流程建議：先觀看動畫建立直觀概念，再以教師應用程式即場示範氣體模式與氣體定律模式，最後讓學生完成氣體與比熱容兩項填空練習。

---

## Curriculum Learning-Outcome Map (CAF 2026)

This unit targets the following HKDSE Physics (CAF Consultation Draft) outcomes:

### a. Heat transfer — heat and internal energy

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| **Temperature as average KE of random molecular motion**: `KE_avg = 3RT/(2N_A) = (3/2)kT` | Teacher app gas mode (KE display, T_est from equipartition); questions.md (g) |
| **Specific heat capacity**: `c = Q/(mΔT)`, fit experimental data | Exercise `specific_heat_exercise.py` (data-analysis: fit Q vs ΔT → c) |
| **Zeroth law of thermodynamics** / thermal equilibrium | Questions.md (i) |
| **Internal energy** as sum of molecular KE + PE | Questions.md (g) (KE_avg relates T to KE) |

### b. Change of state — latent heat, evaporation

*Out of scope for computational physics toolkit this iteration. Calorimetry labs
(latent heat, phase change, cooling curves) are teacher-led practical activities
and are not covered by CP artifacts. See "Removed-content compliance" below.*

### c. Gases — general gas law and kinetic theory

| Learning outcome(s) | Which artifact(s) deliver it |
|---|---|
| **Boyle's law** (p-V), **pressure law** (p-T), **Charles' law** (V-T) | Teacher app `--mode gas_laws` (P-V curve, P-T curve with absolute-zero extrapolation) |
| **Determine absolute zero** by extrapolation of p-T | Teacher app `--mode gas_laws` (P-T graph with linear fit → absolute zero) |
| **Use Kelvin scale** | Questions.md (g)-(h); teacher app Kelvin discussion; pV = NkT formula |
| **Combine to pV/T = constant; solve problems using pV = nRT** | Teacher app `--mode gas_laws` (Boyle + pressure law verification) |
| **Random motion of molecules** | Teacher app gas mode (live MD trajectories); RandomWalkScene (diffusion model) |
| **Gas pressure from molecular bombardment** | Teacher app gas mode (live P_meas vs P_ideal); PressureStatistical scene |
| **KE_avg = 3RT/(2N_A)** relating T to microscopic KE | Teacher app (equipartition T_est); questions.md (g) |
| **Maxwell-Boltzmann distribution** (interpret temperature change) | MaxwellBoltzmann scene; teacher app MB overlay; questions.md (a) |

### Suggested computational physics activities (CAF lines 1543–1546)

| Activity | Which artifact(s) deliver it |
|---|---|
| **Simulate random walk of molecules** | RandomWalk engine + RandomWalkScene (Manim: many walkers, RMS ring) |
| **Simulate motions of gas molecules + MB distribution** | Teacher app gas mode; MaxwellBoltzmann scene; PressureStatistical scene |

### 學習成果對應（中文摘要）

本單元對應 CAF 課程「熱學」的學習成果：**a. 熱傳遞與內能**（溫度為分子隨機運動的平均動能 `KE_avg = 3RT/(2N_A) = (3/2)kT`、比熱容 `c = Q/(mΔT)`、熱力學第零定律、內能）；**c. 氣體與分子動力論**（波義耳定律、壓力定律、查理定律、以 p-T 外推求絕對零度、開爾文溫標、pV = nRT、分子隨機運動、氣體壓力、麥克斯韋-玻爾茲曼分佈）。CAF 建議的計算物理活動包括模擬分子隨機行走及模擬氣體分子運動與 MB 分佈。

---

## Lesson Flow (Suggested Sequence)

### Step 1: Watch the Manim scene(s)

Play the rendered MP4 for the topic you are about to teach:

- **Random walk (diffusion)**: `RandomWalkScene.mp4` — many walkers spread from the origin
  on a 2D grid, with an RMS-radius ring expanding as sqrt(t).  Demonstrates that
  RMS displacement grows as sqrt(N), modelling gas molecule diffusion.
- **Maxwell-Boltzmann distribution**: `MaxwellBoltzmann.mp4` — theoretical MB speed
  distribution at different temperatures, alongside measured distribution.
- **Pressure from collisions**: `PressureStatistical.mp4` — gas box with particles,
  pressure-vs-time graph converging toward the ideal gas law, MB overlay.
- **Numerical methods**: `IntegratorConvergence.mp4` — Euler vs Verlet comparison.

### Step 2: Run the teacher demo app

Open the teacher app and demonstrate the physics live:

- **Gas mode** (`--mode gas`): spawns N particles in a 2D box with velocity arrows.
  Shows speed distribution with MB overlay, live pressure vs ideal gas law, average
  and RMS speed, estimated temperature from equipartition.
- **Gas laws mode** (`--mode gas_laws`): two live graphs — Boyle's law (P vs V, isothermal)
  and pressure law (P vs T, isochoric) with absolute-zero extrapolation.

### Step 3: Complete the fill-in-the-blank exercises

**Gas exercise**: Students implement `_collide_wall` and `_collide_particle`
in `gas_exercise.py`.  The auto-grader checks pressure, energy conservation,
speed distribution, and wall bounce.

**Specific heat exercise**: Students implement `specific_heat_from_fit`,
`energy_to_heat`, and `final_temperature` in `specific_heat_exercise.py`.
The auto-grader checks the linear fit (Q vs ΔT → c), the energy formula Q = mcΔT,
and the temperature change formula.

### 課堂流程（中文摘要）

建議課堂順序分三步：**第一步**播放 Manim 動畫（`RandomWalkScene.mp4` 隨機行走／擴散、`MaxwellBoltzmann.mp4` 速率分佈、`PressureStatistical.mp4` 碰撞壓力、`IntegratorConvergence.mp4` 數值方法）；**第二步**以教師應用程式即場示範（氣體模式 `--mode gas` 顯示速率分佈、即時壓力與理想氣體定律、能量均分估算溫度；氣體定律模式 `--mode gas_laws` 顯示波義耳定律與壓力定律及絕對零度外推）；**第三步**讓學生完成填空練習（氣體練習實作 `_collide_wall` 與 `_collide_particle`；比熱容練習實作 `specific_heat_from_fit`、`energy_to_heat`、`final_temperature`），並以自動評分器核對。

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
uv run pytest tests/test_thermal.py -v
```

### Teacher app

```bash
# Gas mode (fully synthetic — no webcam needed)
uv run python units/02_thermal/teacher_app/main.py --mode gas

# Gas laws mode (Boyle + absolute-zero extrapolation)
uv run python units/02_thermal/teacher_app/main.py --mode gas_laws

# Headless self-check (no window, for CI)
uv run python units/02_thermal/teacher_app/main.py --mode gas --headless-selfcheck
uv run python units/02_thermal/teacher_app/main.py --mode gas_laws --headless-selfcheck
```

Options:
- `--N <count>` — number of gas particles (default: 200, gas mode only)
- `--T <temperature>` — initial temperature (default: 2.0, gas mode only)

### Manim render

```bash
# Render all scenes (requires Docker)
bash units/02_thermal/manim/render.sh

# Render a specific scene
bash units/02_thermal/manim/render.sh random_walk

# Low-quality preview (fast)
bash units/02_thermal/manim/render.sh random_walk -ql
```

Available scenes: `maxwell_boltzmann`, `integrator_convergence`, `pressure_statistical`,
`random_walk`.

### Exercise / grader

```bash
# Grade the gas exercise
uv run pytest units/02_thermal/exercises/test_exercise.py -v

# Grade the specific heat exercise
uv run pytest units/02_thermal/exercises/test_exercise.py -k TestSpecificHeat -v

# Grade against the solution file (teacher self-check)
uv run pytest units/02_thermal/exercises/test_exercise.py -v \
    --override-student=units/02_thermal/exercises/gas_solution.py

uv run pytest units/02_thermal/exercises/test_exercise.py -v \
    --override-student=units/02_thermal/exercises/specific_heat_solution.py \
    -k TestSpecificHeat

# Full self-check
uv run pytest units/02_thermal/exercises/test_exercise.py --selfcheck -v
```

### 執行方法（中文摘要）

先以 `uv sync` 安裝依賴。引擎測試用 `uv run pytest tests/test_thermal.py -v`。教師應用程式以 `uv run python units/02_thermal/teacher_app/main.py --mode gas|gas_laws` 執行（全合成，無需網絡攝影機），可加 `--N` 設定粒子數、`--T` 設定初始溫度。Manim 動畫以 `bash units/02_thermal/manim/render.sh` 渲染（需 Docker）。評分以 `uv run pytest units/02_thermal/exercises/test_exercise.py -v` 執行，比熱容練習加 `-k TestSpecificHeat`，教師可加 `--override-student=...solution.py` 自行核對。

---

## Key Formulas

| Formula | Context |
|---|---|
| `KE_avg = 3RT/(2N_A) = (3/2)kT` | Average kinetic energy per molecule (CAF required) |
| `C = Q/ΔT` | Heat capacity |
| `c = Q/(mΔT)` | Specific heat capacity |
| `pV = NkT` | Ideal gas law (simulation units) |
| `pV = nRT` | Ideal gas law (real-world constants) |
| `P ∝ 1/V` (Boyle), `P ∝ T` (pressure law), `V ∝ T` (Charles') | Empirical gas laws |
| `RMS = s√N` | Random walk RMS displacement |
| `f(v) = (m/kT) v exp(-mv²/2kT)` (2D) | Maxwell-Boltzmann speed distribution |
| `T(K) = T(°C) + 273.15` | Kelvin-Celsius conversion |

### 主要公式（中文摘要）

`KE_avg = 3RT/(2N_A) = (3/2)kT`（每分子平均動能）、`C = Q/ΔT`（熱容量）、`c = Q/(mΔT)`（比熱容）、`pV = NkT` 與 `pV = nRT`（理想氣體定律）、`P ∝ 1/V`（波義耳）、`P ∝ T`（壓力定律）、`V ∝ T`（查理定律）、`RMS = s√N`（隨機行走 RMS 位移）、`f(v) = (m/kT) v exp(-mv²/2kT)`（2D 麥克斯韋-玻爾茲曼速率分佈）、`T(K) = T(°C) + 273.15`（開爾文-攝氏換算）。

---

## Removed-Content Compliance (CAF Annex 3)

The following topics were **removed** from the CAF curriculum and are NOT
taught by this unit's artifacts:

- **Thermometers** — not covered (removed from CAF)
- **Transfer processes** (conduction, convection, radiation) — not covered
- **PV = (1/3)Nm⟨c²⟩** — not covered (removed from CAF)
- **Real gases** — not covered (simulation uses ideal gas model)

If any existing scene or question references these topics, the relevant code
is preserved but labelled "beyond CAF core" for reference use only.

### Out-of-scope notes

- **Calorimetry labs** (determine specific heat capacity, latent heat,
  cooling curves) are teacher-led practical activities and are out of scope
  for the computational physics toolkit.  The specific heat exercise in
  this unit is a data-analysis CP activity (fitting Q vs ΔT), not a
  calorimetry simulation.
- **Phase change** (melting, boiling, latent heat, evaporation) is not
  covered by any CP artifact this iteration.
- **2D vs 3D note**: The gas simulation uses 2D for visual clarity, but the
  CAF kinetic theory outcomes (KE_avg = 3RT/(2N_A)) are explicitly 3D.
  The Maxwell-Boltzmann distribution helpers in `equations.py` support both
  2D and 3D formulas.  Teachers should be aware of this dimensional mismatch
  when discussing the 3/2 factor in KE_avg.

### 已刪除內容與範圍說明（中文摘要）

以下主題已從 CAF 課程**刪除**，本單元不教授：溫度計、傳遞過程（傳導、對流、輻射）、`PV = (1/3)Nm⟨c²⟩`、真實氣體（模擬採用理想氣體模型）。量熱實驗（測定比熱容、潛熱、冷卻曲線）屬教師主導的實驗活動，不在計算物理工具套件範圍內；本單元的比熱容練習是數據分析活動（擬合 Q 對 ΔT），並非量熱模擬。相變（熔化、沸騰、潛熱、蒸發）本迭代亦無任何 CP 教材涵蓋。注意：氣體模擬為 2D 以求視覺清晰，但 CAF 分子動力論成果（KE_avg = 3RT/(2N_A)）明確為 3D，討論 KE_avg 的 3/2 因子時教師應留意此維度差異。

---

## Architecture Notes

### Random walk engine

`physics_core.thermal.random_walk.RandomWalk` is a standalone engine (no
abstract-base / Reference pattern needed).  It provides:

- Seeded deterministic RNG for reproducibility
- 1D or 2D random walk with configurable step length
- Pre-computed position history and RMS displacement
- Final displacement histogram (for distribution analysis)

### Gas simulation engine

`physics_core.thermal.gas_sim.GasSim` is the abstract base with two
physics hooks: `_collide_wall` and `_collide_particle`.  `ReferenceGasSim`
provides the correct reference implementation.  Extended with:

- `set_volume(new_L)` — moving-wall compression/expansion
- `set_temperature(new_T)` — rescale velocities for heating/cooling
- `gas_law_isothermal_curve(V_values)` — generate P-V data (Boyle's law)
- `gas_law_isochoric_curve(T_values)` — generate P-T data (pressure law)

### Specific heat exercise

The exercise uses standalone functions (no class hierarchy needed for
data-analysis style exercises):

- `specific_heat_from_fit(Q_data, delta_T_data, mass) → (C, c, slope_err)`
- `energy_to_heat(mass, c, delta_T) → Q`
- `final_temperature(Q, mass, c, T_initial) → T_final`

### 架構說明（中文摘要）

**隨機行走引擎** `physics_core.thermal.random_walk.RandomWalk` 為獨立引擎（無需抽象基底／Reference 模式），提供可重現的種子隨機數、1D 或 2D 隨機行走、預先計算的位置歷史與 RMS 位移，以及最終位移直方圖。**氣體模擬引擎** `physics_core.thermal.gas_sim.GasSim` 為抽象基底，含兩個物理鉤子 `_collide_wall` 與 `_collide_particle`，`ReferenceGasSim` 提供正確參考實作，並擴充 `set_volume`、`set_temperature`、`gas_law_isothermal_curve`、`gas_law_isochoric_curve`。**比熱容練習**使用獨立函數（數據分析型練習無需類別階層）：`specific_heat_from_fit`、`energy_to_heat`、`final_temperature`。