# yw-000004-010-docs-initials-resolution-reference

## Purpose
Establish the single canonical source for collaborator-initials resolution and register it in the shared-reference registry, so every consumer quotes one contract instead of restating it.

## Scope
Create `claude-code/skills/references/initials-resolution.md` isomorphic to `language-resolution.md`, and add a `## Task Initials Resolution` registry section to `claude-code/skills/CLAUDE.md`.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#fr1--referencesinitials-resolutionmd-신설-ac1` — reference content contract
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#a1--fr5에-공유-reference-레지스트리-추가-critical-1-대응` — registry requirement
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#id-grammar-contract` — `[INITIALS]-[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]`

### Summary
Task IDs gain an `INITIALS` segment (`^[a-z0-9]{2,4}$`) that namespaces the PHASE counter per collaborator, making concurrent-allocation collisions structurally impossible. The resolution procedure — `--initials` flag, then the project `CLAUDE.md ## Task Initials` section, then derivation from `git config user.email` with a one-time confirmation and caching — is defined once in this reference and only quoted elsewhere. Persistence location is a deliberate divergence from the sibling Codex spec (`CLAUDE.md` here, `.codex/ywc.json` there); the grammar itself is owned by this spec and must not fork.

### Out of Scope (from spec)
- Numbering-scan implementation — handled by `yw-000005-010-infra-next-task-number-initials-scan`.
- SKILL.md wiring of the reference — handled by `yw-000005-020-docs-task-generator-skill-initials`.
- Parser regex changes — handled by `yw-000004-020-infra-parser-optional-initials-prefix`.

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)

### Depended By
- `yw-000005-010-infra-next-task-number-initials-scan` — implements the numbering-scope rules defined here.
- `yw-000005-020-docs-task-generator-skill-initials` — cites this reference by `> **Action required**: Read [...]` directive.
- `yw-000006-010-docs-task-generator-artifacts-sync` — templates reuse the canonical section format.

## Key Files
- `claude-code/skills/references/initials-resolution.md` (new)
- `claude-code/skills/CLAUDE.md` (registry section, near the existing `## Language Resolution` block)

## Notes
- `.ywc-config.json` and `ywc-setup/scripts/write-config.sh` do not exist in this tree (grep: 0 hits). Do not port PR #217's config-file mechanism; persist to `CLAUDE.md ## Task Initials` instead.
- Caching is create-or-**replace**, never append — a second `## Task Initials` heading makes the next read ambiguous.
- The derivation edge cases (no git identity, non-ASCII name, `>4` chars, duplicate initials across people) are part of this reference, not of the consuming skill.

## Hardening Evidence
### Test Feedback Path
- No executable surface. Verification is structural: heading count, regex comment presence, and registry cross-link resolution.

### Interface Contract
- Contract: the precedence chain, the derivation algorithm, the `^[a-z0-9]{2,4}$` validation rule, and the canonical `## Task Initials` section format.
- Inputs: `--initials` flag value, project `CLAUDE.md`, `git config user.email` / `user.name`.
- Outputs: a resolved initials string, plus a cached canonical section.
- Error model: no-block invariant — absence of `## Task Initials` never blocks, delays, or errors a consuming skill.
- Impacted tests: N/A — documentation contract.

### Critical Surface Review
- Review requirement: N/A — spec declares no Critical Surfaces.

### Data Integrity Hardening
- Trigger surface: N/A — no shared mutable counter is written by this task.
- Atomic / locking strategy: N/A — reservation lives in `yw-000005-010`.
- Transaction boundary: N/A
- Idempotency guard: create-or-replace of the canonical section is idempotent across re-runs.
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `claude-code/skills/references/initials-resolution.md`
- `claude-code/skills/CLAUDE.md` (new registry section only — do not restructure existing sections)

### Shared Surfaces
- Shared-reference registry in `claude-code/skills/CLAUDE.md`
- Task ID grammar contract (owned by this spec, referenced by the Codex tree)

### Conflicts With
- (None identified)

### Parallelizable After
- (None — root task; runs against the merged `main` baseline)

### Task Verify
- `test "$(grep -c '^## Task Initials Resolution' claude-code/skills/CLAUDE.md)" = 1`
- `test -f claude-code/skills/references/initials-resolution.md`
- `grep -q 'No-block invariant' claude-code/skills/CLAUDE.md`
- `bash scripts/validate.sh`

## Out of Scope
- Any script or SKILL.md change.
- Migrating the repository's own legacy unprefixed task IDs (spec §A7 closed this as "do not migrate").
