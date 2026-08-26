# yw-000004-020-infra-parser-optional-initials-prefix — Implementation Checklist

## Prerequisites
- [ ] Working tree is on a fresh branch from the merged base.
- [ ] The FR4 regex table in the spec has been read in full.

## Allowed Edit Scope
- [ ] Modify only the three named scripts and the fixtures this task adds. Do not touch `next-task-number.sh` or any `SKILL.md`.

## Stop Conditions
- [ ] Stop if any legacy unprefixed input produces output differing from the pre-change build by even one byte.
- [ ] Stop if a proposed regex uses `\b` as the boundary around a hyphen-adjacent group.
- [ ] Stop if a GNU-only construct (`grep -P`, `sed -i` without a backup arg) is required.

## Hardening Gate
- [ ] Capture pre-change output for every fixture input before editing any regex (this is the RED baseline).
- [ ] Record the preserved parser output contract, including `build-pr-title.py`'s field names.
- [ ] Record the compaction idempotency check result.

## Implementation Steps
- [ ] Capture the RED baseline: run each of the three scripts against a fixture set of legacy IDs (`000001-010-db-create-user-table`, `000001-010`, malformed inputs) and save the outputs for later byte comparison.
- [ ] Add prefixed inputs (`yk-000001-010-db-create-user-table`, `yk-000001-010`, `TOOLONG-000001-010-db-x`) to the fixture set and confirm the current scripts reject or misparse them.
- [ ] Update `scaffold-task-dir.sh:38` name validation to `^([a-z0-9]{2,4}-)?[0-9]{6}-[0-9]{3}-[a-z]+-[a-z0-9-]+$`.
- [ ] Update `compact-dependency-graph.py` `PHASE_HEADING_RE` (line 43) to `^##\s*Phase\s+(?:[a-z0-9]{2,4}-)?(\d{6})\b(.*)$`, and capture the initials segment so the group key can include it.
- [ ] Update `compact-dependency-graph.py` `FULL_ID_RE` (line 45) to `(?<![A-Za-z0-9-])((?:[a-z0-9]{2,4}-)?\d{6}-\d{3}-[A-Za-z0-9][A-Za-z0-9-]*)`.
- [ ] Update `compact-dependency-graph.py` `SHORT_ID_RE` (line 46) to `(?<![A-Za-z0-9-])((?:[a-z0-9]{2,4}-)?\d{6}-\d{3})(?![A-Za-z0-9-])`.
- [ ] Change the compactor's PHASE grouping key to the full prefixed string (`yk-000001`), never the bare digits — grouping on digits alone would merge two collaborators' phases into one.
- [ ] Update `build-pr-title.py:46` to `^((?:[a-z0-9]{2,4}-)?\d{6}-\d{3})-(.+)$` and `:50` to `^((?:[a-z0-9]{2,4}-)?\d{6})-(.+)$`, keeping every existing fallback branch and the `TASK_NUMBER` / slug output fields intact.
- [ ] Add a comment block to each changed regex naming the grammar source and the reason for explicit lookbehind/lookahead over `\b`.
- [ ] Build a mixed-format `dependency-graph.md` fixture containing `## Phase 000001`, `## Phase yk-000001`, and rows referencing both `000002-010-x` and `yk-000002-010-x`, then run the compactor and review the diff.
- [ ] Assert on that fixture that no `yk-000001-010` occurrence was rewritten as `000001-010`, and that legacy and prefixed phases were grouped separately.
- [ ] Re-run the compactor on its own output and assert the file is unchanged (idempotency).
- [ ] Replay the RED baseline fixtures and diff against the captured pre-change output; every legacy case must be byte-identical.

## Task Verify
- [ ] `shellcheck claude-code/skills/ywc-task-generator/scripts/scaffold-task-dir.sh`
- [ ] `python3 -m py_compile claude-code/skills/ywc-task-generator/scripts/compact-dependency-graph.py claude-code/skills/ywc-finish-branch/scripts/build-pr-title.py`
- [ ] `bash claude-code/skills/ywc-task-generator/scripts/scaffold-task-dir.sh` accepts `yk-000001-010-db-x` and `000001-010-db-x`, and exits 1 on `TOOLONG-000001-010-db-x`
- [ ] Mixed-format compaction fixture diff reviewed and free of partial-match rewrites
- [ ] Legacy `build-pr-title.py` output byte-identical to the captured baseline

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] shellcheck run locally on the changed shell script (CI does not cover `claude-code/skills/**/scripts`)
- [ ] typecheck passes (N/A — shell and Python scripts)
- [ ] unit tests pass (fixture suites added by this task)
- [ ] app builds without error (N/A — documentation/tooling repository)
