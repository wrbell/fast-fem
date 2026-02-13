# Post-Program Roadmap

Where to go after the 9-week Fast-FEM program ends (Apr 19, 2026). Organized into phases by prerequisite, not timeline — move through them as opportunity and need align.

---

## Phase 1: Deepen (Summer 2026)

**See [summer_2026.md](summer_2026.md) for the full 14-week plan (15 hrs/week alongside internship).**

Summary: portfolio polish → Python scripting (PyMAPDL) → second solver → advanced topic deep dive.

### Key deliverables
- Live portfolio with 6–8 polished case studies
- Python scripting capability for parameterized studies
- Working proficiency in a second solver (LS-DYNA, Abaqus, or OpenFOAM)
- One cross-solver validation study

---

## Phase 2: Expand Solvers

**Goal:** Move beyond ANSYS Student Edition into commercial/research tools.

### LS-DYNA (Explicit Dynamics)
See [solvers.md](solvers.md) for details.
- Crash, impact, forming, blast — problems where implicit solvers fail
- Free academic license through LSTC/Ansys
- Different mindset: time-stepping, mass scaling, hourglass control

### Commercial ANSYS
- Research license through UMich if available (check CAEN or department)
- Removes element count caps → can tackle real-scale problems
- Unlocks HPC features: DMP, GPU solver, cluster submission

### Other Solvers
- **Abaqus** — industry standard for nonlinear (oil/gas, aerospace). Worth learning for job market.
- **COMSOL** — multi-physics coupling done differently. Good for thermal-fluid-structural combos.
- **OpenFOAM** — free, open-source CFD. Steep learning curve but unlimited.

---

## Phase 3: Pre/Post-Processing

**Goal:** Learn industry-standard meshing and visualization tools.

See [pre_post.md](pre_post.md) for details.

### Pre-processors
- **Altair HyperMesh** — industry gold standard for meshing. Hex-dominant meshing on complex geometry.
- **ANSA (BETA CAE)** — powerful for crash/NVH meshing, model assembly, morphing.

### Post-processors
- **META (BETA CAE)** — fast post-processing for large models, especially LS-DYNA results.
- **ParaView** — free, open-source, handles massive datasets. Good for CFD visualization.
- **Tecplot** — publication-quality CFD plots.

### Why bother?
ANSYS Workbench is fine for learning and Student Edition models. At real-world scale (millions of elements), dedicated pre/post tools are 10× faster for mesh generation, model assembly, and result extraction.

---

## Phase 4: Hardware Upgrades

**Goal:** Remove hardware bottlenecks as problems grow beyond Student Edition.

See [hardware_upgrades.md](hardware_upgrades.md) for details.

Current bottleneck order (from config.md):
1. **CPU** — 6 cores is the first constraint for anything beyond Student Edition
2. **RAM** — 64GB is fine now, but large assemblies need more
3. **GPU** — only matters with CFD Enterprise license

---

## Phase 5: Specialization

**Goal:** Pick a domain and go deep. Depends on career direction.

### Structural / Fatigue
- Fracture mechanics (XFEM, J-integral, crack propagation)
- Creep and time-dependent plasticity
- Composite materials (layup, failure criteria, delamination)
- Weld simulation: residual stress prediction, distortion, HAZ modeling

### Vibrations / NVH
- Random vibration and PSD analysis
- Rotordynamics
- Acoustic-structural coupling
- Operational modal analysis (OMA) — testing + simulation correlation

### CFD / Thermal
- Turbulence modeling deep-dive (LES, DES, DNS concepts)
- Conjugate heat transfer on real hardware
- Multiphase flow (VOF, Eulerian)
- Combustion modeling

### Manufacturing Simulation
- Metal forming (stamping, forging) — LS-DYNA or Simufact
- Additive manufacturing simulation — thermal distortion prediction
- Injection molding — Moldflow

---

## Skills Matrix

Current state (end of Fast-FEM) → target state after each phase.

| Skill | After Fast-FEM | Phase 1 | Phase 2 | Phase 3 |
|-------|---------------|---------|---------|---------|
| ANSYS Mechanical | Intermediate | Solid | Solid | Solid |
| ANSYS Fluent | Basic | Intermediate | Solid | Solid |
| Hand calc validation | Solid | Solid | Solid | Solid |
| Mesh convergence | Solid | Solid | Solid | Solid |
| Nonlinear FEA | Basic | Intermediate | Solid | Solid |
| Fatigue (S-N, IIW) | Intermediate | Solid | Solid | Solid |
| Modal / Harmonic | Intermediate | Solid | Solid | Solid |
| Python scripting | Basic | Intermediate | Intermediate | Solid |
| LS-DYNA | — | — | Basic | Intermediate |
| HyperMesh / ANSA | — | — | — | Basic → Intermediate |
| Documentation / V&V | Solid | Solid | Solid | Solid |
