# 000030-010-docs-spec-writer-zh-es

## Purpose

Extend the **claude-code** `ywc-spec-writer` skill from `ko|ja|en` output to also support Simplified Chinese (`zh`) and Spanish (`es`), matching the `ywc-project-docs` precedent (PR #118).

## Scope

- `SKILL.md`: add `zh`/`es` to the `--lang` argument table; broaden the frontmatter `description` "Supports … output" clause and add `zh`/`es` trigger phrases; extend the in-body language-selection prompt (the numbered `한국어 (ko) / English (en) / …` list) to include Chinese and Spanish; bump the `version:` field (minor).
- `references/language-policy.md`: add a **Chinese (Simplified) (`zh`)** section and a **Spanish (`es`)** section following the existing three-part shape (Register + technical-term table + user-story format) — canonical content in the spec's Appendix A.
- README locale set (`README.md`, `.en`, `.ja`, `.ko`, `.zh`, `.es`): update any "supported output languages" wording that reads KR/JA/EN.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/multilang-zh-es-rollout.md` — FR1, FR3, FR4; AC1–AC4, AC6; Appendix A (drop-in zh/es policy content).
- `claude-code/skills/ywc-project-docs/SKILL.md` — visual template for a completed 5-language skill (keep this skill's own `ko` code, not `kr`).

### Summary
Add two languages to one skill's output surface. Body prose follows the selected language; technical terms (`API`, `Backend`, `Database`) stay in English. Default output language stays `ko` — `zh`/`es` are opt-in via `--lang` only.

### Out of Scope (from spec)
codex bundle, `plugins/` mirror, Category B skills, language-code unification (`ko` vs `kr`), Traditional Chinese, default-language changes.

## Criticality

`normal` — documentation/skill-definition edit; no security-sensitive surface. (Spec declares no Critical Surfaces.)

## Dependencies

- **Depends On**: (None) — independent of 000030-020 and 000030-030.
- **Depended By**: (None) — no task consumes this output; parallelizable sibling of 020/030.

## Key Files

- `claude-code/skills/ywc-spec-writer/SKILL.md`
- `claude-code/skills/ywc-spec-writer/references/language-policy.md`
- `claude-code/skills/ywc-spec-writer/README.md`
- `claude-code/skills/ywc-spec-writer/README.en.md`
- `claude-code/skills/ywc-spec-writer/README.ja.md`
- `claude-code/skills/ywc-spec-writer/README.ko.md`
- `claude-code/skills/ywc-spec-writer/README.zh.md`
- `claude-code/skills/ywc-spec-writer/README.es.md`

## Notes

- Keep the existing `ko` code convention (do not switch to `kr`).
- The change adds capability; it does not alter the `ko` default or any existing language's behavior.

## Out of Scope

Any file outside `claude-code/skills/ywc-spec-writer/`. Do not touch `codex/skills/**` or `plugins/**`.

## Parallel Execution Metadata

- **Ownership**: `claude-code/skills/ywc-spec-writer/**` (SKILL.md, references/language-policy.md, README*.md).
- **Shared Surfaces**: `scripts/validate.sh` and `.github/workflows/markdownlint.yml` are read-only shared gates — do not modify.
- **Conflicts With**: (None identified) — disjoint file ownership from 000030-020 and 000030-030.
- **Parallelizable After**: base branch (`main`) — no predecessor.
- **Task Verify**:
  - `bash scripts/validate.sh` → `All checks passed.`
  - `printf '{"MD013":false,"MD031":false,"MD033":false,"MD037":false,"MD040":false,"MD041":false,"MD060":false}' > /tmp/ml.json && npx --yes markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-spec-writer/README*.md"` → 0 errors
  - `grep -rniE "korean, japanese,? (and )?english|ko \| ja \| en|KR/JA/EN" claude-code/skills/ywc-spec-writer/` → no residual 3-language-only wording
  - `git status --porcelain | grep -E '^\s*M (codex/|plugins/)'` → empty (no codex/plugins drift)
