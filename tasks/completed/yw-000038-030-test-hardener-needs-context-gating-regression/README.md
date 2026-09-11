# yw-000038-030-test-hardener-needs-context-gating-regression

## Purpose
Deliver the regression coverage the spec's `## Scope` and AC1/AC2/AC5/AC6/AC8 require: extend the existing shared test harness (`scripts/test-wave-int-checkpoint-ownership.sh`) so `NEEDS_CONTEXT` is exercised end to end — `update-state.py hardener-verdict` acceptance/rejection, and `resume-state.py`'s new `blocked`/`needs_context`/`valid` status branching — against both `claude-code/skills/` and `codex/skills/`.

## Scope
- Extend `scripts/test-wave-int-checkpoint-ownership.sh`'s existing `ROOTS` array/loop (already iterating `claude-code/skills/scripts/update-state.py` and `codex/skills/scripts/update-state.py`) with new assertion blocks for AC1 (`hardener-verdict <N> NEEDS_CONTEXT` accepted, field written) and AC2 (an invalid verdict rejected with the exact sorted 4-value `die()` message).
- Add a **second**, parallel `RESUME_STATE_ROOTS` array (`claude-code/skills/ywc-parallel-executor/scripts/resume-state.py`, `codex/skills/ywc-parallel-executor/scripts/resume-state.py`) and its own loop — `resume-state.py` lives at a structurally different path than `update-state.py` and is a different script, so it cannot reuse the existing `ROOTS` loop. Fixture: a hand-constructed state file with an in-progress wave, empty `pending`, and `hardener_verdict` set to each of `BLOCKED` / `NEEDS_CONTEXT` / absent / `"PASS"` (AC5 for the first two, AC6 non-regression for the latter two, plus AC6's non-empty-`pending` case).
- Promotion-gate documentation presence (AC3, AC7, AC9) is explicitly out of this test script's scope per the spec's Non-Functional Requirements table — those are grep/text-presence checks, already listed in `yw-000038-010`/`yw-000038-020`'s own Task Verify, not runtime assertions this script performs.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md` — full spec; this task delivers the `## Scope` regression-test bullet and closes AC1, AC2, AC5, AC6, AC8 (test half)
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md#acceptance-criteria` — exact scenario definitions, expected `status`/`reason`/`blocked_detail` values
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md#existing-constraints-touched` (harness row) — the `RESUME_STATE_ROOTS`-as-second-parallel-loop requirement this task implements literally
- `scripts/test-wave-int-checkpoint-ownership.sh` — existing harness this task extends (`assert_eq`/`assert_contains` helpers, `ROOTS` array, disposable temp-git-repo pattern)
- `yw-000038-010`, `yw-000038-020` (finished implementations) — the exact `die()` message text, `resume-state.py` status values, and `reason`/`blocked_detail` field shapes this task asserts against

### Summary
The existing script already covers `wave-int-owner`/`wave-int-blocked`/`wave-int-status` and the reuse procedure via one `ROOTS` loop over `update-state.py`. This task adds two independent extensions to that same file rather than a new script: more assertion blocks inside the existing loop (cheap — `hardener-verdict` is already a `cmd_hardener_verdict` subcommand the harness's fixtures can drive) and a wholly new `RESUME_STATE_ROOTS` loop for `resume-state.py`, which needs no live git branch state (unlike the `wave-int-*` scenarios) — just a hand-written `.ywc-run-state.json`-shaped fixture file, since `resume-state.py` only reads the state file and does not touch git.

### Out of Scope (from spec)
- Implementing the `NEEDS_CONTEXT` support itself — `yw-000038-010` (claude-code), `yw-000038-020` (codex).
- AC3/AC7/AC9 text-presence checks against `SKILL.md`/`wave-integration-branch.md`/`checkpoint-resume.md` — these are documentation-text assertions the spec's Non-Functional Requirements table explicitly separates from this script's state-transition scope; they are covered by `yw-000038-010`/`yw-000038-020`'s own Task Verify `grep` commands, not duplicated here.
- Retrofitting tests for pre-existing subcommands unrelated to this spec, or a concurrency-locking mechanism — unchanged, out of scope.

## Criticality
`normal` — test-only artifact, no production code path.

## Dependencies

### Depends On
- `yw-000038-010-domain-hardener-needs-context-gating-claude` — provides the claude-code root's `NEEDS_CONTEXT` support this test exercises.
- `yw-000038-020-domain-hardener-needs-context-gating-codex` — provides the codex root's identical support this test exercises.

### Depended By
- (None — leaf task)

## Key Files
- `scripts/test-wave-int-checkpoint-ownership.sh` — extended, not replaced.

## Notes
- Reuse the file's existing `assert_eq`/`assert_contains` helpers, running pass/fail counter, non-zero exit on any failure, `mktemp -d` + `trap ... EXIT` cleanup convention — no new script, no external test framework (matches this repo's established shell-test pattern).
- The `RESUME_STATE_ROOTS` fixtures are pure JSON files (no live git repo needed) since `resume-state.py` never shells out to `git` for the `in_progress`/`pending`-empty branch this spec touches — a plain `mktemp` file suffices, simpler than the `wave-int-*` scenarios' disposable-repo setup.
- Assert the JSON-mode absent-key omission explicitly for a fixture with `hardener_verdict: NEEDS_CONTEXT` but no `reason`/`blocked_detail` set (spec Edge Cases) — the output must omit those keys, never emit `null`.
- Assert AC6's non-empty-`pending` regression case explicitly: an in-progress wave with `hardener_verdict: NEEDS_CONTEXT` but non-empty `pending` must still return `status: "valid"` (case-1 partial-merge precedence, per spec Edge Cases) — this is the one case most likely to be silently broken by an incorrectly-ordered `if` in the two roots' `resume-state.py` edits.

## Parallel Execution Metadata

### Ownership
- `scripts/test-wave-int-checkpoint-ownership.sh`

### Owned Interface
- (None — leaf task, produces a test artifact only)

### Shared Surfaces
- Reads `claude-code/skills/scripts/update-state.py`, `codex/skills/scripts/update-state.py`, `claude-code/skills/ywc-parallel-executor/scripts/resume-state.py`, `codex/skills/ywc-parallel-executor/scripts/resume-state.py` as black boxes via subprocess calls; does not modify any of them.

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000038-010`, `yw-000038-020` — both must be merged before this task's assertions against either root's actual `NEEDS_CONTEXT` behavior can pass.

### Task Verify
- `bash scripts/test-wave-int-checkpoint-ownership.sh` — exits 0, all scenarios (existing + new) pass against both roots.
- `bash scripts/test-wave-int-checkpoint-ownership.sh --root claude-code/skills/scripts/update-state.py` and `--root codex/skills/scripts/update-state.py` individually — both exit 0.
- `bash scripts/validate.sh` — confirms the extended script still passes shellcheck.
