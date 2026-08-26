# 000027-010-refactor-plan-pr-spec-contracts — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] Working tree changes outside this task's Ownership are reviewed and left untouched.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-plan/**`, `codex/skills/ywc-create-pr/**`, and `codex/skills/ywc-spec-validate/**`.
- [ ] Do not edit generated plugin package.

## Stop Conditions
- [ ] Stop if `ywc-spec-validate --advisor-budget` appears to need replacement rather than extension.
- [ ] Stop if README locale updates require a translation workflow beyond concise semantic edits.
- [ ] Stop if implementing `--tasks` requires changing an executable parser or schema not described in the spec.

## Implementation Steps
- [ ] Update `codex/skills/ywc-plan/SKILL.md`.
  - [ ] Replace the Medium/Large handoff with `Spec drafted: <path>` and an explicit prompt to run `ywc-spec-ready <path>`.
  - [ ] Document the no/skip/non-interactive path as manual `ywc-spec-validate --spec <path>` -> `ywc-task-generator <path>` -> executor.
  - [ ] Adjust validation checklist so downstream execution is allowed only for user-approved `ywc-spec-ready`.
- [ ] Update `codex/skills/ywc-plan/README*.md`.
  - [ ] Add `ywc-spec-ready` to related skills or workflow summaries where present.
  - [ ] Remove wording that implies all downstream execution is prohibited after spec drafting.
- [ ] Update `codex/skills/ywc-create-pr/SKILL.md`.
  - [ ] Add a Rationalization Defense row for author diff review.
  - [ ] Insert Step 6.5 after push and before PR creation requiring `git diff <base-branch>...HEAD`.
  - [ ] List rejection checks for scope creep, debug residue, drive-by edits, secrets, and convention mismatch.
- [ ] Update `codex/skills/ywc-spec-validate/SKILL.md`.
  - [ ] Add `--tasks <dir>` to Arguments without changing existing `--advisor-budget`.
  - [ ] Add Step 4c Cross-Artifact Consistency with Requirement Coverage and Task Provenance tables.
  - [ ] Route UNCOVERED rows to Completeness Critical findings and ORPHAN/dependency-order rows to Consistency findings.
  - [ ] Correct Confidence Gate mapping for `PROCEED` with and without Critical findings.
  - [ ] Change report header vocabulary to `Critical/Warning/Suggestion`.

## Task Verify
- [ ] `rg -n "ywc-spec-ready|auto-converge|자동 수렴|Did not auto-execute" codex/skills/ywc-plan`
- [ ] `rg -n "Author Self-Review Gate|git diff <base-branch>\\.\\.\\.HEAD|does not replace independent" codex/skills/ywc-create-pr`
- [ ] `rg -n -- "--tasks <dir>|Cross-Artifact Consistency|Requirement Coverage|Task Provenance|UNCOVERED|ORPHAN" codex/skills/ywc-spec-validate`
- [ ] `rg -n "Critical/Warning/Suggestion|DONE_WITH_CONCERNS" codex/skills/ywc-spec-validate/SKILL.md`

## Verification
- [ ] Repository validation is deferred to `000028-010-infra-plugin-sync-validation`.
- [ ] `git diff --name-only` for this task contains no `claude-code/**` or `tools/codex-skill/**` paths.
