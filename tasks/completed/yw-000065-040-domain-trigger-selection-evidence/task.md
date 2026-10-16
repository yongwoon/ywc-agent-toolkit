# yw-000065-040-domain-trigger-selection-evidence — Implementation Checklist

## Prerequisites

- [ ] `yw-000065-030-domain-sdk-review-evidence` is completed, accepted and present in the merged baseline.
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
- [ ] Require full `ywc-impl-review` or full manual review before DONE.

## Implementation Steps

- [ ] Correct only the three collision pairs.
  - [ ] Adjust relevant SKILL.md descriptions in ywc-tech-research/product-review for technical trade-offs versus business ROI; ywc-security-audit/product-review for threat modeling versus product risk; ywc-impl-review/code-gen for conformance versus generation.
  - [ ] Preserve existing positive triggers, description ceilings and eval location/schema; strengthen product findings to drop unsupported conclusions, with no new agent types.
- [ ] Add paired deterministic selection expectations.
  - [ ] Extend the five affected evals/evals.json files and tests/fixtures/codex-issue69/trigger-selection-evidence/ with positive/negative prompts for all three pairs.
  - [ ] Retain checks for existing triggers; treat expected selections as fixture assertions, never live observations.
- [ ] Record the six mandatory bounded live observations.
  - [ ] At the changed source revision, run the exact T1–T6 prompts in spec FR-8 via an available Codex session/live harness; stop after selection before audit, implementation or publishing executes.
  - [ ] Record prompt, actual skill, expected skill, source revision and installed catalog identity in tests/fixtures/codex-issue69/trigger-selection-evidence/observations.md without credentials or full transcripts.
  - [ ] Require all six observed matches for AC-9 acceptance; unavailable/mismatched trials remain unverified and prevent a clean implementation completion claim.
- [ ] Close Stage 3 acceptance evidence.
  - [ ] Run final focused, contract, description, agent, distribution and temporary-install gates; check AC-1 through AC-10 and full implementation review with no unresolved Critical/High findings.
  - [ ] Separate structural, fixture and live evidence in the final stage report; do not change release/version metadata or publish PRs without a subsequent execution request.
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
- [ ] Record E2, P1 scenario evidence in `test.md`; map the covered IDs from README to actual assertions or manual observations.

## Verification

- [ ] Required repository check: `bash scripts/validate.sh` passes after package synchronization; its installed-asset checks use temporary destinations.
- [ ] Source-only and fixture assertions are labeled separately from live behavior; missing measurements are explicit gaps.
- [ ] Confirm no Claude Code, version/release metadata or unrelated source changes; frontmatter/locales/agents metadata remain intact.
- [ ] Typecheck/application build: N/A — this repository has no package runtime/build pipeline. Stdlib test execution and structural/install validation are the applicable checks.
- [ ] No spec-supplied command, model invocation or publishing operation runs through the offline fixture runner.
