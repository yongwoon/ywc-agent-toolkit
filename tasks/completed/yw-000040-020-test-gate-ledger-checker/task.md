# yw-000040-020-test-gate-ledger-checker — Implementation Checklist

## Prerequisites
- [ ] `yw-000040-010-domain-gate-ledger-checker` is merged.
- [ ] Its CLI signature and evidence format match this task's bounded contract.

## Allowed Edit Scope
- [ ] Modify only `codex/skills/ywc-verify-done/scripts/test_gate_check.py`.

## Stop Conditions
- [ ] Stop and report `NEEDS_CONTEXT` if an assertion implies the owner contract is wrong.
- [ ] Stop if tests need a third-party package or production limit weakening.

## Hardening Gate
- [ ] Classify as critical regression-test implementation.
- [ ] Retain RED evidence against missing/reverted checker behavior.
- [ ] Consume only the owner's bounded interface contract.
- [ ] Require full review for process cleanup and arbitrary-shell coverage.

## Implementation Steps
- [ ] Build a temporary-directory harness using `Path(__file__)` and helpers for all three CLI modes.
  - Assert exit codes, output, bytes, and sentinel side effects.
- [ ] Cover parser/status cases: missing/zero/duplicate/malformed gates, last-field-wins, fences, MANUAL, literal/flagged regex, and fingerprint byte distinctions.
- [ ] Cover cache/reverify and rewrite cases: exact PASS, invalidation, failures, decisive JSON, final EVIDENCE replacement, EXPECT insertion, and CRLF.
- [ ] Cover `124` timeout, `125` output cap, catastrophic regex bounds, and POSIX SIGTERM-ignoring descendant cleanup with bounded platform skip.
- [ ] Run the direct suite with no network or third-party dependency.

## Task Verify
- [ ] `python3 codex/skills/ywc-verify-done/scripts/test_gate_check.py`
- [ ] `python3 -m py_compile codex/skills/ywc-verify-done/scripts/gate-check.py codex/skills/ywc-verify-done/scripts/test_gate_check.py`

## Verification
- [ ] Lint: N/A — no repository lint command.
- [ ] Typecheck: `python3 -m py_compile ...`.
- [ ] Unit tests: `python3 codex/skills/ywc-verify-done/scripts/test_gate_check.py`.
- [ ] Integration/build: N/A — no service or application build pipeline.

## Implementation Notes (optional)
