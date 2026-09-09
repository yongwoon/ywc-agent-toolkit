# yw-000029-030-domain-impl-review-monitor-citation — Implementation Checklist

## Prerequisites
- [ ] `yw-000028-010-docs-subagent-async-monitoring-contract` is completed (merged) — `claude-code/skills/references/subagent-async-monitoring.md` exists

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`: `claude-code/skills/ywc-impl-review/SKILL.md` only
- [ ] If the task requires edits outside this file, stop and report before proceeding

## Stop Conditions
- [ ] Stop if line 73 no longer opens the Phase 1 5-way dispatch paragraph as described (re-verify with `rg -n "spawn five subagents in parallel" claude-code/skills/ywc-impl-review/SKILL.md`)
- [ ] Stop if line 108 no longer opens the Step 4.5 Independent Verification Pass paragraph as described (re-verify with `rg -n "Independent Verification Pass" claude-code/skills/ywc-impl-review/SKILL.md`)
- [ ] Stop if the edit would require touching the Return Payload Contract text (`SKILL.md:84-94`)

## Implementation Steps
- [ ] Append one sentence to the end of the Phase 1 dispatch paragraph (the paragraph beginning "Use the Task tool to spawn five subagents in parallel...") citing `../references/subagent-async-monitoring.md` for roster reconciliation across the 5-way concurrent dispatch
  - [ ] Do not modify the sub-bullets describing Architecture/Design/Devex/Security/QA subagents
- [ ] Append one sentence to the end of the Step 4.5 dispatch paragraph (the paragraph beginning "Independent Verification Pass — For every Confirmed finding...") citing the same reference for roster reconciliation across the up-to-20-way verifier dispatch
  - [ ] Do not modify the "Bounded dispatch payload" or "Dispatch cap" sub-bullets that follow
- [ ] Re-read the full diff and confirm the Return Payload Contract text (`SKILL.md:84-94`) and the Phase 2 Advisor Pass section are byte-for-byte unchanged

## Task Verify
- [ ] `rg -c "subagent-async-monitoring.md" claude-code/skills/ywc-impl-review/SKILL.md` — expect 2
- [ ] `rg -n "subagent-async-monitoring.md" claude-code/skills/ywc-impl-review/SKILL.md`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-impl-review --format json`

## Verification
- [ ] `bash scripts/validate.sh` still passes
- [ ] `git diff --check` reports no whitespace errors

## Implementation Notes (optional)
