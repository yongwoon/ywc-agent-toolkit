# 000030-020-docs-task-generator-zh-es

## Purpose

Extend the **claude-code** `ywc-task-generator` skill from `korean|japanese|english` output to also support Simplified Chinese and Spanish, matching the `ywc-project-docs` precedent (PR #118).

## Scope

- `SKILL.md`: add `chinese`/`spanish` to the `--lang` argument table and the "supports …" body wording; broaden the frontmatter `description` and add `zh`/`es` trigger phrases; extend the "Which language should the task documents be written in?" prompt; bump the `version:` field (minor).
- `references/language-policy.md`: add a **Chinese (Simplified) (`zh`)** section and a **Spanish (`es`)** section following the existing three-part shape — canonical content in the spec's Appendix A.
- README locale set (`README.md`, `.en`, `.ja`, `.ko`, `.zh`, `.es`): update "supported output languages" wording.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/multilang-zh-es-rollout.md` — FR1, FR3, FR4; AC1–AC4, AC6; Appendix A; **Edge Cases** (word-style flags: `chinese`/`spanish`, not `zh`/`es`).
- `claude-code/skills/ywc-project-docs/SKILL.md` — 5-language visual template.

### Summary
Add two languages to task-document output. This skill uses **word-style** flag values (`korean|japanese|english`), so add `chinese`/`spanish` in the SKILL.md arg table (the policy-file section headings may stay code-tagged `zh`/`es` for parallelism with spec-writer). Body prose follows the selected language; technical terms stay in English. Default stays `english`.

### Out of Scope (from spec)
codex bundle, `plugins/` mirror, Category B skills, language-code unification, Traditional Chinese, default-language changes.

## Criticality

`normal` — documentation/skill-definition edit; no security-sensitive surface.

## Dependencies

- **Depends On**: (None) — independent of 000030-010 and 000030-030.
- **Depended By**: (None) — parallelizable sibling of 010/030.

## Key Files

- `claude-code/skills/ywc-task-generator/SKILL.md`
- `claude-code/skills/ywc-task-generator/references/language-policy.md`
- `claude-code/skills/ywc-task-generator/README.md`
- `claude-code/skills/ywc-task-generator/README.en.md`
- `claude-code/skills/ywc-task-generator/README.ja.md`
- `claude-code/skills/ywc-task-generator/README.ko.md`
- `claude-code/skills/ywc-task-generator/README.zh.md`
- `claude-code/skills/ywc-task-generator/README.es.md`

## Notes

- **Word-style flags**: accept `--lang chinese` / `--lang spanish` (not `zh`/`es`) to match the existing convention. Ensure the CLAUDE.md inference path does not misclassify.
- Adds capability only; does not change the `english` default.

## Out of Scope

Any file outside `claude-code/skills/ywc-task-generator/`. Do not touch `codex/skills/**` or `plugins/**`.

## Parallel Execution Metadata

- **Ownership**: `claude-code/skills/ywc-task-generator/**` (SKILL.md, references/language-policy.md, README*.md).
- **Shared Surfaces**: `scripts/validate.sh`, `.github/workflows/markdownlint.yml` — read-only shared gates.
- **Conflicts With**: (None identified) — disjoint file ownership from 000030-010 and 000030-030.
- **Parallelizable After**: base branch (`main`).
- **Task Verify**:
  - `bash scripts/validate.sh` → `All checks passed.`
  - `printf '{"MD013":false,"MD031":false,"MD033":false,"MD037":false,"MD040":false,"MD041":false,"MD060":false}' > /tmp/ml.json && npx --yes markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-task-generator/README*.md"` → 0 errors
  - `grep -rniE "korean \| japanese \| english|korean/japanese/english" claude-code/skills/ywc-task-generator/` → no residual 3-language-only wording
  - `git status --porcelain | grep -E '^\s*M (codex/|plugins/)'` → empty
