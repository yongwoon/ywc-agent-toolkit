# yw-000029-020-domain-sequential-executor-advisor-monitor — Implementation Checklist

## Prerequisites
- [ ] `yw-000028-010-docs-subagent-async-monitoring-contract` is completed (merged) — `claude-code/skills/references/subagent-async-monitoring.md` exists

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`: `claude-code/skills/ywc-sequential-executor/SKILL.md` only
- [ ] If the task requires edits outside this file, stop and report before proceeding

## Stop Conditions
- [ ] Stop if `wc -l claude-code/skills/ywc-sequential-executor/SKILL.md` does not read 502 before starting (the spec's line-budget arithmetic assumes this exact starting point)
- [ ] Stop if the Rationalization Defense table no longer has exactly 21 data rows at lines 19-39 (re-verify with a fresh read before editing)
- [ ] Stop if line 213 no longer ends the Advisor Escalation Policy paragraph as described (re-verify with `rg -n "Advisor Escalation Policy" -A 5 claude-code/skills/ywc-sequential-executor/SKILL.md`)

## Implementation Steps
- [ ] Add one new Rationalization Defense row (append after the existing 21st row, before the table ends) in the existing Excuse/Reality format:
  - [ ] Excuse: "Task is slow, I'll fork a background agent to check on something while I wait"
  - [ ] Reality: point at `../references/subagent-async-monitoring.md`'s Unique Dispatch Labeling / Full-Roster Reconciliation requirements, and note this skill's Pattern A bounded-Opus-dispatch model (`../references/advisor-pattern.md`) does not admit ad-hoc concurrent forks
- [ ] Append one sentence to the end of the existing Advisor Escalation Policy paragraph at line 213, cross-referencing `../references/subagent-async-monitoring.md` for the bounded single Opus advisor dispatch:
  - [ ] The sentence must extend the existing paragraph text with **no new line break** — do not create a new paragraph or a new line
- [ ] Remove the single blank line at lines 483-485 (the blank line immediately after the closing ` ``` ` fence of the state-cleanup verification code block, before "If the verification line prints `WARNING`..."):
  - [ ] Do not touch any other line in that code block or the following sentence
  - [ ] Do not touch the Rationalization Defense table as a trim source — its 21 (now 22) rows are each a distinct, incident-specific guardrail
- [ ] Run `wc -l claude-code/skills/ywc-sequential-executor/SKILL.md` and confirm the result is exactly 502 (net zero growth: +1 new row, +0 inline append, −1 blank-line removal)

## Task Verify
- [ ] `wc -l claude-code/skills/ywc-sequential-executor/SKILL.md` — expect exactly 502
- [ ] `rg -n "subagent-async-monitoring.md" claude-code/skills/ywc-sequential-executor/SKILL.md`
- [ ] `rg -n "fork a background agent" claude-code/skills/ywc-sequential-executor/SKILL.md`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-sequential-executor --format json`

## Verification
- [ ] `bash scripts/validate.sh` still passes
- [ ] `git diff --check` reports no whitespace errors

## Implementation Notes (optional)
