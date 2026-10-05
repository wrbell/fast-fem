#!/usr/bin/env python3
"""Check Jupyter notebooks, live-script binaries, and env pins.

The check is read-only. It does not strip notebooks in place.
``--execute`` writes a copy in a temp directory and deletes that copy.

Fails when a notebook has outputs, when a notebook is larger than 1 MiB,
when the first cell is not Markdown, when a ``.mlx`` file is not marked
``binary``, or when MATLAB files have no ``matlab-env.txt`` and no README
release in that directory or an ancestor through the scan root.

A notebook listed in the allow file may keep outputs and may be larger
than the limit; its size prints as an ``INFO:`` line. The allow file is
``--allow``, or the repo-owned ``<root>/keep-output.txt`` when it exists
(one path per line, relative to the root; ``#`` starts a comment). Record
each kept-output or over-size notebook in the repository README.

A ``pyproject.toml`` with no ``uv.lock`` beside it prints an
``ADVISORY:`` line: uv is optional, and pins in ``requirements.txt`` or
``pyproject.toml`` are accepted. ``--require-uv`` makes it a failure.

Files come from git's file list (``tools/_repo_files.py``): tracked files
and untracked files that ``.gitignore`` does not exclude. Folders named
``.agents``, ``third_party``, ``.ipynb_checkpoints``,
``.virtual_documents`` or ``tests`` are skipped as well.
"""

# jupyter comes from PATH. Bandit flags every subprocess call.
# ruff: noqa: S603

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _repo_files import tracked_files

MAX_BYTES = 1024 * 1024
ALLOW_NAME = "keep-output.txt"
SKIP_DIRS = frozenset(
    {
        ".agents",
        "third_party",
        ".git",
        ".ipynb_checkpoints",
        ".virtual_documents",
        "tests",
    }
)
_MATLAB_RELEASE = re.compile(r"R20\d{2}[a-z]")


def main(argv: list[str] | None = None) -> int:
    """Check notebooks and return an exit code."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--allow",
        type=Path,
        help=f"newline list of notebook paths (default: <root>/{ALLOW_NAME})",
    )
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="execute notebooks tagged ci-run into a temp directory",
    )
    parser.add_argument(
        "--require-uv",
        action="store_true",
        help="fail when a pyproject.toml has no uv.lock beside it",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    problems, notes = scan_root(
        root, args.allow, args.max_bytes, args.execute, require_uv=args.require_uv
    )
    for note in notes:
        print(note)
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
    *,
    require_uv: bool = False,
) -> list[str]:
    """Return notebook, live-script, and env-pin problems under root."""
    return scan_root(root, allow_file, max_bytes, execute, require_uv=require_uv)[0]


def scan_root(
    root: Path,
    allow_file: Path | None = None,
    max_bytes: int = MAX_BYTES,
    execute: bool = False,
    *,
    require_uv: bool = False,
) -> tuple[list[str], list[str]]:
    """Return ``(problems, notes)`` for the notebooks and pins under root.

    Parameters
    ----------
    root : pathlib.Path
        Scan root, normally the repository root.
    allow_file : pathlib.Path, optional
        Kept-output list. ``None`` reads ``root / keep-output.txt`` when it
        exists.
    max_bytes : int, optional
        Notebook size limit for notebooks that are not allow-listed.
    execute : bool, optional
        Execute notebooks tagged ``ci-run`` into a temp directory.
    require_uv : bool, optional
        Report a missing ``uv.lock`` as a problem, not an advisory note.

    Returns
    -------
    tuple of list of str
        Problems (exit 1) and ``INFO:``/``ADVISORY:`` notes (exit 0).
    """
    if allow_file is None and (root / ALLOW_NAME).is_file():
        allow_file = root / ALLOW_NAME
    allow = _load_allow(allow_file)
    problems: list[str] = []
    notes: list[str] = []
    notebooks = _files(root, ".ipynb")
    for path in notebooks:
        rel = path.relative_to(root).as_posix()
        size = path.stat().st_size
        if size > max_bytes and rel in allow:
            notes.append(
                f"INFO: {rel}: notebook is {size} bytes (limit {max_bytes}); "
                f"allow-listed in {allow_file}"
            )
        problems.extend(_notebook_problems(root, path, allow, max_bytes))
        if execute and _tagged_ci_run(path):
            message = _execute(path)
            if message:
                problems.append(f"{rel}: ci-run failed: {message}")
    for path in _files(root, ".mlx"):
        rel = path.relative_to(root).as_posix()
        if _attribute(root, rel, "binary") != "set":
            problems.append(f"{rel}: .mlx is not marked binary in .gitattributes")
    problems.extend(_matlab_problems(root))
    for project in _files_named(root, "pyproject.toml"):
        if not (project.parent / "uv.lock").is_file():
            rel = project.relative_to(root).as_posix()
            message = f"{rel}: missing uv.lock beside pyproject.toml"
            if require_uv:
                problems.append(message)
            else:
                notes.append(
                    f"ADVISORY: {message} (uv is optional; pin in uv.lock, "
                    "requirements.txt, or pyproject.toml)"
                )
    return problems, notes


def _notebook_problems(
    root: Path, path: Path, allow: set[str], max_bytes: int
) -> list[str]:
    rel = path.relative_to(root).as_posix()
    problems: list[str] = []
    size = path.stat().st_size
    if size > max_bytes and rel not in allow:
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


def _listed(root: Path) -> list[Path]:
    """Return git's file list under root, minus the skipped folders."""
    if not root.is_dir():
        return []
    return [
        path
        for path in tracked_files(root)
        if not SKIP_DIRS.intersection(path.relative_to(root).parts[:-1])
    ]


def _files(root: Path, suffix: str) -> list[Path]:
    return [path for path in _listed(root) if path.name.endswith(suffix)]


def _files_named(root: Path, name: str) -> list[Path]:
    return [path for path in _listed(root) if path.name == name]


def _attribute(root: Path, rel: str, attr: str) -> str | None:
    # Local import keeps this tool usable without the case checker installed
    # as a package. Both modules live in tools/.
    from check_cases import _attribute as case_attribute

    return case_attribute(root, rel, attr)


if __name__ == "__main__":
    sys.exit(main())
