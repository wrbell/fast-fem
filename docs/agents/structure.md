This file lists the folders of the Fast-FEM repository.
AGENTS.md links here.

# Repository structure

## `plan/` — Learning Plan

- `plan/schedule.md` — Schedule. 9-week plan (Feb 23 start) with daily tasks and checkboxes
- `plan/config.md` — Hardware specs (Dell Precision 5860, Xeon W3-2425, RTX 2000 Ada 16GB) and ANSYS settings
- `plan/references.md` — 100+ learning resources: courses, tutorials, YouTube, forums, weld standards

## `reference/` — Look-Up-While-Working Docs

- `reference/methodology.md` — V&V methodology (workflow, error thresholds, mesh convergence)
- `reference/validation.md` — Hand-calc formulas for verifying ANSYS results
- `reference/preflight.md` — Pre-solve checklists for each analysis type (static, modal, thermal, CFD, fatigue, contact)
- `reference/element_guide.md` — Element selection decision tree and reference table
- `reference/visual_guide.md` — Screenshot standards, color maps, naming conventions

## `projects/` — Course Project Briefs

- `projects/me3601_brief.md` — ME3601 project scope
- `projects/me440_brief.md` — ME440 project scope
- `projects/me379_brief.md` — ME379 project scope
- `projects/me4301_brief.md` — ME4301 project scope: two projects (custom CFD code + Fluent analysis)

## `notebooks/` — Hand-Calc Jupyter Notebooks

- `notebooks/static_stress.ipynb` — Static stress, beams, buckling, pressure vessels, welds
- `notebooks/thermal.ipynb` — Conduction, convection, thermal strain, pipe flow
- `notebooks/vibrations.ipynb` — Modal, harmonic, absorbers, beam frequencies
- `notebooks/fatigue.ipynb` — Goodman, Marin, S-N, IIW weld fatigue
- `notebooks/cfd.ipynb` — CFD theory: FTCS, stability, convection schemes, iterative solvers, FVM, SIMPLE

## `scripts/` — Python Tools

- `scripts/mesh_convergence.py` — CLI convergence plotter (CSV → PNG)

## `templates/` — Copy-and-Fill Templates

- `templates/validation_report.md` — Reusable template for documenting each simulation
- `templates/post_mortem.md` — Reflective template for when simulations go wrong

## `results/` — Simulation Output

- `results/sim_log.md` — Chronological simulation journal (date, model, mesh, result, error, lessons)
- `results/week_XX/` — Validation reports and screenshots organized by week

## `docs/` — GitHub Pages Portfolio Site

- Jekyll/minima site. Enable in GitHub repo Settings → Pages → Source: `docs/`

## `future/` — Post-Program Roadmap

- `future/roadmap.md` — Phased plan (Summer 2026+), skills matrix
- `future/summer_2026.md` — 14-week summer plan (15 hrs/week alongside internship)
- `future/solvers.md` — LS-DYNA, Abaqus, OpenFOAM, commercial ANSYS
- `future/pre_post.md` — HyperMesh, ANSA, META, ParaView, Tecplot
- `future/hardware_upgrades.md` — CPU/RAM/GPU upgrade path for Dell 5860
- `future/interview_prep.md` — FEA interview questions and frameworks

## `archive/` — Superseded Files
