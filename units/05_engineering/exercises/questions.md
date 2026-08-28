# Physics & Engineering Exercise — Concept Questions (M5)

These questions test your understanding of the physics behind the optical
fibre, transformer, laser, and motor simulations.  Answer them in a few
sentences each.

---

## Questions

### (a) Critical angle and total internal reflection

An optical fibre has a core refractive index `n₁ = 1.50` and a cladding
refractive index `n₂ = 1.45`.

1. Compute the critical angle `θ_c` in degrees.
2. If a ray enters the fibre at an angle of `60°` (relative to the normal),
   does it undergo total internal reflection?  Explain.
3. What happens if the cladding index is increased to `n₂ = 1.52`?  Can TIR
   still occur?

### (b) Why is the refractive index defined as n = c/v?

1. Explain in one sentence why light travels slower in a medium than in
   vacuum.
2. If the speed of light in a certain glass is `v = 2.0 × 10⁸ m/s`, what
   is the refractive index of the glass?
3. How does a higher refractive index affect the critical angle?

### (c) Ideal transformer ratios

An ideal transformer has `Np = 200` turns on the primary and `Ns = 50`
turns on the secondary.  The primary voltage is `Vp = 240 V`.

1. Compute the secondary voltage `Vs`.
2. If the secondary current is `Is = 4 A`, what is the primary current `Ip`?
3. Verify that power is conserved: `Vp × Ip = Vs × Is`.
4. Why is an ideal transformer assumed to have no power loss?

### (d) Laser coherence and population inversion

1. What is a population inversion, and why is it necessary for laser
   operation?
2. How does stimulated emission differ from spontaneous emission?
3. Why is the light from a laser coherent, while light from an LED is not?

### (e) Motor effect

1. A current-carrying conductor of length `L = 0.2 m` carries a current
   `I = 3 A` in a magnetic field `B = 0.4 T`.  Compute the force on the
   conductor.
2. If the conductor is part of a coil with `N = 10` turns and radius
   `r = 0.05 m`, what is the maximum torque?
3. Why does the torque vary with the armature angle `θ`?

### (f) Transformer applications

1. Why are step-up transformers used in power transmission?
2. A step-down transformer reduces voltage from 240 V to 12 V.  If the
   primary has 200 turns, how many turns does the secondary have?
3. What would happen if a transformer were connected to a DC supply?

---

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. `θ_c = arcsin(n₂/n₁) = arcsin(1.45/1.50) ≈ arcsin(0.9667) ≈ 75.1°`
2. `60° < 75.1°`, so the ray is below the critical angle — it will NOT
   undergo TIR.  The ray leaks out through the cladding.
3. If `n₂ = 1.52 > n₁ = 1.50`, then `n₂/n₁ > 1`, so `arcsin(n₂/n₁)` is
   undefined.  No TIR is possible because the ray would refract into the
   cladding rather than reflect.

### (b) Model answer

1. Light interacts with the atoms/molecules in the medium, causing
   repeated absorption and re-emission that delays the net propagation.
2. `n = c/v = (3.0 × 10⁸) / (2.0 × 10⁸) = 1.50`
3. A higher refractive index means light travels slower in that medium,
   and the critical angle for TIR becomes smaller (since `θ_c = arcsin(n₂/n₁)`
   decreases as `n₁` increases).

### (c) Model answer

1. `Vs = Vp × Ns/Np = 240 × 50/200 = 60 V`
2. `Ip = Is × Ns/Np = 4 × 50/200 = 1 A`
3. `Pp = 240 × 1 = 240 W`, `Ps = 60 × 4 = 240 W` ✓
4. An ideal transformer assumes no resistive losses in the windings, no
   eddy currents in the core, and perfect magnetic coupling — all energy
   is transferred from primary to secondary.

### (d) Model answer

1. Population inversion means more atoms are in the upper energy level
   than the lower level.  This is necessary because stimulated emission
   (which produces laser light) requires more atoms to be ready to emit
   than to absorb.
2. Stimulated emission is triggered by an existing photon and produces a
   second photon identical in phase, direction, and energy.  Spontaneous
   emission occurs randomly without a trigger.
3. Laser light is coherent because stimulated emission produces photons
   that are all in phase (same frequency, phase, and direction).  LED
   light comes from spontaneous emission, which is random in phase and
   direction.

### (e) Model answer

1. `F = B I L = 0.4 × 3 × 0.2 = 0.24 N`
2. Maximum torque: `τ_max = N B I L r = 10 × 0.4 × 3 × 0.2 × 0.05 = 0.12 N·m`
3. Torque `τ = N B I L r cos(θ)` varies with angle because the effective
   lever arm changes as the coil rotates.  Torque is maximum when the coil
   is perpendicular to the field (θ = 0) and zero when parallel (θ = 90°).

### (f) Model answer

1. Step-up transformers increase voltage for transmission, which reduces
   current for the same power (P = VI).  Lower current means less resistive
   loss (I²R) in the transmission lines.
2. `Ns = Np × Vs/Vp = 200 × 12/240 = 10 turns`
3. A transformer requires a changing magnetic flux to induce voltage in
   the secondary.  DC provides a constant current, so no changing flux is
   produced — the transformer would act as a short circuit and overheat.