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


def test_missing_disposition_never_auto_resumes_on_matching_scope():
    missing = {"status": "NEEDS_CONTEXT", "missing": ["--resume-disposition"]}
    assert resolve_resume_disposition(True, "task-a", "task-a", None) == missing
    assert resolve_resume_disposition(True, None, "task-a", None) == missing
    assert resolve_resume_disposition(True, "task-a", "task-a", "bogus") == missing
    assert resolve_resume_disposition(True, "task-a", "task-a", "resume") == {
        "status": "DONE",
        "reason": "resume_accepted",
    }
    assert resolve_resume_disposition(False, None, "task-a", None) == {
        "status": "DONE",
        "reason": "fresh_run",
    }


def test_stop_disposition_preserves_checkpoint():
    result = resolve_resume_disposition(True, "task-a", "task-a", "stop")
    assert result == {"status": "DONE_WITH_CONCERNS", "reason": "resume_stopped"}


def test_url_profile_requires_existing_canonical_policy():
    assert validate_url_profile(None)["status"] == "NEEDS_CONTEXT"
    assert validate_url_profile({"ywDevSequentialExecutor": {"externalSpecUrls": "allowlist"}})["status"] == "NEEDS_CONTEXT"
    assert validate_url_profile(
        {"ywDevSequentialExecutor": {"externalSpecUrls": "allowlist", "externalSpecUrlAllowlist": ["https://example.com"]}}
    ) == {"status": "DONE", "policy": "allowlist"}


def valid_payload():
    checkpoint = {"run_id": "run-1", "unit_id": "task-a", "checkpoint_timestamp": "t"}
    return checkpoint, {
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


def test_handoff_rejects_stale_and_private_payloads_and_preserves_old_file():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        destination = root / ".ywc-context-handoff.json"
        checkpoint, valid = valid_payload()
        atomic_write_handoff(destination, valid)
        original = destination.read_bytes()
        assert load_handoff(destination, checkpoint, project_root=root)["status"] == "DONE"
        stale_checkpoint = dict(checkpoint, unit_id="task-b")
        assert load_handoff(destination, stale_checkpoint, project_root=root)["status"] == "NEEDS_CONTEXT"
        private = dict(valid, transcript="forbidden")
        try:
            atomic_write_handoff(destination, private)
        except ValueError:
            pass
        else:
            raise AssertionError("private handoff field was accepted")
        assert destination.read_bytes() == original
        try:
            atomic_write_handoff(destination, valid, fail_after_write=True)
        except OSError:
            pass
        else:
            raise AssertionError("failure injection did not fail")
        assert destination.read_bytes() == original


def test_nested_private_key_variants_are_rejected():
    _, valid = valid_payload()
    variants = [
        "raw-response",
        "rawResponse",
        "RAW_RESPONSE",
        "raw response",
        "tool_output_text",
        "ChainOfThought",
        "full-diff",
    ]
    with tempfile.TemporaryDirectory() as raw:
        destination = Path(raw) / ".ywc-context-handoff.json"
        for variant in variants:
            payload = dict(
                valid,
                current_unit=dict(valid["current_unit"], nested={variant: "forbidden"}),
            )
            try:
                atomic_write_handoff(destination, payload)
            except ValueError as error:
                assert "privacy field" in str(error), (variant, str(error))
            else:
                raise AssertionError(f"nested private variant accepted: {variant}")
        assert not destination.exists()


def test_valid_nested_keys_are_still_accepted():
    _, valid = valid_payload()
    payload = dict(
        valid,
        current_unit=dict(valid["current_unit"], nested={"summary": "ok", "toolName": "pytest"}),
    )
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        destination = root / ".ywc-context-handoff.json"
        atomic_write_handoff(destination, payload)
        assert load_handoff(destination, valid["checkpoint_identity"], project_root=root)["status"] == "DONE"


def test_handoff_outside_project_root_is_never_trusted():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        worker = root / "worker-a"
        worker.mkdir()
        checkpoint, valid = valid_payload()
        worker_destination = worker / ".ywc-context-handoff.json"
        atomic_write_handoff(worker_destination, valid)
        # Structurally valid, identity-matching, but not this project root's handoff.
        assert load_handoff(worker_destination, checkpoint, project_root=root) == {
            "status": "NEEDS_CONTEXT",
            "reason": "handoff_reconstruct",
        }
        # A non-canonical filename under the root is rejected the same way.
        alias = root / "other-handoff.json"
        alias.write_text(worker_destination.read_text(encoding="utf-8"), encoding="utf-8")
        assert load_handoff(alias, checkpoint, project_root=root)["status"] == "NEEDS_CONTEXT"
        # The worker's own root still loads its own file, so the gate is scoped, not global.
        assert load_handoff(worker_destination, checkpoint, project_root=worker)["status"] == "DONE"


def test_handoff_recovery_uses_checkpoint_then_task_sources():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        checkpoint, _ = valid_payload()
        result = load_handoff(root / ".ywc-context-handoff.json", checkpoint, project_root=root)
        assert result["status"] == "NEEDS_CONTEXT"
        (root / "README.md").write_text("task source\n", encoding="utf-8")
        from transition_safety import recover_handoff

        recovered = recover_handoff(
            root / ".ywc-context-handoff.json",
            checkpoint,
            root / "README.md",
            root / "task.md",
            project_root=root,
        )
        assert recovered == {"status": "DONE_WITH_CONCERNS", "reason": "handoff_reconstructed", "sources": ["checkpoint", "README.md"]}


if __name__ == "__main__":
    for name, value in sorted(globals().items()):
        if name.startswith("test_"):
            value()
    print("PASS: transition safety fixtures")
