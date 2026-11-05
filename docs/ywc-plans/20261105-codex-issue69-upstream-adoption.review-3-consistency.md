# Issue #69 Codex Spec — Consistency iteration 3

Status: DONE
Critical: 0, Warning: 0, Suggestion: 0
Spec: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md
Dimension: Consistency
Review scope: full amended spec including Amendment Iteration 2; no product files edited or executed.

## Confirmed findings

None.

## Full-spec consistency checks

- Purpose/Oracle lines 7–19 continue to require all contract ACs and mandatory local checks while refusing runtime PASS without runtime evidence. Verification 233–239 now makes the evidence boundary concrete: source/expected-trace contracts for Markdown decisions; executed existing helpers for real executable seams; source command recipe execution only for extracted runnable snippets; actual model behavior only with live trace. These grades do not substitute for one another.
- AC-6 at 203 expressly uses source/expected-trace fixtures for PR guard, worker-zero, polling, severity decisions, matching FR-6's instruction behavior at 155–159. It separately reserves actual model call-count PASS for live trace.
- AC-9 at 206 distinguishes extracted executable Git recipes, Markdown flag/path/cwd decisions, existing audit/cleanup helper tests, and live model behavior. Verification 237 identifies the existing helper boundaries. Verification 239 no longer mandates fake-clock execution of a nonexistent polling helper. The 1800-second expected-trace boundary is compatible with FR-6's 30-minute total deadline.
- The optional extracted snippet path preserves the original production recipe instead of passing a test-side recreation off as product execution. Descriptive snippets remain source assertions. This is consistent with NFR 246's data-only treatment of untrusted metadata and with the declared ban on introducing a production dispatcher solely for testing.
- Model Hint remains advisory in FR-1, AC-1, Module Boundaries, and Existing Constraints. Existing executor model selection/pins remain preserved.
- Agentic no-converge/Result/Artifact profile handling is retained at lines 95 and 187–189, with interactive/noninteractive owner counts at AC-10. No double-convergence contradiction was reintroduced.
- FR-2 mode/output boundaries, FR-3 question/seam flow, FR-4 seven categories/redaction/owner limits, FR-5 verified lint evidence, FR-7 confirmed Mission writes/history, FR-8 attestation status routing, FR-9 worktree identity, and FR-10 PR body ordering still have corresponding AC rows. No orphan identifier or incompatible status rule was introduced.
- Immutable local/upstream provenance and the adopted/excluded PR matrix remain present; Global Constraints remain unchanged; source-first plugin generation remains consistent across constraints, FR-10, and verification.
- Previous substantive sections remain present. Amendment Iteration 2 accurately records the Verification and AC-6/9 evidence-policy changes instead of silently narrowing the stated product behavior.

## Outcome Oracle and Blind Spot

Outcome Oracle: complete for source/helper contract implementation. Blind Spot action: proceed for this dimension. Runtime safety remains UNVERIFIED until separately observed, consistent with the declared completion boundary.

## Advisor candidates

None.
