#!/usr/bin/env python3
"""Check Jupyter notebooks, live-script binaries, and env pins.

The check is read-only. It does not strip notebooks in place.
``--execute`` writes a copy in a temp directory and deletes that copy.

Fails when a notebook has outputs (unless the path is allowlisted),
when a notebook is larger than 1 MiB, when the first cell is not
Markdown, when a ``.mlx`` file is not marked ``binary``, when a
``pyproject.toml`` has no ``uv.lock`` beside it, or when MATLAB files
have no ``matlab-env.txt`` and no README release in that directory
or an ancestor through the scan root.
"""

# jupyter comes from PATH. Bandit flags every subprocess call.
# ruff: noqa: S603

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MAX_BYTES = 1024 * 1024
SKIP_DIRS = frozenset({".agents", "third_party", ".git", ".ipynb_checkpoints", "tests"})
_MATLAB_RELEASE = re.compile(r"R20\d{2}[a-z]")


def main(argv: list[str] | None = None) -> int:
    """Check notebooks and return an exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--allow", type=Path, help="newline list of notebook paths")
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="execute notebooks tagged ci-run into a temp directory",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    problems = check_root(root, args.allow, args.max_bytes, args.execute)
    if problems:
        for problem in problems:
            print(problem)
        print(f"{len(problems)} problem(s)", file=sys.stderr)
        return 1
    print("ok: notebooks")
    return 0


def check_root(
    root: Path,
    allow_file: Path | None = None,
    max_bytes: int = MAX_BYTES,
    execute: bool = False,
) -> list[str]:
    """Return notebook, live-script, and env-pin problems under root."""
    allow = _load_allow(allow_file)
    problems: list[str] = []
    notebooks = _files(root, ".ipynb")
    for path in notebooks:
        problems.extend(_notebook_problems(root, path, allow, max_bytes))
        if execute and _tagged_ci_run(path):
            message = _execute(path)
            if message:
                rel = path.relative_to(root).as_posix()
                problems.append(f"{rel}: ci-run failed: {message}")
    for path in _files(root, ".mlx"):
        rel = path.relative_to(root).as_posix()
        if _attribute(root, rel, "binary") != "set":
            problems.append(f"{rel}: .mlx is not marked binary in .gitattributes")
    problems.extend(_matlab_problems(root))
    for project in _files_named(root, "pyproject.toml"):
        if not (project.parent / "uv.lock").is_file():
            rel = project.relative_to(root).as_posix()
            problems.append(f"{rel}: missing uv.lock beside pyproject.toml")
    return problems


def _notebook_problems(
    root: Path, path: Path, allow: set[str], max_bytes: int
) -> list[str]:
    rel = path.relative_to(root).as_posix()
    problems: list[str] = []
    size = path.stat().st_size
    if size > max_bytes:
        problems.append(f"{rel}: notebook is {size} bytes (limit {max_bytes})")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return problems + [f"{rel}: {exc}"]
    if rel not in allow and _has_outputs(data):
        problems.append(f"{rel}: notebook has outputs")
    if not _first_markdown(data):
        problems.append(f"{rel}: first cell must be Markdown")
    return problems


def _has_outputs(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    for cell in data.get("cells", []):
        if not isinstance(cell, dict):
            continue
        outputs = cell.get("outputs") or []
        if outputs:
            return True
        if cell.get("execution_count") is not None:
            return True
    return False


def _first_markdown(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    cells = data.get("cells") or []
    if not cells or not isinstance(cells[0], dict):
        return False
    if cells[0].get("cell_type") != "markdown":
        return False
    source = cells[0].get("source", "")
    if isinstance(source, list):
        source = "".join(source)
    return bool(str(source).strip())


def _tagged_ci_run(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    if not isinstance(data, dict):
        return False
    tags = (data.get("metadata") or {}).get("tags") or []
    if "ci-run" in tags:
        return True
    for cell in data.get("cells", []):
        if not isinstance(cell, dict):
            continue
        cell_tags = (cell.get("metadata") or {}).get("tags") or []
        if "ci-run" in cell_tags:
            return True
    return False


def _execute(path: Path) -> str | None:
    jupyter = shutil.which("jupyter")
    if jupyter is None:
        return "jupyter is not installed"
    with tempfile.TemporaryDirectory(prefix="nb-exec-") as tmp:
        result = subprocess.run(
            [
                jupyter,
                "nbconvert",
                "--execute",
                "--to",
                "notebook",
                "--output",
                "executed",
                "--output-dir",
                tmp,
                str(path),
            ],
            check=False,
            text=True,
            capture_output=True,
        )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        return detail or "nbconvert failed"
    return None


def _matlab_problems(root: Path) -> list[str]:
    """Return directories whose MATLAB files do not record a release."""
    parents = {path.parent for path in _files(root, ".m") + _files(root, ".mlx")}
    problems: list[str] = []
    for directory in sorted(parents):
        if _matlab_recorded(root, directory):
            continue
        rel = directory.relative_to(root).as_posix()
        label = str(root) if rel == "." else rel
        problems.append(
            f"{label}: MATLAB files need matlab-env.txt or a README release"
        )
    return problems


def _matlab_recorded(root: Path, directory: Path) -> bool:
    """Return whether directory or an ancestor through root records MATLAB."""
    current = directory
    while True:
        if (current / "matlab-env.txt").is_file():
            return True
        readme = current / "README.md"
        if readme.is_file() and _readme_has_release(readme):
            return True
        if current == root:
            return False
        parent = current.parent
        if parent == current:
            return False
        current = parent


def _readme_has_release(path: Path) -> bool:
    """Return whether a README names a MATLAB release such as R2025a."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    return _MATLAB_RELEASE.search(text) is not None


def _load_allow(allow_file: Path | None) -> set[str]:
    if allow_file is None or not allow_file.is_file():
        return set()
    allowed: set[str] = set()
    for raw in allow_file.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            allowed.add(line)
    return allowed


def _files(root: Path, suffix: str) -> list[Path]:
    found: list[Path] = []
    if not root.is_dir():
        return found
    for dirpath, _dirnames, filenames in _walk(root):
        for name in filenames:
            if name.endswith(suffix):
                found.append(dirpath / name)
    return found


def _files_named(root: Path, name: str) -> list[Path]:
    found: list[Path] = []
    if not root.is_dir():
        return found
    for dirpath, _dirnames, filenames in _walk(root):
        if name in filenames:
            found.append(dirpath / name)
    return found


def _walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [item for item in dirnames if item not in SKIP_DIRS]
        yield Path(dirpath), dirnames, filenames


def _attribute(root: Path, rel: str, attr: str) -> str | None:
    # Local import keeps this tool usable without the case checker installed
    # as a package. Both modules live in tools/.
    from check_cases import _attribute as case_attribute

    return case_attribute(root, rel, attr)


if __name__ == "__main__":
    sys.exit(main())
