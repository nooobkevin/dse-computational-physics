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

### (b) Why is radioactive decay exponential?

1. The probability that a single nucleus decays in a small time interval *dt* is `p = 1 - exp(-λ dt)`. Explain why this leads to an exponential decay law `N(t) = N₀ · 2^(-t/T)`.
2. What assumption about the independence of nuclei is built into the Monte Carlo simulation?
3. Why can't we predict exactly *which* nucleus will decay next, only the *probability*?

### (c) Monte Carlo vs. analytic methods

1. Your simulation uses the Monte Carlo method. How does the Monte Carlo result differ from the analytic formula `N(t) = N₀ · 2^(-t/T)`?
2. Why does the Monte Carlo estimate of the half-life become more accurate when you increase the initial number of nuclei N₀?
3. What is the main advantage of the Monte Carlo method for simulating radioactive decay?

### (d) Alpha, beta, and gamma radiation

1. List the three types of nuclear radiation in order of **increasing penetrating power**.
2. List them in order of **increasing ionising power**.
3. What material is sufficient to stop alpha radiation? Beta radiation? Gamma radiation?
4. Explain the inverse relationship between ionising power and penetrating power.

### (e) Critical mass and chain reactions

1. What is meant by the "critical mass" of a fissile material?
2. Explain the meaning of the neutron multiplication factor *k*:
   - k < 1
   - k = 1
   - k > 1
3. How do control rods and moderators work in a nuclear reactor?

### (f) Radiation safety and shielding

1. Why is alpha radiation relatively harmless outside the body but extremely dangerous if ingested or inhaled?
2. A worker in a nuclear facility receives a radiation dose of 0.5 mSv per year from background radiation and an additional 1.2 mSv from work. What is the total annual dose?
3. Explain the principle of shielding: why are different materials needed for different types of radiation?
4. What factors determine the risk from a radioactive source?

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