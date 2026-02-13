# Element Selection Guide

Decision tree for choosing ANSYS element types. Pick the simplest element that captures the physics.

---

## Quick Decision Tree

```
What is your geometry?
│
├── Thin-walled (t/L < 0.1)?
│   ├── Flat plate → SHELL181 (linear) or SHELL281 (quadratic)
│   ├── Curved shell → SHELL281 (quadratic preferred)
│   └── Tube / pipe → SHELL181 or PIPE289
│
├── Long, slender (L/d > 10)?
│   ├── Straight beam → BEAM188 (linear) or BEAM189 (quadratic)
│   ├── Frame / truss → BEAM188 (beam) or LINK180 (truss, axial only)
│   └── Pipe → PIPE289 (includes pressure loads)
│
├── Solid / chunky (3D)?
│   ├── Simple geometry → SOLID186 (hex, quadratic) — best accuracy per element
│   ├── Complex geometry → SOLID187 (tet, quadratic) — meshes anything
│   └── Axisymmetric → PLANE183 (2D, quadratic) — huge time savings
│
├── 2D plane (thin or long in z)?
│   ├── Plane stress (thin plate, σ_z ≈ 0) → PLANE183
│   ├── Plane strain (long extrusion, ε_z ≈ 0) → PLANE183
│   └── Axisymmetric (revolved shape) → PLANE183
│
└── Special elements
    ├── Spring / dashpot → COMBIN14
    ├── Point mass → MASS21
    ├── Rigid link → MPC184
    └── Contact → CONTA174 (surface) + TARGE170 (target)
```

---

## Element Reference Table

| Element | Type | Nodes | DOF/Node | Best For | Course |
|---------|------|-------|----------|----------|--------|
| **SOLID186** | 3D hex (20-node) | 20 | ux,uy,uz | Solid parts, mapped mesh | ME3601, ME440 |
| **SOLID187** | 3D tet (10-node) | 10 | ux,uy,uz | Complex geometry, auto mesh | ME3601, ME440 |
| **SHELL181** | Shell (4-node) | 4 | ux,uy,uz,rx,ry,rz | Thin plates, sheet metal | ME3601 |
| **SHELL281** | Shell (8-node) | 8 | ux,uy,uz,rx,ry,rz | Curved shells, accuracy | ME3601 |
| **BEAM188** | Beam (2-node) | 2 | ux,uy,uz,rx,ry,rz | Frames, simple beams | ME3601, ME440 |
| **BEAM189** | Beam (3-node) | 3 | ux,uy,uz,rx,ry,rz | Curved beams, accuracy | ME3601 |
| **PLANE183** | 2D (8-node) | 8 | ux,uy | Plane stress/strain, axisymmetric | ME3601 |
| **LINK180** | Truss (2-node) | 2 | ux,uy,uz | Trusses, axial-only | ME3601 |
| **PIPE289** | Pipe (3-node) | 3 | ux,uy,uz,rx,ry,rz | Piping systems | ME379 |
| **COMBIN14** | Spring-damper | 2 | varies | Springs, vibration absorbers | ME440 |
| **MASS21** | Point mass | 1 | ux,uy,uz,rx,ry,rz | Lumped masses | ME440 |
| **FLUID220** | 3D fluid (hex) | 20 | temp,pres | Thermal-fluid | ME379 |
| **SURF152** | Surface effect | 4–8 | varies | Convection/radiation BCs | ME379 |

---

## Linear vs. Quadratic Elements

| Property | Linear (1st order) | Quadratic (2nd order) |
|----------|--------------------|-----------------------|
| **Shape functions** | Linear (straight edges) | Quadratic (curved edges, midside nodes) |
| **Stress accuracy** | Low — constant or linear stress per element | High — captures stress gradients within element |
| **Mesh requirement** | Need many more elements | Fewer elements for same accuracy |
| **Solve time** | Faster per element | Slower per element, but fewer needed |
| **When to use** | Quick checks, very fine meshes | Default for production runs, stress concentrations |
| **ANSYS examples** | SOLID185, SHELL181 | SOLID186/187, SHELL281, PLANE183 |

**Rule of thumb:** Always use quadratic (2nd order) elements unless you have a specific reason not to. ANSYS Mechanical defaults to quadratic.

---

## Hex vs. Tet Meshing

| Property | Hex (SOLID186) | Tet (SOLID187) |
|----------|---------------|----------------|
| **Accuracy per element** | Higher — better stress recovery | Lower — need more elements |
| **Meshing difficulty** | Hard — needs sweepable or mappable geometry | Easy — meshes anything |
| **When to use** | Simple/regular geometry, extrusions, revolutions | Complex CAD, organic shapes |
| **Element count** | Lower (fewer needed) | Higher (need ~5–10× more for same accuracy) |
| **Convergence behavior** | Faster convergence | Slower convergence |

**Strategy:** Try hex (sweep/map) first. If geometry is too complex, fall back to tet. For critical stress regions, refine the tet mesh locally.

---

## Course-Specific Recommendations

### ME3601 — Machine Elements
- **Shafts:** SOLID186 (hex sweep along axis) or BEAM188 (for quick checks)
- **Gears:** SOLID187 (tet — complex tooth geometry) with contact elements
- **Welded joints:** SOLID186/187 with fine mesh at weld toe. Use SHELL181 for large plate-to-plate welds.
- **Bolted joints:** SOLID186 + Bolt Pretension feature
- **Bearings:** COMBIN14 spring elements to represent bearing stiffness

### ME440 — Vibrations
- **Simple oscillators:** COMBIN14 (spring) + MASS21 (point mass)
- **Beams/bars:** BEAM188 for mode shapes. SOLID186 for detailed stress.
- **Vibration absorbers:** COMBIN14 + MASS21 attached to main structure
- **Plates/panels:** SHELL181 or SHELL281 for plate vibrations

### ME379 — Thermal-Fluid
- **Conduction:** Same structural elements (SOLID186/187) with thermal DOF
- **Convection BCs:** Applied as surface loads — no special elements needed
- **CFD (Fluent):** Uses its own mesh — not Mechanical elements. Target < 512K cells.
- **Coupled thermal-structural:** Thermal solve → import temperature → structural solve

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| Using linear tets (SOLID185 tet) | Overly stiff, wrong stresses | Switch to quadratic (SOLID187) |
| Using beams where shells are needed | Misses local stress | Use SHELL if t/L > 0.1 |
| Mixing element types without transitions | Incompatible DOF | Use MPC contact or bonded contact at transitions |
| Too-coarse mesh at stress concentrations | Underestimates peak stress | Local mesh refinement (sizing on edge/face) |
| Forgetting midside nodes on curved geometry | Faceted approximation | Ensure quadratic elements on curved surfaces |
| Using plane stress when plane strain is correct | Wrong ε_z assumption | Check: is the part thin (stress) or long (strain)? |
