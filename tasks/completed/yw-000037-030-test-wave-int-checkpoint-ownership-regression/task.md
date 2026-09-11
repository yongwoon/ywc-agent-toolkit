# yw-000037-030-test-wave-int-checkpoint-ownership-regression — Implementation Checklist

## Prerequisites
- [ ] `yw-000037-010` is in `tasks/completed/` — claude-code root's subcommands/procedure exist.
- [ ] `yw-000037-020` is in `tasks/completed/` — codex root's subcommands/procedure exist.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `scripts/test-wave-int-checkpoint-ownership.sh` (new file) only. No edits to either `update-state.py` copy, either `wave-integration-branch.md` copy, or `checkpoint-resume.md`.

## Stop Conditions
- [ ] Stop if either root's `wave-int-owner`, `wave-int-blocked`, or `wave-int-status` subcommand is missing or has a different argument shape than `yw-000037-010`'s README/task.md describe — that means the dependency task is incomplete, not a bug in this test.
- [ ] Stop if a scenario cannot be constructed without real network access — every scenario must run against local/temp git repos only (see Notes on simulating `origin` with a bare repo).
- [ ] Stop if fixing a failing assertion would require changing `update-state.py` or `wave-integration-branch.md` — report the mismatch against the finished dependency tasks instead of patching them from this task.

## Implementation Steps
- [ ] Create `scripts/test-wave-int-checkpoint-ownership.sh` with `#!/usr/bin/env bash` and `set -euo pipefail`.
- [ ] Add `--root <path>` argument parsing; when omitted, iterate over `claude-code/skills/scripts/update-state.py` and `codex/skills/scripts/update-state.py` in sequence, running the full scenario suite against each.
- [ ] Add `assert_eq expected actual label` and `assert_contains haystack needle label` helper functions that increment a pass/fail counter and print `ok`/`FAIL` per assertion; `main` exits non-zero if any assertion failed.
- [ ] **Unit-boundary scenarios** (per root, no git repo needed — operate on a temp `.ywc-run-state.json` in a temp cwd):
  - [ ] AC7: `init-parallel` → `run_id` is a non-empty string matching `^[0-9a-f]{8}$`.
  - [ ] AC10 / `wave-int-owner`: executor-mismatch `die()` (run against a `sequential`-executor state) — non-zero exit, stderr contains the exact message text from the spec's API Contract table; `run_id`-unset `die()` — non-zero exit, stderr contains `re-run init-parallel`; wave-not-found `die()`.
  - [ ] AC10 / `wave-int-blocked`: identical three `die()` rows as `wave-int-owner`.
  - [ ] AC10 / `wave-int-status`: executor-mismatch and wave-not-found `die()` rows only; confirm a `run_id`-unset state file does **not** `die()` and instead prints `unset unset` (or the wave's actual recorded values) — this is the negative case Iteration 3 of the spec added.
  - [ ] Success-path print-format assertions for all three subcommands, matching the spec's API Contract table exactly.
- [ ] **Integration-boundary scenarios** (per root, disposable `mktemp -d` git repo + bare "origin" repo, `trap ... EXIT` cleanup):
  - [ ] AC1: create `wave-int/0`, push to origin, record `wave-int-owner 0 --tip-sha <sha>`; merge one more commit onto `wave-int/0` (simulating an unrecorded per-task merge) without re-recording ownership; re-run the reuse check's read+verify logic (`wave-int-status` + `git merge-base --is-ancestor <recorded> wave-int/0`) — confirm it reports "reuse" (exit 0 ancestor check), not a mismatch.
  - [ ] AC2 (unset-owner variant): create `wave-int/1` with no `wave-int-owner` call; confirm the verify logic's owner check reports mismatch.
  - [ ] AC2 (owner-mismatch variant): record `wave-int-owner 1 --tip-sha <sha>` under one `run_id`, then simulate a second run by hand-writing a different `run_id` into a copy of the state file; confirm the mismatch is reported for the second run's perspective.
  - [ ] AC3: record a tip SHA, then force-reset `wave-int/<N>` to an unrelated commit (or amend, changing history); confirm `git merge-base --is-ancestor <recorded> wave-int/<N>` exits non-zero and the scenario reports `wave-int-tip-mismatch`, not `wave-int-materialize-failed`.
  - [ ] AC3 (cat-file-failure variant): record a tip SHA, then delete that commit's reachability (e.g. reset --hard to drop it and `git gc --prune=now`); confirm `git cat-file -e <recorded-sha>` fails and the scenario reports `wave-int-materialize-failed`, not `wave-int-tip-mismatch`.
  - [ ] AC4: push `wave-int/2` to the bare "origin" repo only, delete the local branch (`git branch -D wave-int/2`); confirm the materialization step (`git fetch origin wave-int/2:wave-int/2`) succeeds and `git rev-parse --verify wave-int/2` succeeds afterward.
  - [ ] AC9: record `wave-int-owner 3 --tip-sha <sha>` for a branch that is then deleted both locally and from origin; confirm the verify logic reports `wave-int-branch-missing`.
- [ ] Add a top-level summary print (`N passed, M failed`) and `exit 1` if `M > 0`.

## Task Verify
- [ ] `bash scripts/test-wave-int-checkpoint-ownership.sh` — exits 0.
- [ ] `bash scripts/test-wave-int-checkpoint-ownership.sh --root claude-code/skills/scripts/update-state.py` — exits 0.
- [ ] `bash scripts/test-wave-int-checkpoint-ownership.sh --root codex/skills/scripts/update-state.py` — exits 0.
- [ ] Temporarily break one assertion on purpose (e.g. change an expected string) and confirm the script exits non-zero and prints a `FAIL` line — then revert the temporary change before finishing.

## Verification
- [ ] `bash scripts/validate.sh` exits 0 (includes shellcheck on the new script).
- [ ] No lint/typecheck/build/test toolchain applies to this repository beyond `scripts/validate.sh`.

## Implementation Notes (optional)
