# ANSYS Preflight Checklists

Step-by-step checklists for each analysis type. Run through before solving to catch common mistakes.

---

## General (All Analysis Types)

- [ ] **Units consistent** — check Model > Unit System. ANSYS default is metric (m, kg, s). If mixing, convert everything to one system first.
- [ ] **Geometry imported cleanly** — no gaps, overlapping faces, or zero-thickness surfaces. Use SpaceClaim Repair tools.
- [ ] **Material assigned to every body** — check Model > Materials. Missing material = default structural steel (probably wrong).
- [ ] **Mesh quality acceptable** — check Mesh > Statistics: aspect ratio < 5, skewness < 0.95. Refine near stress concentrations.
- [ ] **Boundary conditions applied to correct faces/edges** — visually verify in Named Selections. Wrong face = wrong answer.
- [ ] **No rigid body motion** — model must be fully constrained. If solver fails with "pivot," you have an unconstrained DOF.
- [ ] **Solver settings per config.md** — 4–5 CPU cores, SMP mode, GPU solver OFF.
- [ ] **Save project before solving** — ANSYS can crash mid-solve. Save your .wbpj.

---

## Static Structural

**When to use:** Linear elastic analysis — stress, strain, deformation under static loads.

### Pre-Solve
- [ ] Analysis type: Static Structural (not Transient, not Modal)
- [ ] Material properties set: E, v (minimum). Add density if gravity is on.
- [ ] Large deflection: OFF for linear (ON only if deformation > 10% of characteristic dimension)
- [ ] At least one fixed support or displacement BC
- [ ] Applied loads: check magnitude AND direction (arrows in viewport)
- [ ] Contact regions: bonded (default), frictional, or frictionless — pick intentionally
- [ ] If symmetry: apply symmetry BC (frictionless support on cut face)

### Post-Solve
- [ ] Check solver convergence — Force Convergence plot should flatten
- [ ] Von Mises stress contour — is max stress at expected location?
- [ ] Deformation plot — does it deform in the expected direction?
- [ ] Check reaction forces — do they sum to applied load? (Newton's 3rd law)
- [ ] Compare max stress to hand calc (validation.md)
- [ ] Check max stress against yield — if σ > σ_y, linear elastic is invalid
- [ ] Document in sim_log.md and validation report

---

## Modal Analysis

**When to use:** Find natural frequencies and mode shapes.

### Pre-Solve
- [ ] Analysis type: Modal
- [ ] Material: E, v, AND density (ρ) — all three required for modal
- [ ] Boundary conditions: match real mounting conditions exactly
  - Free-free: no constraints (good for validation against analytical)
  - Fixed-free: fixed support on one end
- [ ] Number of modes to extract: set to at least 2× what you need (default 6 — increase to 10–20)
- [ ] Damping: usually ignored for modal (add in Harmonic Response instead)
- [ ] No external loads — modal analysis finds natural frequencies, not forced response

### Post-Solve
- [ ] Check mode shapes — do they make physical sense?
  - Mode 1: lowest frequency, simplest shape (1st bending)
  - Higher modes: more complex (2nd bending, torsion, axial)
- [ ] Watch for rigid-body modes — frequencies near 0 Hz mean unconstrained DOF
- [ ] Compare ω_n to hand calc: ω = √(k/m) for simple systems
- [ ] Check effective mass ratio — are important modes captured?
- [ ] Screenshot each mode shape with frequency label
- [ ] Validate against MATLAB eigenvalue solver if possible

---

## Harmonic Response

**When to use:** Frequency sweep — find amplitude vs. frequency under sinusoidal loading.

### Pre-Solve
- [ ] Link from Modal analysis (Modal → Harmonic in Project Schematic)
- [ ] Frequency range: bracket expected resonances (e.g., 0–2× first natural frequency)
- [ ] Number of substeps: enough resolution (50–100 steps minimum)
- [ ] Damping ratio ζ — must specify or response blows up at resonance
  - Steel: ζ ≈ 0.01–0.02
  - Rubber: ζ ≈ 0.05–0.15
- [ ] Applied harmonic load: magnitude and direction
- [ ] Solution method: Mode Superposition (faster) or Full (more accurate for damping)

### Post-Solve
- [ ] Frequency response plot — peaks at natural frequencies?
- [ ] Peak amplitude: compare to X = F₀/√((k−mω²)²+(cω)²)
- [ ] Phase angle plot — 90° at resonance?
- [ ] Check if response exceeds yield at any frequency
- [ ] Document peak frequencies and amplitudes

---

## Steady-State Thermal

**When to use:** Temperature distribution under constant heat loads/BCs.

### Pre-Solve
- [ ] Analysis type: Steady-State Thermal
- [ ] Material: thermal conductivity k (W/m·K). Add density and specific heat only if transient.
- [ ] Boundary conditions:
  - [ ] Temperature BC (Dirichlet): fixed temperature on a face
  - [ ] Heat flux (Neumann): W/m² applied to a surface
  - [ ] Convection: specify h (W/m²·K) AND T_ambient
  - [ ] Radiation (if needed): emissivity + ambient temperature
- [ ] At least one temperature reference (fixed temp or convection) — otherwise solver has no reference point
- [ ] Internal heat generation? Add as body load if applicable.

### Post-Solve
- [ ] Temperature contour — does gradient direction make sense?
- [ ] Check max/min temperatures — are they physically reasonable?
- [ ] Heat flux vectors — do they flow from hot to cold?
- [ ] Validate: q = kA(dT/dx) for 1D conduction
- [ ] Validate: q = hA(T_surface − T_ambient) for convection
- [ ] If linking to structural: export temperature field to Static Structural for thermal stress

---

## Thermal-Structural Coupling

**When to use:** Thermal stress — temperature changes cause expansion/contraction.

### Pre-Solve
- [ ] Set up Steady-State Thermal → Static Structural link in Project Schematic
- [ ] Thermal material properties: k, α (coefficient of thermal expansion)
- [ ] Structural material properties: E, v, α
- [ ] Reference temperature set correctly (stress-free temperature, typically room temp 22°C)
- [ ] Structural BCs: enough to prevent rigid body motion but allow thermal expansion
  - Common mistake: over-constraining prevents thermal expansion → artificially high stress

### Post-Solve
- [ ] Thermal strain: validate ε = αΔT
- [ ] Thermal stress: check against σ = EαΔT (fully constrained case)
- [ ] Deformation pattern: does it expand in expected direction?
- [ ] Compare to hand calc for simple geometries

---

## CFD (Fluent)

**When to use:** Fluid flow — velocity, pressure, temperature in fluid domains.

### Pre-Solve
- [ ] Geometry: define fluid domain (not solid). Use SpaceClaim to extract fluid volume.
- [ ] Mesh: use Fluent Meshing or ANSYS Meshing. Target < 512K cells (Student Edition).
  - [ ] Inflation layers on walls (at least 5 layers, growth ratio 1.2)
  - [ ] y+ check: for wall-resolved, y+ ≈ 1. For wall functions, y+ = 30–300.
- [ ] Solver: Pressure-Based (incompressible) or Density-Based (compressible)
- [ ] Viscous model: Laminar (Re < 2300 for pipe) or Turbulent (k-ε or k-ω SST)
- [ ] Material: fluid properties — density, viscosity, conductivity (if thermal)
- [ ] Boundary conditions:
  - [ ] Inlet: velocity-inlet or mass-flow-inlet
  - [ ] Outlet: pressure-outlet (usually 0 gauge)
  - [ ] Walls: no-slip (default). Specify thermal BC if heat transfer.
- [ ] Solution methods: SIMPLE or Coupled scheme
- [ ] Residual convergence criteria: default 1e-3, tighten to 1e-6 for accuracy
- [ ] CPU cores: 4–5 per config.md

### Post-Solve
- [ ] Residuals converged? All below target and flat for 100+ iterations.
- [ ] Mass flow balance: inlet ≈ outlet (check Reports > Fluxes)
- [ ] Velocity contour / streamlines — make physical sense?
- [ ] Validate: Re = ρVD/μ matches expected regime
- [ ] Pipe flow: validate velocity profile against Hagen-Poiseuille
- [ ] Flat plate: validate boundary layer thickness against Blasius
- [ ] Pressure drop: validate against Darcy-Weisbach
- [ ] If thermal: check temperature field, validate Nu or h

---

## Fatigue

**When to use:** Predict fatigue life under cyclic loading.

### Pre-Solve
- [ ] Run Static Structural first — fatigue uses stress results as input
- [ ] Fatigue Tool inserted under Solution
- [ ] Loading type: Constant Amplitude (fully reversed, zero-based, or ratio)
  - R = -1 (fully reversed), R = 0 (zero-based), R = custom
- [ ] S-N curve: use material-specific data if available, otherwise ANSYS default
  - For welds: use IIW FAT class, not parent metal S-N curve
- [ ] Mean stress correction: Goodman (conservative), Gerber, or Soderberg
- [ ] Scale factor: if actual load differs from static load case
- [ ] Stress component: Von Mises (default) or Max Principal — choose intentionally

### Post-Solve
- [ ] Life contour — minimum life at expected location (notch, weld toe)?
- [ ] Safety factor contour — SF < 1 means failure predicted
- [ ] Compare to hand calc: Goodman line σ_a/S_e + σ_m/S_ut = 1
- [ ] Check if fatigue life is reasonable for application
- [ ] Document FAT class and assumptions

---

## Contact (Bolted/Welded Joints)

**When to use:** Multi-body assemblies with joints, fasteners, or welds.

### Pre-Solve
- [ ] Contact detection: check all auto-detected contacts. Delete spurious ones.
- [ ] Contact type:
  - Bonded: parts glued together (simplest, fastest)
  - No separation: can slide but not separate
  - Frictional: realistic — specify friction coefficient μ
  - Frictionless: idealized sliding
- [ ] For welds: bonded contact at weld location. Mesh weld zone finely.
- [ ] For bolts: use Bolt Pretension feature (not just bonded contact)
- [ ] Formulation: Augmented Lagrange (default) or Pure Penalty
- [ ] Normal stiffness factor: 1.0 default. Reduce to 0.1 if convergence issues.
- [ ] Pinball radius: check that detection region covers the contact zone

### Post-Solve
- [ ] Contact status: check Sliding/Sticking/Open status
- [ ] Contact pressure: reasonable magnitude? Not negative?
- [ ] Stress at contact interface — check for singularities (infinite stress at sharp corners)
- [ ] Reaction forces at contact: match applied loads?
- [ ] Weld: check hot-spot stress (1.0t and 0.4t from weld toe per IIW)
