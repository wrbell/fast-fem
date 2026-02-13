# Validation Formulas Quick Reference

Hand calculations for verifying ANSYS results. Organized by analysis type.

---

## Static Stress & Strain

| Formula | Description | Source | Week |
|---------|-------------|--------|------|
| σ = F/A | Normal stress (axial bar) | Shigley Ch. 3 | 1 |
| σ = My/I | Bending stress in beam | Shigley Ch. 3 | 2, 5 |
| τ = VQ/Ib | Transverse shear stress | Shigley Ch. 3 | 5 |
| ε = σ/E | Hooke's law (linear elastic) | Hughes Ch. 1 | 1 |
| ε = αΔT | Thermal strain | Cengel | 10 |

## Buckling

| Formula | Description | Source | Week |
|---------|-------------|--------|------|
| P_cr = π²EI/(KL)² | Euler critical buckling load | Shigley Ch. 4 | 2 |
| σ_cr = π²E/(KL/r)² | Critical buckling stress | Shigley Ch. 4 | 2 |

## Beam Deflection

| Formula | Description | Source | Week |
|---------|-------------|--------|------|
| δ = PL³/3EI | Cantilever, point load at tip | Hughes Ch. 7 | 1, 5 |
| δ = PL³/48EI | Simply supported, center load | Hughes Ch. 7 | 5 |
| δ = 5wL⁴/384EI | Simply supported, uniform load | Hughes Ch. 7 | 5 |
| θ = TL/GJ | Angle of twist (circular shaft) | Shigley Ch. 3 | 5 |

## Pressure Vessels

| Formula | Description | Source | Week |
|---------|-------------|--------|------|
| σ_h = pr/t | Hoop (circumferential) stress, thin-wall | Shigley Ch. 3 | 7 |
| σ_a = pr/2t | Axial (longitudinal) stress, thin-wall | Shigley Ch. 3 | 7 |

## Thermal / Heat Transfer

| Formula | Description | Source | Week |
|---------|-------------|--------|------|
| q = kA(dT/dx) | Fourier's law (conduction) | Cengel Ch. 2 | 3 |
| q = hAΔT | Newton's law of cooling (convection) | Cengel Ch. 2 | 3 |
| R = L/kA | Thermal resistance (conduction) | Cengel Ch. 2 | 3 |

## Vibrations & Modal Analysis

| Formula | Description | Source | Week |
|---------|-------------|--------|------|
| ω_n = √(k/m) | Natural frequency (1-DOF) | Inman Ch. 9 | 7 |
| f_n = ω_n/2π | Natural frequency in Hz | Inman Ch. 9 | 7 |
| ω_d = ω_n√(1 − ζ²) | Damped natural frequency | Inman Ch. 4 | 8 |
| X = F₀/√((k−mω²)²+(cω)²) | Steady-state amplitude (forced, damped) | Inman Ch. 4 | 8 |
| T = √(1+(2ζr)²)/√((1−r²)²+(2ζr)²) | Transmissibility (r = ω/ω_n) | Inman Ch. 5 | 8 |

## Fatigue

| Formula | Description | Source | Week |
|---------|-------------|--------|------|
| σ_a/S_e + σ_m/S_ut = 1 | Modified Goodman line | Shigley Ch. 6 | 4, 11 |
| S_e = k_a·k_b·k_c·k_d·k_e·S_e' | Endurance limit with Marin factors | Shigley Ch. 6 | 11 |
| N = (σ_rev/a)^(1/b) | S-N curve life prediction | Shigley Ch. 6 | 11 |

## Weld-Specific

| Formula | Description | Source | Week |
|---------|-------------|--------|------|
| τ = F/(0.707·h·l) | Shear stress in fillet weld (throat area) | Shigley Ch. 9 | 1, 2 |
| τ'' = Mr/J | Secondary shear from eccentric load | Shigley Ch. 9 | 2 |
| Allowable = 0.30·S_ut(electrode) | Weld allowable shear (E60/E70) | Shigley Ch. 9 | 2 |

## CFD / Fluid Mechanics

| Formula | Description | Source | Week |
|---------|-------------|--------|------|
| Re = ρVD/μ | Reynolds number | Cengel | 9 |
| δ = 5x/√(Re_x) | Blasius boundary layer thickness | Cengel | 9 |
| ΔP = f(L/D)(ρV²/2) | Darcy-Weisbach (pipe friction loss) | Cengel | 9 |
| v(r) = (ΔP/4μL)(R²−r²) | Hagen-Poiseuille velocity profile (laminar) | Cengel | 9 |
