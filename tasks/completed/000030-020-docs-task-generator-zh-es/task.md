# Task: 000030-020-docs-task-generator-zh-es

## Prerequisites

- [ ] None — starts from `main`, independent of sibling tasks 010/030.

## Allowed Edit Scope

Only files under `claude-code/skills/ywc-task-generator/`. Do **not** edit `codex/skills/**`, `plugins/**`, or any other skill.

## Stop Conditions

- Stop and report if the `--lang` value convention is unclear — this skill uses **words** (`korean|japanese|english`); add `chinese`/`spanish`, never `zh`/`es`, in the SKILL.md arg table.
- Stop and report if adding languages would require changing the `english` default.
- Stop if `scripts/validate.sh` fails for a reason unrelated to this skill.

## Implementation Steps

- [ ] In `claude-code/skills/ywc-task-generator/SKILL.md`, add `chinese` and `spanish` to the `--lang` argument-table row and to the "supports `korean | japanese | english`" body sentence(s).
- [ ] Bump the `version:` frontmatter field (minor increment).
- [ ] Broaden the frontmatter `description` to name Chinese and Spanish; add at least one `zh` and one `es` trigger phrase.
- [ ] Extend the "Which language should the task documents be written in? (korean / japanese / english)" prompt to include `chinese` / `spanish`.
- [ ] In `claude-code/skills/ywc-task-generator/references/language-policy.md`, append a **Chinese (Simplified) (`zh`)** section and a **Spanish (`es`)** section using spec Appendix A content, matching the existing KR/JA/EN three-part structure.
- [ ] Update the language-support wording in all six README files in each file's own locale prose.
- [ ] Grep the skill dir for residual 3-language-only wording and fix any missed spot.

## Task Verify

- [ ] `bash scripts/validate.sh` returns `All checks passed.`
- [ ] `printf '{"MD013":false,"MD031":false,"MD033":false,"MD037":false,"MD040":false,"MD041":false,"MD060":false}' > /tmp/ml.json && npx --yes markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-task-generator/README*.md"` → 0 errors.
- [ ] `git status --porcelain` shows changes only under `claude-code/skills/ywc-task-generator/`.

## Verification

- [ ] `bash scripts/validate.sh` passes.
- [ ] markdownlint (command above) passes with 0 errors.
- [ ] No build/test step applies (skill-definition docs only).
- [ ] Manual: `--lang chinese` / `--lang spanish` accepted in the arg table and prompt; `language-policy.md` has `zh`/`es` sections; default remains `english`.
