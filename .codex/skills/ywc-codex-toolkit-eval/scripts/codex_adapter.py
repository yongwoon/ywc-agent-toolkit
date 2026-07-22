"""Small, non-secret Codex CLI adapter contract used by the isolated runner."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Protocol
import json
import os
import subprocess


@dataclass(frozen=True)
class RunnerRequest:
    """Inputs to one attempt; paths are fresh, evaluator-owned directories."""
    run_id: str
    workspace: Path
    codex_home: Path
    prompt: str
    target_skill: str
    credential_provider: str
    credential_environment: Mapping[str, str]


@dataclass(frozen=True)
class AdapterResult:
    """A normalized adapter outcome; never contains credential material."""
    status: str  # PASS, FAIL, ERROR, INCONCLUSIVE, or SKIPPED_UNAVAILABLE
    final_output: str = ""
    error: str = ""
    command: tuple[str, ...] = ()
    cli_version: str | None = None


class CodexAdapter(Protocol):
    def run(self, request: RunnerRequest, *, timeout_seconds: int) -> AdapterResult: ...


class FakeAdapter:
    """Deterministic test adapter.  A callback may write only into request.workspace."""
    def __init__(self, callback=None, result: AdapterResult | None = None):
        self.callback = callback
        self.result = result or AdapterResult("PASS", final_output="PASS")
        self.requests: list[RunnerRequest] = []

    def run(self, request: RunnerRequest, *, timeout_seconds: int) -> AdapterResult:
        self.requests.append(request)
        if self.callback:
            self.callback(request)
        return self.result


class CodexCliAdapter:
    """One supported CLI invocation, with a JSON-event and final-text fallback."""
    def run(self, request: RunnerRequest, *, timeout_seconds: int) -> AdapterResult:
        command = ("codex", "exec", "--json", request.prompt)
        environment = {"CODEX_HOME": str(request.codex_home), "PATH": os.environ.get("PATH", ""), **request.credential_environment}
        try:
            version = subprocess.run(("codex", "--version"), capture_output=True, text=True, timeout=10, env=environment).stdout.strip() or None
            proc = subprocess.run(command, cwd=request.workspace, capture_output=True, text=True, timeout=timeout_seconds, env=environment)
        except FileNotFoundError:
            return AdapterResult("SKIPPED_UNAVAILABLE", error="codex CLI unavailable", command=command)
        except subprocess.TimeoutExpired:
            return AdapterResult("ERROR", error="codex CLI timed out", command=command)
        final = ""
        for line in proc.stdout.splitlines():
            try:
                event = json.loads(line)
                if isinstance(event, dict) and isinstance(event.get("final_output"), str):
                    final = event["final_output"]
            except json.JSONDecodeError:
                continue
        if not final:
            final = proc.stdout.strip()  # documented text fallback
        return AdapterResult("PASS" if proc.returncode == 0 else "FAIL", final_output=final, error=proc.stderr.strip(), command=command, cli_version=version)
