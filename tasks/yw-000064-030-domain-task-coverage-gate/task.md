# yw-000064-030-domain-task-coverage-gate — Implementation Checklist

## Prerequisites

- [ ] `yw-000064-020-domain-spec-failure-evidence` is completed, accepted and present in the merged baseline.
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

- [ ] Emit attributable coverage evidence.
  - [ ] Extend codex/skills/ywc-task-generator/SKILL.md and its output reference to enumerate every AC, FR and present Failure Modes row as COVERED, DEFERRED_WITH_REASON or UNCOVERED.
  - [ ] Report covered, deferred-in-scope and uncovered counts plus deduplicated unresolved IDs attributable to the current spec and preview identity; any in-scope deferral/uncovered item prevents clean DONE.
  - [ ] Keep this as report evidence: no checkpoint field, handoff schema, planner/ready Result extension or task completion mutation.
- [ ] Make verification and interface evidence explicit.
  - [ ] Update README/task templates to map covered AC IDs to verification files/scenarios; allow documented mapping for existing tests where inline comments are inappropriate.
  - [ ] Compare consumed names/signatures only with explicitly declared owned interfaces, report producer and consumer mismatch evidence, and record missing contract evidence when correctness depends on a prose-only boundary.
  - [ ] Wire codex/skills/ywc-impl-review/references/qa-agent.md to consume mappings; retain library/DB separation and absorb incidental setup into its owning deliverable.
- [ ] Guard both agentic call boundaries atomically.
  - [ ] Update codex/skills/ywc-agentic/SKILL.md immediately after each preview-only and approved-preview consume call: continue only on DONE, zero unresolved counts and no contradictory IDs.
  - [ ] Propagate attributable non-DONE unchanged and preserve artifacts; missing, malformed, contradictory or identity-mismatched evidence returns BLOCKED.
  - [ ] Unresolved preview permits zero consume calls; unresolved consume permits zero executor calls. Repair via existing spec/task preparation within approved scope, with no automatic execution.
- [ ] Verify coverage and authority negatives.
  - [ ] Add O2/O3 fixtures under tests/fixtures/codex-issue69/task-coverage-gate/ covering every gap category, deferral, incompatible signatures and existing-test mappings.
  - [ ] Extend both runners for non-DONE/absent/malformed/contradictory/mismatched reports at each boundary and assert downstream call counts; retain all current preview identity/path/digest negatives.
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
- [ ] Record O2, O3 scenario evidence in `test.md`; map the covered IDs from README to actual assertions or manual observations.

## Verification

- [ ] Required repository check: `bash scripts/validate.sh` passes after package synchronization; its installed-asset checks use temporary destinations.
- [ ] Source-only and fixture assertions are labeled separately from live behavior; missing measurements are explicit gaps.
- [ ] Confirm no Claude Code, version/release metadata or unrelated source changes; frontmatter/locales/agents metadata remain intact.
- [ ] Typecheck/application build: N/A — this repository has no package runtime/build pipeline. Stdlib test execution and structural/install validation are the applicable checks.
- [ ] No spec-supplied command, model invocation or publishing operation runs through the offline fixture runner.
