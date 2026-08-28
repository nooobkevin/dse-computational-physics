# Unit 01 Mechanics — Curriculum Alignment (CAF Consultation Draft)

## 1. Curriculum spec

Extracted from *Physics Curriculum (Secondary 4-6) — Consultation Draft, June 2026*, Topic "1. Mechanics" (lines 940–1349) and Annex 3 (lines 4237–4421).

### Content items and learning outcomes

#### a. Vector and scalar
- Describe change of position in terms of distance and displacement.
- Distinguish between vector and scalar quantities.
- Use scalars and vectors to represent physical quantities.

#### b. Kinematics
- Define velocity as rate of change of displacement: **v = Δs/Δt**.
- Define acceleration as rate of change of velocity: **a = Δv/Δt**.
- Define average speed (distance/time) and average velocity (displacement/time).
- Distinguish instantaneous vs average speed/velocity.
- Present information on s–t, v–t, a–t graphs for moving objects.
- Determine displacement, velocity, acceleration from motion graphs.
- Apply equations of uniformly accelerated motion:
  **v = u + at**, **s = ½(u+v)t**, **s = ut + ½at²**, **v² = u² + 2as**.
- Interpret uniform and uniformly accelerated motion using algebraic and graphical methods.
- State acceleration due to gravity of free-falling object is approximately constant near Earth surface.
- Estimate acceleration due to gravity experimentally.
- Solve problems involving vertical motion of free-falling objects.
- Describe the effect of air resistance on motion of objects falling under gravity.

#### c. Force and motion
- Use free-body diagrams to represent forces acting on objects.
- Find vector sum of coplanar forces graphically and algebraically.
- Resolve a force into components along two mutually perpendicular directions.
- Describe inertia and its relationship to mass.
- Describe situations using Newton's First Law (rest or uniform motion).
- Describe situations using Newton's Second Law (**F = ma**).
- State Newton's Third Law and identify action–reaction pairs.
- Apply Newton's Laws to solve problems involving motion in one dimension.
- Define moment of force as product of force and perpendicular distance from pivot.
- Describe effect of torque on a rigid body.
- State conditions for equilibrium of forces on a rigid body; solve problems with a fixed pivot.
- Interpret centre of gravity and determine it experimentally.

#### d. Work, energy and power
- Interpret mechanical work as energy transfer: **W = Fs cosθ**.
- Derive **KE = ½mv²** and **PE = mgh**.
- Define power as rate of energy transfer: **P = W/t**.
- State the law of conservation of energy.
- Define energy efficiency as (useful energy/power output) / (energy/power input); apply to problems.
- Solve problems involving mechanical work, rate of energy transfer, conservation of energy, and energy conversions with energy loss.

#### e. Momentum
- Realise momentum as quantity of motion: **p = mv**.
- Describe net force acting over time results in change in momentum (impulse).
- Relate net force to rate of change of momentum via Newton's Second Law.
- Describe law of conservation of momentum and relate to Newton's Third Law.
- Distinguish elastic and inelastic collisions.
- Solve problems involving momentum in one dimension.

#### f. Projectile motion
- Describe shape of path taken by a projectile launched horizontally or at an angle.
- Describe independence of horizontal and vertical motions.
- Solve problems involving projectile motion.

#### g. Periodic motion
- Define angular displacement θ using radian.
- Define angular velocity ω = Δθ/Δt.
- Relate tangential velocity to angular velocity: **v = rω**.
- Relate period, frequency, angular velocity: **T = 1/f = 2π/ω**.
- State centripetal acceleration as vector pointing towards centre: **a = v²/r = rω²**.
- Realise centripetal force as resultant force; solve problems.
- Define SHM as motion where acceleration a and displacement x satisfy **a ∝ −x**.
- Describe SHM in terms of displacement, velocity, acceleration, period, frequency.
- Present information on displacement–time graph for SHM.
- Identify SHM and forced oscillation; recognise damping and resonance in daily life.
- Relate displacement of SHM with angular frequency, amplitude, time using trigonometric functions; solve problems.
- *(Annex 3 enrichment)* Variation of displacement, velocity, and acceleration with time in SHM.
- *(Annex 3 enrichment)* Forced oscillation, damping, and resonance.

#### h. Gravitation
- State Newton's law of universal gravitation: **F = GMm/r²**.
- Define gravitational field strength as force per unit mass: **g = F/m**.
- Determine gravitational field strength at a point above a celestial body.
- Solve problems related to gravitational force, gravitational field, and circular orbits of celestial bodies.

### Key practical tasks
1. Determine velocity and acceleration of a moving object.
2. Find acceleration due to gravity of an object.
3. Examine the vector nature of forces.
4. Determine angular velocity of uniform circular motion (e.g. whirling rubber bung / rotating disc).

### Suggested learning and teaching activities
- Investigate factors affecting frictional force.
- Verify Newton's second law (**F = ma**) experimentally.
- Examine conservation of mechanical energy (toy roller coaster / simple pendulum).
- Determine output power of an electric motor.
- Estimate work for various tasks (lifting a book, stretching a spring, climbing Lantau Peak).
- Estimate KE of various moving objects (speeding car, sprinter, air molecule).
- Investigate conservation principles in energy transfer devices.
- Evaluate design of energy transfer devices (household appliances, lifts, escalators, bicycles).
- Measure change of momentum and force during a collision.
- Perform monkey-and-hunter experiment (independence of horizontal/vertical motion).
- Demonstrate SHM as projection of uniform circular motion.
- Find g using simple pendulum (**T = 2π√(L/g)**).
- Investigate factors affecting period of SHM.
- Demonstrate forced oscillation and resonance (Barton's pendulums, spring-mass with signal generator).
- Discuss applications of damping in daily life.
- Study Tacoma Narrows Bridge collapse (lack of damping against forced oscillations).
- Search natural phenomena using resonance.
- Use dimensional analysis to check Mechanics results.
- Challenge preconceived ideas (e.g. "zero" acceleration at max height, "zero" gravity in space shuttle).
- Contrast Newton's Laws with conservation laws in solving motion problems.

### Suggested Computational Physics activities
- Use motion video analysis (MVA) software or apps to analyse different kinds of motions.
- Use computer to program and simulate motions: free fall on different planets, projectile motion with or without air resistance, SHM with or without damping.

---

## 2. Coverage matrix

| Curriculum item | Status | Current artifact | Gap |
|---|---|---|---|
| **a. Vector and scalar** | MISSING | — | No artifact teaches vector/scalar distinction, vector representation, or distance vs displacement. |
| **b. Kinematics** — v = Δs/Δt, a = Δv/Δt | PARTIAL | Teacher app pendulum mode: θ-t graph (angular kinematics); `IntegratorConvergence`: x(t) trajectory comparison | Linear kinematics (s, v, a in 1D) not explicitly taught. Angular kinematics used as proxy. |
| **b. Kinematics** — motion graphs (s–t, v–t, a–t) | PARTIAL | Teacher app pendulum mode: θ-t graph, phase portrait (ω vs θ) | Only angular graphs; no linear s–t, v–t, a–t graphs. |
| **b. Kinematics** — equations of uniformly accelerated motion | MISSING | — | SUVAT equations not demonstrated or exercised. |
| **b. Kinematics** — vertical motion under gravity | PARTIAL | `ProjectileDt`: vertical motion component; teacher app projectile mode: height vs range | Vertical free-fall as isolated 1D case not covered. |
| **b. Kinematics** — air resistance | PARTIAL | `ReferenceProjectileSim` has `drag_coefficient` parameter (src/physics_core/mechanics/projectile.py line 220) | No artifact *teaches* air resistance — the engine supports it but no scene/app/exercise uses drag > 0. |
| **c. Force and motion** — free-body diagrams | MISSING | — | No artifact draws or analyses free-body diagrams. |
| **c. Force and motion** — addition/resolution of forces | PARTIAL | Teacher app projectile mode: vx/vy decomposition arrows | Force resolution not shown (velocity decomposition is a proxy). |
| **c. Force and motion** — Newton's Laws | MISSING | — | No artifact explicitly teaches F = ma, inertia, or action–reaction. |
| **c. Force and motion** — moment of force, torque, equilibrium, centre of gravity | MISSING | — | Not covered. |
| **d. Work, energy and power** — KE, PE, conservation of energy | PARTIAL | `IntegratorConvergence`: energy drift inset (E/E₀); `PendulumSim.energy()` method; `questions.md` Q(c) on energy drift | Work (W = Fs), power (P = W/t), efficiency not covered. |
| **d. Work, energy and power** — power and efficiency | MISSING | — | Not covered. |
| **e. Momentum** — p = mv, impulse, conservation, collisions | MISSING | — | No artifact covers momentum, impulse, or collisions. |
| **f. Projectile motion** — parabolic path, independence of horizontal/vertical | COVERED | `ProjectileDt` scene; teacher app projectile mode (vx/vy decomposition, height vs range graph) | — |
| **g. Periodic motion** — angular displacement/velocity, centripetal force | COVERED | Teacher app circular mode (ω, v, a_c vectors); `CircularMotion` engine | — |
| **g. Periodic motion** — SHM kinematics (displacement, velocity, acceleration, period, frequency) | PARTIAL | `ShmProjection` scene (displacement–time cosine trace); `IntegratorConvergence` (x(t) for SHM); pendulum exercise (period check) | Velocity–time and acceleration–time graphs for SHM not shown. |
| **g. Periodic motion** — SHM as projection of uniform circular motion | COVERED | `ShmProjection` scene (radius vector → cosine trace, phase markers) | — |
| **g. Periodic motion** — forced oscillation, damping, resonance *(Annex 3 enrichment)* | MISSING | — | NEW-IN-CAF: enrichment requires damping and resonance demonstrations. Engine has no damping model for pendulum/SHM. |
| **g. Periodic motion** — variation of displacement, velocity, acceleration with time *(Annex 3 enrichment)* | PARTIAL | `ShmProjection` shows displacement–time only | NEW-IN-CAF: enrichment requires v(t) and a(t) graphs alongside x(t). |
| **h. Gravitation** — Newton's law, gravitational field, circular orbits | MISSING | — | Not covered (orbital motion moved to "Physics and Engineering" per Annex 3 integration, but gravitational field still in Mechanics). |
| **Key practical: determine v and a of moving object** | PARTIAL | Teacher app pendulum mode: ω from θ difference, g from period | Linear v and a not measured. |
| **Key practical: find g experimentally** | COVERED | Teacher app pendulum mode: g estimated from measured period, percent error vs 9.81 | — |
| **Key practical: vector nature of forces** | MISSING | — | Not covered. |
| **Key practical: angular velocity of circular motion** | COVERED | Teacher app circular mode: ω displayed | — |
| **CP activity: motion video analysis** | MISSING | — | No MVA integration (teacher app uses webcam for pendulum tracking but is not framed as MVA). |
| **CP activity: simulate free fall on different planets** | MISSING | — | Engine supports variable g but no artifact varies planet gravity. |
| **CP activity: projectile with/without air resistance** | PARTIAL | Engine has drag; no artifact uses it | Easy win: add drag toggle to projectile mode. |
| **CP activity: SHM with/without damping** | MISSING | — | No damping model in engine or artifacts. |
| **Suggested activity: monkey-and-hunter experiment** | MISSING | — | Not implemented. |
| **Suggested activity: find g using pendulum (T = 2π√(L/g))** | COVERED | Teacher app pendulum mode; pendulum exercise period check | — |
| **Suggested activity: forced oscillation and resonance** | MISSING | — | NEW-IN-CAF enrichment. |
| **Suggested activity: damping applications / Tacoma Narrows** | MISSING | — | NEW-IN-CAF enrichment. |

---

## 3. Required actions (prioritised)

### P1 — Critical gaps (core curriculum items with no coverage)

1. **Add momentum module to physics_core and unit 01**
   - **What**: New `src/physics_core/mechanics/momentum.py` with `CollisionSim` (1D elastic/inelastic, impulse calculation). New Manim scene `ElasticCollision` (two carts colliding, momentum bars). New teacher app mode `--mode collision`. New student exercise (fill in momentum conservation).
   - **Files**: `src/physics_core/mechanics/momentum.py`, `units/01_mechanics/manim/scenes/elastic_collision.py`, `units/01_mechanics/teacher_app/main.py` (add mode), `units/01_mechanics/exercises/collision_exercise.py`, `units/01_mechanics/exercises/test_collision.py`
   - **Physics**: p = mv, impulse = FΔt, conservation of momentum, elastic vs inelastic collisions (CAF item e, lines 1147–1165).
   - **API reuse**: `euler_step`/`verlet_step` from `integrators.py`; `percent_error` from `errors.py`.
   - **Effort**: L
   - **Rationale**: CAF item e (Momentum) is entirely missing — 6 learning outcomes with zero coverage.

2. **Add force-and-motion module (Newton's Laws, free-body diagrams)**
   - **What**: New teacher app mode `--mode forces` showing a block on a surface with applied force, friction, normal reaction, weight vectors. Animated free-body diagram. Student exercise to compute net force and acceleration.
   - **Files**: `units/01_mechanics/teacher_app/forces.py`, `units/01_mechanics/teacher_app/main.py` (add mode), `units/01_mechanics/exercises/forces_exercise.py`
   - **Physics**: Free-body diagrams, vector addition/resolution, F = ma, Newton's Third Law (CAF item c, lines 1061–1112).
   - **API reuse**: No new engine needed — use numpy vector ops.
   - **Effort**: M
   - **Rationale**: CAF item c has 12 learning outcomes; only velocity decomposition (a proxy) is partially covered.

3. **Add work-energy-power module**
   - **What**: New Manim scene `WorkEnergy` (force–displacement graph, area = work). Teacher app mode `--mode energy` showing KE/PE bar charts for pendulum/projectile. Extend `questions.md` with power and efficiency problems.
   - **Files**: `units/01_mechanics/manim/scenes/work_energy.py`, `units/01_mechanics/teacher_app/energy.py`, `units/01_mechanics/exercises/energy_exercise.py`
   - **Physics**: W = Fs cosθ, KE = ½mv², PE = mgh, P = W/t, efficiency (CAF item d, lines 1116–1142).
   - **API reuse**: `PendulumSim.energy()` already returns KE/PE/total; `ReferenceProjectileSim` has position/velocity.
   - **Effort**: M
   - **Rationale**: CAF item d has 6 outcomes; only energy conservation is partially covered.

### P2 — Enrichment gaps (Annex 3 additions)

4. **Add damping to pendulum/SHM engine and artifacts**
   - **What**: Add `damping_coefficient` parameter to `PendulumSim.__init__`; modify `angular_acceleration` to include `-b·ω` term when damping > 0. New Manim scene `DampedSHM` (underdamped, critically damped, overdamped comparison). Teacher app pendulum mode: damping toggle. Student exercise: measure damping ratio.
   - **Files**: `src/physics_core/mechanics/pendulum.py` (add damping), `units/01_mechanics/manim/scenes/damped_shm.py`, `units/01_mechanics/teacher_app/main.py` (damping toggle), `units/01_mechanics/exercises/damping_exercise.py`
   - **Physics**: Damping term −b·ω, underdamped/critical/overdamped regimes, energy dissipation (Annex 3 enrichment: forced oscillation, damping, resonance, lines 4377–4380).
   - **API reuse**: `verlet_step` works unchanged; `energy()` method already tracks total energy.
   - **Effort**: M
   - **Rationale**: NEW-IN-CAF enrichment — explicit requirement for damping and resonance.

5. **Add forced oscillation and resonance demonstration**
   - **What**: New Manim scene `ForcedOscillation` (driven oscillator with variable driving frequency, amplitude vs frequency curve showing resonance peak). Teacher app mode `--mode resonance` with interactive frequency slider.
   - **Files**: `units/01_mechanics/manim/scenes/forced_oscillation.py`, `units/01_mechanics/teacher_app/resonance.py`
   - **Physics**: Forced oscillation, resonance condition ω_drive ≈ ω_natural, amplitude response curve (Annex 3 enrichment, lines 4377–4380).
   - **API reuse**: Extend `PendulumSim` with driving term `A·cos(ω_d·t)`.
   - **Effort**: M
   - **Rationale**: NEW-IN-CAF enrichment; also supports suggested activity "demonstrate forced oscillation and resonance" (line 1300).

6. **Add SHM velocity–time and acceleration–time graphs to ShmProjection**
   - **What**: Extend `ShmProjection` scene to show three stacked graphs: x(t), v(t), a(t) for SHM, with the rotating radius vector driving all three simultaneously.
   - **Files**: `units/01_mechanics/manim/scenes/shm_projection.py`
   - **Physics**: x = A cos(ωt), v = −Aω sin(ωt), a = −Aω² cos(ωt) (Annex 3 enrichment: variation of displacement, velocity, acceleration with time, line 4379).
   - **API reuse**: `CircularMotion` engine; analytical derivatives.
   - **Effort**: S
   - **Rationale**: NEW-IN-CAF enrichment — minimal code change for significant curriculum gain.

### P3 — Enhancement gaps (existing partial coverage)

7. **Add air-resistance toggle to projectile artifacts**
   - **What**: Teacher app projectile mode: checkbox or key toggle to enable drag (use `drag_coefficient` param). `ProjectileDt` scene: add a damped trajectory trace. Student exercise: compare range with/without drag.
   - **Files**: `units/01_mechanics/teacher_app/main.py` (projectile mode), `units/01_mechanics/manim/scenes/projectile_dt.py`, `units/01_mechanics/exercises/projectile_drag_exercise.py`
   - **Physics**: Linear drag, reduced range, terminal velocity (CAF item b: "describe the effect of air resistance", line 1054; CP activity: projectile with air resistance, line 1318).
   - **API reuse**: `ReferenceProjectileSim(drag_coefficient=...)` already exists.
   - **Effort**: S
   - **Rationale**: Engine already supports drag — zero new physics_core work.

8. **Add free-fall-on-different-planets scene**
   - **What**: New Manim scene `PlanetFreeFall` showing objects dropped simultaneously on Earth, Moon, Mars with different g values. Teacher app mode `--mode freefall` with planet selector.
   - **Files**: `units/01_mechanics/manim/scenes/planet_freefall.py`, `units/01_mechanics/teacher_app/freefall.py`
   - **Physics**: g varies by planet; constant acceleration near surface; motion graphs (CAF CP activity: free fall on different planets, line 1317).
   - **API reuse**: `ReferenceProjectileSim(g=...)` or new simple `FreeFallSim` using `euler_step`.
   - **Effort**: S
   - **Rationale**: Explicitly named in CAF CP activities; easy win.

9. **Add kinematics SUVAT exercise**
   - **What**: Student exercise with auto-grader for 1D kinematics: compute displacement, velocity, acceleration from motion graphs; apply SUVAT equations.
   - **Files**: `units/01_mechanics/exercises/kinematics_exercise.py`, `units/01_mechanics/exercises/test_kinematics.py`
   - **Physics**: v = u + at, s = ½(u+v)t, s = ut + ½at², v² = u² + 2as; s–t, v–t, a–t graph interpretation (CAF item b, lines 991–1056).
   - **API reuse**: No engine needed — pure algebra.
   - **Effort**: S
   - **Rationale**: Core kinematics item with 15+ outcomes, zero coverage.

10. **Add vector/scalar concept exercise**
    - **What**: Short student exercise distinguishing vectors from scalars, representing quantities, calculating displacement from path.
    - **Files**: `units/01_mechanics/exercises/vectors_exercise.py`
    - **Physics**: Distance vs displacement, vector vs scalar (CAF item a, lines 981–987).
    - **API reuse**: None needed.
    - **Effort**: S
    - **Rationale**: Smallest gap to close — 3 outcomes, minimal code.

---

## 4. Notes

### Ambiguities
- **Gravitation (item h)** remains in the Mechanics topic (lines 1244–1262) even though Annex 3 integration (line 4250) states "orbital motion under gravity is incorporated into Physics and Engineering". The Mechanics topic still lists gravitational force, field strength, and circular orbits. The unit should cover gravitational field (g = F/m) but can defer orbital mechanics to Unit 05.
- **Moment of force / torque / equilibrium (item c)** is listed under Mechanics but overlaps with content that could be taught in Physics and Engineering. The CAF does not remove it from Mechanics, so it must be covered here.
- **"Motion video analysis"** is listed as a CP activity (line 1316) but the teacher app's webcam pendulum tracking already performs real-time video analysis — it is simply not labelled as MVA. Reframing the existing feature may suffice.

### What the current unit teaches that the new CAF removed
- Nothing. Annex 3 lists no deletions from the Mechanics topic. All current unit content remains valid.

### Risks
- **Scope creep**: Adding momentum, forces, work-energy, damping, resonance, and gravitation would roughly double the unit's artifact count. Consider splitting into sub-units (01a Core Mechanics, 01b Extended Mechanics) or deferring momentum/gravitation to later units.
- **Engine coupling**: Damping requires modifying `PendulumSim.angular_acceleration` signature or adding a new hook — this affects all three front-ends. Must be done carefully to avoid breaking existing scenes and the student exercise.
- **Resonance complexity**: Forced oscillation with a driving term changes the ODE from autonomous to non-autonomous. The current `verlet_step` handles time-dependent derivatives (the `t` parameter is passed), so this is feasible, but the student exercise would need careful scaffolding.
- **Gravitation overlap with Unit 05**: If orbital motion is taught in "Physics and Engineering", the Mechanics unit should cover only gravitational field strength (g = F/m) and Newton's law, not Kepler's laws or orbital mechanics.