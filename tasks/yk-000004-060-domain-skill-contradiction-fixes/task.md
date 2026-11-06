# yk-000004-060-domain-skill-contradiction-fixes — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-task-generator/SKILL.md`
  - `claude-code/skills/ywc-changelog-release-notes/**`
  - `claude-code/skills/ywc-code-gen/SKILL.md`
  - `claude-code/skills/ywc-refactor-clean/SKILL.md`
  - `claude-code/skills/ywc-security-audit/**`
  - `claude-code/skills/ywc-spec-validate/SKILL.md`
  - `claude-code/skills/ywc-infra-review/SKILL.md`
  - `claude-code/skills/ywc-iac-author/SKILL.md`
  - `claude-code/skills/ywc-verify-done/SKILL.md`
  - `claude-code/skills/ywc-skill-author/references/skill-template.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **A2 — Model Hint column**
  - [ ] Edit `ywc-task-generator/SKILL.md:450` per `${TMPDIR:-/tmp}/ywc-issue69-snapshot/.../output-and-validation.md` wording (local text lives inline, not in a reference)
- [ ] **Changelog, code-gen, refactor-clean**
  - [ ] Apply the changelog `Omitted:` / `[Unreleased]` rules and README table update (4 Tier 1 READMEs where the table exists)
  - [ ] Apply the code-gen `NEEDS_CONTEXT` / '0 → 7.5' text and the refactor-clean clean-tree / `git checkout -- <files>` / Status edits
- [ ] **Security-audit, spec-validate**
  - [ ] Correct the prompt-injection severity sentence (`checklist:11`, `:109`) and the Phase 1 parallel description
  - [ ] Restrict the spec-validate Status table to 'Pre-gate status' and point gate status at the Band-to-status table
- [ ] **Infra-review, iac-author**
  - [ ] Add `--scope` apply-history evidence + `Scope evidence:` output line; make the reviewer read inline
  - [ ] Add the per-module dispatch anti-trigger to iac-author
- [ ] **verify-done and skill template**
  - [ ] Remove the `requires: []` line only; change the template description to a `>-` block scalar and keep `requires:` placeholder

## Acceptance Coverage
Covers: AC3, AC8b

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep 'Task list summary' claude-code/skills/ywc-task-generator/SKILL.md | grep -q 'Model Hint'`
- [ ] `grep -q 'Omitted:' claude-code/skills/ywc-changelog-release-notes/SKILL.md`
- [ ] `grep -q 'REVIEW band' claude-code/skills/ywc-code-gen/SKILL.md`
- [ ] `grep -q 'Pre-gate status' claude-code/skills/ywc-spec-validate/SKILL.md`
- [ ] `grep -q 'Scope evidence:' claude-code/skills/ywc-infra-review/SKILL.md`
- [ ] `grep -q 'ywc-infra-engineer' claude-code/skills/ywc-iac-author/SKILL.md`
- [ ] `[ "$(grep -c -- '^requires:' claude-code/skills/ywc-verify-done/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-changelog-release-notes/SKILL.md claude-code/skills/ywc-code-gen/SKILL.md claude-code/skills/ywc-refactor-clean/SKILL.md claude-code/skills/ywc-security-audit/SKILL.md claude-code/skills/ywc-spec-validate/SKILL.md claude-code/skills/ywc-infra-review/SKILL.md claude-code/skills/ywc-iac-author/SKILL.md claude-code/skills/ywc-verify-done/SKILL.md`
- [ ] Review-only: quote before/after for refactor-clean step 0 and the security-audit severity rule in Implementation Notes
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

- **refactor-clean step 0 (added)** — before: loop started at `1. Run the test suite…`; step 4 red path: "`git revert <commit>` (after the commit lands)… Use `git checkout -- <file>` only for the pre-commit state". After: clean-tree precondition paragraph + `0. Require clean target files` (`git status --porcelain -- <files>`; dirty → skip item, `NEEDS_CONTEXT`); step 4 red: "nothing is committed yet, so discard the uncommitted deletion with `git checkout -- <files>` (only the files step 0 verified clean…). Reserve `git revert <commit>` for a regression discovered after the commit has landed". Output template gains `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`. Anti-pattern bullet re-worded ("…after a commit has landed, or for one file of a multi-file deletion") so it no longer contradicts step 4.
- **security-audit severity rule** — before (`prompt-injection-checklist.md:11`): "If the surface is internal-only, downgrade to High; never below High when user input touches a prompt." After: "Adjust severity only by the condition stated in the item's own row of the Severity Reference below — a surface being internal-only does not by itself lower any item, and item 2 is never downgraded. Never below High when user input touches a prompt, except where an item's own row names a lower downgrade." Row `:109` (item 1: "Downgrade to High only if surface is internal-only and audited") is unchanged and is now the only internal-only rule. SKILL.md Phase 1 cluster table: OWASP `A01..A10` labels (which mis-numbered the Top 10) replaced by category names, matching the real 3-cluster parallel structure.
- **ywc-code-gen** — local Step numbering already ends at Step 8 (`0 → 8`), so the upstream "0 → 7.5" text was NOT ported; local Confidence Gate maps REVIEW → DONE_WITH_CONCERNS, while the `NEEDS_CONTEXT` REVIEW band lives in `ywc-impl-review`'s mapping, so the new permitted-stop line refers to a REVIEW band / `--review` result returned by the Step 8 reviews.
- **ywc-infra-review** — local skill has no `ywc-infra-reviewer` dispatch (3-lens fan-out; Write-less lenses already return inline), so the "read reviewer results inline" sentence was dropped (FR3). `--scope` evidence check and `Scope evidence:` line ported.
- **ywc-iac-author** — `ywc-infra-engineer` is not in this repo's `claude-code/agents/`, but the spec and AC8b name it explicitly, so it is added to the description anti-triggers as specified.
- **Review fixes** — changelog anti-pattern row now says refactor/chore are omitted from CHANGELOG too (logged as `Omitted:` in run summary); `ywc-security-audit/README.md` cluster table uses SKILL.md category names instead of A01–A10. `README.zh.md` / `README.es.md` (Tier 2, generated) intentionally NOT edited — out of scope; they still carry the A01–A10 labels until regenerated. infra-review `--scope` BLOCKED trigger clarified ("gives none" alone suffices).
