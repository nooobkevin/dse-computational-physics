# Wave Exercise — Concept Questions

These questions test your understanding of the physics behind the wave
simulation you just implemented.  Answer them in a few sentences each.

> 中文：以下問題測試你對剛才實作的波動模擬背後物理概念的理解。每題以數句作答。

---

## Questions

### (a) Why does superposition produce a standing wave?

You implemented a traveling wave `y(x,t) = A sin(kx - ωt)`.  If you add
a second wave `y₂(x,t) = A sin(kx + ωt)` traveling in the opposite
direction, the sum is a standing wave.

1. Write down the mathematical expression for the sum `y₁ + y₂`.
2. Use the trigonometric identity `sin α + sin β = 2 sin((α+β)/2) cos((α-β)/2)`
   to simplify the sum.  What is the resulting expression?
3. At what positions *x* does the displacement remain zero for all time *t*?
   These are called **nodes**.  Express your answer in terms of the
   wavelength λ.
4. At what positions *x* does the displacement reach its maximum amplitude?
   These are called **anti-nodes**.

> 中文：(a) 為何疊加會產生駐波？你實作了行波 `y(x,t) = A sin(kx - ωt)`。若加上第二個沿相反方向行進的波 `y₂(x,t) = A sin(kx + ωt)`，其和即為駐波。
> 1. 寫出 `y₁ + y₂` 的數學表達式。
> 2. 利用三角恆等式 `sin α + sin β = 2 sin((α+β)/2) cos((α-β)/2)` 化簡此和。所得表達式為何？
> 3. 在哪些位置 *x* 上，位移在所有時間 *t* 均保持為零？這些位置稱為**節點**。請以波長 λ 表示答案。
> 4. 在哪些位置 *x* 上，位移達到最大振幅？這些位置稱為**腹點**。

### (b) Standing waves vs. traveling waves

1. In a traveling wave, does a point on the string ever have zero
   displacement for all time?  Explain.
2. In a standing wave, does energy propagate along the string?  Explain
   why or why not.
3. A standing wave on a string fixed at both ends can only have certain
   wavelengths.  If the string length is *L*, what are the allowed
   wavelengths?  (This is the origin of musical notes on a string
   instrument.)

> 中文：(b) 駐波對行波。
> 1. 在行波中，弦上某一點會在所有時間都保持零位移嗎？解釋之。
> 2. 在駐波中，能量會沿弦傳播嗎？解釋為何會或不會。
> 3. 兩端固定的弦上的駐波只能具有某些波長。若弦長為 *L*，容許的波長為何？（這是弦樂器樂音的來源。）

### (c) Intensity and amplitude

The energy of a wave is proportional to the square of its amplitude:
`I ∝ A²`.

1. If you double the amplitude of a wave, by what factor does the
   intensity increase?
2. If you triple the amplitude, by what factor does the intensity increase?
3. A sound wave with amplitude *A* has intensity *I*.  To produce a sound
   that is 4 times as intense, by what factor must the amplitude increase?
4. Explain in physical terms why energy depends on amplitude squared
   rather than amplitude.  (Hint: consider the kinetic energy of a point
   on the string: `½ m v²`, where *v* is the transverse velocity.)

> 中文：(c) 強度與振幅。波的能量與其振幅的平方成正比：`I ∝ A²`。
> 1. 若將波的振幅加倍，強度會增加多少倍？
> 2. 若將振幅增至三倍，強度會增加多少倍？
> 3. 振幅為 *A* 的聲波強度為 *I*。要產生強度為 4 倍的聲波，振幅須增加多少倍？
> 4. 用物理術語解釋為何能量取決於振幅的平方而非振幅。（提示：考慮弦上一點的動能 `½ m v²`，其中 *v* 為橫向速度。）

### (d) Inverse-square law

A point source emits waves uniformly in all directions.  The intensity
at a distance *r* from the source follows the inverse-square law:
`I ∝ 1/r²`.

1. If you double your distance from a sound source, by what factor does
   the intensity decrease?
2. If the intensity is *I₀* at a distance of 1 m, what is the intensity
   at a distance of 3 m?
3. Why does the intensity follow a `1/r²` law rather than `1/r`?  (Hint:
   consider the surface area of a sphere.)

> 中文：(d) 反平方定律。點源向所有方向均勻發射波。距源 *r* 處的強度遵循反平方定律：`I ∝ 1/r²`。
> 1. 若與聲源的距離加倍，強度會減少多少倍？
> 2. 若在距離 1 m 處強度為 *I₀*，在距離 3 m 處強度為何？
> 3. 為何強度遵循 `1/r²` 定律而非 `1/r`？（提示：考慮球體的表面面積。）

### (e) Interference and Young's double-slit

Young's double-slit experiment demonstrates the wave nature of light.
Bright fringes occur when the path difference from the two slits is an
integer number of wavelengths: `d sin θ = n λ`.

1. What condition must be satisfied for **destructive** interference
   (a dark fringe)?
2. If the slit separation *d* is increased, what happens to the fringe
   spacing on the screen?
3. If the wavelength λ is increased (e.g. red light instead of blue),
   what happens to the fringe spacing?
4. Why does the central fringe (n = 0) always appear bright regardless
   of the wavelength?

> 中文：(e) 干涉與楊氏雙縫。楊氏雙縫實驗證明光的波動性質。當兩縫的光程差為波長的整數倍時出現亮紋：`d sin θ = n λ`。
> 1. **相消**干涉（暗紋）須滿足甚麼條件？
> 2. 若縫距 *d* 增大，屏幕上的條紋間距會有何變化？
> 3. 若波長 λ 增大（例如紅光而非藍光），條紋間距會有何變化？
> 4. 為何中央條紋（n = 0）無論波長為何都總是亮紋？

### (f) Polarisation as evidence for transverse waves

1. Explain why only **transverse** waves can be polarised, while
   **longitudinal** waves cannot.
2. Describe a simple experiment using a polarising filter that
   demonstrates that light is a transverse wave.
3. Sound waves in air are longitudinal.  Can sound waves be polarised?
   Explain.

> 中文：(f) 偏振作為橫波的證據。
> 1. 解釋為何只有**橫波**能被偏振，而**縱波**不能。
> 2. 描述一個使用偏振濾光片的簡單實驗，證明光是橫波。
> 3. 空氣中的聲波是縱波。聲波能被偏振嗎？解釋之。

---

## Model Answers (teacher only)

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. `y₁ + y₂ = A sin(kx - ωt) + A sin(kx + ωt)`
2. Using `sin α + sin β = 2 sin((α+β)/2) cos((α-β)/2)`:
   `y = 2A sin(kx) cos(ωt)`
3. Nodes occur where `sin(kx) = 0`, i.e. `kx = nπ`, so `x = nπ/k = nλ/2`.
   Nodes are at `x = 0, λ/2, λ, 3λ/2, ...`
4. Anti-nodes occur where `|sin(kx)| = 1`, i.e. `kx = (n+½)π`, so
   `x = (n+½)λ/2 = λ/4, 3λ/4, 5λ/4, ...`

> 中文：(a) 參考答案。`y₁ + y₂ = A sin(kx - ωt) + A sin(kx + ωt)`。利用 `sin α + sin β = 2 sin((α+β)/2) cos((α-β)/2)` 得 `y = 2A sin(kx) cos(ωt)`。節點出現於 `sin(kx) = 0`，即 `kx = nπ`，故 `x = nπ/k = nλ/2`，節點位於 `x = 0, λ/2, λ, 3λ/2, ...`。腹點出現於 `|sin(kx)| = 1`，即 `kx = (n+½)π`，故 `x = (n+½)λ/2 = λ/4, 3λ/4, 5λ/4, ...`。

### (b) Model answer

1. No.  In a traveling wave, every point oscillates with the same
   amplitude *A*.  A point has zero displacement only at specific times
   (when the wave passes through equilibrium), not for all time.
2. No.  In a standing wave, energy is stored in the oscillations but
   does not propagate along the string.  The energy is confined between
   the nodes, oscillating between kinetic and potential forms.
3. For a string fixed at both ends of length *L*, the allowed wavelengths
   are `λₙ = 2L/n` where `n = 1, 2, 3, ...` (the harmonic series).
   The fundamental frequency is `f₁ = v/(2L)`.

> 中文：(b) 參考答案。不會。在行波中，每一點都以相同振幅 *A* 振盪，一點只在特定時刻（波經過平衡位置時）位移為零，而非所有時間。不會。在駐波中，能量儲存於振盪中但不沿弦傳播，能量被限制在節點之間，在動能與勢能形式之間振盪。對兩端固定、長度為 *L* 的弦，容許波長為 `λₙ = 2L/n`，其中 `n = 1, 2, 3, ...`（諧波系列），基頻為 `f₁ = v/(2L)`。

### (c) Model answer

1. Doubling amplitude → intensity increases by factor 4 (2² = 4).
2. Tripling amplitude → intensity increases by factor 9 (3² = 9).
3. To quadruple intensity, amplitude must increase by factor 2 (√4 = 2).
4. The transverse velocity of a point on the string is `v_y = ∂y/∂t`.
   For `y = A sin(kx - ωt)`, `v_y = -ωA cos(kx - ωt)`.  Kinetic energy
   is `½ m v_y² ∝ A²`.  Since both kinetic and potential energy scale
   with A², the total energy (intensity) scales as A².

> 中文：(c) 參考答案。振幅加倍 → 強度增加 4 倍（2² = 4）。振幅增至三倍 → 強度增加 9 倍（3² = 9）。要使強度增至 4 倍，振幅須增加 2 倍（√4 = 2）。弦上一點的橫向速度為 `v_y = ∂y/∂t`；對 `y = A sin(kx - ωt)`，`v_y = -ωA cos(kx - ωt)`，動能 `½ m v_y² ∝ A²`。由於動能與勢能均按 A² 標度，總能量（強度）按 A² 標度。

### (d) Model answer

1. Doubling distance → intensity decreases by factor 4 (1/2² = 1/4).
2. At 3 m: `I = I₀ / 3² = I₀ / 9`.
3. The inverse-square law comes from conservation of energy.  The total
   power emitted by the source spreads uniformly over a sphere of surface
   area `4πr²`.  Since power = intensity × area, `I = P / (4πr²) ∝ 1/r²`.
   If it were `1/r`, energy would not be conserved.

> 中文：(d) 參考答案。距離加倍 → 強度減少 4 倍（1/2² = 1/4）。在 3 m 處：`I = I₀ / 3² = I₀ / 9`。反平方定律源於能量守恆：源發出的總功率均勻分佈於表面面積 `4πr²` 的球面上，因功率 = 強度 × 面積，故 `I = P / (4πr²) ∝ 1/r²`；若為 `1/r`，能量便不守恆。

### (e) Model answer

1. Destructive interference (dark fringe): path difference = `(n + ½)λ`,
   i.e. `d sin θ = (n + ½)λ`.
2. Increasing slit separation *d* decreases fringe spacing (fringes get
   closer together).
3. Increasing wavelength λ increases fringe spacing (fringes spread out).
4. The central fringe (n = 0) has zero path difference from both slits,
   so waves arrive in phase for any wavelength, producing constructive
   interference.

> 中文：(e) 參考答案。相消干涉（暗紋）：光程差 = `(n + ½)λ`，即 `d sin θ = (n + ½)λ`。增大縫距 *d* 會減小條紋間距（條紋更密）。增大波長 λ 會增大條紋間距（條紋更疏）。中央條紋（n = 0）對兩縫的光程差為零，故任何波長下波均同相到達，產生相長干涉。

### (f) Model answer

1. Polarisation requires the wave oscillation to have a specific
   direction (orientation).  Transverse waves oscillate perpendicular
   to the direction of propagation, so they have a well-defined
   polarisation direction.  Longitudinal waves oscillate parallel to
   the direction of propagation — there is no "direction" to filter,
   so they cannot be polarised.
2. Pass light through a polarising filter — the transmitted intensity
   is reduced.  Pass it through a second polarising filter rotated by
   90° — no light gets through.  Rotating the second filter back to 0°
   restores transmission.  This shows light has a transverse orientation.
3. No, sound waves in air are longitudinal (compression/rarefaction).
   There is no transverse oscillation to filter, so sound cannot be
   polarised.

> 中文：(f) 參考答案。偏振要求波的振盪具有特定方向（取向）。橫波垂直於傳播方向振盪，故有明確的偏振方向；縱波平行於傳播方向振盪，沒有可過濾的「方向」，故不能偏振。讓光通過偏振濾光片，透射強度會減弱；再通過旋轉 90° 的第二片偏振濾光片，光完全不能通過；把第二片轉回 0° 則恢復透射，這顯示光具有橫向取向。不能，空氣中的聲波是縱波（壓縮／稀疏），沒有可過濾的橫向振盪，故聲波不能偏振。
