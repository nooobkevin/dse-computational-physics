# Physics & Society Exercise — Concept Questions (M5)

These questions test your understanding of the physics behind the
radioactive decay simulation you just implemented.  Answer them in a
few sentences each.

---

## Questions

### (a) Half-life and exponential decay

A radioactive isotope has a half-life of 2.0 years.

1. If you start with 1000 nuclei, how many remain after 2 years? After 4 years? After 6 years?
2. Explain why the number of nuclei never reaches zero in theory, even after a very long time.
3. What is the decay constant λ for this isotope?

**中文版：半衰期與指數衰變**

一種放射性同位素的半衰期為 2.0 年。

1. 若最初有 1000 個原子核，2 年後、4 年後、6 年後分別剩餘多少個？
2. 解釋為何理論上原子核數目即使經過很長時間也永遠不會變為零。
3. 此同位素的衰變常數 λ 是多少？

### (b) Why is radioactive decay exponential?

1. The probability that a single nucleus decays in a small time interval *dt* is `p = 1 - exp(-λ dt)`. Explain why this leads to an exponential decay law `N(t) = N₀ · 2^(-t/T)`.
2. What assumption about the independence of nuclei is built into the Monte Carlo simulation?
3. Why can't we predict exactly *which* nucleus will decay next, only the *probability*?

**中文版：為何放射性衰變是指數的？**

1. 在短時間間隔 *dt* 內，單一原子核衰變的機率為 `p = 1 - exp(-λ dt)`。解釋為何這會導致指數衰變律 `N(t) = N₀ · 2^(-t/T)`。
2. 蒙地卡羅模擬中內建了甚麼關於原子核獨立性的假設？
3. 為何以我們無法準確預測*哪個*原子核會先衰變，只能預測*機率*？

### (c) Monte Carlo vs. analytic methods

1. Your simulation uses the Monte Carlo method. How does the Monte Carlo result differ from the analytic formula `N(t) = N₀ · 2^(-t/T)`?
2. Why does the Monte Carlo estimate of the half-life become more accurate when you increase the initial number of nuclei N₀?
3. What is the main advantage of the Monte Carlo method for simulating radioactive decay?

**中文版：蒙地卡羅與解析方法的比較**

1. 你的模擬採用蒙地卡羅方法。蒙地卡羅結果與解析公式 `N(t) = N₀ · 2^(-t/T)` 有何不同？
2. 為何當你增加初始原子核數目 N₀ 時，蒙地卡羅估計的半衰期會更準確？
3. 蒙地卡羅方法模擬放射性衰變的主要優點是甚麼？

### (d) Alpha, beta, and gamma radiation

1. List the three types of nuclear radiation in order of **increasing penetrating power**.
2. List them in order of **increasing ionising power**.
3. What material is sufficient to stop alpha radiation? Beta radiation? Gamma radiation?
4. Explain the inverse relationship between ionising power and penetrating power.

**中文版：阿爾法、貝他與伽馬輻射**

1. 按**穿透力遞增**的順序列出三種核輻射。
2. 按**電離能力遞增**的順序列出它們。
3. 甚麼材料足以阻擋阿爾法輻射？貝他輻射？伽馬輻射？
4. 解釋電離能力與穿透力之間的相反關係。

### (e) Critical mass and chain reactions

1. What is meant by the "critical mass" of a fissile material?
2. Explain the meaning of the neutron multiplication factor *k*:
   - k < 1
   - k = 1
   - k > 1
3. How do control rods and moderators work in a nuclear reactor?

**中文版：臨界質量與鏈式反應**

1. 可裂變材料的「臨界質量」是甚麼意思？
2. 解釋中子倍增因子 *k* 的意義：
   - k < 1
   - k = 1
   - k > 1
3. 控制棒和慢化劑在核反應爐中如何運作？

### (f) Radiation safety and shielding

1. Why is alpha radiation relatively harmless outside the body but extremely dangerous if ingested or inhaled?
2. A worker in a nuclear facility receives a radiation dose of 0.5 mSv per year from background radiation and an additional 1.2 mSv from work. What is the total annual dose?
3. Explain the principle of shielding: why are different materials needed for different types of radiation?
4. What factors determine the risk from a radioactive source?

**中文版：輻射安全與屏蔽**

1. 為何阿爾法輻射在體外相對無害，但若吞入或吸入則極度危險？
2. 核設施的一名工人每年從背景輻射接受 0.5 mSv，另從工作接受 1.2 mSv。全年總劑量是多少？
3. 解釋屏蔽原理：為何不同類型的輻射需要不同材料？
4. 哪些因素決定放射源的風險？

### (g) Energy sources and mass-energy equivalence

1. Calculate the energy released (in MeV) when a mass defect of 0.2 amu occurs in a nuclear fission reaction.
2. A solar panel with an area of 1.5 m² receives solar radiation of 1000 W/m². If the panel efficiency is 18%, what is the electrical power output?
3. A wind turbine has a rotor radius of 10 m. The wind speed is 8 m/s, air density is 1.2 kg/m³, and the turbine efficiency is 0.35. Calculate the mechanical power output.
4. Explain why doubling the wind speed increases the wind turbine power by a factor of 8.

**中文版：能源與質能等價**

1. 計算當核裂變反應中質量虧損為 0.2 amu 時釋放的能量（以 MeV 為單位）。
2. 一塊面積 1.5 m² 的太陽能電池板接收 1000 W/m² 的太陽輻射。若電池板效率為 18%，電功率輸出是多少？
3. 一台風力渦輪機葉輪半徑為 10 m。風速為 8 m/s，空氣密度為 1.2 kg/m³，渦輪機效率為 0.35。計算機械功率輸出。
4. 解釋為何風速加倍會使風力渦輪機功率增大 8 倍。

### (h) Carbon neutrality and energy trade-offs (STSE)

1. Hong Kong aims to achieve carbon neutrality before 2050. List two advantages and two challenges of using nuclear power as a low-carbon energy source.
2. Compare solar power and wind power in terms of:
   - Land use requirements
   - Intermittency (dependence on weather)
   - Suitability for Hong Kong's geography
3. Explain how individual daily habits (e.g., reducing electricity consumption, choosing public transport) contribute to achieving carbon neutrality.
4. Discuss the environmental impact of extracting, converting, and distributing fossil fuels compared to renewable energy sources.

**中文版：碳中和與能源取捨（STSE）**

1. 香港目標在 2050 年前實現碳中和。列出使用核能作為低碳能源的兩項優點和兩項挑戰。
2. 從以下各方面比較太陽能與風能：
   - 土地需求
   - 間歇性（對天氣的依賴）
   - 對香港地理的適合程度
3. 解釋個人日常習慣（例如減少用電、選擇公共交通）如何有助實現碳中和。
4. 討論開採、轉換和輸送化石燃料與可再生能源在環境影響上的比較。

---

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. After 2 years (one half-life): N = 1000 / 2 = 500
   After 4 years (two half-lives): N = 1000 / 4 = 250
   After 6 years (three half-lives): N = 1000 / 8 = 125

2. Exponential decay approaches zero asymptotically but never reaches it
   because each factor of 1/2 never reduces the number to exactly zero.
   In practice, the number becomes so small that statistically zero
   nuclei remain.

3. λ = ln(2) / T = 0.693 / 2.0 = 0.347 yr⁻¹

**中文提示：** 每經過一個半衰期原子核減半：2 年→500、4 年→250、6 年→125。指數衰變漸近地趨向零但永不為零。λ = ln(2)/T = 0.347 yr⁻¹。

### (b) Model answer

1. The probability p = 1 - exp(-λ dt) means that in each time step, each
   nucleus has the same chance of decaying. Over many steps, this produces
   the exponential decay law N(t) = N₀ · exp(-λ t) = N₀ · 2^(-t/T).

2. The Monte Carlo method assumes each nucleus decays independently of
   all others — the decay of one nucleus does not affect the probability
   of another decaying.

3. Radioactive decay is a quantum-mechanical process — we can only know
   the probability of decay, not the exact time. This is fundamentally
   random, like rolling dice.

**中文提示：** p = 1 − exp(−λ dt) 表示每步每個原子核衰變機率相同，累積成指數衰變律。蒙地卡羅假設各原子核獨立衰變。放射性衰變是量子力學過程，只能知道機率，本質隨機。

### (c) Model answer

1. The Monte Carlo result fluctuates around the analytic curve due to
   random sampling. With enough nuclei, the fluctuations become small
   (law of large numbers).

2. Increasing N₀ reduces the relative size of statistical fluctuations.
   The standard deviation of N is √N, so the relative error is 1/√N.

3. The Monte Carlo method naturally models the random, probabilistic
   nature of decay. It can also handle more complex scenarios (e.g.,
   decay chains, varying conditions) that are difficult to solve
   analytically.

**中文提示：** 蒙地卡羅結果因隨機抽樣在解析曲線附近波動；N₀ 增大時波動變小（大數定律）；標準差為 √N，相對誤差為 1/√N。蒙地卡羅能處理解析方法難以解決的複雜情境。

### (d) Model answer

1. Penetrating power (increasing): alpha < beta < gamma
2. Ionising power (increasing): gamma < beta < alpha
3. Alpha: stopped by paper or a few cm of air
   Beta: stopped by a few mm of aluminium
   Gamma: requires thick lead or concrete (several cm)

4. The inverse relationship exists because larger, slower particles
   (alpha) interact more strongly with matter, depositing energy quickly
   (high ionising power) but being stopped easily (low penetrating power).
   Smaller, faster particles or waves (gamma) interact weakly, penetrating
   deeply but ionising less.

**中文提示：** 穿透力：alpha < beta < gamma；電離能力：gamma < beta < alpha。Alpha 被紙或數厘米空氣阻擋，Beta 被數毫米鋁阻擋，Gamma 需厚鉛或混凝土。較大較慢的粒子（alpha）與物質作用強，電離力高但易被阻擋。

### (e) Model answer

1. Critical mass is the minimum mass of fissile material needed to sustain
   a self-sustaining chain reaction (k ≥ 1).

2. k < 1: subcritical — the chain reaction dies out (not enough neutrons)
   k = 1: critical — self-sustaining (each fission produces exactly one
         neutron that causes another fission)
   k > 1: supercritical — runaway chain reaction (nuclear explosion)

3. Control rods absorb excess neutrons to keep k = 1 during normal
   operation. Moderators (e.g., graphite, water) slow down fast neutrons
   to thermal energies, increasing the probability of fission.

**中文提示：** 臨界質量是維持自持鏈式反應（k ≥ 1）所需的最小可裂變材料質量。k < 1 次臨界（鏈式反應熄滅）；k = 1 臨界（自持）；k > 1 超臨界（失控核爆）。控制棒吸收過剩中子，慢化劑（石墨、水）把快中子減速至熱能，增加裂變機率。

### (f) Model answer

1. Alpha radiation is stopped by the dead layer of skin, so it poses
   little risk externally. But if inhaled or ingested, alpha emitters
   are in direct contact with living tissue, and their high ionising
   power causes severe damage.

2. Total dose = 0.5 + 1.2 = 1.7 mSv per year

3. Different radiation types interact differently with matter:
   - Alpha: large, charged, slow → stopped by light materials
   - Beta: smaller, faster → requires denser material
   - Gamma: uncharged, highly penetrating → requires dense, thick material

4. Risk depends on: radiation type (α, β, γ), energy, half-life (longer
   = more exposure time), chemical form (affects biological uptake),
   and whether the source is external or internal.

**中文提示：** Alpha 被皮膚死層阻擋，體外風險低；但吸入或吞入後與活組織直接接觸，高電離力造成嚴重損害。總劑量 = 0.5 + 1.2 = 1.7 mSv。不同輻射與物質作用不同，故需不同屏蔽材料。風險取決於輻射類型、能量、半衰期、化學形態及內外照射。