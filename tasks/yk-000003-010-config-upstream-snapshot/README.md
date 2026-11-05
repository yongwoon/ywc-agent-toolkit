# yk-000003-010-config-upstream-snapshot

## Purpose
Secure the final upstream (develop-with-llm `main`, commit `2e323a97`) reference files in a fixed path outside the repository so that every port task transplants from a recorded source instead of from memory (AC0).

Spec item: T0 (Phase 0) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- Create `${TMPDIR:-/tmp}/ywc-issue69-snapshot/` (outside the repository, readable by later sessions and subagents) and a `MANIFEST.md` listing every file, its source, and its consuming task.
- Primary source: `gh api repos/yongwoon/develop-with-llm/contents/<path>?ref=2e323a97` (raw). Secondary source when the primary is unavailable: the installed bundle in `~/.claude/skills/` (confirm provenance via `.develop-with-llm.manifest`); the installed bundle is read in place, NOT copied, and recorded as `installed bundle, commit unpinned`.
- If neither source is available for a path, record `BLOCKED` for the consuming task in the MANIFEST. Rewriting from memory is forbidden.
- Paths to fetch (all under upstream `tools/claude-code/`): skills `ywc-plan`, `ywc-auth-implement`, `ywc-finish-branch`, `ywc-impl-review/references/{coderabbit-methodology,recurring-defects,devex-agent,security-agent}.md`, `ywc-create-pr` (SKILL.md, `references/pr-body-features-api.md`, `scripts/{scan-secrets,test-scan-secrets}.sh`), `ywc-debug-rootcause` (SKILL.md + references), `ywc-brainstorm`, `ywc-tdd-ritual`, `ywc-changelog-release-notes`, `ywc-code-gen`, `ywc-refactor-clean`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-infra-review`, `ywc-iac-author`, `ywc-verify-done`, `ywc-skill-author` (SKILL.md, `references/{skill-template,cross-skill-graph}.md`), `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-task-generator` (`references/output-and-validation.md`), `ywc-merge-dependabot/**`, `ywc-setup` (maps to local `ywc-setup-language`), `ywc-handoff/**`, `ywc-retro/**`, `ywc-worktrees`, `ywc-handle-pr-reviews`, `CLAUDE.md` (skills), and agents `ywc-{go,python,typescript}-reviewer.md`, `ywc-qa-engineer.md`.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `### Phase 0` (T0), AC0, FR1, Failure Modes row 'upstream reference unavailable'

### Summary
Later tasks port only the hunks named in their own Scope from these files. The installed bundle can be newer than Issue #69, so no task may copy a snapshot file wholesale. This task only gathers and indexes the files; it ports nothing.

### Out of Scope (from spec)
- Any transplanting of snapshot content into the repository — owned by the Phase A/B/C tasks
- Codex-side snapshots (separate `codex` plan)

## Criticality
normal — No repository change; fetches reference files into a directory outside the repo.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `yk-000004-010-domain-plan-auto-converge` — needs the output of this task
- `yk-000004-020-domain-finish-branch-remote-guard` — needs the output of this task
- `yk-000004-030-domain-executor-local-exclude` — needs the output of this task
- `yk-000004-040-domain-create-pr-features-api` — needs the output of this task
- `yk-000004-050-domain-scan-secrets-guard` — needs the output of this task
- `yk-000004-060-domain-skill-contradiction-fixes` — needs the output of this task
- `yk-000004-070-domain-impl-review-linter-defects` — needs the output of this task
- `yk-000004-080-domain-debug-feedback-loop` — needs the output of this task
- `yk-000004-090-domain-brainstorm-tdd-rules` — needs the output of this task
- `yk-000005-010-domain-skill-path-convention` — needs the output of this task
- `yk-000005-020-domain-user-invoked-skills` — needs the output of this task
- `yk-000005-040-domain-merge-dependabot-workflow` — needs the output of this task
- `yk-000005-050-domain-handoff-retro-skills` — needs the output of this task
- `yk-000006-010-domain-agent-description-alignment` — needs the output of this task
- `yk-000006-020-domain-worktrees-existing-branch` — needs the output of this task
- `yk-000006-030-domain-handle-pr-reviews-worktree` — needs the output of this task

## Key Files
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` — snapshot index (outside repo)
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/**` — fetched upstream files (outside repo)

## Notes
- This task produces NO repository diff. Executors should treat it as a no-diff task: record the MANIFEST path and the count of ok/installed/blocked entries in Implementation Notes, then move the task directory to `completed/`.
- `${TMPDIR:-/tmp}` can be cleaned between sessions. Every consumer lists the MANIFEST check as a Prerequisite and re-runs this task if it is gone.
- Owned Interface is intentionally `None`: the snapshot layout is a file-system convention (`<SNAP>/<upstream path>`), not a code/route/props signature.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (Ownership is outside the repository, not docs-only per include list)

### Ownership
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/**` (outside the repository; no repository file is modified)

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `test -s "${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md"`
- `[ "$(find "${TMPDIR:-/tmp}/ywc-issue69-snapshot" -type f -empty | wc -l | tr -d ' ')" = 0 ]`
- `case "$(cd "${TMPDIR:-/tmp}/ywc-issue69-snapshot" && pwd -P)/" in "$(pwd -P)"/*) echo 'snapshot is inside the repo'; false;; esac`
- `grep -c 'BLOCKED' "${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md"` is reported in Implementation Notes (BLOCKED rows are surfaced, not hidden)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
