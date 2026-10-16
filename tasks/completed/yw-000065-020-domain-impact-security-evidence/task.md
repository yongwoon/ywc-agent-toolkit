# yw-000065-020-domain-impact-security-evidence — Implementation Checklist

## Prerequisites

- [ ] `yw-000065-010-domain-bounded-suggestion-policy` is completed, accepted and present in the merged baseline.
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

- [ ] Generate concise optional Impact from existing evidence.
  - [ ] Update codex/skills/ywc-create-pr/SKILL.md to emit localized affected scope and concrete Before/After only for observable behavior changes.
  - [ ] Reuse the diff already read during author review, respect repository PR templates, and omit Impact for docs-only changes; preserve publishing authority.
- [ ] Derive deduplicated negative-path scenarios.
  - [ ] Update codex/skills/ywc-gen-testcase/SKILL.md to consume the Stage 2 security-qa-lenses.md reference and add one scenario for each triggered lens.
  - [ ] Deduplicate overlapping scenarios without dropping triggered checks; do not add unconditional PR-body fetching, screenshot operations or broad collection.
- [ ] Verify Impact applicability and scenario reuse.
  - [ ] Add behavior-diff, docs-only, localized-template and overlapping-security fixtures under tests/fixtures/codex-issue69/impact-security-evidence/.
  - [ ] Extend focused/contract assertions to expose redundant diff/PR-body acquisition and installed-reference failures.
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
- [ ] Record E1 scenario evidence in `test.md`; map the covered IDs from README to actual assertions or manual observations.

## Verification

- [ ] Required repository check: `bash scripts/validate.sh` passes after package synchronization; its installed-asset checks use temporary destinations.
- [ ] Source-only and fixture assertions are labeled separately from live behavior; missing measurements are explicit gaps.
- [ ] Confirm no Claude Code, version/release metadata or unrelated source changes; frontmatter/locales/agents metadata remain intact.
- [ ] Typecheck/application build: N/A — this repository has no package runtime/build pipeline. Stdlib test execution and structural/install validation are the applicable checks.
- [ ] No spec-supplied command, model invocation or publishing operation runs through the offline fixture runner.
