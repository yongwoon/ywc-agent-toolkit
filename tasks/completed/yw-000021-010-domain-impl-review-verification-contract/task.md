# yw-000021-010-domain-impl-review-verification-contract — Implementation Checklist

## Prerequisites

- [ ] No predecessor task is required; confirm the repository baseline is current.

## Allowed Edit Scope

- [ ] Modify only `codex/skills/ywc-impl-review/SKILL.md`.
- [ ] Stop and report if a change requires evals, READMEs, plugin files, or `codex/agents/*.toml`.

## Stop Conditions

- [ ] Stop if the source skill cannot express the requested behavior without changing the five Phase 1 axes, `--advisor-budget`, or Phase 2 advisor policy.
- [ ] Stop if a blind verifier packet would need the original finding rationale or full worker transcript.
- [ ] Stop if the requested report semantics require a custom-agent contract change.

## Hardening Gate

- [ ] Classify this task as behavior change.
- [ ] Use the existing downstream contract-eval runner as named coverage before source edits.
- [ ] Preserve the Implementation-review orchestration protocol documented in `README.md`; return `NEEDS_CONTEXT` on a protocol mismatch.
- [ ] Data Integrity Hardening is N/A because this changes no mutable data path.
- [ ] Require manual full implementation review because the task changes high-severity finding trust semantics.

## Implementation Steps

- [ ] Update the Rationalization Defense and Advisor Pattern portions of `codex/skills/ywc-impl-review/SKILL.md`.
  - [ ] State that independent verification is mandatory for eligible Phase 1 Critical/High confirmed findings.
  - [ ] State that verifier calls are separate from, and do not reduce, the Phase 2 advisor budget.
- [ ] Insert Step 2.5 after target resolution and before Phase 1 dispatch.
  - [ ] Refuse empty targets and scopes above 200 files for every target mode.
  - [ ] For `--base`, `--git-range`, and `--working-tree`, enforce the 5,000 added-plus-removed-line limit and report exact counts plus five largest files; do not fabricate this metric for `--code`.
- [ ] Insert Step 4.5 between aggregation and Phase 2 selection.
  - [ ] Dispatch a blind `file:line` plus claimed-severity packet for eligible findings, capped at 20 with Critical before High and discovery order within tier.
  - [ ] Define reproduced, `verification-failed`, `verification-error`, and cap-unverified routing, including `--no-advisor` behavior and Phase 2 prioritization.
- [ ] Revise Steps 4–6 and Output Format.
  - [ ] Merge failed/error candidates before the existing Phase 2 budget selection without spending advisor calls.
  - [ ] Add aggregate verification counts and a per-finding Verification field while preserving `[P1]`/`[P2]` and severity symbols.

## Task Verify

- [ ] `rg -n 'Step 2\.5|Step 4\.5|verification-failed|verification-error|cap-unverified|20' codex/skills/ywc-impl-review/SKILL.md`
- [ ] `git diff --check -- codex/skills/ywc-impl-review/SKILL.md`

## Verification

- [ ] Markdown review passes for the owned SKILL file.
- [ ] Deferred integration coverage is explicitly handed to `yw-000021-020-test-impl-review-verification-evals`.
- [ ] Generated package parity is explicitly handed to `yw-000022-010-infra-impl-review-package-validation`.

## Implementation Notes (optional)

