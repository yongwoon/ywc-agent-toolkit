# 000065-010-domain-results-artifacts-ablation

## Purpose

Runner 결과를 단일 status, redacted artifact policy, migration/activation metrics, 그리고 paired ablation evidence로 집계한다. 이는 결과를 quality pass로 과장하지 않고 retire 판단을 사람 승인 전용 후보 상태로 제한한다.

## Scope

- result record/status enum, CLI metadata, activation-observability, V1/V2 migration signals을 구현한다.
- capped/redacted artifacts, successful workspace deletion, failed-artifact opt-in retention과 seven-day pruning을 구현한다.
- pass rate, cost completeness, six paired trial rules, `CANDIDATE_FOR_REVIEW`/`INCONCLUSIVE` aggregation을 구현한다.
- machine-readable summary와 human-readable report data model을 만든다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-1-amendments` — status enum, artifact retention, v1/v2 migration, retire rule
- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-2-amendments` — run summary path, exit policy, cleanup and credential redaction

### Summary

이 task는 runner가 만든 normalized outcome을 보존·집계하는 결과 pipeline이다. `SKIPPED_UNAVAILABLE`과 `ERROR`는 quality pass 또는 baseline update가 아니며, activation signal이 없을 때 precision/recall도 보고하지 않는다. Ablation은 manual-only로 six paired trial과 양쪽 cost evidence가 완료된 경우에만 review candidate를 만들 수 있다.

### Out of Scope (from spec)

- Workspace/CLI adapter implementation — `000064-020-domain-isolated-runner-adapter`
- Fixture content migration — `000065-020-test-v2-fixture-migration`
- GitHub workflow wiring and artifact upload cleanup step — `000066-010-infra-eval-ci-workflow-docs`

## Dependencies

### Depends On

- `000064-020-domain-isolated-runner-adapter` — canonical run status, metadata, and workspace lifecycle events

### Depended By

- `000066-010-infra-eval-ci-workflow-docs` — workflow exit policy, summary location, retention/cleanup contract

## Key Files

- `.codex/skills/ywc-codex-toolkit-eval/scripts/results.py` — result record, redaction, aggregation
- `.codex/skills/ywc-codex-toolkit-eval/scripts/ablation.py` — paired trial aggregation
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_results.py` — lifecycle/retention tests
- `docs/skill-agent-eval/codex/runs/.gitignore` — generated artifact exclusion

## Notes

- Successful workspaces are deleted immediately. Failed workspaces are retained only with `--retain-failed-artifacts`, capped at 10 MB per run, and pruned after seven days.
- Raw credentials, environment dumps, and unbounded transcripts are never persisted.
- `INCONCLUSIVE` exits zero only for manual ablation and never means retire approval.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `.codex/skills/ywc-codex-toolkit-eval/scripts/test_results.py`

### Interface Contract

- Contract: evaluator run-result and ablation-summary JSON
- Inputs: runner result, redaction policy, trial arm metadata/cost, optional activation signal
- Outputs: bounded result record, summary/report fields, aggregate decision
- Error model: oversized artifact, incomplete cost, mismatched paired metadata, unavailable activation signal
- Impacted tests: results, retention, redaction, ablation aggregation tests

### Critical Surface Review

- Review requirement: manual full implementation review — retention and redaction govern sensitive evaluator artifacts.

### Data Integrity Hardening

- Trigger surface: shared mutable state
- Atomic / locking strategy: per-run directory and atomic write/replace for result summaries
- Transaction boundary: write redacted result then update aggregate summary; incomplete writes do not become baselines
- Idempotency guard: run ID/attempt key uniqueness and repeat-safe pruning
- Required tests: duplicate run ID, interrupted summary write, retention pruning, cost-completeness aggregation

## Parallel Execution Metadata

### Ownership

- `.codex/skills/ywc-codex-toolkit-eval/scripts/results.py`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/ablation.py`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_results.py`
- `docs/skill-agent-eval/codex/runs/.gitignore`

### Shared Surfaces

- Runner result schema
- `docs/skill-agent-eval/codex/runs/<run-id>/summary.json` format
- Status-specific process exit policy

### Conflicts With

- `000066-010-infra-eval-ci-workflow-docs` — workflow must wait for finalized result/exit contract.

### Parallelizable After

- `000064-020-domain-isolated-runner-adapter`

### Task Verify

- `python3 -m unittest discover -s .codex/skills/ywc-codex-toolkit-eval/scripts -p 'test_results.py'`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/results.py --self-test`

## Out of Scope

- Executing live evaluations, baseline rewriting, automatic retirement, or workflow-level artifact upload configuration.
