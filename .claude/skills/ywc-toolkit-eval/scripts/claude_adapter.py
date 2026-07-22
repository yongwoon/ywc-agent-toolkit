#!/usr/bin/env python3
"""Dispatch adapter for the Claude Code CLI, plus a fake for tests.

Route N1 (spec Iteration 4) fixed the execution contract: the with-arm is

    claude -p "/<skill> <prompt>" --output-format json

run with the workspace as cwd, authenticated by the developer's existing
subscription session. There is no temporary config dir and no API key —
`--bare` and `CLAUDE_CONFIG_DIR` were both excluded because they sever OAuth.

The json payload carries no activation signal; the spike verified this. So the
adapter returns the outcome only, and the runner records
`activation_observability: "unavailable"` rather than pretending to know
whether the skill fired.

`FakeAdapter` exists so the whole test suite runs with no CLI installed and
spends nothing. At ~$0.54 per real dispatch, a suite that dispatched for real
would cost more than the code it guards.

Stdlib only (`subprocess` + `json`), matching score.py's no-dependency convention.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

DEFAULT_TIMEOUT_SECONDS = 300

# The CLI binary is a constant, never assembled from case data — the same
# rule verifier_registry.py enforces for verifier argv.
CLAUDE_BIN = "claude"


class AdapterUnavailable(RuntimeError):
    """Raised when the `claude` CLI is not installed or not on PATH."""


class AdapterTimeout(RuntimeError):
    """Raised when a dispatch exceeds its timeout."""


def build_argv(skill: str, prompt: str, disable_skills: bool = False) -> list[str]:
    """Build the dispatch argv for one arm of a trial.

    The with-arm sends the explicit `/name prompt` form, which is what
    guarantees the target skill actually runs. The without-arm sends the bare
    prompt plus `--disable-slash-commands`: that flag turns every skill off, so
    a `/name` string there would just be unresolvable text and the comparison
    would measure nothing.

    Returned as a list so `subprocess` never sees a shell string — the prompt
    is one argv element and needs no quoting or escaping.
    """
    invocation = prompt if disable_skills else f"/{skill} {prompt}"
    argv = [CLAUDE_BIN, "-p", invocation, "--output-format", "json"]
    if disable_skills:
        argv.append("--disable-slash-commands")
    return argv


def is_available() -> bool:
    """True when the `claude` CLI can be found on PATH."""
    return shutil.which(CLAUDE_BIN) is not None


def dispatch(skill: str, prompt: str, cwd: Path | str,
             disable_skills: bool = False,
             timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict:
    """Run one dispatch in `cwd` and return `{"is_error": bool, "result": str}`.

    `cwd` is the runner-owned workspace, which is what keeps a file-writing
    skill from touching the real repository.
    """
    if not is_available():
        raise AdapterUnavailable(
            f"{CLAUDE_BIN!r} is not on PATH; install the CLI or use FakeAdapter")

    argv = build_argv(skill, prompt, disable_skills=disable_skills)
    try:
        completed = subprocess.run(  # noqa: S603 — argv list, never shell=True
            argv, cwd=str(cwd), capture_output=True, text=True,
            timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise AdapterTimeout(f"dispatch exceeded {timeout}s") from exc

    return _parse_payload(completed.stdout, completed.returncode, completed.stderr)


def _parse_payload(stdout: str, returncode: int, stderr: str) -> dict:
    """Normalize the CLI's json output into the adapter's two-field contract.

    A non-zero exit or unparseable stdout is an error result rather than an
    exception: the runner needs to record it as `ERROR` alongside the other
    statuses, not crash the whole suite on one bad case.
    """
    if returncode != 0 and not stdout.strip():
        return {"is_error": True, "result": (stderr or "").strip()[:2000]}
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return {"is_error": True,
                "result": f"unparseable adapter output: {stdout.strip()[:500]}"}

    if not isinstance(payload, dict):
        return {"is_error": True,
                "result": f"unexpected payload type {type(payload).__name__}"}

    return {
        "is_error": bool(payload.get("is_error", returncode != 0)),
        "result": str(payload.get("result", "")),
    }


class FakeAdapter:
    """A scripted adapter for tests — no CLI, no network, no cost.

    `writes` maps workspace-relative paths to content, letting a test simulate
    a dispatch that touches the filesystem (declared or otherwise) so the
    runner's snapshot comparison has something real to catch.
    """

    def __init__(self, result: str = "", is_error: bool = False,
                 unavailable: bool = False, timeout: bool = False,
                 writes: dict[str, str] | None = None) -> None:
        self.result = result
        self.is_error = is_error
        self.unavailable = unavailable
        self.timeout = timeout
        self.writes = writes or {}
        self.calls: list[dict] = []

    def dispatch(self, skill: str, prompt: str, cwd: Path | str,
                 disable_skills: bool = False,
                 timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict:
        self.calls.append({"skill": skill, "prompt": prompt,
                           "disable_skills": disable_skills})
        if self.unavailable:
            raise AdapterUnavailable("fake adapter configured as unavailable")

        # Writes land before the timeout is raised on purpose: a real dispatch
        # that hangs may already have written, and cleanup must handle that.
        root = Path(cwd)
        for relative, content in self.writes.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

        if self.timeout:
            raise AdapterTimeout("fake adapter configured to time out")
        return {"is_error": self.is_error, "result": self.result}
