# yw-000037-020-domain-wave-int-checkpoint-ownership-codex — Implementation Checklist

## Prerequisites
- [ ] None — this is a root task (parallel-safe against `yw-000037-010`; touches disjoint files).

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `codex/skills/scripts/update-state.py`, `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md`, `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md`, plus the regenerated `plugins/ywc-agent-toolkit/skills/ywc-parallel-executor/**` and `plugins/ywc-agent-toolkit/skills/scripts/update-state.py` (via sync script only).

## Stop Conditions
- [ ] Stop if implementing this task requires touching `claude-code/skills/scripts/update-state.py` or any file under `claude-code/skills/` — that is `yw-000037-010`.
- [ ] Stop if `bash scripts/sync-codex-plugin.sh` reports an error, or leaves a diff under `plugins/ywc-agent-toolkit` other than the expected `codex/skills/ywc-parallel-executor` mirror update — surface `NEEDS_CONTEXT` rather than hand-editing the plugin path to force a match.
- [ ] Stop if hand-editing anything under `plugins/ywc-agent-toolkit/skills/` directly — the only permitted path to that directory is `scripts/sync-codex-plugin.sh`.
- [ ] Stop if the codex `wave-integration-branch.md` or `update-state.py` have already diverged in unrelated ways from the claude-code copy such that the line-for-line mirroring assumption in this task's Notes does not hold — report the divergence and ask before applying the edit blind.

## Implementation Steps

### `update-state.py` — FR-1/FR-2 (mirror of `yw-000037-010`)
- [ ] Add `import uuid` to the top-level imports.
- [ ] In `cmd_init_parallel`, add `"run_id": uuid.uuid4().hex[:8]` to the `save({...})` dict literal.
- [ ] Add `cmd_wave_int_owner(args)`, `cmd_wave_int_blocked(args)`, `cmd_wave_int_status(args)` with identical logic to `yw-000037-010`'s claude-code implementation (`die()` message text, print format, `run_id` precondition present on the first two, absent on `wave-int-status`).
- [ ] Register the three new argparse subparsers with identical argument shapes to the claude-code copy.
- [ ] Update the module docstring's `Subcommands:` list.

### `wave-integration-branch.md` — FR-3/FR-4/FR-5 (mirror of `yw-000037-010`)
- [ ] Rewrite the "Idempotent creation" section into the same 5-step procedure as `yw-000037-010`, adjusted only for any pre-existing codex-specific prose differences (verify none exist for this section before editing — see Stop Conditions).
- [ ] Insert the FR-4 origin-only materialization block and the two FR-5 `wave-int-owner` call sites at the codex copy's equivalent locations.
- [ ] Use the identical `--detail` strings as the claude-code copy.

### `checkpoint-resume.md` (mirror of `yw-000037-010`)
- [ ] Update the "State File Format" JSON block, Checkpoint Summary table row, and "Resume with `wave-int/<N>`" section identically to `yw-000037-010`.

### Plugin mirror regeneration (AC8)
- [ ] After the three edits above are committed (this task's own commit), run `bash scripts/sync-codex-plugin.sh`.
- [ ] `git add -A plugins/ywc-agent-toolkit` and confirm the staged diff contains only the expected `ywc-parallel-executor` (and its shared `scripts/update-state.py`) changes — no unrelated skill directories.
- [ ] Do not hand-edit any file under `plugins/ywc-agent-toolkit/skills/` — if the sync output looks wrong, fix the `codex/skills/` source and re-run the sync script, never patch the mirror directly.

## Task Verify
- [ ] `python3 codex/skills/scripts/update-state.py init-parallel --mode local-merge --tasks-dir tasks/ --waves '[{"wave":1,"tasks":["t-a"],"has_contract":true}]'` — confirm non-empty top-level `run_id`.
- [ ] `python3 codex/skills/scripts/update-state.py wave-int-owner 1 --tip-sha abc123` then `wave-int-status 1` — confirm output `<run_id> abc123`.
- [ ] `python3 codex/skills/scripts/update-state.py wave-int-blocked 1 --reason wave-int-branch-missing --detail "branch=wave-int/1 recorded-owner=abc recorded-tip=def"` — confirm `waves[0].status == "BLOCKED"`, `blocked_detail` matches verbatim.
- [ ] `python3 codex/skills/scripts/update-state.py wave-int-status 2` (unset wave) — confirm output `unset unset`.
- [ ] `diff <(sed -n '204,285p' codex/skills/scripts/update-state.py) <(sed -n '204,285p' claude-code/skills/scripts/update-state.py)` (line numbers approximate — adjust to the actual new-subcommand region) — confirm the new subcommand handlers are behaviorally identical between roots (AC8).
- [ ] `bash scripts/sync-codex-plugin.sh && git add -A plugins/ywc-agent-toolkit`; `diff -r codex/skills/ywc-parallel-executor plugins/ywc-agent-toolkit/skills/ywc-parallel-executor` exits 0; `diff codex/skills/scripts/update-state.py plugins/ywc-agent-toolkit/skills/scripts/update-state.py` exits 0.

## Verification
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] No lint/typecheck/build/test toolchain applies to this repository beyond `scripts/validate.sh`.

## Implementation Notes (optional)
