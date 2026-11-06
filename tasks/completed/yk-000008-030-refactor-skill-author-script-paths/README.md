# yk-000008-030-refactor-skill-author-script-paths

## Purpose
Fix the repo-relative `bash scripts/audit-skills.sh` paths in `ywc-skill-author`, which break once the skill is installed (final-review M3, rule B9). yk-000005-030's search pattern missed this form.

## Scope
- `claude-code/skills/ywc-skill-author/SKILL.md` (~line 194): `bash "${CLAUDE_SKILL_DIR}/scripts/audit-skills.sh" ...`.
- `claude-code/skills/ywc-skill-author/references/audit-workflow.md` (~line 12): `bash "<skill-base-dir>/scripts/audit-skills.sh" ...` plus the defining sentence from `claude-code/skills/CLAUDE.md` Skill-local script paths (b).
- Sweep `claude-code/skills/*/SKILL.md` and `claude-code/skills/*/references/*.md` for any other `bash scripts/<name>` where `<name>` is a skill-local script (not `scripts/validate.sh` / `scripts/install.sh` at the repo root); fix each in the owning file only if it is listed in Ownership, otherwise list it in Implementation Notes.

## Spec Reference

### Primary Sources
- Issue 69 port final review (Lows, M3, M6) and the yk-000007-010 review (Lows), recorded in those runs' Completion Reports.
- `docs/review-learnings.md` (repository review rules)

### Summary
Follow-up items deferred by earlier runs on `feature/improvement-20261106`. Each Scope bullet names the file and the expected end state.

### Out of Scope (from findings)
- Anything not in Scope; other Phase 000008 tasks' items.

## Criticality
normal

## Dependencies

### Depends On
- (None)

### Depended By
- `yk-000008-040-test-trigger-cases-grounding`

## Key Files
- `claude-code/skills/ywc-skill-author/SKILL.md`
- `claude-code/skills/ywc-skill-author/references/**`

## Parallel Execution Metadata

- Model Hint: sonnet

### Ownership
- `claude-code/skills/ywc-skill-author/SKILL.md`
- `claude-code/skills/ywc-skill-author/references/**`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- Skill-local script path convention (`claude-code/skills/CLAUDE.md`)

### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `[ "$(grep -c 'bash scripts/audit-skills.sh' claude-code/skills/ywc-skill-author/SKILL.md claude-code/skills/ywc-skill-author/references/audit-workflow.md | awk -F: '{s+=$2} END{print s}')" = 0 ]`
- `grep -qF '${CLAUDE_SKILL_DIR}/scripts/audit-skills.sh' claude-code/skills/ywc-skill-author/SKILL.md`
- `grep -qF '<skill-base-dir>/scripts/audit-skills.sh' claude-code/skills/ywc-skill-author/references/audit-workflow.md`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000008 parallel tasks do NOT commit the baseline file; yk-000008-040 stages it last
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-skill-author/SKILL.md`

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
