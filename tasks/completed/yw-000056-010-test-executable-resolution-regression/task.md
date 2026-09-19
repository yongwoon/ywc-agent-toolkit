# Implementation Task

## Prerequisites

- [ ] The resolver and all 20 caller sites are present and migrated.
- [ ] Confirm `scripts/validate.sh`'s existing Codex validation error accounting before wiring the new check.

## Allowed Edit Scope

Edit only `tests/codex_executable_resolution_test.py` and the relevant Codex validation section of `scripts/validate.sh`; add fixture helpers within the test file unless existing test conventions require otherwise.

## Stop Conditions

- Stop if the test can pass without invoking the shipped launcher/resolver.
- Stop if a hostile fixture can execute before the resolver returns `BLOCKED`.
- Stop if the complement checker cannot distinguish prose examples from executable commands without weakening the closed-set invariant.

## Hardening Gate

- RED-first evidence: add failing hostile-target, origin-mismatch, missing-candidate, and no-mutation scenarios before finalizing the implementation.
- Public surface: exercise the actual launcher-selection block and resolver CLI, not a reimplemented predicate.
- Data Integrity: assert unresolved `mark-complete.sh` leaves directories and Git state unchanged.
- Critical surface: review all fixture origins, marker files, symlink paths, and side-effect assertions.

## Implementation Steps

- [ ] Build stdlib-only fixtures for installed success, authorized launcher bootstrap, canonical source fallback, non-`+x` interpreter candidates, hostile target, alternate Git origin/layout mismatch, and missing/untrusted candidates.
  - [ ] Assert marker files are not created for rejected target or alternate-repository candidates.
  - [ ] Assert deterministic `BLOCKED` output includes the expected installed path and remediation.
- [ ] Add the 20-site complement search to `scripts/validate.sh`, excluding documentation-only examples while rejecting executable target-relative assignments and commands.
- [ ] Wire the focused test into the Codex validation section, incrementing `ERRORS` on failure, and add the unresolved-compactor no-mutation regression.
- [ ] Retain the existing `scripts/check-codex-agent-evals.sh` gate and verify no agent TOML changes are needed.

## Task Verify

- [ ] `python3 tests/codex_executable_resolution_test.py`
- [ ] `bash scripts/check-codex-agent-evals.sh`
- [ ] `bash scripts/validate.sh`

## Verification

- [ ] `git diff --check`
- [ ] Confirm a deliberately reintroduced unsafe target-relative command makes the complement check fail, then remove the fixture change.

