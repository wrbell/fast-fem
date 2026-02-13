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
3. **Validation** — Every simulation compared to analytical hand calculations ([methodology](methodology.md) | [formulas](validation.md))
4. **Documentation** — Each simulation logged with model setup, mesh, BCs, results, and error analysis ([sim log](sim_log.md))
5. **Automation** — Python notebooks for hand-calc validation, scripts for convergence plots

## Repository Structure

```
fast-fem/
├── README.md                       ← you are here
├── schedule_canonical.md           ← 9-week study plan (Feb 23 – Apr 19)
├── methodology.md                  ← V&V workflow, error thresholds, mesh convergence
├── config.md                       ← hardware specs & ANSYS settings
├── references.md                   ← 100+ learning resources
├── validation.md                   ← hand-calc formulas for FEA verification
├── sim_log.md                      ← chronological simulation journal
├── checklists/
│   ├── preflight.md                ← pre-solve checklists (static, modal, thermal, CFD, fatigue)
│   └── element_guide.md            ← element selection decision tree
├── notebooks/
│   ├── static_stress.ipynb         ← stress, beams, buckling, pressure vessels, welds
│   ├── thermal.ipynb               ← conduction, convection, thermal strain, pipe flow
│   ├── vibrations.ipynb            ← modal, harmonic, absorbers, beam frequencies
│   └── fatigue.ipynb               ← Goodman, Marin, S-N, IIW weld fatigue
├── scripts/
│   └── mesh_convergence.py         ← convergence plotter (CSV → publication-quality PNG)
├── projects/
│   ├── me3601_brief.md             ← ME3601 project scope & deliverables
│   ├── me440_brief.md              ← ME440 project scope & deliverables
│   └── me379_brief.md              ← ME379 project scope & deliverables
├── results/
│   ├── week_01/ … week_08/        ← validation reports & screenshots by week
├── templates/
│   ├── validation_report.md        ← reusable simulation report template
│   ├── post_mortem.md              ← reflective template for failures/surprises
│   └── visual_guide.md             ← screenshot standards & figure naming
├── docs/                           ← GitHub Pages portfolio site
│   ├── index.md, about.md
│   ├── methodology.md, case-studies.md
│   └── _config.yml
├── future/
│   ├── roadmap.md                  ← phased plan post-program, skills matrix
│   ├── solvers.md                  ← LS-DYNA, Abaqus, OpenFOAM, commercial ANSYS
│   ├── pre_post.md                 ← HyperMesh, ANSA, META, ParaView
│   └── hardware_upgrades.md        ← CPU/RAM/GPU upgrade path for Dell 5860
└── archive/                        ← superseded schedule files
```

## Hardware

Dell Precision 5860 Tower — Intel Xeon W3-2425 (6 cores), 64GB DDR5, NVIDIA RTX 2000 Ada 16GB. Full specs and ANSYS solver settings in [config.md](config.md).

## Schedule

Compressed 9-week plan starting Feb 23, 2026. Spring break used as a theory sprint. See [schedule_canonical.md](schedule_canonical.md) for the full breakdown with daily tasks and course alignment matrix.

## Portfolio Site

Enable GitHub Pages (Settings → Pages → Source: Deploy from branch, `main`, `/docs`) to publish at `https://wrbell.github.io/fast-fem/`.

## Future Goals

Post-program roadmap in [`future/`](future/):

- [**Roadmap**](future/roadmap.md) — phased plan from Summer 2026 onward, with skills matrix
- [**Summer 2026**](future/summer_2026.md) — 14-week plan (15 hrs/week alongside internship)
- [**Solvers**](future/solvers.md) — LS-DYNA, commercial ANSYS, Abaqus, OpenFOAM
- [**Pre/Post**](future/pre_post.md) — HyperMesh, ANSA, META, ParaView, Tecplot
- [**Hardware Upgrades**](future/hardware_upgrades.md) — CPU, RAM, GPU upgrade path for the Dell 5860
