#!/usr/bin/env python3
"""RED-first contract fixtures for parallel transition safety."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from transition_safety import (
    aggregate_handoff_path,
    atomic_write_handoff,
    load_handoff,
    recover_handoff,
    resolve_resume_disposition,
    terminal_status,
)


def valid_payload():
    checkpoint = {
        "run_id": "run-1",
        "unit_id": "wave-1",
        "checkpoint_timestamp": "2026-08-12T01:02:03Z",
        "base_sha": "0123456789abcdef0123456789abcdef01234567",
        "feature_sha": None,
        "worker_shas": [
            {"worker_id": "task-a", "sha": "89abcdef0123456789abcdef0123456789abcdef"}
        ],
    }
    return checkpoint, {
        "schema_version": 1,
        "executor": "parallel",
        "run_id": "run-1",
        "checkpoint_identity": checkpoint,
        "current_unit": {"id": "wave-1", "kind": "wave", "status": "in_progress"},
        "next_unit": {"id": "wave-2", "kind": "wave"},
        "aggregate_status": {"status": "DONE", "reason": "validated"},
        "verified_commands": [],
        "artifact_paths": [],
        "unresolved_status": {"status": "none", "items": []},
        "ownership_boundary": {
            "scope": "parallel-aggregate",
            "writable_paths": [],
            "authority": "cache_only",
        },
    }


def test_parallel_uses_one_root_aggregate_and_rejects_worker_destination():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        assert aggregate_handoff_path(root, "root") == root / ".ywc-context-handoff.json"
        assert aggregate_handoff_path(root / "worker-a", "worker") is None
        _, payload = valid_payload()
        try:
            atomic_write_handoff(root / "worker-a" / ".ywc-context-handoff.json", payload, run_root=root)
        except ValueError:
            pass
        else:
            raise AssertionError("worker handoff destination was accepted")
        try:
            atomic_write_handoff(root / "nested" / ".ywc-context-handoff.json", payload, run_root=root)
        except ValueError:
            pass
        else:
            raise AssertionError("non-canonical root destination was accepted")
        try:
            atomic_write_handoff(root / "worker-a" / ".ywc-context-handoff.json", payload)
        except TypeError:
            pass
        else:
            raise AssertionError("run_root was optional for handoff write")


def test_prompt_branches_close_with_bounded_statuses():
    assert terminal_status("branch_conflict") == {"status": "BLOCKED", "reason": "branch_conflict"}
    assert terminal_status("ci_timeout") == {"status": "DONE_WITH_CONCERNS", "reason": "ci_timeout"}
    assert terminal_status("missing_resume") == {"status": "NEEDS_CONTEXT", "missing": ["--resume-disposition"]}


def test_resume_never_prompts_and_stop_preserves_checkpoint():
    assert resolve_resume_disposition(True, "wave-1", "wave-2", None) == {
        "status": "NEEDS_CONTEXT",
        "missing": ["--resume-disposition"],
    }
    assert resolve_resume_disposition(True, "wave-1", "wave-1", None) == {
        "status": "NEEDS_CONTEXT",
        "missing": ["--resume-disposition"],
    }
    assert resolve_resume_disposition(True, "wave-1", "wave-1", "bogus") == {
        "status": "NEEDS_CONTEXT",
        "missing": ["--resume-disposition"],
    }
    assert resolve_resume_disposition(True, "wave-1", "wave-1", "stop") == {
        "status": "DONE_WITH_CONCERNS",
        "reason": "resume_stopped",
    }
    assert resolve_resume_disposition(True, "wave-1", "wave-1", "resume") == {
        "status": "DONE",
        "reason": "resume_accepted",
    }
    assert resolve_resume_disposition(False, None, "wave-1", None) == {
        "status": "DONE",
        "reason": "fresh_run",
    }


def test_malformed_stale_private_and_failed_handoff_reconstruct_without_replacing_state():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        destination = aggregate_handoff_path(root, "root")
        checkpoint, valid = valid_payload()
        atomic_write_handoff(destination, valid, run_root=root)
        assert load_handoff(destination, checkpoint)["status"] == "DONE"
        assert load_handoff(destination, dict(checkpoint, unit_id="wave-2"))["status"] == "NEEDS_CONTEXT"
        try:
            atomic_write_handoff(destination, dict(valid, transcript="forbidden"), run_root=root)
        except ValueError:
            pass
        else:
            raise AssertionError("private handoff field was accepted")
        try:
            atomic_write_handoff(destination, valid, run_root=root, fail_after_write=True)
        except OSError:
            pass
        else:
            raise AssertionError("failure injection did not fail")
        assert json.loads(destination.read_text())["run_id"] == "run-1"


def test_mixed_type_worker_ids_do_not_crash_the_reader():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        destination = aggregate_handoff_path(root, "root")
        checkpoint, valid = valid_payload()
        corrupted_identity = dict(
            checkpoint,
            worker_shas=[
                {"worker_id": 1, "sha": "89abcdef0123456789abcdef0123456789abcdef"},
                {"worker_id": "task-a", "sha": "0123456789abcdef0123456789abcdef01234567"},
            ],
        )
        corrupted = dict(valid, checkpoint_identity=corrupted_identity)
        destination.write_text(json.dumps(corrupted), encoding="utf-8")
        assert load_handoff(destination, checkpoint) == {
            "status": "NEEDS_CONTEXT",
            "reason": "handoff_reconstruct",
        }


def test_invalid_cache_reconstructs_from_checkpoint_then_current_sources():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        checkpoint, _ = valid_payload()
        (root / "README.md").write_text("current run source\n", encoding="utf-8")
        (root / "task.md").write_text("current task source\n", encoding="utf-8")
        result = recover_handoff(root / ".ywc-context-handoff.json", checkpoint, root / "README.md", root / "task.md")
        assert result == {
            "status": "DONE_WITH_CONCERNS",
            "reason": "handoff_reconstructed",
            "sources": ["checkpoint", "README.md", "task.md"],
        }


if __name__ == "__main__":
    for name, value in sorted(globals().items()):
        if name.startswith("test_"):
            value()
    print("PASS: parallel transition safety fixtures")
