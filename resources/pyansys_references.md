# PyAnsys & PyDYNA References

Organized link collection for Python-based FEA automation. Verified URLs sourced from web research.

**Related files:**
- [pyansys_research.md](pyansys_research.md) — detailed API guide
- [pyansys_applications.md](pyansys_applications.md) — practical project patterns

---

## Official PyAnsys Documentation

| Package | Docs | GitHub | PyPI |
|---------|------|--------|------|
| PyAnsys Portal | [docs.pyansys.com](https://docs.pyansys.com/) | — | — |
| PyAnsys Developer Guide | [dev.docs.pyansys.com](https://dev.docs.pyansys.com/) | — | — |
| PyMAPDL | [mapdl.docs.pyansys.com](https://mapdl.docs.pyansys.com/) | [ansys/pymapdl](https://github.com/ansys/pymapdl) | [ansys-mapdl-core](https://pypi.org/project/ansys-mapdl-core/) |
| PyDPF-Core | [dpf.docs.pyansys.com](https://dpf.docs.pyansys.com/) | [ansys/pydpf-core](https://github.com/ansys/pydpf-core) | [ansys-dpf-core](https://pypi.org/project/ansys-dpf-core/) |
| PyDPF-Post | [post.docs.pyansys.com](https://post.docs.pyansys.com/) | [ansys/pydpf-post](https://github.com/ansys/pydpf-post) | [ansys-dpf-post](https://pypi.org/project/ansys-dpf-post/) |
| PyDYNA | [dyna.docs.pyansys.com](https://dyna.docs.pyansys.com/) | [ansys/pydyna](https://github.com/ansys/pydyna) | [ansys-dyna-core](https://pypi.org/project/ansys-dyna-core/) |
| PyMechanical | [mechanical.docs.pyansys.com](https://mechanical.docs.pyansys.com/) | [ansys/pymechanical](https://github.com/ansys/pymechanical) | [ansys-mechanical-core](https://pypi.org/project/ansys-mechanical-core/) |
| PyOptiSLang | [optislang.docs.pyansys.com](https://optislang.docs.pyansys.com/) | [ansys/pyoptislang](https://github.com/ansys/pyoptislang) | [ansys-optislang-core](https://pypi.org/project/ansys-optislang-core/) |

---

## Cheat Sheets

- [PyMAPDL Cheat Sheet](https://developer.ansys.com/blog/pymapdl-cheat-sheet)
- [PyDPF-Core Cheat Sheet](https://developer.ansys.com/blog/pydpf-core-cheat-sheet)

---

## Tutorials & Getting Started

### PyMAPDL
- [Getting Started with PyMAPDL (Innovation Space)](https://innovationspace.ansys.com/product/getting-started-with-ansys-pymapdl/) — free course
- [PyMAPDL Examples Gallery](https://mapdl.docs.pyansys.com/version/stable/examples/index.html) — official worked examples
- [PyMAPDL Tutorials](https://tutorials.mapdl.docs.pyansys.com/tutorials/01-pymapdl.html) — step-by-step tutorials
- [2D Pressure Vessel (mesh convergence)](https://mapdl.docs.pyansys.com/version/stable/examples/gallery_examples/00-mapdl-examples/2d_pressure_vessel.html) — key example for iterative studies
- [Exhaust Manifold Thermal-Structural](https://mapdl.docs.pyansys.com/version/stable/examples/gallery_examples/00-mapdl-examples/exhaust_manifold_thermal_stress.html) — coupled analysis example
- [Transient Thermal](https://mapdl.docs.pyansys.com/version/stable/examples/gallery_examples/00-mapdl-examples/transient_thermal.html)
- [ML/AI Datasets using PyMAPDL (Innovation Space)](https://innovationspace.ansys.com/product/ml-ai-datasets-using-pymapdl/) — ML integration course
- [Creating Simulation Web Apps with PyMAPDL](https://innovationspace.ansys.com/product/developing-webapps-with-pymapdl/)

### PyDPF
- [PyDPF-Core Examples](https://dpf.docs.pyansys.com/version/stable/examples/index.html)
- [LS-DYNA Operators in DPF](https://dpf.docs.pyansys.com/version/stable/examples/14-lsdyna/00-lsdyna_operators.html) — reading d3plot/binout with DPF

### PyDYNA
- [PyDYNA Getting Started Example](https://dyna.docs.pyansys.com/version/stable/getting-started/example.html)
- [PyDYNA Examples Collection](https://dyna.docs.pyansys.com/version/stable/examples/index.html)

### PyOptiSLang
- [PyOptiSLang Examples](https://optislang.docs.pyansys.com/version/stable/examples/index.html)
- [RDO with Python Solver](https://optislang.docs.pyansys.com/version/stable/examples/workflow_creation/04_1_rdo_python.html)

### PyMechanical
- [PyMechanical Architecture](https://mechanical.docs.pyansys.com/version/stable/architecture.html)
- [PyMechanical FAQ](https://mechanical.docs.pyansys.com/version/stable/faq.html)

### General Python for Ansys
- [Intro to Python (Innovation Space)](https://innovationspace.ansys.com/product/intro-to-python/) — 10 lessons, no prior experience needed
- [Python Courses Hub (Innovation Space)](https://innovationspace.ansys.com/courses/python/)
- [Scripting in Ansys Discovery](https://innovationspace.ansys.com/product/scripting-in-ansys-discovery-modeling/)
- [Advanced Scripting in Ansys Discovery](https://innovationspace.ansys.com/product/advanced-scripting-in-ansys-discovery/)

---

## Ansys Blog Posts

- [Access the Power of Ansys from the Python World](https://www.ansys.com/blog/accessing-ansys-from-python) — PyAnsys intro
- [Ansys Gets Into Open Source With GitHub](https://www.ansys.com/blog/ansys-gets-into-open-source-with-github)
- [Introducing PyAnsys (Developer Portal)](https://developer.ansys.com/blog/introducing-pyansys)
- [Customize & Automate RDO with PyOptiSLang](https://www.ansys.com/blog/customize-automate-rdo-with-ansys-pyoptislang)

---

## LS-DYNA Python Tools (Third-Party)

| Tool | GitHub | PyPI | Status | Description |
|------|--------|------|--------|-------------|
| lasso-python | [open-lasso-python/lasso-python](https://github.com/open-lasso-python/lasso-python) | [lasso-python](https://pypi.org/project/lasso-python/) | **Active** | Fast d3plot/binout read/write (recommended) |
| qd-cae-python | [qd-cae/qd-cae-python](https://github.com/qd-cae/qd-cae-python) | [qd](https://pypi.org/project/qd/) | Archived | d3plot/binout/keyword reading (migrate to lasso) |
| lsreader | — | [lsreader](https://pypi.org/project/lsreader/) | Inactive | d3plot/binout reading (2000+ data types) |
| Codie-D3plot | [svenholcombe/Codie-D3plot](https://github.com/svenholcombe/Codie-D3plot) | — | Legacy | C++/Python d3plot reader |

### lasso-python Documentation
- [D3plot module docs](https://open-lasso-python.github.io/lasso-python/dyna/)
- [Binout module docs](https://open-lasso-python.github.io/lasso-python/dyna/Binout/)

---

## LS-DYNA Resources

### Official
- [LS-DYNA Product Space (Ansys)](https://lsdyna.ansys.com/) — manuals, downloads, knowledge base
- [LS-DYNA Papers (Ansys)](https://lsdyna.ansys.com/papers/)
- [LS-DYNA Keyword Reference](https://lsdyna.ansys.com/keyword/)
- [LS-DYNA Supported Keywords List (PDF)](https://storage.ansys.com/doclinks/LandingPages/Files/WB-LS-DYNA/LS-DYNA_Keywords.pdf)
- [LS-DYNA Keyword Manual Vol I (PDF)](https://ftp.lstc.com/anonymous/outgoing/jday/manuals/LS-DYNA_manual_Vol_I_R6.1.0.pdf)
- [LS-DYNA Keyword Manual Vol II — Materials (PDF)](https://ftp.lstc.com/anonymous/outgoing/jday/manuals/LS-DYNA_manual_Vol_II_R7.1.pdf)
- [d3plot Database Manual (PDF)](https://ftp.lstc.com/anonymous/outgoing/lsprepost/d3plot_database_manual/ls-dyna_database_Sep2017.pdf)

### Getting Started
- [Getting Started with LS-DYNA (dynasupport.com)](https://www.dynasupport.com/tutorial/getting-started-with-ls-dyna/getting-started)
- [Engineering to True Stress/Strain (dynasupport.com)](https://www.dynasupport.com/howtos/material/from-engineering-to-true-strain-true-stress)

### Examples
- [DYNAexamples.com](https://www.dynaexamples.com/) — ~500 free LS-DYNA examples with input files
- [DYNAexamples Introduction](https://www.dynaexamples.com/introduction)

### Conference Papers
- [DYNAlook.com](https://www.dynalook.com/) — 2,300+ papers from LS-DYNA conferences (searchable)
- [15th International LS-DYNA Conference](https://www.dynalook.com/conferences/15th-international-ls-dyna-conference)
- [14th International LS-DYNA Conference](https://www.dynalook.com/conferences/14th-international-ls-dyna-conference)
- [14th European LS-DYNA Conference 2023](https://www.dynalook.com/conferences/14th-european-ls-dyna-conference-2023)
- [qd — Build Your Own LS-DYNA Tools in Python (DYNAlook paper)](https://www.dynalook.com/conferences/15th-international-ls-dyna-conference/computing-technology/qd-2013-build-your-own-ls-dyna-r-tools-quickly-in-python)

### DYNAmore
- [DYNAmore Main Site](https://www.dynamore.de/en)
- [DYNAmore Training Portal](https://www.dynamore.de/en/training)
- [DYNAmore Introductory Seminars](https://www.dynamore.de/en/training/seminars/introduction)
- [Introduction to LS-DYNA Course](https://www.dynamore.de/en/training/seminars/introduction/introduction-to-ls-dyna)
- [DYNAmore Papers & Downloads](https://www.dynamore.de/en/downloads/papers)
- [DYNAmore Tools (ECO SYSTEM)](https://www.dynamore.de/en/products/pre-and-postprocessors/tools) — CLI tools for d3plot compression, sub-models, etc.

---

## Optimization & DOE Libraries

| Library | Link | Description |
|---------|------|-------------|
| SciPy optimize | [docs.scipy.org/doc/scipy/reference/optimize.html](https://docs.scipy.org/doc/scipy/reference/optimize.html) | Minimize, differential_evolution, COBYLA |
| pyDOE2 | [github.com/clicumu/pyDOE2](https://github.com/clicumu/pyDOE2) | Latin Hypercube, factorial, Box-Behnken |
| SMT | [github.com/SMTorg/smt](https://github.com/SMTorg/smt) | Surrogate Modeling Toolbox (Kriging, RBF) |
| scikit-learn GP | [scikit-learn.org](https://scikit-learn.org/stable/modules/gaussian_process.html) | Gaussian Process regression |

---

## GitHub Repositories

### FEA Automation & Parametric Studies
- [Atharva224/fea-surrogate-modeling](https://github.com/Atharva224/fea-surrogate-modeling) — PyMAPDL parameter sweeps + ML surrogates
- [pep-pig/Topology-optimization-via-simp-method](https://github.com/pep-pig/Topology-optimization-of-structure-via-simp-method) — SIMP + ANSYS MAPDL
- [AHartmaier/pyLabFEA](https://github.com/AHartmaier/pyLabFEA) — pure-Python FEA with ML constitutive models
- [tirthajyoti/Design-of-experiment-Python](https://github.com/tirthajyoti/Design-of-experiment-Python) — DOE generator

### Material Calibration
- [LucMarechal/Soft-Robotics-Materials-Database](https://github.com/LucMarechal/Soft-Robotics-Materials-Database) — hyperelastic fitting (Mooney-Rivlin, Ogden)
- [PyMAPDL: Calibrating Hyperelastic Models](https://examples.mapdl.docs.pyansys.com/technology_showcase_examples/techdemo-15/ex_15-teccalvalhyper.html)

### Surrogate Modeling
- [XinWEI2000/Data-driven-surrogate-model](https://github.com/XinWEI2000/Data-driven-surrogate-model) — FEM surrogate with MLP + GPR
- [SMTorg/smt](https://github.com/SMTorg/smt) — Surrogate Modeling Toolbox (Kriging, RBF, KPLS)
- [SMT Documentation](https://smt.readthedocs.io/)

### Topology Optimization
- [zfergus/topopt](https://github.com/zfergus/topopt) — Python topology optimization with MMA
- [dl4to/dl4to](https://github.com/dl4to/dl4to) — deep learning topology optimization (PyTorch)
- [TopOpt Docs](https://topopt.readthedocs.io/en/documentation/TopOpt.html)

### LS-DYNA Specific
- [jfriedlein/Numerical_examples_in_LS-Dyna](https://github.com/jfriedlein/Numerical_examples_in_LS-Dyna) — examples with geometry, mesh, keyword files
- [jfriedlein/usrmat_LS-Dyna_Fortran](https://github.com/jfriedlein/usrmat_LS-Dyna_Fortran) — user-defined material implementation
- [jrycw/ithome2022-cae-ansa-lsdyna](https://github.com/jrycw/ithome2022-cae-ansa-lsdyna) — CAE + ANSA + LS-DYNA tutorials
- [Renumics/mesh2vec](https://github.com/Renumics/mesh2vec) — turn CAE mesh data into ML feature vectors
- [qd-cae/awesome-CAE](https://github.com/qd-cae/awesome-CAE) — curated list of CAE frameworks and libraries

### Fatigue
- [jtipton2/abaqusHCF](https://github.com/jtipton2/abaqusHCF) — Python HCF fatigue analysis (Abaqus, patterns transferable)

### Workbench Scripting
- [sikvelsigma/ANSYS-WB-Batch-Script](https://github.com/sikvelsigma/ANSYS-WB-Batch-Script) — batch scripting examples
- [AshKot1/ANSYS-Scripts-Ironpython](https://github.com/AshKot1/ANSYS-Scripts-Ironpython) — IronPython script collection

---

## ACT (ANSYS Customization Toolkit)

- [ACT Developer Portal](https://developer.ansys.com/docs/act)
- [ACT Developer's Guide (2025 R1, PDF)](https://ansyshelp.ansys.com/public/Views/Secured/corp/v251/en/pdf/Ansys_ACT_Developers_Guide.pdf)
- [Getting Started with ACT (PDF)](https://storage.ansys.com/api-a/v232/GettingStartedWithACT.pdf)
- [ACT Overview (Rand Simulation)](https://resources.randsim.com/brochures/ansys-customization-toolkit-act-overview-and-examples)

---

## Other Useful Tools

- [MaterialMAP](https://materialmap.net/) — generate MAT_024 curves from basic tensile properties
- [Oasys LS-DYNA Python scripting](https://dyna.oasys-software.com/training/using-python-to-interact-with-the-oasys-lsdyna-environment/)
- [CFD_Mapper](https://github.com/galuszkm/CFD_Mapper) — convert CFD pressure to FEM boundary conditions
- [vim-lsdyna](https://github.com/gradzikb/vim-lsdyna) — VIM syntax highlighting for keyword files

---

## NAFEMS & Industry

- [NAFEMS: Python for FEA Automation and Optimization](https://www.nafems.org/training/e-learning/python-for-fea-automation-and-optimization/) — e-learning course
- [Ansys Developer Portal](https://developer.ansys.com/docs/pyansys)

---

## Video & Blog

- [Make Your Own FEA System with Parametric Sweeps (Medium)](https://medium.com/innovating-resourcefully/make-your-own-fea-analysis-system-in-python-including-parametric-sweeps-44e03c98f16)
- [Python for Handling Data in CAE (Gemello)](https://gemello.se/Blog2/post_21.html)
