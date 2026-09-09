# yw-000024-020-domain-sequential-advisor-monitor — Implementation Checklist

## Prerequisites
- [ ] `yw-000023-010-docs-subagent-async-monitoring-contract` is completed and merged

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-sequential-executor/SKILL.md` and its `evals/evals.json`
- [ ] Do not change `references/advisor-escalation.md` unless a precise citation-only adjustment is required; report broader changes

## Stop Conditions
- [ ] Stop if monitoring implies a fourth advisor call or automatic redispatch
- [ ] Stop if a fallback would transfer task-state or worktree ownership from the executor
- [ ] Stop if the condition-specific table cannot preserve existing stop rules

## Hardening Gate
- [ ] Classify as critical behavior change involving bounded retryable collaboration calls
- [ ] Add RED-first advisor-unavailable eval evidence
- [ ] Record the advisor monitor/fallback contract before changing prose
- [ ] Apply the shared data-integrity fields for one-slot/one-escalation behavior
- [ ] Require `ywc-impl-review` before `DONE`

## Implementation Steps
- [ ] Add a citation to the shared monitoring reference at the successful advisor dispatch boundary.
- [ ] Add the owner-specific fallback table for spec conflict, ambiguous verification failure, borderline stop condition, and Pattern C plan review.
- [ ] Preserve the existing three-call advisor budget, delivery ownership, stop rules, and no-background-implementation boundary.
- [ ] Add eval coverage proving unavailable fallback, no auto-redispatch, and no lifecycle mutation.

## Task Verify
- [ ] `node -e 'JSON.parse(require("fs").readFileSync("codex/skills/ywc-sequential-executor/evals/evals.json", "utf8"))'`
- [ ] `python3 codex/skills/ywc-sequential-executor/scripts/test-transition-safety.py`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification
- [ ] Repository validation passes (`bash scripts/validate.sh`)
- [ ] `git diff --check` passes

## Implementation Notes (optional)
