# 000066-010-infra-eval-ci-workflow-docs — Implementation Checklist

## Prerequisites

- [ ] `000065-010-domain-results-artifacts-ablation` is completed and merged.
- [ ] `000065-020-test-v2-fixture-migration` is completed and merged.

## Allowed Edit Scope

- [ ] Stay within workflow, local evaluator documentation, and artifact ignore paths in `README.md`.
- [ ] Stop before changing runner/result behavior or fixture content.

## Stop Conditions

- [ ] Stop if live execution needs a credential provider or API-egress policy that has not been configured by the deployment owner.
- [ ] Stop if a workflow step would upload credentials, raw environment dumps, or unbounded transcripts.
- [ ] Stop if cleanup target cannot be resolved under the evaluator artifact root.
- [ ] Stop if PR validation requires live-suite statuses or live model access.

## Hardening Gate

- [ ] Classify this task as security-sensitive CI infrastructure.
- [ ] Add failing fake-adapter/workflow contract tests for suite gates, status exits, retention cap, and stale cleanup.
- [ ] Record the CI input/output/exit contract before editing workflow YAML.
- [ ] Apply shared-state hardening with run-ID-scoped artifact paths and idempotent cleanup.
- [ ] Require full implementation review before `DONE`.

## Implementation Steps

- [ ] Add `.github/workflows/codex-skill-evals.yml`.
  - [ ] Trigger weekly and `workflow_dispatch`; expose `mocked`/`live` suite selection.
  - [ ] Run schema/lint/mock verifier tests for PR-safe paths only.
  - [ ] Gate live execution on configured credential-provider handoff and API-egress policy; otherwise surface `SKIPPED_UNAVAILABLE` infrastructure status.
- [ ] Implement workflow result handling.
  - [ ] Write `docs/skill-agent-eval/codex/runs/<run-id>/summary.json` and a human report under the gitignored artifact policy.
  - [ ] Map `PASS`, `FAIL`, `ERROR`, and `SKIPPED_UNAVAILABLE` to exits 0/1/2/3.
  - [ ] Permit `INCONCLUSIVE=0` only in manual ablation and prevent it from becoming a retire decision.
- [ ] Add bounded cleanup/upload protections.
  - [ ] Delete only retained failed-run directories older than seven days under the resolved evaluator artifact root.
  - [ ] Enforce the 10 MB cap and redaction before artifact upload.
  - [ ] Test cleanup with fake run directories and ensure no credential/raw environment artifact path is selected.
- [ ] Update `.codex/skills/ywc-codex-toolkit-eval/SKILL.md` and localized README files with the finalized command matrix, local-only boundary, suite gating, and report policy.
- [ ] Integrate only mocked/schema/lint evaluator checks into the existing PR validation path when needed, then run full bundle validation.

## Task Verify

- [ ] `bash scripts/validate.sh`
- [ ] Run the new workflow's mocked command sequence with the fake adapter.
- [ ] Run the workflow contract tests for status mapping, live gating, cap-before-upload, and seven-day cleanup.

## Verification

- [ ] Workflow and documentation contract tests pass.
- [ ] `bash scripts/validate.sh` passes.
- [ ] No PR path invokes a live model suite or uses production credentials.
