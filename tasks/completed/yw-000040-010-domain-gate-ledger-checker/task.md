# yw-000040-010-domain-gate-ledger-checker — Implementation Checklist

## Prerequisites
- [ ] Confirm the spec-ready log for `docs/ywc-plans/20260917-codex-verify-done-gate-ledger-port.md` is `DONE`.

## Allowed Edit Scope
- [ ] Modify only the two Ownership paths in `README.md`.

## Stop Conditions
- [ ] Stop on any need for third-party dependencies, caller rewrites, sandbox claims, or concurrent-write guarantees.
- [ ] Stop if the public signature or parser contract differs from the spec.

## Hardening Gate
- [ ] Classify as critical behavior-changing implementation with arbitrary shell execution.
- [ ] Name `yw-000040-020` as replacement RED-first evidence because no existing checker coverage exists.
- [ ] Preserve the bounded interface contract and Data Integrity Hardening fields in `README.md`.
- [ ] Require full implementation/security review before `DONE`.

## Implementation Steps
- [ ] Create `codex/skills/ywc-verify-done/references/gate-ledger.md` covering grammar, fences, MANUAL semantics, cache/evidence format, installed CLI, shell warning, and PR-poll boundary.
  - Specify last-field-wins parsing, inert continuations, literal EXPECT, and only `i/m/s` regex flags.
- [ ] Create `codex/skills/ywc-verify-done/scripts/gate-check.py` with `argparse`, fail-closed validation, effective gate parsing, duplicate checks, and UTF-8/NUL SHA-256 fingerprints.
  - Implement read-only `--status`, recovery-only bare mode, and all-gates `--reverify`.
- [ ] Implement `Popen(..., shell=True)` with combined 64-KiB output, 120-second timeout, POSIX process-group cleanup, and regex matching in a bounded `multiprocessing.Process`.
  - Serialize `124`/`125` failures and rewrite only the final effective EVIDENCE or insert after final EXPECT while retaining LF/CRLF.
- [ ] Run syntax and temporary-ledger probes without modifying callers.

## Task Verify
- [ ] `python3 -m py_compile codex/skills/ywc-verify-done/scripts/gate-check.py`
- [ ] `python3 codex/skills/ywc-verify-done/scripts/gate-check.py --status <temporary-valid-ledger>` exits 0 without subprocess side effects.

## Verification
- [ ] Lint: N/A — no repository lint command.
- [ ] Typecheck: `python3 -m py_compile ...`.
- [ ] Unit tests: required via `python3 codex/skills/ywc-verify-done/scripts/test_gate_check.py` after the dependent task.
- [ ] Integration/build: N/A — no service or application build pipeline.

## Implementation Notes (optional)
