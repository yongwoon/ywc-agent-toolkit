# yw-000013-010-docs-consumer-script-invocation — Implementation Checklist

## Prerequisites

- [ ] `yw-000012-020` is completed (merged) — `resolve-language.sh` + `--emit-section` exist
- [ ] `yw-000012-030` is completed (merged) — `resolve-initials.sh` exists

## Allowed Edit Scope

- [ ] Stay within the 6 `SKILL.md` files listed in README.md Key Files
- [ ] Do not touch any of the 17 directives FR7 covers — those belong to `yw-000013-020`

## Stop Conditions

- [ ] Stop if the ≤3-line replacement block cannot avoid restating the precedence chain or code list (the single-source-of-truth rule must hold — if it can't, report back rather than silently violating it)
- [ ] Stop if `yw-000013-020` is already in flight on the same files (`ywc-auth-implement`, `ywc-create-pr`) — this is the declared `Conflicts With` pair

## Implementation Steps

- [ ] Replace the language directive in the 5 non-`ywc-setup-language`, non-`ywc-task-generator` consumers
  - `ywc-auth-implement/SKILL.md:50`, `ywc-commit/SKILL.md:135`, `ywc-create-pr/SKILL.md:56`, `ywc-spec-writer/SKILL.md:92`
  - Each becomes: the invocation `bash claude-code/skills/scripts/resolve-language.sh [--lang <code>]`, one line per return value meaning, one conditional pointer to the reference
- [ ] Replace `ywc-setup-language/SKILL.md:24` with the `--emit-section <code>` invocation (`bash claude-code/skills/scripts/resolve-language.sh --emit-section <code>`), since this consumer writes the section rather than reading a resolved code
- [ ] Replace both `ywc-task-generator/SKILL.md:48` (language) and `:114` (initials) directives
  - Language: same invocation form as the other 5 consumers
  - Initials: `bash claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh [--initials <s>]`; keep the human-confirmation prompt for the `NEEDS_CONFIRM <candidate>` return value in the skill body — the script never confirms or caches
- [ ] Verify AC16's exact-match requirement: the invocation string must be byte-identical across all 6 files

## Task Verify

- [ ] `grep -rho 'bash claude-code/skills/scripts/resolve-language\.sh' claude-code/skills/*/SKILL.md | sort -u | wc -l` returns `1`
- [ ] `grep -l 'language-resolution' claude-code/skills/ywc-auth-implement/SKILL.md claude-code/skills/ywc-commit/SKILL.md claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-setup-language/SKILL.md claude-code/skills/ywc-spec-writer/SKILL.md claude-code/skills/ywc-task-generator/SKILL.md` returns no output

## Verification

- [ ] `bash scripts/validate.sh` exits 0
- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/<each of the 6 dirs>` exits 0 for each

## Implementation Notes (optional)
