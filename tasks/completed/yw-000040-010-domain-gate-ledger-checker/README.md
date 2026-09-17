# yw-000040-010-domain-gate-ledger-checker

## Purpose
Deliver the optional Gate Ledger grammar and stdlib-only checker for `ywc-verify-done`.

## Scope
Implement parsing, `--status`, bare recovery, `--reverify`, fingerprints, evidence rewrites, bounded shell execution, regex isolation, and POSIX process cleanup; document the exact grammar beside the checker.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260917-codex-verify-done-gate-ledger-port.md#acceptance-criteria` — observable checker contract
- `docs/ywc-plans/20260917-codex-verify-done-gate-ledger-port.md#functional-requirements` — grammar, modes, limits, and rewrite rules
### Summary
This is an optional escalation for multi-command and accepted-subagent-artifact claims. `--status` is read-only, bare mode resumes only uncached runnable gates, and `--reverify` is the only fresh ledger evidence mode. The checker is not a sandbox; callers must inspect every inherited `CHECK`.
### Out of Scope (from spec)
- Hermetic tests — `yw-000040-020-test-gate-ledger-checker`
- Skill/docs/eval/locales — `yw-000041-010-docs-verify-done-ledger`
- Generated package — `yw-000042-010-infra-verify-done-package-sync`
- PR polling, approval enforcement, concurrent-write safety, and changes to the canonical five-step gate

## Criticality
critical — arbitrary shell execution and process cleanup require full implementation/security review.

## Dependencies
### Depends On
- (None — root task)
### Depended By
- `yw-000040-020-test-gate-ledger-checker` — exercises this CLI contract
- `yw-000041-010-docs-verify-done-ledger` — documents verified semantics

## Key Files
- `codex/skills/ywc-verify-done/scripts/gate-check.py` — checker CLI
- `codex/skills/ywc-verify-done/references/gate-ledger.md` — grammar/reference

## Notes
- Python 3 standard library only; use installed command examples.
- `124` is timeout and `125` is output cap; malformed input fails before checks run.

## Hardening Evidence
- Test feedback path: `yw-000040-020-test-gate-ledger-checker`.
- Interface Contract: owner `gate-check.py`; signature `python3 gate-check.py [--status|--reverify] <ledger.md>`; consumers are the test task and skill docs; return `NEEDS_CONTEXT` on mismatch.
- Data Integrity Hardening: trigger present for evidence rewrite; one read/execute/rewrite per invocation, exact PASS fingerprint as idempotency key, no concurrent-write claim; test final-field replacement, insertion anchor, CRLF, and no-write failures.
- Critical surface review required for shell, timeout, output cap, regex, and process groups.

## Ownership
`codex/skills/ywc-verify-done/scripts/gate-check.py` and `codex/skills/ywc-verify-done/references/gate-ledger.md` only.

## Shared Surfaces
- Ledger grammar and field semantics
- CLI exit statuses, cache fingerprint, and evidence format

## Conflicts With
- `yw-000040-020-test-gate-ledger-checker` — coupled to the finished CLI contract

## Parallelizable After
- (Root task — no predecessor required)

## Task Verify
- `python3 -m py_compile codex/skills/ywc-verify-done/scripts/gate-check.py`
- `python3 codex/skills/ywc-verify-done/scripts/gate-check.py --status <temporary-valid-ledger>` with a side-effect sentinel

## Out of Scope
Do not edit tests, skill prose, locales, evals, generated package, or polling scripts.
