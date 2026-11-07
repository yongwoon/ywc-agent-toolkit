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
- [ ] `grep -qF -- '--json number --jq length' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- '--force-with-lease="refs/heads/$branch:$tip"' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- 'env -u GH_HOST gh repo view --json url,isFork,parent -- "$url"' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- '--repo "$parent"' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- '^[0-9a-f]{40}([0-9a-f]{24})?$' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- '^[A-Za-z0-9.-]+/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- '6. **Open-PR check**' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- 'git remote get-url --push --all origin' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- '2. **Pin the push target**' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- 'a fork of a fork returns `NEEDS_CONTEXT`' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- 'never interpolate `$base` or `$tip` into a `--jq` filter' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF -- 'A small window remains between step 6 and this push' claude-code/skills/ywc-finish-branch/SKILL.md`
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

Critical-review round (team-lead): High (new guard pieces lacked Task Verify coverage) and M-a..M-d plus Lows fixed at `SKILL.md:215-224` and `:28`:
- M-a: `--repo` is now always passed, bound to `origin` via `gh repo view "$(git remote get-url origin)" --json nameWithOwner,isFork,parent`; a fork also runs every check against its parent (shape is `parent.owner.login/parent.name`, confirmed with `gh repo view minio/cli`).
- M-b: deletion needs a merged row with `baseRefName == $base` and `headRefOid == $tip` (step 4) and an open count of `0` (step 5).
- M-c: one line maps each outcome to a status (`:224`, summarized at `:28`).
- M-d: numbered steps in run order; the open-PR check comes last, right before the lease-delete.
- Lows: `tip` and the repo values are shape-checked; the opening sentence now covers the lease-delete path; `$branch`/`$base` are tied to the validated `BRANCH`/`BASE`.
- Task Verify gained 7 `grep -qF --` checks (README.md and task.md); test.md gained Scenarios 3-5.

Security re-review round (team-lead) on d8a5d57a, fixed at `SKILL.md:217-223`:
- H1: new step 2 — `git remote get-url --push --all origin` must print exactly one line equal to `git remote get-url origin`. Reproduced in a scratch repo: `pushInsteadOf` rewrote the push URL to `git@evil:a/b.git`, and two `pushurl`s printed two lines, while the fetch URL stayed the same.
- M1: `repo`/`parent` now include the host (`<host>/<owner>/<name>`, from `gh repo view --json url`); every `gh` runs as `env -u GH_HOST gh … --repo`. Checked: `env -u GH_HOST gh pr list --repo github.com/yongwoon/ywc-agent-toolkit …` exit 0.
- M2: a fork of a fork returns `NEEDS_CONTEXT`.
- L1: `gh repo view --json … -- "$url"` puts flags before `--` (checked: `gh repo view -- "$url" --json url` fails with "accepts at most 1 arg(s), received 5") and the URL must not start with `-`.
- L2: compare `baseRefName`/`headRefOid` on the parsed JSON in-process or with `jq --arg`, never interpolated into `--jq`.
- L3: the guard now states that a small window remains between the open-PR check and the push.
- Task Verify: 3 greps updated, 5 added; test.md gained Scenarios 6-7.
