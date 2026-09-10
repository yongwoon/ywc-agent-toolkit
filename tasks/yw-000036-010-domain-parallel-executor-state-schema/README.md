# yw-000036-010-domain-parallel-executor-state-schema

## Purpose
Add the state-schema foundation that the wave-integration-branch feature needs: three new `waves[]` fields in the claude-code `update-state.py` (`integration_branch`, `hardener_verdict`, `promotion_retry_count`), plus the mutation points that write the latter two.

## Scope
- `cmd_init_parallel`: read a new `has_contract` boolean off each `--waves` entry (default `False`) and seed `integration_branch` accordingly.
- New subcommand(s) to record `hardener_verdict` (`absent | PASS | BLOCKED`) at Hardener dispatch exit, and to increment `promotion_retry_count` on a promotion-conflict retry.
- `claude-code/skills/scripts/update-state.py` only. The codex copy is `yw-000036-020`.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md#fr-5-update-statepy--one-new-field-both-copies` — FR-5 (seed logic, `has_contract` data-source contract, malformed-field note)
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md#fr-4-promotion-conflict-behavior-advisor-concern-2` — FR-4 (`promotion_retry_count`, capped at 2, two-counter bound)
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md#fr-6-checkpoint-resumemd--the-un-promoted-wave-resume-case` — FR-6 (`hardener_verdict` field, written once per Hardener dispatch, reset to `absent` on a new dispatch)
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md#acceptance-criteria` — AC7 (exact field semantics, `None`/`false` defaults)
- `docs/ywc-plans/20260910-quality-gate-contract-port.md` (parent spec, FR-4) — `gate_state` must never be written into `.ywc-run-state.json`; this task's fields are delivery/topology state, not gate state

### Summary
`cmd_init_parallel`'s only input is the `--waves` JSON array (task names only today); it has no access to any task's declared `quality_gate_contract` field, so the spec extends the `--waves` schema with a per-wave boolean `has_contract` that a Pre-flight scan (implemented in `yw-000036-030`'s SKILL.md prose, not in this task) computes and threads in. This task reads that boolean with `wave.get("has_contract", False)` and seeds `integration_branch` to the computed branch name (`wave-int/<N>`) when `True`, `None` otherwise — exactly like the existing `status`/`merged`/`pending` `setdefault` pattern, so an in-flight state file from the previous script version stays loadable. `hardener_verdict` and `promotion_retry_count` are not seeded at init; they are written by new mutation points this task adds, mirroring the existing `cmd_task_merged` / `cmd_wave_complete` pattern (`load()` → mutate → `save()`). None of the three fields is ever a `gate_state` value.

### Out of Scope (from spec)
- The Pre-flight scan itself (reading each task directory's `quality_gate_contract` field, OR-ing across the wave, handling the missing/malformed/absent-task-directory `NEEDS_CONTEXT` cases) — that is orchestration prose, delivered by `yw-000036-030` (claude-code SKILL.md).
- The identical edit to the codex copy — `yw-000036-020`.
- Any change to `save-state.py` / `resume-state.py` — the spec records these as *no change needed* (read-only consumers of the schema; adding an optional field is backward compatible).

## Criticality
`normal` — local JSON state-file schema addition, no auth/payment/secret/PII surface.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `yw-000036-020-domain-parallel-executor-codex-state-schema` — mirrors this task's exact field names and subcommand shape onto the codex copy.
- `yw-000036-030-domain-parallel-executor-hardener-isolation-claude` — SKILL.md prose cites the exact subcommand names/args this task adds, and its Task Verify runs them.

## Key Files
- `claude-code/skills/scripts/update-state.py` — `cmd_init_parallel` (has_contract read, integration_branch seed), new subcommand handler(s) for `hardener_verdict` and `promotion_retry_count`, `argparse` subparser registration, module docstring's subcommand list.

## Notes
- Suggested subcommand names (final call is the implementer's, but keep the imperative-verb-phrase style of `wave-start` / `task-merged` / `wave-complete`): `hardener-verdict N VERDICT` (VERDICT ∈ `absent|PASS|BLOCKED`) and `promotion-retry N` (increments `promotion_retry_count`, no argument beyond the wave number).
- `hardener_verdict` is reset to `absent` when a new Hardener dispatch begins (e.g., FR-4's post-merge re-run) — the `hardener-verdict` subcommand must support writing `absent` explicitly, not just `PASS`/`BLOCKED`.
- Branch-name computation (`wave-int/<N>` vs. some other final form) is an open question the spec leaves to the implementer (see spec `## Open Questions`); pick `wave-int/<N>` as the default per AC2's parenthetical ("or the spec's final branch-name form") unless `yw-000036-030` settles on something else first — if so, match it here.
- `die()` in this file currently returns `{}` unreachable after printing to stderr and `sys.exit(1)` elsewhere in the module — follow the existing error-exit convention for the new subcommand's validation failures (e.g., an invalid `VERDICT` value).

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/scripts/update-state.py`

### Owned Interface
- `cmd_init_parallel` waves[] schema: `integration_branch: str | None` — `wave-int/<N>` string when the wave both uses an isolated mode and `has_contract` is `true`; `None` otherwise.
- New subcommand `hardener-verdict N VERDICT` and `promotion-retry N` (exact names may differ — see Notes) — downstream tasks trust these mutate `waves[N].hardener_verdict` / `waves[N].promotion_retry_count` and `save()` atomically, matching every other subcommand's contract.

### Shared Surfaces
- `.ywc-run-state.json` schema — the produced/consumed JSON shape, shared with `save-state.py`, `resume-state.py`, and the SKILL.md prose that reads it.

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 claude-code/skills/scripts/update-state.py init-parallel --mode local-merge --tasks-dir tasks/ --waves '[{"wave":1,"tasks":["t-a"],"has_contract":true},{"wave":2,"tasks":["t-b"],"has_contract":false}]'` then inspect `.ywc-run-state.json`: wave 1's `integration_branch` is `wave-int/1`, wave 2's is `None`.
- Re-run `init-parallel` with a `--waves` entry omitting `has_contract` entirely; confirm `integration_branch` is `None` (default-`false` backward compatibility).
- Invoke the new `hardener-verdict` and `promotion-retry` subcommands against the state file produced above; confirm `waves[].hardener_verdict` / `waves[].promotion_retry_count` update and every other field is untouched.
- `grep -q 'gate_state' claude-code/skills/scripts/update-state.py` — must find no match (the field name must never appear in this file).
- `bash scripts/validate.sh`

## Out of Scope
- Writing to `codex/skills/scripts/update-state.py` (separate task, `yw-000036-020`).
- Any SKILL.md prose change (the Pre-flight scan description, the promotion procedure, the resume table) — those are `yw-000036-030`.
- Adding a new field to `save-state.py` / `resume-state.py` unless this task's own Task Verify reveals they cannot round-trip the new fields (spec records this as unlikely).
