## Spec Review Result: 20261107-p1-hardening-before-main-pr.md (after Iteration 5)

### Summary
- Critical: 0, Warning: 7, Suggestion: 12
- Confidence gate: 92 PROCEED (Scope clarity 95, Root cause 95); no design change since Iteration 3c
- Phase 2 advisor calls used: 0 of 1 (none) — one candidate (active PR head moves after `--auto`; `--disable-auto` on run-wide BLOCKED) not escalated: Suggestion severity, and the spec accepts the behaviour explicitly (Edge Cases)

### Critical Issues
None.

### Warning Issues
1. [spec FR-3 :129-133] completeness:auto-intent-redundant (feasibility/simplicity) — persisted `auto_intent` has no consumer; resume reads live `autoMergeRequest,headRefOid` anyway — drop it and read `autoMergeRequest` before every `--auto` start.
2. [spec FR-3 :133, Edge Cases :225] consistency:stage3-add-vs-uncertain-exclusion — "any non-zero result … adds it to `stage3`" contradicts "left out of Stage 3" for uncertain PRs; Edge Case skips the re-read — limit the first sentence; add "after the re-read".
3. [spec FR-3 :131] completeness:resume-no-state-reread — resume read lacks `state`; a PR that CI-merged during the crash window is re-started, fails, lands in `stage3` and is reported Failed — read `state`, record MERGED/CLOSED; same for `stage3`/`ci_wait` entries.
4. [spec FR-3 :133] completeness:uncertain-pr-advances-lane — an `auto-merge-uncertain` PR still advances its lane, so two same-lockfile PRs can auto-merge concurrently — hold the lane, or move its remainder to `stage3`.
5. [spec FR-4 :167, AC4, NFR] completeness:finish-guard-order-not-regression-pinned — order (tip < merged < open < lease) is checked only by a one-off AC4 assert and the behavior test outside `validate.sh`; several sub-rules (url `-`, ls-remote exact line, fork-of-fork, open output `0`) unpinned — add an index-order test to `tests/codex_issue69_contract_test.py` and required clauses.
6. [codex/skills/ywc-merge-dependabot/SKILL.md:161,224-225] compat:run-wide-deadline-vs-pinned-161 — unpinned wording "for every rebase/CI wait … set one deadline at the start" and the Stage 2 `deadline=$(…+1800)` illustration contradict the run-wide rule — name them as FR-2 edit targets, keep pinned phrases.
7. [codex/skills/ywc-merge-dependabot/SKILL.md:167] compat:deadline-unreached-label-vs-167 — "Mark remaining PRs failed/stalled" vs `Skipped (deadline reached)` for never-started PRs — amend the unpinned part of :167 as an explicit edit target.

### Suggestions
1. [spec :110,129-151] feasibility:prose-state-machine-untested — note that 3b/resume/`ci_wait` are verified by source assertions only.
2. [spec :110,135] feasibility:deadline-throughput — README line: a rerun continues remaining PRs.
3. [spec AC0-AC7] [unverifiable-ac] — pipelines/test runs not re-executed; AC4 new grep matches baseline 0.
4. [spec :131 vs :133] consistency:resume-enabled-active-vs-leaving-lane — "leaving its lane" trigger on resume undefined.
5. [spec :215 vs :112] consistency:exit0-wait-vs-table — scope API row 0 to outside the post-rebase wait.
6. [spec :101,:120 vs :124] consistency:label-variants-outside-fr2-list — add the "auto-merge still enabled" variant; name the rebase-poll-exhaustion label.
7. [spec :60 vs :173-175] consistency:expected-traces-row-subset — add `open-pr`, `nonparseable`, `api-failure` to the row.
8. [spec :266] consistency:stale-confidence-gate — mark 89 as the original Step 3.6 score.
9. [spec :111,:130,:134] completeness:state-clear-points — `ci_wait`/`stage3` removal rules.
10. [spec :229,:102] security:active-pr-head-moves-after-auto — (advisor candidate, not escalated) consider `--disable-auto` for active PRs on BLOCKED / moved head.
11. [SKILL.md:163] compat:stage3-queue-vs-lanes — state `stage3` is the Stage 3 queue under the `active`/`lanes` rule.
12. [spec FR-3] compat:new-key-absent-vs-malformed — absent new key = empty, not malformed.

### Prior residual Warnings (Iteration 3c)
resolved: resolver-lazy-vs-opens-with, uncertain-trigger-vs-test, blocked-label-precedence, chunk-policy-gaps, stage3-list-unnamed, persisted-base-check-cache, auto-intent-lifecycle (write/clear/failed read), conflict-trigger-undefined, deadline-scope-sequential-stage3. Partly remaining: finish-guard-subrules-unpinned (clauses added; order and four sub-rules not regression-pinned — Warning 5).

### Completion Status
DONE
