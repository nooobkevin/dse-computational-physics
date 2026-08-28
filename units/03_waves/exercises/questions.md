# Wave Exercise — Concept Questions

These questions test your understanding of the physics behind the wave
simulation you just implemented.  Answer them in a few sentences each.

---

## Questions

### (a) Why does superposition produce a standing wave?

You implemented a traveling wave `y(x,t) = A sin(kx - ωt)`.  If you add
a second wave `y₂(x,t) = A sin(kx + ωt)` traveling in the opposite
direction, the sum is a standing wave.

1. Write down the mathematical expression for the sum `y₁ + y₂`.
2. Use the trigonometric identity `sin α + sin β = 2 sin((α+β)/2) cos((α-β)/2)`
   to simplify the sum.  What is the resulting expression?
3. At what positions *x* does the displacement remain zero for all time *t*?
   These are called **nodes**.  Express your answer in terms of the
   wavelength λ.
4. At what positions *x* does the displacement reach its maximum amplitude?
   These are called **anti-nodes**.

### (b) Standing waves vs. traveling waves

1. In a traveling wave, does a point on the string ever have zero
   displacement for all time?  Explain.
2. In a standing wave, does energy propagate along the string?  Explain
   why or why not.
3. A standing wave on a string fixed at both ends can only have certain
   wavelengths.  If the string length is *L*, what are the allowed
   wavelengths?  (This is the origin of musical notes on a string
   instrument.)

### (c) Intensity and amplitude

The energy of a wave is proportional to the square of its amplitude:
`I ∝ A²`.

1. If you double the amplitude of a wave, by what factor does the
   intensity increase?
2. If you triple the amplitude, by what factor does the intensity increase?
3. A sound wave with amplitude *A* has intensity *I*.  To produce a sound
   that is 4 times as intense, by what factor must the amplitude increase?
4. Explain in physical terms why energy depends on amplitude squared
   rather than amplitude.  (Hint: consider the kinetic energy of a point
   on the string: `½ m v²`, where *v* is the transverse velocity.)

### (d) Inverse-square law

A point source emits waves uniformly in all directions.  The intensity
at a distance *r* from the source follows the inverse-square law:
`I ∝ 1/r²`.

1. If you double your distance from a sound source, by what factor does
   the intensity decrease?
2. If the intensity is *I₀* at a distance of 1 m, what is the intensity
   at a distance of 3 m?
3. Why does the intensity follow a `1/r²` law rather than `1/r`?  (Hint:
   consider the surface area of a sphere.)

### (e) Interference and Young's double-slit

Young's double-slit experiment demonstrates the wave nature of light.
Bright fringes occur when the path difference from the two slits is an
integer number of wavelengths: `d sin θ = n λ`.

1. What condition must be satisfied for **destructive** interference
   (a dark fringe)?
2. If the slit separation *d* is increased, what happens to the fringe
   spacing on the screen?
3. If the wavelength λ is increased (e.g. red light instead of blue),
   what happens to the fringe spacing?
4. Why does the central fringe (n = 0) always appear bright regardless
   of the wavelength?

### (f) Polarisation as evidence for transverse waves

1. Explain why only **transverse** waves can be polarised, while
   **longitudinal** waves cannot.
2. Describe a simple experiment using a polarising filter that
   demonstrates that light is a transverse wave.
3. Sound waves in air are longitudinal.  Can sound waves be polarised?
   Explain.

---

## Model Answers (teacher only)

*The section below contains model answers.  Remove it before distributing
the questions to students.*

---

### (a) Model answer

1. `y₁ + y₂ = A sin(kx - ωt) + A sin(kx + ωt)`
2. Using `sin α + sin β = 2 sin((α+β)/2) cos((α-β)/2)`:
   `y = 2A sin(kx) cos(ωt)`
3. Nodes occur where `sin(kx) = 0`, i.e. `kx = nπ`, so `x = nπ/k = nλ/2`.
   Nodes are at `x = 0, λ/2, λ, 3λ/2, ...`
4. Anti-nodes occur where `|sin(kx)| = 1`, i.e. `kx = (n+½)π`, so
   `x = (n+½)λ/2 = λ/4, 3λ/4, 5λ/4, ...`

### (b) Model answer

1. No.  In a traveling wave, every point oscillates with the same
   amplitude *A*.  A point has zero displacement only at specific times
   (when the wave passes through equilibrium), not for all time.
2. No.  In a standing wave, energy is stored in the oscillations but
   does not propagate along the string.  The energy is confined between
   the nodes, oscillating between kinetic and potential forms.
3. For a string fixed at both ends of length *L*, the allowed wavelengths
   are `λₙ = 2L/n` where `n = 1, 2, 3, ...` (the harmonic series).
   The fundamental frequency is `f₁ = v/(2L)`.

### (c) Model answer

1. Doubling amplitude → intensity increases by factor 4 (2² = 4).
2. Tripling amplitude → intensity increases by factor 9 (3² = 9).
3. To quadruple intensity, amplitude must increase by factor 2 (√4 = 2).
4. The transverse velocity of a point on the string is `v_y = ∂y/∂t`.
   For `y = A sin(kx - ωt)`, `v_y = -ωA cos(kx - ωt)`.  Kinetic energy
   is `½ m v_y² ∝ A²`.  Since both kinetic and potential energy scale
   with A², the total energy (intensity) scales as A².

### (d) Model answer

1. Doubling distance → intensity decreases by factor 4 (1/2² = 1/4).
2. At 3 m: `I = I₀ / 3² = I₀ / 9`.
3. The inverse-square law comes from conservation of energy.  The total
   power emitted by the source spreads uniformly over a sphere of surface
   area `4πr²`.  Since power = intensity × area, `I = P / (4πr²) ∝ 1/r²`.
   If it were `1/r`, energy would not be conserved.

### (e) Model answer

1. Destructive interference (dark fringe): path difference = `(n + ½)λ`,
   i.e. `d sin θ = (n + ½)λ`.
2. Increasing slit separation *d* decreases fringe spacing (fringes get
   closer together).
3. Increasing wavelength λ increases fringe spacing (fringes spread out).
4. The central fringe (n = 0) has zero path difference from both slits,
   so waves arrive in phase for any wavelength, producing constructive
   interference.

### (f) Model answer

1. Polarisation requires the wave oscillation to have a specific
   direction (orientation).  Transverse waves oscillate perpendicular
   to the direction of propagation, so they have a well-defined
   polarisation direction.  Longitudinal waves oscillate parallel to
   the direction of propagation — there is no "direction" to filter,
   so they cannot be polarised.
2. Pass light through a polarising filter — the transmitted intensity
   is reduced.  Pass it through a second polarising filter rotated by
   90° — no light gets through.  Rotating the second filter back to 0°
   restores transmission.  This shows light has a transverse orientation.
3. No, sound waves in air are longitudinal (compression/rarefaction).
   There is no transverse oscillation to filter, so sound cannot be
   polarised.
