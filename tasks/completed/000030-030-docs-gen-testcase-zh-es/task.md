# Task: 000030-030-docs-gen-testcase-zh-es

## Prerequisites

- [ ] None — starts from `main`, independent of sibling tasks 010/020.

## Allowed Edit Scope

Only files under `claude-code/skills/ywc-gen-testcase/`. Do **not** create a `references/language-policy.md`, and do **not** edit `codex/skills/**`, `plugins/**`, or any other skill.

## Stop Conditions

- Stop and report if the inline language rules cannot express "keep technical terms in English" without a policy file — the spec prefers an inline one-liner, but flag if that proves inadequate rather than silently creating a policy file.
- Stop and report if adding `zh`/`es` would require changing the auto-detect default behavior.
- Stop if `scripts/validate.sh` fails for a reason unrelated to this skill.

## Implementation Steps

- [ ] In `claude-code/skills/ywc-gen-testcase/SKILL.md`, add `zh` and `es` to the `--lang` argument-table row (currently `ja,ko,en`).
- [ ] Add `zh`/`es` to the auto-detect fallback list (detection order at SKILL.md:276-283) so CLAUDE.md-declared Chinese/Spanish projects resolve.
- [ ] Add a one-line rule: zh/es prose keeps technical terms (API, Backend, Database) in English — no over-translation (addresses spec-validate Warning W1).
- [ ] Bump the `version:` frontmatter field (minor increment).
- [ ] Broaden the frontmatter `description` to name Chinese and Spanish; add at least one `zh` and one `es` trigger phrase.
- [ ] Confirm the "YAML keys, section numbers, template skeleton stay English; only prose follows `--lang`" invariant already scopes zh/es correctly (no skeleton translation) — no edit needed if already generic.
- [ ] Update the language-support wording in all six README files in each file's own locale prose.
- [ ] Grep the skill dir for residual 3-language-only wording and fix any missed spot.

## Task Verify

- [ ] `bash scripts/validate.sh` returns `All checks passed.`
- [ ] `printf '{"MD013":false,"MD031":false,"MD033":false,"MD037":false,"MD040":false,"MD041":false,"MD060":false}' > /tmp/ml.json && npx --yes markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-gen-testcase/README*.md"` → 0 errors.
- [ ] `git status --porcelain` shows changes only under `claude-code/skills/ywc-gen-testcase/`.

## Verification

- [ ] `bash scripts/validate.sh` passes.
- [ ] markdownlint (command above) passes with 0 errors.
- [ ] No build/test step applies (skill-definition docs only).
- [ ] Manual: `--lang zh` / `--lang es` in the arg table and detection fallback; technical-term-in-English rule present; no policy file created; default auto-detect unchanged.
