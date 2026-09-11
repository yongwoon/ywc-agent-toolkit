# yw-000036-010-domain-parallel-executor-state-schema — Implementation Checklist

## Prerequisites
- [ ] None — this is a root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/scripts/update-state.py` only.

## Stop Conditions
- [ ] Stop if `cmd_init_parallel` or the `wave-start`/`task-merged`/`wave-complete` subcommands already read/write a field named `integration_branch`, `hardener_verdict`, or `promotion_retry_count`.
- [ ] Stop if adding the new subcommand(s) would require changing the signature or call shape of any existing subcommand — the spec requires additive-only, `setdefault`-style changes.
- [ ] Stop if implementing this task requires touching `codex/skills/scripts/update-state.py`, `save-state.py`, or `resume-state.py` — those are out of scope for this task.

## Implementation Steps
- [ ] In `cmd_init_parallel`, after the existing `wave.setdefault("pending", ...)` line, add:
  - [ ] `has_contract = bool(wave.get("has_contract", False))`
  - [ ] `wave.setdefault("integration_branch", f"wave-int/{wave['wave']}" if has_contract else None)`
  - [ ] Do not mutate `has_contract` back into the saved wave dict unless it is already part of the input `--waves` entry (avoid inventing a new persisted field beyond the three named in the spec).
- [ ] Add a new argparse subparser (e.g. `hardener-verdict`) taking `wave: int` and `verdict: str`, validated against `{"absent", "PASS", "BLOCKED"}` (reject anything else via the existing `die()`-style error-exit convention), and a handler `cmd_hardener_verdict` that:
  - [ ] `load()`s state, `require_executor(state, "parallel", "hardener-verdict")`, `find_wave(state, args.wave)`.
  - [ ] Sets `wave["hardener_verdict"] = args.verdict`.
  - [ ] `save(state)` and prints a one-line confirmation, matching `cmd_task_merged`'s print style.
- [ ] Add a new argparse subparser (e.g. `promotion-retry`) taking `wave: int`, and a handler `cmd_promotion_retry` that:
  - [ ] `load()`s state, `require_executor(state, "parallel", "promotion-retry")`, `find_wave(state, args.wave)`.
  - [ ] `wave["promotion_retry_count"] = wave.get("promotion_retry_count", 0) + 1`.
  - [ ] `save(state)` and prints the new count.
- [ ] Update the module docstring's `Subcommands:` list to include the two new subcommands, matching the existing one-line-per-subcommand format.
- [ ] Register both new subparsers in the file's `main()`/argparse-setup section, alongside the existing `wave-start` / `task-merged` / `wave-complete` registrations.

## Task Verify
- [ ] `python3 claude-code/skills/scripts/update-state.py init-parallel --mode local-merge --tasks-dir tasks/ --waves '[{"wave":1,"tasks":["t-a"],"has_contract":true},{"wave":2,"tasks":["t-b"],"has_contract":false}]'` — confirm `.ywc-run-state.json` has `waves[0].integration_branch == "wave-int/1"` and `waves[1].integration_branch == null`.
- [ ] Re-run `init-parallel` with a `--waves` entry that omits `has_contract` entirely — confirm `integration_branch` is `null` for that wave.
- [ ] `python3 claude-code/skills/scripts/update-state.py hardener-verdict 1 PASS` then `hardener-verdict 1 absent` — confirm the field round-trips through both values.
- [ ] `python3 claude-code/skills/scripts/update-state.py hardener-verdict 1 bogus` — confirm it exits non-zero and does not write the state file.
- [ ] `python3 claude-code/skills/scripts/update-state.py promotion-retry 1` (run twice) — confirm `waves[0].promotion_retry_count == 2`.
- [ ] `grep -q 'gate_state' claude-code/skills/scripts/update-state.py` — confirm no match.

## Verification
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] No lint/typecheck/build/test toolchain applies to this repository beyond `scripts/validate.sh`.

## Implementation Notes (optional)
