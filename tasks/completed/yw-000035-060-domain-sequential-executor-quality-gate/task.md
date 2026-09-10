# yw-000035-060-domain-sequential-executor-quality-gate — Implementation Checklist

## Prerequisites
- [ ] `yw-000035-010-docs-quality-gate-contract-claude` is completed (merged) — `claude-code/skills/references/quality-gates.md` exists.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/ywc-sequential-executor/SKILL.md` and `claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md` only.

## Stop Conditions
- [ ] Stop if `claude-code/skills/references/quality-gates.md` does not exist (dependency not actually merged).
- [ ] Stop if `### Step 3.5` or `### Step 3.6` already exists.
- [ ] Stop if `### Step 3: Implementation` or `### Step 4: Task Verification` headings are missing (insertion anchors gone).

## Implementation Steps
- [ ] Run `grep -n "^### Step 3: Implementation\|^### Step 4: Task Verification" claude-code/skills/ywc-sequential-executor/SKILL.md` to confirm exact current line numbers.
- [ ] Insert `### Step 3.5: Cleaner (CRAP gate)` after Step 3's content (after the Ownership-scope Gate paragraph), before `### Step 4: Task Verification`:
  - [ ] Dispatch to `ywc-refactor-cleaner` via the Task tool, as a separate dispatch from the Step 3 implementer.
  - [ ] Point to `references/quality-gate-steps.md` for the full procedure.
  - [ ] State the `N/A — no quality gate contract` skip behavior.
- [ ] Insert `### Step 3.6: Hardener (Mutation gate)` immediately after Step 3.5, before `### Step 4: Task Verification`:
  - [ ] Dispatch to `ywc-qa-engineer` via the Task tool.
  - [ ] Point to `references/quality-gate-steps.md` for the 3-round loop cap and survivor-forwarding procedure.
  - [ ] State the `N/A — no quality gate contract` skip behavior.
- [ ] Create `claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md`:
  - [ ] Open with `> **Action required**: Read [../../references/quality-gates.md]` — do not restate thresholds inline.
  - [ ] Document the ordering: Cleaner (Step 3.5) runs first; Hardener (Step 3.6) runs only if Cleaner does not return a blocking result.
  - [ ] Document the 3-round Mutation loop cap; remaining survivors after round 3 forward unchanged to Step 4.5 (Implementation Review).
  - [ ] Document dispatch-failure handling: routes to `DONE_WITH_CONCERNS`, never `BLOCKED`; records `gate_state: "not run — dispatch failed"`.
  - [ ] Add a `## Rationalization Defense` table with at least: Excuse "CRAP gate says a function is logically one unit" / Reality "decomposition or a registered exclusion-list entry are the only two paths past the gate."

## Task Verify
- [ ] `grep -n "^### Step 3: Implementation\|^### Step 3.5: Cleaner\|^### Step 3.6: Hardener\|^### Step 4: Task Verification" claude-code/skills/ywc-sequential-executor/SKILL.md` — confirm ascending line-number order
- [ ] `test -f claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md`
- [ ] `grep -q "Action required" claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md`
- [ ] `grep -q "Rationalization Defense" claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md`
- [ ] `grep -q "N/A — no quality gate contract" claude-code/skills/ywc-sequential-executor/SKILL.md`

## Verification
- [ ] `bash scripts/validate.sh` exits 0
- [ ] No lint/typecheck/build/test toolchain applies to this repository.
