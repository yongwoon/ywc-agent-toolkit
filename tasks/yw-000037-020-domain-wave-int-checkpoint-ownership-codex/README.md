# yw-000037-020-domain-wave-int-checkpoint-ownership-codex

## Purpose
Apply `yw-000037-010`'s claude-code fix (checkpoint ownership + tip-SHA verification before `wave-int/<N>` reuse) to the codex `ywc-parallel-executor` root as an independent hand-edit, then regenerate the `plugins/ywc-agent-toolkit` mirror from the edited codex root — never hand-editing the mirror itself.

## Scope
- `codex/skills/scripts/update-state.py`: identical FR-1 (`run_id`) and FR-2 (`wave-int-owner` / `wave-int-blocked` / `wave-int-status` subcommands) to `yw-000037-010`, applied to this independent copy.
- `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md`: identical FR-3 (5-step reuse-verification rewrite), FR-4 (origin-only materialization), FR-5 (`wave-int-owner` call sites) to `yw-000037-010`.
- `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md`: identical field/table documentation update to `yw-000037-010`.
- Plugin mirror regeneration (AC8 second half): after the above three edits are committed, run `bash scripts/sync-codex-plugin.sh` and stage its output under `plugins/ywc-agent-toolkit/skills/` — this is the correct procedure per `claude-code/skills/CLAUDE.md` §Codex-skill: Maintained Independently; the mirror is never hand-edited directly.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md` — full spec; this task implements FR-1, FR-2, FR-3, FR-4, FR-5 (codex half) and the sync-procedure half of AC8
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md#acceptance-criteria` — AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10 (codex half of each; this task owns AC8 in full since it is the only one that touches the plugin mirror)
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md#global-constraints` — plugin-mirror provenance (mirrors `codex/skills/`, not `claude-code/skills/`) and the pre-commit hook's partial coverage note
- `codex/skills/scripts/update-state.py:97-118` (`cmd_init_parallel`), `:207-215` (`cmd_hardener_verdict` shape to clone) — verified line-for-line identical to the claude-code copy
- `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md:26-32`, `:41` — verified line-for-line identical to the claude-code copy
- `codex/skills/ywc-finish-branch/SKILL.md:109` (codex's `--base-branch` reachability precondition — same rule, different line number than the claude-code copy's `:91`)
- `scripts/sync-codex-plugin.sh` — the canonical regeneration script; `tasks/completed/000001-010-infra-codex-plugin-package-layout/README.md` and sibling completed tasks are the established precedent for this sync-then-commit procedure

### Summary
This task mirrors `yw-000037-010`'s claude-code change onto the codex root, per this repository's "not auto-synced, apply deliberately to each root" convention. `codex/skills/scripts/update-state.py` and `wave-integration-branch.md` are structurally identical to their claude-code counterparts today (same line numbers, same function bodies), so the implementation steps are the same edit applied to a different file. This task additionally owns AC8's mirror-regeneration half: after committing the codex-root edit, `bash scripts/sync-codex-plugin.sh` must leave `plugins/ywc-agent-toolkit/skills/ywc-parallel-executor` byte-identical to the freshly-synced `codex/skills/ywc-parallel-executor`.

### Out of Scope (from spec)
- The claude-code root's hand-edit — `yw-000037-010`.
- The regression test file exercising both roots — `yw-000037-030`.
- Hand-editing `plugins/ywc-agent-toolkit/skills/ywc-parallel-executor` directly — always produced by `scripts/sync-codex-plugin.sh`, per spec `## Global Constraints`.
- Closing the pre-commit hook's enforcement gap (a commit staging only a plugin-path hand-edit is not caught) — spec explicitly notes this is a known, unfixed gap, not part of this spec.

## Criticality
`normal` — internal orchestration state of the parallel executor; no auth/payment/PII surface (spec's own `## Critical Surfaces` states N/A).

## Dependencies

### Depends On
- (None — parallel-safe against `yw-000037-010` since the two touch disjoint files: `codex/skills/**` vs. `claude-code/skills/**`)

### Depended By
- `yw-000037-030-test-wave-int-checkpoint-ownership-regression` — the regression test exercises this task's three subcommands and rewritten reuse procedure against the codex root, and verifies the plugin-mirror sync output.

## Key Files
- `codex/skills/scripts/update-state.py` — same handler/subparser additions as `yw-000037-010`, applied to this file.
- `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md` — same section rewrite as `yw-000037-010`.
- `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md` — same documentation update as `yw-000037-010`.
- `plugins/ywc-agent-toolkit/skills/ywc-parallel-executor/**`, `plugins/ywc-agent-toolkit/skills/scripts/update-state.py` — regenerated output only, staged via `git add -A plugins/ywc-agent-toolkit` after running the sync script.

## Notes
- Implement this task by re-reading `yw-000037-010`'s finished diff against `claude-code/skills/scripts/update-state.py` and applying the equivalent edit to `codex/skills/scripts/update-state.py` — do not re-derive the logic independently, since AC8 requires byte-for-byte-identical subcommand *behavior* (not necessarily identical file bytes, since the two files may otherwise already diverge in unrelated ways).
- Codex's `ywc-finish-branch/SKILL.md` states the same local-ref precondition at a different line number (`:109` vs. claude-code's `:91`) — this task does not edit `ywc-finish-branch` in either root (spec `## Out of Scope`), the citation is grounding only.
- Run the sync script **after** the codex-root edit is committed, matching the pre-commit hook's own documented remedy — do not run it mid-edit against a half-finished `update-state.py`.

## Parallel Execution Metadata

### Ownership
- `codex/skills/scripts/update-state.py`
- `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md`
- `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md`
- `plugins/ywc-agent-toolkit/skills/ywc-parallel-executor/**` and `plugins/ywc-agent-toolkit/skills/scripts/update-state.py` — regenerated via `scripts/sync-codex-plugin.sh` only, never hand-edited

### Owned Interface
- New `.ywc-run-state.json` top-level field: `run_id: str` (codex-root behavior, identical contract to `yw-000037-010`).
- New per-wave fields and subcommands identical to `yw-000037-010`'s Owned Interface, scoped to the codex copy.

### Shared Surfaces
- `.ywc-run-state.json` schema — must match `yw-000037-010`'s claude-code implementation byte-for-byte in subcommand behavior (AC8).
- `plugins/ywc-agent-toolkit/skills/` — build artifact of this task's `codex/skills/` edit; no other task writes to it.

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 codex/skills/scripts/update-state.py init-parallel --mode local-merge --tasks-dir tasks/ --waves '[{"wave":1,"tasks":["t-a"],"has_contract":true}]'` — confirm non-empty top-level `run_id`.
- `python3 codex/skills/scripts/update-state.py wave-int-owner 1 --tip-sha abc123` then `wave-int-status 1` — confirm output `<run_id> abc123`.
- `python3 codex/skills/scripts/update-state.py wave-int-blocked 1 --reason wave-int-branch-missing --detail "branch=wave-int/1 recorded-owner=abc recorded-tip=def"` — confirm `waves[0].status == "BLOCKED"` and `blocked_detail` matches verbatim.
- `diff <(python3 codex/skills/scripts/update-state.py --help) <(python3 claude-code/skills/scripts/update-state.py --help)` — confirm the subcommand list is identical between roots (AC8).
- `bash scripts/sync-codex-plugin.sh && git add -A plugins/ywc-agent-toolkit && git status --short plugins/ywc-agent-toolkit` — confirm no unexpected residual diff after staging (i.e., the sync output is exactly what gets committed); `diff -r codex/skills/ywc-parallel-executor plugins/ywc-agent-toolkit/skills/ywc-parallel-executor` exits 0.
- `bash scripts/validate.sh`
