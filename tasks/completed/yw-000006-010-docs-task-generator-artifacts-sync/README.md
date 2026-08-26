# yw-000006-010-docs-task-generator-artifacts-sync

## Purpose
Bring `ywc-task-generator`'s own supporting artifacts — templates, execution convention, README locales, and evals — in line with the prefixed ID grammar settled in Phase `yw-000005`.

## Scope
Update `references/dependency-graph.md.template` and `references/execution-convention.md`, sync all six README locales, and add one eval scenario covering initials resolution alongside legacy coexistence.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#fr5--문서로케일-동기화-ac9` — documentation sync list
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#existing-constraints-touched` — reuse of the existing legacy-coexistence eval narration style
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#id-grammar-contract` — example ID form

### Summary
The generator's templates seed every future task set, so a stale `## Phase NNNNNN` heading in `dependency-graph.md.template` would keep producing unprefixed graphs even after the allocator is fixed. `evals/evals.json` already carries scenarios where the legacy `001010` form and the `000001-010` form coexist; the new initials scenario follows the same narration style rather than inventing a new one. All six locales are updated together — `translation-check` only warns, but a drifted locale is still a defect.

### Out of Scope (from spec)
- Consumer skills' SKILL.md and READMEs — `yw-000006-020` and `yw-000006-030`.
- `ywc-task-generator/SKILL.md` itself — completed in `yw-000005-020`.
- Regenerating the toolkit-eval baseline — `yw-000007-010`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000005-020-docs-task-generator-skill-initials` — the canonical wording these artifacts mirror.

### Depended By
- `yw-000007-010-infra-validation-gate` — final no-regression gate.

## Key Files
- `claude-code/skills/ywc-task-generator/references/dependency-graph.md.template`
- `claude-code/skills/ywc-task-generator/references/execution-convention.md`
- `claude-code/skills/ywc-task-generator/README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md`
- `claude-code/skills/ywc-task-generator/evals/evals.json`

## Notes
- The compactor keys phase groups on the full prefixed string, so the template heading must be `## Phase <initials>-NNNNNN` while remaining compatible with legacy `## Phase NNNNNN` headings already present in this repository's graph.
- `README.md` is the Korean default; `README.en.md` is the English source for generated translations. Keep them consistent in substance, not word-for-word.
- Do not use `@skill-name` force-load references.

## Hardening Evidence
### Test Feedback Path
- `evals/evals.json` must remain valid JSON and must load through whatever the existing eval runner expects; the added scenario is the RED-first artifact for initials resolution.

### Interface Contract
- Contract: the on-disk `dependency-graph.md` heading format and the task-completion move convention.
- Inputs: prefixed and legacy task IDs.
- Outputs: templates and examples that produce compactor-parsable output.
- Error model: N/A — documentation and fixtures.
- Impacted tests: `evals/evals.json`.

### Critical Surface Review
- Review requirement: N/A — spec declares no Critical Surfaces.

### Data Integrity Hardening
- Trigger surface: N/A — no shared counter written here.
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `claude-code/skills/ywc-task-generator/references/dependency-graph.md.template`
- `claude-code/skills/ywc-task-generator/references/execution-convention.md`
- `claude-code/skills/ywc-task-generator/README*.md`
- `claude-code/skills/ywc-task-generator/evals/evals.json`

### Shared Surfaces
- `dependency-graph.md` heading format
- README locale set
- Eval corpus

### Conflicts With
- (None identified — disjoint file set from `yw-000006-020` and `yw-000006-030`)

### Parallelizable After
- `yw-000005-020-docs-task-generator-skill-initials`

### Task Verify
- `python3 -m json.tool claude-code/skills/ywc-task-generator/evals/evals.json > /dev/null`
- `grep -q 'Phase <initials>-' claude-code/skills/ywc-task-generator/references/dependency-graph.md.template`
- `bash scripts/validate.sh`
- markdownlint with the CI config over `claude-code/skills/*/README*.md`

## Out of Scope
- Any change to a consumer skill.
- Rewriting this repository's existing `tasks/dependency-graph.md`.
