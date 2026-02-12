# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fast-FEM is a compressed 9-week self-directed learning project (Feb 23 – Apr 19, 2026) for mastering Finite Element Method (FEM) theory and ANSYS simulation software. Projects due Apr 27. It supports three concurrent University of Michigan mechanical engineering courses:

- **ME3601** (Machine Elements) — static/fatigue analysis, shafts, gears, bearings, welded joints
- **ME440** (Vibrations) — modal analysis, forced vibration, vibration absorbers
- **ME379** (Thermal-Fluid) — convection, boundary layers, heat transfer

The repository currently contains learning schedules and reference material (no simulation code or ANSYS project files yet).

## Repository Structure

- `schedule_canonical.md` — **Active schedule.** Compressed 9-week plan (Feb 23 start) with dates, course tie-ins, daily tasks, and checkboxes
- `config.md` — Hardware specs (Dell Precision 5860, Xeon W3-2425, RTX 2000 Ada 16GB), ANSYS settings, and performance expectations
- `references.md` — Central index of textbook chapters, ANSYS tutorials, and URLs organized by topic with schedule week mapping
- `validation.md` — Quick-reference sheet of all hand-calc formulas for verifying ANSYS results
- `README.md` — Project goals and future aspirations
- `schedule.md` — Original 12-week FEM curriculum (superseded by canonical)
- `grounded_schedule.md` — Semester-aligned variant (superseded by canonical)
- `schedule_with_weld.md` — Weld-focused variant (superseded by canonical)

## Key References

See `references.md` for the full index. Primary sources:
- **Hughes** — FEM theory (main textbook)
- **Shigley** — Machine design, welded joints, fatigue
- **Inman** — Vibrations
- **Cengel** — Heat transfer
- **Metal Fatigue Handbook** — Weld fatigue methods
- **ANSYS Student Edition** — Primary simulation tool

## Validation Approach

See `validation.md` for the full formula sheet. Each weekly milestone validates ANSYS results against analytical hand calculations across static stress, buckling, beam deflection, thermal, pressure vessels, vibrations, fatigue, welds, and CFD.

## Hardware Notes

See `config.md` for full details. Key constraints:
- 6-core Xeon W3-2425 — use 4–5 cores for ANSYS solver (SMP mode)
- 64GB DDR5 — well above Student Edition element limits
- RTX 2000 Ada — display/visualization only, GPU solver disabled
- Student Edition caps: 128K elements (Mechanical), 512K cells (Fluent)
