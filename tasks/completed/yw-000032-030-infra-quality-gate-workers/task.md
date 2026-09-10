# yw-000032-030-infra-quality-gate-workers — Implementation Checklist

## Prerequisites
- [ ] `yw-000031-010-docs-quality-gate-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within the two new TOML agents, Codex agent catalog, validation/install fixtures, and agent eval files.

## Stop Conditions
- [ ] Stop if either worker needs production/test ownership outside its declared boundary.
- [ ] Stop if a worker requests delivery authority or raw command authority.

## Hardening Gate
- [ ] Classify as critical agent-contract behavior.
- [ ] Write failing contract-eval/install evidence before production contract edits.
- [ ] Record the worker result interface and require full review.
- [ ] Apply the Data Integrity Hardening fields from `README.md`.

## Implementation Steps
- [ ] Create `codex/agents/ywc-complexity-cleaner.toml` with `gpt-5.6-terra`, medium/high reasoning, `workspace-write`, production-only Ownership, baseline test evidence, and no-delivery restrictions.
- [ ] Create `codex/agents/ywc-test-hardener.toml` with the same model contract, test/fixture-only Ownership, three-attempt cap, residual reporting, and no equivalence claim.
- [ ] Update `codex/agents/README.md` and `scripts/validate.sh` so only these exact TOMLs may use `workspace-write`.
- [ ] Add/extend agent evals and installer assertions for missing packet, scope violation, unavailable tool, residual survivor, status, and no-delivery cases.

## Task Verify
- [ ] `bash tests/install-codex-agents-test.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `rg -n "workspace-write|production|tests|fixtures|staging|commit|push|merge|delivery|three" codex/agents/ywc-complexity-cleaner.toml codex/agents/ywc-test-hardener.toml scripts/validate.sh`

## Verification
- [ ] Agent install test passes (`bash tests/install-codex-agents-test.sh`)
- [ ] Repository validation passes (`bash scripts/validate.sh`)
