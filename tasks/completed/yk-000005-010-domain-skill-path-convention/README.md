# yk-000005-010-domain-skill-path-convention

## Purpose
Define the skill-local script path convention and rule B9 so B2 can migrate every call site (AC11b).

Spec item: B1 (#345) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- `claude-code/skills/CLAUDE.md`: new 'Skill-local script paths' section — (a) SKILL.md uses `"${CLAUDE_SKILL_DIR}/scripts/x"`, other skills `"${CLAUDE_SKILL_DIR}/../ywc-x/scripts/y"`; (b) `references/*.md` and `*.md.template` use a `"<skill-base-dir>/…"` placeholder with a one-sentence definition; (c) fallback sentence when SKILL.md was read directly; (c2) always double-quoted; (d) shared scripts (`resolve-language.sh`, `poll-pr-reviews.sh`, `mark-complete.sh`, `update-state.py`) and `${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/…` forms keep the existing contract; (e) table of skill pairs that must be installed together.
- One sentence stating the Bundled Execution Scripts table ('relative to the repository root') applies only to shared scripts; skill-local scripts follow the new section.
- Pair table: only pairs confirmed by a cross-skill script-reference grep at this point: parallel-executor→worktrees, parallel-executor→docker-isolate, finish-branch→task-generator; skill-invocation dependencies (sequential-executor→worktrees, finish-branch→worktrees) in a separate column. The handle-pr-reviews→worktrees row is added by C3.
- `ywc-skill-author`: add rule B9 (upstream B10; local number follows B8). Describe the forbidden form as 'repo-relative script path', never as a literal path, so the AC10 grep does not match the rule text itself; mirror in `references/cross-skill-graph.md`.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 9 (B1), FR3 (B10→B9), AC11b, Failure Modes rows on `${CLAUDE_SKILL_DIR}` and partial install
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/CLAUDE.md` — upstream section (T0 snapshot)

### Summary
Repo-relative script paths break once skills are installed under `~/.claude/skills`. The convention gives each file type a path form that resolves in an installed layout. B2 performs the migration; a validator gate is a follow-up.

### Out of Scope (from spec)
- Validator gate for the new rule (follow-up, Open Question 4)
- Shared-script call-site migration (follow-up, Open Question 6)
- Upstream B9 (Karpathy rows)

## Criticality
normal — Convention documentation; enforcement is a follow-up validator (out of scope).

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream convention text
- `yk-000004-050-domain-scan-secrets-guard` — serializes `claude-code/skills/CLAUDE.md` edits (A8c → B1)

### Depended By
- `yk-000005-020-domain-user-invoked-skills` — needs the output of this task

## Key Files
- `claude-code/skills/CLAUDE.md` — new section + table sentence
- `claude-code/skills/ywc-skill-author/SKILL.md` — rule B9
- `claude-code/skills/ywc-skill-author/references/cross-skill-graph.md` — rule mirror

## Notes
- Run the pair-confirming grep NOW and again after B2; list only pairs the grep shows.
- FR5 order for `ywc-skill-author/SKILL.md`: B1 → B3 → B2.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/CLAUDE.md`
- `claude-code/skills/ywc-skill-author/SKILL.md`
- `claude-code/skills/ywc-skill-author/references/cross-skill-graph.md`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- `claude-code/skills/CLAUDE.md` (A8c → B1 → B3 → B2 → B4 → B5 → C3)
- Rule catalog in `ywc-skill-author`

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`
- `yk-000004-050-domain-scan-secrets-guard`

### Task Verify
- `grep -q 'Skill-local script paths' claude-code/skills/CLAUDE.md`
- `[ "$(grep -c -- '^| B9' claude-code/skills/ywc-skill-author/SKILL.md | tr -d ' ')" = 1 ]`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-skill-author/SKILL.md`

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
