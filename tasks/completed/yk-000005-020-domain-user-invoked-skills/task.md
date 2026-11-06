# yk-000005-020-domain-user-invoked-skills — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yk-000005-010-domain-skill-path-convention` is completed (merged)
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-merge-dependabot/SKILL.md`
  - `claude-code/skills/ywc-merge-dependabot/README*.md`
  - `claude-code/skills/ywc-setup-language/**`
  - `claude-code/skills/ywc-skill-author/**`
  - `claude-code/skills/CLAUDE.md`
  - `CLAUDE.md`
  - .claude/skills/ywc-toolkit-eval/**
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Record the BEFORE gate**
  - [ ] Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` and note PASS
- [ ] **Convert the two skills**
  - [ ] Add `disable-model-invocation: true` and a one-line description to both SKILL.md files
  - [ ] Add the user-invoked blockquote to README.md (ko), README.en.md, README.ja.md, README.ko.md of each skill
  - [ ] Update `cross-skill-graph.md:52,78,157` and `language-resolution.md:108`
- [ ] **Write the policy**
  - [ ] Add the exception sentence at root `CLAUDE.md:88` and `claude-code/skills/CLAUDE.md:83`; add rule A16 and `## Writing Levers` to `ywc-skill-author/SKILL.md`
- [ ] **Update validators and tests**
  - [ ] Skip A2/A3/A4 for `disable-model-invocation: true` in `validate-skill.sh` and `score.py`; keep S2 = 5 for both skills
  - [ ] Add one `test_score.py` case; run it
- [ ] **Fix eval fixtures**
  - [ ] Re-grep `merge-dependabot\|setup-language` in `trigger-cases.json`; remove or relabel each case; run `test_fixture_schema.py`
- [ ] **Record the AFTER gate and commit the baseline**
  - [ ] Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` (PASS) and include the updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

## Acceptance Coverage
Covers: AC12 (2 skills), AC13, FR8

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` BEFORE editing and record PASS in Implementation Notes
- [ ] `[ "$(grep -l '^disable-model-invocation: true' claude-code/skills/*/SKILL.md | wc -l | tr -d ' ')" = 2 ]`
- [ ] `[ "$(grep -c 'user-invoked' claude-code/skills/ywc-skill-author/references/cross-skill-graph.md | tr -d ' ')" -ge 2 ]`
- [ ] `grep -q 'A16' claude-code/skills/ywc-skill-author/SKILL.md`
- [ ] `[ "$(grep -c -- '^## Writing Levers' claude-code/skills/ywc-skill-author/SKILL.md | tr -d ' ')" = 1 ]`
- [ ] `grep -q 'disable-model-invocation' claude-code/skills/ywc-skill-author/scripts/validate-skill.sh`
- [ ] `grep -q 'disable-model-invocation' .claude/skills/ywc-toolkit-eval/scripts/score.py`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` (AFTER; must PASS) and stage the updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-skill-author/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

- BEFORE `score.py --ci`: PASS (62 items, 2 coverage items below minimum). AFTER: PASS (62 items, 3 coverage items below minimum — the two skills' independent positives became negatives; coverage is informational, not a gate).
- `history.mechanical.json` was rewritten by `--ci` but is byte-identical (no axis changed), so there is nothing to stage.
- `language-resolution.md` lives at `claude-code/skills/references/`, outside the declared Ownership; edited one line because Scope names it.
- Snapshot Writing Levers hunk: dropped "See Semantic Packing above for the boundary" (no such section locally, FR3).

<!-- Starts empty at generation time. -->
