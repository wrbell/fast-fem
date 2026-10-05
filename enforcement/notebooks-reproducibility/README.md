# Notebooks and reproducibility

`tools/check_notebooks.py` checks notebooks and env pins.
The pre-commit fragment is
`enforcement/pre-commit/fragments/notebooks-reproducibility.yaml`.
`nbstripout` is pinned at `0.9.1`.
Ruff is pinned at `v0.16.10`.
Jupytext is pinned at `v1.19.5`.

Copy `CITATION.cff` to the root of a public research repo.
Copy `data-README.md` to `data/README.md`.
Copy `gitattributes-notebooks` into `.gitattributes`.
It does not enable the `nbstripout` clean filter. The pre-commit hook
strips outputs; see `STANDARDS.md` §7.

List notebooks that keep outputs in the repo-owned root `keep-output.txt`,
not in the managed copy here.
