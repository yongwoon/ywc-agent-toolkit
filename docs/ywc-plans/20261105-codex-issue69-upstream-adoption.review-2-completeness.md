# Completeness re-validation — Iteration 2

Status: DONE_WITH_CONCERNS
Critical: 0, Warning: 1, Suggestion: 0
Spec: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md
Outcome Oracle: complete.
Blind Spot action: proceed for source-only port scope; no live behavior is inferred from fixtures.

## Previous findings

- C-1 resolved: FR-10 lines 187–189 explicitly owns the agentic caller and --no-converge/profile preservation; AC-10 covers interactive/noninteractive precedence.
- W-1 resolved: immutable local and 13 upstream revisions plus bounded source paths now at lines 75–95.
- W-3 resolved: FR-4 lines 141–142 defines categories, priority, stable tie handling, owner fallback and empty result.
- W-2 materially addressed: concrete behavior test and fixture destinations, commands, schema adapter and source/live evidence distinction added at lines 224–239. Remaining narrow executable-seam ambiguity is below.

## W-1 — Warning — Completeness — deterministic polling/ref test seam remains undefined for Markdown-only decisions

- Target: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:239 (`Verification`).
- Evidence: the section makes helper-owned ref creation/checkout/remote-tip/failure execution and a fake-clock 1800-second boundary mandatory. Existing `codex/skills/ywc-worktrees/scripts/` contains audit-worktrees.sh, cleanup-worktree.sh and test-cleanup-worktree.sh; create is an LLM procedure in SKILL.md. `ywc-merge-dependabot/scripts/` contains only group-by-ecosystem.py; its polling is a partially descriptive fenced Bash example in SKILL.md:185–218, not a runtime helper. Line 237 correctly says Markdown-only decisions use contract fixtures and forbids creating an unrelated dispatcher. Therefore an implementer cannot tell which production callable is the required fake-clock polling/ref seam, or whether only static expectation comparison is intended. A new independent test implementation of the prose would test the test's own logic rather than the distributed skill.
- Improvement: enumerate the actual executable helper boundaries (e.g. cleanup/audit/state helpers) eligible for mandatory temporary Git tests. State that create/PR guards/polling remain source-assertion/expected-trace contracts unless an actual production executable snippet/helper is explicitly introduced. If testing the fenced polling snippet is desired, declare exact source extraction and executable-completeness contract; otherwise mark fake-clock boundary as contract expectation, not executed production behavior. This changes no requirement for live model proof and preserves the source-only product scope.
- Concrete clarifying question: Is polling an extracted executable production snippet or a Markdown decision contract? Current scope permits the latter, so resolve in Verification and AC evidence wording.

## Whole-spec omission checks

AC-1–10 map to FR-1–10. New Mission includes bounded durable-write approval and history; Retro/Handoff include source restrictions, paths/redaction; worktree includes pinned PR/cwd/branch/failure side effects. Status/model pins and advisory hints are separated. UI lenses N/A, security path/input/sensitive exposure covered. No new HTTP service or DB entity requires API/schema fields. Immutable snapshots and primary-source decisions are present. No other task-blocking Completeness gap identified.
