# Spec-ready loop log — 20261107-p1-hardening-before-main-pr

## Iteration 1/5 — 2026-11-07T02:15:59Z
- spec: docs/ywc-plans/20261107-p1-hardening-before-main-pr.md
- status: DONE_WITH_CONCERNS
- findings: Critical 6 / Warning 9 / Suggestion 11
- advisor: used 1 / remaining 3
- action: replan
- note: gate 90 PROCEED with Criticals; P2 advisor ruled the rebase-wait script out of the Codex port
- signatures:
  - Critical tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json:24 — fixture pins check-ref-format --branch contrary to AC4
  - Critical claude-code/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py:21-25 — test copy covers scripts absent from Codex and uses CLAUDE_SKILL_DIR
  - Critical codex/skills/ywc-merge-dependabot/SKILL.md:183-199 — manual conflict path ends in an unpinned merge
  - Critical codex/skills/ywc-merge-dependabot/SKILL.md:246-249 — Stage 2 lane advance starts --auto unchecked
  - Critical codex/skills/ywc-merge-dependabot/SKILL.md:278-280 — Stage 3 omits unconfirmed-base PRs
  - Critical codex/skills/ywc-merge-dependabot/SKILL.md:159-167 — wait-dependabot-rebase.sh incompatible with rebase_intent / one-deadline contract
  - Warning spec FR-3 — base-check persisted field undefined
  - Warning spec FR-2 — NEW_HEAD re-checks and merge-refusal restart contract missing
  - Warning codex/skills/ywc-finish-branch/SKILL.md:312 — open-PR check not last; merged check conditional
  - Warning spec AC4 / NFR — T2 guard has no RED test
  - Warning spec FR-5 — tag token boundary undefined
  - Warning codex/skills/ywc-merge-dependabot/SKILL.md:92-96 — new status labels missing from tables
  - Warning spec AC3 — codex_issue69_behavior_test.py not run by validate.sh
  - Warning claude-code/agents/CLAUDE.md:83 — stale line cite; validator file absent
  - Warning spec FR-3 vs CC Mode Selection — base-check placement drift

## Iteration 2/5 — 2026-11-07T02:25:36Z
- spec: docs/ywc-plans/20261107-p1-hardening-before-main-pr.md
- status: DONE_WITH_CONCERNS
- findings: Critical 1 / Warning 9 / Suggestion 14
- advisor: used 0 / remaining 3
- action: replan
- note: gate 91 PROCEED with a Critical; 2 advisor candidates not escalated — resolved by existing normative text (Codex SKILL.md:165, shared-script-resolution.md)
- signatures:
  - Critical spec FR-2 conflict path — no CI wait on the rebased head; every rebased PR would be skipped as pending
  - Warning codex/skills/ywc-merge-dependabot/SKILL.md:96 — pending row lacks the parallel-auto hand-off; no all-unconfirmed sequential fallback
  - Warning spec FR-3 — stale base_check rule applied to already-started PRs without --disable-auto
  - Warning spec FR-3 — crash window after --auto accepted, before snapshot
  - Warning spec FR-4 — CC guard sub-rules dropped (shape check, ls-remote rule, parent runs, outcomes)
  - Warning tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json — traces encode old order; empty-open-pr allowed without a merged row
  - Warning codex/skills/references/shared-script-resolution.md — normative resolver contract unacknowledged (count pin 20)
  - Warning spec AC4 — behavior test, the only reader of expected-traces.json, not run
  - Warning spec AC1 / FR-1 — trimmed test copy would leak the wait-dependabot-rebase name
  - Warning spec FR-5 — tag token rule breaks on quotes and trailing comments

## Iteration 3/5 — 2026-11-07T02:32:46Z
- spec: docs/ywc-plans/20261107-p1-hardening-before-main-pr.md
- status: DONE
- findings: Critical 0 / Warning 12 / Suggestion 16
- advisor: used 0 / remaining 3
- action: apply-suggestions
- note: gate 92 PROCEED, no Critical; one suggestion pass ran (Suggestions only; pre-existing Warnings not chased)
- signatures:
  - Warning spec FR-3 — auto_intent lifecycle (clear points, failed read) undefined
  - Warning spec FR-2 — restart cap not persisted across chunks
  - Warning spec FR-2 — conflict trigger undefined after manual path removal
  - Warning spec FR-3 — Skipped (deadline reached) vs pinned "incomplete work is failed" clause
  - Warning spec FR-4 — fork/parent, tip shape, residual-window sub-rules not fixture-pinned
  - Warning codex/skills/ywc-merge-dependabot/SKILL.md:161 — deadline scope (run-wide vs per wait) for sequential/Stage 3
  - Warning spec FR-3 — base_check persistence removable (simplicity)
  - Warning codex/skills/ywc-merge-dependabot/SKILL.md:90 — Step 2 intro skip rule not named
  - Warning codex/skills/ywc-finish-branch/SKILL.md:83-88 — Step 1 BRANCH/BASE validation unported, not deferred
  - Warning spec FR-3 — resolver preamble per block unspecified
  - Warning spec Existing Constraints :159-167 row — persisted entries list drift; ci_wait resume edge case
  - Warning spec Scope — T0 SKILL.md edits and T1/T2/T3 ownership / plugins regeneration not stated

## Iteration 3b (suggestion re-validation) — 2026-11-07T02:38:18Z
- spec: docs/ywc-plans/20261107-p1-hardening-before-main-pr.md
- status: DONE_WITH_CONCERNS
- findings: Critical 1 / Warning 22 / Suggestion 24
- advisor: used 0 / remaining 3
- action: repair-suggestion-regression
- note: pass-introduced keys only (every Critical counts); repair pass = spec Amendment Log Iteration 4; not counted toward --max-iterations
- signatures:
  - Critical spec AC7 — whole-run git-range exceeds ywc-impl-review Step 2.5 hard block (225 files, +7028/-848)
  - Warning spec AC7 — --depth flag does not exist
  - Warning spec AC7 vs FR-6 — PR #214 vs replacement-PR fallback
  - Warning spec FR-5 — leading-comment rule outside the numbered procedure
  - Warning spec FR-2 — no-checks vs CI-timeout label precedence at the deadline
  - Warning spec FR-2/FR-3 — resolver failure scope in 3b (run-wide vs per-PR), unlabeled unprocessed PRs
  - Warning spec FR-1 — lane-state.md fallback could move fixture-pinned text
  - Warning spec FR-3 — auto-merge-uncertain trigger undefined
  - Warning spec FR-3 / NFR — SkillContractTest misses new guards

## Iteration 3c (repair re-validation) — 2026-11-07T02:43:06Z
- spec: docs/ywc-plans/20261107-p1-hardening-before-main-pr.md
- status: DONE
- findings: Critical 0 / Warning 10 / Suggestion 30
- advisor: used 0 / remaining 3
- action: handoff
- note: gate 92 PROCEED, Critical 0 after the repair pass; residual warnings listed below (not chased per Step 4); ywc-task-generator not invoked
- signatures:
  - Warning spec FR-2/FR-3 — resolver lines "lazy" (3a) vs "opens with" (FR-3, SkillContractTest)
  - Warning spec FR-3 — auto-merge-uncertain triggers vs test; definite --match-head-commit refusal vs transport failure
  - Warning spec FR-2 — run-wide BLOCKED label precedence vs terminal / uncertain labels
  - Warning spec FR-6/AC7 — chunk coalescing, empty-range NEEDS_CONTEXT, findings fixed at tip
  - Warning spec FR-3 — persisted Stage 3 list unnamed
  - Warning spec FR-3 — base_check persistence removable (simplicity)
  - Warning spec FR-3 — auto_intent lifecycle / clear points (pre-existing)
  - Warning spec FR-2 — conflict trigger (mergeable / mergeStateStatus) undefined (pre-existing)
  - Warning codex/skills/ywc-merge-dependabot/SKILL.md:161 — deadline scope for sequential / Stage 3 waits (pre-existing)
  - Warning spec FR-4 — finish-guard sub-rules and unconditional merged check not fixture-pinned (pre-existing)

## Iteration 5 (user-requested warning cleanup + re-validation) — 2026-11-07
- spec: docs/ywc-plans/20261107-p1-hardening-before-main-pr.md
- step 1: /ywc-plan --update-spec (Re-plan Mode) — Amendment Log Iteration 5; Open Question A marked accepted by the user on 2026-11-07; 10 residual Warnings addressed; duplicate-claim sweep + Step 4b.5 re-run
- step 2: /ywc-spec-validate --advisor-budget 1 → review: docs/ywc-plans/20261107-p1-hardening-before-main-pr.review-5.md
- status: DONE
- findings: Critical 0 / Warning 7 / Suggestion 12
- advisor: used 0 / budget 1 (one Suggestion-level candidate not escalated)
- action: report (no further loop, per team-lead)
- note: 9/10 prior Warnings resolved; finish-guard pinning partly remaining; 7 Warnings, mostly new and from the Iteration 5 edits, not chased
- signatures:
  - Warning spec FR-3 — auto_intent persisted but unconsumed (simplicity)
  - Warning spec FR-3 — stage3 "any non-zero" vs uncertain exclusion; Edge Case skips re-read
  - Warning spec FR-3 — resume read lacks PR state (merged during crash window)
  - Warning spec FR-3 — auto-merge-uncertain PR still advances its lane
  - Warning spec FR-4 — guard order / sub-rules not regression-pinned in validate.sh
  - Warning codex/skills/ywc-merge-dependabot/SKILL.md:161,224-225 — per-wait deadline wording vs run-wide rule
  - Warning codex/skills/ywc-merge-dependabot/SKILL.md:167 — "failed/stalled" vs Skipped (deadline reached)
