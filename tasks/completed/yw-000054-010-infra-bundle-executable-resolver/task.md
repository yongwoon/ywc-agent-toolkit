# Implementation Task

## Prerequisites

- [ ] Confirm the repository guidance and the referenced hardening specification are unchanged.
- [ ] Confirm no later task is required to define the resolver interface.

## Allowed Edit Scope

Only `codex/skills/scripts/resolve-bundle-executable.sh`, `codex/skills/scripts/resolve-bundle-executable.py`, and `codex/skills/references/shared-script-resolution.md` may be edited.

## Stop Conditions

- Stop if the canonical Git origin or expected bundle layout cannot be validated without guessing.
- Stop if the launcher bootstrap would inspect a target-relative executable before trust checks.
- Stop if a design requires a third-party dependency or changes caller arguments.

## Hardening Gate

- RED-first evidence: add resolver fixture coverage or a named existing fixture before relying on the implementation.
- Public surface: preserve the CLI contract in the shared reference; downstream callers must use the exact launcher-selection block.
- Data Integrity: N/A.
- Critical surface: perform full review of path canonicalization, symlink escape rejection, origin matching, and fail-closed behavior.

## Implementation Steps

- [ ] Implement `resolve-bundle-executable.py` with fixed invocation kinds (`bash`, `python`, `python3`, direct), installed-first lookup, explicit development opt-in, canonical Git-root/origin/layout checks, contained regular-file validation, and deterministic `BLOCKED` diagnostics.
  - [ ] Permit non-`+x` candidates only for fixed interpreters; require `+x` for direct execution.
  - [ ] Reject symlinks resolving outside the authorized `codex/skills/` tree.
- [ ] Implement `resolve-bundle-executable.sh` as the shipped installed/source bootstrap launcher, invoking the Python resolver through fixed `python3`.
  - [ ] Ensure source bootstrap validates explicit opt-in, absolute canonical source root, expected origin/layout, and contained launcher before invocation.
- [ ] Document the exact copyable launcher-selection block and non-goals in `shared-script-resolution.md`.

## Task Verify

- [ ] `python3 -m py_compile codex/skills/scripts/resolve-bundle-executable.py`
- [ ] `bash -n codex/skills/scripts/resolve-bundle-executable.sh`
- [ ] `python3 codex/skills/scripts/resolve-bundle-executable.py --help`

## Verification

- [ ] `bash scripts/validate.sh`
- [ ] `git diff --check`

