# 000065-020-test-v2-fixture-migration — Implementation Checklist

## Prerequisites

- [ ] `000064-010-infra-evaluator-discovery-schema-registry` is completed and merged.
- [ ] `000064-020-domain-isolated-runner-adapter` is completed and merged.

## Allowed Edit Scope

- [ ] Stay within the four named skill eval directories and evaluator fixture paths in `README.md`.
- [ ] Stop before editing skill instructions, evaluator schema/registry code, runner code, or CI workflows.

## Stop Conditions

- [ ] Stop if a case needs a raw shell command, host mutation, external credential, or unregistered verifier.
- [ ] Stop if the intended target/dependency cannot be resolved from `codex/skills/<name>/`.
- [ ] Stop if a fixture output requires a path outside its `fixture_root` and declared `output_paths`.
- [ ] Stop if the representative agent needs a new agent schema rather than the evaluator-owned extension.

## Hardening Gate

- [ ] Classify this task as test-only safety coverage.
- [ ] Validate a deliberately invalid fixture before adding happy-path data.
- [ ] Record every fixture's expected/forbidden signals and mock/dry-run evidence contract.
- [ ] Mark Data Integrity `N/A`: no live infrastructure change is allowed.
- [ ] Require full review because infrastructure instructions can otherwise normalize unsafe actions.

## Implementation Steps

- [ ] Create V2 fixture roots and manifests for the four uncovered skills.
  - [ ] Add one `happy_path` case per skill with `schema: 2`, language, trigger expectation, evidence packet, and registry verifier IDs.
  - [ ] Add one `negative` or `boundary` case per skill that proves refusal/safe constraint behavior.
  - [ ] Use mock fixtures or dry-run contracts only; declare all copied inputs and permitted outputs.
- [ ] Extend `agent-smoke-fixtures.json` with one representative V2 agent fixture.
  - [ ] Declare target TOML agent, isolated evidence packet, expected status/signals, forbidden signals, and fixture-local output path.
  - [ ] Keep existing schema-1 captured-output fixtures compatible and unmodified unless explicitly migrated.
- [ ] Run the V2 validator and fake adapter for all migrated cases.
  - [ ] Assert no arbitrary command or executable path is accepted.
  - [ ] Assert the migration report shows V2 coverage for all four skills and the chosen agent.
  - [ ] Record remaining V1 fixtures as backlog signal, not as validation failure.

## Task Verify

- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/fixture_validator.py --repo-root . --report`
- [ ] Run fake-adapter cases for the four skills and representative agent fixture.

## Verification

- [ ] All new cases validate as V2.
- [ ] Existing V1 fixtures remain readable.
- [ ] `bash scripts/validate.sh` passes.
