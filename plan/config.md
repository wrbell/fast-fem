# Hardware Configuration

## Workstation: Dell Precision 5860 Tower
- ISV-certified for ANSYS

### CPU
- Intel Xeon W3-2425 (6 cores / 12 threads, 3.0–4.4 GHz Turbo, 130W, 15MB cache)
- Recommend using 4–5 cores for ANSYS solver, leaving 1–2 for OS/UI

### Memory
- 64GB DDR5-4800 RDIMM ECC (4x16GB)
- 4 empty DIMM slots — expandable to 128GB+
- 64GB is well above what ANSYS Student Edition element limits will ever demand

### GPU
- NVIDIA RTX 2000 Ada Generation 16GB GDDR6 ECC
- 2,816 CUDA cores (Ada Lovelace)
- **Use for display/visualization only** — lacks FP64 cores, so GPU-accelerated solving (Fluent, Mechanical) will be slow
- Keep ANSYS GPU solver **disabled**; rely on CPU solver

### Storage
- NVMe Gen4 SSD (check capacity with `wmic diskdrive get model,size`)
- Fast storage helps with large result files and mesh I/O

## ANSYS Student Edition Limits
These element count caps — not hardware — are the real bottleneck:
- Mechanical: ~128,000 nodes/elements
- Fluent: ~512,000 cells
- CFX: ~512,000 nodes
- HFSS: ~100,000 elements

## Recommended ANSYS Workbench Settings
1. **Solver cores**: Set to 4–5 (Tools > Solve Process Settings > Advanced > Max Number of Cores)
2. **GPU solver**: Disable (Mechanical > Analysis Settings > GPU Acceleration = Off)
3. **Memory**: Default allocation is fine; 64GB gives headroom for mesh convergence studies
4. **Distributed solve (DMP)**: Not needed with 6 cores — use shared-memory parallel (SMP) instead

## Performance Expectations

### ANSYS Mechanical (Structural/Thermal)
- ~95.5% multi-core efficiency (Puget Systems benchmarks)
- Student Edition models (up to 128K elements): **seconds to low minutes** for linear static and modal analysis
- Nonlinear (plasticity, contact, large deformation): slower but manageable at Student Edition element counts
- 4.4 GHz single-thread turbo helps — Mechanical's sparse direct solver (APDL) has serial bottlenecks where clock speed matters

### ANSYS Fluent (CFD)
- ~98.4% multi-core efficiency — scales better than Mechanical (Puget Systems benchmarks)
- ANSYS rule of thumb: **50K–100K cells per core**
- 6 cores × 85K cells = ~512K cells — lines up with the Student Edition cap
- Memory: 8GB/core recommended, we have ~10.7GB/core — above target

### GPU (RTX 2000 Ada)
- Fluent GPU solver requires CFD Enterprise or HPC Ultimate license — Student Edition does not include it
- Even with the right license, this GPU lacks FP64 cores — double-precision solving runs at ~half speed via FP32 emulation
- Use for visualization/rendering only
- Upgrade path if needed later: RTX 4000 Ada (~$1,250, 20GB) is the practical entry point for GPU-accelerated CFD

### Honest Assessment

| Component | Spec | For Student Edition | For research/commercial |
|-----------|------|--------------------|-----------------------|
| CPU (6 cores) | Entry-level Xeon W for this chassis | More than adequate | Bottleneck — upgrade to W5/W7 (16–24 cores) |
| RAM (64GB) | 10.7 GB/core | Overkill for element limits | Sufficient up to ~2M elements |
| GPU (16GB) | No FP64, no GPU solver license | Fine (display only) | Need RTX 4000 Ada+ and Enterprise license |
| Storage (NVMe Gen4) | Fast I/O for result files | No issues | No issues |

### Upgrade Priority (if moving beyond Student Edition)
1. CPU — W7-2495X (24 cores) fits this chassis, biggest impact on solve times
2. RAM — 4 empty DIMM slots, expand to 128GB+ for large models
3. GPU — RTX 4000 Ada ($1,250) only worthwhile with CFD Enterprise license

## Planning Implications
- **Mesh convergence studies**: Run freely — 64GB can handle Student Edition max element counts many times over
- **Parameter sweeps**: With 6 cores and fast storage, batch runs of multiple configurations are practical
- **CFD (Fluent)**: CPU solver with 4–5 cores is well-matched to the 512K cell Student Edition cap. Expect solve times of minutes, not hours
- **Coupled multi-physics (Week 10–12)**: Memory is sufficient; solve times will be the constraint — keep meshes efficient
- **No GPU solver workflows**: Student Edition doesn't include the required license tier anyway
