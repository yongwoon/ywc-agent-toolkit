# yk-000009-010-domain-scan-secrets-and-branch-hardening

## Purpose
Close the remaining security findings from the yk-000007-010 and yk-000008 reviews: two more fail-open paths in `scan-secrets.sh` (both Claude Code and Codex copies), the C2 `check-ref-format` form in two prose guards, and the unquoted, unvalidated `<base-branch>` in the parallel executor's per-task-pr base refresh.

## Scope
1. **`--committed X --staged` downgrade.** In `scan-secrets.sh` a later `--staged` resets `MODE` to `staged`, so Phase 3 is skipped and the scan exits 0 with no committed scan. `--staged` must never downgrade an earlier `--committed`: make `--staged` a no-op when `MODE` is already `committed` (Phases 1-2 always run), and keep `--committed` after `--staged` working. Apply to both `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh` and `codex/skills/ywc-create-pr/scripts/scan-secrets.sh`.
2. **Phase 1/2 swallow git errors.** `git status --short 2>/dev/null | … || true`, `git diff --cached 2>/dev/null || true` and `git diff 2>/dev/null || true` turn a failing git call into "clean". Capture each git command's output first and exit 2 ("nothing was scanned") when it fails; keep `|| true` only on the `grep` filters, where exit 1 means "no match". Same change in both copies.
3. **Tests first** in both `test-scan-secrets.sh` copies (keep them byte-identical):
   - `--committed main --staged` with a committed secret → exit 1 (would be 0 today);
   - `--staged --committed main` with a committed secret → exit 1;
   - a `git` shim mode that fails `git status` → exit 2, and one that fails `git diff --cached` → exit 2.
   Confirm each new case is RED against the current script before fixing it, and that removing each new guard turns the suite red.
4. **C2 `check-ref-format` form.** `claude-code/skills/ywc-worktrees/SKILL.md` (`--existing-branch` bullet) uses `git check-ref-format "refs/heads/<branch>"`. Use the same form in `claude-code/skills/ywc-finish-branch/SKILL.md` Step 5 Remote deletion guard (`git check-ref-format "refs/heads/$branch"`) and `claude-code/skills/references/pr-conflict-resolution.md` (`git check-ref-format "refs/heads/$BASE"`).
5. **Parallel per-task-pr base refresh.** `claude-code/skills/ywc-parallel-executor/SKILL.md` Step 4e (a) step 4 splices `<base-branch>` and `feature/<task-name>` unquoted into `git fetch` / `git merge-base` / `git merge -m`. Hold them in `BASE` / `BRANCH`, validate both per the C2 rule (as `pr-conflict-resolution.md` does, `BLOCKED: invalid branch name` on failure), and quote every use. Use `git -C "<worktree-path>"` (the path captured in Step 4a) instead of the stale `../worktree-<task-name>`.
6. Let the pre-commit hook regenerate `plugins/ywc-agent-toolkit` for the Codex change; never hand-edit it.

## Spec Reference

### Primary Sources
- yk-000007-010 security-lane review (late report) and the yk-000008 Completion Report "Deferred findings".
- `claude-code/skills/ywc-worktrees/SKILL.md` `--existing-branch` bullet — canonical C2 rule.
- `docs/review-learnings.md` (repository review rules).

### Summary
`scan-secrets.sh` must never report clean when it did not scan. Branch names reaching git must pass the same C2 validation everywhere, in the same form.

### Out of Scope (from findings)
- `scan-secrets.sh` secret-pattern changes; the non-UTF-8 grep hardening candidate.
- Codex skill prose (only the Codex `scan-secrets.sh` and its test are in scope).
- Reviewer trigger-case coverage, `score.py` exemptions, and the other deferred items in the yk-000008 report.

## Criticality
critical — secret-detection exit contract and remote-controlled branch names reaching shell commands.

## Dependencies

### Depends On
- (None — all inputs are merged on `feature/improvement-20261106`)

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh`, `test-scan-secrets.sh`
- `codex/skills/ywc-create-pr/scripts/scan-secrets.sh`, `test-scan-secrets.sh`
- `claude-code/skills/ywc-finish-branch/SKILL.md`
- `claude-code/skills/references/pr-conflict-resolution.md`
- `claude-code/skills/ywc-parallel-executor/SKILL.md`

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `codex/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/scripts/**` (generated)
- `plugins/ywc-agent-toolkit/README.md` (generated)
- `claude-code/skills/ywc-finish-branch/SKILL.md`
- `claude-code/skills/references/pr-conflict-resolution.md`
- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

### Owned Interface
- `scan-secrets.sh` exit contract (0 clean / 1 secret / 2 nothing scanned)

### Shared Surfaces
- C2 branch-name rule (`ywc-worktrees`)

### Conflicts With
- (None identified)

### Parallelizable After
- (None)

### Task Verify
- `bash claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `bash codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `cmp claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `cmp codex/skills/ywc-create-pr/scripts/scan-secrets.sh plugins/ywc-agent-toolkit/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `[ "$(grep -c '2>/dev/null || true' claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh | tr -d ' ')" = 0 ]`
- `[ "$(grep -c 'check-ref-format --branch' claude-code/skills/ywc-finish-branch/SKILL.md claude-code/skills/references/pr-conflict-resolution.md | awk -F: '{s+=$2} END{print s}')" = 0 ]`
- `[ "$(grep -c 'git -C ../worktree-<task-name>' claude-code/skills/ywc-parallel-executor/SKILL.md | tr -d ' ')" = 0 ]`
- `grep -qF 'git fetch origin "$BASE"' claude-code/skills/ywc-parallel-executor/SKILL.md`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit if it changed
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-finish-branch/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md`

## Out of Scope
Anything not listed in Scope.
