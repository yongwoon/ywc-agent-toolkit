# yw-000037-030-test-wave-int-checkpoint-ownership-regression

## Purpose
Deliver the regression coverage the spec's `## Scope` and AC8/AC10 require: one shared test script that exercises `wave-int-owner` / `wave-int-blocked` / `wave-int-status` and the rewritten reuse procedure against **both** `claude-code/skills/scripts/update-state.py` and `codex/skills/scripts/update-state.py`, satisfying AC8's "verified by the new regression test running against both copies" and AC10's per-subcommand `die()`-path coverage.

## Scope
- New `scripts/test-wave-int-checkpoint-ownership.sh`, parameterized to run against both roots (default: iterate `claude-code/skills/scripts/update-state.py` then `codex/skills/scripts/update-state.py`; accepts an optional `--root <path>` to target one).
- Subcommand-level (unit-boundary) coverage: AC7 (`run_id` present), AC10 (all `die()` rows for `wave-int-owner`/`wave-int-blocked`: executor-mismatch, `run_id`-unset, wave-not-found; `wave-int-status`'s narrower two-row coverage; success paths and print-format assertions for all three).
- Integration-boundary (git + `.ywc-run-state.json`) coverage using a disposable temp git repo: AC1 (same-run resume, including an intervening per-task merge before the checkpoint's recorded tip), AC2 (ownership mismatch, both the unset-owner and owner-mismatch variants), AC3 (tip-SHA divergence via `merge-base --is-ancestor`, distinct from the `cat-file`-failure path), AC4 (origin-only branch materialization), AC9 (branch missing but checkpoint claims ownership).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md` — full spec; this task delivers the "Add regression coverage for: ..." bullet in `## Scope` and closes AC1, AC2, AC3, AC4, AC7, AC8 (test half), AC9, AC10
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md#acceptance-criteria` — exact scenario definitions and expected `reason`/`blocked_detail` values to assert against
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md#test-seam` (Acceptance Criteria preamble) — "`scripts/update-state.py`'s new subcommand (`wave-int-owner`) as the unit boundary, and the wave-integration-branch reuse bash procedure as the integration boundary (git branch state + `.ywc-run-state.json` as the two observables)"
- `yw-000037-010`, `yw-000037-020` (finished implementations) — the exact subcommand signatures, `die()` message text, and `--detail` strings this task asserts against
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md#normative-subcommand-contract` — the tiebreaker table to assert against if the two roots' finished implementations disagree on subcommand shape (added per Plan Critical Review, 2026-09-11)

### Summary
Neither `update-state.py` root has an existing automated test suite today (verification is currently done via `Task Verify` CLI-invocation checklists only) — this task introduces the first one, scoped narrowly to the wave-int checkpoint-ownership feature per AC8's explicit "new regression test" requirement rather than retrofitting a general test harness for the whole script. The script must exercise real `git` state (a disposable temp repo with `wave-int/<N>` branches) for the integration-boundary scenarios, since the reuse procedure's behavior depends on actual branch existence, ancestry, and tip SHAs — mocking git would not catch the `merge-base --is-ancestor` vs. exact-equality distinction that AC1/AC3 depend on.

### Out of Scope (from spec)
- Implementing the subcommands or reuse procedure themselves — `yw-000037-010` / `yw-000037-020`.
- Retrofitting tests for the pre-existing subcommands (`wave-start`, `task-merged`, `wave-complete`, `hardener-verdict`, `promotion-retry`) — out of scope, this task covers only the three new subcommands and the reuse procedure they enable.
- A locking mechanism for interleaved concurrent runs, or any test asserting one exists — the spec's Concurrency precondition NFR explicitly leaves this unimplemented.
- Testing the plugin-mirror sync output — that is `yw-000037-020`'s own Task Verify (`diff -r` against the synced mirror), not a concern this shared test script needs to re-verify.

## Criticality
`normal` — test-only artifact, no production code path; no auth/payment/PII surface.

## Dependencies

### Depends On
- `yw-000037-010-domain-wave-int-checkpoint-ownership-claude` — provides the claude-code root's three subcommands and rewritten reuse procedure this test exercises.
- `yw-000037-020-domain-wave-int-checkpoint-ownership-codex` — provides the codex root's identical implementation this test exercises.

### Depended By
- (None — leaf task)

## Key Files
- `scripts/test-wave-int-checkpoint-ownership.sh` — new file.

## Notes
- Follow the existing shell-test convention in this repo (e.g. `claude-code/skills/scripts/test-poll-pr-reviews.sh`, `codex/skills/ywc-task-generator/scripts/test-initials-allocation.sh`): plain `bash` + `set -euo pipefail`, `assert_eq`/`assert_contains`-style helper functions, a running pass/fail counter, non-zero exit on any failure, no external test framework dependency (matches this repo's "no lint/typecheck/build/test toolchain beyond `scripts/validate.sh`" convention).
- Use `mktemp -d` for the disposable git repo per integration-boundary scenario; `trap 'rm -rf "$tmpdir"' EXIT` to avoid leaking temp directories across runs.
- For the origin-only materialization scenario (AC4), simulate "origin" with a second bare repo created via `git init --bare` in the same temp directory, added as a `git remote add origin <path>` — no real network access needed.
- AC1's "intervening per-task merge" scenario must merge a task commit onto `wave-int/<N>` *without* calling `wave-int-owner` afterward (per FR-5, ownership is not re-recorded after every per-task merge) — the ancestor-check assertion is what confirms the branch can run ahead of the last recorded tip and still pass.

## Parallel Execution Metadata

### Ownership
- `scripts/test-wave-int-checkpoint-ownership.sh`

### Owned Interface
- (None — leaf task, produces a test artifact only)

### Shared Surfaces
- Reads both `claude-code/skills/scripts/update-state.py` and `codex/skills/scripts/update-state.py` as black boxes via subprocess calls; does not modify either.

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000037-010`, `yw-000037-020` — both must be merged before this task's assertions against either root's actual subcommand behavior can pass.

### Task Verify
- `bash scripts/test-wave-int-checkpoint-ownership.sh` — exits 0, all scenarios pass against both roots.
- `bash scripts/test-wave-int-checkpoint-ownership.sh --root claude-code/skills/scripts/update-state.py` and `--root codex/skills/scripts/update-state.py` individually — both exit 0 (confirms the `--root` parameterization itself works, not just the default both-roots loop).
- `bash scripts/validate.sh` — confirms the new script passes shellcheck per the existing `validate` workflow.
