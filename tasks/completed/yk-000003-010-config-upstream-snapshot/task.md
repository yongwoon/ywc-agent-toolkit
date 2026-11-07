# yk-000003-010-config-upstream-snapshot — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`
- [ ] `gh auth status` succeeds (primary source) or `~/.claude/skills/.develop-with-llm.manifest` exists (secondary source)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `${TMPDIR:-/tmp}/ywc-issue69-snapshot/**` (outside the repository; no repository file is modified)
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Create the snapshot root and the MANIFEST skeleton**
  - [ ] `mkdir -p "${TMPDIR:-/tmp}/ywc-issue69-snapshot"` and confirm its canonical path (`pwd -P`) is not inside the repository
  - [ ] Create `MANIFEST.md` with columns: upstream path | source (`gh api @2e323a97` / `installed bundle, commit unpinned` / `BLOCKED`) | status | consuming task id
- [ ] **Fetch the primary-source files**
  - [ ] For each path listed in README Scope run `gh api "repos/yongwoon/develop-with-llm/contents/<path>?ref=2e323a97" -H 'Accept: application/vnd.github.raw'` and write it to `<SNAP>/<path>`
  - [ ] Quote every path; treat non-zero exit or empty output as 'primary unavailable' for that path only
- [ ] **Fall back per path to the installed bundle**
  - [ ] Confirm `~/.claude/skills/.develop-with-llm.manifest` exists, then verify the file exists under `~/.claude/skills/<skill>/`
  - [ ] Do not copy; record the in-place path and `installed bundle, commit unpinned` in the MANIFEST
  - [ ] Spot-check the known installed-bundle anchors: `ywc-handoff`, `ywc-retro`, `ywc-create-pr/references/pr-body-features-api.md` (107 lines), `ywc-debug-rootcause/references/feedback-loop.md`, `ywc-finish-branch` 'Remote deletion guard', `ywc-auth-implement` `/ywc-plan --no-converge`
- [ ] **Mark unavailable paths BLOCKED**
  - [ ] Record `BLOCKED` plus the consuming task id; do not substitute remembered content
- [ ] **Report the result**
  - [ ] Write counts of ok / installed-bundle / BLOCKED rows and the MANIFEST path into Implementation Notes

## Acceptance Coverage
Covers: AC0

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `test -s "${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md"`
- [ ] `[ "$(find "${TMPDIR:-/tmp}/ywc-issue69-snapshot" -type f -empty | wc -l | tr -d ' ')" = 0 ]`
- [ ] `case "$(cd "${TMPDIR:-/tmp}/ywc-issue69-snapshot" && pwd -P)/" in "$(pwd -P)"/*) echo 'snapshot is inside the repo'; false;; esac`
- [ ] `grep -c 'BLOCKED' "${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md"` is reported in Implementation Notes (BLOCKED rows are surfaced, not hidden)

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->

- MANIFEST: `/var/folders/18/70q6vz3x36j5_n7fd3gvv5xc0000gp/T/ywc-issue69-snapshot/MANIFEST.md` (outside repo; TMPDIR may be cleaned — re-run this task if missing).
- Counts: 129 files total — ok via `gh api @2e323a97`: 129; installed bundle (in place): 0; BLOCKED: 0 (`grep -c BLOCKED MANIFEST.md` = 0).
- Layout: upstream keeps the `tools/claude-code/` prefix at `2e323a97`; snapshot mirrors it. Fetched SKILL.md + references/ + scripts/ only (no README locales, evals, prompts). `ywc-task-generator/SKILL.md` added beyond Scope because A2 edits it. `ywc-setup` = local `ywc-setup-language`.
- Anchors verified in snapshot: `pr-body-features-api.md` 107 lines; `ywc-finish-branch` Remote deletion guard at `:369`; `ywc-auth-implement` `--no-converge` at `:120`; `ywc-debug-rootcause/references/feedback-loop.md` present.
- Task Verify: all three commands passed (exit 0).
