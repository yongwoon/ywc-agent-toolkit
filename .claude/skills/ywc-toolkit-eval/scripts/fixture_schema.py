#!/usr/bin/env python3
"""v2 evaluation-fixture validator and workspace manifest normalizer.

Two contracts live here, and every later task in this batch builds on them:

* `validate_case` — the v2 case shape (spec AC3) and the closed
  `expected_checks` whitelist (AC4). A fixture describes *what to assert*;
  it can never describe *what to run*.
* `normalize_manifest` — `fixture_root` boundary sealing (AC5). Every declared
  path is resolved with `realpath` and must land inside the root, so absolute
  paths, `..` traversal, and symlinks pointing outside are all refused.

v1 fixtures (anything without `schema: 2`) are accepted read-only and
unchanged — the existing `evals.json` and `trigger-cases.json` datasets must
keep passing.

Stdlib only, matching score.py's no-dependency convention.
"""
from __future__ import annotations

import os
from pathlib import Path

import verifier_registry

SCHEMA_VERSION = 2

REQUIRED_FIELDS: tuple[str, ...] = (
    "id", "prompt", "language", "category", "should_trigger", "expected_checks")

CATEGORIES: frozenset[str] = frozenset({"happy_path", "negative", "boundary"})

# The closed set of assertions a fixture may request (AC4). Adding a member
# here is an evaluator-code change and therefore a reviewed change.
CHECK_TYPES: frozenset[str] = frozenset({
    "stdout_regex", "stderr_regex", "file_exists", "file_regex",
    "json_path_equals", "verifier",
})

# Keys that would turn a fixture into a command. Rejected wherever they appear
# anywhere in the case — at any nesting depth and in any letter case. A
# shallow check on `expected_checks` entries would read as closed while
# leaving `{"expected": {"command": ...}}` and top-level keys wide open, and
# the next module to grow a passthrough would inherit that hole silently.
FORBIDDEN_CHECK_KEYS: frozenset[str] = frozenset({
    "command", "argv", "shell", "exec", "executable", "cmd", "script",
    "entrypoint", "interpreter", "run",
})

# Path-valued manifest fields, all sealed to `fixture_root`.
PATH_FIELDS: tuple[str, ...] = ("fixture_files", "output_paths")


class ManifestError(ValueError):
    """Raised when a case cannot yield a safe, fully-sealed manifest."""


def is_v2(case: dict) -> bool:
    """True when `case` declares the v2 schema."""
    return isinstance(case, dict) and case.get("schema") == SCHEMA_VERSION


def _scan_forbidden_keys(node: object, where: str) -> list[str]:
    """Report every command-naming key reachable from `node`, at any depth.

    Case-insensitive and recursive on purpose: `Command` and
    `{"expected": {"argv": [...]}}` are the same smuggling attempt as a
    top-level `command`, and only a full walk can honestly claim the
    whitelist is closed.
    """
    errors: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(key, str) and key.lower() in FORBIDDEN_CHECK_KEYS:
                errors.append(
                    f"{where}: forbidden key {key!r} — a fixture may not name a "
                    f"command; use type 'verifier' with a registered verifier_id "
                    f"instead")
            errors.extend(_scan_forbidden_keys(value, f"{where}.{key}"))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            errors.extend(_scan_forbidden_keys(item, f"{where}[{index}]"))
    return errors


def _validate_check(index: int, check: object) -> list[str]:
    """Validate one `expected_checks` entry; returns human-readable errors."""
    where = f"expected_checks[{index}]"
    if not isinstance(check, dict):
        return [f"{where}: must be an object, got {type(check).__name__}"]

    errors: list[str] = []

    check_type = check.get("type")
    if check_type is None:
        errors.append(f"{where}: missing 'type'")
    elif check_type not in CHECK_TYPES:
        errors.append(
            f"{where}: unsupported check type {check_type!r}; "
            f"allowed types are {', '.join(sorted(CHECK_TYPES))}")
    elif check_type == "verifier":
        verifier_id = check.get("verifier_id")
        if verifier_id is None:
            errors.append(f"{where}: type 'verifier' requires 'verifier_id'")
        elif not verifier_registry.is_registered(verifier_id):
            errors.append(
                f"{where}: verifier_id {verifier_id!r} is not in the evaluator "
                f"registry; registered ids are "
                f"{', '.join(verifier_registry.verifier_ids())}")

    return errors


def validate_case(case: dict) -> list[str]:
    """Return every validation error for `case`; an empty list means valid.

    v1 cases pass unconditionally — they are read-only compatibility input and
    are validated by their own existing consumers, not by this module.
    """
    if not isinstance(case, dict):
        return [f"case must be an object, got {type(case).__name__}"]
    if not is_v2(case):
        return []

    errors: list[str] = _scan_forbidden_keys(case, "case")

    for field in REQUIRED_FIELDS:
        if field not in case:
            errors.append(f"missing required field {field!r}")

    for field in ("id", "prompt", "language"):
        value = case.get(field)
        if field in case and (not isinstance(value, str) or not value.strip()):
            errors.append(f"{field!r} must be a non-empty string")

    if "category" in case and case["category"] not in CATEGORIES:
        errors.append(
            f"'category' must be exactly one of {', '.join(sorted(CATEGORIES))}; "
            f"got {case['category']!r}")

    if "should_trigger" in case and not isinstance(case["should_trigger"], bool):
        errors.append(
            f"'should_trigger' must be a boolean, got "
            f"{type(case['should_trigger']).__name__}")

    checks = case.get("expected_checks")
    if "expected_checks" in case:
        if not isinstance(checks, list):
            errors.append("'expected_checks' must be a list")
        elif not checks:
            errors.append("'expected_checks' must declare at least one check")
        else:
            for index, check in enumerate(checks):
                errors.extend(_validate_check(index, check))

    for verifier_id in case.get("verifier_ids", []) or []:
        if not verifier_registry.is_registered(verifier_id):
            errors.append(
                f"verifier_ids: {verifier_id!r} is not in the evaluator registry")

    return errors


def _seal(raw: object, field: str, root: Path) -> str:
    """Resolve one declared path and prove it stays inside `root`.

    `os.path.realpath` is what makes the symlink case work: it follows every
    link before the containment test, so a link inside the root that points
    outside is caught rather than trusted for its lexical prefix.
    """
    if not isinstance(raw, str) or not raw.strip():
        raise ManifestError(f"{field}: path entries must be non-empty strings")
    if os.path.isabs(raw):
        raise ManifestError(f"{field}: absolute path {raw!r} is not allowed")

    resolved = os.path.realpath(root / raw)
    root_real = os.path.realpath(root)
    if resolved != root_real and not resolved.startswith(root_real + os.sep):
        raise ManifestError(
            f"{field}: {raw!r} resolves to {resolved!r}, outside fixture_root "
            f"{root_real!r}")
    return resolved


def normalize_manifest(case: dict, fixture_root: Path | str) -> dict:
    """Validate `case` and return its workspace manifest with sealed paths.

    Raises `ManifestError` if the case is invalid or any declared path escapes
    `fixture_root`. Callers get either a fully-sealed manifest or an exception —
    never a partially-trusted one.
    """
    errors = validate_case(case)
    if errors:
        raise ManifestError(
            f"case {case.get('id', '<no id>')!r} is invalid: " + "; ".join(errors))

    root = Path(fixture_root)
    if not root.is_dir():
        raise ManifestError(f"fixture_root {str(root)!r} is not a directory")

    manifest: dict = {
        "fixture_root": os.path.realpath(root),
        "target_skill": case.get("target_skill"),
        "skill_dependencies": list(case.get("skill_dependencies", []) or []),
        "verifier_ids": list(case.get("verifier_ids", []) or []),
    }
    for field in PATH_FIELDS:
        manifest[field] = [
            _seal(raw, field, root) for raw in (case.get(field, []) or [])]

    for verifier_id in manifest["verifier_ids"]:
        if not verifier_registry.is_registered(verifier_id):
            raise ManifestError(
                f"verifier_ids: {verifier_id!r} is not in the evaluator registry")

    return manifest
