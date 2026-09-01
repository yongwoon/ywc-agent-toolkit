# yw-000012-020-infra-resolve-language-script

## Purpose

Add the deterministic script that resolves output language, replacing the 121-line
`references/language-resolution.md` read (6 consumers) with a script invocation, per
`CLAUDE.md` §"Bundled Execution Scripts" precedent.

## Scope

- `claude-code/skills/scripts/resolve-language.sh`: 4-rung precedence chain
  (`--lang` flag → project `CLAUDE.md ## Language Policy` → user `~/.claude/CLAUDE.md
  ## Language Policy` → `UNRESOLVED`), verbatim from `references/language-resolution.md:22-33`.
- `normalize()`: case-insensitive full-name→code mapping from `language-resolution.md:61-67`
  (`ko|korean`, `ja|japanese`, `en|english`, `es|spanish`, `zh|chinese`).
- `--emit-section <code>`: prints the canonical `## Language Policy` block
  (`language-resolution.md:47-53`) with `<code>` substituted, for `ywc-setup-language`.
- Shell test file asserting AC1–AC3.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` — FR1, FR2, FR3, AC1, AC2, AC3, AC6
- `claude-code/skills/references/language-resolution.md` — canonical precedence chain, code list, section format (single source of truth; do not restate in the script's comments beyond what implements it)

### Summary

Implements the precedence chain and `normalize()` exactly as documented in
`language-resolution.md`. The terminal rung is deliberately `UNRESOLVED`, never a hardcoded
`en` — routing through each of the 6 callers' own fallback preserves no-regression behavior.
`--emit-section` exists only because `ywc-setup-language` *writes* the canonical section, not
just resolves a code (Edge Case E9).

### Out of Scope (from spec)

- Wiring the script into any consumer `SKILL.md` — handled by `yw-000013-010`.
- `resolve-initials.sh` — handled by `yw-000012-030`.
- Extending shellcheck CI coverage — handled by `yw-000012-040`.

## Criticality

`normal` — read-only resolution script, no auth/payment/crypto/secret surface.

## Dependencies

### Depends On

- `yw-000012-010` — before-baseline must be captured before this script lands

### Depended By

- `yw-000012-040` — needs this script to exist to extend shellcheck coverage over it
- `yw-000013-010` — wires this script into the 6 consumers

## Key Files

- `claude-code/skills/scripts/resolve-language.sh` — new
- `claude-code/skills/scripts/test-resolve-language.sh` — new (naming matches the existing `test-poll-pr-reviews.sh` in the same directory)

## Notes

NFR1–NFR3 apply: POSIX-`sh`-compatible bash, exit 0 in every path (including malformed/missing
policy — E1, E3), read-only (never writes to any `CLAUDE.md` — that stays `ywc-setup-language`'s
job). Malformed policy (E1) and duplicate `## Language Policy` sections (E3) both fall through
without erroring, never more blocking than absence.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/scripts/resolve-language.sh`
- `claude-code/skills/scripts/test-resolve-language.sh`

### Owned Interface

- `resolve-language.sh [--lang <code>] [--emit-section <code>]` → stdout one of `ko|ja|en|es|zh|UNRESOLVED`; exit 0 always

### Shared Surfaces

- (None identified — new files only, no shared file edited)

### Conflicts With

- (None identified)

### Parallelizable After

- `yw-000012-010`

### Task Verify

- `bash claude-code/skills/scripts/test-resolve-language.sh`
- `shellcheck claude-code/skills/scripts/resolve-language.sh`

## Out of Scope

- Any change to `references/language-resolution.md` itself — it remains the human-maintained source of truth.
- Wiring consumers to invoke this script.
