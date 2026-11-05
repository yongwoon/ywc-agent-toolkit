# Feasibility review — iteration 2

Spec: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md
Dimension: Feasibility
Independent source review; no implementation or spec commands executed.

## Resolved prior findings

- F-1 resolved at FR-1 (:119–121), Module Boundaries (:105), existing-constraints caller note (:95): tiers are advisory metadata owned by existing task-metadata-rules.md; the absent runtime-routing reference is explicitly identified as absent and no new executor dispatcher/model selection is introduced. Existing specialist profiles and installer fallback remain unchanged.
- F-2 resolved at Verification (:235–239): unique numeric skill IDs, preserved string source_id, non-empty agent expectations, source fixtures, test runner ownership, and evidence grade are explicit. Existing schema validators support this adaptation. Future tests/codex_issue69_behavior_test.py and fixture paths are deliberately declared new artifacts rather than claimed to exist.

## Outcome Oracle / Blind Spot

The target, quality threshold, evidence and stop contract are explicit. Upstream immutable revisions are now recorded. Static source assertions/schema validation, existing helper execution and optional live traces are distinguished. The missing-runtime-routing assumption no longer changes implementation scope.

## Suggestion F-S1 — Clarify Markdown recipe execution in the behavior harness

- Location: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:239.
- Evidence: merge-dependabot's polling procedure is currently an illustrative fenced Bash block in SKILL.md; its scripts directory contains group-by-ecosystem.py, not a polling runtime. Worktree creation/fetch are also Markdown instructions; existing worktree scripts implement audit/cleanup. Line 237 correctly limits executable helpers and keeps Markdown-only decisions as contract evidence, while line 239 additionally requires fake-clock deadline execution.
- Improvement: State that tests may execute bounded source command recipes/snippets against fake date/sleep/gh and temporary Git when the recipe is executable, labeling that recipe evidence rather than model traces; placeholders and LLM decisions stay instruction-only. Alternatively identify a deliberately owned pure test oracle for the deadline boundary. Do not introduce a new production dispatcher solely for test coverage.
- Severity rationale: This is a precision suggestion, not a feasibility blocker; a bounded test-only harness can validate command recipes using the current toolchain without runtime redesign. Existing source/helper-vs-model distinction prevents false live-PASS claims.

Critical: 0, Warning: 0, Suggestion: 1
Advisor candidates: none.
Status: DONE
