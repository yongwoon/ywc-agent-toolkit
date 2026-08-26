# yw-000001-030-parser-prefixed-task-ids — Implementation Checklist

## Prerequisites
- [ ] `yw-000001-010-config-initials-writer` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only the two named parser scripts and their focused fixtures.

## Stop Conditions
- [ ] Stop if legacy numeric or unprefixed parser behavior changes unexpectedly.
- [ ] Stop if completion matching becomes case-insensitive beyond the existing exact suffix rule.

## Hardening Gate
- [ ] Record RED-first parser fixture evidence.
- [ ] Record the stable parser output contract.
- [ ] Mark Data Integrity Hardening N/A because this is read-only parsing.

## Implementation Steps
- [ ] Extend `compact-dependency-graph.py` full/short ID regexes to accept optional lowercase initials prefixes.
- [ ] Preserve `rest.strip().lower() == "— done"` semantics and add the `— Done prerequisites` non-completion fixture.
- [ ] Extend `build-pr-title.py` task-name parsing with an optional initials segment while preserving all current fallbacks.
- [ ] Add prefixed and legacy fixtures covering full IDs, short IDs, malformed IDs, and generated title fields.

## Task Verify
- [ ] Run the compactor fixture suite.
- [ ] Run the PR-title parser fixture suite.
- [ ] `python3 -m py_compile codex/skills/ywc-task-generator/scripts/compact-dependency-graph.py codex/skills/ywc-finish-branch/scripts/build-pr-title.py`

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — Python scripts)
- [ ] unit tests pass (focused parser fixtures)
- [ ] integration tests pass (N/A — no external integration)
- [ ] app builds without error (N/A — documentation/tooling repository)
