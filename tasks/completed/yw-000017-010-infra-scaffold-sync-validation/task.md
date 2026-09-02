# yw-000017-010-infra-scaffold-sync-validation — Implementation Checklist

## Prerequisites
- [ ] `yw-000016-010-test-scaffold-contract-evals` is merged.
- [ ] All Phase 000015 source edits are present in the merged baseline.

## Allowed Edit Scope
- [ ] Run the sync script to update `plugins/ywc-agent-toolkit/skills/`; do not hand-edit generated files.
- [ ] Do not modify source files unless returning a finding to the owning task.

## Stop Conditions
- [ ] Stop if sync reports an error or generated output does not contain source changes.
- [ ] Stop if validation requires unrelated source modifications or a new dependency.
- [ ] Stop if generated files appear to require manual repair.

## Implementation Steps
- [ ] Validate JSON and source contract tokens before packaging.
  - Related AC/FR: AC10–AC11 / FR6
  - Contract / Behavior Change: source fixtures and required terms are syntactically valid before sync.
  - Verification Command / Evidence: `python3 -m json.tool ...` and targeted `rg` checks.
- [ ] Run `bash scripts/sync-codex-plugin.sh` from the repository root.
  - Related AC/FR: AC11 / FR6
  - Contract / Behavior Change: marketplace package is regenerated from Codex source.
  - Verification Command / Evidence: sync output and generated diff.
- [ ] Confirm generated `SKILL.md`, `references/javascript.md`, `references/go.md`, and `evals/evals.json` contain the source changes without manual edits.
  - Related AC/FR: AC11 / FR6
  - Contract / Behavior Change: packaged skill is fresh and distributable.
  - Verification Command / Evidence: `rg -n 'reference-refresh|Trend Check|Naming Convention|Component Logic Colocation|Go Large \(Layered, Connect RPC\)' plugins/ywc-agent-toolkit/skills/ywc-project-scaffold`.
- [ ] Run install listing, contract eval validation, Markdown lint for the three edited source Markdown files, and the full repository validator.
  - Related AC/FR: AC10–AC11 / Verification
  - Contract / Behavior Change: all required local gates pass.
  - Verification Command / Evidence: command exit codes and final diff review.

## Task Verify
- [ ] `python3 -m json.tool codex/skills/ywc-project-scaffold/evals/evals.json >/dev/null && bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: exit 0 and contract validator PASS.
  - Pre-change Failing Evidence / Exception: N/A — final validation task.
  - Contract/Test Evidence: JSON parser and contract harness.
- [ ] `bash scripts/sync-codex-plugin.sh && rg -n 'reference-refresh|Trend Check|Naming Convention|Component Logic Colocation|Go Large \(Layered, Connect RPC\)' plugins/ywc-agent-toolkit/skills/ywc-project-scaffold`
  - Expected Passing Signal: sync succeeds and all required terms appear in generated output.
  - Pre-change Failing Evidence / Exception: N/A — packaging gate.
  - Contract/Test Evidence: generated-package token check.
- [ ] `bash scripts/install.sh --list --codex && bash scripts/validate.sh`
  - Expected Passing Signal: install listing and full repository validation exit 0.
  - Pre-change Failing Evidence / Exception: N/A — repository gate.
  - Contract/Test Evidence: validation output.
- [ ] `npx markdownlint-cli2@0.22.1 codex/skills/ywc-project-scaffold/SKILL.md codex/skills/ywc-project-scaffold/references/javascript.md codex/skills/ywc-project-scaffold/references/go.md`
  - Expected Passing Signal: Markdown lint exits 0, or the repository-installed equivalent passes.
  - Pre-change Failing Evidence / Exception: N/A — use installed equivalent if network/package resolution is unavailable.
  - Contract/Test Evidence: Markdown lint report.

## Verification
- [ ] lint passes (`npx markdownlint-cli2@0.22.1` against the three edited source Markdown files)
- [ ] typecheck passes (N/A — documentation and packaging task)
- [ ] unit tests pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] integration tests pass (`bash scripts/validate.sh`)
- [ ] app builds without error (N/A — repository has no application build)
