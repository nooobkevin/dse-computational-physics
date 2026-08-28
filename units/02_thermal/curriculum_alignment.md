# Unit 02 Thermal Physics — Curriculum Alignment (CAF Consultation Draft)

## 1. Curriculum spec

### Topic 2. Thermal Physics — content items (CAF lines 1382–1518)

**a. Heat transfer**
- Heat and internal energy
- Heat capacity and specific heat capacity
- Outcomes: realise temperature as degree of hotness; interpret temperature as quantity associated with average KE of random molecular motion; define heat as energy transferred due to temperature difference; describe thermal equilibrium via zeroth law; describe effect of mass, temperature, state on internal energy; relate internal energy to sum of KE (random motion) + PE (molecular); define C = Q/ΔT and c = Q/(mΔT); determine specific heat capacity; realise practical importance of high specific heat capacity of water; solve problems involving C and c.

**b. Change of state**
- Latent heat and specific latent heat
- Evaporation
- Outcomes: realise change of state at melting/boiling point; realise latent heat as energy transfer during change of state without temperature change; interpret latent heat in terms of change of molecular PE; define l_f = Q/m and l_v = Q/m; solve related problems; explain evaporation below boiling point, cooling effect, factors affecting rate of evaporation in terms of molecular motion.

**c. Gases**
- General gas law
- Kinetic theory
- Outcomes: state Boyle's law (p-V), pressure law (p-T), Charles' law (V-T); determine absolute zero by extrapolation of p-T or V-T; use Kelvin scale; combine three relationships to obtain pV/T = constant; solve problems using pV = nRT; realise random motion of molecules; realise gas pressure from molecular bombardment on container wall; relate macroscopic T with microscopic average KE by KE_avg = 3RT/(2N_A); interpret temperature change from Maxwell-Boltzmann distribution; solve problems involving kinetic theory.

### Suggested learning and teaching activities (lines 1529–1539)
- Calibrate a thermometer and reproduce fixed points on Celsius scale
- Use mixture method to estimate specific heat capacity
- Perform experiments to study cooling curve of a melted substance and determine its melting point
- Determine factors affecting the rate of evaporation
- Examine p-T and V-T relationships of a gas and determine absolute zero experimentally
- Observe random motion of molecules inside a smoke cell using microscope and video camera
- Use mechanical gas model to simulate gas molecule movements and explain gas laws

### Suggested Computational Physics activities (lines 1543–1546)
- Simulate random walk of molecules
- Simulate motions of gas molecules inside a container and illustrate Maxwell-Boltzmann distribution

### Key practical tasks (lines 1522–1525)
- Determine specific heat capacity of a substance (e.g. water, metal block)
- Determine specific latent heat of fusion and vaporisation of water
- Examine Boyle's law of a gas

### Annex 3 — changes affecting Thermal Physics (lines 4270–4282, 4354–4356)

**REMOVED from "Heat and Gases":**
- Thermometers
- Transfer processes
- Microscopic and macroscopic relationship for ideal gases: PV = (1/3)Nm⟨c²⟩
- Real gases

**ADJUSTED:**
- Maxwell-Boltzmann distribution outcomes (line 4356) — learning outcomes adjusted for clarity

---

## 2. Coverage matrix

| Curriculum item | Status | Current artifact | Gap |
|---|---|---|---|
| **a. Heat transfer** — heat, internal energy, heat capacity, specific heat capacity | **MISSING** | No artifact covers heat transfer, calorimetry, or specific heat capacity | Entire sub-topic absent from unit. No Manim scene, teacher app mode, or exercise addresses heat transfer, C, c, or internal energy as KE+PE. |
| **a. Heat transfer** — zeroth law, thermal equilibrium | **MISSING** | Not mentioned in any artifact | No coverage of zeroth law or thermal equilibrium concept. |
| **a. Heat transfer** — temperature as average KE of random molecular motion | **PARTIAL** | Teacher app shows T_est from KE via equipartition (gas_sim.py:394–413); questions.md (b) covers equipartition | Covered only in the context of ideal gas kinetic theory, not as a general concept for all matter. |
| **b. Change of state** — latent heat, specific latent heat, evaporation | **MISSING** | No artifact covers phase change, latent heat, or evaporation | Entire sub-topic absent. No melting/boiling, latent heat, or evaporation content. |
| **c. Gases** — Boyle's law, pressure law, Charles' law | **MISSING** | No artifact teaches the three gas laws individually or the pV/T = constant relationship | The unit teaches pV = NkT (ideal gas law) but not the empirical gas laws or absolute-zero determination. |
| **c. Gases** — absolute zero determination by extrapolation | **MISSING** | Not addressed | No p-T or V-T extrapolation exercise. |
| **c. Gases** — Kelvin scale | **MISSING** | Simulation uses arbitrary units (kB=1.0); no Kelvin concept taught | No Kelvin/Celsius conversion or absolute temperature discussion. |
| **c. Gases** — pV = nRT / pV = NkT | **COVERED** | gas_sim.py:415–429 (ideal_gas_pressure); teacher app shows P_meas vs P_ideal; PressureStatistical scene shows convergence | Covered in simulation units. Real-world nRT form not explicitly shown. |
| **c. Gases** — random motion of molecules | **COVERED** | Teacher app gas mode shows particle trajectories with velocity arrows; MaxwellBoltzmann scene shows speed distribution | Well covered by MD simulation visualisation. |
| **c. Gases** — gas pressure from molecular bombardment | **COVERED** | gas_sim.py:338–359 (pressure from momentum transfer); PressureStatistical scene; teacher app live P_meas | Well covered. |
| **c. Gases** — KE_avg = 3RT/(2N_A) relating T to microscopic KE | **PARTIAL** | gas_sim.py:394–413 (temperature_from_ke) uses equipartition: T = (2/dim)·⟨KE_per⟩/kB | Uses simulation units (kB=1.0) and general equipartition, not the specific formula KE_avg = 3RT/(2N_A). 3D formula not explicitly shown. |
| **c. Gases** — Maxwell-Boltzmann distribution (interpret temperature change) | **COVERED** | MaxwellBoltzmann scene; equations.py:17–60; teacher app MB overlay; questions.md (a) | Well covered. Both 2D and 3D formulas in equations.py. |
| **c. Gases** — solve problems involving kinetic theory | **PARTIAL** | Student exercise implements collision hooks; questions.md has conceptual questions | No quantitative problem-solving exercises (e.g. calculate pressure from given N, T, V). |
| **Key practical: determine specific heat capacity** | **MISSING** | Not addressed | No calorimetry lab or simulation. |
| **Key practical: determine specific latent heat** | **MISSING** | Not addressed | No phase-change lab or simulation. |
| **Key practical: examine Boyle's law** | **MISSING** | Not addressed | No Boyle's law experiment or simulation. |
| **Suggested activity: calibrate thermometer** | **MISSING** | Not addressed | No thermometer calibration. |
| **Suggested activity: mixture method for specific heat** | **MISSING** | Not addressed | No mixture method. |
| **Suggested activity: cooling curve / melting point** | **MISSING** | Not addressed | No cooling curve. |
| **Suggested activity: factors affecting evaporation** | **MISSING** | Not addressed | No evaporation experiment. |
| **Suggested activity: examine p-T/V-T, determine absolute zero** | **MISSING** | Not addressed | No gas law experiment. |
| **Suggested activity: observe random motion (smoke cell)** | **PARTIAL** | Teacher app shows random particle motion on screen | Not a real Brownian motion observation, but a computational analogue. |
| **Suggested activity: mechanical gas model** | **COVERED** | Teacher app gas mode is a computational gas model | The toolkit's MD simulation is a direct computational implementation of this. |
| **Comp. phys. activity: simulate random walk of molecules** | **MISSING** | No random walk simulation | The unit has MD simulation but no explicit random walk. |
| **Comp. phys. activity: simulate gas molecules + MB distribution** | **COVERED** | MaxwellBoltzmann scene; teacher app; gas_sim.py | Well covered. |
| **REMOVED: Thermometers** | ✅ Correctly absent | Not taught | Compliant — removed content is not taught. |
| **REMOVED: Transfer processes** | ✅ Correctly absent | Not taught | Compliant — removed content is not taught. |
| **REMOVED: PV = (1/3)Nm⟨c²⟩** | ✅ Correctly absent | Not taught | Compliant — removed content is not taught. |
| **REMOVED: Real gases** | ✅ Correctly absent | Not taught | Compliant — removed content is not taught. |
| **ADJUSTED: MB distribution outcomes** | **COVERED** | MB distribution is a core focus | The adjusted outcomes are well served by the existing artifacts. |

---

## 3. Required actions (prioritised)

### P1 — Critical gaps (missing entire CAF sub-topics)

1. **Add heat transfer content (sub-topic a)**
   - **What**: Create a new Manim scene, teacher app mode, and/or exercise covering heat capacity, specific heat capacity, internal energy (KE+PE), and calorimetry.
   - **Files**: New `units/02_thermal/manim/scenes/heat_transfer.py`, new teacher app mode, new exercise `units/02_thermal/exercises/heat_exercise.py`.
   - **Physics content**: C = Q/ΔT, c = Q/(mΔT), internal energy as sum of molecular KE and PE, zeroth law, thermal equilibrium.
   - **physics_core API**: New module `src/physics_core/thermal/calorimetry.py` with `CalorimetrySim` (abstract) + `ReferenceCalorimetrySim`.
   - **Effort**: L
   - **CAF citation**: Lines 1382–1430 (sub-topic a), lines 1523–1524 (key practical tasks), lines 1530–1531 (suggested activities).

2. **Add change-of-state content (sub-topic b)**
   - **What**: Create artifacts covering latent heat, specific latent heat (l_f, l_v), evaporation, cooling effect.
   - **Files**: New Manim scene, teacher app mode, exercise.
   - **Physics content**: l_f = Q/m, l_v = Q/m, latent heat as molecular PE change, evaporation below boiling point, factors affecting evaporation rate.
   - **physics_core API**: New module `src/physics_core/thermal/phase_change.py`.
   - **Effort**: L
   - **CAF citation**: Lines 1435–1467 (sub-topic b), line 1525 (key practical), lines 1532–1534 (suggested activities).

3. **Add gas-law content (sub-topic c — empirical laws)**
   - **What**: Create artifacts covering Boyle's law, pressure law, Charles' law, absolute zero determination by extrapolation, Kelvin scale.
   - **Files**: New Manim scene(s), teacher app mode, exercise.
   - **Physics content**: p-V, p-T, V-T relationships; pV/T = constant; pV = nRT; absolute zero from extrapolation; Kelvin vs Celsius.
   - **physics_core API**: Could extend `gas_sim.py` with isothermal/isochoric/isobaric modes, or create a separate `gas_laws.py` module.
   - **Effort**: L
   - **CAF citation**: Lines 1471–1518 (sub-topic c), lines 1526, 1535–1536 (key practical + suggested activities).

### P2 — Important enhancements

4. **Add random walk simulation (comp. phys. activity)**
   - **What**: Create a Manim scene and/or exercise simulating random walk of molecules (Brownian motion analogue).
   - **Files**: New `units/02_thermal/manim/scenes/random_walk.py`, optional exercise.
   - **Physics content**: Random walk, diffusion, relationship to molecular motion.
   - **physics_core API**: New `src/physics_core/thermal/random_walk.py` or extend existing.
   - **Effort**: M
   - **CAF citation**: Line 1544 (suggested computational physics activity).

5. **Add explicit KE_avg = 3RT/(2N_A) formula**
   - **What**: Add the specific CAF formula to the teacher app info panel and/or questions.md, showing the connection between simulation units and real-world constants.
   - **Files**: `units/02_thermal/teacher_app/main.py`, `units/02_thermal/exercises/questions.md`.
   - **Physics content**: KE_avg = 3RT/(2N_A) = (3/2)kT, relationship between R, N_A, and k_B.
   - **physics_core API**: No change needed (already supports equipartition).
   - **Effort**: S
   - **CAF citation**: Lines 1509–1511.

6. **Add quantitative kinetic theory problem-solving**
   - **What**: Add numerical exercises where students calculate pressure, temperature, or speed from given parameters using the ideal gas law and kinetic theory formulas.
   - **Files**: `units/02_thermal/exercises/questions.md` or new `problems.md`.
   - **Physics content**: pV = nRT, KE_avg = (3/2)kT, RMS speed calculations.
   - **physics_core API**: No change needed.
   - **Effort**: S
   - **CAF citation**: Lines 1490–1491, 1518 (solve problems involving general gas law and kinetic theory).

### P3 — Polish

7. **Add Kelvin scale discussion to teacher app**
   - **What**: Show temperature in Kelvin (simulation units already map to Kelvin-like scale) and add a note about absolute zero.
   - **Files**: `units/02_thermal/teacher_app/main.py` info panel.
   - **Effort**: S
   - **CAF citation**: Lines 1483–1484 (use Kelvin as a temperature scale).

8. **Add zeroth law / thermal equilibrium concept question**
   - **What**: Add a question to questions.md about thermal equilibrium and the zeroth law.
   - **Files**: `units/02_thermal/exercises/questions.md`.
   - **Effort**: S
   - **CAF citation**: Lines 1401–1403.

---

## 4. Notes

### What the unit teaches that CAF removed
- **None.** The unit focuses on kinetic theory, Maxwell-Boltzmann distribution, and the ideal gas law — all of which are retained or adjusted in the CAF. The removed items (thermometers, transfer processes, PV = (1/3)Nm⟨c²⟩, real gases) are not taught.

### What CAF keeps that the unit misses
- **Heat transfer (a) and change of state (b)** are entirely absent. These are major sub-topics covering ~50% of the Thermal Physics curriculum content. The unit effectively covers only sub-topic (c) Gases.
- **Empirical gas laws** (Boyle's, Charles', pressure law) and **absolute zero determination** are missing. The unit jumps straight to pV = NkT without building up from the three empirical relationships.
- **Key practical tasks** (specific heat capacity, latent heat, Boyle's law) are not addressed by any artifact.

### Ambiguities and risks
- The CAF renames the topic from "Heat and Gases" to "Thermal Physics" and reorganises content. The unit name "Thermal Physics (Kinetic Theory)" is accurate for what it covers but misleading in scope — it implies broader thermal coverage than it delivers.
- The CAF "adjusts" Maxwell-Boltzmann distribution outcomes (Annex 3, line 4356) but does not specify the exact adjustment. The unit's MB coverage is thorough and likely exceeds the adjusted requirements.
- The computational physics activities in the CAF (random walk + MB distribution) are a subset of what the unit could deliver. Adding the random walk would make the unit fully compliant with the suggested computational activities.
- The unit uses 2D simulation for visual clarity, but the CAF kinetic theory outcomes (KE_avg = 3RT/(2N_A)) are explicitly 3D. The equations.py already supports both 2D and 3D, but the default artifacts use 2D. Teachers should be aware of this dimensional mismatch.

### Summary of compliance
- **COVERED**: 7 items
- **PARTIAL**: 3 items
- **MISSING**: 14 items (including 2 entire sub-topics)
- **NEW-IN-CAF**: 0 (no new content in Thermal Physics beyond what was in the previous curriculum)
- **REMOVED-IN-CAF**: 4 items — all correctly absent from the unit
