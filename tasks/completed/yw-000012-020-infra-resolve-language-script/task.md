# yw-000012-020-infra-resolve-language-script — Implementation Checklist

## Prerequisites

- [ ] `yw-000012-010` is completed (merged) — before-baseline recorded

## Allowed Edit Scope

- [ ] Stay within `claude-code/skills/scripts/resolve-language.sh` and `test-resolve-language.sh`
- [ ] If a change to `references/language-resolution.md` seems needed, stop and report — this task consumes that reference, it does not edit it

## Stop Conditions

- [ ] Stop if implementing the precedence chain requires deviating from `language-resolution.md:22-33` — the reference is canonical, the script must match it, not the other way around
- [ ] Stop if `--emit-section`'s output cannot exactly reproduce `language-resolution.md:47-53`'s block

## Implementation Steps

- [ ] Implement the 4-rung precedence resolver
  - `--lang <value>` flag, run through `normalize()` first (case-insensitive, full name or code)
  - Project `CLAUDE.md ## Language Policy` (read `Output language:` line), then user `~/.claude/CLAUDE.md ## Language Policy`
  - Malformed policy (unrecognized code) or a second `## Language Policy` heading in the same file: treat as absent, fall through (E1, E3)
  - Terminal rung: print `UNRESOLVED`, exit 0 — never `en`
- [ ] Implement `normalize()` per the table at `language-resolution.md:61-67` (`ko`/`korean`→`ko`, etc.), case-insensitive
- [ ] Implement `--emit-section <code>`: print the exact block from `language-resolution.md:47-53` with `<code>` substituted into `Output language:`
- [ ] Write `test-resolve-language.sh` asserting:
  - AC1: `--lang Japanese` → `ja`, exit 0
  - AC2: no policy anywhere, no `--lang` → `UNRESOLVED`, exit 0
  - AC3: project policy `ko` + user policy `ja` → `ko` (project wins), using fixture directories

## Task Verify

- [ ] `bash claude-code/skills/scripts/test-resolve-language.sh` exits 0
- [ ] `shellcheck claude-code/skills/scripts/resolve-language.sh` exits 0

## Verification

- [ ] `bash scripts/validate.sh` exits 0

## Implementation Notes (optional)
