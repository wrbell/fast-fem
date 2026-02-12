# Fast-FEM

Accelerated self-study in Finite Element Method theory and ANSYS simulation, built to support three concurrent mechanical engineering course projects at the University of Michigan (Winter 2026).

## Objective

Go from zero ANSYS experience to validated multi-physics simulations in 9 weeks, producing portfolio-quality FEA work for real engineering projects across structural, vibration, and thermal-fluid domains.

## Course Projects

| Course | Focus | Project |
|--------|-------|---------|
| ME3601 — Machine Elements | Static/fatigue analysis, welded joints, shafts, gears | [Brief](projects/me3601_brief.md) |
| ME440 — Vibrations | Modal analysis, forced response, vibration absorbers | [Brief](projects/me440_brief.md) |
| ME379 — Thermal-Fluid | Convection, boundary layers, coupled thermal-structural | [Brief](projects/me379_brief.md) |

All projects due **Apr 27, 2026**.

## Approach

1. **Theory** — Hughes (FEM), Shigley (machine design), Inman (vibrations), Cengel (heat transfer), Metal Fatigue Handbook
2. **Simulation** — ANSYS Student Edition (Mechanical, Fluent, DesignXplorer)
3. **Validation** — Every simulation compared to analytical hand calculations ([formula reference](validation.md))
4. **Documentation** — Each simulation logged with model setup, mesh, BCs, results, and error analysis ([sim log](sim_log.md))

## Repository Structure

```
fast-fem/
├── README.md                   ← you are here
├── schedule_canonical.md       ← 9-week study plan (Feb 23 – Apr 19)
├── config.md                   ← hardware specs & ANSYS settings
├── references.md               ← 100+ learning resources (courses, tutorials, forums)
├── validation.md               ← hand-calc formulas for FEA verification
├── sim_log.md                  ← chronological simulation journal
├── projects/
│   ├── me3601_brief.md         ← ME3601 project scope & deliverables
│   ├── me440_brief.md          ← ME440 project scope & deliverables
│   └── me379_brief.md          ← ME379 project scope & deliverables
├── results/
│   ├── week_01/                ← validation reports & screenshots by week
│   ├── week_02/
│   └── ...
└── templates/
    └── validation_report.md    ← reusable template for documenting simulations
```

## Hardware

Dell Precision 5860 Tower — Intel Xeon W3-2425 (6 cores), 64GB DDR5, NVIDIA RTX 2000 Ada 16GB. Full specs and ANSYS solver settings in [config.md](config.md).

## Schedule

Compressed 9-week plan starting Feb 23, 2026. Spring break used as a theory sprint. See [schedule_canonical.md](schedule_canonical.md) for the full breakdown with daily tasks and course alignment matrix.

## Future Goals

- Advanced solvers: LS-DYNA, full ANSYS (commercial license)
- Advanced pre-processors: Altair HyperMesh, ANSA
- Advanced post-processors: META
- GPU-accelerated CFD (with RTX 4000 Ada+ upgrade)
