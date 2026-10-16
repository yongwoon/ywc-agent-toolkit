# yw-000064-010-domain-conditional-omission-lenses — Implementation Checklist

## Prerequisites

- [ ] `yw-000063-020-domain-spec-review-availability` is completed, accepted and present in the merged baseline.
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

- [ ] Create bounded applicability references.
  - [ ] Add codex/skills/ywc-spec-validate/references/ui-qa-lenses.md with triggers/checks for round-trip fidelity, loading/empty/error, optimistic updates, IME composition, and keyboard accessibility.
  - [ ] Add security-qa-lenses.md in the same directory for authentication, authorization/IDOR, input validation, secrets, rate limits, sensitive output, CSRF, and file/path handling.
- [ ] Apply lenses only to matching requirements.
  - [ ] Wire both references into codex/skills/ywc-spec-validate/SKILL.md; report applicability and missing observable requirements.
  - [ ] Do not invent unrelated product requirements; retain support for legacy specs without Failure Modes.
- [ ] Verify source and installed references.
  - [ ] Add UI, auth/upload, unrelated-documentation and legacy-spec fixtures under tests/fixtures/codex-issue69/conditional-omission-lenses/.
  - [ ] Extend the focused and contract runners; confirm validate.sh installed-asset coverage resolves both new references in a temporary CODEX_HOME.
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
- [ ] Record O1, P1 scenario evidence in `test.md`; map the covered IDs from README to actual assertions or manual observations.

## Verification

- [ ] Required repository check: `bash scripts/validate.sh` passes after package synchronization; its installed-asset checks use temporary destinations.
- [ ] Source-only and fixture assertions are labeled separately from live behavior; missing measurements are explicit gaps.
- [ ] Confirm no Claude Code, version/release metadata or unrelated source changes; frontmatter/locales/agents metadata remain intact.
- [ ] Typecheck/application build: N/A — this repository has no package runtime/build pipeline. Stdlib test execution and structural/install validation are the applicable checks.
- [ ] No spec-supplied command, model invocation or publishing operation runs through the offline fixture runner.
