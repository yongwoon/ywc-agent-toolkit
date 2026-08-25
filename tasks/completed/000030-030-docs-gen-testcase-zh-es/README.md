# 000030-030-docs-gen-testcase-zh-es

## Purpose

Extend the **claude-code** `ywc-gen-testcase` skill from `ja|ko|en` prose output to also support Simplified Chinese (`zh`) and Spanish (`es`), matching the `ywc-project-docs` precedent (PR #118).

## Scope

- `SKILL.md`: add `zh`/`es` to the `--lang` argument table and to the auto-detect fallback list; broaden the frontmatter `description` and add `zh`/`es` trigger phrases; add a one-line rule that zh/es prose keeps technical terms in English (spec-validate Warning W1); bump the `version:` field (minor).
- README locale set (`README.md`, `.en`, `.ja`, `.ko`, `.zh`, `.es`): update "supported languages" wording.
- **No `references/language-policy.md`** — this skill keeps its language rules inline; do not create a policy file unless the inline rules prove insufficient.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/multilang-zh-es-rollout.md` — FR2, FR3, FR4; AC1, AC3, AC4, AC6; **Edge Cases** (auto-detect fallback must include zh/es).
- `claude-code/skills/ywc-gen-testcase/SKILL.md:57,276-283` — existing `--lang` arg table, detection order, and the "YAML keys/section numbers/template skeleton stay English, only prose follows `--lang`" invariant.

### Summary
Add two languages to testsheet prose. The template skeleton, YAML keys, and section numbers stay English regardless of `--lang`; only prose (Summary, Goal, Steps, Expected, Notes) follows the chosen language. Because this skill has no policy file, explicitly add a one-line "zh/es prose keeps technical terms in English" rule so AC1 is enforceable. Default stays auto-detect.

### Out of Scope (from spec)
codex bundle, `plugins/` mirror, Category B skills, language-code unification, Traditional Chinese, default-behavior changes, creating a policy file.

## Criticality

`normal` — documentation/skill-definition edit; no security-sensitive surface.

## Dependencies

- **Depends On**: (None) — independent of 000030-010 and 000030-020.
- **Depended By**: (None) — parallelizable sibling of 010/020.

## Key Files

- `claude-code/skills/ywc-gen-testcase/SKILL.md`
- `claude-code/skills/ywc-gen-testcase/README.md`
- `claude-code/skills/ywc-gen-testcase/README.en.md`
- `claude-code/skills/ywc-gen-testcase/README.ja.md`
- `claude-code/skills/ywc-gen-testcase/README.ko.md`
- `claude-code/skills/ywc-gen-testcase/README.zh.md`
- `claude-code/skills/ywc-gen-testcase/README.es.md`

## Notes

- **W1 (from spec-validate)**: the inline rules only say "prose follows `--lang`"; add an explicit "keep technical terms (API/Backend/Database) in English, no over-translation" note so zh/es output satisfies AC1 without a policy file.
- **Auto-detect**: add `zh`/`es` to the detection fallback list so a project whose CLAUDE.md declares Chinese/Spanish docs resolves correctly.

## Out of Scope

Any file outside `claude-code/skills/ywc-gen-testcase/`. Do not create `references/language-policy.md`. Do not touch `codex/skills/**` or `plugins/**`.

## Parallel Execution Metadata

- **Ownership**: `claude-code/skills/ywc-gen-testcase/**` (SKILL.md, README*.md).
- **Shared Surfaces**: `scripts/validate.sh`, `.github/workflows/markdownlint.yml` — read-only shared gates.
- **Conflicts With**: (None identified) — disjoint file ownership from 000030-010 and 000030-020.
- **Parallelizable After**: base branch (`main`).
- **Task Verify**:
  - `bash scripts/validate.sh` → `All checks passed.`
  - `printf '{"MD013":false,"MD031":false,"MD033":false,"MD037":false,"MD040":false,"MD041":false,"MD060":false}' > /tmp/ml.json && npx --yes markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-gen-testcase/README*.md"` → 0 errors
  - `grep -rniE "ja,ko,en|ja \| ko \| en|japanese/korean/english" claude-code/skills/ywc-gen-testcase/` → no residual 3-language-only wording
  - `git status --porcelain | grep -E '^\s*M (codex/|plugins/)'` → empty
