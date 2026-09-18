# yw-000051-020-docs-mobile-first-reviewer — Implementation Checklist

## Prerequisites
- [ ] `yw-000050-010-docs-mobile-first-policy` is completed and merged.
- [ ] The shared policy reference exists at `codex/skills/references/mobile-first-ui.md`.

## Allowed Edit Scope
- [ ] Modify only the reviewer TOML and the single eval record in Ownership.
- [ ] Stop before editing the deterministic runner or generated plugin.

## Stop Conditions
- [ ] Stop if the reviewer must infer end-user UI or PC/tablet-only intent.
- [ ] Stop if the change expands beyond the bounded TS/JS diff or read-only contract.
- [ ] Stop if the eval schema or existing agent scenarios require unrelated changes.

## Hardening Gate
- [ ] Classify as bounded read-only contract/eval work.
- [ ] Use `bash scripts/check-codex-agent-evals.sh` as existing coverage and add source-contract verification downstream.
- [ ] Record the bounded reviewer interface and return `NEEDS_CONTEXT` for missing target-surface evidence.
- [ ] Mark data integrity and critical review as N/A.

## Implementation Steps
- [ ] Update `codex/agents/ywc-typescript-reviewer.toml` with the conditional Framework-idiom check.
  - Trigger only for end-user UI layout/style changes identified in the evidence packet.
  - Read the shared policy and flag desktop-first claw-back patterns.
  - Skip legacy UI without explicit redesign scope and return `NEEDS_CONTEXT` for missing scope evidence.
- [ ] Add one `ywc-typescript-reviewer` scenario to `codex/agents/evals/evals.json`.
  - Cover an in-scope violation and the bounded expected finding/status.
  - Preserve read-only and no-delivery expectations.
- [ ] Confirm no new agent role or sandbox/model contract is introduced.

## Task Verify
- [ ] `jq empty codex/agents/evals/evals.json`
- [ ] `bash scripts/check-codex-agent-evals.sh`
- [ ] `git diff --check`

## Verification
- [ ] lint passes (`N/A — repository has no separate TOML/Markdown lint command in AGENTS.md`)
- [ ] typecheck passes (`N/A — agent contract/eval data only`)
- [ ] unit tests pass (`bash scripts/check-codex-agent-evals.sh`)
- [ ] integration tests pass (`N/A — no runtime integration`)
- [ ] app builds without error (`N/A — agent contract/eval data only`)

## Implementation Notes

