#!/usr/bin/env python3
"""Small, offline-safe primitives used by the evaluator CI workflow."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from results import MAX_ARTIFACT_BYTES, ArtifactStore, redact

STATUS_EXITS = {"PASS": 0, "FAIL": 1, "ERROR": 2, "SKIPPED_UNAVAILABLE": 3}
SENSITIVE_PATH_PARTS = ("credential", "secret", "token", "password", "environment", "transcript")


def status_exit(status: str, *, suite: str, manual_ablation: bool = False) -> int:
    """Map evaluator status to the documented CI exit contract."""
    if status == "INCONCLUSIVE" and suite == "ablation" and manual_ablation:
        return 0
    if status == "INCONCLUSIVE":
        return 2
    try:
        return STATUS_EXITS[status]
    except KeyError as exc:
        raise ValueError(f"unsupported evaluator status: {status}") from exc


def live_available(environment: dict[str, str]) -> bool:
    """Live runs require both an explicit handoff and explicit egress approval."""
    return environment.get("EVAL_CREDENTIAL_PROVIDER") == "configured" and environment.get("EVAL_API_EGRESS_POLICY") == "allow"


def check_upload_root(root: Path) -> None:
    """Reject unbounded or sensitive artifact paths before any upload occurs."""
    root = Path(root)
    if not root.is_dir():
        raise ValueError("evaluator artifact root does not exist")
    total = 0
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("artifact upload does not permit symlinks")
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(marker in part.lower() for part in relative.parts for marker in SENSITIVE_PATH_PARTS):
            raise ValueError(f"sensitive artifact path is not uploadable: {relative}")
        total += path.stat().st_size
        if total > MAX_ARTIFACT_BYTES:
            raise ValueError("evaluator artifacts exceed 10 MB cap")
        try:
            contents = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            # The report contract is text-only. Rejecting opaque binary data is
            # safer than uploading bytes that cannot be scanned for secrets.
            raise ValueError(f"non-text artifact is not uploadable: {relative}") from exc
        if redact(contents) != contents:
            raise ValueError(f"secret-like artifact content is not uploadable: {relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status")
    parser.add_argument("--suite", choices=("mocked", "live", "ablation"), default="mocked")
    parser.add_argument("--manual-ablation", action="store_true")
    parser.add_argument("--check-upload-root", type=Path)
    parser.add_argument("--cleanup-root", type=Path)
    args = parser.parse_args()
    if args.check_upload_root:
        check_upload_root(args.check_upload_root)
    if args.cleanup_root:
        print(json.dumps({"removed": ArtifactStore(args.cleanup_root).prune_expired()}, sort_keys=True))
    if args.status:
        return status_exit(args.status, suite=args.suite, manual_ablation=args.manual_ablation)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
