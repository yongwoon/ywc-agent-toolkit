# yk-000007-010-domain-security-guard-followups

## Purpose
Close the four security-related Medium findings left by the `--final-review` of the Issue 69 port run (yk-000003-010..yk-000006-030, branch `feature/improvement-20261106`, HEAD `ed552a62`).

## Scope
1. **Wire the unwired security tests into `scripts/validate.sh`** (final-review M1). Add the same "missing → ERROR / failed → ERROR" block used for `test-scan-secrets.sh` (validate.sh ~733-741) for:
   - `claude-code/skills/ywc-handle-pr-reviews/tests/resolve-pr-head-test.sh` (bash)
   - `claude-code/skills/ywc-handoff/tests/test_handoff_safety.py` (python3)
   - `claude-code/skills/ywc-retro/tests/test_retro_safety.py` (python3)
   All three pass today, as checked on `ed552a62`.
2. **`scan-secrets.sh --committed` fail-closed** (final-review M2). Phase 3 runs `git diff "${BASE_BRANCH}...HEAD" 2>/dev/null || true`, so an unresolvable base yields an empty diff and `OK` / exit 0 even with a committed AWS key. Required behaviour:
   - `BASE_BRANCH` must match `^[A-Za-z0-9._/-]+$` and not start with `-`.
   - `git rev-parse --verify --quiet "${BASE_BRANCH}^{commit}"` must succeed.
   - Drop the `|| true` on the committed diff, so a diff failure is not swallowed.
   - On any failure: print to stderr and exit 2. Exit 2 is the existing "could not scan" code; confirm it in the script header before using it.
   - Add `test-scan-secrets.sh` cases:
     - unknown base → exit 2;
     - base with `-` prefix → exit 2;
     - valid base with a committed `AKIA…` line → exit 1;
     - valid base with a clean history → exit 0.
     The exit-0 and exit-1 cases also close the 050 deferral.
3. **`ywc-finish-branch` remote deletion guard allowlist** (final-review M4). `SKILL.md` Step 5 "Remote deletion guard" relies on `git check-ref-format --branch` alone. Prepend the C2 rule from `ywc-worktrees/SKILL.md` Step 2 (the `--existing-branch` bullet) in the same order:
   - Validate in-process, without interpolating the value into a shell command.
   - Whole-string `^[A-Za-z0-9._/-]+$`, no leading `-`, no `..`.
   - Only then `git check-ref-format`.
4. **`pr-conflict-resolution.md` base-name validation** (final-review M5). "Update Branch From Base" passes `<base-branch>` (from the PR's remote-controlled `baseRefName`, reached from `ywc-handle-pr-reviews` Step 8) straight into `git fetch` and `git merge -m`. Add a validation sentence before the code block with the same C2 rule, and on failure `BLOCKED: invalid base branch name`. Quote every use of the branch as a variable in the snippet.

## Spec Reference

### Primary Sources
- Final review of the Issue 69 port run (report-only, findings M1, M2, M4, M5), recorded in that run's Completion Report.
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — Critical Surfaces and Failure Modes rows "malicious branch / PR number" and "handoff secret" (this task completes them).
- `claude-code/skills/ywc-worktrees/SKILL.md` Step 2 (`--existing-branch` bullet) — the canonical C2 branch-name rule to reuse verbatim in intent.

### Summary
Three critical-area test suites exist but CI never runs them. The secret scan reports clean when it could not scan. Two places pass remote-controlled branch names to git with weaker validation than the C2 rule already adopted by `ywc-worktrees` and `ywc-handle-pr-reviews`.

### Out of Scope (from findings)
- M3 (`ywc-skill-author` repo-relative `bash scripts/audit-skills.sh`) and M6 (trigger-cases fixture L001/L004 grounding) — separate non-security follow-ups.
- Codex mirror of the `scan-secrets.sh` guard (`codex/`, `plugins/ywc-agent-toolkit`).

## Criticality
critical — touches a secret-detection exit contract and remote-controlled branch names reaching shell commands.

## Dependencies

### Depends On
- (None — all inputs are merged on `feature/improvement-20261106`)

### Depended By
- (None)

## Key Files
- `scripts/validate.sh` — test wiring
- `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh` — Phase 3 guard
- `claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh` — new `--committed` cases
- `claude-code/skills/ywc-finish-branch/SKILL.md` — Step 5 remote deletion guard
- `claude-code/skills/references/pr-conflict-resolution.md` — Update Branch From Base
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — baseline

## Notes
- Reuse the existing validate.sh block shape; do not introduce a test-runner abstraction for four entries.
- The scan-secrets test must build its fixture repo under `mktemp -d` and never touch the real repository.

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `scripts/validate.sh`
- `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `claude-code/skills/ywc-finish-branch/SKILL.md`
- `claude-code/skills/references/pr-conflict-resolution.md`
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

### Owned Interface
- `scan-secrets.sh --committed` exit contract (0 clean / 1 secret / 2 could not scan)

### Shared Surfaces
- C2 branch-name rule (`ywc-worktrees`)

### Conflicts With
- (None identified)

### Parallelizable After
- (None)

### Task Verify
- `grep -q 'resolve-pr-head-test.sh' scripts/validate.sh`
- `grep -q 'test_handoff_safety.py' scripts/validate.sh`
- `grep -q 'test_retro_safety.py' scripts/validate.sh`
- `grep -q 'rev-parse --verify' claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `grep -q -- '--committed' claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `bash claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `grep -qF '^[A-Za-z0-9._/-]+$' claude-code/skills/ywc-finish-branch/SKILL.md`
- `grep -qF '^[A-Za-z0-9._/-]+$' claude-code/skills/references/pr-conflict-resolution.md`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-finish-branch/SKILL.md`

## Out of Scope
Anything not listed in Scope. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), README changes, findings M3 and M6, and the Low findings of the same review.
