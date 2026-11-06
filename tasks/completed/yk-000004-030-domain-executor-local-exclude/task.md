# yk-000004-030-domain-executor-local-exclude — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-sequential-executor/**`
  - `claude-code/skills/ywc-parallel-executor/**`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Extract long sections first (NFR1)**
  - [ ] Pick one long self-contained section per executor (e.g. Operational Self-Improvement, State Init details) and move it to a new `references/*.md` (≥30 lines)
  - [ ] Link the new file by name from the SKILL.md body; confirm both bodies end ≤490 lines before continuing
- [ ] **Switch ignore handling to the repo-local exclude**
  - [ ] Replace the echo-append and prose sites listed in Scope with a `git rev-parse --git-path info/exclude` based append that is idempotent
  - [ ] On failure to resolve or write, report `BLOCKED`
- [ ] **Apply the learnings and dry-run rules**
  - [ ] Replace 'Add the file to `.gitignore`' for `.ywc-learnings.jsonl` in both `SKILL.md:482` sites
  - [ ] State `--dry-run` runs only read-only parts; fix the 'four layers' wording
- [ ] **Review-only reference corrections**
  - [ ] Correct Step numbers in `advisor-escalation.md`, make `--pr-lang` conditional in `aggregate-pr.md`, fix publish/prune targets in `worktree-run.md`; record before/after quotes

## Acceptance Coverage
Covers: AC9, NFR1

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `[ "$(grep -rn '>> .gitignore' claude-code/skills | grep -c 'ywc-run-state\|ywc-learnings' | tr -d ' ')" = 0 ]`
- [ ] `[ "$(grep -rn 'git-path info/exclude' claude-code/skills | wc -l | tr -d ' ')" -ge 2 ]`
- [ ] `[ "$(grep -rn 'Add the file to `.gitignore`' claude-code/skills | wc -l | tr -d ' ')" = 0 ]`
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] Review-only: quote the before/after of the 'four layers', `--pr-lang`, advisor-escalation Step numbers and worktree-run lines in Implementation Notes
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

- Extraction: moved the Completion Report body (task list, `--terse`, symbols) of each executor into new `references/report-format.md` (named `report-format.md`, not `completion-report.md`, because the upstream file of that name does not exist locally and its `DONE` definition change is out of scope). Bodies: sequential 498 -> 485, parallel 496 -> 477.
- Exclude wiring: State Init in both SKILL.md files and sequential `checkpoint-resume.md` §6 now append to `git rev-parse --git-path info/exclude` (idempotent, `BLOCKED` on resolve/write failure); learnings sites point to the same exclude file. `.ywc-learnings.jsonl` is also added at State Init.
- `--dry-run` (sequential): before `perform Pre-flight and Task Resolution as usual` / after `perform only the read-only parts of Pre-flight and Task Resolution — skip State Init ..., any persistence of the Pre-flight 5 URL-policy decision, and any resume prompt`. Parallel executor has no `--dry-run`.
- Four layers: Step 4 before `Run verification in three layers` / after `Run verification in four layers` (the list has 4 items and Definition of Done already said four).
- `--pr-lang` (`aggregate-pr.md`): before `--pr-lang <pr-lang>` / after `[--pr-lang <pr-lang>]   # include only when the user passed --pr-lang; otherwise omit it`; the `/ywc-create-pr` example drops the unconditional `--lang <pr-lang> \` line and states when to add it.
- advisor-escalation: before `(Step 6a, --local-merge mode)` and `(Step 6, normal mode)` / after `(Step 5, delivered by ywc-finish-branch; this skill no longer owns it)` for both.
- worktree-run: prune target before `--branch work/<name>` / after `--branch integration/run-<slug>` (aggregate-pr) with the rationale sentence; added the "Publish a newly created integration branch (PR modes only)" paragraph. The upstream sentence naming the SKILL.md "Base branch not yet on origin" stop was dropped: that stop does not exist locally (FR3).
- Not ported: upstream `--worktree` fetch variant, Docker isolation, baseline §3.5, `<skill-base-dir>` path forms (B2 owns path forms).
