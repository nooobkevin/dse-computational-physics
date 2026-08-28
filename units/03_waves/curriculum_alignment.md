# Unit 03 Waves — Curriculum Alignment (CAF Consultation Draft)

> **Source:** *Physics Curriculum (Secondary 4-6) — Consultation Draft, June 2026*
> **Topic:** 3. Waves (lines 1563–1842)
> **Annex 3 changes:** lines 4237–4421
> **Comp. Physics emphasis:** §2.2.2 (lines 571–730)

---

## 1. Curriculum spec

### 1.1 Content items and learning outcomes

| Item | Content | Students should be able to |
|------|---------|---------------------------|
| **a** | **Nature of waves** — Wave motion and propagation; Traveling waves and stationary waves | • recognise wave motion in terms of oscillation<br>• realise travelling waves as transmitting energy without transferring matter<br>• relate wave energy to amplitude<br>• distinguish between transverse and longitudinal waves<br>• describe wave motion in terms of waveform, crest, trough, compression, rarefaction, wavefront, phase, displacement, amplitude, period, frequency, wavelength and wave speed<br>• describe the superposition of traveling waves and the formation of a stationary wave (transverse wave only)<br>• interpret displacement-time and displacement-distance graphs for travelling waves and stationary waves (transverse wave only)<br>• apply *v = fλ* to solve problems |
| **b** | **Properties of waves** — Reflection; Refraction; Diffraction; Interference | • describe the reflection of waves at a plane barrier/reflector/surface<br>• examine the condition for a phase change on reflection<br>• describe the refraction of waves across a plane boundary of different media<br>• realise the change in wave speeds during refraction and define refractive index in terms of wave speeds<br>• describe the diffraction of waves through a narrow gap and around a corner<br>• examine the effect of width of slit on the degree of diffraction<br>• describe the interference of waves resulted from superposition<br>• distinguish between constructive and destructive interferences of waves<br>• examine the interference of waves from two coherent sources<br>• determine the conditions for constructive and destructive interferences in terms of path difference<br>• draw wavefront diagrams to show the properties of waves |
| **c** | **Light waves** — Reflection and refraction; Polarisation, diffraction and interference; Intensity | • state that the speed of light and electromagnetic wave in a vacuum is 3.0 × 10⁸ m s⁻¹<br>• state the range of wavelengths for visible light and other parts of the electromagnetic spectrum<br>• examine the polarisation of light as an evidence for light as transverse wave<br>• realise reflection and refraction as the wave properties of light<br>• realise the occurrence of total internal reflection of light and its daily applications<br>• realise diffraction and interference as evidences for the wave nature of light<br>• examine the interference pattern in the Young's double slit experiment<br>• examine the diffraction pattern when light passes through the plane transmission grating<br>• define intensity as power per unit area in classical wave theory<br>• recognise the intensity distribution of the fringe pattern in the Young's double slit experiment<br>• discuss daily applications of light and electromagnetic waves using properties of waves<br>• apply *d sinθ = nλ* to solve problems related to light source passing through a plane transmission grating<br>• apply *Δy = λD/a* to estimate the wavelength of the light source used in the Young's double slit experiment |
| **d** | **Sound waves** — Wave properties in sound; Audible frequency; Musical notes | • realise sound as an example of longitudinal waves and possesses the properties of waves<br>• realise that sound can exhibit reflection, refraction, diffraction and interference<br>• compare the general properties of sound waves and those of electromagnetic waves<br>• realise the existence of ultrasound beyond the audible frequency range<br>• discuss the applications of ultrasound in ranging, cleaning and imaging<br>• compare musical notes using pitch, loudness and quality in terms of waveforms<br>• relate frequency and amplitude with the pitch and loudness of a note respectively<br>• recognise the role of resonance in producing sound in musical instruments |

### 1.2 Key Practical Tasks

- Illustrate stationary wave at different frequencies (e.g. string, Kundt's tube) and estimate the wave speed
- Determine wavelength of monochromatic source using plane transmission grating
- Examine the inverse square law of intensity of light
- Receive radio/microwave signals from artificial and natural objects for simple data analysis

### 1.3 Suggested Learning and Teaching Activities

- Demonstrate transverse wave and longitudinal wave using long spring
- Illustrate phase change on reflection using a slinky spring
- Perform ripple tank experiment to observe properties of waves
- Study the factors affecting the properties of waves in water waves, microwaves or sound waves
- Illustrate the superposition of two pulses using slinky spring
- Illustrate the superposition of transverse wave using oscilloscope
- Examine the conditions for constructive and destructive interference from two coherent sources
- Examine polarisation of light using polarisers
- Determine the effects of wavelengths, slit separation or slit-screen distance on an interference pattern in double slit experiment
- Examine fringe pattern using Young's double slits and estimate the wavelength of the monochromatic light source
- Determine audible frequency range experimentally and examine the existence of ultrasound
- Use mobile App to measure loudness and pitch, and study the interference pattern of sound
- Demonstrate resonance of sound waves (e.g. resonance box, water xylophone)
- Observe an ultrasound image of body organs and gather information
- Demonstrate the principles of pulse-echo using ultrasound transmitters and receivers
- Design and make a distancing device using sonic sensor

### 1.4 Suggested Computational Physics Activities

- Simulate superposition of transverse waves
- Simulate the formation of stationary wave

---

## 2. Coverage matrix

**Status key:** COVERED — fully addressed by one or more artifacts; PARTIAL — addressed but incomplete (e.g. only in concept questions, or only one aspect covered); MISSING — no artifact addresses this; NEW-IN-CAF — content added by the CAF draft; REMOVED-IN-CAF — content deleted by Annex 3 (should NOT be present).

### 2.1 Item a — Nature of waves

| # | Curriculum outcome | Status | Current artifact | Gap |
|---|---|---|---|---|
| a.1 | Recognise wave motion in terms of oscillation | PARTIAL | Teacher app traveling mode (moving particle on sine wave) | No explicit oscillation visualisation (e.g. a single point tracing its motion over time with velocity arrows) |
| a.2 | Travelling waves transmit energy without transferring matter | PARTIAL | Exercise docstring mentions it; README overview | No dedicated artifact visualises energy transport vs. matter transport |
| a.3 | Relate wave energy to amplitude | COVERED | Manim `WaveSpeedIntensity` (I ∝ A² bar chart); exercise test 4; `equations.intensity()` | — |
| a.4 | Distinguish transverse vs longitudinal waves | PARTIAL | Questions.md (Qf) discusses polarisation as transverse evidence | No longitudinal wave visualisation (compression/rarefaction); no side-by-side comparison |
| a.5 | Describe wave motion: waveform, crest, trough, compression, rarefaction, wavefront, phase, displacement, amplitude, period, frequency, wavelength, wave speed | PARTIAL | Teacher app traveling mode shows waveform, labels A, λ, f, v, phase; displacement-time graph | No labelled crest/trough/compression/rarefaction/wavefront on the visualisation |
| a.6 | Describe superposition → stationary wave (transverse only) | COVERED | Manim `SuperpositionStanding`; teacher app standing mode; exercise test 3 | — |
| a.7 | Interpret d-t and d-d graphs for travelling and stationary waves (transverse only) | PARTIAL | Teacher app traveling mode has d-t graph; no d-d graph | No displacement-distance graph; no stationary-wave d-t or d-d graph |
| a.8 | Apply *v = fλ* | COVERED | Teacher app displays v = fλ; `equations.wave_speed()`; `WaveSim.__init__` computes v = fλ | — |

### 2.2 Item b — Properties of waves

| # | Curriculum outcome | Status | Current artifact | Gap |
|---|---|---|---|---|
| b.1 | Describe reflection at a plane barrier | MISSING | — | No reflection visualisation (ripple tank or equivalent) |
| b.2 | Examine phase change on reflection | MISSING | — | No phase-change demonstration |
| b.3 | Describe refraction across a plane boundary | MISSING | — | No refraction visualisation |
| b.4 | Realise change in wave speed during refraction; define refractive index via wave speeds | MISSING | — | No refraction simulation |
| b.5 | Describe diffraction through a narrow gap and around a corner | MISSING | — | No diffraction visualisation |
| b.6 | Examine effect of slit width on degree of diffraction | MISSING | — | No slit-width parameter in any artifact |
| b.7 | Describe interference from superposition | COVERED | Manim `SuperpositionStanding`; teacher app standing mode | — |
| b.8 | Distinguish constructive vs destructive interference | COVERED | Manim `YoungSlit` (bright/dark fringes); questions.md Qe | — |
| b.9 | Examine interference from two coherent sources | COVERED | Manim `YoungSlit`; teacher app interference mode | — |
| b.10 | Determine conditions for constructive/destructive in terms of path difference | COVERED | Manim `YoungSlit` (path difference readout); questions.md Qe | — |
| b.11 | Draw wavefront diagrams | MISSING | — | No wavefront diagramming tool or visualisation |

### 2.3 Item c — Light waves

| # | Curriculum outcome | Status | Current artifact | Gap |
|---|---|---|---|---|
| c.1 | Speed of light / EM waves in vacuum = 3.0 × 10⁸ m s⁻¹ | MISSING | — | Not displayed anywhere |
| c.2 | Range of wavelengths for visible light and EM spectrum | MISSING | — | No EM spectrum visualisation |
| c.3 | Examine polarisation as evidence for transverse wave | PARTIAL | Questions.md Qf covers concept | No polarisation visualisation (Manim or teacher app); no polariser simulation |
| c.4 | Realise reflection and refraction as wave properties of light | MISSING | — | No reflection/refraction of light |
| c.5 | Realise TIR and its daily applications | MISSING | — | No TIR simulation (note: optical fibres are in Unit 05) |
| c.6 | Realise diffraction and interference as evidence for wave nature of light | PARTIAL | Manim `YoungSlit` shows interference | No explicit "evidence" framing; no diffraction-grating pattern |
| c.7 | Examine Young's double-slit interference pattern | COVERED | Manim `YoungSlit`; teacher app interference mode | — |
| c.8 | Examine diffraction pattern through plane transmission grating | PARTIAL | `equations.diffraction_grating_angle()` exists | No dedicated Manim/teacher app artifact for grating pattern |
| c.9 | Define intensity as power per unit area in classical wave theory | PARTIAL | `equations.intensity()` returns A²; questions.md Qc | No explicit "power per unit area" definition or calculation |
| c.10 | Recognise intensity distribution of fringe pattern in Young's double slit | MISSING | — | No intensity-vs-position graph for fringe pattern |
| c.11 | Discuss daily applications of light and EM waves | MISSING | — | No application discussion in any artifact |
| c.12 | Apply *d sinθ = nλ* for plane transmission grating | PARTIAL | `equations.diffraction_grating_angle()`; Manim `YoungSlit` shows d sinθ = nλ | Grating formula exists in engine but no dedicated artifact uses it |
| c.13 | Apply *Δy = λD/a* to estimate wavelength | COVERED | Manim `YoungSlit` displays Δy; teacher app computes fringe spacing | — |

### 2.4 Item d — Sound waves

| # | Curriculum outcome | Status | Current artifact | Gap |
|---|---|---|---|---|
| d.1 | Sound as longitudinal wave with wave properties | PARTIAL | Questions.md Qf mentions longitudinal | No sound-specific visualisation (compression/rarefaction animation) |
| d.2 | Sound exhibits reflection, refraction, diffraction, interference | MISSING | — | No sound wave simulation |
| d.3 | Compare sound and EM wave properties | MISSING | — | No comparison artifact |
| d.4 | Existence of ultrasound beyond audible range | MISSING | — | No frequency-range visualisation |
| d.5 | Applications of ultrasound: ranging, cleaning, imaging | MISSING | — | No ultrasound application demo |
| d.6 | Compare musical notes: pitch, loudness, quality in terms of waveforms | PARTIAL | Questions.md Qb (standing waves on strings, harmonics) | No waveform comparison (e.g. sine vs square vs sawtooth) |
| d.7 | Relate frequency → pitch, amplitude → loudness | MISSING | — | No pitch/loudness interactive demo |
| d.8 | Role of resonance in musical instruments | MISSING | — | No resonance visualisation |

### 2.5 Key Practical Tasks

| # | Task | Status | Current artifact | Gap |
|---|---|---|---|---|
| KPT.1 | Illustrate stationary wave at different frequencies; estimate wave speed | PARTIAL | Manim `SuperpositionStanding`; teacher app standing mode | No frequency slider/parameter variation in teacher app |
| KPT.2 | Determine wavelength using plane transmission grating | MISSING | — | No grating experiment simulation |
| KPT.3 | Examine inverse square law of intensity of light | PARTIAL | `equations.intensity_inverse_square()`; questions.md Qd | No interactive inverse-square demo |
| KPT.4 | Receive radio/microwave signals for data analysis | MISSING | — | No radio/microwave simulation |

### 2.6 Computational Physics Activities (CAF §2.2.2)

| # | Activity | Status | Current artifact | Gap |
|---|---|---|---|---|
| CPA.1 | Simulate superposition of transverse waves | COVERED | Manim `SuperpositionStanding`; teacher app standing mode; exercise superposition check | — |
| CPA.2 | Simulate the formation of stationary wave | COVERED | Manim `SuperpositionStanding`; teacher app standing mode | — |

### 2.7 Annex 3 — Changes affecting Waves

| Change | CAF citation | Status | Notes |
|--------|-------------|--------|-------|
| **REMOVED:** Longitudinal wave d-t and d-d graphs for travelling waves | Annex 3, lines 4284–4285 | REMOVED-IN-CAF | Current unit has d-t graph (transverse only) — compliant. No action needed. |
| **REMOVED:** Geometrical optics (ray diagrams for reflection/refraction/TIR, image formation by lenses, lens formula) | Annex 3, lines 4286–4288 | REMOVED-IN-CAF | No geometrical optics artifacts exist — compliant. |
| **REMOVED:** Noise | Annex 3, line 4289 | REMOVED-IN-CAF | No noise artifacts exist — compliant. |
| **INTEGRATED-IN:** Intensity concepts (from Astronomy/Atomic World/Energy) — progressive learning of intensity | Annex 3, lines 4347–4351 | PARTIAL | I ∝ A² covered; inverse-square law in `equations`; intensity as power/area not yet explicit |
| **INTEGRATED-IN:** Ultrasonic range-measurement (from Medical Physics) | Annex 3, lines 4258–4260 | MISSING | No ultrasound ranging simulation exists |
| **ENRICHED:** Polarisation of light as evidence light is transverse | Annex 3, lines 4383 | PARTIAL | Concept in questions.md; no visualisation |

---

## 3. Required actions (prioritised)

### P1 — Critical gaps (missing entire curriculum items)

**1. Add reflection/refraction/diffraction visualisation (Item b.1–b.6)**
- **What:** New Manim scene + teacher app mode showing wave reflection at a plane barrier, refraction across a boundary (with speed change), and diffraction through a narrow gap (with slit-width parameter).
- **Files:** `units/03_waves/manim/scenes/wave_properties.py`, `units/03_waves/teacher_app/main.py` (new mode), `src/physics_core/waves/equations.py` (Snell's law helper if needed)
- **Physics content:** Reflection angle = incidence angle; refraction via v₂/v₁ = sinθ₂/sinθ₁; diffraction spreading ∝ λ/a
- **Reusable API:** Add `reflect()`, `refract()`, `diffract()` to `equations.py` or a new `wave_properties.py` module
- **Effort:** L
- **CAF citation:** Item b.1–b.6 (lines 1632–1652)

**2. Add sound wave visualisation (Item d.1–d.8)**
- **What:** New Manim scene + teacher app mode showing longitudinal waves (compression/rarefaction), audible frequency range, ultrasound, and musical note waveforms.
- **Files:** `units/03_waves/manim/scenes/sound_waves.py`, `units/03_waves/teacher_app/main.py` (new mode), `src/physics_core/waves/sound.py` (new module)
- **Physics content:** Longitudinal wave animation (oscillating dots or pressure graph); frequency slider for audible/ultrasound range; waveform comparison (sine, square, triangle); resonance demonstration
- **Reusable API:** New `src/physics_core/waves/sound.py` with `LongitudinalWaveSim`, `audible_range()`, `note_frequency()`, `resonance_modes()`
- **Effort:** L
- **CAF citation:** Item d.1–d.8 (lines 1743–1777)

**3. Add ultrasound ranging simulation (Item d.5, KPT.4, Annex 3 integration)**
- **What:** Teacher app mode or exercise simulating pulse-echo ultrasound range measurement (distance = v × t / 2).
- **Files:** `units/03_waves/teacher_app/main.py` (new mode), `units/03_waves/exercises/questions.md` (add ultrasound questions)
- **Physics content:** Pulse-echo principle; speed of sound in tissue; distance calculation
- **Reusable API:** Extend `sound.py` with `ultrasound_echo(distance, speed)`
- **Effort:** M
- **CAF citation:** Item d.5 (lines 1763–1765); Annex 3 integration (lines 4258–4260)

### P2 — Important partial gaps

**4. Add polarisation visualisation (Item c.3, Annex 3 enrichment)**
- **What:** Manim scene or teacher app mode showing transverse wave passing through a polarising filter (slit analogy), with Malus's law I = I₀ cos²θ.
- **Files:** `units/03_waves/manim/scenes/polarisation.py` or `units/03_waves/teacher_app/main.py` (new mode)
- **Physics content:** Transverse wave oscillation direction; filter transmission axis; intensity vs. angle
- **Reusable API:** Add `malus_law(theta, I0)` to `equations.py`
- **Effort:** M
- **CAF citation:** Item c.3 (lines 1689–1691); Annex 3 enrichment (line 4383)

**5. Add plane transmission grating visualisation (Item c.8, c.12, KPT.2)**
- **What:** Manim scene or teacher app mode showing diffraction grating pattern with multiple orders, d sinθ = nλ, and wavelength estimation.
- **Files:** `units/03_waves/manim/scenes/diffraction_grating.py` or extend `young_slit.py`
- **Physics content:** Multiple-slit interference; order separation; wavelength calculation
- **Reusable API:** `equations.diffraction_grating_angle()` already exists
- **Effort:** M
- **CAF citation:** Item c.8 (lines 1716–1718); c.12 (lines 1732–1734); KPT.2 (line 1784)

**6. Add displacement-distance graph for stationary waves (Item a.7)**
- **What:** Extend teacher app traveling mode to show a d-d graph panel alongside the existing d-t graph.
- **Files:** `units/03_waves/teacher_app/main.py` (extend `_run_traveling`)
- **Physics content:** Snapshot of wave profile at fixed t; compare d-t (fixed x) vs d-d (fixed t)
- **Reusable API:** Already available via `sim.field(sim.x, t)`
- **Effort:** S
- **CAF citation:** Item a.7 (lines 1621–1625)

**7. Add intensity distribution graph for Young's double-slit (Item c.10)**
- **What:** Extend Manim `YoungSlit` or teacher app interference mode to show an intensity-vs-position graph alongside the fringe pattern.
- **Files:** `units/03_waves/manim/scenes/young_slit.py` or `units/03_waves/teacher_app/main.py`
- **Physics content:** I(y) = I₀ cos²(π d y / λ D); central maximum brightest
- **Reusable API:** Add `young_intensity(y, d, lam, D)` to `equations.py`
- **Effort:** S
- **CAF citation:** Item c.10 (lines 1724–1726)

**8. Add EM spectrum visualisation (Item c.1, c.2)**
- **What:** Static infographic or simple Manim scene showing EM spectrum with wavelength ranges and visible light highlighted.
- **Files:** `units/03_waves/manim/scenes/em_spectrum.py`
- **Physics content:** c = 3×10⁸ m/s; λ ranges for radio to gamma; visible light 380–750 nm
- **Reusable API:** Add `em_spectrum_bands()` to `equations.py`
- **Effort:** S
- **CAF citation:** Item c.1–c.2 (lines 1681–1687)

### P3 — Nice-to-have enhancements

**9. Add wavefront diagram drawing (Item b.11)**
- **What:** Teacher app mode showing circular/plane wavefronts reflecting, refracting, diffracting.
- **Files:** `units/03_waves/teacher_app/main.py` (new mode)
- **Effort:** M

**10. Add frequency/amplitude → pitch/loudness interactive demo (Item d.7)**
- **What:** Extend teacher app with sound synthesis (simple sine wave tone) where frequency and amplitude sliders change pitch and loudness.
- **Files:** `units/03_waves/teacher_app/main.py` (new mode)
- **Effort:** M

**11. Add resonance demonstration (Item d.8)**
- **What:** Manim scene showing driven oscillator / resonance curve for a musical instrument.
- **Files:** `units/03_waves/manim/scenes/resonance.py`
- **Effort:** M

**12. Add inverse-square law interactive demo (KPT.3)**
- **What:** Teacher app mode showing intensity vs. distance with movable source and detector.
- **Files:** `units/03_waves/teacher_app/main.py` (new mode)
- **Effort:** S

**13. Add daily applications discussion prompts (Item c.11)**
- **What:** Add questions to `questions.md` about applications of EM waves (WiFi, remote controls, smart cameras).
- **Files:** `units/03_waves/exercises/questions.md`
- **Effort:** S

---

## 4. Notes

### Ambiguities

- **Reflection/refraction of light (Item c.4–c.5):** The CAF specifies "realise reflection and refraction as the wave properties of light" and "realise TIR and its daily applications" — but geometrical optics (ray diagrams, lenses, lens formula) is **removed** (Annex 3 lines 4286–4288). The toolkit must show reflection/refraction as *wave* phenomena (e.g. ripple tank or wavefront simulation), not as ray optics. Unit 05 covers optical fibres (TIR application) — coordinate to avoid duplication.
- **Intensity definition (Item c.9):** The CAF adds "define intensity as power per unit area in classical wave theory" — this is a new emphasis. The current `intensity()` function returns A² (arbitrary units). A proper power-per-unit-area definition requires specifying the medium impedance: `I = ½ ρ v ω² A²`. Decide whether to implement the full classical expression or keep the simplified proportional form for S4 level.
- **Ultrasound ranging (Annex 3 integration):** The CAF integrates ultrasonic range-measurement from Medical Physics into Waves. The spec lists "applications of ultrasound in ranging, cleaning and imaging" (Item d.5). The pulse-echo principle can be demonstrated computationally without requiring medical physics context.

### Risks

- **Scope creep:** Items b.1–b.6 (reflection, refraction, diffraction) are a large addition — essentially a second ripple-tank simulation suite. Consider whether these are better implemented as a single combined "wave properties" scene with mode toggles rather than separate scenes.
- **Sound section (Item d):** The entire sound sub-topic (d.1–d.8) is currently almost entirely MISSING. This is the single biggest gap in the unit. Adding sound requires both longitudinal wave visualisation (new engine concept) and audio output (for pitch/loudness demos), which the current OpenCV teacher app does not support.
- **Longitudinal wave d-t/d-d graphs (REMOVED):** The CAF explicitly removes "present information of longitudinal waves on displacement-time and displacement-distance graphs for travelling waves" (Annex 3 lines 4284–4285). The current unit has no such graphs for longitudinal waves, so no removal action is needed. However, the teacher app's d-t graph is for *transverse* waves only, which remains in the curriculum.
- **Noise (REMOVED):** The CAF removes "Noise" from Waves. The current unit has no noise content — compliant.

### Removed content still present in unit

None identified. The unit does not contain geometrical optics, longitudinal wave d-t/d-d graphs, or noise content.

### Cross-unit dependencies

- **Unit 05 (Physics & Engineering):** Optical fibres and TIR — coordinate so that TIR as a wave property of light (Item c.5) is introduced in Unit 03 and applied in Unit 05.
- **Unit 08 (Astrophysics & Relativity):** Doppler effect — ensure intensity concepts introduced in Unit 03 are consistent with luminosity/intensity in Unit 08.
- **Unit 09 (Scientific Inquiry):** The computational model-building skills (translate physics to code, modify models) are exercised by the student fill-in exercise — this alignment is already strong.

### CAF Computational Physics alignment

The two CAF-suggested computational physics activities for Waves (simulate superposition of transverse waves; simulate formation of stationary wave) are both **COVERED** by the current unit. This is the strongest alignment point. The CAF §2.2.2 progression (lines 702–705) explicitly mentions "simulating superposition of wave" as a later-stage computational physics task — the unit is well-positioned here.