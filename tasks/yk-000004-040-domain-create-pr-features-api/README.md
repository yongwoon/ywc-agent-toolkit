# yk-000004-040-domain-create-pr-features-api

## Purpose
Move the 'Changes' instruction of `ywc-create-pr` into a new reference that requires a feature list and a conditional API-change table (AC6).

Spec item: A5 (#391) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- Create `claude-code/skills/ywc-create-pr/references/pr-body-features-api.md` (upstream is 107 lines).
- In `SKILL.md` replace the `[List of specific changes made]` placeholder (`:257`) with a feature-list instruction plus an 'Action required: Read references/pr-body-features-api.md' link.
- The reference's Placement rule says the Review Guide goes last; locally there is no `pr-body-review-guide.md`, so rewrite that to 'after Design Background'.
- Add one sentence about the feature list / API table to the four Tier 1 `ywc-create-pr` READMEs.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 5 (A5), AC6, Existing Constraints Touched 'create-pr Changes'
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-create-pr/references/pr-body-features-api.md` — upstream reference (T0 snapshot)

### Summary
PR bodies should list what changed as features and, when an API contract changed, show a table of changes. The detailed rules live in a reference so `SKILL.md` stays small.

### Out of Scope (from spec)
- `design-background-template.md`, `reviewer-brief.md`, `ui-screenshots.md` (installed-bundle only / not local)
- scan-secrets changes — owned by the A8c task

## Criticality
normal — PR-body authoring guidance; no security-sensitive surface.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream reference file

### Depended By
- `yk-000004-050-domain-scan-secrets-guard` — needs the output of this task

## Key Files
- `claude-code/skills/ywc-create-pr/references/pr-body-features-api.md` — new
- `claude-code/skills/ywc-create-pr/SKILL.md` — :257 placeholder → instruction + link
- `claude-code/skills/ywc-create-pr/README{,.en,.ja,.ko}.md` — one sentence

## Notes
- `ywc-create-pr/SKILL.md` is 436 lines; the reference absorbs the new text.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/ywc-create-pr/references/pr-body-features-api.md`
- `claude-code/skills/ywc-create-pr/README*.md`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- `ywc-create-pr/SKILL.md` is also edited by the scan-secrets task and B2

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`

### Task Verify
- `test -f claude-code/skills/ywc-create-pr/references/pr-body-features-api.md`
- `grep -q 'pr-body-features-api' claude-code/skills/ywc-create-pr/SKILL.md`
- `[ "$(grep -c -- '\[List of specific changes made\]' claude-code/skills/ywc-create-pr/SKILL.md | tr -d ' ')" = 0 ]`
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-create-pr/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
