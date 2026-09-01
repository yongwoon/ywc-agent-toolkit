# yw-000013-010-docs-consumer-script-invocation

## Purpose

Wire the two new scripts into their consumers, replacing the eager `**Action required**:
Read [references/language-resolution.md]` / `[references/initials-resolution.md]` directives
with a script invocation, per FR5/FR6.

## Scope

Replace the directive in exactly these 7 locations (6 skills, `ywc-task-generator` counted once
for both of its directives):

- `claude-code/skills/ywc-auth-implement/SKILL.md:50`
- `claude-code/skills/ywc-commit/SKILL.md:135`
- `claude-code/skills/ywc-create-pr/SKILL.md:56`
- `claude-code/skills/ywc-setup-language/SKILL.md:24` — also wires `--emit-section` (Edge Case E9: this consumer *writes* the canonical section, so FR2 and FR5 ship together here)
- `claude-code/skills/ywc-spec-writer/SKILL.md:92`
- `claude-code/skills/ywc-task-generator/SKILL.md:48` (language) and `:114` (initials)

Each replacement block is ≤3 lines: the invocation
`bash claude-code/skills/scripts/resolve-language.sh` (or the initials equivalent), the meaning
of each possible return value, and a conditional pointer back to the reference for section-format
details — never a restatement of the precedence chain or code list (single-source-of-truth rule
still applies).

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` — FR5 (as amended by Iteration 1 A1.3), FR6, AC6, AC16

### Summary

FR5 (amended) fixes the invocation string to exactly
`bash claude-code/skills/scripts/resolve-language.sh` across all 6 consumers — AC16 verifies
this with `grep -rho 'bash claude-code/skills/scripts/resolve-language\.sh'
claude-code/skills/*/SKILL.md | sort -u | wc -l` returning 1. FR6 does the same for
`ywc-task-generator`'s initials directive, keeping the human confirmation prompt in the skill
body since the script only emits `NEEDS_CONFIRM`, never confirms or caches itself.

### Out of Scope (from spec)

- The remaining 17 non-language/non-initials directives — handled by `yw-000013-020`.
- The scripts themselves — handled by `yw-000012-020`/`yw-000012-030`.

## Criticality

`normal` — documentation/instruction-text change only.

## Dependencies

### Depends On

- `yw-000012-020` — `resolve-language.sh` (incl. `--emit-section`) must exist
- `yw-000012-030` — `resolve-initials.sh` must exist

### Depended By

- `yw-000014-010` — documents this pattern as the canonical convention in `CLAUDE.md`
- `yw-000014-020` — verifies AC6/AC16 hold in the final report

## Key Files

- `claude-code/skills/ywc-auth-implement/SKILL.md`
- `claude-code/skills/ywc-commit/SKILL.md`
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/ywc-setup-language/SKILL.md`
- `claude-code/skills/ywc-spec-writer/SKILL.md`
- `claude-code/skills/ywc-task-generator/SKILL.md`

## Notes

`ywc-setup-language` is the one consumer that needs `--emit-section` rather than a plain
resolved code, because it writes the canonical `## Language Policy` block into a project or
user `CLAUDE.md` — it cannot do that from a bare `ko`/`ja`/etc. return value.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-auth-implement/SKILL.md`
- `claude-code/skills/ywc-commit/SKILL.md`
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/ywc-setup-language/SKILL.md`
- `claude-code/skills/ywc-spec-writer/SKILL.md`
- `claude-code/skills/ywc-task-generator/SKILL.md`

### Owned Interface

- (None — no public interface owned; SKILL.md body text only)

### Shared Surfaces

- The exact invocation string `bash claude-code/skills/scripts/resolve-language.sh` — must be spelled identically across all 6 files (AC16)

### Conflicts With

- `yw-000013-020` — shares `ywc-auth-implement/SKILL.md` and `ywc-create-pr/SKILL.md`; do not run these two tasks in parallel worktrees

### Parallelizable After

- `yw-000012-020`, `yw-000012-030`

### Task Verify

- `grep -rho 'bash claude-code/skills/scripts/resolve-language\.sh' claude-code/skills/*/SKILL.md | sort -u | wc -l` returns exactly `1`
- `grep -l 'language-resolution' claude-code/skills/ywc-auth-implement/SKILL.md claude-code/skills/ywc-commit/SKILL.md claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-setup-language/SKILL.md claude-code/skills/ywc-spec-writer/SKILL.md claude-code/skills/ywc-task-generator/SKILL.md` returns no output (directive text replaced, not merely supplemented — a residual conditional pointer to the reference is fine, but the old unconditional `**Action required**: Read [references/language-resolution.md]` form must be gone)

## Out of Scope

- Editing `references/language-resolution.md` or `references/initials-resolution.md` themselves.
- Any directive unrelated to language or initials resolution.
