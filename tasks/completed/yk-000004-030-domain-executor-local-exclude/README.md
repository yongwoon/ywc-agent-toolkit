# yk-000004-030-domain-executor-local-exclude

## Purpose
Stop the executors from editing the tracked `.gitignore` for run-state files; use the repo-local exclude file instead, and extract long sections first so `SKILL.md` stays ≤500 body lines (AC9, NFR1).

Spec item: A8 (executors) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- FIRST extract existing long sections from `ywc-sequential-executor/SKILL.md` (body 498) and `ywc-parallel-executor/SKILL.md` (body 496) into new `references/` files (≥30 lines each, linked by name from the body) so each has headroom before any addition.
- Replace every tracked-`.gitignore` instruction for `.ywc-run-state.json` and `.ywc-learnings.jsonl` with the repo-local exclude (`git rev-parse --git-path info/exclude`, correct inside linked worktrees). Sites: echo-append in `ywc-sequential-executor/references/checkpoint-resume.md:110` and `ywc-parallel-executor/SKILL.md:129-131`; prose in sequential `checkpoint-resume.md:9,61`, parallel `checkpoint-resume.md:48`, `ywc-sequential-executor/SKILL.md:116-120`; learnings `ywc-sequential-executor/SKILL.md:482` and `ywc-parallel-executor/SKILL.md:482`.
- Failure to resolve/write the exclude file → `BLOCKED`; `--dry-run` performs only read-only steps; fix the verification 'four layers' wording (sequential `SKILL.md`).
- Review-only corrections: Step numbers in `ywc-sequential-executor/references/advisor-escalation.md`, `--pr-lang` made conditional in `references/aggregate-pr.md`, integration-branch publish and prune targets in `references/worktree-run.md`.
- Do NOT port the completion-report `DONE` definition change (target file does not exist locally).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 8 (executor bullet), AC9, NFR1, Existing Constraints Touched 'executor ignore', Edge Cases (linked worktree)
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-sequential-executor` — upstream final text (T0 snapshot)
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-parallel-executor` — upstream final text (T0 snapshot)

### Summary
The executors currently append to the tracked `.gitignore`, which dirties the user's tree and breaks in linked worktrees (`.git` is a file). The exclude file is local and untracked. Both SKILL.md bodies sit 2–4 lines under the 500 cap, so extraction must come before additions or `score.py --ci` regresses.

### Out of Scope (from spec)
- Root `.gitignore` entry for `.ywc-run-state.json` (this repo's own — unchanged)
- completion-report.md / rationalization-defense.md (do not exist locally)

## Criticality
normal — Workflow-state ignore handling; no security-sensitive surface.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream executor files

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-sequential-executor/SKILL.md` — ignore guard, learnings, four layers, extraction
- `claude-code/skills/ywc-parallel-executor/SKILL.md` — echo-append site, learnings, extraction
- `claude-code/skills/ywc-sequential-executor/references/*.md` — checkpoint-resume, advisor-escalation, aggregate-pr, worktree-run + new extracted file
- `claude-code/skills/ywc-parallel-executor/references/*.md` — checkpoint-resume + new extracted file

## Notes
- Extracted references must be ≥30 lines (else S4 −1) and linked by name from the body (A14).
- B2 later rewrites script paths in these same files — keep this task free of path-form changes.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/ywc-sequential-executor/**`
- `claude-code/skills/ywc-parallel-executor/**`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- Execution-state files `.ywc-run-state.json`, `.ywc-learnings.jsonl`
- Score gate: SKILL.md body ≤500 lines

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`

### Task Verify
- `[ "$(grep -rn '>> .gitignore' claude-code/skills | grep -c 'ywc-run-state\|ywc-learnings' | tr -d ' ')" = 0 ]`
- `[ "$(grep -rn 'git-path info/exclude' claude-code/skills | wc -l | tr -d ' ')" -ge 2 ]`
- `[ "$(grep -rn 'Add the file to `.gitignore`' claude-code/skills | wc -l | tr -d ' ')" = 0 ]`
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md`
- Review-only: quote the before/after of the 'four layers', `--pr-lang`, advisor-escalation Step numbers and worktree-run lines in Implementation Notes
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
