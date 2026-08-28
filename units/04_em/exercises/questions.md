# Electricity & Magnetism Exercise — Concept Questions (M5)

These questions test your understanding of the physics behind the electric
field and circuit simulations you just implemented.  Answer them in a few
sentences each.

---

## Questions

### (a) Coulomb's inverse-square law

You place a charge `q = +2 nC` at the origin.

1. Compute the electric field magnitude at `r = 0.5 m` and `r = 1.0 m`.
2. By what factor does the field decrease when you double the distance?
3. If you replace the charge with `q = -2 nC`, how does the field change?

### (b) Electric field vs. electric potential

Consider a point charge `q = +1 nC`.

1. Compute the potential `V` at `r = 0.5 m` and `r = 1.0 m`.
2. How does the potential scale with distance compared to the field?
   (i.e., `V ∝ 1/r^n` vs `E ∝ 1/r^m` — what are *n* and *m*?)
3. Explain in one sentence why the potential falls off more slowly with
   distance than the field.

### (c) Why is the electric field perpendicular to equipotential surfaces?

1. From the definition `E = -∇V`, explain why field lines must be
   perpendicular to equipotential surfaces.
2. What would happen if the field had a component *along* an equipotential
   surface?

### (d) Kirchhoff's current law (KCL)

In a circuit, three branches meet at a node:
- Branch 1: current `I₁ = 2 A` entering the node
- Branch 2: current `I₂ = 3 A` leaving the node
- Branch 3: unknown current `I₃`

1. Determine the magnitude and direction of `I₃`.
2. Explain KCL in terms of charge conservation.

### (e) Kirchhoff's voltage law (KVL)

A series circuit has a 12 V battery and two resistors `R₁ = 4 Ω` and
`R₂ = 6 Ω`.

1. Compute the current in the circuit.
2. Compute the voltage drop across each resistor.
3. Verify KVL: `ΣV = 0` around the loop.

### (f) Internal resistance and terminal voltage

A battery has an emf of `ε = 9.0 V` and an internal resistance of
`r = 0.5 Ω`.  It is connected to an external load `R = 4.5 Ω`.

1. Compute the current in the circuit.
2. Compute the terminal voltage (voltage across the battery terminals).
3. How much power is dissipated inside the battery?  How much in the
   external load?
4. What is the efficiency of the battery (power delivered to load /
   total power supplied)?

---

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. At `r = 0.5 m`:
       E = q / (4π ε₀ r²) = 2×10⁻⁹ / (4π × 8.85×10⁻¹² × 0.25) ≈ 71.9 N/C
   At `r = 1.0 m`:
       E ≈ 2×10⁻⁹ / (4π × 8.85×10⁻¹² × 1.0) ≈ 18.0 N/C

2. Doubling the distance reduces the field by a factor of 4 (inverse
   square law: E ∝ 1/r²).

3. The field magnitude is the same (71.9 N/C), but the direction reverses
   — it points toward the charge (radially inward) instead of away.

### (b) Model answer

1. At `r = 0.5 m`: V = 18.0 V; at `r = 1.0 m`: V = 9.0 V.
2. `V ∝ 1/r` (n = 1), while `E ∝ 1/r²` (m = 2).
3. Potential is the line integral of the field (`V = ∫ E·dr`), so the
   `1/r²` field integrates to a `1/r` potential, which falls off more
   slowly.

### (c) Model answer

1. `E = -∇V` means the field points in the direction of the steepest
   *decrease* in potential.  Along an equipotential surface, `V` is
   constant, so `∇V` has no component parallel to the surface — the
   field must be perpendicular.
2. If the field had a component along the surface, moving along the
   surface would change the potential, contradicting the definition
   of an equipotential.

### (d) Model answer

1. `I₃` must be `1 A` entering the node (KCL: `I_in = I_out`, so
   `2 + I₃ = 3`, giving `I₃ = 1 A` entering).
2. KCL expresses conservation of charge: charge cannot accumulate at
   a node (in steady state), so the total current entering must equal
   the total current leaving.

### (e) Model answer

1. `I = ε / (R₁ + R₂) = 12 / 10 = 1.2 A`
2. `V₁ = I × R₁ = 1.2 × 4 = 4.8 V`, `V₂ = I × R₂ = 1.2 × 6 = 7.2 V`
3. KVL: `12 - 4.8 - 7.2 = 0.0 V` ✓

### (f) Model answer

1. `I = ε / (R + r) = 9.0 / (4.5 + 0.5) = 9.0 / 5.0 = 1.8 A`
2. Terminal voltage: `V = ε - I r = 9.0 - 1.8 × 0.5 = 9.0 - 0.9 = 8.1 V`
3. Internal power: `P_int = I² r = (1.8)² × 0.5 = 1.62 W`
   Load power: `P_load = I² R = (1.8)² × 4.5 = 14.58 W`
4. Efficiency: `η = P_load / (P_load + P_int) = 14.58 / 16.20 = 90%`

---

### (d) Model answer (detailed)

KCL at a node: `2 A (in) = 3 A (out) + I₃`
If we define current entering as positive: `2 - 3 + I₃ = 0`, so `I₃ = 1 A`
entering the node.

### (e) Model answer (detailed)

Equivalent resistance: `R_eq = R₁ + R₂ = 4 + 6 = 10 Ω`
Current: `I = V / R_eq = 12 / 10 = 1.2 A`
Voltage drops: `V_R₁ = 1.2 × 4 = 4.8 V`, `V_R₂ = 1.2 × 6 = 7.2 V`
KVL check: `+12 V (battery rise) - 4.8 V - 7.2 V = 0 V` ✓

---

### (g) Lorentz force on a moving charge

A proton (`q = +1.6×10⁻¹⁹ C`, `m = 1.67×10⁻²⁷ kg`) moves with speed `v = 2.0×10⁶ m/s` at an angle of `30°` to a uniform magnetic field of strength `B = 0.5 T`.

1. Compute the magnitude of the magnetic force on the proton.
2. What is the force when the angle is `0°`? When it is `90°`?
3. Determine the radius of the circular path if the velocity is perpendicular to the field.
4. If the particle were an electron (same speed, opposite charge), how would the force magnitude and direction change?

### (h) Right-hand rule

A positively charged particle enters a uniform magnetic field pointing out of the page (⊙). The particle is moving to the right (+x direction).

1. Use the right-hand rule to determine the direction of the magnetic force.
2. Describe the resulting trajectory (shape, plane of motion).
3. How would the trajectory change if the particle were negatively charged?

### (i) Circular motion in a magnetic field

A particle of mass `m` and charge `q` moves in a uniform magnetic field `B` with velocity perpendicular to the field.

1. Derive the expression for the orbital radius `r = mv/(qB)` by equating the magnetic force to the centripetal force.
2. If the magnetic field strength is doubled, how does the radius change?
3. If the particle's speed is doubled (and the field is constant), how does the radius change?
4. Show that the orbital period `T = 2πm/(qB)` is independent of velocity.

---