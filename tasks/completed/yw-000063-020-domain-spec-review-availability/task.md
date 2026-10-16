# yw-000063-020-domain-spec-review-availability — Implementation Checklist

## Prerequisites

- [ ] `yw-000063-010-domain-event-monitoring` is completed, accepted and present in the merged baseline.
- [ ] Read the primary plan sections and this README; preserve Stage 1 → Stage 2 → Stage 3 acceptance gates.

## Allowed Edit Scope

- [ ] Treat README Ownership as the operational edit boundary, including exact generated copies, fixtures and shared-runner edits.
- [ ] Edit source first; generated marketplace files come only from synchronization. Other tasks and existing user edits must be preserved.

## Stop Conditions

- [ ] Stop on an unmerged/unaccepted predecessor, missing input contract, changed spec, or ownership spill.
- [ ] Stop if concurrent shared-script/catalog/package edits cannot be reconciled within Ownership; report the conflicting task.
- [ ] Return NEEDS_CONTEXT for contract/signature/consumer disagreement; do not invent a canonical function signature from prose.
- [ ] Do not claim implementation completion with failed required evidence, unresolved Critical/High findings, or missing mandatory live selections.

## Hardening Gate

- [ ] Classify as behavior-changing skill-contract work with focused offline test coverage; record RED-first failure, named existing coverage or a justified exception before production edits.
- [ ] Record cross-task input/output/error expectations from spec Module Boundaries and FR sections; preserve identity, status, preview and artifact authority.
- [ ] Data Integrity: N/A for runtime data writes; no state-schema change. If scope unexpectedly introduces mutable state, stop and apply `codex/skills/references/data-integrity-hardening.md` before expanding scope.
- [ ] Require stage implementation review with no unresolved Critical/High findings.

## Implementation Steps

- [ ] Extend the bounded read-only worker exception.
  - [ ] Update codex/skills/references/subagent-status-actions.md for explicitly designated spec-review dimension workers using captured canonical identity, Status, one-line Summary, at most five confirmed findings and two advisor candidates.
  - [ ] Retain bounded concern/blocker/context fields; disallow artifact writes or promises, fabricated terminal results, and identity derived from requested labels.
- [ ] Gate aggregation on availability evidence.
  - [ ] Wire codex/skills/ywc-spec-validate/SKILL.md to the shared monitor before aggregation/Phase 2; possibly-live lanes return BLOCKED and prevent aggregation, direct fallback, and handoff.
  - [ ] For proved-quiescent unavailable lanes, review each affected dimension once with the same rubric and record target, elapsed time, final roster state, evidence category, direct result, and degraded coverage.
  - [ ] Keep failed dispatch/missing identity on existing failure handling; distinguish no-delegation inline review and preserve all four review dimensions.
- [ ] Prove fallback boundaries.
  - [ ] Extend the focused runner, contract assertions and availability fixtures for quiescent, possibly-live, API-error, escalation-completion, missing-target and no-delegation cases.
  - [ ] Record an optional real delegated-review observation when available; otherwise explicitly retain the live-evidence gap.
- [ ] Preserve distribution and localized usage evidence.
  - [ ] Update affected README.md / README.en.md / README.ja.md / README.ko.md and maintained README.zh.md / README.es.md deltas within Ownership; retain agents/openai.yaml and two-field frontmatter.
  - [ ] Run `bash scripts/sync-codex-plugin.sh` from source; inspect generated copies, reject unrelated deltas, and run Task Verify before stage acceptance.

## Task Verify

- [ ] `python3 tests/codex_issue69_contract_test.py`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/check-codex-skill-descriptions.sh`
- [ ] `bash scripts/check-codex-agent-evals.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] Record M1, M2 scenario evidence in `test.md`; map the covered IDs from README to actual assertions or manual observations.

## Verification

- [ ] Required repository check: `bash scripts/validate.sh` passes after package synchronization; its installed-asset checks use temporary destinations.
- [ ] Source-only and fixture assertions are labeled separately from live behavior; missing measurements are explicit gaps.
- [ ] Confirm no Claude Code, version/release metadata or unrelated source changes; frontmatter/locales/agents metadata remain intact.
- [ ] Typecheck/application build: N/A — this repository has no package runtime/build pipeline. Stdlib test execution and structural/install validation are the applicable checks.
- [ ] No spec-supplied command, model invocation or publishing operation runs through the offline fixture runner.
