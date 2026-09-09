# yw-000030-010-infra-async-monitoring-validation

## Purpose
Final validation gate confirming the Subagent Async Monitoring Contract port introduces no mechanical regression across the four touched files and that the required citations/registrations are actually present.

## Scope
Run the repository's skill-structure validator and the mechanical scorer's CI regression gate against the touched skills, verify the exact line-count invariant on `ywc-sequential-executor`, and confirm each required citation/registration point exists via targeted search. No new source prose is written beyond what the CI regen produces in `history.mechanical.json`.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#acceptance-criteria` — AC1–AC7 (final confirmation of all seven)
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#non-functional-requirements` — "every touched file must continue to pass `bash scripts/validate.sh`"
- `.claude/skills/ywc-toolkit-eval/scripts/score.py:381,393` — `A8_body_cap` (S2 structure) and S4 token-economy gates this task re-runs

### Summary
AC7 requires `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` (or the equivalent `bash scripts/validate.sh` check) to report no new regression on the touched skills' mechanical scores after the four prior tasks land. This task is the single hard gate that runs both checks once, after all four upstream edits are merged, and regenerates the `--ci` regression baseline (`history.mechanical.json`) atomically with the confirmation — mirroring the "regen and confirmation land in the same commit" pattern used by prior batches in this repository (e.g. Batch 2's `000009-010`).

### Out of Scope (from spec)
- Any new source prose in `claude-code/skills/references/subagent-async-monitoring.md`, `ywc-parallel-executor/SKILL.md`, `ywc-sequential-executor/SKILL.md`, `ywc-impl-review/SKILL.md`, or `CLAUDE.md` — those are owned by the four upstream tasks and must already be correct entering this task
- `codex/skills/` and generated plugin package files — out of scope for the whole spec

## Criticality
normal — verification-only task; no auth, payment, crypto, PII, or external-input-handling code path.

## Dependencies

### Depends On
- `yw-000028-010-docs-subagent-async-monitoring-contract` — reference file + CLAUDE.md registration must exist
- `yw-000029-010-domain-parallel-executor-monitor-gate` — `4b-monitor` gate + Status Routing row must exist
- `yw-000029-020-domain-sequential-executor-advisor-monitor` — RD row + Advisor citation + line-count invariant must hold
- `yw-000029-030-domain-impl-review-monitor-citation` — Phase 1 + Step 4.5 citations must exist

### Depended By
- (None — final task in the batch)

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — regenerated regression baseline (side effect of `score.py --ci`, no manual edits)

## Notes
- If `score.py --ci` reports a regression on any of the three touched skills' S2/S4 axes, **stop and report** which axis/skill regressed — do not silently accept the new baseline by re-running `--ci` a second time to overwrite it.
- The `wc -l` check on `ywc-sequential-executor/SKILL.md` is the single authoritative confirmation of AC3's "no net growth" requirement — a passing `score.py` alone (`body_lines <= 500`) is necessary but not sufficient, since the spec's own ≤502-line cap is one line tighter in effect than the mechanical gate.
- This task performs no plugin/package sync — `claude-code/skills/**` has no generated-package mirror analogous to `sync-codex-plugin.sh` (confirmed: `plugins/ywc-agent-toolkit/skills/` mirrors only Codex sources).

## Parallel Execution Metadata

### Ownership
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (regenerated baseline only, via `score.py --ci`)

### Owned Interface
- (None)

### Shared Surfaces
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — shared regression baseline; only this task's `--ci` run touches it in this batch

### Conflicts With
- All three Phase `yw-000029` tasks (this task must not run until they have all merged)

### Parallelizable After
- `yw-000029-010-domain-parallel-executor-monitor-gate`, `yw-000029-020-domain-sequential-executor-advisor-monitor`, `yw-000029-030-domain-impl-review-monitor-citation` (all three must be merged)

### Task Verify
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `wc -l claude-code/skills/ywc-sequential-executor/SKILL.md`
- `rg -n "Unique Dispatch Labeling|Full-Roster Reconciliation|Mandatory Fallback Wakeup|Bounded Escalation on Stall|Known Limitations" claude-code/skills/references/subagent-async-monitoring.md`
- `rg -c "subagent-async-monitoring.md" claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-impl-review/SKILL.md`
- `rg -n "## Subagent Async Monitoring Contract" claude-code/skills/CLAUDE.md`
- `git diff --check`

## Out of Scope
- Any edit to the four upstream tasks' owned files beyond what `score.py --ci` writes to `history.mechanical.json`.
- `codex/skills/` and generated plugin package files.
