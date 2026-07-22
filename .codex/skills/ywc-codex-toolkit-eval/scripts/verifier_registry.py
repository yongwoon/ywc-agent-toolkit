"""Fixed, evaluator-owned deterministic verifier definitions.

Fixtures name entries from this module; they never supply a command, executable,
working directory, environment, or timeout.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class VerifierMode(str, Enum):
    FIXTURE_WORKSPACE = "fixture_workspace"
    SOURCE_CHECKOUT_READONLY = "source_checkout_readonly"


@dataclass(frozen=True)
class VerifierEntry:
    verifier_id: str
    mode: VerifierMode
    argv: tuple[str, ...]
    cwd: str
    timeout_seconds: int
    allowed_environment: tuple[str, ...]
    expected_exit_status: int
    output_regex: str | None = None
    readonly_roots: tuple[str, ...] = ()


VERIFIER_REGISTRY: dict[str, VerifierEntry] = {
    "bundle.validate": VerifierEntry(
        verifier_id="bundle.validate",
        mode=VerifierMode.SOURCE_CHECKOUT_READONLY,
        argv=("bash", "scripts/validate.sh"),
        cwd=".",
        timeout_seconds=300,
        allowed_environment=(),
        expected_exit_status=0,
        readonly_roots=("codex", "claude-code", "scripts", "plugins"),
    ),
}


def get_verifier(verifier_id: str) -> VerifierEntry:
    try:
        return VERIFIER_REGISTRY[verifier_id]
    except KeyError as exc:
        raise KeyError(f"unknown verifier: {verifier_id}") from exc
