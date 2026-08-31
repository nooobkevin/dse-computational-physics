# Pendulum Exercise — Concept Questions (M5)

These questions test your understanding of the physics behind the pendulum
simulation you just implemented.  Answer them in a few sentences each.

> 中文：以下問題測試你對剛才實作的擺錘模擬背後物理概念的理解。每題以數句作答。

---

## Questions

### (a) Estimating *g* from the measured period

You run your pendulum simulation with `length = 1.0 m` and measure an
oscillation period of `T = 2.01 s`.

1. Use the small-angle formula to estimate the gravitational acceleration
   *g* from these values.
2. Compute the percent error compared to the standard value *g* = 9.81 m/s².
3. Report your result with the appropriate number of significant figures.

> 中文：(a) 由量得的週期估算 *g*。你以 `length = 1.0 m` 執行擺錘模擬，量得振動週期 `T = 2.01 s`。
> 1. 利用小角度公式由這些數值估算重力加速度 *g*。
> 2. 與標準值 *g* = 9.81 m/s² 比較，計算百分誤差。
> 3. 以適當的有效數字位數報告結果。

### (b) Sources of error

In a real (physical) pendulum experiment, the measured period often differs
from the theoretical prediction.  List **at least three** sources of error
and explain how each one affects the measured period (does it make *T*
longer, shorter, or unpredictable?).

Consider:
- Air resistance / drag
- Parallax error when reading the angle
- The small-angle approximation
- Human reaction time when timing with a stopwatch
- Pixel-tracking noise (if using video analysis)

> 中文：(b) 誤差來源。在真實（物理）擺錘實驗中，量得的週期往往與理論預測不同。列出**至少三項**誤差來源，並解釋每一項如何影響量得的週期（會令 *T* 變長、變短，還是無法預測？）。
> 可考慮：空氣阻力／阻力、讀取角度時的視差誤差、小角度近似、以秒錶計時的人為反應時間、像素追蹤雜訊（若使用影片分析）。

### (c) Explicit Euler vs. Velocity-Verlet

Your simulation can use either the Explicit Euler scheme or the
Velocity-Verlet scheme.  When you run the pendulum with Euler at a
moderate time-step (e.g. `dt = 0.01 s`), the total energy drifts upward
over time.  With Verlet at the same `dt`, the energy stays nearly constant.

1. Why does Explicit Euler cause energy drift?
2. Why does Velocity-Verlet conserve energy much better?
3. What would happen if you used a very small `dt` (e.g. `dt = 0.0001 s`)
   with Euler — would the drift disappear?  Explain.

*Hint: think about whether each method is **symplectic** (preserves phase-space
area) and whether the numerical trajectory obeys a conserved quantity.*

> 中文：(c) 顯式 Euler 與 Velocity-Verlet。你的模擬可使用顯式 Euler 或 Velocity-Verlet 方案。以 Euler 在中等時間步長（如 `dt = 0.01 s`）執行擺錘時，總能量會隨時間向上漂移；以相同 `dt` 用 Verlet 時，能量幾乎保持不變。
> 1. 為何顯式 Euler 會造成能量漂移？
> 2. 為何 Velocity-Verlet 能更好地守恆能量？
> 3. 若以非常小的 `dt`（如 `dt = 0.0001 s`）配合 Euler，漂移會消失嗎？解釋之。
> 提示：思考各方法是否為**辛（symplectic）**積分器（保持相空間面積），以及數值軌跡是否遵守守恆量。

### (d) Small-angle approximation

The small-angle formula for the period is `T = 2π √(L/g)`, which assumes
`sin(θ) ≈ θ`.

1. For what range of initial amplitudes is this approximation valid?
   (State a quantitative condition, e.g. "θ₀ < X rad" or "error < Y%".)
2. If you start the pendulum at `θ₀ = 0.5 rad` (≈ 29°), will the true
   period be longer or shorter than the small-angle prediction?  Why?
3. At what amplitude does the small-angle approximation overestimate or
   underestimate the period by more than 1%?

> 中文：(d) 小角度近似。週期的小角度公式為 `T = 2π √(L/g)`，其假設 `sin(θ) ≈ θ`。
> 1. 此近似在多大的初始振幅範圍內有效？（請給出定量條件，例如「θ₀ < X rad」或「誤差 < Y%」。）
> 2. 若以 `θ₀ = 0.5 rad`（約 29°）啟動擺錘，真實週期會比小角度預測長還是短？為何？
> 3. 在多大振幅下，小角度近似對週期的誤差會超過 1%？

---

## Model Answers (teacher only)

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. From `T = 2π √(L/g)`, solving for *g*:

       g = (4π² L) / T²
       g = (4π² × 1.0) / (2.01)²
       g ≈ 39.478 / 4.0401 ≈ 9.77 m/s²

2. Percent error vs 9.81:

       % error = |9.77 - 9.81| / 9.81 × 100 ≈ 0.41%

3. Significant figures: *T* = 2.01 has 3 sig figs, *L* = 1.0 has 2 sig figs.
   The result should be reported to 2 sig figs: *g* ≈ 9.8 m/s² (or 9.77 m/s²
   if keeping 3 sig figs from *T*).  The percent error is 0.4%.

> 中文：(a) 參考答案。由 `T = 2π √(L/g)` 解出 *g*：`g = (4π² L) / T²`，代入得 `g ≈ 9.77 m/s²`。百分誤差約 0.41%。有效數字：*T* = 2.01 有 3 位、*L* = 1.0 有 2 位，結果應取 2 位有效數字，即 *g* ≈ 9.8 m/s²，百分誤差為 0.4%。

### (b) Model answer

| Source | Effect on period | Explanation |
|--------|-----------------|-------------|
| Air resistance / drag | Increases *T* (slows the pendulum) | Drag opposes motion, reducing the effective restoring force and increasing the period. |
| Parallax error | Random / systematic | Misreading the angle from the side introduces random error in amplitude measurement; if consistently off, it biases the period measurement. |
| Small-angle approximation | Systematic — true period is slightly longer | The true period for a physical pendulum is longer than `2π√(L/g)` because `sin(θ) < θ` for θ > 0, reducing the restoring torque. |
| Human reaction time | Random error, typically ±0.1–0.2 s | Starting/stopping the stopwatch late adds random scatter.  Averaging over many periods reduces this. |
| Pixel-tracking noise | Random error in amplitude/position | Sub-pixel jitter in video tracking introduces noise in the measured angle, which propagates to period estimates. |

> 中文：(b) 參考答案。空氣阻力／阻力令 *T* 變長（阻力抵消運動，減弱有效回復力）；視差誤差屬隨機／系統性（側面讀角引入振幅量度誤差）；小角度近似屬系統性，真實週期略長（因 θ > 0 時 `sin(θ) < θ`，回復力矩較弱）；人為反應時間屬隨機誤差（典型 ±0.1–0.2 s，多次平均可減低）；像素追蹤雜訊屬隨機誤差（次像素抖動引入角度雜訊）。

### (c) Model answer

1. **Explicit Euler** updates position and velocity using the *current*
   acceleration only.  This is a first-order method that does not respect
   the geometric structure of Hamiltonian systems.  The numerical trajectory
   does not lie on the constant-energy surface; instead it systematically
   drifts to higher energy (the method is not symplectic — it expands
   phase-space area).

2. **Velocity-Verlet** is a symplectic integrator: it preserves phase-space
   area and approximately conserves a "shadow Hamiltonian" close to the true
   Hamiltonian.  As a result, the total energy oscillates around the true
   value but does not systematically drift, even over long integration times.

3. With a very small `dt`, Euler's energy drift per step is smaller, but it
   is still systematic — the energy will still drift upward, just more
   slowly.  The drift does **not** disappear; it scales as O(dt).  Verlet's
   energy error oscillates with amplitude O(dt²) but does not drift, so
   Verlet is always preferable for long simulations.

> 中文：(c) 參考答案。**顯式 Euler** 只以*當前*加速度更新位置與速度，是一階方法，不尊重哈密頓系統的幾何結構，數值軌跡不在等能量面上，會系統性地漂移到較高能量（非辛，會擴張相空間面積）。**Velocity-Verlet** 是辛積分器，保持相空間面積並近似守恆接近真實哈密頓量的「影子哈密頓量」，總能量圍繞真實值振盪而不系統性漂移。即使 `dt` 很小，Euler 的漂移仍屬系統性，不會消失，只是按 O(dt) 變慢；Verlet 的能量誤差以 O(dt²) 振盪但不漂移，故長模擬宜用 Verlet。

### (d) Model answer

1. The small-angle approximation `sin(θ) ≈ θ` is accurate to within ~1% for
   `θ₀ < 0.14 rad` (≈ 8°).  A common rule of thumb is `θ₀ < 0.1 rad` (≈ 6°)
   for < 0.5% error.

2. The true period is **longer** than the small-angle prediction.  For
   `θ₀ = 0.5 rad`, `sin(θ) < θ`, so the restoring torque is weaker than the
   linear approximation, making the pendulum swing more slowly.

3. The error exceeds 1% for `θ₀ > 0.14 rad` (≈ 8°).  The exact threshold
   depends on the required precision; the period can be expressed as a
   series: `T_true = T_small × (1 + θ₀²/16 + 11θ₀⁴/3072 + ...)`.  The
   first correction term `θ₀²/16` exceeds 0.01 when `θ₀ > 0.4 rad`, but
   the full numerical error (including higher terms) reaches 1% at about
   `θ₀ ≈ 0.14 rad`.

> 中文：(d) 參考答案。小角度近似 `sin(θ) ≈ θ` 在 `θ₀ < 0.14 rad`（約 8°）內誤差約 1% 以內；常用經驗法則為 `θ₀ < 0.1 rad`（約 6°）時誤差 < 0.5%。在 `θ₀ = 0.5 rad` 時，因 `sin(θ) < θ`，回復力矩較線性近似弱，真實週期**較長**。誤差在 `θ₀ > 0.14 rad`（約 8°）時超過 1%；週期級數為 `T_true = T_small × (1 + θ₀²/16 + 11θ₀⁴/3072 + ...)`，首個修正項 `θ₀²/16` 在 `θ₀ > 0.4 rad` 時超過 0.01，但含高階項的完整數值誤差約在 `θ₀ ≈ 0.14 rad` 達 1%。