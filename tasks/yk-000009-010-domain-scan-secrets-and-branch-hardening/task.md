# yk-000009-010-domain-scan-secrets-and-branch-hardening — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read `claude-code/skills/ywc-worktrees/SKILL.md` `--existing-branch` bullet (C2 rule)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a caller depends on `--committed X --staged` meaning staged-only (grep `scan-secrets.sh` callers in `claude-code/skills/` and `codex/skills/`)
- [ ] Stop if required changes spill outside Ownership

## Implementation Steps
- [ ] **Tests first (both copies, byte-identical)**: add the 4 new cases from Scope 3; show them RED
- [ ] **Flag order (Scope 1)**: `--staged` never downgrades `--committed`; both copies
- [ ] **Phase 1/2 git errors (Scope 2)**: capture git output, exit 2 on failure; `|| true` only on grep; both copies
- [ ] **Mutation check**: remove each new guard in a scratch copy outside the repo and confirm the suite fails
- [ ] **C2 form (Scope 4)**: `check-ref-format "refs/heads/…"` in finish-branch Step 5 guard and pr-conflict-resolution
- [ ] **Parallel base refresh (Scope 5)**: `BASE` / `BRANCH` variables, C2 validation, quoting, `git -C "<worktree-path>"`
- [ ] **Final gate**: Task Verify, `bash scripts/validate.sh`, `score.py --ci`

## Acceptance Coverage
Covers: Scope 1-6

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `bash claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `bash codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `cmp claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `cmp codex/skills/ywc-create-pr/scripts/scan-secrets.sh plugins/ywc-agent-toolkit/skills/ywc-create-pr/scripts/scan-secrets.sh`
- [ ] `[ "$(grep -c '2>/dev/null || true' claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh | tr -d ' ')" = 0 ]`
- [ ] `[ "$(grep -c 'check-ref-format --branch' claude-code/skills/ywc-finish-branch/SKILL.md claude-code/skills/references/pr-conflict-resolution.md | awk -F: '{s+=$2} END{print s}')" = 0 ]`
- [ ] `[ "$(grep -c 'git -C ../worktree-<task-name>' claude-code/skills/ywc-parallel-executor/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `grep -qF 'git fetch origin "$BASE"' claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit if it changed
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-finish-branch/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`, includes shellcheck)
- [ ] typecheck: N/A
- [ ] unit tests: both `test-scan-secrets.sh` suites
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->

- RED: of the 5 new cases, 4 failed against the old script (`--committed main --staged` → 0; `git status` / `git diff --cached` / unstaged `git diff` failure → 0). `--staged --committed main` already passed and is kept as a regression guard for the fixed flag order.
- Mutation check (scratch copies): restoring `MODE="staged"` on `--staged`, or `|| true` on any of the three Phase 1/2 git calls, turns the suite red (4/4 killed). The suite has 17 cases and is byte-identical in the Claude Code and Codex copies.
- `--staged` is now a no-op flag: Phases 1-2 always run, and no caller combines the two flags (grep of `claude-code/skills` and `codex/skills`).
- Scope 5 premise correction: this repo's `ywc-parallel-executor/SKILL.md` still names the task worktree `../worktree-<task-name>` everywhere (Step 4a creates it there), so `<worktree-path>` would be undefined in this file. The base-refresh block holds that path in `WT` and quotes it. The stale-path Task Verify was narrowed from any `worktree-<task-name>` to the unquoted `git -C ../worktree-<task-name>` form.
