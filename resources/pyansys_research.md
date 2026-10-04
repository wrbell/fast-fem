# PyAnsys & PyDYNA Ecosystem Research

Comprehensive guide to using Python APIs for Ansys MAPDL and LS-DYNA automation, parametric studies, and post-processing.

**Related files:**
- [pyansys_references.md](pyansys_references.md) — link collection
- [pyansys_applications.md](pyansys_applications.md) — practical project patterns

---

## Table of Contents

1. [PyAnsys Overview](#pyansys-overview)
2. [PyMAPDL](#pymapdl)
3. [PyDPF](#pydpf)
4. [PyDYNA](#pydyna)
5. [LASSO-Python](#lasso-python)
6. [Iterative Study Patterns](#iterative-study-patterns)
7. [Workbench Scripting](#workbench-scripting)
8. [Installation & Setup](#installation--setup)

---

## PyAnsys Overview

PyAnsys is a family of open-source Python packages providing programmatic access to the Ansys simulation stack. All packages are MIT-licensed, use gRPC for client-server communication, and follow a consistent API design.

**Core packages:**

| Package | PyPI Name | Purpose |
|---------|-----------|---------|
| PyMAPDL | `ansys-mapdl-core` | MAPDL solver control (pre/solve/post) |
| PyDPF-Core | `ansys-dpf-core` | Operator-based result extraction |
| PyDPF-Post | `ansys-dpf-post` | High-level postprocessing API |
| PyDYNA | `ansys-dyna-core` | LS-DYNA keyword building & solver |
| PyMechanical | `ansys-mechanical-core` | Mechanical GUI automation |
| PyOptiSLang | `ansys-optislang-core` | Design optimization (DOE, RDO) |

**Documentation portal:** https://docs.pyansys.com/

---

## PyMAPDL

The primary tool for scripting ANSYS MAPDL from Python. Replaces APDL macro files with Pythonic workflows.

### Launch & Connect

```python
from ansys.mapdl.core import launch_mapdl

# Launch local instance
mapdl = launch_mapdl(nproc=4, run_location="/tmp/mapdl_run")

# Connect to running instance (remote or Docker)
from ansys.mapdl.core import Mapdl
mapdl = Mapdl(ip="192.168.1.100", port=50052)
```

**Key launch parameters:**
- `nproc` — number of CPU cores (default 2)
- `run_location` — working directory for result files
- `jobname` — MAPDL job name (default "file")
- `loglevel` — "ERROR", "WARNING", "INFO", "DEBUG"
- `additional_switches` — extra MAPDL flags (e.g., `-smp` for shared memory)

### Core Workflow

```python
# === PREPROCESSING ===
mapdl.prep7()

# Material
mapdl.mp("EX", 1, 200e3)    # Young's modulus (MPa)
mapdl.mp("PRXY", 1, 0.3)    # Poisson's ratio
mapdl.mp("DENS", 1, 7.85e-9) # Density (tonne/mm³)

# Geometry (direct or from file)
mapdl.block(0, 100, 0, 50, 0, 10)  # create block
# or: mapdl.cdread("db", "model", "cdb")

# Element type and mesh
mapdl.et(1, "SOLID186")      # 20-node hex
mapdl.esize(5)               # element size
mapdl.vmesh("ALL")

# Boundary conditions
mapdl.nsel("S", "LOC", "X", 0)
mapdl.d("ALL", "ALL", 0)     # fix all DOF
mapdl.allsel()

# Loads
mapdl.nsel("S", "LOC", "X", 100)
mapdl.f("ALL", "FX", 1000)   # nodal force
mapdl.allsel()

# === SOLVING ===
mapdl.run("/SOLU")
mapdl.antype("STATIC")
mapdl.solve()
mapdl.finish()

# === POSTPROCESSING ===
mapdl.post1()

# Nodal results (returns numpy arrays)
disp = mapdl.post_processing.nodal_displacement("X")
stress = mapdl.post_processing.nodal_eqv_stress()
print(f"Max displacement: {disp.max():.4f} mm")
print(f"Max von Mises: {stress.max():.2f} MPa")

# Plot
mapdl.post_processing.plot_nodal_eqv_stress(cpos="iso")
```

### Parameter Management

```python
# Set parameters
mapdl.parameters["my_load"] = 5000
mapdl.parameters["thickness"] = 2.5

# Get parameters
load = mapdl.parameters["my_load"]

# Use in APDL commands
mapdl.run("F,ALL,FY,%my_load%")

# Access mesh info
n_nodes = mapdl.mesh.n_node
n_elem = mapdl.mesh.n_elem
nodes = mapdl.mesh.nodes  # (n, 3) numpy array
```

### Extracting Results as Arrays

```python
mapdl.post1()

# Stress components
sx = mapdl.post_processing.nodal_component_stress("X")
sy = mapdl.post_processing.nodal_component_stress("Y")
sz = mapdl.post_processing.nodal_component_stress("Z")
sxy = mapdl.post_processing.nodal_component_stress("XY")

# Principal stresses
s1 = mapdl.post_processing.nodal_principal_stress("1")
s3 = mapdl.post_processing.nodal_principal_stress("3")

# Strain
eqv_strain = mapdl.post_processing.nodal_eqv_strain()

# Element results via ETABLE
mapdl.etable("SVOL", "VOLU")
mapdl.etable("SSE", "SENE")  # strain energy
```

### Performance Tips

- **Suppress graphical output** during batch runs: `mapdl.run("/NOPR")` and `mapdl.graphics("OFF")`
- **Reuse mesh** — only clear loads/BCs between parameter sweeps, not the entire model
- **Use `mapdl.clear()` sparingly** — it restarts the database; prefer `mapdl.run("FDELE,ALL,ALL")` to clear loads
- **Write results to arrays**, not text — `post_processing` properties return numpy arrays directly
- **SMP mode** for Student Edition — `launch_mapdl(additional_switches="-smp")` since HPC/DMP requires a license

---

## PyDPF

Data Processing Framework — a separate result-reading engine that works with any Ansys result file (.rst, .rth, d3plot, binout).

### PyDPF-Core (Operator-Based)

Low-level, flexible API where you chain operators to build processing pipelines.

```python
from ansys.dpf import core as dpf

# Load result file
model = dpf.Model("file.rst")
print(model)  # summary of available results

# Extract von Mises stress
stress_op = model.results.stress()
vm_op = dpf.operators.invariant.von_mises_eqv(stress_op)
vm_field = vm_op.outputs.fields_container()[0]

print(f"Max von Mises: {vm_field.data.max():.2f} MPa")

# Chain operators
norm_op = dpf.operators.math.norm(model.results.displacement())
disp_norm = norm_op.outputs.fields_container()[0]
```

**Operator categories:**
- `result` — read specific results (stress, displacement, temperature)
- `math` — arithmetic, norms, dot products
- `invariant` — von Mises, principal stresses, tresca
- `filter` — scoping by node/element sets
- `mesh` — mesh operations, skinning, node/element extraction
- `utility` — data manipulation, merging fields

### PyDPF-Post (High-Level)

Physics-oriented API built on DPF-Core. Simpler for common tasks.

```python
from ansys.dpf import post

# Load and explore
simulation = post.StaticMechanicalSimulation("file.rst")

# Get displacement dataframe
disp_df = simulation.displacement(components=["X", "Y", "Z"])
print(disp_df)

# Get stress with element scoping
stress_df = simulation.stress_eqv_von_mises(element_ids=[1, 2, 3])

# Named selections
stress_at_fillet = simulation.stress_eqv_von_mises(
    named_selections=["fillet_region"]
)
```

### Reading LS-DYNA Results with DPF

DPF can read d3plot and binout files directly:

```python
from ansys.dpf import core as dpf

# Read d3plot
ds = dpf.DataSources()
ds.set_result_file_path("d3plot", "d3plot")
model = dpf.Model(ds)

# Extract displacement at all time steps
disp_op = model.results.displacement()
disp_fc = disp_op.outputs.fields_container()
for i, field in enumerate(disp_fc):
    print(f"Step {i}: max disp = {field.data.max():.4f}")
```

---

## PyDYNA

Python API for building LS-DYNA keyword input decks, running the solver, and post-processing.

### Keyword Construction

```python
from ansys.dyna.core.pre import DynaMech, DynaMaterial
from ansys.dyna.core.pre.dynamaterial import MatElastic, MatPiecewiseLinearPlasticity

# Create mechanical analysis
analysis = DynaMech()

# Define materials
mat_steel = MatPiecewiseLinearPlasticity(
    mid=1, ro=7.85e-9, e=200e3, pr=0.3, sigy=250,
    lcss=1  # load curve ID for hardening
)
analysis.add(mat_steel)

# Set termination
analysis.set_termination(endtime=0.01)

# Database output controls
analysis.set_output_database(
    glstat=1e-4,   # global statistics interval
    matsum=1e-4,   # material energies interval
    nodout=1e-4,   # nodal output interval
    elout=1e-4     # element output interval
)

# Write keyword file
analysis.save_file("model.k")
```

### Direct Keyword File Construction (Manual)

For full control, build keyword files as strings:

```python
def build_keyword_deck(E, sigy, thickness, termination):
    """Build a minimal LS-DYNA keyword deck."""
    deck = f"""*KEYWORD
*TITLE
Parametric study: E={E}, sigy={sigy}, t={thickness}
*CONTROL_TERMINATION
$  ENDTIM    ENDCYC     DTMIN    ENDENG    ENDMAS
  {termination:.6e}         0       0.0       0.0       0.0
*MAT_PIECEWISE_LINEAR_PLASTICITY
$      MID        RO         E        PR      SIGY      ETAN
         1  7.85E-09  {E:.4e}       0.3  {sigy:.4e}       0.0
*SECTION_SHELL
$    SECID    ELFORM      SHRF       NIP     PROPT
         1         2       1.0         5       0.0
$       T1        T2        T3        T4
  {thickness:.4f}  {thickness:.4f}  {thickness:.4f}  {thickness:.4f}
*DATABASE_GLSTAT
$       DT
  1.000E-04
*DATABASE_BINARY_D3PLOT
$       DT      LCDT
  5.000E-04         0
*END
"""
    return deck

# Write for each parameter combination
for E in [180e3, 200e3, 220e3]:
    for sigy in [200, 250, 300]:
        deck = build_keyword_deck(E, sigy, 2.0, 0.01)
        fname = f"run_E{E:.0f}_sigy{sigy:.0f}.k"
        with open(fname, "w") as f:
            f.write(deck)
```

### Solver Execution

```python
import subprocess
import os

def run_lsdyna(input_file, ncpus=4, memory="200m"):
    """Run LS-DYNA solver on a keyword file."""
    cmd = [
        "ls-dyna_smp_s_R13.1",  # solver executable
        f"i={input_file}",
        f"ncpu={ncpus}",
        f"memory={memory}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0
```

### Post-Processing d3plot/binout

See [LASSO-Python](#lasso-python) below for the recommended approach.

---

## LASSO-Python

Fast, open-source reader/writer for LS-DYNA d3plot and binout files. Recommended over the archived qd-cae-python.

### d3plot Reading

```python
from lasso.dyna import D3plot, ArrayType, FilterType

# Read d3plot (handles multi-file d3plot, d3plot01, d3plot02, ...)
d3plot = D3plot("path/to/d3plot")

# Available array types
print(D3plot.arrays.keys())

# Node displacement — shape: (n_timesteps, n_nodes, 3)
disp = d3plot.arrays[ArrayType.node_displacement]
print(f"Timesteps: {disp.shape[0]}, Nodes: {disp.shape[1]}")

# Shell stress — shape: (n_timesteps, n_shells, n_layers, 6)
shell_stress = d3plot.arrays[ArrayType.element_shell_stress]

# Effective plastic strain
eps_p = d3plot.arrays[ArrayType.element_shell_effective_plastic_strain]

# Node coordinates (reference config)
coords = d3plot.arrays[ArrayType.node_coordinates]

# Part IDs
part_ids = d3plot.arrays[ArrayType.element_shell_part_indexes]

# Filter by part (read only specific parts — saves memory)
d3plot_filtered = D3plot(
    "path/to/d3plot",
    state_filter=FilterType.SHELL,
)
```

### binout Reading

```python
from lasso.dyna import Binout

# Read binout (supports wildcards for split files)
binout = Binout("path/to/binout*")

# List available categories
print(binout.read())  # e.g., ['glstat', 'matsum', 'nodout', ...]

# Global statistics
glstat = binout.read("glstat")
print(glstat.keys())  # 'time', 'eroded_kinetic_energy', ...

time = binout.read("glstat", "time")
ke = binout.read("glstat", "kinetic_energy")
ie = binout.read("glstat", "internal_energy")

# Plot energy balance
import matplotlib.pyplot as plt
plt.plot(time, ke, label="Kinetic")
plt.plot(time, ie, label="Internal")
plt.plot(time, ke + ie, label="Total")
plt.xlabel("Time (s)")
plt.ylabel("Energy")
plt.legend()
plt.title("Energy Balance")
plt.show()

# Contact forces
rcforc_time = binout.read("rcforc", "time")
rcforc_force = binout.read("rcforc", "force")
```

### Comparison of LS-DYNA Python Readers

| Library | d3plot | binout | Keyword | Status | Speed |
|---------|--------|--------|---------|--------|-------|
| **lasso-python** | Read/Write | Read/Write | No | Active | Fast (C backend) |
| **qd-cae-python** | Read | Read | Read | Archived | Fast (C++ backend) |
| **lsreader** | Read | Read | No | Inactive | Moderate |
| **PyDPF** | Read | Read | No | Active | Moderate |

**Recommendation:** Use lasso-python for d3plot/binout I/O and PyDYNA for keyword generation.

---

## Iterative Study Patterns

### Mesh Convergence

```python
import numpy as np
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

def solve_at_esize(esize):
    mapdl.clear()
    mapdl.prep7()
    # ... geometry, material, element type setup ...
    mapdl.esize(esize)
    mapdl.vmesh("ALL")
    # ... boundary conditions, loads ...
    mapdl.run("/SOLU")
    mapdl.antype("STATIC")
    mapdl.solve()
    mapdl.finish()
    mapdl.post1()
    max_stress = mapdl.post_processing.nodal_eqv_stress().max()
    n_dof = mapdl.mesh.n_node * 3
    mapdl.finish()
    return n_dof, max_stress

# Logarithmic spacing — captures convergence behavior well
element_sizes = np.logspace(1.5, 0.3, 12)  # coarse → fine
results = [solve_at_esize(es) for es in element_sizes]
dofs, stresses = zip(*results)

# Convergence criterion: < 2% change between successive refinements
for i in range(1, len(stresses)):
    change = abs(stresses[i] - stresses[i-1]) / stresses[i-1] * 100
    print(f"h={element_sizes[i]:.2f}: σ={stresses[i]:.2f} MPa, "
          f"Δ={change:.2f}%")
```

### Material Sweeps

```python
import pandas as pd
import numpy as np

E_values = np.linspace(150e3, 250e3, 10)
results = []

for E in E_values:
    mapdl.clear()
    mapdl.prep7()
    # ... geometry, mesh (reuse same mesh) ...
    mapdl.mp("EX", 1, E)
    mapdl.mp("PRXY", 1, 0.3)
    # ... BCs, loads, solve ...
    mapdl.solve()
    mapdl.post1()
    max_disp = mapdl.post_processing.nodal_displacement("NORM").max()
    max_stress = mapdl.post_processing.nodal_eqv_stress().max()
    results.append({"E": E, "max_disp": max_disp, "max_stress": max_stress})
    mapdl.finish()

df = pd.DataFrame(results)
df.to_csv("material_sweep.csv", index=False)
```

### DOE (Design of Experiments)

```python
from scipy.stats.qmc import LatinHypercube, scale
import numpy as np

# Define parameter space
param_names = ["E", "yield_stress", "thickness"]
l_bounds = [150e3, 200, 1.0]
u_bounds = [250e3, 400, 5.0]

# Generate LHS samples
sampler = LatinHypercube(d=len(param_names))
sample = sampler.random(n=50)
designs = scale(sample, l_bounds, u_bounds)

# Run FEA for each design point
results = []
for i, params in enumerate(designs):
    E, sigy, t = params
    # ... build model, solve, extract response ...
    response = run_fea(E, sigy, t)
    results.append({**dict(zip(param_names, params)), **response})
    print(f"Run {i+1}/50 complete")

df = pd.DataFrame(results)
df.to_csv("doe_results.csv", index=False)
```

### Optimization Loop

```python
from scipy.optimize import minimize, differential_evolution

def objective(params):
    """Minimize mass subject to stress constraint."""
    thickness, radius = params
    # ... build and solve model ...
    mass = compute_mass(thickness, radius)
    max_stress = compute_max_stress(thickness, radius)

    # Penalty for stress constraint violation
    stress_limit = 300.0  # MPa
    penalty = max(0, max_stress - stress_limit) ** 2 * 1e3
    return mass + penalty

bounds = [(1.0, 10.0), (5.0, 50.0)]

# Derivative-free global optimization (best for FEA)
result = differential_evolution(objective, bounds, maxiter=50, seed=42)
print(f"Optimal: thickness={result.x[0]:.2f}, radius={result.x[1]:.2f}")
print(f"Min mass: {result.fun:.2f}")
```

### Surrogate Modeling Pipeline

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
import numpy as np

# 1. Generate training data from FEA (expensive)
X_train = designs           # from DOE above
Y_train = np.array([r["max_stress"] for r in results])

# 2. Train surrogate (cheap)
kernel = ConstantKernel() * RBF(length_scale=[1.0] * 3)
gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
gpr.fit(X_train, Y_train)

# 3. Predict on dense grid (instant)
X_test = scale(sampler.random(n=10000), l_bounds, u_bounds)
Y_pred, Y_std = gpr.predict(X_test, return_std=True)

# 4. Find optimum on surrogate
best_idx = np.argmin(Y_pred)
print(f"Predicted optimum: {X_test[best_idx]}")
print(f"Predicted stress: {Y_pred[best_idx]:.2f} ± {Y_std[best_idx]:.2f}")

# 5. Validate optimum with actual FEA
actual = run_fea(*X_test[best_idx])
print(f"Actual stress: {actual['max_stress']:.2f}")
```

---

## Workbench Scripting

### IronPython vs CPython

| Aspect | IronPython (legacy) | CPython (PyAnsys) |
|--------|--------------------|--------------------|
| Runtime | .NET CLR, embedded in Workbench | Standard CPython, out-of-process |
| Version | 2.7 | 3.9–3.13 |
| NumPy/SciPy | Not available (no C extensions) | Full support |
| Use case | GUI automation, ACT extensions | Scripting, parametric studies, CI/CD |
| Package | Built into Mechanical | `pip install ansys-mechanical-core` |

**Recommendation:** For new automation work, use PyMechanical (CPython) over internal IronPython scripting. PyMechanical exposes the same API but runs in standard CPython with full package access.

### ACT (ANSYS Customization Toolkit)

ACT allows building custom extensions for Ansys Mechanical using XML + IronPython:
- Define custom UI elements, simulation objects, and result types
- Embed third-party tools directly into the Ansys GUI
- Extensions packaged as `.wbex` files for distribution

ACT is relevant for building reusable tools within the Workbench GUI. For batch/headless automation, PyMAPDL or PyMechanical are better choices.

### PyMechanical

```python
from ansys.mechanical.core import launch_mechanical

mechanical = launch_mechanical()

# Run Mechanical scripting commands
output = mechanical.run_python_script("""
import Ansys
model = DataModel.Project.Model
static = model.Analyses[0]
solution = static.Solution
solution.Solve(True)
""")
```

---

## Installation & Setup

### Basic Install

```bash
# Core packages
pip install ansys-mapdl-core
pip install ansys-dpf-core ansys-dpf-post

# LS-DYNA tools
pip install ansys-dyna-core
pip install lasso-python

# Optimization/DOE
pip install pyDOE2 scipy scikit-learn

# Surrogate modeling
pip install smt  # Surrogate Modeling Toolbox
```

### Prerequisites

- **ANSYS installation required** for PyMAPDL (needs MAPDL solver binary)
- **LS-DYNA installation required** for PyDYNA solver execution
- **No installation required** for lasso-python (pure result reading)
- **No installation required** for PyDPF-Post with DPF server

### WSL2 Notes (Dell Precision 5860)

- PyMAPDL can launch MAPDL on Windows from WSL2 via `launch_mapdl(exec_file="/path/to/mapdl.exe")`
- Alternatively, run PyMAPDL natively on Windows and connect from WSL2 via gRPC
- lasso-python works fully in WSL2 (no solver dependency)
- For best performance, keep result files on the same filesystem as the reader (avoid cross-OS file access on `/mnt/`)
