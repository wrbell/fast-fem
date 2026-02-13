# Canonical Schedule: FEM & ANSYS (10 hrs/week)

Fresh start from Feb 23, 2026 (post-Colorado). Projects due Apr 27.
Compressed into 9 weeks: 1 setup week, spring break for theory, 7 hands-on weeks, plus buffer.

**Key principles:**
- ~4 hrs/week theory, ~5 hrs ANSYS hands-on, ~1 hr review/milestones
- Weld content integrated where it aligns with ME3601
- Real-life events: spring break (Mar 2–8), ME3601 Exam II (Mar 26)
- Validate every simulation against hand calculations (see reference/validation.md)
- Hardware: 6-core Xeon, 64GB RAM, CPU solver only (see plan/config.md)

---

## Week 0 — Feb 23 (Sunday): Desktop Setup
**Goal:** Machine operational, ANSYS installed and verified

- [ ] Morning (2 hrs): Unpack Dell Precision 5860. Install OS updates, NVIDIA driver for RTX 2000 Ada.
- [ ] Afternoon (2 hrs): Download and install ANSYS Student Edition (ansys.com/academic/students). Verify Workbench launches.
- [ ] Evening (1 hr): Configure ANSYS solver settings per plan/config.md (4–5 CPU cores, GPU solver off, SMP mode). Run trivial test — 1D bar under tension, check stress ≈ F/A.

**Milestone:** Desktop operational. ANSYS verified with a trivial simulation.

---

## Week 1 — Feb 24–Mar 1: FEM Fundamentals & Static Analysis
**Course tie-in:** ME3601 (static failure, stress/strain, buckling)
**SMART goal:** 2D plate analysis + mesh convergence + first weld sim — all validated within 5%

- [ ] Day 1 Mon (2 hrs): Read Hughes Ch. 1–2 (weak formulation, 1D elasticity). CADFEM beginner tutorial (cantilever beam).
- [ ] Day 2 Tue (2 hrs): ANSYS 2D plane stress — plate with hole. Structured vs. unstructured meshing.
- [ ] Day 3 Wed (2 hrs): Read Hughes Ch. 3 (shape functions, assembly). Buckling tutorial — validate Euler's formula.
- [ ] Day 4 Thu (2 hrs): Mesh convergence study — document stress error vs. element size plot.
- [ ] Day 5 Fri (2 hrs): Welded joints intro — Shigley Ch. 9.1–9.6 (weld symbols, stress analysis, strength, static loading). Model fillet weld in ANSYS; validate against hand calc.

**Milestone:** 2D plate + mesh convergence documented. First weld FEA compared to Shigley.

---

## Week 2 — Mar 2–8: Spring Break (Theory Sprint)
**Course tie-in:** Recharge + front-load theory reading for denser hands-on weeks ahead
**SMART goal:** Complete all major theory reading; outline Apr 27 project

Use break to read ahead — no new ANSYS sims required. This pays off in Weeks 3–8 when you can focus on hands-on work.

- [ ] Day 1 (1.5 hrs): Hughes Ch. 4 (mixed and penalty methods, reduced integration).
- [ ] Day 2 (1.5 hrs): Cottrell Ch. 1–2 (heat as FEM problem, weak form). Cengel Ch. 2 (conduction, convection).
- [ ] Day 3 (1.5 hrs): Shigley Ch. 6.1–6.6 (fatigue intro, S-N method, endurance limit, Marin factors). Shigley Ch. 9.7 (weld fatigue).
- [ ] Day 4 (1.5 hrs): Hertzberg Ch. 5–6 (fracture overview, stress intensity factors), Ch. 9–10 (cyclic fatigue, crack propagation).
- [ ] Day 5 (1.5 hrs): Hughes Ch. 5 (plates and beams — C⁰ approach, Timoshenko vs. Euler-Bernoulli). Hughes Ch. 6 (curved structural elements — shells).
- [ ] Day 6 (1 hr): Inman Ch. 1–6 skim (vibrations overview — free, forced, damped, MDOF, absorbers, beam vibration).
- [ ] Weekend (1 hr): Outline Apr 27 project — brainstorm welded component for capstone.

**Milestone:** Core theory for Weeks 3–8 front-loaded. Project concept drafted.

---

## Week 3 — Mar 9–15: Thermal FEM, Fatigue & Element Types
**Course tie-in:** ME379 labs (heat transfer); ME3601 (fatigue intro)
**SMART goal:** Thermal sim validated against Cengel; fatigue sim matching S-N data

- [ ] Day 1 (2 hrs): ANSYS steady-state thermal — conduction in rod. Add convection BC; validate q = hAΔT.
- [ ] Day 2 (2 hrs): 2D heat transfer in plate — validate with Cengel equations.
- [ ] Day 3 (2 hrs): Experiment with element types (quad/tri, higher-order) on Week 1 model. Mesh convergence with different element orders.
- [ ] Day 4 (2 hrs): ANSYS Fatigue Tool tutorial — simulate fatigue on simple welded bracket. Validate life cycles against Shigley Ch. 6.
- [ ] Day 5 (2 hrs): Weld fatigue comparison — bolted vs. welded under cyclic load. Document stress concentration differences.

**Milestone:** Thermal FEA validated. First fatigue sim on welded joint compared to Shigley.

---

## Week 4 — Mar 16–22: Beams, Plates, Shells & Welded Shafts
**Course tie-in:** ME3601 (shafts, bearings, gears)
**SMART goal:** Beam deflection within 10% of Timoshenko; shell hoop stress validated

- [ ] Day 1 (2 hrs): ANSYS beam element tutorial. Simply supported beam + multi-span beam. Validate δ = PL³/48EI.
- [ ] Day 2 (2 hrs): Plate — shell tutorial for flat plate under pressure. Validate deflection.
- [ ] Day 3 (2 hrs): ANSYS cylindrical pressure vessel — validate hoop stress σ = pr/t.
- [ ] Day 4 (2 hrs): Welded shafts — Hertzberg Ch. 6 (fracture mechanics — apply stress intensity factors to weld defects). Simulate welded shaft under torque using contacts.
- [ ] Day 5 (2 hrs): Model shaft-bearing assembly, check weld stresses. Tie to ME3601 shaft project.

**Milestone:** Beam/plate/shell deflection validated. Welded shaft FEA completed.

---

## Week 5 — Mar 23–29: Modal Analysis & Forced Vibrations
**Course tie-in:** ME440 (multi-DOF, free/forced response, harmonic)
**SMART goal:** Natural frequencies matching Inman; harmonic response validated
**Note:** ME3601 Exam II Mar 26 — lighter load that day

- [ ] Day 1 (2 hrs): Hughes Ch. 10 (eigenvalue problem solution techniques). ANSYS Modal tutorial — simple oscillator.
- [ ] Day 2 (2 hrs): Multi-DOF modal sim — compare to MATLAB eigenvalue solver. Validate ω = √(k/m).
- [ ] Day 3 (2 hrs): Welded assembly vibration — modal analysis on welded gear-shaft assembly.
- [ ] Day 4 (1 hr, light — exam day): ANSYS Harmonic Response — frequency sweep with damping.
- [ ] Day 5 (2 hrs): Validate X = F/(k − mω² + cωi). Tie to ME440 absorber design.

**Milestone:** First 5 natural frequencies extracted. Harmonic response validated. Absorber design sketched.

---

## Week 6 — Mar 30–Apr 5: CFD & Coupled Multi-Physics
**Course tie-in:** ME379 labs (viscous flows, boundary layers); cross-tie thermal + stress
**SMART goal:** Pipe flow validated against analytical; thermo-mechanical sim validated (ε = αΔT)

- [ ] Day 1 (2 hrs): ANSYS Fluent — laminar pipe flow (CPU solver, 4–5 cores per plan/config.md). Validate Hagen-Poiseuille.
- [ ] Day 2 (2 hrs): External flow — boundary layer over flat plate. Compare to Blasius solution.
- [ ] Day 3 (2 hrs): ANSYS thermal-stress coupling tutorial — beam with temperature gradient. Validate ε = αΔT.
- [ ] Day 4 (2 hrs): Model convection on welded pipe — tie fluid + thermal on practical geometry.
- [ ] Day 5 (2 hrs): Weld thermal effects — heat-affected zones, residual stress. ANSYS DesignXplorer intro — optimize weld geometry.

**Milestone:** Laminar flow validated. Coupled thermo-structural validated. First optimization run.

---

## Week 7 — Apr 6–12: Advanced Fatigue & Nonlinear
**Course tie-in:** ME3601 fatigue/shafts; ME440 FEM vibration
**SMART goal:** Nonlinear weld sim complete; fatigue life validated against handbook

- [ ] Day 1 (2 hrs): Shigley Ch. 6 deep-dive + Hertzberg Ch. 9 (cyclic stress-strain fatigue, S-N approach).
- [ ] Day 2 (2 hrs): ANSYS Fatigue Tool — multiaxial fatigue on welded shaft. Validate life cycles.
- [ ] Day 3 (2 hrs): Nonlinear FEM theory (beyond Hughes' linear scope — see Bathe or Crisfield for reference). Nonlinear static — plasticity in welds (large deformation).
- [ ] Day 4 (2 hrs): Nonlinear contact sim on gears. Vibration-fatigue combo — ME440 harmonic loads + fatigue life.
- [ ] Day 5 (2 hrs): Hertzberg Ch. 10–11 (fatigue crack propagation, engineering failure analysis). Refine fatigue model.

**Milestone:** Nonlinear weld plasticity simulated. Fatigue life validated against handbook/Shigley.

---

## Week 8 — Apr 13–19: Capstone Synthesis
**Course tie-in:** Final prep for Apr 27 projects (ME3601/ME440/ME379)
**SMART goal:** Integrated thermo-vib-stress sim on welded prototype documented for reports

- [ ] Day 1 (2 hrs): Build full assembly — welded shaft-gear-bearing system in ANSYS.
- [ ] Day 2 (2 hrs): Coupled analysis — vibration + thermal + fatigue on welded joints.
- [ ] Day 3 (2 hrs): Optimize design — adjust weld sizing, mesh, BCs. Cross-validate vs. SOLIDWORKS/MATLAB.
- [ ] Day 4 (2 hrs): Validation pass — compare all results to Shigley/Inman/Cengel. Document in report format.
- [ ] Day 5 (2 hrs): Write report sections on FEA methodology and validation. Practice presentation.

**Milestone:** Integrated capstone model complete. Results validated and documented for Apr 27 submission.

---

## Buffer — Apr 20–26: Polish & Finals Prep
- Light FEA only — polish project reports, fix remaining validation gaps.
- **Apr 27: Projects due.**

---

## Summary: Course Alignment Matrix

| Week | Dates | ME3601 (Machine Elements) | ME440 (Vibrations) | ME379 (Thermal-Fluid) |
|------|-------|--------------------------|--------------------|-----------------------|
| 0 | Feb 23 | *(desktop setup)* | *(setup)* | *(setup)* |
| 1 | Feb 24–Mar 1 | Stress/strain, buckling, weld intro | — | — |
| 2 | Mar 2–8 | *(break — theory sprint)* | *(break — theory)* | *(break — theory)* |
| 3 | Mar 9–15 | Fatigue intro, weld fatigue | — | Thermal conduction/convection |
| 4 | Mar 16–22 | Shafts, bearings, welded shafts | — | — |
| 5 | Mar 23–29 | Exam II (Mar 26) | Modal, forced vib, harmonic | — |
| 6 | Mar 30–Apr 5 | Weld optimization | — | CFD, coupled thermo-structural |
| 7 | Apr 6–12 | Fatigue deep-dive, nonlinear welds | Vib-fatigue combo | — |
| 8 | Apr 13–19 | Capstone integration | Capstone integration | Capstone integration |
| — | Apr 20–26 | *(polish/buffer)* | *(polish/buffer)* | *(polish/buffer)* |

## What Got Compressed

Compared to the original 12-week plan:
- **Weeks 1–2 merged** into Week 1 (fundamentals + static + weld intro)
- **Thermal + fatigue + element types** combined into Week 3
- **Spring break repurposed** as a theory sprint — front-loads reading so Weeks 3–8 are pure hands-on
- **CFD + coupled multi-physics** merged into Week 6 (both involve thermal coupling)
- **B-splines/isogeometric** dropped — not needed for the three course projects
- **Shells** folded into Week 4 with beams/plates (natural progression)
