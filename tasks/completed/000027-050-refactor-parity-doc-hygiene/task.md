# 000027-050-refactor-parity-doc-hygiene — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] Working tree changes outside this task's Ownership are reviewed and left untouched.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/references/project-docs-structure.md` and `codex/skills/ywc-gen-testcase/**`.

## Stop Conditions
- [ ] Stop if stale internal URL appears only in historical changelog outside active skill docs.
- [ ] Stop if removing split project-docs names would contradict another active Codex skill.
- [ ] Stop if Source line changes require altering report data structures outside docs.

## Implementation Steps
- [ ] Update `codex/skills/references/project-docs-structure.md`.
  - [ ] Replace `ywc-project-docs-ja` / `ywc-project-docs-kr` references with unified `ywc-project-docs`.
  - [ ] Keep language-routing guidance accurate without naming nonexistent split skills.
- [ ] Update `codex/skills/ywc-gen-testcase/references/examples.md`.
  - [ ] Replace `legalforce/cas-marketing-on` with `https://github.com/acme/web-app/pull/250`.
  - [ ] Keep the example semantically equivalent.
- [ ] Update `codex/skills/ywc-gen-testcase/README*.md`.
  - [ ] Patch required locale files and any existing es/zh README that contains the stale URL.
  - [ ] Preserve localized structure and only change active example content.
- [ ] Update `codex/skills/ywc-gen-testcase/SKILL.md`.
  - [ ] Confirm no stale internal URL remains.
  - [ ] Normalize the report `Source` line to mention task range and git range notation with concrete placeholders.

## Task Verify
- [ ] `rg -n "ywc-project-docs-ja|ywc-project-docs-kr" codex/skills/references/project-docs-structure.md` returns no matches.
- [ ] `rg -n "legalforce/cas-marketing-on" codex/skills/ywc-gen-testcase` returns no matches.
- [ ] `rg -n "task range|git range|Source:" codex/skills/ywc-gen-testcase/SKILL.md`

## Verification
- [ ] Repository validation is deferred to `000028-010-infra-plugin-sync-validation`.
- [ ] `git diff --name-only` for this task contains no `claude-code/**` paths.
