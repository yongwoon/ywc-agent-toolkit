# yk-000010-060-test-reviewer-trigger-coverage — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] `yk-000010-010-domain-scan-secrets-hunk-filter` is completed (merged)
- [ ] `yk-000010-020-domain-merge-dependabot-hardening` is completed (merged)
- [ ] `yk-000010-030-domain-retro-readonly-lenses` is completed (merged)
- [ ] `yk-000010-040-domain-finish-branch-guard-review` is completed (merged)
- [ ] `yk-000010-050-docs-metadata-followups` is completed (merged)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `.claude/skills/ywc-toolkit-eval/scripts/score.py`
  - `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`
  - `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] List the 9 items and their counts (read `score.py`'s coverage code to print them).
- [ ] For each item, decide: (a) add real cases only from an actual source (`session-trace` / `user-prompt` with a citable origin) — never synthesize a source; or (b) if the item's description says a user-typed request belongs to another skill (dispatch-only), exempt it from the positives minimum in `score.py` via an explicit, documented list or a frontmatter-derived rule, still requiring its collision cases. Record each decision as a Ruling.
- [ ] Do not lower the global minimums.
- [ ] Run `score.py --ci` last and stage the auto-updated `history.mechanical.json` (this task runs after all Wave 1 tasks so the baseline covers them).
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci 2>&1 | grep -q '0 items below minimum\|coverage.*OK'` — or, if exemptions are used, the report names each exempt item
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
- Premise: 10 of 65 (not 9 of 64) — Wave 1 added dispatch-only agent `ywc-retro-lens`.
- Below-minimum list before change (positives/collisions, independent only): ywc-handoff 0/0, ywc-merge-dependabot 0/0, ywc-retro 0/0, ywc-setup-language 0/0 (all `disable-model-invocation: true`); ywc-mine-review-history 0/0; ywc-go-reviewer 0/1, ywc-python-reviewer 0/0, ywc-typescript-reviewer 0/0, ywc-retro-lens 0/0 (dispatch-only agents); ywc-performance-engineer 3/1.
- score.py now prints `[coverage] exempt (<reason>): <item>` and `[coverage] below minimum: <item>` lines to stderr.
- Exemption is derived from the item's own frontmatter (`apply_coverage_exemption`): slash-only skills waive both floors; dispatch-only agents (description says "no natural-language triggers" or a user-typed review request is owned by ywc-impl-review) waive only positives and still need >= 2 independent collisions.
- 8 new collision cases reuse verbatim prompts from existing `user-prompt` cases (origin id cited in each `note`); only the sibling label is new. No new prompt text was written.
- Residual: `ywc-mine-review-history` stays below minimum (0/0). No real prompt exists in the repo and no rule-based exemption applies; left open rather than invented.
