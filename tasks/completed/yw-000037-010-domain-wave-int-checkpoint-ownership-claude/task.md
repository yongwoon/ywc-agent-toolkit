# yw-000037-010-domain-wave-int-checkpoint-ownership-claude — Implementation Checklist

## Prerequisites
- [ ] None — this is a root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/scripts/update-state.py`, `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md`, `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md`.

## Stop Conditions
- [ ] Stop if `cmd_init_parallel` or any existing subcommand already reads/writes a field named `run_id`, `integration_branch_owner`, or `integration_branch_tip_sha`.
- [ ] Stop if implementing this task requires touching `codex/skills/scripts/update-state.py` or any file under `codex/skills/` — that is `yw-000037-020`.
- [ ] Stop if the wave-integration-branch rewrite would need to change the promotion fast-forward / base-merge-in / Hardener re-run sequence (`wave-integration-branch.md:54-85`) — this task's verification runs strictly before that sequence and must not alter it.
- [ ] Stop if writing the reuse-verification steps would require a new `save-state.py` / `resume-state.py` field beyond documentation updates — those scripts are read-only consumers and out of scope per the parent spec's precedent.

## Implementation Steps

### `update-state.py` — FR-1: `run_id`
- [ ] Add `import uuid` to the top-level imports.
- [ ] In `cmd_init_parallel`, add `"run_id": uuid.uuid4().hex[:8]` to the `save({...})` dict literal, alongside `executor`, `mode`, `tasks_dir`, `started_at`, `current_wave`, `waves`.
- [ ] Do not add any code path that mutates `run_id` after `init-parallel` — no subcommand may reassign it.

### `update-state.py` — FR-2: three new subcommands
- [ ] Add `cmd_wave_int_owner(args)`: `state = load()`; if `state.get("executor") != "parallel"` → `die(f"'wave-int-owner' requires executor='parallel', but state is '{state.get('executor')}'")`; if not `state.get("run_id")` → `die("state has no run_id — re-run init-parallel (state predates wave-int ownership tracking)")`; `wave = find_wave(state, args.n)`; set `wave["integration_branch_owner"] = state["run_id"]`, `wave["integration_branch_tip_sha"] = args.tip_sha`; `save(state)`; print `f"wave {args.n}: integration_branch_owner -> {state['run_id']}, tip_sha -> {args.tip_sha}"`.
- [ ] Add `cmd_wave_int_blocked(args)`: same `executor`/`run_id` checks as above, then `wave = find_wave(state, args.n)`; set `wave["status"] = "BLOCKED"`, `wave["reason"] = args.reason`; if `args.detail` is not `None`, set `wave["blocked_detail"] = args.detail`; `save(state)`; print `f"wave {args.n}: status -> BLOCKED ({args.reason}) — {args.detail}"` when `args.detail` given, else `f"wave {args.n}: status -> BLOCKED ({args.reason})"`.
- [ ] Add `cmd_wave_int_status(args)`: `state = load()`; if `state.get("executor") != "parallel"` → `die(...)` matching the same message shape as above (no `run_id` check); `wave = find_wave(state, args.n)`; print `f"{wave.get('integration_branch_owner', 'unset')} {wave.get('integration_branch_tip_sha', 'unset')}"`; do **not** call `save()`.
- [ ] Register three new argparse subparsers: `wave-int-owner` (positional `n: int`, `--tip-sha` required), `wave-int-blocked` (positional `n: int`, `--reason` required, `--detail` optional default `None`), `wave-int-status` (positional `n: int` only).
- [ ] Update the module docstring's `Subcommands:` list to add the three new lines, matching the existing one-line-per-subcommand format.

### `wave-integration-branch.md` — FR-3/FR-4/FR-5
- [ ] Rewrite the "Idempotent creation" section (current `:26-32`) into the 5-step procedure from spec FR-3: (1) `wave-int-status <N>` read, (2) existence check unchanged, (3) branch-missing-but-owned → `wave-int-blocked --reason wave-int-branch-missing`, (4) branch-does-not-exist-no-owner → fresh creation then `wave-int-owner` (AC6 creation half), (5) branch-exists → owner-unset or owner-mismatch → `wave-int-blocked --reason wave-int-ownership-mismatch`; owner-matched → materialize (FR-4) → `git cat-file -e` → on failure `wave-int-blocked --reason wave-int-materialize-failed`; on success `git merge-base --is-ancestor` → non-zero → `wave-int-blocked --reason wave-int-tip-mismatch`; zero → reuse (AC1).
- [ ] Insert FR-4's origin-only materialization block (`git fetch origin wave-int/<N>:wave-int/<N>`) as the first sub-step under 5's "owner matched" branch, before the `cat-file`/ancestor checks.
- [ ] Insert the `wave-int-owner <N> --tip-sha <new-branch-tip-sha>` call immediately after the existing `git push origin wave-int/<N>` at the creation block (current `:34-39`).
- [ ] Insert the `wave-int-owner <N> --tip-sha <sha>` call immediately after the existing `git push origin wave-int/<N>` in the promotion-conflict base-merge block (current `:70-77`).
- [ ] Use the exact `--detail` strings from spec FR-3 steps 3/5.1/5.2/5.3 (e.g. `"branch=wave-int/<N> recorded-owner=<owner> recorded-tip=<tip-sha>"`) — do not paraphrase.

### `checkpoint-resume.md`
- [ ] Update the "State File Format" JSON block to add top-level `run_id` and the per-wave `integration_branch_owner` / `integration_branch_tip_sha` fields, matching the spec's Data Model section exactly.
- [ ] Add a row to the Checkpoint Summary table for the `wave-int-owner` write at creation and at post-base-merge (mirroring the existing `hardener-verdict` row's phrasing).
- [ ] Extend the "Resume with `wave-int/<N>`" section's case 1 (Partial-merge) to note that same-run resume passes the ownership/tip-SHA check trivially — `run_id` and the last recorded tip SHA are already present in this run's own state file.

## Task Verify
- [ ] `python3 claude-code/skills/scripts/update-state.py init-parallel --mode local-merge --tasks-dir tasks/ --waves '[{"wave":1,"tasks":["t-a"],"has_contract":true}]'` — confirm `.ywc-run-state.json` has a non-empty top-level `run_id` (8 hex chars).
- [ ] `python3 claude-code/skills/scripts/update-state.py wave-int-owner 1 --tip-sha abc123` — confirm `waves[0].integration_branch_owner` equals the recorded `run_id`, `integration_branch_tip_sha == "abc123"`.
- [ ] `python3 claude-code/skills/scripts/update-state.py wave-int-status 1` — confirm output is `<run_id> abc123`.
- [ ] `python3 claude-code/skills/scripts/update-state.py wave-int-blocked 1 --reason wave-int-tip-mismatch --detail "branch=wave-int/1 recorded=abc123 actual=def456"` — confirm `waves[0].status == "BLOCKED"`, `reason == "wave-int-tip-mismatch"`, `blocked_detail` matches verbatim.
- [ ] `python3 claude-code/skills/scripts/update-state.py wave-int-status 2` (a wave with no owner/tip-sha ever set) — confirm output is `unset unset`, exit 0.
- [ ] Hand-strip `run_id` from the state file with `python3 -c "..."`, then `wave-int-owner 1 --tip-sha x` — confirm non-zero exit, stderr contains `re-run init-parallel`, and the file is unchanged (`git diff` / byte comparison against a saved copy); `wave-int-status 1` against the same stripped file — confirm it still succeeds.
- [ ] `grep -n 'wave-int-owner\|wave-int-blocked\|wave-int-status' claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md` — confirm all three appear at the call sites described above.
- [ ] `grep -n 'run_id\|integration_branch_owner\|integration_branch_tip_sha' claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md` — confirm the new fields are documented.

## Verification
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] No lint/typecheck/build/test toolchain applies to this repository beyond `scripts/validate.sh`.

## Implementation Notes (optional)
