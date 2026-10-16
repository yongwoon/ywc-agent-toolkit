# yw-000065-010-domain-bounded-suggestion-policy — Implementation Checklist

## Prerequisites

- [ ] `yw-000064-030-domain-task-coverage-gate` is completed, accepted and present in the merged baseline.
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

- [ ] Change Suggestion policy at its owner.
  - [ ] Update codex/skills/ywc-spec-ready/SKILL.md and references/convergence.md wherever the replaced policy appears; preserve explicit apply/defer and user instructions.
  - [ ] With no explicit policy and no Critical/Warning findings, attempt at most one Suggestion amendment/revalidation in either interaction mode; residual Suggestions remain advisory.
  - [ ] Explicit defer does no amendment; new Critical/Warning findings return to bounded blocking convergence; malformed evidence retains failure routing and invalid policy stays NEEDS_CONTEXT.
- [ ] Propagate the owner policy consistently.
  - [ ] Update planner handoff, agentic arguments/preflight/propagation, and affected references/examples/evals in the declared source paths together.
  - [ ] Remove stale prompts or repeated NEEDS_CONTEXT: --suggestions for residual advisory findings without altering closed Result parsing or artifact authority.
- [ ] Reuse approval only inside the existing preview contract.
  - [ ] Align task-generator and caller wording so matching already-approved unchanged previews consume once without another confirmation.
  - [ ] Retain preview-only, explicit approval, path containment, spec/tasks-dir/language/mode/path/revision/digest identity and consume-only checks; newly generated previews remain unapproved.
- [ ] Prove policy and approval boundaries.
  - [ ] Add I1/I2 fixtures under tests/fixtures/codex-issue69/bounded-suggestion-policy/ and extend existing contract evals.
  - [ ] Cover no Suggestions, one default pass, apply/defer, residual Suggestions, new Warning, invalid/malformed evidence, fresh/unapproved/stale/escaping previews, and zero task writes in preview-only mode.
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
- [ ] Record I1, I2 scenario evidence in `test.md`; map the covered IDs from README to actual assertions or manual observations.

## Verification

- [ ] Required repository check: `bash scripts/validate.sh` passes after package synchronization; its installed-asset checks use temporary destinations.
- [ ] Source-only and fixture assertions are labeled separately from live behavior; missing measurements are explicit gaps.
- [ ] Confirm no Claude Code, version/release metadata or unrelated source changes; frontmatter/locales/agents metadata remain intact.
- [ ] Typecheck/application build: N/A — this repository has no package runtime/build pipeline. Stdlib test execution and structural/install validation are the applicable checks.
- [ ] No spec-supplied command, model invocation or publishing operation runs through the offline fixture runner.
