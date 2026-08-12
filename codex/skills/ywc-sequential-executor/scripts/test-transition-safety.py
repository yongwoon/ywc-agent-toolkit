#!/usr/bin/env python3
"""RED-first contract fixtures for sequential transition safety."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from transition_safety import (
    atomic_write_handoff,
    load_handoff,
    resolve_resume_disposition,
    validate_url_profile,
)


def test_resume_scope_requires_disposition_without_prompt():
    result = resolve_resume_disposition(
        checkpoint_exists=True,
        saved_scope="task-a",
        current_scope="task-b",
        disposition=None,
    )
    assert result == {"status": "NEEDS_CONTEXT", "missing": ["--resume-disposition"]}


def test_stop_disposition_preserves_checkpoint():
    result = resolve_resume_disposition(True, "task-a", "task-a", "stop")
    assert result == {"status": "DONE_WITH_CONCERNS", "reason": "resume_stopped"}


def test_url_profile_requires_existing_canonical_policy():
    assert validate_url_profile(None)["status"] == "NEEDS_CONTEXT"
    assert validate_url_profile({"ywDevSequentialExecutor": {"externalSpecUrls": "allowlist"}})["status"] == "NEEDS_CONTEXT"
    assert validate_url_profile(
        {"ywDevSequentialExecutor": {"externalSpecUrls": "allowlist", "externalSpecUrlAllowlist": ["https://example.com"]}}
    ) == {"status": "DONE", "policy": "allowlist"}


def test_handoff_rejects_stale_and_private_payloads_and_preserves_old_file():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        destination = root / ".ywc-context-handoff.json"
        checkpoint = {"run_id": "run-1", "unit_id": "task-a", "checkpoint_timestamp": "t"}
        valid = {
            "schema_version": 1,
            "executor": "sequential",
            "run_id": "run-1",
            "checkpoint_identity": checkpoint,
            "current_unit": {"id": "task-a", "kind": "task", "status": "in_progress"},
            "next_unit": {"id": "", "kind": "task"},
            "aggregate_status": {"status": "DONE", "reason": "validated"},
            "verified_commands": [],
            "artifact_paths": [],
            "unresolved_status": {"status": "none", "items": []},
            "ownership_boundary": {"scope": "sequential", "writable_paths": [], "authority": "cache_only"},
        }
        atomic_write_handoff(destination, valid)
        assert load_handoff(destination, checkpoint)["status"] == "DONE"
        stale_checkpoint = dict(checkpoint, unit_id="task-b")
        assert load_handoff(destination, stale_checkpoint)["status"] == "NEEDS_CONTEXT"
        private = dict(valid, transcript="forbidden")
        try:
            atomic_write_handoff(destination, private)
        except ValueError:
            pass
        else:
            raise AssertionError("private handoff field was accepted")
        try:
            atomic_write_handoff(destination, valid, fail_after_write=True)
        except OSError:
            pass
        else:
            raise AssertionError("failure injection did not fail")
        assert json.loads(destination.read_text())["run_id"] == "run-1"


def test_handoff_recovery_uses_checkpoint_then_task_sources():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        checkpoint = {"run_id": "run-1", "unit_id": "task-a", "checkpoint_timestamp": "t"}
        result = load_handoff(root / ".ywc-context-handoff.json", checkpoint)
        assert result["status"] == "NEEDS_CONTEXT"
        (root / "README.md").write_text("task source\n", encoding="utf-8")
        from transition_safety import recover_handoff

        recovered = recover_handoff(root / ".ywc-context-handoff.json", checkpoint, root / "README.md", root / "task.md")
        assert recovered == {"status": "DONE_WITH_CONCERNS", "reason": "handoff_reconstructed", "sources": ["checkpoint", "README.md"]}


if __name__ == "__main__":
    for name, value in sorted(globals().items()):
        if name.startswith("test_"):
            value()
    print("PASS: transition safety fixtures")
