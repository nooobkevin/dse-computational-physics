# Unit 01: Mechanics 力學 — S4

## The Big Idea 本課主線

> **One sentence:** 力學的每個「定律」都是同一個想法——**位置隨時間怎麼變**。
> 這一課的每個動畫都在回答一個具體問題，而抽象公式是那些問題的答案。

---

## Hook: 先問一個「為什麼」，再給公式

不要從定義開始。先讓學生心裡有這個問題，才讓公式登場。

| # | 具體 Hook 問題 | 對應動畫 | 背後的 aha moment |
|---|---|---|---|
| 1 | 「為什麼我晃一個掛在繩上的球，它會上下來回、而且**來回一次要的時間固定**？」 | `ShmProjection.mp4` | 簡諧運動 = 圓周運動的投影：時間固定是因為圓周轉速固定 |
| 2 | 「我在電腦裡模擬一個單擺，為什麼**越小步走一算，能量越飄**？」 | `IntegratorConvergence.mp4` | 數值方法有「品質」：Euler 會偷加能量，Verlet 不會 |
| 3 | 「同樣一個砲彈，為什麼我**算得越粗心，飛得越近**？」 | `ProjectileDt.mp4` | 步長 dt 控制誤差；細步長逼近解析解 |
| 4 | 「汽車避震器為什麼要調到**剛剛好**？太軟太硬都不行？」 | `DampedSHM.mp4` | 欠/臨界/過阻尼三種衰減；臨界阻尼回正最快 |
| 5 | 「為什麼跳過某些頻率時，鞦韆會**越盪越高**？」 | `Resonance.mp4` | 驅動頻率 = 固有頻率時能量最有效輸入（共振）|
| 6 | 「月球上跳一下，跟地球上跳一下，誰飄得久？」 | `PlanetFreeFall.mp4` | g 因星球而異，落地時間隨 √(1/g) 長 |
| 7 | 「為什麼高爾夫球飛得比想像中近？」 | `ProjectileDrag.mp4` | 空氣阻力使實際拋體偏離理想拋物線 |

## The Payoff 核心 Aha（全課支點）

> **「能量守恆」是看懂所有力學場景的那把鑰匙。**
> - Euler 偷能量 → 越算越亂（`IntegratorConvergence`）
> - Verlet 守能量 → 軌跡可信（`IntegratorConvergence`）
> - 阻尼散能量 → 振幅遞減（`DampedSHM`）
> - 共振輸入能量 → 振幅暴增（`Resonance`）

讓學生先握住這個主線，再看每個場景，就不會覺得是七個孤立的公式。

---

## Key Formulas 核心公式（在 aha 之後登場）

| Formula | Meaning | 出現於 |
|---|---|---|
| $x(t) = R\cos(\omega t)$ | SHM 是圓周投影 | Hook 1 |
| $T = 2\pi\sqrt{L/g}$ | 單擺週期（能量守恒的種子） | Hook 1/6 |
| $v^2 = u^2 + 2as$ | SUVAT（無時間式） | Hook 3 |
| $\alpha = -\frac{g}{L}\theta - b\,\omega$ | 阻尼擺角加速度 | Hook 4 |
| $A(\omega_d)=\frac{g/L}{\sqrt{(\omega_0^2-\omega_d^2)^2+(b\omega_d)^2}}$ | 振盪幅值-頻率響應 | Hook 5 |
| $KE = \tfrac{1}{2}mv^2,\ PE = mgh$ | 機械能（驗證守恆） | Hook 2 |

## Lesson Flow 課堂流程（敘事順序）

**Step 1 — 建立主線（3 min）** 先講「能量守恆是鑰匙」，播放 `IntegratorConvergence.mp4`：看 Euler 怎麼偷能量。

**Step 2 — 逐個解 hook（每 hook 一個場景）**
1. 晃繩球 → `ShmProjection.mp4`（圓周投影）
2. 砲彈誤差 → `ProjectileDt.mp4` + `ProjectileDrag.mp4`（dt 與阻力）
3. 涉振器 → `DampedSHM.mp4`（三種阻尼）
4. 鞦韆 → `Resonance.mp4`（共振）
5. 月球跳 → `PlanetFreeFall.mp4`（g vs.T）

**Step 3 — 動手發現（Interact，非示範）** 用 `--mode pendulum` 讓學生自己動：把 `--length` 改大改小、把初角 θ₀ 調大，觀察週期怎麼變——自己「發現」T ∝ √(L/g)，而非被告訴。

**Step 4 — 用代碼驗證（Code）** 讓學生 `pendulum_exercise.py` 填 `angular_acceleration`，跑通後用 `test_exercise.py` 檢查能量漂移 < 2%（Verlet）——把「能量守恆」從口號變成他們親手證明的東西。

## Simulation Commands 指令
```bash
uv sync
uv run python units/01_mechanics/teacher_app/main.py --mode pendulum   # 動手發現
uv run python units/01_mechanics/teacher_app/main.py --mode circular
uv run python units/01_mechanics/teacher_app/main.py --mode projectile
bash units/01_mechanics/manim/render.sh shm_projection -ql   # Docker（重渲染）
uv run pytest units/01_mechanics/exercises/test_exercise.py -v
```

## Assessment 評估
- **Exercise** 練習: `uv run pytest units/01_mechanics/exercises/test_exercise.py -v` (auto-grader).
- **Quiz** 小測: `uv run pytest units/01_mechanics/exercises/test_quiz.py` (expect 10 fails on blank).
- **Teacher key** 教師核對: `DSE_QUIZ_ANSWERS=units/01_mechanics/exercises/quiz_solution.py uv run pytest units/01_mechanics/exercises/test_quiz.py` (expect 10 passes).
