# Task: yw-000038-030-test-hardener-needs-context-gating-regression

## Prerequisites
- [ ] `yw-000038-010-domain-hardener-needs-context-gating-claude` merged (claude-code `NEEDS_CONTEXT` support present).
- [ ] `yw-000038-020-domain-hardener-needs-context-gating-codex` merged (codex `NEEDS_CONTEXT` support present).

## Allowed Edit Scope
Only `scripts/test-wave-int-checkpoint-ownership.sh`. Do not modify `update-state.py`, `resume-state.py`, `SKILL.md`, or any reference file in either root — this task is test-only.

## Stop Conditions
- If `scripts/test-wave-int-checkpoint-ownership.sh`'s existing `ROOTS` array or `assert_eq`/`assert_contains` helper signatures have changed shape since `yw-000037-030` wrote them, stop and report — do not silently reshape the existing harness.
- If either root's `resume-state.py --json` output for a `NEEDS_CONTEXT`/`BLOCKED` fixture does not include `status`, or includes `null` for an absent `reason`/`blocked_detail` instead of omitting the key, stop and report — this is a spec-defined regression in the upstream task, not something to paper over with a lenient assertion.

## Implementation Steps
- [ ] Add an `assert_eq`-based block inside the existing `ROOTS` loop asserting `hardener-verdict <N> NEEDS_CONTEXT` writes `waves[].hardener_verdict == "NEEDS_CONTEXT"` and exits 0 (AC1).
- [ ] Add an `assert_contains`-based block inside the same loop asserting `hardener-verdict <N> BOGUS` exits non-zero and its stderr/stdout contains the exact sorted-4-value `die()` message `verdict must be one of ['BLOCKED', 'NEEDS_CONTEXT', 'PASS', 'absent'], got 'BOGUS'` (AC2).
- [ ] Declare a new `RESUME_STATE_ROOTS=("claude-code/skills/ywc-parallel-executor/scripts/resume-state.py" "codex/skills/ywc-parallel-executor/scripts/resume-state.py")` array near the existing `ROOTS` declaration.
- [ ] Write a fixture-builder helper (e.g. `make_resume_fixture <pending_json> <hardener_verdict_or_empty> <reason_or_empty> <blocked_detail_or_empty>`) that emits a minimal valid `.ywc-run-state.json` with one `in_progress` wave carrying the given `pending`/`hardener_verdict`/`reason`/`blocked_detail`, using `mktemp` for the file (no git repo needed).
- [ ] Add a new loop over `RESUME_STATE_ROOTS` asserting, per script:
  - `pending: []`, `hardener_verdict: "NEEDS_CONTEXT"` → `--json` output `status == "needs_context"` (AC5).
  - `pending: []`, `hardener_verdict: "BLOCKED"` → `status == "blocked"` (AC5).
  - `pending: []`, `hardener_verdict` absent → `status == "valid"` (AC6).
  - `pending: []`, `hardener_verdict: "PASS"` → `status == "valid"` (AC6).
  - `pending: ["task-a"]` (non-empty), `hardener_verdict: "NEEDS_CONTEXT"` → `status == "valid"` (AC6, case-1 partial-merge precedence per spec Edge Cases).
  - `pending: []`, `hardener_verdict: "NEEDS_CONTEXT"`, no `reason`/`blocked_detail` set → JSON output omits both keys entirely (no `null`) (spec Edge Cases).
- [ ] Confirm the new blocks run under both the default (all-roots) invocation and an explicit `--root <path>` invocation, matching the existing `update-state.py` blocks' parameterization convention.
- [ ] Update the script's running pass/fail summary output (if it names scenario groups) to include the new group names.

## Task Verify
- [ ] `bash scripts/test-wave-int-checkpoint-ownership.sh` — exits 0.
- [ ] `bash scripts/test-wave-int-checkpoint-ownership.sh --root claude-code/skills/scripts/update-state.py` — exits 0.
- [ ] `bash scripts/test-wave-int-checkpoint-ownership.sh --root codex/skills/scripts/update-state.py` — exits 0.

## Verification
- [ ] `bash scripts/validate.sh` passes (shellcheck on the extended script).

## Implementation Notes
(Populated during execution — not authored at generation time.)
