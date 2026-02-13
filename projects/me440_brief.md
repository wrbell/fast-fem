# ME440 — Vibrations: Project Brief

**Status:** TBD — fill in when project is assigned
**Due:** Apr 27, 2026

---

## Objective

*What engineering question is this project answering?*

> (e.g., "Design a tuned vibration absorber to suppress resonance in a machine frame")

## System / Geometry

*What are you modeling? Sketch or describe the system.*

- System description:
- Key dimensions / masses:
- Material(s):
- DOF count: (1-DOF / multi-DOF / continuous)

## Analysis Type

*Check all that apply:*

- [ ] Modal analysis (natural frequencies, mode shapes)
- [ ] Harmonic response (frequency sweep)
- [ ] Transient structural (time-domain)
- [ ] Random vibration
- [ ] Vibration absorber / isolator design
- [ ] Other:

## Boundary Conditions & Loads

| BC / Load | Type | Value | Location |
|-----------|------|-------|----------|
| | | | |
| | | | |
| | | | |

## Damping

- Damping model: (Rayleigh / constant / modal)
- Damping ratio ζ:
- Source: (measured / assumed / Inman table)

## Validation Plan

| Result | Hand Calc Formula | Expected Value | ANSYS Target Error |
|--------|------------------|----------------|--------------------|
| ω_n (mode 1) | ω = √(k/m) | | < 5% |
| ω_n (mode 2) | | | < 5% |
| Peak amplitude | X = F₀/√((k−mω²)²+(cω)²) | | < 10% |
| | | | |

*Reference: reference/validation.md for formula lookup*

## Deliverables

- [ ] ANSYS model file (.wbpj)
- [ ] Validation report (use templates/validation_report.md)
- [ ] Mode shape screenshots (first 5 modes)
- [ ] Frequency response plot (amplitude vs. frequency)
- [ ] MATLAB eigenvalue comparison
- [ ] Written report section on FEA methodology
- [ ] Other:

## Schedule Alignment

*Which canonical schedule weeks does this project draw from?*

- Week 5: Modal analysis, forced vibrations, absorber design
- Week 7: Vibration-fatigue combination
- Week 8: Capstone integration

## Notes

*Design decisions, instructor guidance, constraints, etc.*
