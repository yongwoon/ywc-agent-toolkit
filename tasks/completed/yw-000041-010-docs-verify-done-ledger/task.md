# yw-000041-010-docs-verify-done-ledger — Implementation Checklist

## Prerequisites
- [ ] Both Phase `yw-000040` tasks are merged and checker tests pass.
- [ ] The installed CLI signature is unchanged.

## Allowed Edit Scope
- [ ] Edit only the source skill, eval JSON, and six README locale files.

## Stop Conditions
- [ ] Stop if preserving Steps 1–6 or Claim Classification needs code changes.
- [ ] Stop on unrelated locale cleanup or a request to alter `agents/openai.yaml`.

## Hardening Gate
- [ ] Classify as additive docs/eval contract.
- [ ] Record checker-suite and contract-eval coverage before changing claims.
- [ ] Consume only the bounded checker contract; Data Integrity Hardening is N/A.

## Implementation Steps
- [ ] Insert `Gate Ledger Escalation (Optional)` after Step 6 without renumbering existing steps.
  - Explain installed `--status`, bare resume, `--reverify`, MANUAL, positive controls, untrusted CHECK inspection, and independent PR polling.
  - Add Common Mistakes for positive controls and recomputing supplied counts.
- [ ] Add one ledger-specific eval while retaining IDs 1–3 and valid JSON schema.
- [ ] Update all six README locales with localized optional-ledger usage and shell warning; keep technical identifiers in English.
- [ ] Compare `agents/openai.yaml` byte-for-byte and inspect diff for accidental scope expansion.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `jq empty codex/skills/ywc-verify-done/evals/evals.json`
- [ ] `git diff --check -- codex/skills/ywc-verify-done`

## Verification
- [ ] Lint/typecheck/build: N/A — no repository application pipeline.
- [ ] Unit tests: predecessor checker suite and contract-eval runner.
- [ ] Integration tests: N/A — no service integration.

## Implementation Notes (optional)
