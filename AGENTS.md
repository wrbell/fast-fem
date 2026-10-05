# AGENTS.md

## Project

Fast-FEM is a self-directed learning project in Finite Element Method theory
and ANSYS simulation. It supports University of Michigan mechanical engineering
courses (ME3601 Machine Elements, ME440 Vibrations, ME379 Thermal-Fluid,
ME4301 / ME525 CFD). The goals are course project delivery and
portfolio-quality documentation. The main language is Python (Jupyter
notebooks and one script). Willem reviews every merge.

Current status is in the README (`README.md`, "Status" line). This file does
not state status.

- Folder map: [docs/agents/structure.md](docs/agents/structure.md)
- Plan and schedule: `plan/schedule.md`; hardware and ANSYS settings:
  `plan/config.md`; resources: `plan/references.md`
- Main textbooks: Hughes (FEM theory), Shigley (machine design, welds,
  fatigue), Inman (vibrations), Cengel (heat transfer), Hertzberg
  (_Deformation and Fracture Mechanics of Engineering Materials_, Wiley, 6th
  ed.), Zikanov (_Essential Computational Fluid Dynamics_, Wiley, 2nd ed.)
- Primary simulation tool: ANSYS Student Edition

## Commands

- Setup: `pip install -r requirements.txt`
- Open a notebook: `jupyter notebook notebooks/static_stress.ipynb`
- Convergence plot (full example in `README.md`, "Quick Start"):
  `python scripts/mesh_convergence.py scripts/example_convergence.csv -o convergence.png`
- Lint: `ruff check --config enforcement/ruff/ruff.toml .`
- Format check: `ruff format --check --config enforcement/ruff/ruff.toml .`
- Pre-commit on files you changed: `pre-commit run --files <files>`
  (never pass a `.ipynb` file; the nbstripout hook rewrites it on disk)

The repository has no automated test suite. `requirements.txt` lists the
dependencies.

## Code style

Follow the config files. Do not paste a style guide into this file.

- Python: `enforcement/ruff/ruff.toml`
- Editor defaults: `.editorconfig`
- Markdown: `enforcement/markdownlint/.markdownlint-cli2.yaml`
- YAML: `enforcement/yamllint/.yamllint.yml`
- Notebooks: `enforcement/notebooks-reproducibility/README.md`

Notebooks are committed without outputs. Use only the pre-commit `nbstripout`
hook. Do not install the nbstripout clean filter (`nbstripout --install
--attributes`): it can drop notebook outputs on disk.

Collection standards live in `/Users/willem/Code/standards/STANDARDS.md`.
When a standards file and this file disagree, this file wins.
Say that in the pull request body.

## Tests

Validate every ANSYS result against an analytical hand calculation before you
trust it.

- Method: `reference/methodology.md` (workflow, error thresholds, mesh
  convergence). Formula sheet: `reference/validation.md`.
- Use the notebooks in `notebooks/` to compute the hand calculation and the
  error for each weekly milestone.
- Document every simulation with `templates/validation_report.md` and log it
  in `results/sim_log.md`.
- Use `templates/post_mortem.md` for lessons from a failed simulation.
- Pre-solve checklists for each analysis type: `reference/preflight.md`.

Hardware limits that affect a simulation (details in `plan/config.md`):

- 6-core Xeon W3-2425: use 4 cores for the ANSYS solver (SMP mode; 4 cores
  without an HPC license).
- 64 GB DDR5 is well above the Student Edition element limits.
- RTX 2000 Ada is for display only; the GPU solver is disabled.
- Student Edition caps: about 128K nodes plus elements combined (Mechanical)
  and about 512K cells plus nodes combined (Fluent).

## Pull requests and commits

Use a Conventional Commit subject.
Open the pull request as a draft.
Wait for CI to pass.
List each assumption and each open tradeoff in the pull request body.
Keep each change near 100 lines.
Do not edit files outside the task.
A new dependency needs a reason in the pull request.
Do not force-push, rewrite history, delete a branch, merge, or publish
unless Willem asks.

## Security

Do not commit a secret.
Do not put a secret in a prompt or a log.
Do not use a production credential.
Do not commit course material or other copyrighted files (the `.gitignore`
ignores `*.pdf`).
GitHub Pages publishes `docs/`; put nothing private there.

## Clarity

Write explanations to Willem in Simplified Technical English. Use the same style
for a pull request description, a commit message body, and prose in a README or
another doc. Aim for about 80 percent of the rules. Full compliance with
ASD-STE100 is not the goal.

The rules are in the standards repository at `standards/writing-ste/ste.md`.
The upstream skill is
[simplified-technical-english](https://github.com/0xpili/simplified-technical-english/tree/1e148d670cba46685ad2b4c3f2354a637a7fdbbe)
(MIT, commit `1e148d670cba46685ad2b4c3f2354a637a7fdbbe`). Link to that skill.
Do not copy the skill into this repository again.

Code, identifiers, math, command-line output, and quoted error text are exempt.

When structure, flow, or architecture is the point, use a mermaid diagram.
For a complex result, offer a self-contained HTML page.
That page is a throwaway file.
Do not commit it unless Willem asks.

Make a video only when Willem asks for a video.
Do not add an API key or a secret.

`scripts/ste_check.py` in the upstream skill is an optional check on docs.
Do not use it as a CI gate.

<!-- standards:begin -->
## Collection standards

Every project under `/Users/willem/Code` follows the shared standards in
`/Users/willem/Code/standards/` (index: `standards/STANDARDS.md`; future
standards: `standards/ROADMAP.md`).

- **Presentations:** build every deck from
  `standards/powerpoint template/Willem-Default.potx` (theme "Helena": Neue Haas
  Grotesk Text Pro, 16:9, black on white with a gray ramp, template v2). Spec:
  `standards/powerpoint template/STANDARD.md`. Generate with
  `standards/powerpoint template/house_style.py` (open
  `Willem-Default-Base.pptx`, never the `.potx`) and gate with
  `standards/powerpoint template/deck_checks.py` before calling a deck done.
- **Deck rules:** no speaker notes in submitted decks; editable shapes, not
  chart images; numbered, linked superscript citations with a final References
  slide; no bottom rules, citation strips, or page counters; footer text only
  when a course or client requires it (for example `ME460 HWx`), which overrides
  the default of no footer; export the deliverable PDF with native PowerPoint
  and use LibreOffice renders only for QA.
- **Everything else:** do not invent facts, dates, or numbers; mark unknowns TBD
  and point at the source. Keep copyrighted course material out of git. This
  block is managed by `standards/tools/apply_standards.py`; edit
  `standards/ai-files/BLOCK-root.md`, not this copy.
- **AI use (school work):** no AI-generated or AI-modified images in any school
  deliverable; AI-written deliverable text only with written adviser
  pre-clearance (`docs/ai-clearances/`); never cite an AI tool as a source;
  never edit graded report text (the repo's `protected-paths.txt`; example:
  `standards/enforcement/senior-design-repo/sd-protected-paths.txt`). AI-use
  logging and attestation are opt-in per repo via `ai-attestation-roots.txt`;
  see `standards/standards/ai-use-disclosure/ai-use-disclosure.md`.
- **AI files:** one `AGENTS.md` (≤ 200 lines, Clarity verbatim); `CLAUDE.md` is
  `@AGENTS.md`. Gates: `standards/tools/agents_md_lint.py`, `ai_file_lint.py`.
<!-- standards:end -->
