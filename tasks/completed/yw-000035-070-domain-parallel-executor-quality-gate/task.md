# yw-000035-070-domain-parallel-executor-quality-gate — Implementation Checklist

## Prerequisites
- [ ] `yw-000035-010-docs-quality-gate-contract-claude` is completed (merged) — `claude-code/skills/references/quality-gates.md` exists.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/ywc-parallel-executor/SKILL.md` only.

## Stop Conditions
- [ ] Stop if `claude-code/skills/references/quality-gates.md` does not exist.
- [ ] Stop if `**4c.5.` or `**4e.5.` already exists.
- [ ] Stop if the Category table already has `Cleaner`/`Hardener` columns.

## Implementation Steps
- [ ] Run `grep -n "^\*\*4[a-z]\." claude-code/skills/ywc-parallel-executor/SKILL.md` to confirm current 4c/4d/4e/4g line numbers.
- [ ] Insert `**4c.5. Cleaner (CRAP gate, per-task)**` immediately after 4c's existing content, before 4d:
  - [ ] Runs per-task, dispatching to `ywc-refactor-cleaner` via the Task tool.
  - [ ] Dispatch-failure → `DONE_WITH_CONCERNS`, never `BLOCKED`.
  - [ ] Records `gate_state` in the per-task subagent return payload — never in `.ywc-run-state.json`.
  - [ ] Links `../../references/quality-gates.md` via `> **Action required**: Read [...]`, does not restate thresholds.
  - [ ] States the `N/A — no quality gate contract` skip behavior.
- [ ] Insert `**4e.5. Hardener (Mutation gate, wave boundary)**` immediately after 4e's existing content, before 4g:
  - [ ] Runs once against the wave's merged diff, dispatching to `ywc-qa-engineer` via the Task tool.
  - [ ] Dispatch-failure → `DONE_WITH_CONCERNS`, never `BLOCKED`.
  - [ ] Records `gate_state` in the wave-level Completion Report — never in `.ywc-run-state.json`.
  - [ ] Links `../../references/quality-gates.md`, does not restate thresholds.
  - [ ] States the `N/A — no quality gate contract` skip behavior.
- [ ] Extend the Step 3 Category → `subagent_type` table (5 rows) with `Cleaner` and `Hardener` columns: both populated with `ywc-refactor-cleaner` / `ywc-qa-engineer` for every code-producing category row (`db`/`api`/`domain`/`lib`/`worker`, `ui`, `test`, `infra`, `refactor`).

## Task Verify
- [ ] `grep -n "^\*\*4c\.\|^\*\*4c\.5\.\|^\*\*4d\.\|^\*\*4e\.\|^\*\*4e\.5\.\|^\*\*4g\." claude-code/skills/ywc-parallel-executor/SKILL.md` — confirm ascending line-number order
- [ ] `grep -n "^| Category" claude-code/skills/ywc-parallel-executor/SKILL.md` then confirm header row includes `Cleaner` and `Hardener`
- [ ] `grep -q "N/A — no quality gate contract" claude-code/skills/ywc-parallel-executor/SKILL.md`

## Verification
- [ ] `bash scripts/validate.sh` exits 0
- [ ] No lint/typecheck/build/test toolchain applies to this repository.
