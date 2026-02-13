# Summer 2026 Roadmap

**Timeline:** ~May 5 – Aug 15 (14 weeks)
**Budget:** 15 hrs/week alongside internship (~210 total hours)
**Premise:** Fast-FEM 9-week program is complete. Three course projects submitted. ANSYS fundamentals are solid.

---

## Objectives

After Fast-FEM you can follow an ANSYS tutorial and validate the result. That's a foundation — not a skill set. The summer closes five gaps:

### 1. Work without a tutorial
Set up, solve, and validate a problem you've never seen before — without following someone else's steps. Given an engineering question and a geometry, you can independently choose the analysis type, element, mesh strategy, BCs, and validation approach.

### 2. Automate
Move from clicking in a GUI to scripting workflows in Python. Parameterize a model, sweep a design variable, extract results, and plot — all without touching Workbench. This is the single biggest differentiator between "I know ANSYS" and "I can do FEA."

### 3. Communicate
Have a live portfolio that demonstrates engineering judgment, not just colorful contour plots. Someone looking at your work should see: the question you asked, the assumptions you made, how you verified the answer, and what you learned when it didn't match.

### 4. Broaden
Be conversant in more than one solver. Not expert-level — enough to set up, solve, and compare a benchmark problem. This proves the understanding is transferable, not tool-specific.

### 5. Compound on the internship
Whatever problems, tools, or workflows you encounter at work, rebuild a simplified version at home and validate it. Two exposures per concept. The internship provides context; the self-study provides depth.

---

## Principles

- **Compound on the internship.** Study the theory behind whatever you see at work. Two learning streams reinforce each other.
- **Script everything.** Automation is the career differentiator.
- **Finish before starting.** Polish the Fast-FEM portfolio before picking up new tools. Half-finished work looks worse than no work.
- **One new solver.** Don't try LS-DYNA, Abaqus, and OpenFOAM in one summer. Pick the one that aligns with your internship.

---

## Phase 0 — Weeks 1–2: Portfolio Polish (30 hrs)

**Goal:** Fast-FEM portfolio is presentation-ready. GitHub Pages live. LinkedIn-worthy.

### Week 1 (15 hrs)
- [ ] Review all 8 weeks of sim results. Identify the 3–4 strongest case studies.
- [ ] Rewrite those validation reports for a public audience (less "homework," more "engineering narrative").
- [ ] Ensure every case study has: problem motivation, clean contour plots (per visual_guide.md), convergence study, hand calc comparison, and a "what I learned" section.
- [ ] Run any missing mesh convergence studies.

### Week 2 (15 hrs)
- [ ] Build out GitHub Pages case study pages (docs/case-studies.md → individual pages).
- [ ] Add screenshots and convergence plots to each case study.
- [ ] Write a 2-paragraph LinkedIn post introducing the project. Link to the GitHub Pages site.
- [ ] Send the portfolio link to 2–3 people for feedback (professor, peer, mentor).
- [ ] Fix anything they flag.

**Deliverable:** Live portfolio at wrbell.github.io/fast-fem with 3–4 polished case studies.

---

## Phase 1 — Weeks 3–6: Python Scripting & Automation (60 hrs)

**Goal:** Automate ANSYS workflows. Parameterize models. Run batch studies. This is the highest-ROI skill to add.

### Week 3 (15 hrs): PyMAPDL Fundamentals
- [ ] Install PyMAPDL (`pip install ansys-mapdl-core`). Connect to local MAPDL instance.
- [ ] Recreate Week 1 cantilever beam entirely in PyMAPDL (no GUI).
- [ ] Script: geometry → material → mesh → BCs → solve → extract stress → compare to hand calc.
- [ ] Read: PyMAPDL documentation (mapdl.docs.pyansys.com) — getting started + examples.

### Week 4 (15 hrs): Parameterized Studies
- [ ] Parameterize the cantilever: sweep beam length, load magnitude, and mesh density.
- [ ] Generate a mesh convergence plot entirely from script (no manual ANSYS interaction).
- [ ] Parameterize a pressure vessel: sweep r/t ratio, compare hoop stress to analytical.
- [ ] Output results to CSV. Plot with matplotlib. Save figures automatically.

### Week 5 (15 hrs): Batch Automation
- [ ] Script a full DOE (Design of Experiments) on a welded bracket:
  - Variables: weld size, plate thickness, load magnitude
  - Output: max stress, fatigue life, weight
- [ ] Generate a response surface plot (stress vs. weld size vs. thickness).
- [ ] Write results to a structured report (markdown or HTML) automatically.
- [ ] If internship uses Fluent: start PyFluent (`pip install ansys-fluent-core`), recreate pipe flow.

### Week 6 (15 hrs): Portfolio Integration
- [ ] Write a case study: "Automated Parametric Weld Optimization" — show the script, the DOE, the response surface, the optimal design.
- [ ] Add to GitHub Pages as a featured project.
- [ ] Push all scripts to `scripts/` with docstrings and README.
- [ ] Commit notebooks showing parameterized results.

**Deliverable:** 3–4 Python scripts that automate ANSYS workflows. One portfolio-ready parametric study.

---

## Phase 2 — Weeks 7–10: New Solver (60 hrs)

**Goal:** Add a second solver to your toolkit. Pick ONE based on internship domain.

### Option A: LS-DYNA (if internship is automotive, defense, or impact-related)

#### Week 7: Setup & First Model
- [ ] Install LS-DYNA Student + LS-PrePost (free from lsdyna.ansys.com).
- [ ] Run the included example: bar impact (explicit time integration).
- [ ] Understand: keyword input format, time step control, energy balance.
- [ ] Read: Erhart intro to LS-DYNA (free PDF), chapters 1–3.

#### Week 8: Validation
- [ ] Taylor impact test (cylinder on rigid wall) — validate plastic deformation against published results.
- [ ] Drop test of a simple bracket — validate peak force against energy methods.
- [ ] Compare explicit (LS-DYNA) vs implicit (ANSYS Mechanical) on the same quasi-static problem.

#### Week 9: Intermediate
- [ ] Contact modeling in LS-DYNA (different contact types, friction).
- [ ] Material models: Johnson-Cook plasticity, strain-rate effects.
- [ ] Simple crash tube — crush force vs displacement.

#### Week 10: Portfolio
- [ ] Write case study: "Explicit vs Implicit FEA — When to Use Each" with side-by-side comparison.
- [ ] Add to GitHub Pages.

### Option B: Abaqus (if internship is aerospace, oil/gas, or biomechanics)

#### Week 7: Setup & First Model
- [ ] Install Abaqus Student Edition (free from 3DS).
- [ ] Recreate cantilever beam in Abaqus CAE. Compare to ANSYS result.
- [ ] Understand: input file format (.inp), step definitions, output requests.

#### Week 8: Validation
- [ ] Plate with hole — stress concentration, compare to ANSYS and hand calc.
- [ ] Modal analysis — compare natural frequencies to ANSYS and MATLAB.
- [ ] Pressure vessel — compare to ANSYS.

#### Week 9: Intermediate
- [ ] Nonlinear: plasticity in Abaqus (von Mises, isotropic hardening).
- [ ] Contact: Abaqus surface interaction, friction.
- [ ] Python scripting in Abaqus (abaqus cae noGUI=script.py).

#### Week 10: Portfolio
- [ ] Write case study: "Cross-Solver Validation — ANSYS vs Abaqus" with same problem, same mesh, compared results.
- [ ] Add to GitHub Pages.

### Option C: OpenFOAM (if internship is CFD-heavy)

#### Week 7: Setup & First Case
- [ ] Install OpenFOAM on WSL or Linux.
- [ ] Run tutorial: lid-driven cavity (icoFoam).
- [ ] Understand: case structure (0/, constant/, system/), blockMesh, controlDict.

#### Week 8: Validation
- [ ] Laminar pipe flow — compare to Hagen-Poiseuille (same problem as Week 6 Fluent).
- [ ] Flat plate boundary layer — compare to Blasius.
- [ ] Post-process with ParaView.

#### Week 9: Intermediate
- [ ] Turbulent pipe flow with k-ε model.
- [ ] External flow over cylinder — validate drag coefficient.
- [ ] Mesh generation with snappyHexMesh (complex geometry).

#### Week 10: Portfolio
- [ ] Write case study: "Open-Source vs Commercial CFD — Fluent vs OpenFOAM" comparison.
- [ ] Add to GitHub Pages.

**Deliverable:** Working proficiency in a second solver. One cross-solver comparison case study.

---

## Phase 3 — Weeks 11–13: Advanced Topics (45 hrs)

**Goal:** Go deeper on one area that interests you most. Pick ONE track.

### Track A: Nonlinear & Fracture
- [ ] XFEM crack modeling in ANSYS (or Abaqus if Phase 2 was Abaqus)
- [ ] J-integral computation, stress intensity factors
- [ ] Large deformation + plasticity on a real part
- [ ] Write case study with validation against handbook SIF solutions

### Track B: Vibrations & NVH
- [ ] Random vibration (PSD input) in ANSYS
- [ ] Modal superposition vs full transient — compare accuracy and cost
- [ ] Experimental modal analysis correlation (if you have test data from ME440)
- [ ] Write case study on simulation-test correlation

### Track C: CFD Deep Dive
- [ ] Turbulence model comparison (k-ε vs k-ω SST vs realizable k-ε) on same geometry
- [ ] Conjugate heat transfer — solid + fluid in one model
- [ ] Transient CFD — flow startup or vortex shedding
- [ ] Write case study comparing turbulence models

### Track D: HyperMesh Intro
- [ ] Install HyperMesh (Altair student license)
- [ ] Re-mesh a complex part from the 9-week program using HyperMesh
- [ ] Export to ANSYS, solve, compare to original ANSYS mesh
- [ ] Learn 2D automesh + 3D solid map + quality checks
- [ ] Write case study: "Impact of Mesh Quality on FEA Accuracy"

**Deliverable:** One more polished case study in a specialized area.

---

## Phase 4 — Week 14: Wrap-Up (15 hrs)

- [ ] Update portfolio with all summer work.
- [ ] Update `future/roadmap.md` — what's next for Fall 2026?
- [ ] Update skills matrix in roadmap.md with honest self-assessment.
- [ ] Write a "Summer 2026 Retrospective" post-mortem: what worked, what didn't, what to change.
- [ ] Clean up repo: archive any dead ends, update README.
- [ ] LinkedIn post showcasing summer progress.

---

## Weekly Time Budget

| Activity | Hours/Week | Notes |
|----------|-----------|-------|
| Tutorial / reading | 4 | Theory, documentation, examples |
| Hands-on simulation | 7 | Building, solving, debugging |
| Documentation | 3 | Reports, portfolio, commits |
| Review / reflection | 1 | Post-mortem, update roadmap |
| **Total** | **15** | |

---

## Summer Checklist

By August 15, you should have:

- [ ] Live portfolio with 6–8 polished case studies (3–4 from Fast-FEM + 3–4 from summer)
- [ ] Python scripting capability (PyMAPDL or PyFluent)
- [ ] Working proficiency in a second solver
- [ ] One parametric/optimization study showcasing automation
- [ ] One cross-solver validation study
- [ ] One advanced-topic deep dive
- [ ] Updated skills matrix and roadmap for Fall 2026

---

## Internship Synergy

Whatever you encounter at the internship, loop it back:

| At work you see... | At home you study... |
|--------------------|---------------------|
| A specific solver (LS-DYNA, Abaqus, Nastran) | That solver in Phase 2 |
| A meshing tool (HyperMesh, ANSA) | That tool in Phase 3, Track D |
| A material model you don't understand | The theory behind it, validate in ANSYS |
| A simulation you can't explain | Rebuild a simplified version at home, validate against hand calc |
| A workflow that's manual and slow | Automate it with Python (Phase 1 skills) |

The fastest way to learn is to study what you're also doing at work. Two exposures per concept instead of one.
