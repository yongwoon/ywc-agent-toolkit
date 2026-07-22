#!/usr/bin/env python3
"""Bounded, redacted evaluator result records and per-run artifact storage."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

VALID_STATUSES = {"PASS", "FAIL", "SKIPPED_UNAVAILABLE", "ERROR", "INCONCLUSIVE"}
_SENSITIVE_KEY = re.compile(r"(?:credential|secret|token|password|api[_-]?key|environment|transcript)", re.I)
_SENSITIVE_VALUE = re.compile(r"((?:api[_-]?key|token|password|secret)\s*[=:]\s*)[^\s,;]+", re.I)
MAX_ARTIFACT_BYTES = 10 * 1024 * 1024
RETENTION_SECONDS = 7 * 24 * 60 * 60


def redact(value: Any) -> Any:
    """Remove sensitive fields and mask recognizable secret assignments."""
    if isinstance(value, dict):
        return {str(key): redact(item) for key, item in value.items() if not _SENSITIVE_KEY.search(str(key))}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return _SENSITIVE_VALUE.sub(r"\1[REDACTED]", value)
    return value


@dataclass(frozen=True)
class ResultRecord:
    run_id: str
    status: str
    profile: str
    case_id: str
    attempt: int
    duration_seconds: float
    cli_version: str | None
    cli_arguments: tuple[str, ...]
    target_skill: str
    dependencies: tuple[str, ...]
    deterministic_verdict: str | None = None
    judge_verdict: str | None = None
    activation_observability: str = "unavailable"

    @classmethod
    def from_runner_result(cls, result: dict[str, Any], *, profile: str, case_id: str,
                           attempt: int, duration_seconds: float, target_skill: str,
                           dependencies: Iterable[str], activation_signal: bool | None = None) -> "ResultRecord":
        status = result.get("status")
        if status not in VALID_STATUSES:
            raise ValueError("status must be one of the evaluator status values")
        run_id = result.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            raise ValueError("run_id is required")
        command = result.get("command", ())
        if not isinstance(command, (list, tuple)) or not all(isinstance(item, str) for item in command):
            raise ValueError("command must be a string array")
        return cls(run_id, status, profile, case_id, attempt, duration_seconds,
                   result.get("cli_version"), tuple(command), target_skill, tuple(dependencies),
                   result.get("deterministic_verdict"), result.get("judge_verdict"),
                   "available" if activation_signal is not None else "unavailable")

    @property
    def is_quality_pass(self) -> bool:
        return self.status == "PASS"

    @property
    def updates_baseline(self) -> bool:
        return self.status not in {"SKIPPED_UNAVAILABLE", "ERROR"}

    def to_dict(self) -> dict[str, Any]:
        return redact({"run_id": self.run_id, "status": self.status, "profile": self.profile,
            "case_id": self.case_id, "attempt": self.attempt, "duration_seconds": self.duration_seconds,
            "cli_version": self.cli_version, "cli_arguments": list(self.cli_arguments),
            "target_skill": self.target_skill, "dependencies": list(self.dependencies),
            "deterministic_verdict": self.deterministic_verdict, "judge_verdict": self.judge_verdict,
            "activation_observability": self.activation_observability,
            "quality_pass": self.is_quality_pass, "baseline_eligible": self.updates_baseline})


class ArtifactStore:
    """Owns one run directory per run ID; never appends to shared summaries."""
    def __init__(self, root: Path, *, max_artifact_bytes: int = MAX_ARTIFACT_BYTES,
                 retention_seconds: int = RETENTION_SECONDS):
        self.root = Path(root)
        self.max_artifact_bytes = max_artifact_bytes
        self.retention_seconds = retention_seconds

    def _run_dir(self, run_id: str) -> Path:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", run_id):
            raise ValueError("unsafe run_id")
        return self.root / run_id

    @staticmethod
    def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as output:
            json.dump(redact(payload), output, sort_keys=True, indent=2)
            output.write("\n")
            temporary = Path(output.name)
        os.replace(temporary, path)

    def write_result(self, record: ResultRecord, report: dict[str, Any] | None = None) -> Path:
        run_dir = self._run_dir(record.run_id)
        summary = run_dir / "summary.json"
        if summary.exists():
            raise ValueError(f"duplicate run ID: {record.run_id}")
        # mkdir is the duplicate-run guard; a competing writer cannot overwrite.
        try:
            run_dir.mkdir(parents=True, exist_ok=False)
        except FileExistsError as exc:
            raise ValueError(f"duplicate run ID: {record.run_id}") from exc
        payload = record.to_dict()
        if report is not None:
            payload["report"] = redact(report)
        self._atomic_json(summary, payload)
        return summary

    def retain_failed_workspace(self, run_id: str, workspace: Path, *, retain: bool) -> Path | None:
        if not retain:
            return None
        source = Path(workspace)
        if not source.is_dir():
            raise ValueError("failed workspace must be a directory")
        files = [path for path in source.rglob("*") if path.is_file() and not path.is_symlink()]
        total = sum(path.stat().st_size for path in files)
        if total > self.max_artifact_bytes:
            raise ValueError("failed artifact exceeds configured cap")
        target = self._run_dir(run_id) / "failed-workspace"
        if target.exists():
            raise ValueError(f"duplicate retained artifact: {run_id}")
        for path in files:
            relative = path.relative_to(source)
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            data = path.read_bytes()
            try:
                destination.write_text(redact(data.decode("utf-8")), encoding="utf-8")
            except UnicodeDecodeError:
                destination.write_bytes(data)
        return target

    def prune_expired(self, *, now: float | None = None) -> list[str]:
        """Remove only expired failed runs owned by this artifact root.

        A malformed or incomplete run directory is intentionally retained: cleanup
        must never turn an investigation artifact into data loss.
        """
        current = time.time() if now is None else now
        if not self.root.exists():
            return []
        removed: list[str] = []
        for run_dir in sorted(path for path in self.root.iterdir() if path.is_dir()):
            summary = run_dir / "summary.json"
            try:
                status = json.loads(summary.read_text(encoding="utf-8")).get("status")
            except (OSError, json.JSONDecodeError):
                continue
            if status in {"FAIL", "ERROR"} and current - run_dir.stat().st_mtime > self.retention_seconds:
                shutil.rmtree(run_dir)
                removed.append(run_dir.name)
        return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        assert ResultRecord.from_runner_result({"run_id": "self-test", "status": "PASS"}, profile="self-test", case_id="self-test", attempt=1, duration_seconds=0, target_skill="self-test", dependencies=[]).is_quality_pass
        print("results self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
