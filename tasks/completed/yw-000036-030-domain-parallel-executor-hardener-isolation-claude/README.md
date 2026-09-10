# yw-000036-030-domain-parallel-executor-hardener-isolation-claude

## Purpose
Move the claude-code `ywc-parallel-executor`'s wave-boundary Hardener gate to run before delivery, by routing wave delivery through a temporary integration branch (`wave-int/<N>`) and gating promotion on the Hardener's verdict — closing the defect where an `enforced` gate at Step 4e.5 currently runs after the wave is already merged into base.

## Scope
- `claude-code/skills/ywc-parallel-executor/SKILL.md`:
  - Reorder so the `wave-complete` checkpoint fires only after a passing Hardener, via a new promotion step.
  - Step 4e: create `wave-int/<N>` (idempotently — reuse if it already exists) only when the Pre-flight scan found the wave contract-bearing; push it to origin immediately at creation; extend the `--local-merge`/`--draft`/`--aggregate-pr` finish-branch mode-mapping rows with `--base-branch wave-int/<N>`.
  - New Pre-flight scan step (before Step 4a's worktree creation, or wherever Pre-flight already lives): for each wave, read every member task's declared `quality_gate_contract` field, OR across the wave, and produce the `has_contract` boolean fed into `init-parallel --waves`; malformed/missing/absent-task-directory cases stop with `NEEDS_CONTEXT`.
  - New promotion step (after Hardener, before `wave-complete`): fast-forward base to `wave-int/<N>` on a passing gate; on failure, merge base into the integration branch and re-run Hardener (never rebase), bounded by the two-counter attempt bound (Mutation Loop Cap per dispatch, `promotion_retry_count` capped at 2 for base-churn).
  - `--per-task-pr`'s advisory-cap statement and the carve-out rule ("an isolation branch can only protect state whose point-of-no-return sits after the gate").
  - Step 4i's terminal-state audit: third bucket for tasks individually `DONE` but wave-int promotion Hardener-`BLOCKED`.
- New `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md`: the integration-branch lifecycle, promotion procedure, and promotion-conflict handling, linked from the body with `> **Action required**: Read [...]`.
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md`: amend the `task-merged`/`wave-complete` semantics rows; add the un-promoted-wave, partial-merge, and `hardener_verdict`-branching resume cases.
- `claude-code/skills/ywc-parallel-executor/references/aggregate-pr.md`: amend the end-of-run `git reset --hard origin/<base>` step so it does not discard an un-promoted integration branch.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md` — full spec; this task implements FR-1, FR-2, FR-3, FR-6, FR-9, FR-11 (claude-code half), and FR-12 (claude-code half)
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md#acceptance-criteria` — AC1, AC2, AC3, AC4, AC5, AC6, AC8, AC12, AC14
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.architecture-verdict.md` — the adjudicated decision (3-mode isolation, `--per-task-pr` carve-out, the principled rule, branch-lineage reasoning); cite rather than re-derive
- `claude-code/skills/ywc-parallel-executor/SKILL.md:264` (`4e`), `:351` (`4e.5`), `:306-312` (mode-mapping table), `:270-302` (per-task PR lifecycle, do not change), `:268` (sequential delivery loop — cited reason no new locking is needed), `:385-396` (Step 4i two-bucket audit)
- `claude-code/skills/ywc-finish-branch/SKILL.md:45` (`--base-branch` argument, no change needed), `:218-226` (`local-merge` sequence, `git pull origin <base-branch>` unconditional at `:222`)
- `claude-code/skills/ywc-sequential-executor/references/aggregate-pr.md:30,34-35` (`WORK_BRANCH` push-at-creation precedent, generalized here)
- `claude-code/skills/references/pr-conflict-resolution.md` — merge base in, never rebase

### Summary
Today, Step 4e delivers every wave task into base and stamps `task-merged`/`wave-complete`, then Step 4e.5's Hardener runs against the merged base — too late for a `BLOCKED` verdict to prevent anything. This task keeps the merged-diff property Hardener needs (cross-task interaction gaps only surface post-merge) while moving the merge target to a wave-scoped integration branch, `wave-int/<N>`, for the three modes whose point-of-no-return sits after the wave boundary (`--local-merge`, `--draft`, `--aggregate-pr`). `--per-task-pr`'s point-of-no-return (`gh pr merge --delete-branch`) is inside the wave per task, so it cannot be isolated — it keeps today's ordering and the wave-boundary check becomes advisory/reporting-only there, per `yw-000036-050`'s enforcement-eligibility rule. A wave with zero contract-bearing tasks never creates `wave-int/<N>` and delivers direct to base exactly as today (OR-based per-wave routing, not per-task). Interruption/resume must distinguish "merged but not yet promoted" from a deliberate Hardener `BLOCKED` via the new `hardener_verdict` field from `yw-000036-010`.

### Out of Scope (from spec)
- The codex variant — `yw-000036-040`.
- The `quality-gates.md` enforcement-eligibility rule text itself — `yw-000036-050` (this task only links to it, per the `> **Action required**: Read [...]` convention; it must not restate the rule inline).
- The ADR — `yw-000036-060`.
- `--per-task-pr`'s per-task PR lifecycle body (`SKILL.md:270-302`) — explicitly unchanged except the advisory-cap statement and rationale.
- Retargeting per-task PR bases, or a second int→base PR per wave — rejected Option B, not implemented anywhere.

## Criticality
`normal` — skill prompt/reference text and branch-topology procedure; no auth/payment/secret/PII surface (spec's own `## Critical Surfaces` states N/A).

## Dependencies

### Depends On
- `yw-000036-010-domain-parallel-executor-state-schema` — provides `integration_branch`, `hardener_verdict`, `promotion_retry_count` fields and the `hardener-verdict`/`promotion-retry` subcommands this task's prose describes and this task's Task Verify invokes.

### Depended By
- `yw-000036-060-docs-adr-hardener-isolation` — the ADR records the final branch-name/promotion-step-label decisions this task settles.

## Key Files
- `claude-code/skills/ywc-parallel-executor/SKILL.md` — Step 4e/4e.5 reorder, new Pre-flight subsection, new promotion step, mode-mapping table, carve-out rule, Step 4i third bucket.
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md` (new) — lifecycle/promotion/conflict-handling procedure.
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md` — amended resume table.
- `claude-code/skills/ywc-parallel-executor/references/aggregate-pr.md` — amended end-of-run reset guard.

## Notes
- Resolve the two spec Open Questions here (the promotion step's label and `wave-int/<N>`'s exact form/namespacing): use `4e.6` for the promotion step (avoids colliding with the unported upstream `4f`) and `wave-int/<N>` as the branch name unless a concurrent-run collision concern makes a run-id/timestamp segment worth adding — if added, mirror `aggregate-pr.md`'s existing `draft/`/`aggregate/` timestamp-segment pattern and keep it consistent with whatever `yw-000036-010` already assumed for branch-name computation.
- Both `SKILL.md` files are at/over the ~500-line soft convention (484 at investigation time) — this task's body changes must stay minimal (step reorder, Pre-flight subsection, carve-out rule, pointer to the new reference) with the bulk of new prose in `references/wave-integration-branch.md` (FR-9).
- The dispatch-failure rule ("`DONE_WITH_CONCERNS`, never `BLOCKED`") at `SKILL.md:351` must be preserved verbatim and must still allow promotion — a dispatch failure is not a blocking Hardener verdict.
- `wave-complete`'s "refuses while any task is pending" guard in `update-state.py` is reused unchanged as the promotion precondition — only the call site moves later in the skill body.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md` (new)
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md`
- `claude-code/skills/ywc-parallel-executor/references/aggregate-pr.md`

### Owned Interface
- The promotion step's final label (e.g. `4e.6`) and `wave-int/<N>`'s final branch-name form — downstream tasks (`yw-000036-060`) trust these exact strings without re-deriving them.

### Shared Surfaces
- `claude-code/skills/scripts/update-state.py` (read-only — invoked via its CLI, not edited)
- `claude-code/skills/references/quality-gates.md` (read-only link, not edited — that's `yw-000036-050`)
- `claude-code/skills/ywc-finish-branch/SKILL.md` (read-only — this task relies on its existing `--base-branch` argument and unconditional `git pull`, does not modify it)

### Conflicts With
- (None identified — disjoint files from every other task in this batch)

### Parallelizable After
- `yw-000036-010-domain-parallel-executor-state-schema`

### Task Verify
- `grep -n "^\*\*4e\.\|^\*\*4e\.5\.\|^\*\*4e\.6\.\|^\*\*4g\." claude-code/skills/ywc-parallel-executor/SKILL.md` — confirm the promotion step appears between Hardener (`4e.5`) and Clean Up (`4g`), and that the `wave-complete` invocation is textually inside/after the promotion step, not inside `4e`.
- `grep -n "wave-int/" claude-code/skills/ywc-parallel-executor/SKILL.md` — confirm the mode-mapping table rows for `--local-merge`, `--draft`, `--aggregate-pr` reference `--base-branch wave-int/`.
- `grep -c "isolation branch can only protect state whose point-of-no-return" claude-code/skills/ywc-parallel-executor/SKILL.md` — confirm the carve-out rule is stated as a rule (≥1 match).
- `grep -n "Hardener-BLOCKED\|hardener.*blocked" claude-code/skills/ywc-parallel-executor/SKILL.md` — confirm Step 4i's third bucket exists.
- `grep -n "Action required" claude-code/skills/ywc-parallel-executor/SKILL.md` — confirm the new reference is linked via the canonical directive, not inlined.
- `python3 claude-code/skills/scripts/update-state.py init-parallel --mode local-merge --tasks-dir tasks/ --waves '[{"wave":1,"tasks":["t-a"],"has_contract":true}]'` then `hardener-verdict 1 BLOCKED` — confirm the state this task's prose describes for a blocked promotion (integration branch preserved, `wave-complete` not stamped) matches the actual schema the prose cites.
- `bash scripts/validate.sh`

## Out of Scope
- Any change to `codex/skills/ywc-parallel-executor/SKILL.md` or its references — `yw-000036-040`.
- Any change to `claude-code/skills/references/quality-gates.md` — `yw-000036-050`.
- Writing the ADR — `yw-000036-060`.
- Changing `--per-task-pr`'s PR lifecycle body (`SKILL.md:270-302`) beyond the advisory-cap statement.
- Changing `ywc-finish-branch/SKILL.md` itself — its existing `--base-branch` argument already suffices.
