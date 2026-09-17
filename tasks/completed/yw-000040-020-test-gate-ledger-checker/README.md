# yw-000040-020-test-gate-ledger-checker

## Purpose
Prove the Gate Ledger checker contract with a direct Python 3 standard-library suite.

## Scope
Cover parsing, status read-only behavior, cache/reverify, rewrites, malformed input, regex/fences, CRLF, output/time limits, fingerprints, and POSIX descendant cleanup.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260917-codex-verify-done-gate-ledger-port.md#acceptance-criteria` — required hermetic evidence matrix
- `docs/ywc-plans/20260917-codex-verify-done-gate-ledger-port.md#fr-5-tests-and-package-flow` — direct test and install requirements
### Summary
The suite runs directly with `python3` and resolves the sibling checker with `Path(__file__)`. It proves fail-closed safety and positive behavior, including no subprocesses for `--status` and cleanup of SIGTERM-ignoring descendants.
### Out of Scope (from spec)
- Checker implementation — `yw-000040-010-domain-gate-ledger-checker`
- Docs/eval/locales — `yw-000041-010-docs-verify-done-ledger`
- Generated package and PR polling

## Criticality
critical — required regression evidence for shell execution and process cleanup.

## Dependencies
### Depends On
- `yw-000040-010-domain-gate-ledger-checker` — provides the checker CLI
### Depended By
- `yw-000041-010-docs-verify-done-ledger` — needs verified semantics

## Key Files
- `codex/skills/ywc-verify-done/scripts/test_gate_check.py` — hermetic assertions

## Notes
Tests may copy the checker and replace named timeout constants only in the copy; production limits remain unchanged.

## Hardening Evidence
- Test feedback path: this suite with explicit exit/assertion output.
- Interface Contract: owner `yw-000040-010`; signature `python3 gate-check.py [--status|--reverify] <ledger.md>`; consumer is this suite; return `NEEDS_CONTEXT` on mismatch.
- Data Integrity Hardening: N/A in production; assert the owner's rewrite/idempotency behavior.
- Full implementation/security review must include process cleanup and bounds results.

## Ownership
`codex/skills/ywc-verify-done/scripts/test_gate_check.py` only.

## Shared Surfaces
- Checker CLI and serialized PASS/FAIL evidence
- Named timeout constants copied for fixtures

## Conflicts With
- `yw-000040-010-domain-gate-ledger-checker` — assertions consume its contract

## Parallelizable After
- `yw-000040-010-domain-gate-ledger-checker`

## Task Verify
- `python3 codex/skills/ywc-verify-done/scripts/test_gate_check.py`
- `python3 -m py_compile codex/skills/ywc-verify-done/scripts/gate-check.py codex/skills/ywc-verify-done/scripts/test_gate_check.py`

## Out of Scope
Do not modify the checker, docs, evals, locales, generated package, or validation scripts.
