#!/usr/bin/env python3
"""Validate captured Codex custom-agent smoke outputs.

The validator is intentionally local-file only. It checks fixture declarations
against saved agent outputs; it never invokes Codex, models, networks, or app
runtimes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "id",
    "agent",
    "output_path",
    "intent",
    "evidence_packet",
    "expected_status",
    "expected_signals",
    "forbidden_signals",
}
VALID_STATUSES = {"DONE", "DONE_WITH_CONCERNS", "BLOCKED", "NEEDS_CONTEXT"}
AGENT_ROOT = Path("codex/agents")


def find_repo_root(start: Path) -> Path:
    probe = start if start.is_dir() else start.parent
    for candidate in [probe, *probe.parents]:
        if (candidate / AGENT_ROOT).is_dir():
            return candidate
    raise RuntimeError(f"could not locate repository root containing {AGENT_ROOT} from {start}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"fixture JSON parse error: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("fixture file must contain a JSON object")
    return payload


def require_string(value: Any, field: str, fixture_id: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{fixture_id}: field {field!r} must be a non-empty string")
    return value


def require_string_list(value: Any, field: str, fixture_id: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{fixture_id}: field {field!r} must be a list of strings")
    return value


def known_agents(repo_root: Path) -> set[str]:
    return {path.stem for path in (repo_root / AGENT_ROOT).glob("*.toml")}


def resolve_output_path(evaluator_root: Path, outputs_root: Path, output_path: str) -> Path:
    rel = Path(output_path)
    if rel.is_absolute():
        raise ValueError("absolute output_path is not allowed")
    if ".." in rel.parts:
        raise ValueError("output_path must not contain '..'")
    candidate = (evaluator_root / rel).resolve()
    root = outputs_root.resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("output_path must stay under evals/agent-smoke-output/") from exc
    return candidate


def validate_fixture_shape(
    fixture: Any,
    *,
    seen_ids: set[str],
    agent_names: set[str],
) -> tuple[str, str, str, str, list[str], list[str]]:
    if not isinstance(fixture, dict):
        raise ValueError("fixture entries must be JSON objects")
    fixture_id = require_string(fixture.get("id"), "id", "<unknown>")
    missing = sorted(REQUIRED_FIELDS - set(fixture))
    if missing:
        raise ValueError(f"{fixture_id}: missing required fields: {', '.join(missing)}")
    if fixture_id in seen_ids:
        raise ValueError(f"{fixture_id}: duplicate fixture id")
    seen_ids.add(fixture_id)

    agent = require_string(fixture["agent"], "agent", fixture_id)
    if agent not in agent_names:
        raise ValueError(f"{fixture_id}: unknown agent {agent}")
    output_path = require_string(fixture["output_path"], "output_path", fixture_id)
    require_string(fixture["intent"], "intent", fixture_id)
    if not isinstance(fixture["evidence_packet"], dict):
        raise ValueError(f"{fixture_id}: field 'evidence_packet' must be an object")
    expected_status = require_string(fixture["expected_status"], "expected_status", fixture_id)
    if expected_status not in VALID_STATUSES:
        raise ValueError(f"{fixture_id}: unsupported expected_status {expected_status}")
    expected_signals = require_string_list(fixture["expected_signals"], "expected_signals", fixture_id)
    forbidden_signals = require_string_list(
        fixture["forbidden_signals"], "forbidden_signals", fixture_id
    )
    return fixture_id, agent, output_path, expected_status, expected_signals, forbidden_signals


def validate_output(
    *,
    fixture_id: str,
    output_file: Path,
    expected_status: str,
    expected_signals: list[str],
    forbidden_signals: list[str],
) -> list[str]:
    failures: list[str] = []
    if not output_file.is_file():
        return [f"missing output: {output_file}"]
    text = output_file.read_text(encoding="utf-8")
    status_line = f"Status: {expected_status}"
    if status_line not in text.splitlines():
        failures.append(f"missing status line: {status_line}")
    for signal in expected_signals:
        if signal not in text:
            failures.append(f"missing expected signal: {signal}")
    for signal in forbidden_signals:
        if signal in text:
            failures.append(f"forbidden signal present: {signal}")
    return failures


def validate(fixtures_path: Path, outputs_root: Path) -> int:
    payload = load_json(fixtures_path)
    if "schema" not in payload or "fixtures" not in payload:
        raise ValueError("fixture file requires top-level 'schema' and 'fixtures' fields")
    if payload["schema"] != 1:
        raise ValueError(f"unsupported schema: {payload['schema']}")
    fixtures = payload["fixtures"]
    if not isinstance(fixtures, list):
        raise ValueError("'fixtures' must be a list")

    repo_root = find_repo_root(fixtures_path.resolve())
    evaluator_root = outputs_root.resolve().parent.parent
    agent_names = known_agents(repo_root)
    seen_ids: set[str] = set()
    failed = 0

    for fixture in fixtures:
        try:
            fixture_id, agent, output_path, expected_status, expected_signals, forbidden_signals = (
                validate_fixture_shape(fixture, seen_ids=seen_ids, agent_names=agent_names)
            )
            output_file = resolve_output_path(evaluator_root, outputs_root, output_path)
            failures = validate_output(
                fixture_id=fixture_id,
                output_file=output_file,
                expected_status=expected_status,
                expected_signals=expected_signals,
                forbidden_signals=forbidden_signals,
            )
        except ValueError as exc:
            failed += 1
            fixture_id = fixture.get("id", "<unknown>") if isinstance(fixture, dict) else "<unknown>"
            agent = fixture.get("agent", "<unknown>") if isinstance(fixture, dict) else "<unknown>"
            print(f"FAIL {fixture_id} ({agent}): {exc}")
            continue

        if failures:
            failed += 1
            print(f"FAIL {fixture_id} ({agent})")
            for failure in failures:
                print(f"  - {failure}")
        else:
            print(f"PASS {fixture_id} ({agent})")

    total = len(fixtures)
    passed = total - failed
    print(f"Summary: {passed}/{total} passed")
    return 0 if failed == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--outputs", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        return validate(args.fixtures, args.outputs)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
