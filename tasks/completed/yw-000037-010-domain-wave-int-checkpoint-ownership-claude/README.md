# yw-000037-010-domain-wave-int-checkpoint-ownership-claude

## Purpose
Close the wave-int reuse gap in the claude-code `ywc-parallel-executor`: a later run can silently promote stale, non-base content left over `BLOCKED` by a prior run's `wave-int/<N>`, and an origin-only `wave-int/<N>` has no local ref for `ywc-finish-branch` to target. Add a `run_id` + per-wave checkpoint ownership/tip-SHA fields to `.ywc-run-state.json`, and rewrite the wave-int reuse procedure to verify ownership and tip-SHA before any reuse, materializing an origin-only branch when needed.

## Scope
- `claude-code/skills/scripts/update-state.py`:
  - FR-1: `cmd_init_parallel` generates and writes a top-level `run_id` (`uuid.uuid4().hex[:8]`), immutable for the run's life.
  - FR-2: three new subcommands — `wave-int-owner <N> --tip-sha <sha>`, `wave-int-blocked <N> --reason <reason> [--detail <text>]`, `wave-int-status <N>` (read-only, no `run_id` precondition) — cloning `cmd_hardener_verdict` / `cmd_promotion_retry`'s load → find_wave → mutate → save shape.
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md`:
  - FR-3: rewrite the "Idempotent creation" section (`:26-32`) into the 5-step verification procedure (status read → existence check → branch-missing-but-owned → fresh creation → owner-matched reuse with ancestor-check).
  - FR-4: origin-only branch materialization (`git fetch origin wave-int/<N>:wave-int/<N>`) before the ancestor-check comparison.
  - FR-5: `wave-int-owner` call sites at creation (`:34-39`) and post-base-merge (`:70-77`).
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md`: document the new `run_id` / `integration_branch_owner` / `integration_branch_tip_sha` fields and the resume-time ownership check (same-run resume passes trivially since `run_id` and prior tip SHA are already in this run's own state file).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md` — full spec; this task implements FR-1, FR-2, FR-3, FR-4, FR-5 (claude-code half)
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md#acceptance-criteria` — AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC9, AC10 (claude-code half of each)
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md#api-contract` — exact `die()` message text and success-print format for all three subcommands
- `claude-code/skills/scripts/update-state.py:97-118` (`cmd_init_parallel`), `:57-68` (`save`), `:207-215` (`cmd_hardener_verdict`, the subcommand shape to clone), `:218` (`PROMOTION_RETRY_CAP` module-constant precedent)
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md:26-32` (idempotent-creation check to rewrite), `:41` (push-at-creation precedent)
- `claude-code/skills/ywc-finish-branch/SKILL.md:91` (local-ref `--base-branch` precondition this task's FR-4 materialization satisfies)
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md:86-94` (Resume with `wave-int/<N>` — the three existing resume cases this task's ownership check extends)

### Summary
`cmd_init_parallel` and the wave-integration-branch reuse check currently have no way to distinguish a legitimate same-run resume from a different run reusing a wave number whose `wave-int/<N>` was left `BLOCKED` by a prior run — the existing check only asks "does the branch exist?" and reuses unconditionally. This task adds a `run_id` generated once at `init-parallel` and two optional per-wave checkpoint fields (`integration_branch_owner`, `integration_branch_tip_sha`), plus three subcommands that read/write them without ever hand-editing `.ywc-run-state.json`. The reuse procedure is rewritten so ownership is verified before merge, tip-SHA divergence is detected via `git merge-base --is-ancestor` (not exact equality — AC1's own resume scenario, interrupted after a partial per-task merge, would otherwise false-positive), and an origin-only branch is fetched into a local tracking ref before any task delivery. Every `BLOCKED` outcome routes through `wave-int-blocked` with a `--detail` string naming the branch and the relevant SHA(s), never a bare prose instruction.

### Out of Scope (from spec)
- The codex root's identical hand-edit — `yw-000037-020`.
- The regression test file exercising both roots — `yw-000037-030`.
- Any change to `ywc-finish-branch` itself — materializing the local ref before the call is sufficient (spec `## Out of Scope`).
- Any change to the promotion fast-forward / base-merge-in / Hardener re-run / `promotion_retry_count` logic (`wave-integration-branch.md:54-85`) — this task's verification runs strictly before that existing sequence.
- Non-contract-bearing waves (`integration_branch == None`) — unaffected, per spec `## Out of Scope`.
- A locking mechanism for interleaved concurrent runs — explicitly out of scope per the spec's Concurrency precondition NFR.

## Criticality
`normal` — internal orchestration state of the parallel executor (`.ywc-run-state.json`, already `.gitignore`d); no auth/payment/PII surface (spec's own `## Critical Surfaces` states N/A).

## Dependencies

### Depends On
- (None — root task, parallel-safe against `yw-000037-020` since the two touch disjoint files)

### Depended By
- `yw-000037-030-test-wave-int-checkpoint-ownership-regression` — the regression test exercises this task's three subcommands and the rewritten reuse procedure against the claude-code root.

## Key Files
- `claude-code/skills/scripts/update-state.py` — `cmd_init_parallel` (`run_id` generation), new `cmd_wave_int_owner` / `cmd_wave_int_blocked` / `cmd_wave_int_status` handlers, argparse subparser registration, module docstring subcommand list, new `import uuid`.
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md` — "Idempotent creation" section rewrite (`:26-32` region), call sites at `:34-39` and `:70-77`.
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md` — State File Format JSON block, Checkpoint Summary table, "Resume with `wave-int/<N>`" section.

## Notes
- `wave-int-owner`'s owner is always read from the state's own `run_id` — never accept an `--owner` argument, so a caller cannot claim ownership on behalf of a different run (spec FR-2).
- `wave-int-status` has **no** `run_id` precondition (spec Iteration 3's fix) — it is a pure read with no mutation, so a pre-this-spec checkpoint missing `run_id` entirely still gets `unset unset` rather than a `die()`, which is what lets the reuse procedure reach its own AC2 branch for that edge case.
- FR-3 step 5.3's `git cat-file -e <recorded-sha>` check must run *before* the `git merge-base --is-ancestor` check — a missing object is a git-internal failure (`wave-int-materialize-failed`), never `wave-int-tip-mismatch`.
- `--detail` strings are exact per FR-3's numbered steps (e.g. `"branch=wave-int/<N> recorded-owner=<owner> recorded-tip=<tip-sha>"`) — match them verbatim so AC2/AC3/AC9's diagnostic-content requirement is satisfiable by a test asserting on `blocked_detail`.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/scripts/update-state.py`
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md`
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md`

### Owned Interface
- New `.ywc-run-state.json` top-level field: `run_id: str` (immutable post-`init-parallel`).
- New per-wave fields: `integration_branch_owner: str` (absent until first write), `integration_branch_tip_sha: str` (absent until first write).
- New subcommands: `wave-int-owner <N> --tip-sha <sha>`, `wave-int-blocked <N> --reason <reason> [--detail <text>]`, `wave-int-status <N>` — downstream tasks (`yw-000037-030`) trust these mutate/read exactly per the spec's `## API Contract` table.

### Shared Surfaces
- `.ywc-run-state.json` schema — the codex root (`yw-000037-020`) independently implements an identical schema; no direct file overlap, but subcommand behavior must match byte-for-byte per AC8.

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 claude-code/skills/scripts/update-state.py init-parallel --mode local-merge --tasks-dir tasks/ --waves '[{"wave":1,"tasks":["t-a"],"has_contract":true}]'` then inspect `.ywc-run-state.json`: top-level `run_id` is a non-empty 8-hex-char string (AC7).
- `python3 claude-code/skills/scripts/update-state.py wave-int-owner 1 --tip-sha abc123` — confirm `waves[0].integration_branch_owner` equals the state's own `run_id` and `integration_branch_tip_sha == "abc123"`; confirm `wave-int-status 1` prints `<run_id> abc123`.
- `python3 claude-code/skills/scripts/update-state.py wave-int-blocked 1 --reason wave-int-ownership-mismatch --detail "branch=wave-int/1 no owner recorded for run xyz"` — confirm `waves[0].status == "BLOCKED"`, `reason == "wave-int-ownership-mismatch"`, `blocked_detail` matches.
- `python3 claude-code/skills/scripts/update-state.py wave-int-status 2` against a wave with no owner/tip-sha set — confirm it prints `unset unset` and exits 0.
- Manually unset `run_id` in the state file, then `python3 claude-code/skills/scripts/update-state.py wave-int-owner 1 --tip-sha abc` — confirm non-zero exit and no write; `wave-int-status 1` against the same file — confirm it still succeeds.
- `bash scripts/validate.sh`
