#!/usr/bin/env python3
"""Deterministic, prompt-free transition and handoff primitives."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

STATUSES = {"DONE", "DONE_WITH_CONCERNS", "BLOCKED", "NEEDS_CONTEXT"}
PRIVATE_FIELDS = {
    "transcript",
    "chain_of_thought",
    "generated_source",
    "full_diff",
    "raw_tool_output",
    "raw_response",
    "tool_output",
}
HANDOFF_FIELDS = {
    "schema_version", "executor", "run_id", "checkpoint_identity", "current_unit",
    "next_unit", "aggregate_status", "verified_commands", "artifact_paths",
    "unresolved_status", "ownership_boundary",
}
ROOT_HANDOFF_NAME = ".ywc-context-handoff.json"


def _normalize_field(name: str) -> str:
    """Collapse a key to a lowercase alphanumeric token.

    `raw-response`, `rawResponse`, and `RAW_RESPONSE` all normalize to
    `rawresponse`, so separator and casing variants cannot bypass the check.
    """
    return "".join(character for character in name if character.isalnum()).lower()


PRIVATE_FIELD_TOKENS = {_normalize_field(field) for field in PRIVATE_FIELDS}


def resolve_resume_disposition(
    checkpoint_exists: bool,
    saved_scope: str | None,
    current_scope: str,
    disposition: str | None,
) -> dict[str, object]:
    """Resolve resume intent without prompting.

    `saved_scope` / `current_scope` are retained for caller reporting only: an
    existing checkpoint always demands an explicit disposition, so a scope match
    never licenses a silent auto-resume.
    """
    if not checkpoint_exists:
        return {"status": "DONE", "reason": "fresh_run"}
    if disposition not in {"resume", "stop"}:
        return {"status": "NEEDS_CONTEXT", "missing": ["--resume-disposition"]}
    if disposition == "stop":
        return {"status": "DONE_WITH_CONCERNS", "reason": "resume_stopped"}
    return {"status": "DONE", "reason": "resume_accepted"}


def validate_url_profile(settings: dict[str, object] | None) -> dict[str, object]:
    key = ".codex/settings.local.json:ywDevSequentialExecutor.externalSpecUrls"
    if not isinstance(settings, dict):
        return {"status": "NEEDS_CONTEXT", "missing": [key]}
    profile = settings.get("ywDevSequentialExecutor", settings)
    if not isinstance(profile, dict):
        return {"status": "NEEDS_CONTEXT", "missing": [key]}
    policy = profile.get("externalSpecUrls")
    if policy not in {"deny", "allow", "allowlist"}:
        return {"status": "NEEDS_CONTEXT", "missing": [key]}
    if policy == "allowlist":
        origins = profile.get("externalSpecUrlAllowlist")
        if not isinstance(origins, list) or not origins:
            return {"status": "NEEDS_CONTEXT", "missing": [key]}
        for origin in origins:
            try:
                parsed = urlsplit(origin) if isinstance(origin, str) else None
                port = parsed.port if parsed is not None else None
            except ValueError:
                parsed, port = None, None
            canonical = (
                f"https://{parsed.hostname.lower()}" + f":{port}"
                if parsed is not None and parsed.hostname and port
                else f"https://{parsed.hostname.lower()}"
                if parsed is not None and parsed.hostname
                else None
            )
            if (
                parsed is None or parsed.scheme != "https" or not parsed.hostname
                or parsed.path not in {"", "/"} or parsed.query or parsed.fragment
                or parsed.username or parsed.password or port == 443 or origin != canonical
            ):
                return {"status": "NEEDS_CONTEXT", "missing": [key]}
    return {"status": "DONE", "policy": policy}


def _walk(value: object, path: str = "$", seen: set[str] | None = None) -> None:
    if seen is None:
        seen = set()
    if isinstance(value, dict):
        for key, child in value.items():
            # Containment, not equality: an affixed key such as `tool_output_text`
            # carries the same payload as `tool_output` and must not slip through.
            normalized = _normalize_field(key) if isinstance(key, str) else ""
            if any(token in normalized for token in PRIVATE_FIELD_TOKENS):
                raise ValueError(f"privacy field: {path}.{key}")
            if key in seen:
                raise ValueError(f"duplicate field: {path}.{key}")
            if isinstance(child, str) and len(child) > 512:
                raise ValueError(f"bounded field: {path}.{key}")
            _walk(child, f"{path}.{key}", seen | {key})
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk(child, f"{path}[{index}]", seen)


def _validate_handoff(payload: object) -> None:
    if not isinstance(payload, dict) or set(payload) != HANDOFF_FIELDS:
        raise ValueError("closed handoff shape")
    if payload["schema_version"] != 1 or payload["executor"] != "sequential":
        raise ValueError("handoff identity")
    _walk(payload)


def atomic_write_handoff(
    destination: Path, payload: dict[str, object], *, fail_after_write: bool = False
) -> None:
    """Replace only the cache; a failed write leaves the old cache intact."""
    _validate_handoff(payload)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f"{ROOT_HANDOFF_NAME}.tmp.", dir=destination.parent, text=False
    )
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
            dir_fd = os.open(destination.parent, os.O_RDONLY)
        except OSError:
            dir_fd = None
        if dir_fd is not None:
            try:
                try:
                    os.fsync(dir_fd)
                except OSError:
                    # Directory fsync is not available on every supported host;
                    # the file fsync and same-directory rename remain atomic.
                    pass
            finally:
                os.close(dir_fd)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def expected_handoff_path(project_root: Path) -> Path:
    """The single legal handoff location: the authoritative project root's cache."""
    return Path(project_root).resolve() / ROOT_HANDOFF_NAME


def load_handoff(
    destination: Path,
    checkpoint_identity: dict[str, object],
    *,
    project_root: Path,
) -> dict[str, object]:
    """Read the cache only from the authoritative project root.

    A structurally valid handoff written inside a worker worktree is still not
    this run's handoff, so any destination other than the expected root path is
    rejected before its payload is parsed — recovery then falls back to the
    checkpoint and task sources downstream.
    """
    try:
        if Path(destination).resolve() != expected_handoff_path(project_root):
            return {"status": "NEEDS_CONTEXT", "reason": "handoff_reconstruct"}
        payload = json.loads(Path(destination).read_text(encoding="utf-8"))
        _validate_handoff(payload)
    except (OSError, ValueError, json.JSONDecodeError):
        return {"status": "NEEDS_CONTEXT", "reason": "handoff_reconstruct"}
    if payload["checkpoint_identity"] != checkpoint_identity:
        return {"status": "NEEDS_CONTEXT", "reason": "handoff_reconstruct"}
    return {"status": "DONE", "handoff": payload}


def recover_handoff(
    destination: Path,
    checkpoint_identity: dict[str, object],
    readme: Path,
    task: Path,
    *,
    project_root: Path,
) -> dict[str, object]:
    """Use checkpoint first, then task sources; never infer from the cache."""
    loaded = load_handoff(destination, checkpoint_identity, project_root=project_root)
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
