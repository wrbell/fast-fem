#!/usr/bin/env python3
"""Check simulation case folders.

The check is read-only. It does not launch a solver.
It does not move files to Git LFS and it does not rewrite history.

Case roots come from ``sim-cases.txt`` at the repository root, one path per
line, relative to the root, with ``#`` comments. ``--cases-dir`` overrides the
file. Without either, every folder named ``cases`` is a case root.
Case discovery is a walk of the file system. It does not read ``.gitignore``,
so ignored case folders inside a declared root are still checked.

A case folder is a direct child of a case root, or
``_attempts/<run_id>/<case_id>/`` inside a root. The run id is
``YYYYMMDDTHHMMSS-<hex>``. Other folders whose name starts with ``_`` or ``.``
are skipped. The folder name is ``YYYY-MM-DD_<study>_<variant>`` or a generated
snake_case id such as ``vg_16deg_40hz_corr``.
``case.yaml`` must carry the keys the run check needs. A ``planned`` case
needs only the keys a generator knows before the run.
Tracked solver binaries fail the check.
A tracked file larger than 50 MiB fails unless Git LFS tracks it.
A figure in ``post/`` needs a script in ``post/`` and a CSV with the same stem.
Identical ``*.mat`` blobs in two paths fail the check.
"""

# Git is a fixed executable. Bandit flags every subprocess call.
# ruff: noqa: S603, S607

from __future__ import annotations

import argparse
import hashlib
import math
import os
import re
import subprocess
import sys
from pathlib import Path

from plain_yaml import YamlError, parse_yaml

MAX_BYTES = 50 * 1024 * 1024
CASE_ROOTS_FILE = "sim-cases.txt"
DEFAULT_ROOT_NAME = "cases"
ATTEMPTS_DIR = "_attempts"
CASE_NAME = re.compile(r"^(?:\d{4}-\d{2}-\d{2}_[^/]+|[a-z][a-z0-9]*(?:_[a-z0-9]+)+)$")
RUN_ID = re.compile(r"^\d{8}T\d{6}-[0-9a-f]+$")
SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
TIME_PART = re.compile(r"^[0-9]+(?:\.[0-9]+)?$")
SKIP_DIRS = frozenset({".agents", "third_party", ".git", ".ipynb_checkpoints", "tests"})
FIGURE_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg", ".pdf", ".tif", ".tiff"}
SCRIPT_SUFFIXES = {".py", ".m"}
BINARY_SUFFIXES = (
    ".cas.h5",
    ".dat.h5",
    ".d3plot",
    ".cas",
    ".dat",
    ".vtk",
    ".vtu",
)
REQUIRED_PATHS = (
    "case_id",
    "solver.name",
    "solver.version",
    "inputs_commit",
    "machine.host",
    "machine.cores",
    "mesh.id",
    "mesh.cells",
    "mesh.h_m",
    "mesh.total_volume_m3",
    "models.turbulence",
    "models.wall_treatment",
    "reference.area_m2",
    "reference.length_m",
    "reference.velocity_m_s",
    "reference.density_kg_m3",
    "convergence.residual_orders_dropped",
    "convergence.monitor_window_iters",
    "qoi",
    "run_check",
    "status",
)
# A generator writes these before a run. Run facts stay empty until the run.
PLANNED_PATHS = (
    "case_id",
    "study",
    "variant",
    "inputs",
    "status",
)
PLANNED_MESH_ONE_OF = ("mesh.source", "mesh.file")
PLANNED = "planned"
STATUSES = frozenset({PLANNED, "ok", "failed", "diverged"})
BOUND_AXES = ("x", "y", "z")


def main(argv: list[str] | None = None) -> int:
    """Check case folders and return an exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--cases-dir",
        action="append",
        default=None,
        metavar="PATH",
        help=(
            "case root relative to --root; repeat for more roots "
            f"(overrides {CASE_ROOTS_FILE})"
        ),
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=MAX_BYTES,
        help=f"size limit for a tracked file that is not in Git LFS (default {MAX_BYTES})",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    problems = check_root(root, args.max_bytes, case_roots=args.cases_dir)
    if problems:
        for problem in problems:
            print(problem)
        print(f"{len(problems)} problem(s)", file=sys.stderr)
        return 1
    print("ok: simulation cases")
    return 0


def check_root(
    root: Path,
    max_bytes: int = MAX_BYTES,
    case_roots: list[str] | None = None,
) -> list[str]:
    """Return problems for case folders and tracked sim files under root.

    ``case_roots`` lists case roots relative to ``root``. When it is None,
    the roots come from ``sim-cases.txt``, or from every ``cases`` folder.
    """
    problems: list[str] = []
    problems.extend(_check_cases(root, case_roots))
    problems.extend(_check_tracked(root, max_bytes))
    return problems


def read_case_roots(root: Path) -> list[str] | None:
    """Return the roots listed in ``sim-cases.txt``, or None without the file."""
    path = root / CASE_ROOTS_FILE
    if not path.is_file():
        return None
    roots: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            roots.append(line)
    return roots


def case_roots_for(
    root: Path, case_roots: list[str] | None = None
) -> tuple[list[Path], list[str]]:
    """Return the case root folders and the problems with the declaration."""
    declared = case_roots if case_roots is not None else read_case_roots(root)
    if declared is None:
        return _cases_dirs(root), []
    found: list[Path] = []
    problems: list[str] = []
    for entry in declared:
        text = entry.strip().replace("\\", "/").rstrip("/")
        parts = text.split("/")
        if (
            text in {"", "."}
            or text.startswith("/")
            or ":" in parts[0]
            or ".." in parts
        ):
            problems.append(
                f"{CASE_ROOTS_FILE}: {entry!r} must be a path relative to the repo root"
            )
            continue
        folder = root / text
        if not folder.is_dir():
            problems.append(f"{text}: declared case root does not exist")
            continue
        if folder not in found:
            found.append(folder)
    return found, problems


def case_folders(cases_root: Path) -> tuple[list[Path], list[Path]]:
    """Return the case folders in one root and the malformed attempt folders.

    A direct child is a case. ``_attempts/<run_id>/<case_id>/`` is a case.
    Any other child whose name starts with ``_`` or ``.`` is skipped.
    """
    cases: list[Path] = []
    bad_runs: list[Path] = []
    for child in _child_dirs(cases_root, keep=(ATTEMPTS_DIR,)):
        if child.name == ATTEMPTS_DIR:
            for run in _child_dirs(child):
                if not RUN_ID.match(run.name):
                    bad_runs.append(run)
                cases.extend(_child_dirs(run))
            continue
        cases.append(child)
    return cases, bad_runs


def _child_dirs(folder: Path, keep: tuple[str, ...] = ()) -> list[Path]:
    return sorted(
        path
        for path in folder.iterdir()
        if path.is_dir() and (path.name in keep or not path.name.startswith(("_", ".")))
    )


def _check_cases(root: Path, case_roots: list[str] | None = None) -> list[str]:
    roots, problems = case_roots_for(root, case_roots)
    for cases_dir in roots:
        cases, bad_runs = case_folders(cases_dir)
        for run in bad_runs:
            rel_run = run.relative_to(root).as_posix()
            problems.append(f"{rel_run}: run id must be YYYYMMDDTHHMMSS-<hex>")
        for child in cases:
            rel = child.relative_to(root).as_posix()
            if not CASE_NAME.match(child.name):
                problems.append(
                    f"{rel}: case folder name must be YYYY-MM-DD_study_variant"
                    " or a generated snake_case id"
                )
            case_file = child / "case.yaml"
            if not case_file.is_file():
                problems.append(f"{rel}: missing case.yaml")
                continue
            problems.extend(_check_case_yaml(case_file, child.name, rel))
            problems.extend(_check_figures(child, rel))
    return problems


def _cases_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    if not root.is_dir():
        return found
    for dirpath, dirnames, _filenames in _walk(root):
        if dirpath.name == DEFAULT_ROOT_NAME:
            found.append(dirpath)
            dirnames.clear()
    return found


def _check_case_yaml(path: Path, folder: str, rel: str) -> list[str]:
    problems: list[str] = []
    where = f"{rel}/case.yaml"
    try:
        data = parse_yaml(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, YamlError) as exc:
        return [f"{where}: {exc}"]
    if not isinstance(data, dict):
        return [f"{where}: the root must be a mapping"]
    status = _lookup(data, "status")
    planned = status == PLANNED
    for key in PLANNED_PATHS if planned else REQUIRED_PATHS:
        if _empty(_lookup(data, key)):
            problems.append(f"{where}: missing {key}")
    if planned and all(_empty(_lookup(data, key)) for key in PLANNED_MESH_ONE_OF):
        problems.append(f"{where}: missing mesh.source or mesh.file")
    case_id = _lookup(data, "case_id")
    if isinstance(case_id, str) and case_id and case_id != folder:
        problems.append(f"{where}: case_id {case_id} does not match {folder}")
    if isinstance(status, str) and status and status not in STATUSES:
        problems.append(
            f"{where}: status {status!r} is not planned, ok, failed, or diverged"
        )
    problems.extend(_check_qoi(data.get("qoi"), where, planned))
    problems.extend(_check_mesh_identity(data.get("mesh"), where))
    return problems


def _check_qoi(qoi: object, where: str, planned: bool) -> list[str]:
    if not isinstance(qoi, list):
        return []
    problems: list[str] = []
    if not qoi and not planned:
        problems.append(f"{where}: qoi is empty")
    # A planned case names its quantities; the output file comes with the run.
    fields = ("name", "units") if planned else ("name", "units", "file")
    for index, item in enumerate(qoi, start=1):
        if not isinstance(item, dict):
            problems.append(f"{where}: qoi item {index} is not a mapping")
            continue
        for field in fields:
            if item.get(field) in (None, ""):
                problems.append(f"{where}: qoi item {index} lacks {field}")
    return problems


def _check_mesh_identity(mesh: object, where: str) -> list[str]:
    """Check the optional mesh identity keys copied from ``<mesh>.meta.json``."""
    if not isinstance(mesh, dict):
        return []
    problems: list[str] = []
    for key in ("sha256", "source_stl_sha256"):
        value = mesh.get(key)
        if _empty(value) or _is_tbd(value):
            continue
        if not isinstance(value, str) or not SHA256.match(value):
            problems.append(f"{where}: mesh.{key} must be 64 hex digits or TBD")
    zones = mesh.get("zones")
    if not _empty(zones) and not _is_tbd(zones):
        if not isinstance(zones, list) or not all(
            isinstance(zone, str) and zone.strip() for zone in zones
        ):
            problems.append(f"{where}: mesh.zones must be a list of zone names or TBD")
    bounds = mesh.get("bounds_m")
    if not _empty(bounds) and not _is_tbd(bounds) and not _valid_bounds(bounds):
        problems.append(
            f"{where}: mesh.bounds_m must map x, y (and z) to [min, max] in metres, or TBD"
        )
    return problems


def _valid_bounds(bounds: object) -> bool:
    if not isinstance(bounds, dict) or not bounds:
        return False
    if any(axis not in BOUND_AXES for axis in bounds) or not {"x", "y"} <= set(bounds):
        return False
    for pair in bounds.values():
        if not isinstance(pair, list) or len(pair) != 2:
            return False
        if not all(
            isinstance(value, (int, float)) and not isinstance(value, bool)
            for value in pair
        ):
            return False
        low, high = pair
        if not (math.isfinite(low) and math.isfinite(high)) or low >= high:
            return False
    return True


def _empty(value: object) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _is_tbd(value: object) -> bool:
    return isinstance(value, str) and value.strip().upper().startswith("TBD")


def _lookup(data: dict, dotted: str) -> object:
    current: object = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _check_figures(case_dir: Path, rel: str) -> list[str]:
    post = case_dir / "post"
    if not post.is_dir():
        return []
    figures = [
        path
        for path in post.iterdir()
        if path.is_file() and path.suffix.lower() in FIGURE_SUFFIXES
    ]
    if not figures:
        return []
    scripts = [
        path
        for path in post.iterdir()
        if path.is_file() and path.suffix.lower() in SCRIPT_SUFFIXES
    ]
    problems: list[str] = []
    for figure in figures:
        figure_rel = f"{rel}/post/{figure.name}"
        if not scripts:
            problems.append(f"{figure_rel}: no script in post/")
        csv_path = post / f"{figure.stem}.csv"
        if not csv_path.is_file():
            problems.append(f"{figure_rel}: no {figure.stem}.csv next to the figure")
    return problems


def _check_tracked(root: Path, max_bytes: int) -> list[str]:
    tracked = _tracked(root)
    problems: list[str] = []
    openfoam_cases = _openfoam_cases(root)
    hashes: dict[str, str] = {}
    for rel in tracked:
        path = root / rel
        if not path.is_file():
            continue
        if _skip_rel(rel):
            continue
        if _is_solver_binary(rel, openfoam_cases):
            problems.append(f"{rel}: tracked solver binary")
        if path.suffix.lower() == ".mat":
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            previous = hashes.get(digest)
            if previous is not None:
                problems.append(f"{rel}: same bytes as {previous}")
            else:
                hashes[digest] = rel
        size = path.stat().st_size
        if size > max_bytes and not _in_lfs(root, rel, path):
            problems.append(f"{rel}: {size} bytes and not in Git LFS")
    return problems


def _is_solver_binary(rel: str, openfoam_cases: set[str]) -> bool:
    name = Path(rel).name
    lowered = name.lower()
    if lowered.startswith("d3plot"):
        return True
    for suffix in BINARY_SUFFIXES:
        if lowered.endswith(suffix):
            return True
    parts = rel.split("/")
    for case in openfoam_cases:
        prefix = case + "/"
        if not rel.startswith(prefix):
            continue
        rest = parts[len(case.split("/")) :]
        if any(TIME_PART.match(part) for part in rest[:-1]):
            return True
    return False


def _openfoam_cases(root: Path) -> set[str]:
    found: set[str] = set()
    for control in root.glob("**/system/controlDict"):
        if any(part in SKIP_DIRS for part in control.parts):
            continue
        case = control.parent.parent
        try:
            found.add(case.relative_to(root).as_posix())
        except ValueError:
            continue
    return found


def _in_lfs(root: Path, rel: str, path: Path) -> bool:
    if path.is_file():
        head = path.read_bytes()[:80]
        if head.startswith(b"version https://git-lfs.github.com/spec/v1"):
            return True
    value = _attribute(root, rel, "filter")
    return value == "lfs"


def _attribute(root: Path, rel: str, name: str) -> str | None:
    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "-C", str(root), "check-attr", name, "--", rel],
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            # "path: name: value"
            text = result.stdout.strip()
            if text.endswith(": unspecified"):
                return None
            marker = f": {name}: "
            if marker in text:
                return text.rsplit(marker, 1)[1].strip()
    return _attribute_from_files(root, rel, name)


def _attribute_from_files(root: Path, rel: str, name: str) -> str | None:
    value: str | None = None
    for attrs in _attribute_files(root, rel):
        for pattern, parsed in _read_attributes(attrs):
            if _attr_match(pattern, rel, attrs.parent, root) and name in parsed:
                raw = parsed[name]
                value = None if raw in {"unset", "unspecified"} else raw
    return value


def _attribute_files(root: Path, rel: str) -> list[Path]:
    files: list[Path] = []
    root_file = root / ".gitattributes"
    if root_file.is_file():
        files.append(root_file)
    current = root
    for part in Path(rel).parts[:-1]:
        current = current / part
        candidate = current / ".gitattributes"
        if candidate.is_file() and candidate not in files:
            files.append(candidate)
    return files


def _read_attributes(path: Path) -> list[tuple[str, dict[str, str]]]:
    rows: list[tuple[str, dict[str, str]]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        tokens = line.split()
        pattern = tokens[0]
        attrs: dict[str, str] = {}
        for token in tokens[1:]:
            if token.startswith("-"):
                attrs[token[1:]] = "unset"
            elif token.startswith("!"):
                attrs[token[1:]] = "unspecified"
            elif "=" in token:
                key, raw_value = token.split("=", 1)
                attrs[key] = raw_value
            else:
                attrs[token] = "set"
        rows.append((pattern, attrs))
    return rows


def _attr_match(pattern: str, rel: str, attrs_dir: Path, root: Path) -> bool:
    try:
        base = attrs_dir.relative_to(root).as_posix()
    except ValueError:
        base = ""
    local = rel[len(base) + 1 :] if base and rel.startswith(base + "/") else rel
    if "/" not in pattern.strip("/"):
        return _glob(pattern).match(Path(local).name) is not None
    target = pattern.removeprefix("/")
    return _glob(target).match(local) is not None


def _glob(pattern: str) -> re.Pattern[str]:
    parts: list[str] = []
    index = 0
    while index < len(pattern):
        if pattern.startswith("**", index):
            parts.append(".*")
            index += 2
        elif pattern[index] == "*":
            parts.append("[^/]*")
            index += 1
        else:
            parts.append(re.escape(pattern[index]))
            index += 1
    return re.compile("^" + "".join(parts) + "$")


def _tracked(root: Path) -> list[str]:
    try:
        # Shared helper from the same tools folder. Older copies lack it.
        from _repo_files import tracked_files
    except ImportError:
        return _tracked_local(root)
    found: list[str] = []
    for item in tracked_files(root):
        path = Path(item)
        if path.is_absolute():
            path = path.relative_to(root.resolve())
        found.append(path.as_posix())
    return found


def _tracked_local(root: Path) -> list[str]:
    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            return [item for item in result.stdout.split("\0") if item]
    found: list[str] = []
    for dirpath, _dirnames, filenames in _walk(root):
        for name in filenames:
            path = dirpath / name
            found.append(path.relative_to(root).as_posix())
    return found


def _walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        yield Path(dirpath), dirnames, filenames


def _skip_rel(rel: str) -> bool:
    return any(part in SKIP_DIRS for part in rel.split("/"))


if __name__ == "__main__":
    sys.exit(main())
