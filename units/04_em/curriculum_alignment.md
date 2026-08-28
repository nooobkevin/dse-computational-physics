# Unit 04 Electricity and Magnetism — Curriculum Alignment (CAF Consultation Draft)

## 1. Curriculum spec

Source: *Physics Curriculum (Secondary 4-6) — Consultation Draft, June 2026*, Topic 4 (lines 1843–2097), Annex 3 (lines 4237–4421), §2.2.2 (lines 571–730).

### Content items

| Letter | Sub-topic | Learning outcomes (abbreviated; formulas preserved) |
|---|---|---|
| **a** | Electric current, electric potential, and resistance | define electric current as rate of net flow of electric charges; distinguish convention direction vs electron flow; define p.d./voltage as energy converted per unit charge passing between points outside source; define e.m.f. as energy imparted per unit charge passing through source; define resistance `R = V/I` and resistivity `ρ = RA/l`; identify variation of current with applied p.d. for ohmic and non-ohmic conductors |
| **b** | Simple circuits and electrical power — Kirchhoff's Laws, equivalent resistance in series and parallel, internal resistance, electrical power dissipation | state KCL (ΣI=0) and KVL (ΣV=0); compare series/parallel circuits in terms of p.d. and current; derive `R = R₁+R₂+…` (series) and `1/R = 1/R₁+1/R₂+…` (parallel); assign earthed points as zero potential; compare e.m.f. vs terminal voltage, relate to internal resistance; state power dissipation `P`; derive `P = VI`, `P = I²R`, `P = V²/R`; solve problems involving simple circuits |
| **c** | Electrostatics — Electric charges, Coulomb's law, Electric field, Electric field strength | examine evidence for two kinds of charges; realise attraction/repulsion; interpret charging/discharging as electron transfer; state Coulomb's law `F = Q₁Q₂/(4πε₀ r²)`; solve problems involving forces between point charges; describe electric field around a point charge and between parallel charged plates; represent electric field using field lines; explain how charges interact via an electric field; define electric field strength as force per unit charge on a positive test charge; state `E = Q/(4πε₀ r²)` around a point charge and `E = V/d` between parallel plates; solve related problems |
| **d** | Magnetic field — Magnetic force and magnetic field, Magnetic effect of electric current, Current-carrying conductor in magnetic field | examine magnetic field pattern around a permanent magnet; describe behaviour of a compass in a magnetic field; represent magnetic field using field lines; examine magnetic field patterns for currents through a long straight wire, a circular coil and a long solenoid; apply `B = μ₀I/(2πr)` and `B = μ₀NI/l`; solve related problems; examine force on a current-carrying conductor in a magnetic field, determine relative directions of force, field and current; determine factors affecting force on a straight current-carrying wire, `F = BIl sinθ`; determine turning effect on a current-carrying coil in a magnetic field; solve problems involving current-carrying conductors in a magnetic field; represent force on a moving charge in a magnetic field by `F = BQv sinθ` and solve problems |

### Key practical tasks (lines 2046–2049)
- compare V-I graphs of ohmic and non-ohmic conductors
- determine internal resistance of a power source
- measure magnetic field strengths around a long straight wire and/or inside a long solenoid carrying current using hall probe/search coil

### Suggested Learning and Teaching Activities (lines 2054–2074)
- examine a wire's resistivity through investigating factors affecting resistance
- identify parallel or series circuit in a bread board
- design and construct a simple circuit to perform a simple function using bread board
- examine attractive and repulsive force upon different kinds of charges
- show nature of attraction and repulsion of charges using electrostatic generation equipment
- demonstrate bouncing metal ball between uniform electric field (parallel metal plates with EHT)
- measure magnetic field strength by using simple current balance
- use virtual reality device to visualise electric field and magnetic field patterns
- examine force on a current-carrying conductor in a magnetic field, determine relative directions
- examine `F = BIl sinθ` by varying length and current
- demonstrate deflection of electron beam by electric field and magnetic field using cathode ray tube
- read Maxwell's story of the development on electromagnetism
- study the development in definition of Ampere

### Suggested Computational Physics activities (line 2078)
- simulate the electric field or magnetic field patterns

### Annex 3 — Removed from E&M (lines 4290–4295)
- Variation of current with applied potential difference for different materials, effect of temperature on the resistance of metals and semiconductors
- Effect of resistance of ammeters and voltmeters on measurements
- Root-mean-square value of alternating current

### Annex 3 — Adjusted learning outcomes for E&M (line 4358)
- Kirchhoff's laws (learning outcomes adjusted)

---

## 2. Coverage matrix

| # | Curriculum item | Status | Current artifact | Gap |
|---|---|---|---|---|
| **a1** | Define electric current as rate of net flow of charge | MISSING | — | No artifact defines current; circuit mode shows `I` value but never states the definition |
| **a2** | Distinguish conventional current vs electron flow | MISSING | — | No artifact addresses this distinction |
| **a3** | Define p.d./voltage as energy per unit charge | MISSING | — | Circuit mode displays voltage drops but does not define the quantity |
| **a4** | Define e.m.f. as energy imparted per unit charge | PARTIAL | `questions.md` Q(f) computes terminal voltage vs e.m.f. | Definition not stated explicitly; only implicit in internal-resistance problem |
| **a5** | Define resistance `R = V/I` and resistivity `ρ = RA/l` | PARTIAL | Circuit mode uses `R` values; `questions.md` uses Ohm's law | Resistivity `ρ = RA/l` not covered anywhere |
| **a6** | Identify variation of current with applied p.d. for ohmic/non-ohmic conductors | PARTIAL | Circuit mode shows ohmic (linear) behaviour only | Non-ohmic conductors not shown; no V-I graph comparison |
| **a6-rem** | Variation of current with applied PD for *different materials*; temperature effect on resistance of metals/semiconductors | REMOVED-IN-CAF | — | Annex 3 deletes this sub-topic; do NOT add |
| **a6-rem** | Effect of resistance of ammeters/voltmeters on measurements | REMOVED-IN-CAF | — | Annex 3 deletes this; do NOT add |
| **a6-rem** | RMS value of alternating current | REMOVED-IN-CAF | — | Annex 3 deletes this; do NOT add |
| **b1** | State KCL (ΣI=0) and KVL (ΣV=0) | COVERED | Manim `CircuitComparison`; teacher app `--mode circuit`; exercise `StudentCircuit.resolve()`; `questions.md` Q(d)(e) | — |
| **b2** | Compare series and parallel circuits in terms of p.d. and current | PARTIAL | Series circuit shown in teacher app and Manim | Parallel circuit not implemented in any artifact |
| **b3** | Derive `R = R₁+R₂+…` (series) and `1/R = 1/R₁+1/R₂+…` (parallel) | PARTIAL | Series equivalent resistance implicit in circuit mode | Parallel combination not shown; derivation not demonstrated |
| **b4** | Assign earthed points as zero potential | COVERED | Nodal analysis in `ReferenceCircuit` uses node 0 as ground (0 V) | — |
| **b5** | Compare e.m.f. vs terminal voltage, relate to internal resistance | PARTIAL | `questions.md` Q(f) computes terminal voltage and internal power | No interactive artifact demonstrates internal resistance; no Manim scene or teacher-app mode for it |
| **b6** | State power dissipation; derive `P = VI`, `P = I²R`, `P = V²/R` | COVERED | Teacher app circuit mode displays `P = I²R`; Manim shows power; exercise checks `power_dissipated()` | — |
| **b7** | Solve problems involving simple circuits | PARTIAL | Series circuit solved in all artifacts | Only series topology; no parallel or mixed circuits |
| **c1** | Examine evidence for two kinds of charges | MISSING | — | No artifact covers charging by friction, induction, or evidence for ± charges |
| **c2** | Attraction and repulsion between charges | MISSING | — | No artifact demonstrates Coulomb force between two charges |
| **c3** | Interpret charging/discharging as electron transfer | MISSING | — | No artifact covers this |
| **c4** | State Coulomb's law `F = Q₁Q₂/(4πε₀ r²)` | COVERED | `ReferenceElectricField.field()` implements Coulomb's law; Manim `ElectricFieldLines`; teacher app field mode; exercise `StudentElectricField.field()` | — |
| **c5** | Solve problems involving forces between point charges | PARTIAL | Exercise computes field (force per unit charge) | No two-charge force calculation; only single-charge field |
| **c6** | Describe electric field around a point charge and between parallel charged plates | COVERED | Manim `ElectricFieldLines` (both point charge and parallel plates); teacher app field mode (both) | — |
| **c7** | Represent electric field using field lines | COVERED | Manim `ElectricFieldLines`; teacher app `draw_field_lines()` | — |
| **c8** | Explain how charges interact via an electric field | PARTIAL | Field mode shows field lines but does not articulate the "action-at-a-distance" explanation | Conceptual explanation missing from artifacts |
| **c9** | Define electric field strength as force per unit charge on a positive test charge | PARTIAL | Teacher app info panel shows `E = q/(4πε₀ r²)` | Definition "force per unit charge" not stated explicitly |
| **c10** | State `E = Q/(4πε₀ r²)` and `E = V/d`; solve related problems | COVERED | Point charge `E` formula in teacher app and Manim; parallel plate `E = V/d` shown in Manim | — |
| **d1** | Examine magnetic field pattern around a permanent magnet | MISSING | — | Only current-carrying wire field is implemented |
| **d2** | Describe behaviour of a compass in a magnetic field | MISSING | — | No compass simulation |
| **d3** | Represent magnetic field using field lines | PARTIAL | Teacher app `--mode magnet` shows concentric circles for straight wire | Permanent magnet field lines missing |
| **d4** | Examine magnetic field patterns for straight wire, circular coil, long solenoid | PARTIAL | Straight wire in teacher app; `ReferenceSolenoid` exists in engine | Circular coil missing entirely; solenoid has engine API but no teacher app or Manim scene |
| **d5** | Apply `B = μ₀I/(2πr)` and `B = μ₀NI/l`; solve related problems | PARTIAL | Straight wire formula in teacher app info panel; solenoid formula in `ReferenceSolenoid` | No interactive solenoid demo; no Manim scene for B-field |
| **d6** | Examine force on current-carrying conductor in magnetic field; determine relative directions | MISSING | — | No artifact implements `F = BIl sinθ` or right-hand rule for force |
| **d7** | Determine factors affecting force on straight wire; `F = BIl sinθ` | MISSING | — | No artifact varies `I`, `l`, `θ` to show force dependence |
| **d8** | Determine turning effect on a current-carrying coil in a magnetic field | MISSING | — | No motor-effect simulation |
| **d9** | Solve problems involving current-carrying conductors in a magnetic field | MISSING | — | No problems or exercises for this |
| **d10** | Represent force on a moving charge `F = BQv sinθ`; solve problems | MISSING | — | No artifact covers Lorentz force on moving charge |
| **KP1** | Compare V-I graphs of ohmic and non-ohmic conductors | PARTIAL | Circuit mode shows ohmic I-V data | No V-I graphing; non-ohmic not shown |
| **KP2** | Determine internal resistance of a power source | PARTIAL | `questions.md` Q(f) computes it | No interactive experiment for internal resistance |
| **KP3** | Measure magnetic field strengths around straight wire and/or solenoid using hall probe | MISSING | — | No measurement simulation |
| **CP** | Simulate electric field or magnetic field patterns | COVERED | Teacher app field mode + magnet mode; Manim scenes | — |

### Status summary

| Status | Count |
|---|---|
| COVERED | 9 |
| PARTIAL | 15 |
| MISSING | 16 |
| REMOVED-IN-CAF | 3 |
| NEW-IN-CAF | 0 |

---

## 3. Required actions (prioritised)

### P1 — High (curriculum-critical gaps)

1. **Add parallel-circuit teacher-app mode and Manim scene** — `teacher_app/main.py` and new Manim scene `parallel_circuit.py`. Physics: two-branch parallel resistors with KCL verification at the junction node. Reuses `ReferenceCircuit` (engine already supports arbitrary topologies). Effort: **M**. CAF citation: item b2, b3, b7 (lines 1915–1923).

2. **Add internal-resistance teacher-app mode** — new mode `--mode internal-r` or extend circuit mode. Show battery with internal resistor `r` in series with load `R`, display terminal voltage `V = ε - Ir`. Reuses `ReferenceCircuit` (add a branch with small R for internal resistance). Effort: **S**. CAF citation: item b5 (lines 1928–1932), key practical task line 2047.

3. **Add Lorentz-force (`F = BIl sinθ`) teacher-app mode** — new mode `--mode lorentz`. Show a current-carrying wire segment in a uniform B-field; vary `I`, `l`, `θ` with sliders; display computed force vector. Requires new `physics_core/em/force.py` module (or extend `magnetism.py`). Effort: **M**. CAF citation: item d6, d7 (lines 2017–2027).

4. **Add moving-charge Lorentz force (`F = BQv sinθ`) teacher-app mode or Manim scene** — charged particle moving through a uniform B-field, showing circular/helical trajectory. Reuses `integrators.py` for ODE stepping. Effort: **M**. CAF citation: item d10 (lines 2037–2039).

5. **Add solenoid magnetic-field teacher-app mode** — new mode `--mode solenoid`. Show solenoid cross-section with uniform internal field `B = μ₀NI/l` and near-zero external field. Uses existing `ReferenceSolenoid`. Effort: **S**. CAF citation: item d4, d5 (lines 2000–2015).

6. **Add permanent-magnet field teacher-app mode** — new mode `--mode magnet-static`. Show dipole field pattern (bar magnet) with field lines from N to S pole. Requires new `ReferenceBarMagnet` in `magnetism.py`. Effort: **M**. CAF citation: item d1, d3 (lines 1987–1993).

### P2 — Medium (important but can follow P1)

7. **Add V-I graphing mode for ohmic vs non-ohmic conductors** — new teacher-app mode `--mode vi-graph`. Plot I vs V for a resistor (ohmic) and a diode/filament (non-ohmic). Use synthetic data. Effort: **S**. CAF citation: item a6 (lines 1904–1906), key practical task line 2046.

8. **Add two-charge Coulomb force exercise** — extend `StudentElectricField` or create new exercise for force between two point charges `F = k q₁q₂/r²`. Requires new engine hook or subclass. Effort: **M**. CAF citation: item c4, c5 (lines 1957–1960).

9. **Add concept-animation scenes for current definition and electron flow** — short Manim scene contrasting conventional current direction with electron flow in a wire. Effort: **S**. CAF citation: item a1, a2 (lines 1873–1879).

10. **Add resistivity exploration mode** — teacher app `--mode resistivity` showing how `R = ρL/A` varies with length, cross-section, and material. Effort: **S**. CAF citation: item a5 (lines 1901–1902), suggested activity line 2054.

11. **Add turning-effect (motor) Manim scene** — current-carrying rectangular coil in uniform B-field, showing torque and rotation. Effort: **M**. CAF citation: item d8 (lines 2029–2031).

### P3 — Low (nice-to-have / enrichment)

12. **Add circular-coil magnetic field mode** — extend `magnetism.py` with `ReferenceCircularCoil`; teacher app mode showing field pattern on the coil axis. Effort: **M**. CAF citation: item d4 (lines 2000–2003).

13. **Add compass-overlay to magnet modes** — small compass needles that align with the local field direction in the magnet teacher-app modes. Effort: **S**. CAF citation: item d2 (lines 1991–1992).

14. **Add charging-by-friction / two-kinds-of-charge Manim scene** — show charge transfer via rubbing, electroscope response. Effort: **M**. CAF citation: item c1, c2, c3 (lines 1948–1954).

15. **Add electron-beam deflection Manim scene** — CRT-style beam deflected by E-field (parallel plates) and B-field (Helmholtz coils). Effort: **M**. CAF citation: suggested activity line 2070–2071.

### Cleanup — Removed content still present

16. **Check for any residual references to removed sub-topics** — search codebase for "RMS", "ammeter resistance", "voltmeter resistance", "temperature coefficient of resistance". If found, remove or annotate as historical. Effort: **S**. CAF citation: Annex 3 lines 4291–4295.

---

## 4. Notes

### Ambiguities

- **Ohmic vs non-ohmic identification (item a6)** remains in the spec (line 1904–1906) even though Annex 3 removes "variation of current with applied potential difference for different materials". The distinction is that basic identification of ohmic vs non-ohmic conductors is retained; the deeper treatment (different materials, temperature effects) is removed. The toolkit currently covers only ohmic conductors, so a basic V-I comparison mode is still needed.
- **Kirchhoff's laws "adjusted" (Annex 3 line 4358)** — the nature of the adjustment is not specified in the consultation draft. The toolkit's current treatment (KCL + KVL with nodal analysis) is robust and likely exceeds whatever the adjustment entails. Monitor the final curriculum for specifics.

### Risks

- **Magnetic field coverage is the weakest area** — 6 of 10 outcomes are MISSING. The toolkit has a solid engine foundation (`ReferenceStraightWire`, `ReferenceSolenoid`) but only one teacher-app mode (straight wire) and no Manim scenes for magnetism. This is the highest-risk gap.
- **Item a (current, voltage, resistance) has 4 MISSING outcomes** — the toolkit jumps straight to circuit analysis without defining the fundamental quantities. Students using the toolkit without prior lecture may lack context.
- **Parallel circuits are entirely absent** — every artifact uses a series topology. This is a significant gap since the curriculum explicitly requires comparison of series and parallel.
- **No student exercise for magnetism** — the exercise covers only electrostatics and circuits. Magnetism has no fill-in-the-blank coding task.

### Removed content still present

- The teacher app and Manim scenes do **not** contain any of the Annex 3 removed items (RMS, ammeter/voltmeter loading, temperature effects on resistance). No cleanup needed for this unit.
- However, the `questions.md` internal-resistance question (Qf) is still valid — internal resistance is **not** removed; only the ammeter/voltmeter loading effect is removed.

### Computational Physics alignment

The CAF suggests "simulate the electric field or magnetic field patterns" as the CP activity for this topic (line 2078). The toolkit exceeds this with three artifacts (Manim, teacher app, student exercise) for electric fields and one (teacher app) for magnetic fields. The gap is that the student exercise does not include a magnetism coding task — adding one would bring the unit fully in line with the CP recommendation.

### Cross-unit dependencies

- **Unit 05 (Physics & Engineering)** inherits domestic electricity, electromagnetic induction, AC, and transformers from the old E&M topic per Annex 3 reorganisation (lines 4341–4345). The E&M unit should **not** cover these; they belong in Unit 05.
- The `ReferenceSolenoid` engine class is shared — any solenoid visualisation added here will also be usable by Unit 05 for transformer core physics.