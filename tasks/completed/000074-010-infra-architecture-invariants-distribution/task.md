# 000074-010-infra-architecture-invariants-distribution — Implementation Checklist

## Prerequisites
- [ ] `000073-010-domain-architecture-invariants-contract` is completed and merged.
- [ ] `000073-020-test-architecture-invariants-evaluator` is completed and merged.
- [ ] `000073-030-refactor-architecture-consumer-packets` is completed and merged.
- [ ] `000073-040-domain-architecture-run-evidence` is completed and merged.

## Allowed Edit Scope
- [ ] Modify generated `plugins/ywc-agent-toolkit/**` through the sync script.
- [ ] Modify release metadata or `scripts/validate.sh` only when a concrete inventory check requires it.
- [ ] Use a temporary `CODEX_HOME` for installation checks.

## Stop Conditions
- [ ] Stop if source and generated package differ after synchronization.
- [ ] Stop if validation requires broad unrelated changes.
- [ ] Stop if installation writes to the real user Codex directory.
- [ ] Stop if any final check reveals executable manifest/evidence fields or raw evidence forwarding.

## Hardening Gate
- RED-first evidence: all predecessor fixtures and source contract checks must be green before package synchronization.
- Public contract: generated package mirrors the finalized source skill/helper and metadata.
- Data Integrity Hardening: N/A — distribution-only task.
- Critical review: inspect generated and metadata diffs for secret/local-artifact leakage and forbidden command fields.

## Implementation Steps
- [ ] Run `bash scripts/sync-codex-plugin.sh` and confirm the new skill and shared helper are represented in `plugins/ywc-agent-toolkit`.
  - Related AC/FR: AC8 / Iteration 2 A, E
  - Contract / Behavior Change: marketplace package matches Codex source of truth.
  - Verification Command / Evidence: sync completes and stale-package checks pass.
- [ ] Add only required release metadata/inventory entries for `ywc-architecture-invariants`, preserving existing bundle conventions.
  - Related AC/FR: AC8 / FR-6
  - Contract / Behavior Change: install and validation tooling recognizes the new skill.
  - Verification Command / Evidence: `bash scripts/install.sh --list` includes the skill.
- [ ] Run full repository validation and the architecture-specific standard-library test/eval commands.
  - Related AC/FR: AC1–AC8 / Iteration 2 A, E
  - Contract / Behavior Change: final source tree passes structure, metadata, contract, and security checks.
  - Verification Command / Evidence: `python3 tests/architecture_invariants_test.py`, `bash scripts/run-codex-skill-contract-evals.sh`, and `bash scripts/validate.sh` exit 0.
- [ ] Run isolated Codex installation smoke with a temporary `CODEX_HOME` and remove the temporary directory after verification.
  - Related AC/FR: AC8 / Verification Plan
  - Contract / Behavior Change: distributable skill installs without mutating the user environment.
  - Verification Command / Evidence: isolated install exits 0 and target skill files exist.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
  - Expected Passing Signal: generated package synchronization exits 0.
  - Pre-change Failing Evidence / Exception: N/A — terminal packaging step.
  - Contract/Test Evidence: stale-package validation passes.
- [ ] `python3 tests/architecture_invariants_test.py && bash scripts/run-codex-skill-contract-evals.sh && bash scripts/validate.sh`
  - Expected Passing Signal: all commands exit 0.
  - Pre-change Failing Evidence / Exception: predecessor tasks provide RED/GREEN fixture history.
  - Contract/Test Evidence: complete AC1–AC8 verification path.
- [ ] `bash scripts/install.sh --list`
  - Expected Passing Signal: `ywc-architecture-invariants` appears in the installable list.
  - Pre-change Failing Evidence / Exception: N/A — new distribution inventory.
  - Contract/Test Evidence: installer scan output.
- [ ] `isolated_codex_home=$(mktemp -d) && CODEX_HOME="$isolated_codex_home" bash scripts/install.sh --codex ywc-architecture-invariants; status=$?; rm -rf "$isolated_codex_home"; exit "$status"`
  - Expected Passing Signal: isolated install exits 0 without writing to the real Codex home.
  - Pre-change Failing Evidence / Exception: N/A — isolated smoke.
  - Contract/Test Evidence: installed skill contains required `SKILL.md` and `agents/openai.yaml`.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — repository skill bundle)
- [ ] unit tests pass (`python3 tests/architecture_invariants_test.py`)
- [ ] integration tests pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] app builds without error (`bash scripts/sync-codex-plugin.sh` plus `bash scripts/validate.sh`)
