# yw-000012-030-infra-resolve-initials-script — Implementation Checklist

## Prerequisites

- [ ] `yw-000012-010` is completed (merged) — before-baseline recorded

## Allowed Edit Scope

- [ ] Stay within `claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh` and `test-resolve-initials.sh`
- [ ] If a change to `references/initials-resolution.md` seems needed, stop and report

## Stop Conditions

- [ ] Stop if the script would need to prompt the user or write a file to satisfy an AC — it must not; prompting/writing is the calling skill's job
- [ ] Stop if the derivation algorithm needs to deviate from `initials-resolution.md:44-50`

## Implementation Steps

- [ ] Implement the precedence chain: `--initials <s>` flag (validated `^[a-z0-9]{2,4}$`) → derive from `git config user.email` (local-part before `@`), falling back to `git config user.name` if email is unset
- [ ] Implement the derivation algorithm: split local-part on `.`/`_`/`-`, take first char of each segment lowercased, join (`yongwoon.kim` → `yk`); if result < 2 chars, take first 2–4 lowercase alphanumeric chars of the original string instead
- [ ] Never confirm or write: print `NEEDS_CONFIRM <candidate>` when a derivable candidate exists but is unconfirmed; print `NONE` when nothing is derivable (no email, no name, or derivation yields an unusable string)
- [ ] Write `test-resolve-initials.sh` asserting:
  - AC4: no flag, no section, `git config user.email = yongwoon.kim@example.com` → `NEEDS_CONFIRM yk`, exit 0
  - AC5: no flag, no section, no resolvable git identity → `NONE`, exit 0

## Task Verify

- [ ] `bash claude-code/skills/ywc-task-generator/scripts/test-resolve-initials.sh` exits 0
- [ ] `shellcheck claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh` exits 0

## Verification

- [ ] `bash scripts/validate.sh` exits 0

## Implementation Notes (optional)
