"""Read-only V1 compatibility and strict V2 evaluator fixture validation."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from verifier_registry import VERIFIER_REGISTRY


class FixtureValidationError(ValueError):
    """A fixture violates the evaluator-owned input contract."""


V2_CATEGORIES = {"happy_path", "negative", "boundary"}
CHECK_TYPES = {"stdout_regex", "stderr_regex", "file_exists", "file_regex", "json_path_equals", "verifier"}
FORBIDDEN_KEYS = {"command", "executable", "argv", "cwd", "timeout", "environment", "env", "shell"}
CHECK_FIELDS: dict[str, tuple[tuple[str, type], ...]] = {
    "stdout_regex": (("regex", str),),
    "stderr_regex": (("regex", str),),
    "file_exists": (("path", str),),
    "file_regex": (("path", str), ("regex", str)),
    "json_path_equals": (("path", str), ("json_path", str), ("expected_value", object)),
    "verifier": (("verifier_id", str),),
}


def _require(value: Any, name: str, expected: type) -> None:
    if not isinstance(value, expected) or (expected is str and not value.strip()):
        raise FixtureValidationError(f"{name} is required and must be a {expected.__name__}")


def _require_json_value(value: Any, name: str) -> None:
    if value is None or isinstance(value, (str, int, float, bool)):
        return
    if isinstance(value, list):
        for item in value:
            _require_json_value(item, name)
        return
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        for item in value.values():
            _require_json_value(item, name)
        return
    raise FixtureValidationError(f"{name} must be a JSON value")


def _safe_relative(value: Any, name: str) -> Path:
    _require(value, name, str)
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise FixtureValidationError(f"{name} must be a relative path without '..'")
    return path


def _contained(root: Path, relative: str, name: str, *, must_exist: bool) -> None:
    path = _safe_relative(relative, name)
    candidate = root / path
    if must_exist and not candidate.exists():
        raise FixtureValidationError(f"{name} does not exist: {relative}")
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve(strict=must_exist)
    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise FixtureValidationError(f"{name} escapes fixture root: {relative}") from exc


def _validate_check(check: Any, declared_verifiers: set[str], manifest_root: Path) -> None:
    if not isinstance(check, dict):
        raise FixtureValidationError("expected_checks entries must be objects")
    forbidden = FORBIDDEN_KEYS.intersection(check)
    if forbidden:
        raise FixtureValidationError(f"fixture execution fields are not permitted: {', '.join(sorted(forbidden))}")
    check_type = check.get("type")
    if check_type not in CHECK_TYPES:
        raise FixtureValidationError(f"unsupported check type: {check_type}")
    for field, expected in CHECK_FIELDS[check_type]:
        if field not in check:
            raise FixtureValidationError(f"expected_checks.{field} is required for {check_type}")
        if expected is object:
            _require_json_value(check[field], f"expected_checks.{field}")
        else:
            _require(check[field], f"expected_checks.{field}", expected)
    for path_key in ("path", "file", "output_path"):
        if path_key in check:
            _contained(manifest_root, check[path_key], f"expected_checks.{path_key}", must_exist=False)
    if check_type == "verifier":
        verifier_id = check.get("verifier_id")
        _require(verifier_id, "verifier_id", str)
        if verifier_id not in declared_verifiers or verifier_id not in VERIFIER_REGISTRY:
            raise FixtureValidationError(f"unknown verifier: {verifier_id}")


def _reject_execution_fields(value: Any) -> None:
    if isinstance(value, dict):
        forbidden = FORBIDDEN_KEYS.intersection(value)
        if forbidden:
            raise FixtureValidationError(f"fixture execution fields are not permitted: {', '.join(sorted(forbidden))}")
        for nested in value.values():
            _reject_execution_fields(nested)
    elif isinstance(value, list):
        for nested in value:
            _reject_execution_fields(nested)


def _validate_v2(payload: dict[str, Any], fixture_root: Path, available_skills: set[str] | None) -> None:
    _reject_execution_fields(payload)
    if "evals" in payload or "fixtures" in payload:
        raise FixtureValidationError("V1/V2 fixture shape is ambiguous")
    for key, expected in (("id", str), ("prompt", str), ("language", str), ("category", str), ("should_trigger", bool), ("expected_checks", list), ("workspace", dict)):
        _require(payload.get(key), key, expected)
    if payload["category"] not in V2_CATEGORIES:
        raise FixtureValidationError(f"unsupported category: {payload['category']}")
    workspace = payload["workspace"]
    for key, expected in (("fixture_root", str), ("target_skill", str), ("skill_dependencies", list), ("fixture_files", list), ("output_paths", list), ("evidence_packet", dict), ("verifier_ids", list)):
        _require(workspace.get(key), f"workspace.{key}", expected)
    fixture_dir = _safe_relative(workspace["fixture_root"], "workspace.fixture_root")
    manifest_root = fixture_root / fixture_dir
    if not manifest_root.is_dir():
        raise FixtureValidationError(f"workspace.fixture_root does not exist: {fixture_dir}")
    try:
        manifest_root.resolve().relative_to(fixture_root.resolve())
    except ValueError as exc:
        raise FixtureValidationError(f"workspace.fixture_root escapes fixture root: {fixture_dir}") from exc
    verifier_ids = set(workspace["verifier_ids"])
    if not all(isinstance(value, str) and value in VERIFIER_REGISTRY for value in verifier_ids):
        raise FixtureValidationError("workspace.verifier_ids contains an unknown verifier")
    for dependency in workspace["skill_dependencies"]:
        _require(dependency, "workspace.skill_dependencies item", str)
        if available_skills is not None and dependency not in available_skills:
            raise FixtureValidationError(f"unknown dependency: {dependency}")
    if available_skills is not None and workspace["target_skill"] not in available_skills:
        raise FixtureValidationError(f"unknown target skill: {workspace['target_skill']}")
    for relative in workspace["fixture_files"]:
        _contained(manifest_root, relative, "workspace.fixture_files item", must_exist=True)
    for relative in workspace["output_paths"]:
        _contained(manifest_root, relative, "workspace.output_paths item", must_exist=False)
    for check in payload["expected_checks"]:
        _validate_check(check, verifier_ids, manifest_root)


def _validate_v2_agent(payload: dict[str, Any], fixture_root: Path) -> None:
    _reject_execution_fields(payload)
    fixtures = payload.get("fixtures")
    _require(fixtures, "fixtures", list)
    if any(key in payload for key in ("id", "prompt", "workspace", "expected_checks", "evals")):
        raise FixtureValidationError("V1/V2 fixture shape is ambiguous")
    for fixture in fixtures:
        if not isinstance(fixture, dict):
            raise FixtureValidationError("agent fixture entries must be objects")
        forbidden = FORBIDDEN_KEYS.intersection(fixture)
        if forbidden:
            raise FixtureValidationError(f"fixture execution fields are not permitted: {', '.join(sorted(forbidden))}")
        for key, expected in (("id", str), ("agent", str), ("input", dict), ("evidence_packet", dict), ("expected_status", str), ("expected_signals", list), ("forbidden_signals", list), ("output_path", str)):
            _require(fixture.get(key), key, expected)
        _contained(fixture_root, fixture["output_path"], "output_path", must_exist=False)


def validate_fixture(payload: dict[str, Any], *, fixture_root: Path, available_skills: set[str] | None = None) -> dict[str, Any]:
    """Return a copied normalized payload or raise a deterministic validation error."""
    if not isinstance(payload, dict):
        raise FixtureValidationError("fixture document must be an object")
    normalized = copy.deepcopy(payload)
    schema = normalized.get("schema")
    if schema == 2:
        if "fixtures" in normalized:
            _validate_v2_agent(normalized, fixture_root)
        else:
            _validate_v2(normalized, fixture_root, available_skills)
        normalized["v1_remaining"] = 0
        return normalized
    if schema == 1 or "schema" not in normalized:
        if "schema" in normalized and schema != 1:
            raise FixtureValidationError(f"unsupported fixture schema: {schema}")
        if "schema" not in normalized and not ("evals" in normalized or "fixtures" in normalized):
            raise FixtureValidationError("V1 fixture must contain evals or fixtures")
        normalized["schema"] = 1
        normalized["v1_remaining"] = len(normalized.get("evals", normalized.get("fixtures", [])))
        return normalized
    raise FixtureValidationError(f"unsupported fixture schema: {schema}")
