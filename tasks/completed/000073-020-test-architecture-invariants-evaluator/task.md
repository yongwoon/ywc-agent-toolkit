# 000073-020-test-architecture-invariants-evaluator — Implementation Checklist

## Prerequisites
- [ ] `000073-010-domain-architecture-invariants-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only `tests/architecture_invariants_test.py` and the new skill's `evals/evals.json`.
- [ ] Stop before changing helper behavior; report contract gaps to the predecessor task.

## Stop Conditions
- [ ] Stop if a test requires arbitrary command execution or network access.
- [ ] Stop if a fixture cannot identify the expected terminal status deterministically.
- [ ] Stop if consumer behavior is being tested without the bounded packet task's final interface.

## Hardening Gate
- RED-first evidence: add each new behavior as a failing fixture before accepting the implementation signal.
- Public contract: assert exact closed result keys, verdict precedence, and normalized evidence paths.
- Data Integrity Hardening: N/A — test-only tooling.
- Critical review: include recursive rejection of raw command/output, transcript, source, generated source, chain of thought, full diff, and unknown keys.

## Implementation Steps
- [ ] Build reusable temporary-repository fixtures for valid manifests, malformed/closed-schema input, duplicate/dangling IDs, invalid globs, explicit no-fallback, and ambiguous component mapping.
  - Related AC/FR: AC1, AC4 / Iteration 2 B
  - Contract / Behavior Change: locks schema and path safety behavior to executable cases.
  - Verification Command / Evidence: named unittest cases pass.
- [ ] Add scope normalization, digest, mapping, coverage, allow/forbid, unsafe-path, and aggregate-precedence cases.
  - Related AC/FR: AC3, AC6 / Iteration 2 B–C
  - Contract / Behavior Change: prevents incomplete evidence from yielding `MAINTAINED`.
  - Verification Command / Evidence: full/partial and affected/unaffected rule assertions pass.
- [ ] Instrument process-launch surfaces and assert v1 never launches a child process from manifest/evidence data.
  - Related AC/FR: AC2, AC7 / Iteration 2 A, E
  - Contract / Behavior Change: executable fields are rejected with `NEEDS_CONTEXT` and no launch occurs.
  - Verification Command / Evidence: zero-launch counter remains zero for all cases.
- [ ] Mirror fixture IDs and expected statuses in `codex/skills/ywc-architecture-invariants/evals/evals.json`.
  - Related AC/FR: AC8 / Iteration 2 E
  - Contract / Behavior Change: contract eval inventory points to the same executable coverage.
  - Verification Command / Evidence: `bash scripts/run-codex-skill-contract-evals.sh` passes.

## Task Verify
- [ ] `python3 tests/architecture_invariants_test.py`
  - Expected Passing Signal: all named architecture-invariant tests pass and launch count is zero.
  - Pre-change Failing Evidence / Exception: RED evidence required for newly added cases.
  - Contract/Test Evidence: unittest output and fixture IDs.
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: structural eval contract passes.
  - Pre-change Failing Evidence / Exception: N/A — eval inventory is new.
  - Contract/Test Evidence: JSON shape and unique IDs are validated.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — standard-library Python test; execute it directly)
- [ ] unit tests pass (`python3 tests/architecture_invariants_test.py`)
- [ ] integration tests pass (consumer cases deferred to `000073-030`)
- [ ] app builds without error (N/A — skills bundle)
