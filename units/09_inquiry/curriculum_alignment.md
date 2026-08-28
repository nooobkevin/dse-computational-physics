# Unit 09 Scientific Inquiry in Physics — Curriculum Alignment (CAF Consultation Draft)

## 1. Curriculum Spec

### 1.1 Overview (lines 3150–3159)

Topic 9 replaces the former "Investigative Study". A portion of lesson time is
allocated for developing scientific inquiry skills through practical tasks and
scientific investigations / engineering design activities. Computational Physics
should be implemented in connection with these tasks. Students are expected to
value the importance of using digital tools and AI critically and responsibly.

### 1.2 Time allocation (lines 3186–3220)

- **16 lesson hours total** — no core/extension split.
- At least **8 hands-on practical tasks** performed by students.
- At least **1 scientific investigation OR engineering design activity**.
- Practical tasks: ~80 minutes each.
- Investigation/design activity: ~240 minutes.

### 1.3 Learning targets (lines 3192–3200)

| Domain | Sub-skills |
|---|---|
| **Scientific Inquiry** | Laboratory Technique, Data Analysis, Order of Accuracy and Error Treatment, Awareness of Safety |
| **Computational Physics** | Building Computational Models, Computer-Assisted Data Analysis |

### 1.4 Process outcomes (lines 3202–3214)

**Practical tasks:** Prepare experiment → Use apparatus/computational tools →
Complete assignments/reports.

**Scientific investigation:** Develop and justify investigation plan → Implement
plan → Analyse preliminary data and refine plan → Report results and error
analysis.

**Engineering design:** Define problem and design solutions → Develop prototypes
and conduct scientific tests → Analyse data to determine optimal setting →
Improve prototype based on analysed data.

### 1.5 Student capabilities (lines 3168–3180)

Students should be able to:
- Develop an investigation plan and justify its appropriateness
- Suggest improvements for validity/reliability (investigation) or
  effectiveness/efficiency (product)
- Use accurate terminologies and appropriate reporting styles
- Use digital tools (data-loggers, sensors, spreadsheets, graphing software, AI)
  to collect, process, interpret data, search for/organise information, and
  evaluate reliability/accuracy of digital/AI outputs
- Evaluate validity of conclusions with reference to investigation process and
  data gathered

### 1.6 Suggested investigation topics (lines 3255–3266)

Cooling rate, uniform vs uniformly accelerated motion, terminal velocity,
projectile motion parameters, solar cell efficiency, celestial distance, radio
signals from celestial bodies, programming SHM simulation with damping,
programming complex systems (forest fire, disease spread, crowd control).

### 1.7 Suggested engineering design topics (lines 3280–3292)

Pendulum clock, solar cooker, water rocket, antenna, robotic system with
sensors, wind turbine, renewable energy powered system, parking alarm with
sonic sensor + micro-computing, smart devices with infrared sensor.

### 1.8 Computational Physics — Computer-Assisted Data Analysis (lines 659–690)

Students should be able to:
- Collect, import, organise raw experimental/simulated data into digital formats
- Prepare datasets: unit conversions, derived quantities, outlier handling,
  error estimation
- Create and fit graphical representations: linear plots, trendlines with
  displayed equations
- Interpret graphical outputs: slope, intercept, physical significance,
  impact of uncertainties and errors

### 1.9 Computational Physics — Building Computational Models (lines 616–653)

Students should be able to:
- Translate physics into computer program code
- Build algorithms using conditional logic
- Develop/use computational models to simulate or predict physical phenomena
- Modify models in response to new evidence or by introducing complexity
- Explore numerical methods: Finite Difference method, Monte Carlo method

### 1.10 Scientific Inquiry Skills (lines 490–565)

**Experiment Techniques:** calibrate apparatus, make preliminary measurements,
read scales to max accuracy, make alignments/locate peak values, connect/check
electrical circuits.

**Data Analysis:** SI base units, derive units, handle/display data in tabular
and graphical form, plot graph/fit curve with suitable scales, transform
formulae into linear graphs (1/x, 1/x², etc.), interpret physical meaning from
graphs (intercepts, slope, area).

**Order of Accuracy and Error Treatment:** repeat measurements, identify
outliers, quote results with significant figures, identify absolute/relative/
percentage error, estimate maximum error, appreciate order of magnitude.

**Awareness of Safety:** (general lab safety).

---

## 2. Coverage Matrix

| # | Curriculum item | Status | Current artifact | Gap |
|---|---|---|---|---|
| **Scientific Inquiry — Learning Targets** | | | | |
| 1 | Laboratory Technique | **MISSING** | None | No content on apparatus calibration, scale reading, circuit connection, preliminary measurements |
| 2 | Data Analysis (general) | **PARTIAL** | Manim Linearisation, Teacher app analysis/experiment, Student exercise | Covers linearisation and fitting well; missing tabular display, choosing scales, 1/x and 1/x² transforms |
| 3 | Order of Accuracy and Error Treatment | **PARTIAL** | Manim Uncertainty, Teacher app (percent error, uncertainty propagation), Concept questions (d, e) | Covers percent error and propagation; missing repeat measurements, outlier identification, sig figs depth, maximum error estimation |
| 4 | Awareness of Safety | **MISSING** | None | Not addressed anywhere |
| **Computational Physics — Learning Targets** | | | | |
| 5 | Building Computational Models | **PARTIAL** | Student exercise (implement `model()` method) | Only linear fit; missing conditional logic, Monte Carlo, Finite Difference, model modification |
| 6 | Computer-Assisted Data Analysis | **PARTIAL** | Teacher app (fit + display), Student exercise (fit), Manim (linearisation) | Covers fitting and interpretation; missing data import/export, outlier handling, unit conversions, real data sources |
| **Process — Practical Tasks** | | | | |
| 7 | Prepare the experiment | **MISSING** | None | No content on experimental setup, apparatus selection, preliminary measurements |
| 8 | Use apparatus/computational tools to conduct experiment | **PARTIAL** | Teacher app (synthetic data generation) | Synthetic only; no real apparatus, data-loggers, sensors, MVA, SDR, mobile apps |
| 9 | Complete assignments/reports | **MISSING** | None | No report template, rubric, or reporting guidance |
| **Process — Scientific Investigation** | | | | |
| 10 | Develop and justify investigation plan | **MISSING** | None | No scaffold for planning an investigation |
| 11 | Implement investigation plan | **MISSING** | None | No structured investigation workflow |
| 12 | Analyse preliminary data and refine plan | **MISSING** | None | No iterative refinement cycle |
| 13 | Report results and error analysis | **PARTIAL** | Concept questions (f) | Questions touch on evaluation but no formal report structure |
| **Process — Engineering Design** | | | | |
| 14 | Define problem and design solutions | **MISSING** | None | Entire engineering design strand absent |
| 15 | Develop prototypes and conduct scientific tests | **MISSING** | None | No prototyping or testing |
| 16 | Analyse data to determine optimal setting | **MISSING** | None | No optimisation workflow |
| 17 | Improve prototype based on analysed data | **MISSING** | None | No iteration cycle |
| **Student Capabilities** | | | | |
| 18 | Develop investigation plan, justify appropriateness | **MISSING** | None | Not covered |
| 19 | Suggest improvements for validity/reliability | **PARTIAL** | Concept questions (f) | Questions ask for improvements but no systematic treatment |
| 20 | Use accurate terminologies and reporting styles | **MISSING** | None | No reporting guidance |
| 21 | Use digital tools (data-loggers, sensors, spreadsheets, AI) | **MISSING** | None | All data is synthetic; no real digital tool integration |
| 22 | Evaluate reliability/accuracy of digital/AI outputs | **MISSING** | None | AI evaluation not addressed |
| 23 | Evaluate validity of conclusions | **PARTIAL** | Manim Conclusion, Concept questions (f) | Inquiry loop shown; evaluation questions exist but shallow |
| **Suggested Investigation Topics** | | | | |
| 24 | Factors affecting rate of cooling | **MISSING** | None | Not implemented |
| 25 | Uniform vs uniformly accelerating motion | **MISSING** | None | Not implemented |
| 26 | Estimating terminal velocity | **MISSING** | None | Not implemented |
| 27 | Projectile motion parameters | **MISSING** | None | Not implemented |
| 28 | Factors affecting solar cell efficiency | **MISSING** | None | Not implemented |
| 29 | Distance of celestial object from Earth | **MISSING** | None | Not implemented |
| 30 | Analysing radio signals from celestial bodies | **MISSING** | None | Not implemented |
| 31 | Programming SHM simulation + damping factor | **MISSING** | None | Not implemented (note: unit 01 has SHM but not in inquiry context) |
| 32 | Programming complex systems (forest fire, disease, crowd) | **MISSING** | None | Not implemented |
| **Suggested Engineering Design Topics** | | | | |
| 33 | Pendulum clock for specific period | **MISSING** | None | Not implemented |
| 34 | Solar cooker performance | **MISSING** | None | Not implemented |
| 35 | Water rocket (height, accuracy, parachute) | **MISSING** | None | Not implemented |
| 36 | Antenna for radio signal | **MISSING** | None | Not implemented |
| 37 | Robotic system with sensors | **MISSING** | None | Not implemented |
| 38 | Wind turbine to generate electricity | **MISSING** | None | Not implemented |
| 39 | Renewable energy powered system | **MISSING** | None | Not implemented |
| 40 | Parking alarm with sonic sensor + micro-computing | **MISSING** | None | Not implemented |
| 41 | Smart devices for smart home/campus | **MISSING** | None | Not implemented |
| **Scientific Inquiry Skills (2.2.1)** | | | | |
| 42 | Calibrate apparatus before measurements | **MISSING** | None | Not covered |
| 43 | Make rough preliminary measurements | **MISSING** | None | Not covered |
| 44 | Read scales to maximum accuracy | **MISSING** | None | Not covered |
| 45 | Make alignments / locate peak values | **MISSING** | None | Not covered |
| 46 | Connect and check electrical circuits | **MISSING** | None | Not covered |
| 47 | SI base units and derived units | **MISSING** | None | Not covered |
| 48 | Handle data in tabular and graphical form | **PARTIAL** | Teacher app (scatter plot display) | Only scatter plots; no table construction |
| 49 | Plot graph/fit curve with suitable scales | **PARTIAL** | Teacher app (auto-scaled plots) | Auto-scaling hides the skill of choosing scales |
| 50 | Transform formulae into linear graphs (1/x, 1/x²) | **PARTIAL** | Manim Linearisation (T² vs L only) | Only one linearisation type; missing 1/x, 1/x², log transforms |
| 51 | Interpret physical meaning from graphs | **COVERED** | Manim Linearisation, Teacher app, Concept questions (b, c) | Slope → physical constant well covered |
| 52 | Repeat measurements and identify outliers | **MISSING** | None | Not covered |
| 53 | Quote results with significant figures | **PARTIAL** | Teacher app uses `sig_figs()` | Displayed but not taught as a skill |
| 54 | Identify absolute/relative/percentage error | **COVERED** | `percent_error()` in all artifacts | Well covered |
| 55 | Estimate maximum error in simple cases | **MISSING** | None | Not covered |
| 56 | Appreciate order of magnitude and accuracy | **MISSING** | None | Not covered |
| **Computer-Assisted Data Analysis (2.2.2)** | | | | |
| 57 | Collect/import/organise data into digital formats | **MISSING** | None | All data synthetic; no import workflow |
| 58 | Unit conversions, derived quantities, outlier handling | **MISSING** | None | Not covered |
| 59 | Create/fit graphical representations with trendlines | **COVERED** | Teacher app, Student exercise | Well covered for linear fits |
| 60 | Interpret graphical outputs (slope, intercept, uncertainty impact) | **COVERED** | Manim, Teacher app, Concept questions | Well covered |
| **Building Computational Models (2.2.2)** | | | | |
| 61 | Translate physics into program code | **PARTIAL** | Student exercise (implement `model()`) | Only one small translation task |
| 62 | Build algorithms using conditional logic | **MISSING** | None | Not covered |
| 63 | Develop/use models to simulate/predict phenomena | **PARTIAL** | Student exercise (linear fit predicts y) | Very narrow scope |
| 64 | Modify model in response to new evidence | **MISSING** | None | Not covered |
| 65 | Finite Difference method | **MISSING** | None | Not covered (exists in unit 01 integrators but not in inquiry context) |
| 66 | Monte Carlo method | **MISSING** | None | Not covered (exists in unit 06 but not in inquiry context) |

---

## 3. Required Actions (Prioritised)

### P1 — Critical gaps (missing core curriculum requirements)

**1. Add Engineering Design module**
- **What:** Create a new teacher app mode (`--mode design`) and corresponding
  Manim scene for the engineering design cycle (Define → Design → Prototype →
  Test → Analyse → Improve). Start with one concrete topic (e.g. water rocket
  optimisation or pendulum clock).
- **Files:** `teacher_app/main.py` (new mode), `manim/scenes/engineering_design.py`,
  `exercises/design_exercise.py`, `exercises/test_design.py`
- **Physics content:** Engineering design cycle, optimisation, trade-off
  analysis, iterative improvement
- **Reusable API:** `physics_core.inquiry.analysis` (existing fit/error tools);
  may need new `physics_core.inquiry.design` module for design metrics
- **Effort:** L (large — new sub-unit)
- **CAF citation:** lines 3269–3292 (engineering design process + suggested
  topics); lines 3202–3214 (engineering design process outcomes)

**2. Add Laboratory Technique content**
- **What:** Create concept questions and a teacher-app mode that demonstrates
  apparatus calibration, scale reading, and preliminary measurements. Add a
  Manim scene showing how to read a vernier caliper / ruler / protractor to
  maximum accuracy.
- **Files:** `exercises/questions.md` (new section), `manim/scenes/lab_technique.py`,
  `teacher_app/main.py` (new `--mode technique`)
- **Physics content:** Calibration, significant figures from instrument
  precision, parallax error, preliminary range-finding
- **Reusable API:** `physics_core.errors.sig_figs` (already exists)
- **Effort:** M (medium)
- **CAF citation:** lines 507–515 (experiment techniques i–v); lines 536–543
  (order of accuracy and error treatment i–v)

**3. Add Awareness of Safety content**
- **What:** Add safety briefing slides to the Conclusion Manim scene or as a
  standalone scene. Include safety symbols, lab rules, risk assessment
  principles.
- **Files:** `manim/scenes/conclusion.py` (extend) or new `manim/scenes/safety.py`
- **Physics content:** Lab safety, risk assessment, hazard symbols
- **Reusable API:** None needed
- **Effort:** S (small — text-based scene)
- **CAF citation:** line 3195 (Awareness of Safety learning target)

**4. Add Scientific Investigation planning workflow**
- **What:** Create a structured investigation-plan template and a teacher-app
  mode that guides students through: define question → identify variables →
  plan procedure → predict outcomes → collect data → analyse → conclude →
  evaluate. The Manim Conclusion scene already shows the loop; extend it with
  an interactive version.
- **Files:** `teacher_app/main.py` (new `--mode investigate`),
  `exercises/investigation_plan.md` (template), `manim/scenes/conclusion.py`
  (extend with planning detail)
- **Physics content:** Hypothesis formulation, variable identification,
  controlled experiment design, prediction
- **Reusable API:** `physics_core.inquiry.analysis` (for the analysis step)
- **Effort:** M (medium)
- **CAF citation:** lines 3168–3180 (student capabilities); lines 3202–3214
  (investigation process); lines 3240–3251 (scientific investigation approach)

### P2 — Important extensions (partial coverage needs deepening)

**5. Expand Computer-Assisted Data Analysis to include real data sources**
- **What:** Add a teacher-app mode that imports CSV data (simulating data-logger
  output), performs unit conversions, identifies outliers, and fits a model.
  Add a Manim scene showing outlier detection (e.g. Chauvenet's criterion or
  IQR method).
- **Files:** `teacher_app/main.py` (new `--mode import`),
  `manim/scenes/outliers.py`, sample CSV files in `units/09_inquiry/data/`
- **Physics content:** Data import/export, unit conversion, outlier
  identification, data cleaning
- **Reusable API:** `physics_core.inquiry.analysis` (existing fit);
  `physics_core.errors` (sig figs)
- **Effort:** M (medium)
- **CAF citation:** lines 671–682 (computer-assisted data analysis outcomes);
  lines 684–690 (open data, MVA, SDR, mobile apps)

**6. Add multiple linearisation types**
- **What:** Extend the Linearisation Manim scene to show 1/x (for xy=constant),
  1/x² (for inverse square law), and log-log transforms. Add corresponding
  concept questions.
- **Files:** `manim/scenes/linearisation.py` (extend), `exercises/questions.md`
  (new questions)
- **Physics content:** Inverse relationships, inverse square law, power laws,
  logarithmic relationships
- **Reusable API:** `physics_core.inquiry.analysis` (unchanged — same linear
  fit on transformed data)
- **Effort:** S (small — extend existing scene)
- **CAF citation:** lines 527–532 (transform formulae into linear graphs);
  lines 534–535 (interpret physical meaning)

**7. Add significant figures and maximum error estimation**
- **What:** Create a Manim scene or concept-question section on significant
  figures: how to determine sig figs from instrument precision, how to quote
  results, how to estimate maximum error from instrument specifications.
- **Files:** `manim/scenes/uncertainty.py` (extend) or new
  `manim/scenes/sig_figs.py`, `exercises/questions.md` (new section)
- **Physics content:** Significant figures, decimal places, absolute error,
  maximum error estimation, order-of-magnitude appreciation
- **Reusable API:** `physics_core.errors.sig_figs` (already exists)
- **Effort:** S (small)
- **CAF citation:** lines 537–543 (order of accuracy and error treatment i–v)

**8. Add repeat measurements and outlier handling**
- **What:** Extend the Uncertainty scene to show multiple trials at each data
  point, mean ± std, and outlier flagging. Add a teacher-app mode that
  generates repeated measurements and computes statistics.
- **Files:** `manim/scenes/uncertainty.py` (extend), `teacher_app/main.py`
  (extend experiment mode)
- **Physics content:** Repeat measurements, mean, standard deviation, outlier
  identification, random vs systematic error
- **Reusable API:** `physics_core.inquiry.analysis` (propagate_uncertainty)
- **Effort:** S (small)
- **CAF citation:** line 537 (repeat measurements and identify outliers)

### P3 — Enhancement opportunities (suggested topics not yet implemented)

**9. Add one complex systems simulation (forest fire / disease spread)**
- **What:** Implement a cellular automaton simulation as a teacher-app mode and
  Manim scene. Students modify parameters (infection rate, recovery rate,
  population density) and observe emergent behaviour.
- **Files:** `teacher_app/main.py` (new `--mode epidemic`),
  `manim/scenes/complex_systems.py`, `exercises/epidemic_exercise.py`
- **Physics content:** Emergent phenomena, complex systems, computational
  modelling, parameter sensitivity
- **Reusable API:** New `physics_core.inquiry.complex` module (cellular
  automaton engine)
- **Effort:** L (large — new engine + three artifacts)
- **CAF citation:** lines 3263–3266 (programming complex systems)

**10. Add SHM simulation with damping investigation**
- **What:** Implement a SHM simulation where students vary damping coefficient
  and observe the effect on oscillation. Teacher app shows phase-space plots.
- **Files:** `teacher_app/main.py` (new `--mode shm`),
  `manim/scenes/shm_damping.py`, `exercises/shm_exercise.py`
- **Physics content:** Simple harmonic motion, damping coefficient, underdamped
  vs critically damped vs overdamped
- **Reusable API:** `physics_core.mechanics.pendulum` (existing SHM engine)
- **Effort:** M (medium — reuses existing physics_core)
- **CAF citation:** line 3262 (programming SHM simulation and damping factor)

**11. Add digital tools / AI evaluation content**
- **What:** Create concept questions and a teacher-app mode that demonstrates
  using AI to analyse data (e.g. comparing AI-generated fit vs student fit),
  and evaluating the reliability and accuracy of AI outputs.
- **Files:** `exercises/questions.md` (new section), `teacher_app/main.py`
  (new `--mode ai-eval`)
- **Physics content:** AI literacy, critical evaluation of digital tools,
  limitations of automated analysis
- **Reusable API:** None needed (conceptual)
- **Effort:** S (small)
- **CAF citation:** lines 3156–3159 (using AI critically and responsibly);
  lines 3175–3178 (evaluate reliability of digital/AI outputs)

**12. Add reporting and communication scaffold**
- **What:** Create a lab-report template (Markdown/LaTeX) with sections:
  Objective, Method, Data, Analysis, Conclusion, Evaluation. Include
  exemplar reports for the pendulum and free-fall experiments.
- **Files:** `exercises/report_template.md`, `exercises/report_exemplar.md`
- **Physics content:** Scientific communication, appropriate terminology,
  evidence-based argumentation
- **Reusable API:** None needed
- **Effort:** S (small)
- **CAF citation:** lines 3173–3174 (accurate terminologies and appropriate
  reporting styles)

---

## 4. Notes

### Ambiguities

1. **Scope of "at least 8 practical tasks"**: The curriculum states teachers
   should arrange at least 8 practical tasks across *all* topics, not just
   within Unit 09. The toolkit's other units (01–08) each contain practical
   tasks. Unit 09's role is to provide the *inquiry framework* that those
   tasks use. The alignment document assumes Unit 09 provides the methodology,
   not all 8 tasks.

2. **Relationship to SBA**: The curriculum defers SBA details to the
   Assessment Guide (not yet available in the consultation draft). The
   engineering design and investigation requirements may change when the
   Assessment Guide is published.

3. **"No core/extension split"**: Unlike other topics, Unit 09 has no
   core/extension distinction. All 16 hours are core. This means all content
   must be accessible to all students — the engineering design and
   computational model-building activities must have low-floor entry points.

4. **Integration vs standalone**: The curriculum says teachers "select and
   integrate [inquiry elements] into practical activities across different
   topics" (Annex 3, lines 4412–4416). Unit 09 could be taught as a standalone
   methodology unit early in S4, with the skills then applied in later units.
   The current implementation treats it as standalone, which is one valid
   interpretation.

### Risks

1. **Engineering design is a hard gap**: The entire engineering design strand
   (defining problems, prototyping, testing, improving) is absent. This is the
   single biggest risk because the CAF explicitly introduces it as a new
   requirement replacing the old "Investigative Study". Without it, the unit
   does not satisfy the curriculum.

2. **Synthetic-only data limits authenticity**: The curriculum emphasises
   real data collection (data-loggers, sensors, MVA, SDR, mobile apps). The
   current synthetic-only approach is a deliberate design choice for
   portability, but it means students never practice data collection from real
   instruments. Teachers must supplement with real lab work.

3. **AI evaluation requirement is new and underspecified**: The curriculum
   requires students to "evaluate the reliability and scientific accuracy of
   digital and AI-generated outputs" (line 3177–3178). This is a novel
   requirement with no precedent in the old curriculum. The toolkit needs to
   develop a pedagogical approach for this.

4. **Computational model-building scope is narrow**: The curriculum expects
   students to "translate physics into code", "build algorithms with
   conditional logic", and "modify the model in response to new evidence"
   (lines 629–632). The current student exercise (implementing one linear
   model method) is far too narrow to meet these outcomes.

5. **16 hours is tight**: With 8+ practical tasks and 1+ investigation/design
   activity, 16 hours leaves little room for deep computational work. The
   toolkit's three-artifact approach (watch → interact → code) is efficient
   but may still need prioritisation.

### Current strengths worth preserving

- The **three-artifact pattern** (Manim + teacher app + student exercise)
  maps well to the curriculum's "watch → do → analyse" progression.
- The **physics_core inquiry engine** (`LinearFit` / `ReferenceLinearFit`)
  correctly follows the abstract-base pattern and is reusable across all
  planned extensions.
- The **concept questions** cover variable identification, linearisation,
  percent error, systematic vs random error, and evaluation — a solid
  foundation.
- The **auto-grader** tests numerical behaviour (not source-code matching),
  which is robust and scalable.