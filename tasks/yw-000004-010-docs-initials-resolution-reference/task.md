# yw-000004-010-docs-initials-resolution-reference — Implementation Checklist

## Prerequisites
- [ ] Working tree is on a fresh branch from the merged base.
- [ ] `docs/ywc-plans/20260826-task-id-collaborator-initials.md` FR1 and A1 have been read.

## Allowed Edit Scope
- [ ] Create `claude-code/skills/references/initials-resolution.md`.
- [ ] Add exactly one new registry section to `claude-code/skills/CLAUDE.md`. Touch nothing else.

## Stop Conditions
- [ ] Stop if `claude-code/skills/CLAUDE.md` already contains a `## Task Initials Resolution` section (report instead of duplicating).
- [ ] Stop if the reference would need to restate rules that belong in a script comment (NFR3 single-source violation).

## Hardening Gate
- [ ] Confirm the no-block invariant is stated verbatim in both the reference and the registry section.
- [ ] Confirm the canonical `## Task Initials` section format appears exactly once, in the reference.
- [ ] Mark Data Integrity Hardening N/A — no shared counter is written here.

## Implementation Steps
- [ ] Read `claude-code/skills/references/language-resolution.md` end to end and mirror its section order, heading depth, and tone in the new file.
- [ ] Create `claude-code/skills/references/initials-resolution.md` with a `Scope` section stating this governs the task-ID numbering namespace only, and is unrelated to session or output language.
- [ ] Add a `Precedence chain` section: `--initials` flag → project `CLAUDE.md ## Task Initials` → derive + one-time confirmation → cache.
- [ ] Add a `Derivation algorithm` section: take the local-part of `git config user.email` before `@`, split on `.`/`_`/`-`, join the lowercased first character of each segment (`yongwoon.kim` → `yk`); if the result is under 2 characters, use the first 2–4 lowercase alphanumeric characters of the local-part; fall back to `git config user.name` when email is unset.
- [ ] Add a `Validation` section requiring `^[a-z0-9]{2,4}$`, and stating that a cached value failing this regex is treated as invalid and re-confirmed.
- [ ] Add a `Canonical section format` section containing the exact `## Task Initials` markdown block (`- **Initials**: yk` with the `^[a-z0-9]{2,4}$` comment, plus the `Applies to:` line).
- [ ] Add a `Caching` section stating create-or-replace semantics, and that if two `## Task Initials` headings exist the first is updated and the rest removed, leaving exactly one.
- [ ] Add a `Numbering scope` section: comparison is limited to entries carrying the resolved initials prefix; the scan unions all linked worktrees; legacy unprefixed entries seed the first PHASE per FR3; delegate the mechanics to `next-task-number.sh`'s own comments rather than restating them.
- [ ] Add a `Collision advisory` section per §A9: present the disk-scanned list of existing initials in the confirmation prompt, warn when the derived value is already in use with the existing count, and never block.
- [ ] Add an `Edge cases` section covering: no git identity (ask the user, invent nothing), derivation failing the regex (propose but prefer user input, re-ask on failure), and two collaborators deriving the same initials (advisory only).
- [ ] Add a `No-block invariant` statement: absence of `## Task Initials` never blocks, delays, or errors any consuming skill.
- [ ] Add a `## Task Initials Resolution` section to `claude-code/skills/CLAUDE.md`, placed adjacent to `## Language Resolution` and written in the same referenced-not-inlined style.
- [ ] In that registry section, register `references/initials-resolution.md` as a shared reference of equal standing to `language-resolution.md`.
- [ ] In that registry section, list the consuming skills as exactly one entry (`ywc-task-generator`), and note this differs from `language-resolution.md`'s six consumers.
- [ ] In that registry section, restate the no-block invariant for initials.

## Task Verify
- [ ] `test -f claude-code/skills/references/initials-resolution.md`
- [ ] `test "$(grep -c '^## Task Initials Resolution' claude-code/skills/CLAUDE.md)" = 1`
- [ ] `grep -q '\^\[a-z0-9\]{2,4}\$' claude-code/skills/references/initials-resolution.md`
- [ ] `grep -qi 'no-block invariant' claude-code/skills/CLAUDE.md claude-code/skills/references/initials-resolution.md`

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] markdownlint passes with the CI config and scope (`.github/workflows/markdownlint.yml`) — note `claude-code/skills/references/**` is outside that scope, so this is a no-regression check only
- [ ] typecheck passes (N/A — documentation only)
- [ ] unit tests pass (N/A — documentation only)
- [ ] app builds without error (N/A — documentation/tooling repository)
