# 000066-010-infra-eval-ci-workflow-docs

## Purpose

완성된 evaluator를 repository CI 운영으로 연결한다. PR은 mocked/schema/lint만 수행하고, live deterministic은 scheduled/manual gated suite로 한정하며, expensive ablation은 manual-only로 유지한다.

## Scope

- `.github/workflows/codex-skill-evals.yml`에 weekly schedule과 `workflow_dispatch` mocked/live selection을 추가한다.
- credential provider/API-egress policy가 없으면 live suite를 disabled 또는 infrastructure-unavailable로 처리한다.
- summary/report 위치, status-specific exit code, seven-day cleanup, 10 MB cap-before-upload을 workflow로 검증한다.
- local evaluator SKILL/README command matrix와 artifact boundary를 새 interface에 맞춰 갱신한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-2-amendments` — workflow, run path, suite gating, exit policy, cleanup
- `docs/ywc-plans/codex-skill-eval-upgrade.md#revised-rollout` — PR mocked checks → adapter/manual validation → scheduled live → manual ablation 순서

### Summary

CI는 finalized validator, runner, result schema, migrated fixture inventory를 호출만 해야 하며 그들의 source of truth가 되어서는 안 된다. Live suite는 configured credential-provider handoff와 explicit API-egress policy가 있어야 한다. `SKIPPED_UNAVAILABLE`은 silently green이 아닌 infrastructure alert이며, `INCONCLUSIVE`은 manual ablation에서만 zero exit를 허용한다.

### Out of Scope (from spec)

- Evaluator implementation changes — `000064-010`, `000064-020`, `000065-010`
- Fixture authoring — `000065-020-test-v2-fixture-migration`
- Live credential provisioning or API-egress infrastructure creation — deployment owner decision required
- Automatic retirement — spec out of scope

## Dependencies

### Depends On

- `000065-010-domain-results-artifacts-ablation` — result summary, cleanup, status exit contract
- `000065-020-test-v2-fixture-migration` — complete initial V2 fixture inventory

### Depended By

- (None — final operationalization task)

## Key Files

- `.github/workflows/codex-skill-evals.yml` — mocked/live workflow gates
- `.github/workflows/validate.yml` — PR mocked/schema/lint integration if required
- `.codex/skills/ywc-codex-toolkit-eval/SKILL.md` — command matrix and operational boundary
- `.codex/skills/ywc-codex-toolkit-eval/README*.md` — localized evaluator usage docs
- `.gitignore` — generated evaluator artifact exclusions

## Notes

- Report artifacts are gitignored; only an intentionally reviewed report or scoreboard may be committed separately.
- Cleanup must delete retained failed-run directories older than seven days and enforce the cap before upload.
- Do not make `scripts/validate.sh` execute a live model suite.

## Hardening Evidence

### Test Feedback Path

- RED-first target: workflow contract tests using fake adapter/fixture and `.github/workflows/codex-skill-evals.yml` inspection

### Interface Contract

- Contract: evaluator CI command matrix and status exit policy
- Inputs: suite selection (`mocked`/`live`), credential provider configuration, API-egress policy, result summary
- Outputs: job outcome, machine summary, human report, infrastructure alert
- Error model: `PASS=0`, `FAIL=1`, `ERROR=2`, `SKIPPED_UNAVAILABLE=3`, manual-ablation-only `INCONCLUSIVE=0`
- Impacted tests: fake workflow command tests and evaluator CLI exit tests

### Critical Surface Review

- Review requirement: manual full implementation review — CI can expose credentials or make unintended live calls.

### Data Integrity Hardening

- Trigger surface: shared mutable state
- Atomic / locking strategy: unique run ID directories; workflow cleanup scopes only evaluator artifact root
- Transaction boundary: cap/redact/cleanup before upload and summary publication
- Idempotency guard: cleanup is repeat-safe and never targets outside evaluator artifact root
- Required tests: stale retained-run cleanup, cap enforcement, status exit mapping, live gate rejection

## Parallel Execution Metadata

### Ownership

- `.github/workflows/codex-skill-evals.yml`
- `.github/workflows/validate.yml`
- `.codex/skills/ywc-codex-toolkit-eval/SKILL.md`
- `.codex/skills/ywc-codex-toolkit-eval/README*.md`
- `.gitignore`

### Shared Surfaces

- GitHub Actions credentials and API-egress policy
- Evaluator result schema and artifact root
- Repository PR validation pipeline

### Conflicts With

- `000065-010-domain-results-artifacts-ablation` — workflow exit/retention policy must not diverge from result code.
- `000065-020-test-v2-fixture-migration` — workflow fixture selection must use final migrated inventory.

### Parallelizable After

- `000065-010-domain-results-artifacts-ablation`
- `000065-020-test-v2-fixture-migration`

### Task Verify

- `bash scripts/validate.sh`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --suite mocked`
- workflow fake-adapter contract test command added by this task

## Out of Scope

- Production secret creation, live provider selection, cost-cap approval, and any general CI refactor unrelated to evaluator operation.
