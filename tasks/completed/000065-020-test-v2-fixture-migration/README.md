# 000065-020-test-v2-fixture-migration

## Purpose

현재 coverage가 없는 4개 infra/IAc skill과 representative Codex custom agent에 안전한 V2 fixture를 추가한다. Migration은 실제 host mutation 없이 mocked/dry-run evidence를 사용하며, V1 fixture는 읽기 전용 호환 상태를 유지한다.

## Scope

- `ywc-iac-author`, `ywc-infra-design`, `ywc-infra-optimize`, `ywc-infra-review`에 각 1개 happy-path와 1개 negative/boundary V2 case를 작성한다.
- V2 agent fixture를 기존 evaluator-owned `agent-smoke-fixtures.json`에 한 representative agent 대상으로 추가한다.
- workspace manifest, fixture root, evidence packet, expected/forbidden signal과 fixture-local output path를 schema에 맞춰 작성한다.
- V1/V2 fixture count와 coverage/backlog signal을 검증한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-eval-upgrade.md#revised-acceptance-criteria` — 4개 uncovered skill 및 representative agent migration 요구사항
- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-2-amendments` — workspace manifest와 agent fixture fields
- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-3-amendments` — fixture root/file/output containment

### Summary

각 live-ready V2 case는 explicit schema와 evaluator-validated manifest를 가져야 한다. Docker, infra, external-system 사례는 host mutation 대신 mock 또는 dry-run contract를 검증한다. 기존 V1 fixture는 migration이 끝날 때까지 수정하거나 제거하지 않고 읽기 전용으로 유지한다.

### Out of Scope (from spec)

- V2 schema/validator/registry 구현 — `000064-010-infra-evaluator-discovery-schema-registry`
- Workspace isolation 또는 live adapter 구현 — `000064-020-domain-isolated-runner-adapter`
- 모든 48개 skill의 대량 fixture 작성 — spec out of scope
- Scheduled live execution enablement — `000066-010-infra-eval-ci-workflow-docs`

## Dependencies

### Depends On

- `000064-010-infra-evaluator-discovery-schema-registry` — V2 validator와 registry contract
- `000064-020-domain-isolated-runner-adapter` — validated manifest와 fake adapter execution path

### Depended By

- `000066-010-infra-eval-ci-workflow-docs` — PR mocked checks와 scheduled/manual suite input

## Key Files

- `codex/skills/ywc-iac-author/evals/evals.json`
- `codex/skills/ywc-infra-design/evals/evals.json`
- `codex/skills/ywc-infra-optimize/evals/evals.json`
- `codex/skills/ywc-infra-review/evals/evals.json`
- `.codex/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json`
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/**`

## Notes

- Fixture fields never contain arbitrary shell command text or executable path.
- Fixture files and outputs are relative to `fixture_root`; do not use symlinks that escape it.
- Each skill gets exactly the minimum requested coverage; broader migration is deliberately deferred.

## Hardening Evidence

### Test Feedback Path

- RED-first target: V2 fixture validator tests from `000064-010` plus fake-runner fixture execution from `000064-020`

### Interface Contract

- Contract: V2 skill case and V2 agent smoke fixture
- Inputs: prompt, language, category, trigger expectation, manifest/evidence packet, registry verifier IDs
- Outputs: validator-accepted case and deterministic/fake-runner evidence
- Error model: unsupported category, command field, free-form path, escaped output, unknown verifier/dependency
- Impacted tests: fixture validator and fake-adapter migration tests

### Critical Surface Review

- Review requirement: manual full implementation review — fixtures direct infra/IaC safety behavior and allowed outputs.

### Data Integrity Hardening

- Trigger surface: N/A — fixtures must use mocked/dry-run contracts and perform no host mutation.
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: validator rejection and mock/dry-run evidence

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-iac-author/evals/**`
- `codex/skills/ywc-infra-design/evals/**`
- `codex/skills/ywc-infra-optimize/evals/**`
- `codex/skills/ywc-infra-review/evals/**`
- `.codex/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json`
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/**`

### Shared Surfaces

- V2 fixture/workspace manifest schema
- Verifier registry IDs
- Agent smoke fixture format

### Conflicts With

- `000066-010-infra-eval-ci-workflow-docs` — workflow must not be authored against incomplete fixture inventory.

### Parallelizable After

- `000064-010-infra-evaluator-discovery-schema-registry`
- `000064-020-domain-isolated-runner-adapter`

### Task Verify

- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/fixture_validator.py --repo-root . --report`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py --fixtures .codex/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json --outputs .codex/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output`

## Out of Scope

- Unrelated skill fixture changes, production cloud actions, credential configuration, and legacy fixture removal.
