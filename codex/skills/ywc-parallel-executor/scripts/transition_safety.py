#!/usr/bin/env python3
"""Prompt-free, checkpoint-first transition primitives for parallel runs."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

STATUSES = {"DONE", "DONE_WITH_CONCERNS", "BLOCKED", "NEEDS_CONTEXT"}
PRIVATE_FIELDS = {
    "transcript", "chain_of_thought", "generated_source", "full_diff",
    "raw_tool_output", "raw_response", "tool_output",
}
HANDOFF_FIELDS = {
    "schema_version", "executor", "run_id", "checkpoint_identity", "current_unit",
    "next_unit", "aggregate_status", "verified_commands", "artifact_paths",
    "unresolved_status", "ownership_boundary",
}
ROOT_HANDOFF_NAME = ".ywc-context-handoff.json"


def aggregate_handoff_path(run_root: Path, root_kind: str) -> Path | None:
    """Return the sole root destination; workers have no handoff authority."""
    if root_kind != "root":
        return None
    return Path(run_root) / ROOT_HANDOFF_NAME


def terminal_status(reason: str) -> dict[str, object]:
    if reason == "branch_conflict":
        return {"status": "BLOCKED", "reason": reason}
    if reason == "ci_timeout":
        return {"status": "DONE_WITH_CONCERNS", "reason": reason}
    if reason == "missing_resume":
        return {"status": "NEEDS_CONTEXT", "missing": ["--resume-disposition"]}
    if reason not in {"resume_stopped", "url_policy", "worktree_missing"}:
        return {"status": "BLOCKED", "reason": "transition_failed"}
    return {"status": "DONE_WITH_CONCERNS", "reason": reason}


def resolve_resume_disposition(
    checkpoint_exists: bool,
    saved_scope: str | None,
    current_scope: str,
    disposition: str | None,
) -> dict[str, object]:
    if not checkpoint_exists:
        return {"status": "DONE", "reason": "fresh_run"}
    # An existing checkpoint always demands an explicit disposition; `None` never
    # silently resumes, regardless of whether the saved scope matches the current one.
    if disposition not in {"resume", "stop"}:
        return terminal_status("missing_resume")
    if disposition == "stop":
        return terminal_status("resume_stopped")
    return {"status": "DONE", "reason": "resume_accepted"}


def _walk(value: object, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValueError("non-string property")
            if key.lower() in PRIVATE_FIELDS:
                raise ValueError(f"privacy field: {path}.{key}")
            if isinstance(child, str) and len(child) > 512:
                raise ValueError(f"bounded field: {path}.{key}")
            _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk(child, f"{path}[{index}]")


def _exact(value: object, keys: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"closed {label} shape")
    return value


def _validate_handoff(payload: object) -> None:
    root = _exact(payload, HANDOFF_FIELDS, "handoff")
    if root["schema_version"] != 1 or root["executor"] != "parallel":
        raise ValueError("handoff identity")
    identity = _exact(root["checkpoint_identity"], {
        "run_id", "unit_id", "checkpoint_timestamp", "base_sha", "feature_sha", "worker_shas"
    }, "checkpoint_identity")
    if identity["run_id"] != root["run_id"] or identity["feature_sha"] is not None:
        raise ValueError("parallel checkpoint identity")
    if not isinstance(identity["worker_shas"], list) or not identity["worker_shas"]:
        raise ValueError("parallel worker identity")
    worker_ids = []
    for worker in identity["worker_shas"]:
        worker = _exact(worker, {"worker_id", "sha"}, "worker_sha")
        worker_ids.append(worker["worker_id"])
    if not all(isinstance(worker_id, str) for worker_id in worker_ids):
        raise ValueError("parallel worker identity type")
    if worker_ids != sorted(set(worker_ids)):
        raise ValueError("parallel worker ordering")
    current = _exact(root["current_unit"], {"id", "kind", "status"}, "current_unit")
    next_unit = _exact(root["next_unit"], {"id", "kind"}, "next_unit")
    aggregate = _exact(root["aggregate_status"], {"status", "reason"}, "aggregate_status")
    unresolved = _exact(root["unresolved_status"], {"status", "items"}, "unresolved_status")
    boundary = _exact(root["ownership_boundary"], {"scope", "writable_paths", "authority"}, "ownership_boundary")
    if not isinstance(root["verified_commands"], list) or not isinstance(root["artifact_paths"], list):
        raise ValueError("handoff arrays")
    if not isinstance(unresolved["items"], list) or not isinstance(boundary["writable_paths"], list):
        raise ValueError("handoff nested arrays")
    if current["kind"] not in {"task", "wave"} or current["status"] not in {"pending", "in_progress", "completed", "blocked"}:
        raise ValueError("current unit values")
    if next_unit["kind"] not in {"task", "wave"} or aggregate["status"] not in STATUSES:
        raise ValueError("handoff status values")
    if unresolved["status"] not in {"none", "open", "blocked"}:
        raise ValueError("unresolved status")
    if unresolved["status"] == "none" and unresolved["items"]:
        raise ValueError("unresolved items")
    for item in root["verified_commands"]:
        _exact(item, {"id", "status"}, "verified_command")
        if item["status"] not in {"pass", "fail"}:
            raise ValueError("verified command status")
    if not all(isinstance(path, str) and path and len(path) <= 4096 for path in root["artifact_paths"]):
        raise ValueError("artifact path")
    if root["ownership_boundary"]["authority"] != "cache_only":
        raise ValueError("handoff authority")
    _walk(root)


def atomic_write_handoff(
    destination: Path,
    payload: dict[str, object],
    *,
    run_root: Path,
    fail_after_write: bool = False,
) -> None:
    """Atomically replace only the root aggregate cache."""
    destination = Path(destination)
    # `run_root` is mandatory: the sole legal destination is the root aggregate path,
    # so a worker cannot claim write authority by omitting the root context.
    if destination != aggregate_handoff_path(run_root, "root"):
        raise ValueError("parallel workers cannot write handoff")
    _validate_handoff(payload)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f"{ROOT_HANDOFF_NAME}.tmp.", dir=destination.parent)
    temporary_path = Path(temporary)
    try:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        with os.fdopen(fd, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        if fail_after_write:
            raise OSError("injected handoff write failure")
        os.replace(temporary_path, destination)
        try:
            directory = os.open(destination.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        except OSError:
            pass
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def load_handoff(destination: Path, checkpoint_identity: dict[str, object]) -> dict[str, object]:
    try:
        payload = json.loads(Path(destination).read_text(encoding="utf-8"))
        _validate_handoff(payload)
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return {"status": "NEEDS_CONTEXT", "reason": "handoff_reconstruct"}
    if payload["checkpoint_identity"] != checkpoint_identity:
        return {"status": "NEEDS_CONTEXT", "reason": "handoff_reconstruct"}
    return {"status": "DONE", "handoff": payload}


def recover_handoff(
    destination: Path,
    checkpoint_identity: dict[str, object],
    readme: Path,
    task: Path,
) -> dict[str, object]:
    loaded = load_handoff(destination, checkpoint_identity)
    if loaded["status"] == "DONE":
        return loaded
    sources = [path for path in (readme, task) if Path(path).is_file()]
    if not sources:
        return {"status": "NEEDS_CONTEXT", "reason": "handoff_reconstruct"}
    return {
        "status": "DONE_WITH_CONCERNS",
        "reason": "handoff_reconstructed",
        "sources": ["checkpoint"] + [path.name for path in sources],
    }
