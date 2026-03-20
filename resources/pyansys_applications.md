# PyAnsys & PyDYNA — Common Projects & Applications

Practical application patterns organized by domain. Each section includes the problem statement, tools used, and a code skeleton.

**Related files:**
- [pyansys_research.md](pyansys_research.md) — detailed API guide
- [pyansys_references.md](pyansys_references.md) — link collection

---

## Table of Contents

1. [Material Characterization](#1-material-characterization)
2. [Parametric Studies](#2-parametric-studies)
3. [Structural Optimization](#3-structural-optimization)
4. [Mesh Convergence Automation](#4-mesh-convergence-automation)
5. [Thermal-Structural Coupling](#5-thermal-structural-coupling)
6. [Fatigue Automation](#6-fatigue-automation)
7. [Crash & Impact (LS-DYNA)](#7-crash--impact-ls-dyna)
8. [Surrogate Modeling](#8-surrogate-modeling)

---

## 1. Material Characterization

### 1a. Hyperelastic Calibration (Mooney-Rivlin, Ogden)

**Problem:** Fit hyperelastic material model parameters from uniaxial tensile test data (stretch vs. stress).

**Tools:** SciPy optimize, PyMAPDL (for validation)

```python
import numpy as np
from scipy.optimize import minimize

def mooney_rivlin_stress(stretch, C10, C01):
    """Uniaxial Cauchy stress for incompressible Mooney-Rivlin."""
    lam = stretch
    return 2 * (lam - 1 / lam**2) * (C10 + C01 / lam)

def ogden_stress_1term(stretch, mu, alpha):
    """Uniaxial Cauchy stress for 1-term Ogden."""
    lam = stretch
    return (mu / alpha) * (lam**alpha - lam**(-alpha / 2))

def fit_mooney_rivlin(stretch_data, stress_data):
    def residual(params):
        C10, C01 = params
        pred = mooney_rivlin_stress(stretch_data, C10, C01)
        return np.sum((pred - stress_data) ** 2)

    result = minimize(residual, x0=[0.1, 0.1], method="Nelder-Mead")
    return result.x

# Load test data
data = np.loadtxt("tensile_test.csv", delimiter=",", skiprows=1)
stretch = data[:, 0]  # lambda = 1 + engineering strain
stress = data[:, 1]   # Cauchy stress (MPa)

C10, C01 = fit_mooney_rivlin(stretch, stress)
print(f"Mooney-Rivlin: C10={C10:.4f}, C01={C01:.4f} MPa")

# Validate in PyMAPDL
from ansys.mapdl.core import launch_mapdl
mapdl = launch_mapdl()
mapdl.prep7()
mapdl.tb("MOONEY", 1, "", "", 2)
mapdl.tbdata(1, C10, C01)
# ... build single-element model, apply same stretch, compare stress ...
```

**Key references:**
- [Hyperelastic Material Fitting (GitHub)](https://github.com/LucMarechal/Soft-Robotics-Materials-Database)
- [PyMAPDL: Calibrating Hyperelastic Models](https://examples.mapdl.docs.pyansys.com/technology_showcase_examples/techdemo-15/ex_15-teccalvalhyper.html)

---

### 1b. MAT_024 Parameter Fitting (LS-DYNA Piecewise Linear Plasticity)

**Problem:** Convert engineering tensile test data to true stress vs. effective plastic strain for LS-DYNA MAT_024.

**Tools:** NumPy, SciPy interpolation

```python
import numpy as np
from scipy.interpolate import interp1d

def engineering_to_true(eng_stress, eng_strain):
    """Convert engineering to true stress-strain."""
    true_strain = np.log(1 + eng_strain)
    true_stress = eng_stress * (1 + eng_strain)
    return true_stress, true_strain

def extract_plastic(true_stress, true_strain, E):
    """Remove elastic component: eps_p = eps_true - sigma/E."""
    eps_elastic = true_stress / E
    eps_plastic = true_strain - eps_elastic
    mask = eps_plastic >= 0
    return eps_plastic[mask], true_stress[mask]

def create_mat024_card(eng_stress, eng_strain, E, density, nu, n_points=15):
    """Generate MAT_024 keyword card from tensile test data."""
    true_s, true_e = engineering_to_true(eng_stress, eng_strain)
    eps_p, sigma = extract_plastic(true_s, true_e, E)

    # Smooth and subsample
    f = interp1d(eps_p, sigma, kind="cubic")
    eps_p_out = np.linspace(0, eps_p[-1], n_points)
    sigma_out = f(eps_p_out)

    lines = [
        "*MAT_PIECEWISE_LINEAR_PLASTICITY",
        f"$      MID        RO         E        PR      SIGY      ETAN",
        f"         1  {density:.2E}  {E:.4E}  {nu:.4f}  {sigma_out[0]:.4E}       0.0",
        f"*DEFINE_CURVE",
        f"$     LCID      SIDR       SFA       SFO      OFFA      OFFO",
        f"         1         0       1.0       1.0       0.0       0.0",
    ]
    for ep, s in zip(eps_p_out, sigma_out):
        lines.append(f"  {ep:.6E},{s:.6E}")

    return "\n".join(lines)

# Example: mild steel
eng_strain = np.linspace(0, 0.3, 100)
eng_stress = 350 * (1 - np.exp(-10 * eng_strain))  # placeholder curve
E = 200e3  # MPa

card = create_mat024_card(eng_stress, eng_strain, E, 7.85e-9, 0.3)
print(card)
```

**Key requirements:**
- Input must be **true stress** vs. **effective plastic strain**
- First data point should be at (0.0, yield_stress)
- Elastic portion must be subtracted: `eps_p = eps_true - sigma_true / E`

**References:**
- [Engineering to True Stress/Strain (dynasupport.com)](https://www.dynasupport.com/howtos/material/from-engineering-to-true-strain-true-stress)
- [MaterialMAP](https://materialmap.net/) — web tool for MAT_024 generation

---

### 1c. ML-Based Material Calibration

**Problem:** When analytical models don't fit well (e.g., complex hardening, rate dependence), use ML to map test data to material parameters.

**Tools:** scikit-learn, SMT, PyMAPDL

```python
from smt.surrogate_models import KRG
import numpy as np

# 1. Generate training data: sweep material params → FEA → response
#    (force-displacement curve, necking point, etc.)
param_space = {
    "E": (180e3, 220e3),
    "sigy": (200, 400),
    "n_hardening": (0.1, 0.5),
}

# 2. Run N FEA simulations, extract simulated force-disp curves
# 3. Compute error metric between simulated and experimental curves
# 4. Train surrogate: params → error
# 5. Minimize surrogate to find best-fit params

# This is an inverse problem — the surrogate replaces the forward
# FEA model in the optimization loop
```

---

## 2. Parametric Studies

### 2a. Thickness Sweep

**Problem:** How does plate/shell thickness affect maximum stress and displacement?

```python
import numpy as np
import pandas as pd
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

thicknesses = np.linspace(1.0, 10.0, 20)
results = []

for t in thicknesses:
    mapdl.clear()
    mapdl.prep7()

    # Material
    mapdl.mp("EX", 1, 200e3)
    mapdl.mp("PRXY", 1, 0.3)

    # Shell element with variable thickness
    mapdl.et(1, "SHELL181")
    mapdl.sectype(1, "SHELL")
    mapdl.secdata(t)  # thickness parameter

    # Geometry (rectangular plate)
    mapdl.rectng(0, 200, 0, 100)
    mapdl.esize(5)
    mapdl.amesh("ALL")

    # BCs: fix one edge, pressure on surface
    mapdl.nsel("S", "LOC", "X", 0)
    mapdl.d("ALL", "ALL", 0)
    mapdl.allsel()
    mapdl.sfe("ALL", 1, "PRES", "", 1.0)  # 1 MPa pressure

    # Solve
    mapdl.run("/SOLU")
    mapdl.antype("STATIC")
    mapdl.solve()
    mapdl.finish()

    # Extract results
    mapdl.post1()
    max_disp = mapdl.post_processing.nodal_displacement("NORM").max()
    max_stress = mapdl.post_processing.nodal_eqv_stress().max()
    mapdl.finish()

    results.append({
        "thickness": t,
        "max_disp": max_disp,
        "max_stress": max_stress,
    })
    print(f"t={t:.1f} mm: disp={max_disp:.4f} mm, σ={max_stress:.2f} MPa")

df = pd.DataFrame(results)
df.to_csv("thickness_sweep.csv", index=False)
```

### 2b. Material Comparison

**Problem:** Compare structural response across multiple material candidates.

```python
materials = {
    "Steel":    {"EX": 200e3, "PRXY": 0.30, "DENS": 7.85e-9},
    "Aluminum": {"EX": 70e3,  "PRXY": 0.33, "DENS": 2.70e-9},
    "Titanium": {"EX": 110e3, "PRXY": 0.34, "DENS": 4.43e-9},
    "Copper":   {"EX": 117e3, "PRXY": 0.34, "DENS": 8.96e-9},
}

results = []
for name, props in materials.items():
    mapdl.clear()
    mapdl.prep7()
    for key, val in props.items():
        mapdl.mp(key, 1, val)
    # ... same geometry, mesh, BCs, loads ...
    mapdl.solve()
    mapdl.post1()
    results.append({
        "material": name,
        "max_stress": mapdl.post_processing.nodal_eqv_stress().max(),
        "max_disp": mapdl.post_processing.nodal_displacement("NORM").max(),
        "weight": props["DENS"] * total_volume,
    })
    mapdl.finish()
```

### 2c. Batch Runs (LS-DYNA)

**Problem:** Run multiple LS-DYNA simulations with varying parameters, collect results.

```python
import subprocess
import os
from itertools import product
from lasso.dyna import Binout
import pandas as pd

# Parameter grid
velocities = [5.0, 10.0, 15.0]  # m/s
thicknesses = [1.0, 1.5, 2.0]   # mm

results = []
for v, t in product(velocities, thicknesses):
    run_dir = f"run_v{v:.0f}_t{t:.1f}"
    os.makedirs(run_dir, exist_ok=True)

    # Generate keyword file with substituted parameters
    template = open("template.k").read()
    deck = template.replace("__VELOCITY__", f"{v:.4e}")
    deck = deck.replace("__THICKNESS__", f"{t:.4f}")
    with open(f"{run_dir}/input.k", "w") as f:
        f.write(deck)

    # Run solver
    subprocess.run(
        ["/path/to/ls-dyna", f"i={run_dir}/input.k"],
        cwd=run_dir, capture_output=True
    )

    # Extract peak force from binout
    binout = Binout(f"{run_dir}/binout*")
    force = binout.read("rcforc", "force")
    peak_force = abs(force).max()

    results.append({
        "velocity": v, "thickness": t,
        "peak_force": peak_force,
    })

df = pd.DataFrame(results)
df.to_csv("batch_results.csv", index=False)
```

---

## 3. Structural Optimization

### 3a. Topology Optimization (SIMP via PyMAPDL)

**Problem:** Find optimal material distribution to minimize compliance (maximize stiffness) for a given volume fraction.

```python
import numpy as np
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

# Model setup (2D cantilever beam)
mapdl.prep7()
mapdl.et(1, "PLANE182", kop1=3)  # plane stress with thickness
mapdl.mp("EX", 1, 200e3)
mapdl.mp("PRXY", 1, 0.3)
mapdl.rectng(0, 200, 0, 100)
mapdl.esize(5)
mapdl.amesh("ALL")

n_elem = mapdl.mesh.n_elem
E0 = 200e3
vol_frac = 0.4
penalization = 3  # SIMP penalty
rho = np.ones(n_elem) * vol_frac  # initial density

for iteration in range(100):
    # Update element stiffness: E_eff = rho^p * E0
    for i in range(n_elem):
        mapdl.mp("EX", i + 1, rho[i] ** penalization * E0)

    # Solve
    mapdl.run("/SOLU")
    mapdl.solve()
    mapdl.finish()
    mapdl.post1()

    # Extract element strain energies
    mapdl.etable("SE", "SENE")
    mapdl.etable("VOL", "VOLU")
    se = np.array(mapdl.pretab("SE").to_list())
    vol = np.array(mapdl.pretab("VOL").to_list())
    mapdl.finish()

    # Sensitivity
    dc = -penalization * rho ** (penalization - 1) * se / vol

    # OC update (bisection on Lagrange multiplier)
    l1, l2 = 0, 1e9
    move = 0.2
    while (l2 - l1) / (l1 + l2) > 1e-3:
        lmid = 0.5 * (l2 + l1)
        rho_new = np.maximum(0.001,
            np.maximum(rho - move,
            np.minimum(1.0,
            np.minimum(rho + move,
                rho * np.sqrt(-dc / lmid)))))
        if rho_new.sum() > vol_frac * n_elem:
            l1 = lmid
        else:
            l2 = lmid
    rho = rho_new

    compliance = se.sum()
    print(f"Iter {iteration}: compliance={compliance:.4f}")
```

### 3b. SciPy-Driven Shape Optimization

**Problem:** Optimize geometry parameters (fillet radius, hole position, etc.) to minimize stress.

```python
from scipy.optimize import minimize

def fea_objective(params):
    """Run FEA and return max stress for given geometry params."""
    fillet_r, hole_x, hole_r = params
    mapdl.clear()
    mapdl.prep7()
    # ... build geometry with fillet_r, hole at (hole_x, 50)
    #     with radius hole_r ...
    mapdl.solve()
    mapdl.post1()
    max_stress = mapdl.post_processing.nodal_eqv_stress().max()
    mapdl.finish()
    return max_stress

bounds = [(2, 20), (30, 170), (3, 15)]  # fillet_r, hole_x, hole_r
result = minimize(fea_objective, x0=[5, 100, 10],
                  method="Nelder-Mead",
                  options={"maxiter": 100, "xatol": 0.5})
print(f"Optimal: fillet_r={result.x[0]:.1f}, "
      f"hole_x={result.x[1]:.1f}, hole_r={result.x[2]:.1f}")
print(f"Min stress: {result.fun:.2f} MPa")
```

### 3c. PyOptiSLang Design Optimization

**Problem:** Full DOE → sensitivity → optimization workflow using Ansys optiSLang.

```python
from ansys.optislang.core import Optislang

osl = Optislang()
# Create project with:
# 1. Parameter definitions (ranges, distributions)
# 2. Solver node (PyMAPDL or external solver)
# 3. Response extraction
# 4. Sensitivity analysis (MOP)
# 5. Optimization (EA, gradient-based, or surrogate-based)
# See PyOptiSLang examples for complete workflows
```

---

## 4. Mesh Convergence Automation

**Problem:** Automatically determine the mesh density at which results converge (< 2% change).

```python
import numpy as np
import matplotlib.pyplot as plt
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

def run_at_esize(mapdl, esize):
    """Build, solve, extract max stress for given element size."""
    mapdl.clear()
    mapdl.prep7()

    mapdl.mp("EX", 1, 200e3)
    mapdl.mp("PRXY", 1, 0.3)
    mapdl.et(1, "SOLID186")

    # Geometry (example: plate with hole)
    # ... create geometry ...

    mapdl.esize(esize)
    mapdl.vmesh("ALL")
    n_elem = mapdl.mesh.n_elem
    n_dof = mapdl.mesh.n_node * 3

    # BCs and loads
    # ...

    mapdl.run("/SOLU")
    mapdl.antype("STATIC")
    mapdl.solve()
    mapdl.finish()

    mapdl.post1()
    max_stress = mapdl.post_processing.nodal_eqv_stress().max()
    mapdl.finish()

    return {"esize": esize, "n_elem": n_elem, "n_dof": n_dof,
            "max_stress": max_stress}

# Logarithmic spacing captures convergence behavior
esizes = np.logspace(1.5, 0.2, 15)  # 31.6 → 1.6 mm
results = [run_at_esize(mapdl, es) for es in esizes]

# Check convergence criterion
for i in range(1, len(results)):
    prev = results[i - 1]["max_stress"]
    curr = results[i]["max_stress"]
    change = abs(curr - prev) / prev * 100
    converged = "✓" if change < 2.0 else ""
    print(f"h={results[i]['esize']:.2f}: σ={curr:.2f} MPa, "
          f"Δ={change:.1f}% {converged}")

# Plot
dofs = [r["n_dof"] for r in results]
stresses = [r["max_stress"] for r in results]
plt.semilogx(dofs, stresses, "o-")
plt.xlabel("Degrees of Freedom")
plt.ylabel("Max von Mises Stress (MPa)")
plt.title("Mesh Convergence Study")
plt.grid(True)
plt.savefig("mesh_convergence.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

## 5. Thermal-Structural Coupling

### 5a. Sequential (Weak) Coupling

**Problem:** Compute thermal stresses from a known temperature field.

```python
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

# === Step 1: Thermal Analysis ===
mapdl.prep7()
mapdl.et(1, "PLANE77")         # 2D thermal element
mapdl.mp("KXX", 1, 50)         # conductivity (W/m·K)
mapdl.mp("C", 1, 500)          # specific heat (J/kg·K)
mapdl.mp("DENS", 1, 7850)      # density (kg/m³)

# ... geometry, mesh ...

# Thermal BCs
mapdl.nsel("S", "LOC", "X", 0)
mapdl.d("ALL", "TEMP", 100)     # 100°C at left edge
mapdl.allsel()
mapdl.nsel("S", "LOC", "X", 200)
mapdl.sf("ALL", "CONV", 10, 25)  # convection: h=10, T_inf=25°C
mapdl.allsel()

mapdl.run("/SOLU")
mapdl.antype("STATIC")
mapdl.solve()
mapdl.finish()

# === Step 2: Structural Analysis ===
mapdl.prep7()
mapdl.etchg("TTS")              # thermal → structural element swap
mapdl.mp("EX", 1, 200e3)        # Young's modulus
mapdl.mp("PRXY", 1, 0.3)
mapdl.mp("ALPX", 1, 12e-6)      # thermal expansion coeff

mapdl.run("/SOLU")
mapdl.antype("STATIC")
mapdl.ldread("TEMP", "", "", "", "", "file", "rth")  # load thermal results
# ... structural BCs (constrain rigid body motion) ...
mapdl.solve()
mapdl.finish()

# Post-process thermal stress
mapdl.post1()
thermal_stress = mapdl.post_processing.nodal_eqv_stress()
print(f"Max thermal stress: {thermal_stress.max():.2f} MPa")
```

### 5b. Strong (Direct) Coupling

**Problem:** Fully coupled thermo-mechanical with temperature-dependent properties.

```python
mapdl.prep7()
# Use coupled-field elements
mapdl.et(1, "SOLID226", 11)  # keyopt(1)=11 → thermo-structural

# Temperature-dependent material properties
mapdl.mptemp(1, 20, 100, 200, 300, 400, 500)
mapdl.mpdata("EX", 1, 1, 210e3, 205e3, 198e3, 190e3, 180e3, 165e3)
mapdl.mpdata("ALPX", 1, 1, 11e-6, 11.5e-6, 12e-6, 12.5e-6, 13e-6, 13.5e-6)
mapdl.mp("KXX", 1, 50)
mapdl.mp("PRXY", 1, 0.3)

# Both thermal and structural BCs applied simultaneously
# ... geometry, mesh, BCs ...
mapdl.solve()
```

---

## 6. Fatigue Automation

### 6a. Multi-Load-Case Stress Extraction

**Problem:** Extract stress results from multiple load cases for fatigue life calculation.

```python
import numpy as np
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

load_cases = [
    {"name": "gravity",   "direction": "FY", "magnitude": -9810},
    {"name": "pressure",  "direction": "PRES", "magnitude": 5.0},
    {"name": "torque",    "direction": "MZ", "magnitude": 500},
]

stress_fields = {}

for lc in load_cases:
    mapdl.clear()
    mapdl.prep7()
    # ... shared geometry, material, mesh ...

    # Apply load-case-specific loading
    if lc["direction"] == "PRES":
        mapdl.sfe("ALL", 1, "PRES", "", lc["magnitude"])
    else:
        mapdl.f("ALL", lc["direction"], lc["magnitude"])

    mapdl.run("/SOLU")
    mapdl.solve()
    mapdl.finish()

    mapdl.post1()
    stress_fields[lc["name"]] = {
        "seqv": mapdl.post_processing.nodal_eqv_stress(),
        "sx": mapdl.post_processing.nodal_component_stress("X"),
        "sy": mapdl.post_processing.nodal_component_stress("Y"),
        "sxy": mapdl.post_processing.nodal_component_stress("XY"),
    }
    mapdl.finish()
```

### 6b. Programmatic Fatigue Life Calculation

```python
def basquin_life(stress_amplitude, Sf_prime, b):
    """Basquin equation: Sa = Sf' * (2*Nf)^b → Nf = (Sa/Sf')^(1/b) / 2"""
    return 0.5 * (stress_amplitude / Sf_prime) ** (1.0 / b)

def miner_damage(stress_amplitudes, cycles, Sf_prime, b):
    """Palmgren-Miner linear damage accumulation."""
    damage = 0
    for Sa, n in zip(stress_amplitudes, cycles):
        if Sa <= 0:
            continue
        Nf = basquin_life(Sa, Sf_prime, b)
        damage += n / Nf
    return damage  # failure when D >= 1.0

def goodman_equivalent(stress_amp, stress_mean, Sut):
    """Goodman mean stress correction: Sa_eq = Sa / (1 - Sm/Sut)"""
    return stress_amp / (1 - stress_mean / Sut)

# Example: compute fatigue at critical node across load cases
Sf_prime = 800  # fatigue strength coefficient (MPa)
b = -0.12       # fatigue strength exponent
Sut = 600       # ultimate tensile strength (MPa)

# For each node, superpose load cases, extract Sa and Sm
# Then apply Goodman correction and Miner's rule
critical_node = 1234
sa_values = [stress_fields[lc]["seqv"][critical_node] / 2 for lc in load_cases]
n_cycles = [1e6, 5e5, 1e6]  # expected cycle counts

D = miner_damage(sa_values, n_cycles, Sf_prime, b)
print(f"Cumulative damage at node {critical_node}: D = {D:.4f}")
print(f"Predicted life: {1.0 / D:.0f} blocks" if D > 0 else "Infinite life")
```

---

## 7. Crash & Impact (LS-DYNA)

### 7a. Crashworthiness DOE

**Problem:** Optimize energy absorption of a thin-walled tube under axial impact.

```python
import numpy as np
import pandas as pd
from scipy.stats.qmc import LatinHypercube, scale
from lasso.dyna import Binout
import subprocess
import os

# Parameters: wall thickness, trigger size, material yield
l_bounds = [1.0, 2.0, 200]
u_bounds = [3.0, 8.0, 400]

sampler = LatinHypercube(d=3)
designs = scale(sampler.random(n=30), l_bounds, u_bounds)

results = []
for i, (t, trigger, sigy) in enumerate(designs):
    run_dir = f"crash_run_{i:03d}"
    os.makedirs(run_dir, exist_ok=True)

    # Generate keyword file
    deck = generate_crush_tube_deck(
        thickness=t,
        trigger_depth=trigger,
        yield_stress=sigy,
        impact_velocity=10.0,  # m/s
        termination=0.05,      # 50 ms
    )
    with open(f"{run_dir}/crush.k", "w") as f:
        f.write(deck)

    # Run LS-DYNA
    subprocess.run(["ls-dyna", f"i=crush.k"], cwd=run_dir,
                    capture_output=True)

    # Post-process
    binout = Binout(f"{run_dir}/binout*")
    time = binout.read("glstat", "time")
    ie = binout.read("glstat", "internal_energy")
    ke = binout.read("glstat", "kinetic_energy")

    # Metrics
    energy_absorbed = ie[-1]
    peak_force = binout.read("rwforc", "force").max()
    mean_force = energy_absorbed / 0.15  # crush distance estimate
    cfe = mean_force / peak_force  # crush force efficiency

    results.append({
        "thickness": t, "trigger": trigger, "yield_stress": sigy,
        "energy_absorbed": energy_absorbed,
        "peak_force": peak_force,
        "cfe": cfe,
    })

df = pd.DataFrame(results)
df.to_csv("crashworthiness_doe.csv", index=False)

# Find Pareto front: maximize energy, minimize peak force
# ... multi-objective optimization on surrogate ...
```

### 7b. Metal Forming Optimization

**Problem:** Optimize blank holder force and draw bead geometry to minimize thinning in a stamping process.

```python
# Similar DOE pattern as 7a, but:
# - Parameters: blank holder force, friction coefficient, draw bead height
# - Response: max thinning (%), springback angle, wrinkle indicator
# - Solver: LS-DYNA with *MAT_037 (transversely anisotropic elastic-plastic)
# - Post-process: d3plot shell thickness strain

from lasso.dyna import D3plot, ArrayType

d3plot = D3plot("forming_run/d3plot")
thickness_strain = d3plot.arrays[ArrayType.element_shell_thickness]
# thickness_strain shape: (n_timesteps, n_shells)
final_thinning = (1 - thickness_strain[-1, :]) * 100  # percent
max_thinning = final_thinning.max()
```

### 7c. Occupant Safety

**Problem:** Evaluate head injury criterion (HIC) from an impact simulation.

```python
from lasso.dyna import Binout
import numpy as np

binout = Binout("occupant_run/binout*")
time = binout.read("nodout", "time")
accel_x = binout.read("nodout", "x_acceleration")  # head CG node
accel_y = binout.read("nodout", "y_acceleration")
accel_z = binout.read("nodout", "z_acceleration")

# Resultant acceleration in g's
g = 9810  # mm/s²
accel_res = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2) / g

def compute_hic(time, accel_g, window=0.015):
    """Compute Head Injury Criterion (HIC15)."""
    dt = np.diff(time)
    hic_max = 0
    for i in range(len(time)):
        for j in range(i + 1, len(time)):
            delta_t = time[j] - time[i]
            if delta_t > window:
                break
            if delta_t < 1e-6:
                continue
            integral = np.trapz(accel_g[i:j+1], time[i:j+1])
            avg_a = integral / delta_t
            hic = delta_t * avg_a ** 2.5
            hic_max = max(hic_max, hic)
    return hic_max

hic15 = compute_hic(time, accel_res, window=0.015)
print(f"HIC15 = {hic15:.1f}")
print(f"{'PASS' if hic15 < 700 else 'FAIL'} (limit: 700)")
```

---

## 8. Surrogate Modeling

### 8a. Full Pipeline: FEA → Surrogate → Optimization

**Problem:** Replace expensive FEA evaluations with a fast surrogate model for design optimization.

```python
import numpy as np
import pandas as pd
from scipy.stats.qmc import LatinHypercube, scale
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel
from scipy.optimize import differential_evolution

# ── Step 1: Define parameter space ──
param_names = ["thickness", "fillet_radius", "hole_diameter"]
l_bounds = [1.0, 2.0, 5.0]
u_bounds = [8.0, 15.0, 30.0]

# ── Step 2: Generate DOE samples ──
sampler = LatinHypercube(d=3)
X_train = scale(sampler.random(n=40), l_bounds, u_bounds)

# ── Step 3: Run FEA for each sample ──
Y_stress = np.array([run_fea_stress(*x) for x in X_train])
Y_mass = np.array([compute_mass(*x) for x in X_train])

# ── Step 4: Train surrogate models ──
kernel = ConstantKernel() * Matern(nu=2.5, length_scale=[1.0] * 3)

gpr_stress = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
gpr_stress.fit(X_train, Y_stress)

gpr_mass = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
gpr_mass.fit(X_train, Y_mass)

# ── Step 5: Optimize on surrogate (instant evaluations) ──
def surrogate_objective(x):
    mass_pred = gpr_mass.predict(x.reshape(1, -1))[0]
    stress_pred, stress_std = gpr_stress.predict(
        x.reshape(1, -1), return_std=True
    )
    # Conservative: use mean + 2*std
    stress_upper = stress_pred[0] + 2 * stress_std[0]
    penalty = max(0, stress_upper - 300) ** 2 * 1000
    return mass_pred + penalty

bounds_opt = list(zip(l_bounds, u_bounds))
result = differential_evolution(surrogate_objective, bounds_opt,
                                 maxiter=200, seed=42)

print(f"Optimal design: {dict(zip(param_names, result.x))}")
print(f"Predicted mass: {gpr_mass.predict(result.x.reshape(1,-1))[0]:.2f}")

# ── Step 6: Validate optimum with actual FEA ──
actual_stress = run_fea_stress(*result.x)
predicted_stress = gpr_stress.predict(result.x.reshape(1, -1))[0]
error = abs(actual_stress - predicted_stress) / actual_stress * 100
print(f"Surrogate error at optimum: {error:.1f}%")
```

### 8b. Adaptive Sampling (Bayesian Optimization)

For higher accuracy with fewer FEA evaluations, use Bayesian optimization to intelligently select new sample points:

```python
from smt.surrogate_models import KRG
from smt.sampling_methods import LHS
import numpy as np

xlimits = np.array([l_bounds, u_bounds]).T

# Initial samples
sampling = LHS(xlimits=xlimits)
X = sampling(20)
Y = np.array([run_fea_stress(*x) for x in X])

for iteration in range(20):
    # Train Kriging
    sm = KRG(theta0=[1e-2] * 3, print_global=False)
    sm.set_training_values(X, Y.reshape(-1, 1))
    sm.train()

    # Find point with maximum predicted uncertainty
    candidates = scale(sampler.random(n=1000), l_bounds, u_bounds)
    variances = sm.predict_variances(candidates)
    next_idx = np.argmax(variances)
    x_new = candidates[next_idx]

    # Evaluate FEA at new point
    y_new = run_fea_stress(*x_new)
    X = np.vstack([X, x_new])
    Y = np.append(Y, y_new)

    print(f"Iter {iteration}: added point, max variance = "
          f"{variances[next_idx]:.2f}")
```

This converges faster than uniform DOE because it focuses samples where the surrogate is least certain.
