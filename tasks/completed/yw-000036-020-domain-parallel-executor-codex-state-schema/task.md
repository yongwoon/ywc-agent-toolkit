# yw-000036-020-domain-parallel-executor-codex-state-schema — Implementation Checklist

## Prerequisites
- [ ] `yw-000036-010-domain-parallel-executor-state-schema` is completed (merged) — establishes the exact field names, seed logic, and subcommand shapes this task mirrors.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `codex/skills/scripts/update-state.py` only.

## Stop Conditions
- [ ] Stop if `yw-000036-010`'s chosen subcommand names or field names cannot be determined (e.g., its task is not actually merged).
- [ ] Stop if `codex/skills/scripts/update-state.py` has already diverged from `claude-code/skills/scripts/update-state.py` by more than the known single docstring line before this task starts — investigate and report rather than papering over an unexpected divergence.
- [ ] Stop if mirroring the edit would require a codex-specific behavior change (it should not — this is a byte-for-byte-shape port).

## Implementation Steps
- [ ] Read the merged `claude-code/skills/scripts/update-state.py` diff from `yw-000036-010` (or the file itself) to get the exact subcommand names, field names, and code shape.
- [ ] In `codex/skills/scripts/update-state.py`'s `cmd_init_parallel`, apply the identical `has_contract` read + `integration_branch` `setdefault` seed.
- [ ] Add the identical `hardener-verdict` and `promotion-retry` subcommands (same names, same argument shapes, same handler logic) as `yw-000036-010`.
- [ ] Update this file's module docstring `Subcommands:` list identically (keep the one pre-existing docstring-line difference between the two files untouched — do not accidentally make the docstrings fully identical or introduce a new difference).
- [ ] Register both new subparsers in `main()`/argparse setup, mirroring the claude-code file's registration order.

## Task Verify
- [ ] Re-run every functional check from `yw-000036-010`'s Task Verify against `codex/skills/scripts/update-state.py`.
- [ ] `diff claude-code/skills/scripts/update-state.py codex/skills/scripts/update-state.py` — confirm exactly one line differs (the pre-existing docstring line), no more, no less.
- [ ] `grep -q 'contract_state' codex/skills/scripts/update-state.py` — must find no match (this script writes neither `gate_state` nor `contract_state`; those are prose-level fields, not state-file fields).

## Verification
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] No lint/typecheck/build/test toolchain applies to this repository beyond `scripts/validate.sh`.

## Implementation Notes (optional)
