# Verification & Validation Methodology

How this project ensures that simulation results are correct and meaningful.

---

## Why V&V Matters

A simulation that produces numbers is not the same as a simulation you can trust. The gap between "ANSYS gave me a result" and "I have confidence in this result" is bridged by verification and validation (V&V).

- **Verification** — Am I solving the equations correctly? (math and numerics)
- **Validation** — Am I solving the right equations? (physics and modeling)

This project applies both to every simulation, creating a documented trail of evidence for each result.

---

## The V&V Workflow

Every simulation in this project follows this loop:

```
1. Define the problem
   └── What quantity do I need? What assumptions am I making?

2. Hand calculation
   └── Solve analytically using known formulas (see validation.md)
   └── This is the "expected answer" — compute it BEFORE running ANSYS

3. Build the FEA model
   └── Geometry → Material → Mesh → BCs → Solver settings
   └── Use checklists/preflight.md before solving

4. Solve and extract results

5. Compare
   └── Error = |FEA − hand calc| / hand calc × 100%
   └── Target: < 5% for structural, < 10% for thermal/CFD

6. If error too large:
   ├── Check mesh (refine → re-solve → compare)
   ├── Check BCs (wrong face? wrong magnitude?)
   ├── Check material properties
   ├── Check assumptions (is linear elastic valid?)
   └── Check hand calc (is the formula applicable?)

7. Document
   └── Validation report + sim_log.md entry
```

The key discipline: **always compute the hand calculation first.** If you run ANSYS first, confirmation bias will make any result look "close enough."

---

## Mesh Convergence

Mesh convergence is the primary verification technique. It answers: "Is my mesh fine enough that further refinement doesn't change the answer?"

### Method

1. Start with a coarse mesh. Record the quantity of interest (e.g., max von Mises stress).
2. Refine the mesh (halve element size or double element count). Record again.
3. Repeat until the result changes by less than 2% between successive refinements.

| Refinement | Elements | Max Stress (MPa) | % Change |
|-----------|----------|-------------------|----------|
| Coarse | 500 | 98.2 | — |
| Medium | 2,000 | 112.5 | 14.6% |
| Fine | 8,000 | 118.3 | 5.2% |
| Very Fine | 32,000 | 119.1 | 0.7% |

In this example, the "Fine" mesh is borderline. "Very Fine" is converged (< 2% change).

### Rules of Thumb

- Refine locally at stress concentrations (fillets, holes, weld toes) — not the entire model.
- Quadratic elements converge faster than linear elements.
- Hex elements converge faster than tet elements.
- If stress keeps increasing without limit at a sharp corner, that's a **stress singularity** — the mesh will never converge there. Re-evaluate the geometry (add a fillet) or extract stress away from the singularity.
- Use the mesh convergence plotting script (`scripts/mesh_convergence.py`) to generate publication-quality convergence plots.

---

## Error Thresholds

These thresholds are guidelines, not rigid rules. Context matters.

| Analysis Type | Target Error vs. Hand Calc | Notes |
|---------------|---------------------------|-------|
| Static stress (simple geometry) | < 5% | Hand calc should be very close for bars, beams, pressure vessels |
| Static stress (complex geometry) | < 10% | Hand calc uses simplifying assumptions; some deviation expected |
| Beam deflection | < 5% | Classical beam theory is accurate for L/d > 10 |
| Buckling load | < 10% | Euler formula assumes ideal conditions; FEA captures imperfections |
| Natural frequency | < 5% | Analytical solutions exist for simple systems |
| Thermal (steady-state) | < 5% | 1D conduction formulas are exact for simple geometries |
| CFD velocity / pressure | < 10% | Analytical solutions are approximate (Blasius, Hagen-Poiseuille) |
| Fatigue life | < factor of 2 | Fatigue scatter is inherently large; within 2× is acceptable |

### When Errors Are Large

Large errors don't always mean the FEA is wrong. Investigate systematically:

1. **Mesh not converged** — most common. Refine and re-solve.
2. **Wrong BCs** — applied to wrong face, wrong direction, wrong magnitude.
3. **Wrong material** — using default structural steel instead of the actual material.
4. **Hand calc assumptions violated** — e.g., using thin-wall formula on a thick-wall vessel.
5. **Nonlinear effects** — if stresses exceed yield, linear elastic analysis underestimates deformation.
6. **Modeling simplification** — e.g., 2D model missing 3D effects.

---

## Validation Sources

Results are compared against these sources, in order of preference:

1. **Closed-form analytical solutions** — exact for the idealized problem (validation.md formulas)
2. **Published benchmark problems** — ANSYS Verification Manual, NAFEMS benchmarks
3. **Textbook examples** — Shigley, Inman, Cengel worked examples
4. **MATLAB / Python computation** — eigenvalue solvers, numerical integration
5. **Previous validated simulations** — building on prior work in this project

Each validation report documents which source was used and why.

---

## Documentation Standards

Every simulation produces two artifacts:

### 1. Validation Report (`templates/validation_report.md`)
Full documentation of the simulation: problem, model setup, mesh, BCs, results, comparison to hand calc, discussion, and lessons learned. This is the detailed record.

### 2. Sim Log Entry (`sim_log.md`)
One-paragraph summary: date, model description, key result, hand calc comparison, error, and lesson. This is the chronological index.

### Post-Mortem (`templates/post_mortem.md`)
For simulations where something unexpected happened — a reflection on what went wrong, root cause, and what to do differently. These are the most valuable documents for learning.

---

## Quality Indicators

Signs a simulation is trustworthy:

- Mesh convergence study shows < 2% change with refinement
- Result matches hand calc within expected error threshold
- Deformation and stress patterns are physically intuitive
- Reaction forces balance applied loads
- No warnings or errors in the solver output

Signs a simulation needs more work:

- Result changes significantly with mesh refinement (not converged)
- Large unexplained discrepancy with hand calc
- Stress singularities at sharp corners (infinite stress with refinement)
- Solver warnings about contact, convergence, or element quality
- "It looks right" is the only evidence

---

*Formula reference: validation.md | Checklists: checklists/preflight.md | Report template: templates/validation_report.md*
