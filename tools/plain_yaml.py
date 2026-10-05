#!/usr/bin/env python3
"""Read a small YAML subset.

The subset is mappings, nested mappings, lists of mappings, and scalars.
Comments and quoted strings are supported.
Anchors, tags, and flow collections are not supported.
"""

from __future__ import annotations

import re
from typing import Any

_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")


class YamlError(ValueError):
    """The text is not in the supported subset."""

    def __init__(self, line: int, message: str) -> None:
        super().__init__(f"line {line}: {message}")
        self.line = line


def parse_yaml(text: str) -> Any:
    """Parse ``text`` and return a dict, list, or scalar."""
    lines: list[tuple[int, int, str]] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or stripped in {"---", "..."}:
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip(" \t"))]:
            raise YamlError(lineno, "use spaces for indent")
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((lineno, indent, raw.strip()))
    if not lines:
        return {}
    value, index = _parse_block(lines, 0, lines[0][1])
    if index != len(lines):
        raise YamlError(lines[index][0], "unexpected content")
    return value


def _parse_block(
    lines: list[tuple[int, int, str]], index: int, indent: int
) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    _lineno, next_indent, text = lines[index]
    if next_indent < indent:
        return {}, index
    if text.startswith("- "):
        return _parse_list(lines, index, next_indent)
    return _parse_map(lines, index, next_indent)


def _parse_map(
    lines: list[tuple[int, int, str]], index: int, indent: int
) -> tuple[dict[str, Any], int]:
    mapping: dict[str, Any] = {}
    while index < len(lines):
        lineno, line_indent, text = lines[index]
        if line_indent < indent:
            break
        if line_indent > indent:
            raise YamlError(lineno, "unexpected indent")
        if text.startswith("- "):
            break
        key, rest = _split_key(lineno, text)
        index += 1
        if rest == "":
            if index < len(lines) and lines[index][1] > line_indent:
                child_indent = lines[index][1]
                child, index = _parse_block(lines, index, child_indent)
                mapping[key] = child
            else:
                mapping[key] = None
        else:
            mapping[key] = _scalar(lineno, rest)
    return mapping, index


def _parse_list(
    lines: list[tuple[int, int, str]], index: int, indent: int
) -> tuple[list[Any], int]:
    items: list[Any] = []
    while index < len(lines):
        lineno, line_indent, text = lines[index]
        if line_indent < indent:
            break
        if line_indent != indent or not text.startswith("- "):
            break
        body = text[2:].strip()
        index += 1
        if body == "":
            if index < len(lines) and lines[index][1] > line_indent:
                child, index = _parse_block(lines, index, lines[index][1])
                items.append(child)
            else:
                items.append(None)
            continue
        key, rest, is_key = _maybe_key(body)
        if not is_key:
            items.append(_scalar(lineno, body))
            continue
        item: dict[str, Any] = {}
        if rest == "":
            if index < len(lines) and lines[index][1] > line_indent:
                child, index = _parse_block(lines, index, lines[index][1])
                item[key] = child
            else:
                item[key] = None
        else:
            item[key] = _scalar(lineno, rest)
        while index < len(lines):
            key_line, key_indent, key_text = lines[index]
            if key_indent <= line_indent or key_text.startswith("- "):
                break
            child_key, child_rest = _split_key(key_line, key_text)
            index += 1
            if child_rest == "":
                if index < len(lines) and lines[index][1] > key_indent:
                    child, index = _parse_block(lines, index, lines[index][1])
                    item[child_key] = child
                else:
                    item[child_key] = None
            else:
                item[child_key] = _scalar(key_line, child_rest)
        items.append(item)
    return items, index


def _split_key(lineno: int, text: str) -> tuple[str, str]:
    key, rest, is_key = _maybe_key(text)
    if not is_key:
        raise YamlError(lineno, "expected a key")
    return key, rest


def _maybe_key(text: str) -> tuple[str, str, bool]:
    if text.startswith(("'", '"')):
        return "", text, False
    key, sep, rest = text.partition(":")
    if sep != ":" or not _KEY.match(key.strip()):
        return "", text, False
    return key.strip(), rest.strip(), True


def _scalar(lineno: int, text: str) -> Any:
    raw = text.strip()
    if raw.startswith('"'):
        end = raw.find('"', 1)
        if end < 0:
            raise YamlError(lineno, "unterminated string")
        return raw[1:end]
    if raw.startswith("'"):
        end = raw.find("'", 1)
        if end < 0:
            raise YamlError(lineno, "unterminated string")
        return raw[1:end]
    if " #" in raw:
        raw = raw.split(" #", 1)[0].rstrip()
    if raw in {"", "null", "~"}:
        return None
    if raw == "true":
        return True
    if raw == "false":
        return False
    if _is_int(raw):
        return int(raw)
    if _is_float(raw):
        return float(raw)
    return raw


def _is_int(text: str) -> bool:
    digits = text[1:] if text.startswith(("+", "-")) else text
    return bool(digits) and digits.isdigit()


def _is_float(text: str) -> bool:
    if text.count(".") != 1:
        return False
    left, right = text.split(".", 1)
    if not right.isdigit():
        return False
    return _is_int(left) if left not in {"", "+", "-"} else True
