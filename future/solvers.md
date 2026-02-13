# Future Solvers

Solvers to learn after the 9-week Fast-FEM program. Prioritized by job-market value and complementarity to ANSYS.

---

## LS-DYNA (Explicit Dynamics)

### What it is
Explicit finite element solver for high-speed transient problems — crash, impact, blast, forming, drop tests. Where implicit solvers (ANSYS Mechanical) would fail to converge due to large deformations, contact changes, and material failure.

### Why learn it
- Industry standard for automotive crashworthiness (OEM and Tier 1 suppliers)
- Used heavily in defense, aerospace, consumer products
- Free academic license through LSTC/Ansys (LS-DYNA Student)
- Complements ANSYS — covers the problem class that Mechanical doesn't handle well

### Key differences from ANSYS Mechanical
| Aspect | ANSYS Mechanical (Implicit) | LS-DYNA (Explicit) |
|--------|---------------------------|-------------------|
| Time integration | Implicit (Newton-Raphson) | Explicit (central difference) |
| Time step | Large, adaptive | Tiny, controlled by smallest element |
| Convergence | Can fail on high nonlinearity | Always advances (no convergence check) |
| Best for | Static, modal, slow transient | Impact, crash, fast transient |
| Mesh sensitivity | Mesh quality matters | Mass scaling, hourglass control |
| Material models | ~50 | 300+ (metals, foams, composites, soil, biological) |

### Learning path
1. LS-DYNA Student Edition — free download from lsdyna.ansys.com
2. LS-PrePost (free pre/post processor)
3. Start with: bar impact, drop test, Taylor impact (cylinder on rigid wall)
4. Validate: compare to analytical solutions (Hertz contact, plastic collapse)
5. LSTC training: free webinars and examples at lsdyna.ansys.com/training

### Resources
- LS-DYNA Keyword User Manual (Vol I & II)
- LS-DYNA Examples Manual
- Erhart/Borrvall: Introduction to LS-DYNA (free PDF)
- DYNAmore tutorials and seminars

---

## Commercial ANSYS

### What changes with a full license
| Feature | Student Edition | Research/Commercial |
|---------|----------------|-------------------|
| Element cap (Mechanical) | 128K | Unlimited |
| Cell cap (Fluent) | 512K | Unlimited |
| GPU solver (Fluent) | Not available | Available with HPC license |
| DMP (distributed memory) | Not available | Available |
| HPC Pack licensing | Not available | Available |
| DesignXplorer limits | Limited DOE | Full parametric |

### How to get it
- **UMich research license** — check CAEN software catalog or ask department IT
- **ANSYS startup program** — free commercial license for startups < $5M revenue
- **Personal learning** — ANSYS Discovery (free, limited) or student competitions

### What to do with it
- Run mesh convergence studies past 128K elements (find where Student Edition was lying)
- Large assemblies: full engine, full vehicle subsystem
- DMP solving: distribute across multiple machines
- GPU-accelerated Fluent (with RTX 4000 Ada upgrade, see hardware_upgrades.md)

---

## Abaqus

### What it is
Dassault Systèmes' flagship FEA solver. The other industry standard alongside ANSYS.

### Why learn it
- Dominant in oil & gas, aerospace, biomechanics
- Stronger nonlinear capabilities than ANSYS Mechanical in some areas (UMAT, cohesive elements)
- Many employers require Abaqus experience
- Different input philosophy (keyword-driven vs GUI) — good to know both

### Key differences from ANSYS
| Aspect | ANSYS Mechanical | Abaqus |
|--------|-----------------|--------|
| GUI | Workbench (polished) | CAE (functional) |
| Input | GUI-driven, APDL scripting | Keyword input (.inp files), Python scripting |
| Strengths | Broad multi-physics, good GUI | Deep nonlinear, user subroutines (UMAT/VUMAT) |
| Explicit | LS-DYNA (separate) | Abaqus/Explicit (integrated) |
| CFD | Fluent (excellent) | Limited (usually coupled with external) |

### Learning path
1. Abaqus Student Edition (free from 3DS)
2. MIT course: "Computational Mechanics of Materials" uses Abaqus
3. Start with: same problems you did in ANSYS — compare results
4. Then: user subroutines (Fortran UMAT) for custom material models

---

## OpenFOAM (Open-Source CFD)

### What it is
Free, open-source CFD toolbox. C++ based, command-line driven, unlimited mesh size.

### Why learn it
- No license cost, no mesh limits
- Teaches CFD fundamentals (you configure everything manually — no black boxes)
- Used in research and increasingly in industry
- Runs on Linux clusters — good for HPC experience

### Tradeoffs vs Fluent
| Aspect | Fluent | OpenFOAM |
|--------|--------|----------|
| Cost | License required | Free |
| GUI | Polished | Minimal (ParaView for post) |
| Setup time | Fast (GUI-driven) | Slow (text files, scripts) |
| Learning curve | Moderate | Steep |
| Mesh limits | License-dependent | Hardware only |
| Turbulence models | Comprehensive | Comprehensive |
| Documentation | Excellent | Decent (community-driven) |

### Learning path
1. Install on Linux (WSL works, native Linux better)
2. OpenFOAM tutorials: cavity, pitzDaily, motorBike
3. Start with: same laminar pipe flow from Week 6 — compare to Fluent
4. CFD Direct tutorials: cfd.direct/openfoam/user-guide
