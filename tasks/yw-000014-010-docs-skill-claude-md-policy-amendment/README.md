# yw-000014-010-docs-skill-claude-md-policy-amendment

## Purpose

Amend `claude-code/skills/CLAUDE.md` so the lazy/scripted convention this spec establishes is
what the next authored skill inherits by default, per FR8/FR9. Without this, the next skill
author reintroduces eager unconditioned directives.

## Scope

- Four mandating sections: "Bot Review Polling Parameters" (~line 97), "PR Conflict &
  Merge-Readiness Resolution" (~line 124), "Language Resolution" (~line 390), "Task Initials
  Resolution" (~line 418) — change the required form from "read the file" to "read the file
  **on entering the branch that needs it**".
- For the Language/Initials sections specifically: make script invocation
  (`resolve-language.sh` / `resolve-initials.sh`) the canonical mechanism, with the reference
  file retained as the human-maintained source of truth (not deleted, not deprecated).
- Add both new scripts as rows in the "Bundled Execution Scripts" table (~line 296).
- Correct or remove the stale `ywc-confidence-gate/scripts/score-gate.py` row (~line 321) —
  `claude-code/skills/ywc-confidence-gate/scripts/` does not exist in this repository.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` — FR8, FR9, AC13
- `claude-code/skills/CLAUDE.md` — the file being amended

### Summary

FR8 amends the four sections' required form; FR9 adds the two new scripts to the bundled-scripts
table and fixes the stale row. `ywc-sequential-executor:78` (verified compliant by
`yw-000013-020`) is the canonical exemplar the amended Language/Initials sections should point
to as the target shape — "do not 'fix' it" is the spec's own instruction, it's already correct.

### Out of Scope (from spec)

- Any change to the SKILL.md bodies themselves — this task only edits `CLAUDE.md`.
- Deleting `references/language-resolution.md` or `references/initials-resolution.md` — both stay as the human-maintained source of truth per FR8.

## Criticality

`normal` — policy documentation change only.

## Dependencies

### Depends On

- `yw-000013-010` — the invocation pattern must be finalized before documenting it as canonical
- `yw-000013-020` — `ywc-sequential-executor:78` must be verified compliant before citing it as the exemplar

### Depended By

- `yw-000014-020` — final report quotes the amended policy for AC13 verification

## Key Files

- `claude-code/skills/CLAUDE.md`

## Notes

This is a docs-only task with no script or SKILL.md body changes — `CLAUDE.md` isn't linted by
any automated tool, so verification is manual diff review against AC13's four checkpoints, not
a single grep/test command.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/CLAUDE.md`

### Owned Interface

- (None — no public interface owned; policy prose only)

### Shared Surfaces

- (None identified — sole editor of this file in this batch)

### Conflicts With

- (None identified)

### Parallelizable After

- `yw-000013-010`, `yw-000013-020`

### Task Verify

- Manual review: each of the 4 mandating sections states "on entering the branch that needs it"; both new scripts appear in the Bundled Execution Scripts table; the stale `score-gate.py` row is corrected or removed

## Out of Scope

- Any SKILL.md body edit.
- Deleting either shared reference file.
