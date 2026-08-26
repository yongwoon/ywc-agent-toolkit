# 000073-040-domain-architecture-run-evidence — Implementation Checklist

## Prerequisites
- [ ] `000073-010-domain-architecture-invariants-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only the evidence-related helper functions, `codex/skills/ywc-agentic/**`, and the precise `.gitignore` entry.

## Stop Conditions
- [ ] Stop if the artifact requires fields outside the final Section C audit-result object.
- [ ] Stop if a write is not atomic or if malformed input can replace valid evidence.
- [ ] Stop if agentic logic treats the artifact as authoritative checkpoint/task state.

## Hardening Gate
- RED-first evidence: add closed-artifact and forbidden-field tests before production write/read changes.
- Public contract: preserve the exact audit-result object and diagnostic-only authority boundary.
- Data Integrity Hardening: N/A — no database or business-data mutation; use atomic replacement for the local artifact.
- Critical review: require review of path normalization, ignore rules, recursive key rejection, and raw-data exclusion.

## Implementation Steps
- [ ] Add strict version-1 audit-result validation and recursive rejection of unknown/raw fields to the shared helper.
  - Related AC/FR: AC7 / Iteration 2 C, E
  - Contract / Behavior Change: only exact audit result objects are accepted or written.
  - Verification Command / Evidence: closed-schema and forbidden-field fixtures pass.
- [ ] Implement atomic replacement of `.ywc-architecture-invariants-evidence.json` only after a completed bounded audit.
  - Related AC/FR: AC7 / Iteration 2 E
  - Contract / Behavior Change: incomplete or failed audits cannot publish stale/partial evidence.
  - Verification Command / Evidence: temporary-file/replace behavior and malformed-write cases pass.
- [ ] Add the ignored artifact path without altering authoritative `.ywc-run-state.json` semantics.
  - Related AC/FR: AC7 / Iteration 2 E
  - Contract / Behavior Change: diagnostic evidence remains local and untracked.
  - Verification Command / Evidence: `.gitignore` and repository status checks.
- [ ] Update `ywc-agentic` to read the artifact only as non-authoritative diagnostic evidence and preserve existing checkpoint/task authority.
  - Related AC/FR: AC5, AC7 / Iteration 2 E
  - Contract / Behavior Change: agentic packets cannot elevate local evidence into execution authority.
  - Verification Command / Evidence: targeted agentic eval and static authority-boundary review.

## Task Verify
- [ ] `python3 tests/architecture_invariants_test.py`
  - Expected Passing Signal: evidence write/read and forbidden-field cases pass.
  - Pre-change Failing Evidence / Exception: RED fixtures required for the new artifact contract.
  - Contract/Test Evidence: exact result shape and atomic-write assertions.
- [ ] `rg -n 'raw_command|raw_command_output|transcript|chain_of_thought|generated_source|full_diff' codex/skills/scripts/architecture-invariants.py codex/skills/ywc-agentic`
  - Expected Passing Signal: only intentional rejection/validation references remain; no persistence or forwarding path exists.
  - Pre-change Failing Evidence / Exception: N/A — static hardening check.
  - Contract/Test Evidence: diff review confirms raw data is rejected, not stored.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — Python standard-library helper and Markdown skill changes)
- [ ] unit tests pass (`python3 tests/architecture_invariants_test.py`)
- [ ] integration tests pass (agentic contract evals)
- [ ] app builds without error (N/A — bundle validation is terminal)
