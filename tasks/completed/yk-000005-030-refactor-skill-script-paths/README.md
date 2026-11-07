# yk-000005-030-refactor-skill-script-paths

## Purpose
Replace every repo-relative skill-local script path and `<path-to-skill>` placeholder with the B1 convention across 17 files (AC10, AC11).

Spec item: B2 (#345) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- 39 hits in 15 files matching the AC10 pattern: `ywc-create-pr/SKILL.md` 3, `ywc-docker-isolate/SKILL.md` 3, `ywc-finish-branch/SKILL.md` 3, `ywc-handle-pr-reviews/SKILL.md` 2, `ywc-mine-review-history/SKILL.md` 1, `ywc-parallel-executor/SKILL.md` 6, `ywc-release-pr-list/SKILL.md` 1, `ywc-sequential-executor/SKILL.md` 2, `ywc-sequential-executor/references/aggregate-pr.md` 1, `ywc-skill-author/SKILL.md` 1, `ywc-spec-writer/SKILL.md` 5, `ywc-task-generator/SKILL.md` 4, `ywc-task-generator/references/dependency-graph.md.template` 1, `ywc-verify-done/SKILL.md` 3, `ywc-verify-done/references/gate-ledger.md` 3.
- 6 `<path-to-skill>` hits: `ywc-sequential-executor/references/checkpoint-resume.md:97-99`, `ywc-parallel-executor/references/checkpoint-resume.md:112-114`.
- SKILL.md → `"${CLAUDE_SKILL_DIR}/scripts/x"` (other skill: `"${CLAUDE_SKILL_DIR}/../ywc-x/scripts/y"`); references/templates → `"<skill-base-dir>/…"` with the one-sentence definition.
- Not targets: `ywc-confidence-gate/SKILL.md`, `worktree-run.md`, `hook-setup.md` (B1(d) forms), shared-script calls, non-`.md` files (usage comments, `test_gate_check.py:4`), and `ywc-merge-dependabot` (B4).
- After the substitution re-run the cross-skill grep and re-confirm the B1 pair table.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 10 (B2), AC10, AC11, Existing Constraints Touched 'script path'
- `claude-code/skills/CLAUDE.md` — 'Skill-local script paths' section written by B1

### Summary
Installed skills live under `~/.claude/skills/`, where repo-relative paths do not exist. This task is a mechanical migration; no wording other than the path form changes. Executor SKILL.md bodies have almost no headroom, so substitutions must not add lines.

### Out of Scope (from spec)
- Shared-script call sites (follow-up)
- `ywc-merge-dependabot` paths (B4)
- A validator gate (follow-up)

## Criticality
normal — Mechanical path-form substitution with no behavior change.

## Dependencies

### Depends On
- `yk-000005-020-domain-user-invoked-skills` — serializes `ywc-skill-author/SKILL.md` and the CLAUDE.md edits (B1 → B3 → B2); B1 convention and every Phase `yk-000004` edit to the shared files are already merged via the phase gate

### Depended By
- `yk-000005-040-domain-merge-dependabot-workflow` — needs the output of this task

## Key Files
- `(15 files listed in Scope)` — AC10-pattern substitutions
- `claude-code/skills/ywc-sequential-executor/references/checkpoint-resume.md` — `<path-to-skill>`
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md` — `<path-to-skill>`
- `claude-code/skills/CLAUDE.md` — pair table re-check only

## Notes
- AC10 grep excludes `claude-code/skills/CLAUDE.md` itself, which documents the forbidden form.
- Executor SKILL.md bodies were extracted in the executor task; confirm ≤500 afterwards.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/ywc-docker-isolate/SKILL.md`
- `claude-code/skills/ywc-finish-branch/SKILL.md`
- `claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `claude-code/skills/ywc-mine-review-history/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/**`
- `claude-code/skills/ywc-release-pr-list/SKILL.md`
- `claude-code/skills/ywc-sequential-executor/**`
- `claude-code/skills/ywc-skill-author/SKILL.md`
- `claude-code/skills/ywc-spec-writer/SKILL.md`
- `claude-code/skills/ywc-task-generator/**`
- `claude-code/skills/ywc-verify-done/**`
- `claude-code/skills/CLAUDE.md` (pair table only)

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- Skill-local script path convention
- `claude-code/skills/CLAUDE.md` pair table

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000005-020-domain-user-invoked-skills`

### Task Verify
- `[ "$(grep -rnE '(tools/)?claude-code/skills/ywc-[a-z-]+/scripts/' --include='*.md' --include='*.template' claude-code/skills | grep -v 'claude-code/skills/CLAUDE.md' | wc -l | tr -d ' ')" = 0 ]`
- `[ "$(grep -rn '<path-to-skill>' claude-code/skills | wc -l | tr -d ' ')" = 0 ]`
- AC11 existence check: for each substituted `${CLAUDE_SKILL_DIR}` / `<skill-base-dir>` path, replace the placeholder with the skill directory and `test -f` it (one-liner recorded in Implementation Notes)
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-finish-branch/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-spec-writer/SKILL.md claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-verify-done/SKILL.md`

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
