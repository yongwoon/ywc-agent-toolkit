# yw-000035-020-domain-quality-gate-spec-template — Implementation Checklist

## Prerequisites
- [ ] None — root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/ywc-plan/references/spec-template.md` only.
- [ ] If any other file needs to change, stop and report before proceeding.

## Stop Conditions
- [ ] Stop if `## Quality Gate Contract` or `## Module Boundaries` already exists in the file at task start (re-verify with `grep -n "^## "`).
- [ ] Stop if `## Existing Constraints Touched` or `## Acceptance Criteria` headings are missing (the insertion anchor no longer exists).

## Implementation Steps
- [ ] Run `grep -n "^## " claude-code/skills/ywc-plan/references/spec-template.md` to confirm current heading order and exact line numbers before editing.
- [ ] Insert `## Quality Gate Contract` immediately after the `## Existing Constraints Touched` section's content, before `## Acceptance Criteria`:
  - [ ] Body states: per spec, either concrete CRAP Complexity (6–8) / Mutation Score (≥90%) thresholds this spec's tasks must meet, or the literal sentinel `N/A — no quality gate contract`.
  - [ ] Include an `> **Action required**: Read [../../references/quality-gates.md]` pointer — do not restate thresholds inline.
- [ ] Insert `## Module Boundaries` immediately after `## Quality Gate Contract`, before `## Acceptance Criteria`:
  - [ ] Body states: the new module's public interface and forbidden edges, or the literal sentinel `N/A — no code module introduced`.
- [ ] Apply the identical two-section insertion to the **second occurrence** of the template if the file contains a duplicated "Worked Example" copy of the same headings (the file has two `## Existing Constraints Touched`-style blocks per the earlier grep — verify whether the second occurrence at the bottom "Worked Example" section needs the same two headings for consistency, or leave it if it is illustrative-only and not meant to be exhaustive; document the decision taken).

## Task Verify
- [ ] `grep -n "^## Quality Gate Contract" claude-code/skills/ywc-plan/references/spec-template.md`
- [ ] `grep -n "^## Module Boundaries" claude-code/skills/ywc-plan/references/spec-template.md`
- [ ] `grep -q "Action required" claude-code/skills/ywc-plan/references/spec-template.md`
- [ ] Line-number check: `## Existing Constraints Touched` < `## Quality Gate Contract` < `## Module Boundaries` < `## Acceptance Criteria`

## Verification
- [ ] `bash scripts/validate.sh` exits 0
- [ ] No lint/typecheck/build/test toolchain applies to this repository.
