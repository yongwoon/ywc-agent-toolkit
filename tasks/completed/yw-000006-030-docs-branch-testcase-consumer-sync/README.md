# yw-000006-030-docs-branch-testcase-consumer-sync

## Purpose
Update the two remaining consumer skills — `ywc-finish-branch` and `ywc-gen-testcase` — so their task-ID examples reflect the prefixed grammar.

## Scope
SKILL.md examples plus one prefix-matching sentence for each skill, and all six README locales per skill.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#fr5--문서로케일-동기화-ac9` — documentation sync list
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#existing-constraints-touched` — `ywc-gen-testcase/SKILL.md:53,360` as reference points

### Summary
`ywc-finish-branch` consumes task IDs for PR titles and for the Mark Task Complete move; its parser was already widened in `yw-000004-020`, so only its prose needs updating. `ywc-gen-testcase` references task IDs purely as identifiers. Both changes are examples plus one clarifying sentence, with no logic edits, and each skill keeps one legacy example so readers see that both forms are accepted.

### Out of Scope (from spec)
- `build-pr-title.py` — already changed in `yw-000004-020-infra-parser-optional-initials-prefix`.
- The three executor-family skills — `yw-000006-020`.
- `ywc-task-generator`'s own artifacts — `yw-000006-010`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000005-020-docs-task-generator-skill-initials` — the canonical wording these examples mirror.

### Depended By
- `yw-000007-010-infra-validation-gate` — final no-regression gate.

## Key Files
- `claude-code/skills/ywc-finish-branch/SKILL.md` + `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md`
- `claude-code/skills/ywc-gen-testcase/SKILL.md` + the same six README locales

## Notes
- Fourteen files, all mechanical. Keep the diff to examples and the one added sentence per SKILL.md.
- `ywc-finish-branch/scripts/build-pr-title.py` is owned by `yw-000004-020` and must not be edited here.
- Do not use `@skill-name` force-load references.

## Hardening Evidence
### Test Feedback Path
- No executable surface. Verification is a grep sweep plus `validate.sh` and markdownlint.

### Interface Contract
- Contract: task-ID examples and PR-title prefix examples in the two skills.
- Inputs: prefixed and legacy task IDs.
- Outputs: documentation only; no behavioral change.
- Error model: N/A
- Impacted tests: N/A — covered by the toolkit-eval gate in `yw-000007-010`.

### Critical Surface Review
- Review requirement: N/A — spec declares no Critical Surfaces.

### Data Integrity Hardening
- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `claude-code/skills/ywc-finish-branch/SKILL.md`, `claude-code/skills/ywc-finish-branch/README*.md`
- `claude-code/skills/ywc-gen-testcase/SKILL.md`, `claude-code/skills/ywc-gen-testcase/README*.md`

### Shared Surfaces
- PR title prefix format as documented
- README locale set

### Conflicts With
- `yw-000004-020-infra-parser-optional-initials-prefix` — shares the `ywc-finish-branch` directory; that task owns `scripts/build-pr-title.py`, this one owns the markdown. The dependency ordering already separates them, but never edit the script from this task.

### Parallelizable After
- `yw-000005-020-docs-task-generator-skill-initials`

### Task Verify
- `bash scripts/validate.sh`
- markdownlint with the CI config over `claude-code/skills/*/README*.md`
- `git diff --name-only` lists 14 files across the two skills, with no `.py` file
- Each SKILL.md contains both a prefixed and a legacy example

## Out of Scope
- Any change under these skills' `scripts/` or `references/` directories.
