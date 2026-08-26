# yw-000004-020-infra-parser-optional-initials-prefix

## Purpose
Make every task-ID parser accept an optional initials prefix without changing a single byte of its output for legacy unprefixed IDs.

## Scope
Widen the ID regexes in `scaffold-task-dir.sh`, `compact-dependency-graph.py`, and `build-pr-title.py`, add explicit match boundaries to prevent partial matching, and prove both directions with fixtures.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#fr4--스크립트-정규식에-선택적-접두-추가-ac6-ac7-ac8` — the exact replacement regex table
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#acceptance-criteria` — AC6, AC7, AC8
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#id-grammar-contract` — generation always prefixes, parsing accepts both

### Summary
The ID grammar is deliberately asymmetric: the generator always emits an initials prefix, while every parser accepts the prefix as optional. That asymmetry is what makes migrating the repository's 81 existing legacy phases unnecessary. The dangerous failure here is silent: `\b` matches on both sides of a hyphen, so `\b(\d{6}-\d{3})\b` matches the `000001-010` *inside* `yk-000001-010`, which would let the compactor rewrite or group the wrong rows. Boundaries must be expressed with explicit lookbehind/lookahead, and PHASE grouping in the compactor must key on the full prefixed string.

### Out of Scope (from spec)
- `next-task-number.sh` — handled by `yw-000005-010-infra-next-task-number-initials-scan`.
- Any prose describing the grammar in SKILL.md — handled by `yw-000005-020` and the `yw-000006` phase.

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)

### Depended By
- `yw-000005-010-infra-next-task-number-initials-scan` — the allocator emits IDs that `scaffold-task-dir.sh` must accept.
- `yw-000006-010-docs-task-generator-artifacts-sync` — the dependency-graph template must use headings the compactor can parse.
- `yw-000007-010-infra-validation-gate` — final no-regression gate.

## Key Files
- `claude-code/skills/ywc-task-generator/scripts/scaffold-task-dir.sh`
- `claude-code/skills/ywc-task-generator/scripts/compact-dependency-graph.py`
- `claude-code/skills/ywc-finish-branch/scripts/build-pr-title.py`
- Fixture inputs used for the before/after diff (kept alongside the scripts or under the scratchpad, per whichever convention the existing scripts already follow)

## Notes
- The three changed scripts live under `claude-code/skills/**/scripts/`, which `.github/workflows/validate.yml:22` does **not** shellcheck (`scandir: ./scripts`). Run `shellcheck` locally on the shell script — CI will not catch a portability regression here.
- NFR2: macOS default shell tooling only. No `flock`, no `grep -P`, no GNU `sed -i`.
- The spec flags these files as requiring fixture-based before/after diff verification because a regex regression corrupts `dependency-graph.md` silently rather than loudly.

## Hardening Evidence
### Test Feedback Path
- RED-first target: a mixed-format `dependency-graph.md` fixture (legacy `## Phase 000001` and prefixed `## Phase yk-000001` in one file) that the current compactor mishandles, plus prefixed inputs that `scaffold-task-dir.sh` and `build-pr-title.py` currently reject or misparse.

### Interface Contract
- Contract: task-name validation (accept/reject + exit code), compaction decisions, and `build-pr-title.py` output fields.
- Inputs: prefixed IDs, legacy unprefixed IDs, over-length prefixes, malformed IDs.
- Outputs: unchanged shape; legacy inputs must be byte-identical to the pre-change output.
- Error model: existing exit codes and fallbacks preserved.
- Impacted tests: the fixture suites added by this task.

### Critical Surface Review
- Review requirement: N/A for security, but a mandatory before/after diff on the compactor because partial-match regression corrupts data silently.

### Data Integrity Hardening
- Trigger surface: `compact-dependency-graph.py` rewrites `dependency-graph.md` in place.
- Atomic / locking strategy: N/A — single-process rewrite; no shared counter.
- Transaction boundary: N/A
- Idempotency guard: compaction must remain idempotent — running it twice on the same file produces identical output.
- Required tests: mixed legacy/prefixed fixture diff, and a re-run idempotency check.

## Parallel Execution Metadata
### Ownership
- `claude-code/skills/ywc-task-generator/scripts/scaffold-task-dir.sh`
- `claude-code/skills/ywc-task-generator/scripts/compact-dependency-graph.py`
- `claude-code/skills/ywc-finish-branch/scripts/build-pr-title.py`
- Parser fixtures added by this task

### Shared Surfaces
- Task ID grammar contract
- `dependency-graph.md` on-disk format
- PR title prefix format consumed by `ywc-finish-branch`

### Conflicts With
- (None identified — `yw-000004-010` touches only documentation files)

### Parallelizable After
- (None — root task; runs against the merged `main` baseline)

### Task Verify
- `shellcheck claude-code/skills/ywc-task-generator/scripts/scaffold-task-dir.sh`
- `python3 -m py_compile claude-code/skills/ywc-task-generator/scripts/compact-dependency-graph.py claude-code/skills/ywc-finish-branch/scripts/build-pr-title.py`
- Mixed legacy/prefixed compaction fixture: before/after `diff` reviewed, no `yk-000001-010` reduced to `000001-010`
- Legacy `build-pr-title.py` inputs produce byte-identical output to the pre-change build

## Out of Scope
- Changing PHASE width, SEQUENCE stepping, or the category vocabulary.
- Migrating existing legacy task directories.
