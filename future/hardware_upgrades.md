# Hardware Upgrade Path

Upgrade priority for the Dell Precision 5860 as simulation needs grow beyond ANSYS Student Edition. Reference: plan/config.md for current specs.

---

## Current Specs

| Component | Current | Rating for Student Edition |
|-----------|---------|--------------------------|
| CPU | Xeon W3-2425 (6c/12t) | More than adequate |
| RAM | 64GB DDR5-4800 (4×16GB, 4 slots empty) | Overkill |
| GPU | RTX 2000 Ada 16GB | Fine (display only) |
| Storage | NVMe Gen4 | No issues |

---

## Upgrade 1: CPU (Biggest Impact)

**When:** Moving to research/commercial ANSYS license with models > 128K elements.

**Why:** ANSYS solve time scales almost linearly with core count. Going from 6 to 24 cores ≈ 4× faster solves.

**Options for Dell 5860 (W3/W5/W7 socket):**

| CPU | Cores | Threads | Base/Turbo | TDP | Approx Cost |
|-----|-------|---------|------------|-----|-------------|
| W3-2425 (current) | 6 | 12 | 3.0/4.4 GHz | 130W | — |
| W5-2455X | 12 | 24 | 3.2/4.6 GHz | 200W | ~$800 |
| W5-2465X | 16 | 32 | 3.1/4.7 GHz | 200W | ~$1,200 |
| W7-2495X | 24 | 48 | 2.5/4.8 GHz | 225W | ~$2,400 |

**Recommendation:** W5-2465X (16 cores) is the sweet spot — 2.5× more cores for ~$1,200, fits within 5860 cooling. W7-2495X if budget allows.

**What it unlocks:**
- ANSYS Mechanical: linear static on 500K+ elements in seconds
- Fluent: 1M+ cells with good per-core cell count
- DMP (Distributed Memory Parallel): efficient at 12+ cores
- Parametric sweeps and DOE run much faster

---

## Upgrade 2: RAM

**When:** Running models with > 500K elements, or large assemblies, or Fluent meshes > 1M cells.

**Why:** ANSYS Mechanical uses ~1–2 GB per 100K elements (sparse direct solver). Fluent uses ~0.5–1 GB per 100K cells. Running out of RAM forces paging to disk → 100× slower.

**Current:** 64GB in 4×16GB, with 4 empty DIMM slots.

**Options:**

| Config | Total | Cost | When |
|--------|-------|------|------|
| Add 4×16GB | 128GB | ~$150 | Models up to ~2M elements |
| Replace all with 8×32GB | 256GB | ~$600 | Large assemblies, DOE with many simultaneous runs |

**Recommendation:** Add 4×16GB (same spec: DDR5-4800 RDIMM ECC) for $150. Easiest win.

---

## Upgrade 3: GPU

**When:** You have a CFD Enterprise or HPC Ultimate license AND regularly run Fluent models > 1M cells.

**Why:** Fluent GPU solver can be 5–10× faster than CPU on large meshes. But requires:
1. GPU with sufficient FP64 performance (not RTX 2000 Ada)
2. Correct ANSYS license tier (not Student Edition)

**Options for PCIe slot in Dell 5860:**

| GPU | VRAM | FP64 (TFLOPS) | Power | Approx Cost |
|-----|------|---------------|-------|-------------|
| RTX 2000 Ada (current) | 16GB | ~0.2 (emulated) | 70W | — |
| RTX 4000 Ada | 20GB | ~0.4 (emulated) | 130W | ~$1,250 |
| RTX 5000 Ada | 32GB | ~0.6 (emulated) | 250W | ~$4,000 |
| RTX 6000 Ada | 48GB | ~1.3 (emulated) | 300W | ~$6,800 |

**Recommendation:** RTX 4000 Ada is the practical entry point. Only worth it with the right license. Don't upgrade until you've confirmed the license situation.

**What it unlocks:**
- Fluent GPU solver: 5–10× speedup on large steady-state cases
- Multi-GPU possible (add second card) for very large transient cases
- Better visualization performance for complex post-processing

---

## Upgrade 4: Storage

**When:** Running transient simulations or DOE studies that produce hundreds of GB of result files.

**Current:** NVMe Gen4 SSD (check capacity).

**If running low:**
- Add a second NVMe Gen4 drive (2TB: ~$120)
- Dedicate it as the ANSYS scratch directory (Workbench > Tools > Options > Directories)
- Keeps result file I/O off the OS drive

---

## Upgrade Priority Summary

| Priority | Upgrade | Cost | Impact | Trigger |
|----------|---------|------|--------|---------|
| 1 | CPU (W5-2465X) | ~$1,200 | 2.5× solve speed | Research ANSYS license |
| 2 | RAM (+64GB) | ~$150 | Enables large models | Models > 500K elements |
| 3 | GPU (RTX 4000 Ada) | ~$1,250 | 5–10× Fluent GPU | CFD Enterprise license |
| 4 | Storage (+2TB NVMe) | ~$120 | Prevents disk bottleneck | Transient/DOE studies |

**Total for upgrades 1+2+4:** ~$1,470 — transforms the machine from Student Edition workstation to capable research platform.

---

*Reference: plan/config.md for current hardware details and ANSYS settings.*
