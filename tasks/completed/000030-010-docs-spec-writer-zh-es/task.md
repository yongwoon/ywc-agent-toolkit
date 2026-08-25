# Task: 000030-010-docs-spec-writer-zh-es

## Prerequisites

- [ ] None — this task starts from `main` and is independent of sibling tasks 020/030.

## Allowed Edit Scope

Only files under `claude-code/skills/ywc-spec-writer/`. Do **not** edit `codex/skills/**`, `plugins/**`, or any other skill.

## Stop Conditions

- Stop and report if `references/language-policy.md`'s existing KR/JA/EN sections do **not** follow the three-part shape (Register + term table + user-story format) — the spec assumes they do.
- Stop and report if adding `zh`/`es` would require changing the `ko` default or altering any existing language's output.
- Stop if `scripts/validate.sh` fails for a reason unrelated to this skill.

## Implementation Steps

- [ ] In `claude-code/skills/ywc-spec-writer/SKILL.md`, add `zh` and `es` to the `--lang` argument-table row (currently `ko | ja | en`).
- [ ] Bump the `version:` frontmatter field (minor increment).
- [ ] Broaden the frontmatter `description` "Supports Korean, Japanese, and English output" clause to include Chinese and Spanish; add at least one `zh` and one `es` trigger phrase.
- [ ] Extend the in-body language-selection prompt (the numbered `1. 한국어 (ko) … 2. English (en) …` block) to list `中文 (zh)` and `Español (es)`.
- [ ] In `claude-code/skills/ywc-spec-writer/references/language-policy.md`, append a **Chinese (Simplified) (`zh`)** section and a **Spanish (`es`)** section using the drop-in content from spec Appendix A (Register + technical-term table + user-story format), matching the existing KR/JA/EN structure.
- [ ] Update the language-support wording in all six README files (`README.md`, `.en`, `.ja`, `.ko`, `.zh`, `.es`) wherever they say "Korean/Japanese/English" (or `ko|ja|en`), in each file's own locale prose.
- [ ] Grep the skill dir for residual 3-language-only wording and fix any missed spot.

## Task Verify

- [ ] `bash scripts/validate.sh` returns `All checks passed.`
- [ ] `printf '{"MD013":false,"MD031":false,"MD033":false,"MD037":false,"MD040":false,"MD041":false,"MD060":false}' > /tmp/ml.json && npx --yes markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-spec-writer/README*.md"` → 0 errors.
- [ ] `git status --porcelain` shows changes only under `claude-code/skills/ywc-spec-writer/`.

## Verification

- [ ] Lint/structure: `bash scripts/validate.sh` passes.
- [ ] Markdown: markdownlint (command above) passes with 0 errors.
- [ ] No build/test step applies (skill-definition docs only).
- [ ] Manual: `references/language-policy.md` now has `zh` and `es` sections; `--lang zh` / `--lang es` appear in the SKILL.md arg table and selection prompt; default remains `ko`.
