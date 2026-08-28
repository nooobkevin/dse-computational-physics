# Unit 07 Quantum Physics — Curriculum Alignment (CAF Consultation Draft)

## 1. Curriculum Spec

### Topic 7. Quantum Physics — Overview
Quantum Physics studies physical phenomena at small scales (atoms, subatomic particles). It embraces a probabilistic approach (vs deterministic classical physics). Key concepts: quantisation, photoelectric effect, wave-particle duality, quantum superposition, Heisenberg's uncertainty principle.

**Nature of Science:** Classical theory failed to explain line spectra and photoelectric effect → scientific laws are subject to revision when new evidence emerges (lines 2671-2675).

---

### Content Items (a-e)

#### a. Atomic Model (lines 2682-2697)
- Recognise JJ Thomson's discovery of electron
- Describe Rutherford's construction of atomic model (nucleus + electrons) from scattering experiments
- State limitations of Rutherford's model in accounting for line spectra

#### b. Photoelectric effect (lines 2701-2726)
- Evidence for light quanta, Einstein's interpretation, photoelectric equation
- Describe photoelectric effect experiment and its results
- State limitations of wave theory of light in explaining photoelectric effect
- State photons as light quanta, relate energy to frequency using E = hf
- Describe how intensity of light of a given frequency relates to number of photons
- Realise photoelectric effect as evidence of particle nature of light
- Explain photoelectric effect using Einstein's equation: hf - phi = 0.5 * m_e * v_max^2
- Apply E = hf and Einstein's photoelectric equation to solve problems

#### c. Bohr's atomic model of hydrogen (lines 2730-2787)
- Discrete energy levels, electron transition among energy levels, Bohr's equation of electron energy
- Describe special features of line spectra of hydrogen and other monatomic gases
- Realise line spectra as evidence of quantised energy levels
- Realise energy levels of hydrogen are quantised (discrete values)
- Explain spectral lines in terms of electron transitions between energy levels
- Distinguish quantum vs classical aspects in Bohr's model
- Realise daily applications: X-ray production, quantum dots in RGB displays
- Represent electron energy: E_tot = -13.6 eV / n^2
- Distinguish ionisation and excitation energies
- Derive 1/lambda_{a->b} = (-13.6 eV)/(hc) (1/b^2 - 1/a^2) for photon wavelength
- Interpret line spectra using Bohr's equation
- Apply E = hf and 1/lambda formula to solve problems

#### d. Wave-particle duality (lines 2791-2816)
- de Broglie formula lambda = h/p, Rayleigh criterion
- Realise wave-particle duality of electrons and light
- Describe evidence of electrons and light exhibiting both wave and particle properties
- Apply de Broglie formula lambda = h/p to solve problems
- Describe limitations of optical microscopes in observing small-scale substances
- Explain advantage of high resolution of electron microscopes using de Broglie wavelength and Rayleigh criterion: theta = 1.22*lambda/d

#### e. Probabilistic nature and Heisenberg's uncertainty principle (lines 2820-2863)
- Quantum superposition, measurement of a quantum particle, Heisenberg's uncertainty principle
- Realise probabilistic nature of quantum particles
- Realise graphical representation as normalised wavefunction psi(x) and probability density |psi(x)|^2
- Describe superposition state |psi> = a1|phi1> + a2|phi2> where |a1|^2 + |a2|^2 = 1
- Describe effect of measurement of a quantum particle
- Solve problems involving quantum superposition and measurement
- Realise quantum tunnelling and discuss STM application
- State Heisenberg's uncertainty principle: Delta_x * Delta_p >= h/(4*pi)
- Apply Delta_x * Delta_p >= h/(4*pi) to solve problems
- Discuss recent development and applications of quantum technology (computing, cryptography, communication)

---

### Key Practical Tasks (lines 2867-2868)
- Perform experiment using LED to estimate Planck's constant

### Suggested Learning and Teaching Activities (lines 2872-2904)
1. Rutherford black-box analogy activity
2. Gold leaf photoelectric effect with monochromatic sources
3. Photocell experiment for stopping potential
4. Electron diffraction with electron gun
5. e/m ratio with Helmholtz coils
6. Study electron microscope images
7. Observe emission/absorption line spectra with grating
8. RGB vs full colour spectrum (TV displays)
9. Diffraction limit experiment for visible light
10. Schrodinger's cat analogy for probability
11. Quantum tunnelling in radioactive decay and nuclear fusion
12. Learn about key scientists
13. Search and study particle accelerators (CERN, IHEP, SKEKB)
14. Study standard model of particle physics
15. Visit HK Science Museum (quantum technology exhibits)
16. Visit Standards and Calibration Laboratory (caesium atomic clock)

### Suggested Computational Physics Activities (lines 2908-2909)
- Simulate Rutherford scattering experiment

### STSE Connections (lines 2913-2921)
- Principles of qubits in quantum computing vs traditional computers
- Displays using quantum technology (energy efficiency)
- Daily applications of quantum technology
- Latest developments and societal/economic impacts

## 2. Coverage Matrix

| Curriculum item | Status | Current artifact | Gap |
|---|---|---|---|
| **a. Atomic Model** | | | |
| JJ Thomson's discovery of electron | MISSING | None | No content exists |
| Rutherford's atomic model from scattering | MISSING | None | **Critical gap**: CAF's #1 CP activity |
| Limitations of Rutherford's model for line spectra | MISSING | None | No explicit bridge to Bohr |
| **b. Photoelectric effect** | | | |
| Describe experiment + results | PARTIAL | Teacher app photoelectric mode | App shows K_max vs f graph, not the experiment |
| Limitations of wave theory | PARTIAL | Concept questions (questions.md) | No dedicated visual |
| Photons as light quanta, E = hf | COVERED | PhotoElectric engine, teacher app, Manim | Fully present |
| Intensity vs number of photons | MISSING | None | Not addressed |
| Particle nature of light (evidence) | PARTIAL | Concept questions | Needs explicit visual/activity |
| Einstein's photoelectric equation | COVERED | physics_core, teacher app, Manim scene | hf - phi = K_max present |
| Apply E=hf and photoelectric equation | PARTIAL | Concept questions | Text-only |
| **c. Bohr's atomic model of hydrogen** | | | |
| ***MODEL MISMATCH*** | PARTIAL | Infinite square well E_n = n^2*h^2/(8*m*L^2) | CAF requires E_n = -13.6/n^2 eV |
| Line spectra of hydrogen | PARTIAL | Energy level diagram | Square well, not hydrogen Balmer/Lyman |
| Quantised energy levels (concept) | PARTIAL | Manim EnergyLevels, teacher app | Conceptually present, wrong model |
| Spectral lines via transitions | PARTIAL | Transition arrows with Delta_E, lambda | Square well only |
| Bohr's equation E_n = -13.6/n^2 eV | MISSING | None | Formula absent |
| Quantum vs classical aspects | MISSING | None | Not addressed |
| Applications (X-ray, quantum dots) | MISSING | None | Not addressed |
| Ionisation vs excitation energies | MISSING | None | Not addressed |
| Derive Rydberg-like formula 1/lambda | MISSING | None | Not addressed |
| Interpret line spectra (Bohr) | MISSING | None | Not addressed |
| **d. Wave-particle duality** | | | |
| Wave-particle duality (concept) | PARTIAL | de Broglie teacher app mode, questions | Covers de Broglie not dual nature evidence |
| Evidence of wave/particle properties | PARTIAL | Concept questions | No dedicated artifact |
| de Broglie formula lambda = h/p | COVERED | physics_core, teacher app, tests | Fully present |
| Limitations of optical microscopes | MISSING | None | Not addressed |
| Electron microscope resolution + Rayleigh criterion | MISSING | None | Rayleigh criterion not implemented |
| **e. Probabilistic nature & Heisenberg UP** | | | |
| ***ENRICHED per Annex 3*** | | | Probabilistic nature, superposition, UP newly enriched |
| Probabilistic nature of quantum particles | PARTIAL | Wavefunction probability density | |psi|^2 as probability present |
| Normalised psi(x) and |psi(x)|^2 | COVERED | physics_core, Manim, exercise, tests | Fully present |
| Quantum superposition bra-ket | MISSING | None | **Key enriched item**: bra-ket notation, superposition missing |
| Measurement effect | MISSING | None | Not addressed |
| Quantum tunnelling + STM | MISSING | None | Not addressed |
| Heisenberg UP: Delta_x*Delta_p >= h/(4*pi) | PARTIAL | Concept questions | Mentioned, no interactive/visual |
| Apply Heisenberg UP | PARTIAL | Concept questions | Text only |
| Quantum technology (computing, cryptography, comms) | MISSING | None | STSE gap |
| **Key Practical Tasks** | | | |
| LED experiment for Planck's constant | MISSING | None | Should have teacher app mode |
| **Comp. Phys. Activities** | | | |
| Simulate Rutherford scattering | MISSING | None | **Primary CP gap**: only CP activity in CAF |
| **STSE Connections** | | | |
| Qubits/quantum computing | MISSING | None | Not addressed |
| Quantum displays | MISSING | None | Not addressed |
| Daily quantum technology applications | MISSING | None | Not addressed |
| **REMOVED items (Annex 3 L4312-4317)** | | | |
| Bohr model angular momentum quantisation | REMOVED-IN-CAF | Absent | Correctly absent |
| Nano-scale, TEM, nanotechnology | REMOVED-IN-CAF | Absent | Correctly absent |

## 3. Required Actions (Prioritised)

### P1 — Critical (CAF mandatory, complete absence)

**1. Add Rutherford scattering simulation**
- What: New Manim scene + teacher app mode + physics_core module simulating alpha-particle scattering by a gold foil (Coulomb repulsion + randomised impact parameters)
- Files: `src/physics_core/quantum/rutherford.py` (new), `units/07_quantum/manim/scenes/rutherford_scattering.py` (new), teacher app mode `--mode rutherford`, exercise variant
- Physics: Coulomb force F = k q1 q2 / r^2, randomised impact parameter b, scattering angle theta(b)
- Reusable API: `RutherfordScattering` engine class with `scatter(impact_parameter, energy)` hook
- Effort: L
- CAF: lines 2908-2909 "simulate the Rutherford scattering experiment"; lines 2684-2688 describe Rutherford's model; Annex 3 L4252-4254 integrates Atomic World content

**2. Replace infinite square well with Bohr hydrogen atom model**
- What: Change physics_core from `E_n = n^2 h^2 / (8mL^2)` (square well) to `E_n = -13.6/n^2 eV` (Bohr hydrogen). Update all Manim scenes, teacher app well mode, student exercise, concept questions, and tests. Square well can remain as a pedagogical stepping-stone but the primary CAF model must be Bohr.
- Files: `src/physics_core/quantum/wavefunctions.py` (rename/refactor or add `BohrHydrogenAtom` class), all Manim scenes, teacher app, exercise, tests, questions.md
- Physics: E_n = -13.6/n^2 eV, 1/lambda = R_H (1/n_f^2 - 1/n_i^2), Balmer/Lyman series
- Reusable API: `BohrHydrogenAtom` with `energy_level(n)`, `transition_wavelength(n_i, n_f)`, `ionisation_energy()`, `excitation_energy(n)`
- Effort: L
- CAF: lines 2730-2787 Bohr's model; E_tot = -13.6/n^2 eV L2763-2765; Rydberg formula L2769-2777

**3. Add quantum superposition state visualisation**
- What: New Manim scene + teacher app mode showing |psi> = a1|phi1> + a2|phi2> with probability weights |a1|^2 + |a2|^2 = 1
- Files: `units/07_quantum/manim/scenes/superposition.py` (new), teacher app mode `--mode superposition`
- Physics: Bra-ket notation, probability amplitudes, normalisation, measurement collapse
- Reusable API: `SuperpositionState` class in `src/physics_core/quantum/superposition.py`
- Effort: M
- CAF: lines 2828-2840 (enriched content per Annex 3 L4394-4395); "describe superposition state using |psi> = a1|phi1> + a2|phi2>"

### P2 — High (important gaps in existing topics)

**4. Add photoelectric intensity-photon number visualisation**
- What: Extend teacher app photoelectric mode to show intensity slider controlling photon count, illustrating that intensity affects current not K_max
- Files: `units/07_quantum/teacher_app/main.py` (_run_photoelectric)
- Physics: intensity proportional to number of photons per second per area
- Reusable API: Extend `PhotoElectric` with `photon_flux(intensity, f)` method
- Effort: S
- CAF: lines 2711-2712 "relate intensity to number of photons"

**5. Add Heisenberg uncertainty principle interactive visualisation**
- What: Teacher app mode showing Delta_x * Delta_p >= h/(4*pi) with sliders for well width L showing how confinement affects minimum energy
- Files: `units/07_quantum/teacher_app/main.py` (new `--mode uncertainty` or extend well mode)
- Physics: Delta_x ~ L, Delta_p ~ h/(4*pi*L), E_min ~ (Delta_p)^2/(2m) ~ h^2/(32*pi^2*m*L^2)
- Reusable API: Add `uncertainty_energy(L)` to `QuantumWell` base
- Effort: S
- CAF: lines 2852-2855 Heisenberg's UP; enrichment per Annex 3 L4396

**6. Add Rayleigh criterion / electron microscope resolution visualisation**
- What: Teacher app mode showing theta = 1.22*lambda/d for optical vs electron microscopes. Compare resolution limits visually.
- Files: `units/07_quantum/teacher_app/main.py` (new `--mode rayleigh`), physics_core method
- Physics: theta_min = 1.22*lambda/d, de Broglie lambda = h/p for electrons
- Reusable API: `rayleigh_criterion(wavelength, aperture_diameter)` in physics_core
- Effort: M
- CAF: lines 2807-2816 (limitations of optical microscopes, Rayleigh criterion)

### P3 — Medium (CAF-mandated but less central)

**7. Add quantum tunnelling + STM demonstration**
- What: New teacher app mode showing wavefunction penetration through finite barrier, STM tip-surface tunnelling current
- Files: `src/physics_core/quantum/tunnelling.py` (new), teacher app mode `--mode tunnelling`
- Physics: Finite potential barrier, exponential decay of psi in classically forbidden region, tunnelling probability
- Reusable API: `TunnellingBarrier` class with `transmission_probability(E, V0, width)` and `tunnelling_current(distance)`
- Effort: M
- CAF: lines 2842-2844 "realise quantum tunnelling and discuss STM"

**8. Add quantum technology STSE module**
- What: Teacher app info panel or concept questions on qubits, quantum cryptography, quantum communication
- Files: `units/07_quantum/exercises/questions.md` (extend), teacher app mode(s)
- Effort: S
- CAF: lines 2857-2863 (quantum computing, cryptography, communication), lines 2913-2921 (STSE)

**9. Add LED Planck's constant experiment simulation**
- What: Teacher app mode simulating LED I-V curves at different wavelengths, computing h from V_threshold vs 1/lambda
- Files: `src/physics_core/quantum/led_experiment.py` (new), teacher app `--mode led`
- Physics: eV_threshold = hc/lambda, h = eV_threshold * lambda / c
- Reusable API: `LEDExperiment` with `threshold_voltage(lambda_, temperature)` and `planck_from_led(voltages, wavelengths)`
- Effort: M
- CAF: lines 2867-2868 "perform experiment using LED to estimate Planck's constant"

**10. Add historical scientists timeline activity**
- What: Brief teacher app mode or README timeline of JJ Thomson, Planck, Einstein, Rutherford, Bohr, de Broglie, Schrodinger, Heisenberg
- Files: `units/07_quantum/README.md` (extend)
- Effort: S
- CAF: lines 2895-2897 "learn about scientists"

### P4 — Low (nice-to-have, enrichment)

**11. Add standard model / particle accelerator info**
- Effort: S
- CAF: lines 2898-2901

**12. Add quantum dots / RGB displays application**
- Effort: S
- CAF: lines 2754-2760 "quantum dots in RGB displays"

---

## 4. Notes

### Ambiguities and Risks

1. **Model mismatch risk**: The current infinite square well (E_n = n^2 h^2 / 8mL^2) is a pedagogical simplification. The CAF requires Bohr hydrogen (E_n = -13.6/n^2 eV). Students could be confused if both models coexist without clear labelling. Square well can stay as a "simplified model" enrichment but the primary CAF-mandated content is Bohr hydrogen. The student exercise must target the Bohr formula, not the square well.

2. **Rutherford scattering as CP activity**: The CAF lists "simulate Rutherford scattering experiment" as the sole Suggested Computational Physics activity for Quantum Physics (line 2908-2909). This is a clear mandate. Given the toolkit's architecture (physics_core engine → three artifacts), implementing this aligns perfectly with the project's design philosophy.

3. **Removed content not present**: The Annex 3 removals (Bohr quantisation of angular momentum L4313-4314, nano-scale/TEM/nanotechnology L4315-4317) are correctly absent from the current unit. No action needed.

4. **Superposition notation**: The CAF uses Dirac bra-ket notation (|psi> = a1|phi1> + a2|phi2>). This is a significant conceptual leap for DSE students. The implementation must balance rigour with accessibility.

5. **Computational physics vs teacher demo**: Several CAF learning activities (LED experiment, gold leaf experiment, photocell, electron diffraction) are hands-on lab activities, not computational simulations. The toolkit's teacher app can complement but not replace these. The gap analysis flags only computational-amenable items.

6. **Rayleigh criterion crossover**: The Rayleigh criterion appears in both Quantum Physics (electron microscope resolution) and Waves (optical resolution). The CAF integrates intensity concepts across topics. Ensure the Quantum unit's implementation references the Waves unit's treatment to avoid duplication.

### Removed Content Still Present
None. The unit correctly avoids all REMOVED-IN-CAF items.
