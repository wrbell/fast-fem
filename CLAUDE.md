# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fast-FEM is a compressed 9-week self-directed learning project (Feb 23 – Apr 19, 2026) for mastering Finite Element Method (FEM) theory and ANSYS simulation software. Projects due Apr 27. It supports three concurrent University of Michigan mechanical engineering courses:

- **ME3601** (Machine Elements) — static/fatigue analysis, shafts, gears, bearings, welded joints
- **ME440** (Vibrations) — modal analysis, forced vibration, vibration absorbers
- **ME379** (Thermal-Fluid) — convection, boundary layers, heat transfer

Goals are both course project delivery and portfolio-quality documentation.

## Repository Structure

### Planning & Reference
- `schedule_canonical.md` — **Active schedule.** 9-week plan (Feb 23 start) with daily tasks and checkboxes
- `config.md` — Hardware specs (Dell Precision 5860, Xeon W3-2425, RTX 2000 Ada 16GB) and ANSYS settings
- `references.md` — 100+ learning resources: courses, tutorials, YouTube, forums, weld standards
- `validation.md` — Hand-calc formulas for verifying ANSYS results

### Projects
- `projects/me3601_brief.md` — ME3601 project scope (TBD — fill in when assigned)
- `projects/me440_brief.md` — ME440 project scope (TBD)
- `projects/me379_brief.md` — ME379 project scope (TBD)

### Results & Documentation
- `sim_log.md` — Chronological simulation journal (date, model, mesh, result, error, lessons)
- `results/week_XX/` — Validation reports and screenshots organized by week
- `templates/validation_report.md` — Reusable template for documenting each simulation

### Legacy (superseded by canonical schedule)
- `schedule.md`, `grounded_schedule.md`, `schedule_with_weld.md`

## Key References

See `references.md` for the full index. Primary sources:
- **Hughes** — FEM theory (main textbook)
- **Shigley** — Machine design, welded joints, fatigue
- **Inman** — Vibrations
- **Cengel** — Heat transfer
- **Metal Fatigue Handbook** — Weld fatigue methods
- **ANSYS Student Edition** — Primary simulation tool

## Validation Approach

See `validation.md` for the full formula sheet. Each weekly milestone validates ANSYS results against analytical hand calculations. Every simulation should be documented using `templates/validation_report.md` and logged in `sim_log.md`.

## Hardware Notes

See `config.md` for full details. Key constraints:
- 6-core Xeon W3-2425 — use 4–5 cores for ANSYS solver (SMP mode)
- 64GB DDR5 — well above Student Edition element limits
- RTX 2000 Ada — display/visualization only, GPU solver disabled
- Student Edition caps: 128K elements (Mechanical), 512K cells (Fluent)
