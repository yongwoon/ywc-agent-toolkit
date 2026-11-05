# yk-000005-010-domain-skill-path-convention — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yk-000004-050-domain-scan-secrets-guard` is completed (merged)
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/CLAUDE.md`
  - `claude-code/skills/ywc-skill-author/SKILL.md`
  - `claude-code/skills/ywc-skill-author/references/cross-skill-graph.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Write the convention section**
  - [ ] Add items (a)–(e) to `claude-code/skills/CLAUDE.md` using the snapshot wording, with FR3 name mapping
- [ ] **Build the pair table from evidence**
  - [ ] Run a grep for cross-skill script references (`../ywc-` and `ywc-x/scripts` forms) and list only confirmed pairs
  - [ ] Add the 'skill invocation' column for dependencies by invocation rather than script path
- [ ] **Add rule B9**
  - [ ] Add the B9 row to `ywc-skill-author/SKILL.md` and mirror in `cross-skill-graph.md`, worded as 'repo-relative script path'
- [ ] **Add the Bundled Scripts scope sentence**
  - [ ] One sentence under the Bundled Execution Scripts table limiting it to shared scripts

## Acceptance Coverage
Covers: AC11b

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep -q 'Skill-local script paths' claude-code/skills/CLAUDE.md`
- [ ] `[ "$(grep -c -- '^| B9' claude-code/skills/ywc-skill-author/SKILL.md | tr -d ' ')" = 1 ]`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-skill-author/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
