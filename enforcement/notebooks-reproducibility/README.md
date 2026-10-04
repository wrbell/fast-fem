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
