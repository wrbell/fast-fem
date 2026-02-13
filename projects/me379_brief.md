# ME379 — Thermal-Fluid: Project Brief

**Status:** TBD — fill in when project is assigned
**Due:** Apr 27, 2026

---

## Objective

*What engineering question is this project answering?*

> (e.g., "Simulate convective heat transfer over a heated surface and validate against analytical boundary layer solution")

## Geometry / Domain

*What are you modeling? Sketch or describe the flow domain.*

- Domain description:
- Key dimensions:
- Fluid: (air / water / other)
- Solid material(s) (if conjugate heat transfer):

## Analysis Type

*Check all that apply:*

- [ ] Internal flow (pipe, duct)
- [ ] External flow (flat plate, cylinder, airfoil)
- [ ] Steady-state thermal (conduction only)
- [ ] Conjugate heat transfer (fluid + solid)
- [ ] Coupled thermal-structural (thermal stress)
- [ ] Transient thermal
- [ ] Other:

## Boundary Conditions & Loads

| BC / Load | Type | Value | Location |
|-----------|------|-------|----------|
| Inlet | Velocity / mass flow | | |
| Outlet | Pressure | | |
| Wall | Temp / heat flux / convection | | |
| | | | |

## Flow Parameters

- Reynolds number:
- Flow regime: (laminar / turbulent)
- Turbulence model (if turbulent): (k-ε / k-ω SST / other)

## Solver Settings (per plan/config.md)

- Solver: Fluent CPU (4–5 cores)
- Mesh cells: (target, max 512K for Student Edition)
- Precision: double

## Validation Plan

| Result | Hand Calc Formula | Expected Value | ANSYS Target Error |
|--------|------------------|----------------|--------------------|
| Velocity profile | Hagen-Poiseuille or Blasius | | < 5% |
| Heat transfer coeff | q = hAΔT | | < 10% |
| Thermal strain | ε = αΔT | | < 5% |
| | | | |

*Reference: reference/validation.md for formula lookup*

## Deliverables

- [ ] ANSYS Fluent model file
- [ ] Validation report (use templates/validation_report.md)
- [ ] Velocity contour / streamline screenshots
- [ ] Temperature distribution plot
- [ ] Mesh convergence study
- [ ] Written report section on CFD methodology
- [ ] Other:

## Schedule Alignment

*Which canonical schedule weeks does this project draw from?*

- Week 3: Thermal FEM (conduction, convection)
- Week 6: CFD (Fluent), coupled thermo-structural
- Week 8: Capstone integration

## Notes

*Design decisions, instructor guidance, constraints, etc.*
