# yk-000004-050-domain-scan-secrets-guard — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yk-000004-040-domain-create-pr-features-api` is completed (merged)
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-create-pr/scripts/**`
  - `claude-code/skills/ywc-create-pr/SKILL.md`
  - `claude-code/skills/CLAUDE.md`
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
- [ ] **Measure the baseline**
  - [ ] In a scratchpad temp directory run the current script outside a work tree, in a bare repo and with an unresolved path; paste exit codes into Implementation Notes
- [ ] **Change the script**
  - [ ] Add the not-a-work-tree / bare-repo guard returning exit 2 with a stderr message; update the header comment `:9-13`
- [ ] **Add the abridged test**
  - [ ] Create `test-scan-secrets.sh` (755) with the three cases; every temp repo setup uses `env -u GIT_DIR -u GIT_INDEX_FILE -u GIT_WORK_TREE`
  - [ ] Run `shellcheck` and fix findings (scandir `claude-code/skills` lints it automatically)
- [ ] **Register and document**
  - [ ] Add `-f` check + `bash` execution in `scripts/validate.sh` `check_cc_support_dirs` beside the poll test loop (`:721-731`)
  - [ ] Update the `claude-code/skills/CLAUDE.md` row and add the exit 0/1-only rule to `ywc-create-pr/SKILL.md`

## Acceptance Coverage
Covers: AC8

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `bash claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `d=$(mktemp -d) && (cd "$d" && bash "$OLDPWD/claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh" --staged; test $? -eq 2)`
- [ ] `[ "$(grep -c 'BLOCKED' claude-code/skills/ywc-create-pr/SKILL.md | tr -d ' ')" -ge 3 ]`
- [ ] `[ "$(grep -c 'test-scan-secrets' scripts/validate.sh | tr -d ' ')" -ge 1 ]`
- [ ] `[ "$(grep -c 'test-scan-secrets' .github/workflows/validate.yml | tr -d ' ')" = 0 ]`
- [ ] `shellcheck claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-create-pr/SKILL.md`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
