# yw-000006-020-docs-executor-consumer-sync

## Purpose
Update the three worktree/execution consumer skills so their task-specifier and branch examples show the prefixed ID grammar, without changing any matching logic.

## Scope
`ywc-sequential-executor`, `ywc-parallel-executor`, and `ywc-worktrees`: SKILL.md examples plus one sentence each on prefix matching, and all six README locales per skill.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#fr5--문서로케일-동기화-ac9` — documentation sync list and the "examples and one sentence only" constraint
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#existing-constraints-touched` — grep evidence that `ywc-parallel-executor/scripts/*.sh` contains no 6-digit PHASE regex

### Summary
These three skills consume task IDs as opaque strings. Prefix matching is plain string prefix matching, so an initials segment passes through transparently — the grep sweep found zero 6-digit PHASE regexes in `ywc-parallel-executor/scripts/`, and worktree names are forwarded verbatim. The change here is therefore examples plus a single clarifying sentence per skill, with no logic edits. Branch names of the form `feature/yk-000001-010-…` are valid git refs and need no special handling.

### Out of Scope (from spec)
- Any script change in these skills — the spec explicitly enumerates them as "listed but not touched".
- `ywc-finish-branch` and `ywc-gen-testcase` — `yw-000006-030`.
- `ywc-task-generator`'s own artifacts — `yw-000006-010`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000005-020-docs-task-generator-skill-initials` — the canonical wording these examples mirror.

### Depended By
- `yw-000007-010-infra-validation-gate` — final no-regression gate.

## Key Files
- `claude-code/skills/ywc-sequential-executor/SKILL.md` + `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md`
- `claude-code/skills/ywc-parallel-executor/SKILL.md` + the same six README locales
- `claude-code/skills/ywc-worktrees/SKILL.md` + the same six README locales

## Notes
- Twenty-one files, all mechanical. Keep the diff to examples and the one added sentence per SKILL.md; resist rewriting surrounding prose.
- `ywc-sequential-executor/SKILL.md` reference points from the spec: lines 49, 174, 270. `ywc-worktrees/SKILL.md`: lines 49, 50, 53. Treat these as starting points, not an exhaustive list — re-grep before editing.
- Do not use `@skill-name` force-load references.
- Keep at least one legacy unprefixed example in each skill so readers see that both forms are accepted.

## Hardening Evidence
### Test Feedback Path
- No executable surface. Verification is a grep sweep confirming no unprefixed-only example remains as the sole illustration, plus `validate.sh` and markdownlint.

### Interface Contract
- Contract: task-specifier and branch-name examples in the three executor-family skills.
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
- `claude-code/skills/ywc-sequential-executor/SKILL.md`, `claude-code/skills/ywc-sequential-executor/README*.md`
- `claude-code/skills/ywc-parallel-executor/SKILL.md`, `claude-code/skills/ywc-parallel-executor/README*.md`
- `claude-code/skills/ywc-worktrees/SKILL.md`, `claude-code/skills/ywc-worktrees/README*.md`

### Shared Surfaces
- Task ID grammar as presented to executors
- README locale set

### Conflicts With
- (None identified — disjoint file set from `yw-000006-010` and `yw-000006-030`)

### Parallelizable After
- `yw-000005-020-docs-task-generator-skill-initials`

### Task Verify
- `bash scripts/validate.sh`
- markdownlint with the CI config over `claude-code/skills/*/README*.md`
- `git diff --name-only` lists 21 files across the three skills
- Each of the three SKILL.md files contains both a prefixed and a legacy example

## Out of Scope
- Any change under these skills' `scripts/` or `references/` directories.
- Changing prefix-matching logic.
