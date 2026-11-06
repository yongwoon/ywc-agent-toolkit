# yk-000005-040-domain-merge-dependabot-workflow — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yk-000005-030-refactor-skill-script-paths` is completed (merged)
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-merge-dependabot/**`
  - `claude-code/skills/CLAUDE.md` (scripts table rows)
  - `scripts/validate.sh`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Port the scripts and test**
  - [ ] Copy the four scripts and the test from the snapshot unchanged except FR3 name/path mapping; set mode 755
  - [ ] Run the test locally (no network)
- [ ] **Add base-branch validation to SKILL.md**
  - [ ] Insert the allowlist + `git check-ref-format --branch` step before any use of `baseRefName`
  - [ ] Define the 'cannot confirm → sequential pass' path using the snapshot wording
- [ ] **Port the workflow safeguards**
  - [ ] Required-check gate, CI failed/pending split, Dockerfile-only `FROM` detection, single rebase comment, polling chunk constants, major-bump skip
  - [ ] Replace `/path/to/` references (`:118,121`) with the B1 convention
- [ ] **Register tables and tests**
  - [ ] Add table rows in `claude-code/skills/CLAUDE.md`; register the test in `scripts/validate.sh`; run `shellcheck` on both `.sh` scripts
- [ ] **Update READMEs**
  - [ ] Add 1–2 sentences to README.md (ko), README.en.md, README.ja.md, README.ko.md of `ywc-merge-dependabot` (keep the B3 user-invoked blockquote)

## Acceptance Coverage
Covers: AC13b

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `python3 claude-code/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py`
- [ ] `for f in poll-merge-queue.py wait-dependabot-rebase.sh detect-dockerfile-from.sh detect-major-bump.py test_merge_dependabot_scripts.py; do test -x claude-code/skills/ywc-merge-dependabot/scripts/$f || exit 1; done`
- [ ] `grep -q 'chunk_deadline' claude-code/skills/ywc-merge-dependabot/scripts/poll-merge-queue.py`
- [ ] `for k in required_status_checks baseRefName check-ref-format; do grep -q "$k" claude-code/skills/ywc-merge-dependabot/SKILL.md || exit 1; done`
- [ ] `[ "$(grep -c -- '/path/to/' claude-code/skills/ywc-merge-dependabot/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `shellcheck claude-code/skills/ywc-merge-dependabot/scripts/wait-dependabot-rebase.sh claude-code/skills/ywc-merge-dependabot/scripts/detect-dockerfile-from.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-merge-dependabot/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
