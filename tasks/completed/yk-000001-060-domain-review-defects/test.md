# Review defects and targeted linters — scenarios

## AC-5 — A-005 through A-007
1. Exercise positive and negative source fixtures for A-005 checkout credential exposure, A-006 unawaited/boolean Promise misuse, and A-007 discarded errors.
2. Include provenance for each finding and an internal-only prompt-injection severity row with a condition that does not permit downgrade.
3. Run with each stack linter present and absent.

Expected: all three catalog rules are present with correct severity rationale; targeted lint findings corroborate review but never decide the finding alone; unavailable linters are reported as unavailable without blocking unrelated review scope.

## Failure-mode coverage
Steps: confirm a row-level prompt-injection exception is applied only when that row's condition is satisfied; test internal-only context alone as a negative case.

Expected: item 2's downgrade prohibition is preserved and internal-only status does not globally downgrade severity. Numeric eval IDs and source provenance remain stable.
