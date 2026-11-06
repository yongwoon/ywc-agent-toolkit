# yk-000010-040-domain-finish-branch-guard-review — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] Run a focused security review of `claude-code/skills/ywc-finish-branch/SKILL.md` Step 5 Remote deletion guard (~line 215) and every block that deletes a branch or relies on the "merged" judgement (Steps 5 and 8). Lenses: open-PR check failure modes, `gh pr list` result parsing, `headRefOid` vs `ls-remote` tip comparison, fork PRs (same head name, different owner), and multiple PRs for one head.
- [ ] yk-000009-010 already moved the guard to the C2 `refs/heads/` form and quoted `BASE`/`BRANCH`; do not redo those. List each remaining Medium+ finding in Implementation Notes with file:line, then fix it in place.
- [ ] If none of the four can be reproduced, record that as a Ruling with the review evidence; do not invent changes.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep -q 'Remote deletion guard' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF 'git check-ref-format "refs/heads/$branch"' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-finish-branch/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->

Review of `claude-code/skills/ywc-finish-branch/SKILL.md:215` (Step 5 Remote deletion guard; Step 8 references it at :276-282, which only runs `git branch -d` and needs no change):

- M1 (Medium, fixed) :215 — open-PR check `gh pr list --head "$branch" --state open` had no `--json`, so "parsed result is empty" was undefined for text output. Now `--json number --jq length` must print exactly `0`.
- M2 (Medium, fixed) :215 — both `gh pr list` queries used gh's implicit repo pick, while `ls-remote` / deletion target `origin`. With origin = fork and gh default = the fork, an open upstream PR from this head is invisible, so the open check reads empty and deletion closes it. Now `--repo` of the base repository is required when more than one remote exists; undeterminable → `NEEDS_CONTEXT`.
- M3 (Medium, fixed) :215 — `git ls-remote origin "refs/heads/$branch"` tail-matches patterns; reproduced locally: it printed both `refs/heads/foo` and `refs/heads/x/refs/heads/foo`. "Equals the current remote tip" was undefined for multi-line or empty output. Now the tip is the single line whose ref is exactly `refs/heads/$branch`; zero/ambiguous → stop and report.
- M4 (Medium, fixed) :215 — TOCTOU: a push between the tip comparison and the deletion was lost. Now deletion uses `git push --force-with-lease="refs/heads/$branch:$tip" origin --delete "refs/heads/$branch"`; reproduced locally: stale lease rejected (exit 1, "stale info"), matching lease deleted (exit 0).
- L1 (Low, no change) — `--limit` default 30: truncation cannot turn a non-empty open result into `0`; on the merged query it can only hide a matching row, which yields "stop and report" (fail-safe).
- L2 (Low, no change) — fork PRs with the same head name (`--head` matches name only): on the open check they cause a false stop (fail-safe); on the merged check a matching row also requires `headRefOid` == origin tip, so the tip commit really was merged into the intended base.
- M1 also applied to the Rationalization Defense row at :28, which restated the old check.
- L3 (Low, no change) — multiple PRs per head: the guard already requires "a row" matching both base and tip, and states `gh pr view` cannot settle it.
