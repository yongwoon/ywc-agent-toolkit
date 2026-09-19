# Test Plan

## Scenario 1: Installed bundle

1. Create an installed fixture under a temporary `CODEX_HOME`.
2. Invoke the shipped launcher and resolver for each fixed invocation kind.
3. Confirm the installed absolute path is selected and the candidate runs when expected.

Expected result: installed resolution succeeds without consulting the target checkout.

## Scenario 2: Authorized development source

1. Create a canonical source-root fixture with the expected Git origin and layout.
2. Set `YWC_BUNDLE_DEVELOPMENT=1` and `YWC_BUNDLE_SOURCE_ROOT`.
3. Test contained regular files, including non-`+x` interpreter candidates.

Expected result: authorized source candidates resolve; direct execution still requires `+x`.

## Scenario 3: Hostile target and origin mismatch

1. Add lookalike files under a target repository.
2. Use a different Git repository or mismatched origin as the configured source.
3. Invoke the launcher and resolver while recording marker files.

Expected result: resolution returns `BLOCKED` before either lookalike executes and no marker is created.

## Scenario 4: `mark-complete.sh` blocked compactor

1. Arrange for the compactor to be unresolved.
2. Run `mark-complete.sh` against a temporary task directory and Git index.
3. Compare source/destination paths and commit count before and after.

Expected result: the command reports `BLOCKED` and performs no move, staging, or commit.

