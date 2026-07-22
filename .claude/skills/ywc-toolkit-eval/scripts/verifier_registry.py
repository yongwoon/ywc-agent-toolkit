#!/usr/bin/env python3
"""Evaluator-owned registry of runnable verifiers.

A fixture may name a verifier by id and nothing else. The argv, working
directory, timeout, environment allowlist, and expected exit code all live
here, in evaluator-owned code that a human reviews — never in fixture data.

That asymmetry is the whole security model (spec AC4). If a fixture could
supply a command string, an interpreter path, or even an argv fragment, then
running the evaluation suite would be arbitrary code execution on the
developer's machine. Resolution takes an id and returns a contract; there is
no parameter through which fixture text can travel.

Stdlib only, matching score.py's no-dependency convention.
"""
from __future__ import annotations

import copy

# Environment variables every verifier may see. Deliberately excludes every
# credential-bearing name — a verifier is a determinism check, not a client.
_BASE_ENV_ALLOWLIST: tuple[str, ...] = ("PATH", "HOME", "LANG", "LC_ALL", "PYTHONHASHSEED")

# Each entry is a complete execution contract. `cwd` is relative to the
# workspace root the runner owns, never to a fixture-supplied path.
REGISTRY: dict[str, dict] = {
    "toolkit_eval_unit_tests": {
        "description": "Mechanical scorer regression suite.",
        "argv": ["python3", ".claude/skills/ywc-toolkit-eval/scripts/test_score.py"],
        "cwd": ".",
        "timeout": 120,
        "env_allowlist": _BASE_ENV_ALLOWLIST,
        "expected_exit": 0,
    },
    "toolkit_eval_fixture_tests": {
        "description": "v2 fixture schema and verifier registry suite.",
        "argv": ["python3",
                 ".claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py"],
        "cwd": ".",
        "timeout": 120,
        "env_allowlist": _BASE_ENV_ALLOWLIST,
        "expected_exit": 0,
    },
    "toolkit_eval_score_ci": {
        "description": "Deterministic mechanical scorer gate (baseline must not drift).",
        "argv": ["python3", ".claude/skills/ywc-toolkit-eval/scripts/score.py", "--ci"],
        "cwd": ".",
        "timeout": 300,
        "env_allowlist": _BASE_ENV_ALLOWLIST,
        "expected_exit": 0,
    },
}


class UnknownVerifier(KeyError):
    """Raised when a fixture names a verifier id that is not registered."""


def verifier_ids() -> tuple[str, ...]:
    """Every registered verifier id, in declaration order."""
    return tuple(REGISTRY)


def is_registered(verifier_id: object) -> bool:
    """True when `verifier_id` names a registry entry.

    Accepts `object` because the caller is usually validating untrusted
    fixture data, where the value may not even be a string.
    """
    return isinstance(verifier_id, str) and verifier_id in REGISTRY


def resolve(verifier_id: str) -> dict:
    """Return a deep copy of the execution contract for `verifier_id`.

    The copy matters: callers routinely build a command from the entry, and a
    shared mutable dict would let one case's mutation leak into the next.
    """
    if not is_registered(verifier_id):
        raise UnknownVerifier(
            f"unregistered verifier id {verifier_id!r}; "
            f"registered ids are {', '.join(verifier_ids())}")
    return copy.deepcopy(REGISTRY[verifier_id])
