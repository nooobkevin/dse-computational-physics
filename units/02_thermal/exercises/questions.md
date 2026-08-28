# Gas Simulation Exercise — Concept Questions (M5)

These questions test your understanding of the physics behind the gas
simulation you just implemented.  Answer them in a few sentences each.

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

### (c) Pressure from collisions

Pressure in an ideal gas arises from particles colliding with the walls
of the container.

1. Explain in words how a single particle hitting a wall transfers
   momentum.  How much momentum is transferred per collision?
2. If you double the number of particles *N* (keeping the box size and
   temperature constant), what happens to the pressure?  Why?
3. If you double the box side length *L* (keeping *N* and *T* constant),
   what happens to the pressure?  Why?

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

### (e) Verlet vs Euler energy conservation

Your simulation uses the Velocity-Verlet integration scheme.

1. For a single free particle (no collisions), why does Verlet conserve
   kinetic energy exactly?
2. What would happen if you used Explicit Euler instead?  Would the
   kinetic energy still be conserved?
3. When a particle bounces off a wall, is the collision handled by the
   integrator or by the collision hook?  Does the energy remain exactly
   conserved after a wall bounce?

### (f) 2D vs 3D

The Maxwell-Boltzmann distribution has a different functional form in
2D vs 3D.

1. Write down the 2D and 3D Maxwell-Boltzmann speed distributions.
2. How does the number of degrees of freedom affect the relationship
   between temperature and average kinetic energy?
3. If you ran your simulation in 3D instead of 2D, would the pressure
   be higher or lower for the same *N*, *T*, and *L*?  Explain using
   the ideal gas law.

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

### (b) Model answer

1. In 2D: 2 degrees of freedom (v_x, v_y).  In 3D: 3 degrees of freedom
   (v_x, v_y, v_z).

2. Each degree of freedom contributes ½ k_B T to the average energy.
   For *d* dimensions: ⟨KE⟩ = (d/2) N k_B T.  Per particle:
   ⟨KE_per⟩ = (d/2) k_B T.  So T = (2/d) ⟨KE_per⟩ / k_B.

3. For 2D (d=2): T = (2/2) * 2.5 / 1.0 = 2.5.

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

### (d) Model answer

| Source of error | Effect |
|----------------|--------|
| **Discrete time steps** | Wall collisions are detected after the particle has already crossed the wall, introducing a small position error.  Smaller dt reduces this. |
| **2D vs 3D** | Real gases are 3D.  The 2D simulation has different collision rates and pressure scaling.  The qualitative behaviour (MB distribution, equipartition) is the same. |
| **Point particles** | Real atoms have finite size (van der Waals radius).  Our simulation uses a small but non-zero radius for collision detection, which introduces excluded-volume effects. |
| **No inter-particle forces** | Real gases have attractive van der Waals forces.  Our simulation only has hard-sphere collisions, so it models an ideal gas, not a real gas with phase changes. |
| **O(N²) collision detection** | The pairwise check is computationally expensive for large N.  Real MD simulations use neighbour lists or cell indexing.  For N < 1000, O(N²) is acceptable. |

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

### (f) Model answer

1. 2D: f(v) = (m/k_B T) v exp(-mv²/2k_B T)
   3D: f(v) = 4π (m/2πk_B T)^(3/2) v² exp(-mv²/2k_B T)

2. In 2D (d=2): ⟨KE⟩ = N k_B T.  In 3D (d=3): ⟨KE⟩ = (3/2) N k_B T.
   More dimensions mean more ways to store energy, so the same
   temperature corresponds to higher total KE.

3. For the same N, T, and L: P_2D = N k_B T / L², P_3D = N k_B T / L³.
   In 3D, the volume is L³ instead of L², so the pressure is lower
   (divided by an extra factor of L).  For L > 1, P_3D < P_2D.