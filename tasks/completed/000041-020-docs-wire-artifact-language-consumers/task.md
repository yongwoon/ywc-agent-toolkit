# Task: 000041-020-docs-wire-artifact-language-consumers

## Prerequisites

- [ ] `000040-010-docs-codex-language-resolution-reference` is completed.

## Allowed Edit Scope

- [ ] Stay within:
  - `codex/skills/ywc-task-generator/**`
  - `codex/skills/ywc-spec-writer/**`
  - `codex/skills/ywc-gen-testcase/**`
  - `codex/skills/ywc-project-docs/**`
- [ ] Do not edit PR/orchestration skills, root docs, or generated plugin files.

## Stop Conditions

- [ ] Stop if an old fallback is required for backward compatibility and conflicts with AC8.
- [ ] Stop if a README locale change cannot be made consistently across existing maintained locale files.
- [ ] Stop if resolving `ywc-gen-testcase` heuristics requires a product decision not covered by the spec.

## Hardening Gate

- [ ] Classify this task as docs-only behavior-contract update.
- [ ] Record named exception: no RED-first test; use targeted grep and validation.
- [ ] Record interface contract: generated artifact prose follows shared language resolution.
- [ ] Data Integrity fields are N/A.
- [ ] Critical surface review is N/A.

## Implementation Steps

- [ ] Update `ywc-task-generator`.
  - [ ] Replace inference/default prose with shared reference link.
  - [ ] Remove documented `en` skill default.
  - [ ] Keep `ko|ja|en|zh|es` support and existing aliases.
  - [ ] Update `references/language-policy.md` to focus on writing rules, not resolution order.
  - [ ] Update README locale files that document old default behavior.
- [ ] Update `ywc-spec-writer`.
  - [ ] Remove documented `ko` skill default.
  - [ ] Route omitted `--lang` through shared resolution.
  - [ ] Keep locale-specific writing policy and `init-spec-structure.sh <lang>` behavior aligned with resolved code.
  - [ ] Update README locale files that document old default behavior.
- [ ] Update `ywc-gen-testcase`.
  - [ ] Replace English fallback with shared resolution.
  - [ ] Decide and document whether recent testsheets / README language are lower-priority hints or removed; no final skill default.
  - [ ] Preserve machine-facing English template rules.
  - [ ] Update README locale files that document old default behavior.
- [ ] Update `ywc-project-docs`.
  - [ ] Insert project/user config tiers before ask.
  - [ ] Preserve `kr` input alias if already documented, normalize canonical code to `ko`.
  - [ ] Keep technical terms in English.
  - [ ] Update README locale files that document old ask-only behavior.

## Task Verify

- [ ] `grep -q "language-resolution.md" codex/skills/ywc-task-generator/SKILL.md`
- [ ] `grep -q "language-resolution.md" codex/skills/ywc-spec-writer/SKILL.md`
- [ ] `grep -q "language-resolution.md" codex/skills/ywc-gen-testcase/SKILL.md`
- [ ] `grep -q "language-resolution.md" codex/skills/ywc-project-docs/SKILL.md`
- [ ] `! rg -n "Default:.*(ko|en)|default:.*(ko|en)|Default is Korean|Fallback.*English" codex/skills/ywc-task-generator codex/skills/ywc-spec-writer codex/skills/ywc-gen-testcase codex/skills/ywc-project-docs`

## Verification

- [ ] `bash scripts/validate.sh`
