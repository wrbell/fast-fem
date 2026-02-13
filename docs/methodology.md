---
layout: page
title: Methodology
permalink: /methodology/
---

# Verification & Validation Methodology

Every simulation in this portfolio follows a structured V&V workflow to ensure results are correct and meaningful.

## The Difference

- **Verification** — Am I solving the equations correctly? *(math and numerics)*
- **Validation** — Am I solving the right equations? *(physics and modeling)*

## Workflow

```
1. Define the problem → What quantity? What assumptions?
2. Hand calculation → Solve analytically BEFORE running ANSYS
3. Build FEA model → Geometry → Material → Mesh → BCs
4. Solve and extract results
5. Compare → Error = |FEA − analytical| / analytical × 100%
6. Iterate if error too large → refine mesh, check BCs, check assumptions
7. Document → Validation report + simulation log entry
```

## Error Thresholds

| Analysis Type | Target Error |
|---------------|-------------|
| Static stress (simple) | < 5% |
| Static stress (complex) | < 10% |
| Beam deflection | < 5% |
| Natural frequencies | < 5% |
| Thermal (steady-state) | < 5% |
| CFD velocity/pressure | < 10% |
| Fatigue life | < factor of 2 |

## Mesh Convergence

Every critical result includes a mesh convergence study:

1. Start with a coarse mesh
2. Refine (double element count)
3. Repeat until result changes < 2%
4. Report the convergence plot

## Quality Indicators

**Trustworthy results show:**
- Mesh convergence < 2% change
- Match hand calc within threshold
- Physically intuitive deformation/stress patterns
- Balanced reaction forces

**Red flags:**
- Result changes significantly with refinement
- Large unexplained discrepancy with hand calc
- Stress singularities at sharp corners
- Solver convergence warnings

---

*Full methodology details: [reference/methodology.md on GitHub](https://github.com/wrbell/fast-fem/blob/main/reference/methodology.md)*
