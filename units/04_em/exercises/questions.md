# Electricity & Magnetism Exercise — Concept Questions (M5)
# 電與磁練習 — 概念問題（中五）

These questions test your understanding of the physics behind the electric
field and circuit simulations you just implemented.  Answer them in a few
sentences each.

這些問題測試你對剛才所實作的電場與電路模擬背後物理的理解。請以數句簡短作答。

---

## Questions

### (a) Coulomb's inverse-square law 庫侖平方反比定律

You place a charge `q = +2 nC` at the origin.

1. Compute the electric field magnitude at `r = 0.5 m` and `r = 1.0 m`.
2. By what factor does the field decrease when you double the distance?
3. If you replace the charge with `q = -2 nC`, how does the field change?

你在原點放置一個電荷 `q = +2 nC`。

1. 計算在 `r = 0.5 m` 及 `r = 1.0 m` 處的電場大小。
2. 當距離加倍時，電場減小多少倍？
3. 若把電荷換成 `q = -2 nC`，電場會如何改變？

**中文版：庫侖反平方定律**

你在原點放置一個電荷 `q = +2 nC`。

1. 計算在 `r = 0.5 m` 及 `r = 1.0 m` 處的電場大小。
2. 當距離加倍時，電場會減少多少倍？
3. 若把電荷換成 `q = -2 nC`，電場會如何改變？

### (b) Electric field vs. electric potential 電場與電勢之比較

Consider a point charge `q = +1 nC`.

1. Compute the potential `V` at `r = 0.5 m` and `r = 1.0 m`.
2. How does the potential scale with distance compared to the field?
   (i.e., `V ∝ 1/r^n` vs `E ∝ 1/r^m` — what are *n* and *m*?)
3. Explain in one sentence why the potential falls off more slowly with
   distance than the field.

考慮一個點電荷 `q = +1 nC`。

1. 計算在 `r = 0.5 m` 及 `r = 1.0 m` 處的電勢 `V`。
2. 與電場相比，電勢隨距離如何變化？（即 `V ∝ 1/r^n` 對比 `E ∝ 1/r^m`，*n* 和 *m* 各是多少？）
3. 用一句話解釋為何電勢隨距離衰減得比電場慢。

**中文版：電場與電勢的比較**

考慮一個點電荷 `q = +1 nC`。

1. 計算在 `r = 0.5 m` 及 `r = 1.0 m` 處的電勢 `V`。
2. 與電場相比，電勢隨距離如何變化？（即 `V ∝ 1/r^n` 對比 `E ∝ 1/r^m`，*n* 和 *m* 各是多少？）
3. 用一句話解釋為何電勢隨距離衰減得比電場慢。

### (c) Why is the electric field perpendicular to equipotential surfaces? 為何電場垂直於等勢面？

1. From the definition `E = -∇V`, explain why field lines must be
   perpendicular to equipotential surfaces.
2. What would happen if the field had a component *along* an equipotential
   surface?

1. 由定義 `E = -∇V`，解釋為何電場線必須垂直於等勢面。
2. 若電場在等勢面上有*沿面*的分量，會發生甚麼事？

**中文版：為何電場垂直於等勢面？**

1. 由定義 `E = -∇V`，解釋為何電場線必須垂直於等勢面。
2. 若電場在等勢面上有*沿面*的分量，會發生甚麼事？

### (d) Kirchhoff's current law (KCL) 基爾霍夫電流定律（KCL）

In a circuit, three branches meet at a node:
- Branch 1: current `I₁ = 2 A` entering the node
- Branch 2: current `I₂ = 3 A` leaving the node
- Branch 3: unknown current `I₃`

1. Determine the magnitude and direction of `I₃`.
2. Explain KCL in terms of charge conservation.

在電路中，三條支路匯合於一個節點：
- 支路 1：電流 `I₁ = 2 A` 流入節點
- 支路 2：電流 `I₂ = 3 A` 流出節點
- 支路 3：未知電流 `I₃`

1. 求 `I₃` 的大小及方向。
2. 以電荷守恆解釋 KCL。

**中文版：基爾霍夫電流定律（KCL）**

在電路中，三條支路匯合於一個節點：
- 支路 1：電流 `I₁ = 2 A` 流入節點
- 支路 2：電流 `I₂ = 3 A` 流出節點
- 支路 3：未知電流 `I₃`

1. 求 `I₃` 的大小和方向。
2. 以電荷守恆解釋 KCL。

### (e) Kirchhoff's voltage law (KVL) 基爾霍夫電壓定律（KVL）

A series circuit has a 12 V battery and two resistors `R₁ = 4 Ω` and
`R₂ = 6 Ω`.

1. Compute the current in the circuit.
2. Compute the voltage drop across each resistor.
3. Verify KVL: `ΣV = 0` around the loop.

一個串聯電路有一個 12 V 電池及兩個電阻 `R₁ = 4 Ω` 和 `R₂ = 6 Ω`。

1. 計算電路中的電流。
2. 計算每個電阻兩端的電勢差（電壓降）。
3. 驗證 KVL：繞迴路一圈 `ΣV = 0`。

**中文版：基爾霍夫電壓定律（KVL）**

一個串聯電路有 12 V 電池及兩個電阻 `R₁ = 4 Ω` 和 `R₂ = 6 Ω`。

1. 計算電路中的電流。
2. 計算每個電阻兩端的電勢差（電壓降）。
3. 驗證 KVL：繞迴路一圈 `ΣV = 0`。

### (f) Internal resistance and terminal voltage 內阻與端電壓

A battery has an emf of `ε = 9.0 V` and an internal resistance of
`r = 0.5 Ω`.  It is connected to an external load `R = 4.5 Ω`.

1. Compute the current in the circuit.
2. Compute the terminal voltage (voltage across the battery terminals).
3. How much power is dissipated inside the battery?  How much in the
   external load?
4. What is the efficiency of the battery (power delivered to load /
   total power supplied)?

一個電池的電動勢為 `ε = 9.0 V`，內阻為 `r = 0.5 Ω`，連接一個外電阻 `R = 4.5 Ω`。

1. 計算電路中的電流。
2. 計算端電壓（電池兩端的電壓）。
3. 電池內部消耗多少功率？外電阻消耗多少？
4. 電池的效率是多少（輸送至負載的功率／總供應功率）？

**中文版：內阻與端電壓**

一個電池的電動勢為 `ε = 9.0 V`，內阻為 `r = 0.5 Ω`，連接一個外電阻 `R = 4.5 Ω`。

1. 計算電路中的電流。
2. 計算端電壓（電池兩端的電勢差）。
3. 電池內部消耗多少功率？外電阻消耗多少？
4. 電池的效率是多少（輸送至負載的功率／總供應功率）？

---

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. At `r = 0.5 m`:
       E = q / (4π ε₀ r²) = 2×10⁻⁹ / (4π × 8.85×10⁻¹² × 0.25) ≈ 71.9 N/C
   At `r = 1.0 m`:
       E ≈ 2×10⁻⁹ / (4π × 8.85×10⁻¹² × 1.0) ≈ 18.0 N/C

2. Doubling the distance reduces the field by a factor of 4 (inverse
   square law: E ∝ 1/r²).

3. The field magnitude is the same (71.9 N/C), but the direction reverses
   — it points toward the charge (radially inward) instead of away.

**中文提示：** 距離加倍，電場減為四分之一（反平方定律 E ∝ 1/r²）。電荷變號只改變電場方向（改為指向電荷），大小不變。

### (b) Model answer

1. At `r = 0.5 m`: V = 18.0 V; at `r = 1.0 m`: V = 9.0 V.
2. `V ∝ 1/r` (n = 1), while `E ∝ 1/r²` (m = 2).
3. Potential is the line integral of the field (`V = ∫ E·dr`), so the
   `1/r²` field integrates to a `1/r` potential, which falls off more
   slowly.

**中文提示：** V ∝ 1/r（n = 1），E ∝ 1/r²（m = 2）。電勢是電場的線積分，故 1/r² 的電場積分得 1/r 的電勢，衰減較慢。

### (c) Model answer

1. `E = -∇V` means the field points in the direction of the steepest
   *decrease* in potential.  Along an equipotential surface, `V` is
   constant, so `∇V` has no component parallel to the surface — the
   field must be perpendicular.
2. If the field had a component along the surface, moving along the
   surface would change the potential, contradicting the definition
   of an equipotential.

**中文提示：** E = -∇V 指向電勢下降最快的方向；等勢面上 V 不變，故 ∇V 無沿面分量，電場必垂直於等勢面。

### (d) Model answer

1. `I₃` must be `1 A` entering the node (KCL: `I_in = I_out`, so
   `2 + I₃ = 3`, giving `I₃ = 1 A` entering).
2. KCL expresses conservation of charge: charge cannot accumulate at
   a node (in steady state), so the total current entering must equal
   the total current leaving.

**中文提示：** KCL：流入 = 流出，2 + I₃ = 3，故 I₃ = 1 A 流入節點。KCL 體現電荷守恆。

### (e) Model answer

1. `I = ε / (R₁ + R₂) = 12 / 10 = 1.2 A`
2. `V₁ = I × R₁ = 1.2 × 4 = 4.8 V`, `V₂ = I × R₂ = 1.2 × 6 = 7.2 V`
3. KVL: `12 - 4.8 - 7.2 = 0.0 V` ✓

**中文提示：** I = 12/10 = 1.2 A；V₁ = 4.8 V，V₂ = 7.2 V；KVL 驗證 12 − 4.8 − 7.2 = 0 ✓。

### (f) Model answer

1. `I = ε / (R + r) = 9.0 / (4.5 + 0.5) = 9.0 / 5.0 = 1.8 A`
2. Terminal voltage: `V = ε - I r = 9.0 - 1.8 × 0.5 = 9.0 - 0.9 = 8.1 V`
3. Internal power: `P_int = I² r = (1.8)² × 0.5 = 1.62 W`
   Load power: `P_load = I² R = (1.8)² × 4.5 = 14.58 W`
4. Efficiency: `η = P_load / (P_load + P_int) = 14.58 / 16.20 = 90%`

**中文提示：** I = 1.8 A；端電壓 V = ε − Ir = 8.1 V；內阻功率 1.62 W，負載功率 14.58 W；效率 η = 14.58/16.20 = 90%。

---

### (d) Model answer (detailed)

KCL at a node: `2 A (in) = 3 A (out) + I₃`
If we define current entering as positive: `2 - 3 + I₃ = 0`, so `I₃ = 1 A`
entering the node.

**中文提示：** 節點處 KCL：2 − 3 + I₃ = 0，故 I₃ = 1 A 流入節點。

### (e) Model answer (detailed)

Equivalent resistance: `R_eq = R₁ + R₂ = 4 + 6 = 10 Ω`
Current: `I = V / R_eq = 12 / 10 = 1.2 A`
Voltage drops: `V_R₁ = 1.2 × 4 = 4.8 V`, `V_R₂ = 1.2 × 6 = 7.2 V`
KVL check: `+12 V (battery rise) - 4.8 V - 7.2 V = 0 V` ✓

**中文提示：** 等效電阻 R_eq = 10 Ω，電流 I = 1.2 A，電壓降 V_R₁ = 4.8 V、V_R₂ = 7.2 V，KVL 驗證 +12 − 4.8 − 7.2 = 0 ✓。

---

### (g) Lorentz force on a moving charge 運動電荷所受的洛倫茲力

A proton (`q = +1.6×10⁻¹⁹ C`, `m = 1.67×10⁻²⁷ kg`) moves with speed `v = 2.0×10⁶ m/s` at an angle of `30°` to a uniform magnetic field of strength `B = 0.5 T`.

1. Compute the magnitude of the magnetic force on the proton.
2. What is the force when the angle is `0°`? When it is `90°`?
3. Determine the radius of the circular path if the velocity is perpendicular to the field.
4. If the particle were an electron (same speed, opposite charge), how would the force magnitude and direction change?

一個質子（`q = +1.6×10⁻¹⁹ C`，`m = 1.67×10⁻²⁷ kg`）以速度 `v = 2.0×10⁶ m/s` 與磁場強度 `B = 0.5 T` 成 `30°` 角運動。

1. 計算質子所受磁力的大小。
2. 當角度為 `0°` 時力是多少？`90°` 時呢？
3. 若速度垂直於磁場，求圓形路徑的半徑。
4. 若粒子是電子（同速、電荷相反），力的大小及方向會如何改變？

**中文版：運動電荷所受的洛倫茲力**

一個質子（`q = +1.6×10⁻¹⁹ C`，`m = 1.67×10⁻²⁷ kg`）以速度 `v = 2.0×10⁶ m/s`、與均勻磁場 `B = 0.5 T` 成 `30°` 角運動。

1. 計算質子所受磁力的大小。
2. 當角度為 `0°` 時力是多少？`90°` 時呢？
3. 若速度垂直於磁場，求圓形路徑的半徑。
4. 若粒子是電子（速度相同、電荷相反），力的大小和方向會如何改變？

### (h) Right-hand rule 右手定則

A positively charged particle enters a uniform magnetic field pointing out of the page (⊙). The particle is moving to the right (+x direction).

1. Use the right-hand rule to determine the direction of the magnetic force.
2. Describe the resulting trajectory (shape, plane of motion).
3. How would the trajectory change if the particle were negatively charged?

一個帶正電的粒子進入一個指向頁面外的均勻磁場（⊙）。粒子向右（+x 方向）運動。

1. 用右手定則判斷磁力的方向。
2. 描述其運動軌跡（形狀、運動平面）。
3. 若粒子帶負電，軌跡會如何改變？

**中文版：右手定則**

一個帶正電的粒子進入一個指向頁面外（⊙）的均勻磁場，粒子向右（+x 方向）運動。

1. 用右手定則判斷磁力的方向。
2. 描述其運動軌跡（形狀、運動平面）。
3. 若粒子帶負電，軌跡會如何改變？

### (i) Circular motion in a magnetic field 磁場中的圓周運動

A particle of mass `m` and charge `q` moves in a uniform magnetic field `B` with velocity perpendicular to the field.

1. Derive the expression for the orbital radius `r = mv/(qB)` by equating the magnetic force to the centripetal force.
2. If the magnetic field strength is doubled, how does the radius change?
3. If the particle's speed is doubled (and the field is constant), how does the radius change?
4. Show that the orbital period `T = 2πm/(qB)` is independent of velocity.

一個質量為 `m`、電荷為 `q` 的粒子在均勻磁場 `B` 中運動，速度垂直於磁場。

1. 令磁力等於向心力，推導軌道半徑 `r = mv/(qB)` 的表示式。
2. 若磁場強度加倍，半徑會如何改變？
3. 若粒子速度加倍（磁場不變），半徑會如何改變？
4. 證明軌道週期 `T = 2πm/(qB)` 與速度無關。

**中文版：磁場中的圓周運動**

一個質量為 `m`、電荷為 `q` 的粒子在均勻磁場 `B` 中以垂直於磁場的速度運動。

1. 令磁力等於向心力，推導軌道半徑 `r = mv/(qB)` 的公式。
2. 若磁場強度加倍，半徑會如何改變？
3. 若粒子速度加倍（磁場不變），半徑會如何改變？
4. 證明軌道週期 `T = 2πm/(qB)` 與速度無關。

---