# yw-000016-010-test-scaffold-contract-evals — Implementation Checklist

## Prerequisites
- [ ] `yw-000015-010-domain-scaffold-routing` is merged.
- [ ] `yw-000015-020-refactor-scaffold-reference-enrichment` is merged.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-project-scaffold/evals/evals.json`.

## Stop Conditions
- [ ] Stop if the current eval harness schema cannot represent the expected behavior without inventing fields.
- [ ] Stop if a fixture expects automatic research edits or a silent reference rewrite.
- [ ] Stop if existing fixture IDs or content must be changed to make the new cases pass.

## Implementation Steps
- [ ] Inspect the current four fixture objects and preserve their IDs, prompts, expected outputs, and `files` arrays.
  - Related AC/FR: AC10 / FR6
  - Contract / Behavior Change: existing coverage remains valid JSON and semantically intact.
  - Verification Command / Evidence: `git diff -- codex/skills/ywc-project-scaffold/evals/evals.json`.
- [ ] Append a large/contested scaffold case that asserts Trend Check delegation, material-delta Extras handling, baseline retention, and no silent edit.
  - Related AC/FR: AC1–AC3 / FR2, FR6
  - Contract / Behavior Change: conditional research behavior is machine-readable.
  - Verification Command / Evidence: JSON inspection plus contract script.
- [ ] Append a `go.md` refresh case that asserts `reference-refresh`, target/language inference, additive proposal, approval stop, and preservation of existing variants.
  - Related AC/FR: AC4–AC6 / FR3, FR6
  - Contract / Behavior Change: refresh is proposal-first and never silently writes.
  - Verification Command / Evidence: JSON inspection plus contract script.

## Task Verify
- [ ] `python3 -m json.tool codex/skills/ywc-project-scaffold/evals/evals.json >/dev/null`
  - Expected Passing Signal: exit 0.
  - Pre-change Failing Evidence / Exception: N/A — fixture addition.
  - Contract/Test Evidence: JSON parser.
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: `PASS: Codex skill contract evals are structurally valid.`
  - Pre-change Failing Evidence / Exception: N/A — structural contract check.
  - Contract/Test Evidence: repository eval validator.

## Verification
- [ ] lint passes (N/A — JSON fixture has no configured linter)
- [ ] typecheck passes (N/A — JSON-only task)
- [ ] unit tests pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] app builds without error (N/A — repository has no application build)
