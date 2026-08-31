# Gas Simulation Exercise — Concept Questions (M5)

These questions test your understanding of the physics behind the gas
simulation you just implemented.  Answer them in a few sentences each.

> 中文：以下問題測試你對剛才實作的氣體模擬背後物理概念的理解。每題以數句作答。

---

## Questions

### (a) Maxwell-Boltzmann distribution

The speed distribution of particles in your simulation should approximate
the Maxwell-Boltzmann distribution.

1. Why do the particle speeds follow the Maxwell-Boltzmann distribution
   rather than all having the same speed?
2. What happens to the distribution when you increase the temperature?
   Sketch the shape change (broader/narrower, peak shift).
3. In 2D, the most probable speed is `v_p = √(k_B T / m)`.  Why is the
   most probable speed *not* the same as the average speed or the RMS
   speed?

> 中文：(a) 麥克斯韋-玻爾茲曼分佈。模擬中粒子的速率分佈應近似麥克斯韋-玻爾茲曼分佈。
> 1. 為何粒子速率遵循麥克斯韋-玻爾茲曼分佈，而非全部具有相同速率？
> 2. 當溫度升高時，分佈會有何變化？（描述形狀變化：變寬／變窄、峰值移動。）
> 3. 在 2D 中，最概然速率為 `v_p = √(k_B T / m)`。為何最概然速率*不等於*平均速率或 RMS 速率？

### (b) Equipartition of energy

The equipartition theorem states that each quadratic degree of freedom
contributes `½ k_B T` to the average energy per particle.

1. How many degrees of freedom does a single particle have in a 2D
   simulation?  In 3D?
2. Using equipartition, derive the relationship between the average
   kinetic energy per particle and the temperature.
3. Your simulation uses `kB = 1.0` (simulation units).  If you measure
   an average KE per particle of 2.5, what is the estimated temperature
   in a 2D simulation?

> 中文：(b) 能量均分。能量均分定理指出每個二次自由度對每粒子的平均能量貢獻 `½ k_B T`。
> 1. 在 2D 模擬中，單一粒子有多少個自由度？在 3D 呢？
> 2. 利用能量均分，推導每粒子平均動能與溫度的關係。
> 3. 你的模擬使用 `kB = 1.0`（模擬單位）。若量得每粒子平均動能為 2.5，在 2D 模擬中估算溫度為何？

### (c) Pressure from collisions

Pressure in an ideal gas arises from particles colliding with the walls
of the container.

1. Explain in words how a single particle hitting a wall transfers
   momentum.  How much momentum is transferred per collision?
2. If you double the number of particles *N* (keeping the box size and
   temperature constant), what happens to the pressure?  Why?
3. If you double the box side length *L* (keeping *N* and *T* constant),
   what happens to the pressure?  Why?

> 中文：(c) 碰撞產生的壓力。理想氣體的壓力源於粒子與容器壁碰撞。
> 1. 用文字解釋單一粒子撞擊牆壁時如何傳遞動量。每次碰撞傳遞多少動量？
> 2. 若將粒子數 *N* 加倍（保持容器大小與溫度不變），壓力會有何變化？為何？
> 3. 若將容器邊長 *L* 加倍（保持 *N* 與 *T* 不變），壓力會有何變化？為何？

### (d) Sources of error

Your simulation is a simplified model of a real gas.  List **at least
three** ways in which the simulation differs from a real gas, and explain
how each difference affects the results.

Consider:
- Discrete time steps (dt > 0)
- 2D vs 3D
- Point particles vs finite-size atoms
- No inter-particle forces (except collisions)
- The particle-particle collision detection (O(N²) pairwise check)

> 中文：(d) 誤差來源。你的模擬是真實氣體的簡化模型。列出**至少三項**模擬與真實氣體的差異，並解釋每項差異如何影響結果。
> 可考慮：離散時間步（dt > 0）、2D 對 3D、點粒子對有限大小原子、無粒子間作用力（碰撞除外）、粒子間碰撞偵測（O(N²) 兩兩檢查）。

### (e) Verlet vs Euler energy conservation

Your simulation uses the Velocity-Verlet integration scheme.

1. For a single free particle (no collisions), why does Verlet conserve
   kinetic energy exactly?
2. What would happen if you used Explicit Euler instead?  Would the
   kinetic energy still be conserved?
3. When a particle bounces off a wall, is the collision handled by the
   integrator or by the collision hook?  Does the energy remain exactly
   conserved after a wall bounce?

> 中文：(e) Verlet 與 Euler 的能量守恆。你的模擬使用 Velocity-Verlet 積分方案。
> 1. 對單一自由粒子（無碰撞），為何 Verlet 能精確守恆動能？
> 2. 若改用顯式 Euler，會發生甚麼？動能仍會守恆嗎？
> 3. 當粒子從牆壁反彈時，碰撞是由積分器還是碰撞鉤子處理？牆壁反彈後能量仍精確守恆嗎？

### (f) 2D vs 3D

The Maxwell-Boltzmann distribution has a different functional form in
2D vs 3D.

1. Write down the 2D and 3D Maxwell-Boltzmann speed distributions.
2. How does the number of degrees of freedom affect the relationship
   between temperature and average kinetic energy?
3. If you ran your simulation in 3D instead of 2D, would the pressure
   be higher or lower for the same *N*, *T*, and *L*?  Explain using
   the ideal gas law.

> 中文：(f) 2D 對 3D。麥克斯韋-玻爾茲曼分佈在 2D 與 3D 中具有不同的函數形式。
> 1. 寫出 2D 與 3D 的麥克斯韋-玻爾茲曼速率分佈。
> 2. 自由度的數目如何影響溫度與平均動能的關係？
> 3. 若在 3D 而非 2D 執行模擬，在相同 *N*、*T*、*L* 下壓力會較高還是較低？利用理想氣體定律解釋。

---

## Additional Questions (CAF-aligned)

### (g) Average kinetic energy and the Kelvin scale

The CAF curriculum states that the average kinetic energy of gas molecules
is given by:

    KE_avg = 3RT / (2N_A)

where *R* is the universal gas constant (8.314 J/(mol·K)) and *N_A* is
Avogadro's number (6.022 × 10²³ mol⁻¹).

1. Show that KE_avg = 3RT/(2N_A) is equivalent to (3/2)kT, where
   k = R/N_A is the Boltzmann constant.
2. Why must the temperature *T* in this formula be expressed in Kelvin
   rather than Celsius?  What would happen if you used Celsius?
3. At T = 0 K (absolute zero), what is the average kinetic energy of
   an ideal gas?  Is this physically possible for a real gas?
4. Calculate KE_avg for a gas molecule at room temperature (T = 293 K).
   Express your answer in joules and in electronvolts (1 eV = 1.602 × 10⁻¹⁹ J).

> 中文：(g) 平均動能與開爾文溫標。CAF 課程指出氣體分子的平均動能為 `KE_avg = 3RT / (2N_A)`，其中 *R* 為通用氣體常數（8.314 J/(mol·K)），*N_A* 為亞佛加厥常數（6.022 × 10²³ mol⁻¹）。
> 1. 證明 KE_avg = 3RT/(2N_A) 等價於 (3/2)kT，其中 k = R/N_A 為玻爾茲曼常數。
> 2. 為何此公式中的溫度 *T* 必須以開爾文而非攝氏表示？若用攝氏會發生甚麼？
> 3. 在 T = 0 K（絕對零度）時，理想氣體的平均動能為何？對真實氣體而言這在物理上可能嗎？
> 4. 計算室溫（T = 293 K）下氣體分子的 KE_avg，分別以焦耳及電子伏特表示（1 eV = 1.602 × 10⁻¹⁹ J）。

### (h) Why Kelvin?

The three empirical gas laws (Boyle's, Charles', pressure law) can be
combined into the general gas law pV/T = constant.

1. If you measured temperature in Celsius instead of Kelvin, would
   pV/T still be constant?  Explain why or why not.
2. Charles' law states that V ∝ T at constant pressure.  If you plot
   V vs T (in Celsius), what does the intercept on the temperature
   axis represent?
3. Explain why the Kelvin scale is called an *absolute* temperature
   scale, and why it is essential for the kinetic theory of gases.

> 中文：(h) 為何用開爾文？三條經驗氣體定律（波義耳、查理、壓力定律）可合併為一般氣體定律 pV/T = 常數。
> 1. 若以攝氏而非開爾文量度溫度，pV/T 仍會是常數嗎？解釋為何會或不會。
> 2. 查理定律指出定壓下 V ∝ T。若繪畫 V 對 T（以攝氏計）的圖，溫度軸上的截距代表甚麼？
> 3. 解釋為何開爾文溫標稱為*絕對*溫標，以及為何它對氣體分子動力論至關重要。

### (i) Zeroth law of thermodynamics

The zeroth law of thermodynamics is a fundamental concept that underpins
the measurement of temperature.

1. State the zeroth law of thermodynamics in your own words.
2. Explain how the zeroth law justifies the use of a thermometer to
   measure temperature.  What assumption does a thermometer make about
   thermal equilibrium?
3. If object A is in thermal equilibrium with object B, and object B is
   in thermal equilibrium with object C, what can you conclude about
   objects A and C?
4. How does the zeroth law relate to the concept of temperature as a
   quantity associated with the average kinetic energy of random
   molecular motion?

> 中文：(i) 熱力學第零定律。熱力學第零定律是支撐溫度量度的基本概念。
> 1. 用自己的文字陳述熱力學第零定律。
> 2. 解釋第零定律如何支持使用溫度計量度溫度。溫度計對熱平衡作了甚麼假設？
> 3. 若物體 A 與物體 B 處於熱平衡，而物體 B 與物體 C 處於熱平衡，你能對 A 與 C 得出甚麼結論？
> 4. 第零定律與「溫度是與分子隨機運動平均動能相關的量」這個概念有何關係？

---

## Model Answers (teacher only)

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. Particles move randomly and exchange energy through collisions.  Over
   time, the system reaches thermal equilibrium, where the speeds follow
   the Maxwell-Boltzmann distribution — the most probable distribution
   that maximises entropy for a given total energy.  Not all particles
   have the same speed because energy is distributed probabilistically
   among the particles.

2. When temperature increases, the distribution broadens (wider spread
   of speeds) and the peak shifts to a higher speed.  The area under
   the curve remains 1 (normalised).  The distribution becomes flatter
   and extends to higher speeds.

3. The most probable speed is the speed at which *f(v)* is maximum.
   The average speed is higher because the distribution is skewed to
   the right (there is a long tail of high-speed particles).  The RMS
   speed is higher still because it weights high speeds more heavily
   (the square in the average).  For 2D: v_p < ⟨v⟩ < v_rms.

> 中文：(a) 參考答案。粒子隨機運動並透過碰撞交換能量，系統最終達熱平衡，速率遵循麥克斯韋-玻爾茲曼分佈（在給定總能量下使熵最大的最概然分佈）；能量在粒子間按機率分配，故並非所有粒子速率相同。溫度升高時，分佈變寬（速率範圍更廣）且峰值移向較高速率，曲線下面積保持 1（已歸一化），分佈變得更平坦並延伸至較高速率。最概然速率是 *f(v)* 最大處的速率；因分佈右偏（有高速粒子的長尾），平均速率較高；RMS 速率因對高速加權更重（平均中的平方）而更高。2D 下：v_p < ⟨v⟩ < v_rms。

### (b) Model answer

1. In 2D: 2 degrees of freedom (v_x, v_y).  In 3D: 3 degrees of freedom
   (v_x, v_y, v_z).

2. Each degree of freedom contributes ½ k_B T to the average energy.
   For *d* dimensions: ⟨KE⟩ = (d/2) N k_B T.  Per particle:
   ⟨KE_per⟩ = (d/2) k_B T.  So T = (2/d) ⟨KE_per⟩ / k_B.

3. For 2D (d=2): T = (2/2) * 2.5 / 1.0 = 2.5.

> 中文：(b) 參考答案。2D 有 2 個自由度（v_x、v_y），3D 有 3 個自由度（v_x、v_y、v_z）。每個自由度對平均能量貢獻 ½ k_B T；對 *d* 維：⟨KE⟩ = (d/2) N k_B T，每粒子 ⟨KE_per⟩ = (d/2) k_B T，故 T = (2/d) ⟨KE_per⟩ / k_B。2D（d=2）下：T = (2/2) × 2.5 / 1.0 = 2.5。

### (c) Model answer

1. When a particle hits a wall, its velocity component normal to the
   wall reverses direction.  The momentum change is Δp = 2m|v_perp|.
   This momentum is transferred to the wall.

2. Pressure doubles.  P = N k_B T / V, so doubling N doubles P at
   constant T and V.  More particles mean more wall collisions per
   second.

3. Pressure decreases by a factor of 4 (in 2D).  P = N k_B T / L²,
   so doubling L quadruples the area, reducing P to 1/4.  Particles
   travel farther between wall collisions.

> 中文：(c) 參考答案。粒子撞牆時，垂直於牆壁的速度分量反向，動量變化為 Δp = 2m|v_perp|，此動量傳遞給牆壁。壓力加倍：P = N k_B T / V，N 加倍則定 T、V 下 P 加倍，因每秒牆壁碰撞次數增加。壓力減為 1/4（2D）：P = N k_B T / L²，L 加倍令面積變為 4 倍，P 減為 1/4，粒子在兩次牆壁碰撞間走得更遠。

### (d) Model answer

| Source of error | Effect |
|----------------|--------|
| **Discrete time steps** | Wall collisions are detected after the particle has already crossed the wall, introducing a small position error.  Smaller dt reduces this. |
| **2D vs 3D** | Real gases are 3D.  The 2D simulation has different collision rates and pressure scaling.  The qualitative behaviour (MB distribution, equipartition) is the same. |
| **Point particles** | Real atoms have finite size (van der Waals radius).  Our simulation uses a small but non-zero radius for collision detection, which introduces excluded-volume effects. |
| **No inter-particle forces** | Real gases have attractive van der Waals forces.  Our simulation only has hard-sphere collisions, so it models an ideal gas, not a real gas with phase changes. |
| **O(N²) collision detection** | The pairwise check is computationally expensive for large N.  Real MD simulations use neighbour lists or cell indexing.  For N < 1000, O(N²) is acceptable. |

> 中文：(d) 參考答案。**離散時間步**：牆壁碰撞在粒子已越過牆壁後才被偵測，引入少量位置誤差，較小 dt 可減低。**2D 對 3D**：真實氣體為 3D，2D 模擬的碰撞率與壓力標度不同，但定性行為（MB 分佈、能量均分）相同。**點粒子**：真實原子有有限大小（范德華半徑），模擬以細小但非零的半徑作碰撞偵測，引入排除體積效應。**無粒子間作用力**：真實氣體有范德華吸引力，模擬只有硬球碰撞，故模擬的是理想氣體而非有相變的真實氣體。**O(N²) 碰撞偵測**：兩兩檢查在大 N 時計算昂貴，真實 MD 模擬使用鄰居表或格點索引；N < 1000 時 O(N²) 可接受。

### (e) Model answer

1. For a free particle (a=0), both Euler and Verlet reduce to the same
   update: x(t+dt) = x(t) + dt*v(t).  The velocity never changes, so
   KE is exactly conserved regardless of the scheme.

2. For a free particle, Euler also conserves KE exactly (same update).
   The difference between Euler and Verlet only appears when forces are
   present (a ≠ 0).  For the gas simulation with only hard-wall
   collisions, both schemes give identical results.

3. The wall collision is handled by the collision hook, not the
   integrator.  The collision is instantaneous and elastic, so energy
   is exactly conserved (the speed magnitude doesn't change, only the
   direction).  The integrator's role is just to move particles between
   collisions.

> 中文：(e) 參考答案。對自由粒子（a=0），Euler 與 Verlet 均化為相同更新：x(t+dt) = x(t) + dt·v(t)，速度永不改變，故無論何種方案動能均精確守恆。對自由粒子，Euler 亦精確守恆動能（更新相同）；Euler 與 Verlet 的差異只在有力（a ≠ 0）時出現，對只有硬牆碰撞的氣體模擬，兩者結果相同。牆壁碰撞由碰撞鉤子而非積分器處理；碰撞即時且彈性，故能量精確守恆（速率大小不變，僅方向改變），積分器只負責在碰撞之間移動粒子。

### (f) Model answer

1. 2D: f(v) = (m/k_B T) v exp(-mv²/2k_B T)
   3D: f(v) = 4π (m/2πk_B T)^(3/2) v² exp(-mv²/2k_B T)

2. In 2D (d=2): ⟨KE⟩ = N k_B T.  In 3D (d=3): ⟨KE⟩ = (3/2) N k_B T.
   More dimensions mean more ways to store energy, so the same
   temperature corresponds to higher total KE.

3. For the same N, T, and L: P_2D = N k_B T / L², P_3D = N k_B T / L³.
   In 3D, the volume is L³ instead of L², so the pressure is lower
   (divided by an extra factor of L).  For L > 1, P_3D < P_2D.

> 中文：(f) 參考答案。2D：f(v) = (m/k_B T) v exp(-mv²/2k_B T)；3D：f(v) = 4π (m/2πk_B T)^(3/2) v² exp(-mv²/2k_B T)。2D（d=2）下 ⟨KE⟩ = N k_B T，3D（d=3）下 ⟨KE⟩ = (3/2) N k_B T；維度愈多代表儲存能量的方式愈多，故相同溫度對應較高的總動能。相同 N、T、L 下：P_2D = N k_B T / L²、P_3D = N k_B T / L³；3D 的體積為 L³ 而非 L²，壓力較低（多除以一個 L 因子），L > 1 時 P_3D < P_2D。