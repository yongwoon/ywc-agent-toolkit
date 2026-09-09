# yw-000030-010-infra-async-monitoring-validation — Implementation Checklist

## Prerequisites
- [ ] `yw-000028-010-docs-subagent-async-monitoring-contract` is completed (merged)
- [ ] `yw-000029-010-domain-parallel-executor-monitor-gate` is completed (merged)
- [ ] `yw-000029-020-domain-sequential-executor-advisor-monitor` is completed (merged)
- [ ] `yw-000029-030-domain-impl-review-monitor-citation` is completed (merged)

## Allowed Edit Scope
- [ ] No manual source edits — this task only runs verification commands and lets `score.py --ci` regenerate `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- [ ] If any verification step reveals a defect in an upstream task's edit, stop and report which task/file needs a fix rather than patching it here

## Stop Conditions
- [ ] Stop if `bash scripts/validate.sh` reports any new `ERROR` line
- [ ] Stop if `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` reports a regression on `ywc-parallel-executor`, `ywc-sequential-executor`, or `ywc-impl-review`'s S2/S4 axes versus the pre-batch baseline
- [ ] Stop if `wc -l claude-code/skills/ywc-sequential-executor/SKILL.md` is not exactly 502
- [ ] Stop if any of the required citation/registration `rg` checks below return no match

## Implementation Steps
- [ ] Run `bash scripts/validate.sh` and confirm it exits 0 with no new errors for the four touched skills (`ywc-parallel-executor`, `ywc-sequential-executor`, `ywc-impl-review`, and the `references/` addition under the skills tree)
- [ ] Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` and confirm no regression is reported for `ywc-parallel-executor`, `ywc-sequential-executor`, or `ywc-impl-review` on S2 (structure) or S4 (token economy); this call regenerates `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` as its expected side effect
- [ ] Run `wc -l claude-code/skills/ywc-sequential-executor/SKILL.md` and confirm the result is exactly 502
- [ ] Run `rg -n "Unique Dispatch Labeling|Full-Roster Reconciliation|Mandatory Fallback Wakeup|Bounded Escalation on Stall|Known Limitations" claude-code/skills/references/subagent-async-monitoring.md` and confirm all four section names plus the Known Limitations note are present
- [ ] Run `rg -c "subagent-async-monitoring.md" claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-impl-review/SKILL.md` and confirm each file has at least one citation (`ywc-impl-review/SKILL.md` should show 2)
- [ ] Run `rg -n "## Subagent Async Monitoring Contract" claude-code/skills/CLAUDE.md` and confirm the new section exists
- [ ] Run `git diff --check` and confirm no whitespace errors were introduced across the batch (in particular the blank-line trim in `yw-000029-020`)
- [ ] Summarize AC1–AC7 status against the spec in the completion report — each of the seven should now be satisfied

## Task Verify
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `wc -l claude-code/skills/ywc-sequential-executor/SKILL.md`
- [ ] `rg -c "subagent-async-monitoring.md" claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-impl-review/SKILL.md`
- [ ] `rg -n "## Subagent Async Monitoring Contract" claude-code/skills/CLAUDE.md`
- [ ] `git diff --check`

## Verification
- [ ] `bash scripts/validate.sh` passes with no new errors
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` reports no regression
- [ ] `git diff --check` reports no whitespace errors

## Implementation Notes (optional)
