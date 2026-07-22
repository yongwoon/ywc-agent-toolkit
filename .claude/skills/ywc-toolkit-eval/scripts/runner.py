#!/usr/bin/env python3
"""Isolated evaluation runner: dispatch a skill, then score the outcome.

What isolation means here, stated exactly, because overclaiming it is the
failure the spec explicitly guards against:

* **catalog isolation — abandoned.** Route N1 runs against the developer's
  real installation, so every installed skill loads. That is why attribution
  is claimed only from with/without ablation, never from a single run.
* **workspace isolation — kept, and mandatory.** Each case runs in its own
  temporary directory. This is independent of authentication and is what makes
  it safe to evaluate a skill that commits, pushes, or writes files.

The grade is `best-effort`. Nothing here claims host-filesystem
unobservability; a dispatch could still read outside its workspace.

Detection of undeclared writes is a before/after snapshot of the workspace,
compared against the case's declared `output_paths`. Anything else that
appeared, changed, vanished, or was re-pointed is a `FAIL` — that check is the
only reason a destructive skill can be evaluated at all.

Stdlib only, matching score.py's no-dependency convention.

  python3 .claude/skills/ywc-toolkit-eval/scripts/runner.py --adapter fake --case <id>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claude_adapter  # noqa: E402
import fixture_schema  # noqa: E402
import verifier_registry  # noqa: E402

# AC6 — every run resolves to exactly one of these.
STATUSES: tuple[str, ...] = (
    "PASS", "FAIL", "SKIPPED_UNAVAILABLE", "ERROR", "INCONCLUSIVE")

# Measured on the spike at 243 loaded skills, not estimated (spec §NFR1").
COST_PER_DISPATCH_USD = 0.54

WORKSPACE_PREFIX = "ywc-eval-"

SKILL_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = SKILL_ROOT / "evals" / "fixtures"
# Gitignored by this task; reports live beside it as tracked `<date>-<name>.md`.
RUNS_ROOT = (Path(__file__).resolve().parents[4]
             / "docs" / "skill-agent-eval" / "claude" / "runs")

# Credential shapes stripped from any recorded text. The eval prompt and the
# model's reply both pass through here, and a run record is a file on disk.
_REDACTIONS: tuple[tuple[re.Pattern, str], ...] = (
    (re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}"), "<REDACTED:anthropic-key>"),
    (re.compile(r"ghp_[A-Za-z0-9]{16,}"), "<REDACTED:github-token>"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "<REDACTED:github-pat>"),
    (re.compile(r"gho_[A-Za-z0-9]{16,}"), "<REDACTED:github-oauth>"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "<REDACTED:aws-key>"),
)

MAX_RECORDED_CHARS = 4000


def new_run_id() -> str:
    """A collision-free id per run. Random, not time-based.

    Two runs can legitimately start inside the same clock tick, and a
    timestamp id would collide there — exactly the case AC19 asks about.
    """
    return secrets.token_hex(8)


def make_workspace(run_id: str) -> Path:
    """Create this run's private workspace."""
    return Path(tempfile.mkdtemp(prefix=f"{WORKSPACE_PREFIX}{run_id}-"))


def cleanup(workspace: Path | str, keep_on_fail: bool = False,
            failed: bool = False) -> None:
    """Remove the workspace unless it failed and retention was requested.

    Retention is opt-in and failure-only: a passing run must leave nothing
    behind, or the artifact budget in AC13 is meaningless.
    """
    path = Path(workspace)
    if keep_on_fail and failed:
        return
    shutil.rmtree(path, ignore_errors=True)


def redact(text: str) -> str:
    """Strip credential-shaped substrings and cap the recorded length."""
    for pattern, replacement in _REDACTIONS:
        text = pattern.sub(replacement, text)
    if len(text) > MAX_RECORDED_CHARS:
        text = text[:MAX_RECORDED_CHARS] + f"... [truncated, {len(text)} chars]"
    return text


def snapshot(workspace: Path | str) -> dict[str, str]:
    """Map every path under `workspace` to a fingerprint of its content.

    Symlinks are fingerprinted by their *target*, not by the content they
    point at. A dispatch that re-points a link without touching any file is a
    real undeclared change, and following the link would hide it.
    """
    root = Path(workspace)
    entries: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        key = str(path.relative_to(root))
        if path.is_symlink():
            entries[key] = f"symlink:{os.readlink(path)}"
        elif path.is_dir():
            entries[key] = "dir"
        else:
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError as exc:
                digest = f"unreadable:{exc.errno}"
            entries[key] = f"file:{digest}"
    return entries


def diff_snapshot(before: dict[str, str], after: dict[str, str],
                  allowed_paths: list[str]) -> list[str]:
    """Report every change not covered by a declared output path.

    `allowed_paths` holds absolute, already-sealed paths from the manifest;
    they are matched by basename so a declared output can be written without
    tripping the gate.
    """
    allowed = {Path(p).name for p in allowed_paths}
    changes: list[str] = []

    for key in sorted(set(before) | set(after)):
        if Path(key).name in allowed:
            continue
        old, new = before.get(key), after.get(key)
        if old == new:
            continue
        if old is None:
            changes.append(f"added: {key}")
        elif new is None:
            changes.append(f"deleted: {key}")
        else:
            changes.append(f"modified: {key} ({old} -> {new})")
    return changes


def _run_check(check: dict, result: str, workspace: Path) -> tuple[bool, str]:
    """Evaluate one deterministic check. Returns (passed, detail)."""
    kind = check.get("type")

    if kind in ("stdout_regex", "stderr_regex"):
        pattern = check.get("pattern", "")
        return (bool(re.search(pattern, result)), f"pattern {pattern!r}")

    if kind == "file_exists":
        target = workspace / check.get("path", "")
        return (target.exists(), f"path {check.get('path')!r}")

    if kind == "file_regex":
        target = workspace / check.get("path", "")
        if not target.is_file():
            return (False, f"missing file {check.get('path')!r}")
        content = target.read_text(encoding="utf-8", errors="replace")
        return (bool(re.search(check.get("pattern", ""), content)),
                f"file {check.get('path')!r}")

    if kind == "json_path_equals":
        target = workspace / check.get("path", "")
        if not target.is_file():
            return (False, f"missing file {check.get('path')!r}")
        try:
            payload = json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return (False, f"invalid json: {exc}")
        node = payload
        for segment in str(check.get("json_path", "")).split("."):
            if not segment:
                continue
            if not isinstance(node, dict) or segment not in node:
                return (False, f"json path {check.get('json_path')!r} not found")
            node = node[segment]
        return (node == check.get("expected_value"),
                f"json path {check.get('json_path')!r}")

    if kind == "verifier":
        # Resolution alone proves the id is registered; actually executing the
        # verifier belongs to the deterministic CI tier, not to a dispatch run.
        entry = verifier_registry.resolve(check["verifier_id"])
        return (True,
                f"verifier {check['verifier_id']!r} resolved ({entry['argv'][0]})")

    return (False, f"unsupported check type {kind!r}")


def estimate_cost(dispatches: int) -> float:
    """Projected spend, so a run can be aborted before it costs anything."""
    return dispatches * COST_PER_DISPATCH_USD


def announce_cost(dispatches: int, stream=sys.stderr) -> None:
    """Print the projected dispatch count and cost before any run starts."""
    print(f"[runner] planned dispatches: {dispatches} - "
          f"estimated cost: ${estimate_cost(dispatches):.2f} "
          f"(${COST_PER_DISPATCH_USD:.2f}/dispatch, measured at 243 loaded skills)",
          file=stream)


def run_case(case: dict, adapter=None, attempt: int = 1,
             keep_on_fail: bool = False, record_root: Path | None = None) -> dict:
    """Execute one case in its own workspace and return a status record.

    The workspace is always removed (or deliberately retained on failure)
    before returning — including on timeout, which is the path most likely to
    leak a directory.
    """
    adapter = adapter or claude_adapter
    run_id = new_run_id()
    workspace = make_workspace(run_id)
    started = time.monotonic()

    record: dict = {
        "run_id": run_id,
        "case_id": case.get("id", "<no id>"),
        "attempt": attempt,
        "status": "INCONCLUSIVE",
        "duration_ms": 0,
        "workspace": str(workspace),
        "artifact_path": None,
        "activation_observability": "unavailable",
        "undeclared_changes": [],
        "checks": [],
        "result": "",
    }

    failed = True
    try:
        manifest = fixture_schema.normalize_manifest(case, FIXTURE_ROOT)

        before = snapshot(workspace)
        payload = adapter.dispatch(
            case.get("target_skill", ""), case.get("prompt", ""), workspace)
        after = snapshot(workspace)

        record["result"] = redact(str(payload.get("result", "")))
        record["undeclared_changes"] = diff_snapshot(
            before, after, manifest["output_paths"])

        if payload.get("is_error"):
            record["status"] = "ERROR"
        elif record["undeclared_changes"]:
            # Checks may well have passed; an undeclared write still fails the
            # case, because containment is the property being asserted.
            record["status"] = "FAIL"
        else:
            results = [_run_check(c, record["result"], workspace)
                       for c in case.get("expected_checks", [])]
            record["checks"] = [{"passed": ok, "detail": redact(detail)}
                                for ok, detail in results]
            record["status"] = "PASS" if all(ok for ok, _ in results) else "FAIL"

    except claude_adapter.AdapterUnavailable as exc:
        record["status"] = "SKIPPED_UNAVAILABLE"
        record["result"] = redact(str(exc))
    except claude_adapter.AdapterTimeout as exc:
        record["status"] = "ERROR"
        record["result"] = redact(f"timeout: {exc}")
    except (fixture_schema.ManifestError, verifier_registry.UnknownVerifier,
            OSError, ValueError, KeyError) as exc:
        record["status"] = "ERROR"
        record["result"] = redact(f"{type(exc).__name__}: {exc}")
    finally:
        record["duration_ms"] = int((time.monotonic() - started) * 1000)
        failed = record["status"] != "PASS"
        cleanup(workspace, keep_on_fail=keep_on_fail, failed=failed)

    if record_root is not None:
        record["artifact_path"] = _write_record(record, record_root)
    return record


def _write_record(record: dict, record_root: Path) -> str:
    """Persist the redacted record under a gitignored run directory."""
    target_dir = Path(record_root) / record["run_id"]
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "record.json"
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2),
                      encoding="utf-8")
    return str(target)


def load_case(case_id: str) -> dict:
    """Load one v2 fixture by its `id` field."""
    for path in sorted(FIXTURE_ROOT.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        if case.get("id") == case_id:
            return case
    raise SystemExit(f"no fixture with id {case_id!r} under {FIXTURE_ROOT}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--adapter", choices=("claude", "fake"), default="fake",
                        help="'fake' costs nothing and needs no CLI (default)")
    parser.add_argument("--case", required=True, help="fixture id to run")
    parser.add_argument("--retain-failed-artifacts", action="store_true",
                        help="keep the workspace when the case does not pass")
    parser.add_argument("--record", action="store_true",
                        help="write a redacted record under the gitignored runs root")
    args = parser.parse_args(argv)

    case = load_case(args.case)
    adapter = (claude_adapter if args.adapter == "claude"
               else claude_adapter.FakeAdapter(result="DONE"))

    if args.adapter == "claude":
        announce_cost(1)

    record = run_case(case, adapter=adapter,
                      keep_on_fail=args.retain_failed_artifacts,
                      record_root=RUNS_ROOT if args.record else None)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if record["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
