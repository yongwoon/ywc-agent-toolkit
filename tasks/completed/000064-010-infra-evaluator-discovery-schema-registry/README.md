# 000064-010-infra-evaluator-discovery-schema-registry

## Purpose

로컬 `ywc-codex-toolkit-eval`의 평가 대상 발견 규칙과 V2 fixture 계약을 evaluator 소유 코드로 고정한다. 임의 shell command가 fixture에서 실행되지 않도록 verifier registry를 도입하고, SKILL.md 품질 신호는 warning-only로 제공한다.

## Scope

- `codex/skills/<SKILL.md가 있는 디렉터리>`와 `codex/agents/*.toml`만 발견하도록 inventory를 보강한다.
- V1 read-only 호환성과 V2 skill/agent fixture schema, workspace manifest 검증을 구현한다.
- registry-owned verifier의 ID, mode, argv, cwd, timeout, allowlisted environment 계약을 구현한다.
- 500줄 초과, 중복/무의미 지시문 후보, 비명령형 안내문 후보를 warning으로 보고한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-1-amendments` — local evaluator, registry-only verifier, V2 fixture와 migration 정책
- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-2-amendments` — workspace manifest와 verifier mode 계약
- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-3-amendments` — fixture root realpath containment 요구사항

### Summary

이 task는 live runner보다 먼저 평가 대상과 입력 계약을 결정한다. Fixture는 command나 실행 경로를 포함할 수 없고, verifier는 evaluator 코드에서 review된 registry entry만 사용할 수 있다. V1 fixture를 읽는 호환성은 유지하지만 새 fixture와 기존 fixture 수정은 V2로 검증해야 한다.

### Out of Scope (from spec)

- Temporary `CODEX_HOME`와 Codex CLI 실행 — `000064-020-domain-isolated-runner-adapter`
- 결과 artifact lifecycle과 ablation 집계 — `000065-010-domain-results-artifacts-ablation`
- 실제 fixture 작성 — `000065-020-test-v2-fixture-migration`

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000064-020-domain-isolated-runner-adapter` — 검증된 manifest와 verifier registry를 소비한다.
- `000065-010-domain-results-artifacts-ablation` — 결과가 참조할 case/schema metadata를 소비한다.
- `000065-020-test-v2-fixture-migration` — V2 fixture shape와 migration report를 사용한다.
- `000066-010-infra-eval-ci-workflow-docs` — CI가 호출할 validator 계약을 사용한다.

## Key Files

- `.codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py` — discovery와 linter evidence
- `.codex/skills/ywc-codex-toolkit-eval/scripts/fixture_validator.py` — V1/V2 schema 및 manifest validator
- `.codex/skills/ywc-codex-toolkit-eval/scripts/verifier_registry.py` — allowlisted verifier 정의
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_*.py` — discovery, validator, registry regression tests

## Notes

- `codex/skills/references`와 `codex/skills/scripts`는 `SKILL.md`가 없으므로 평가 대상이 아니어야 한다.
- Registry entry의 `fixture_workspace`와 `source_checkout_readonly` mode는 명시적으로 분리한다. `bundle.validate`는 후자여야 한다.
- Linter warning은 CI failure로 승격하지 않는다. suppression은 rule ID와 이유를 요구한다.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `.codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py` 및 `test_inventory_gate.py`

### Interface Contract

- Contract: V2 fixture/workspace manifest 및 verifier registry schema
- Inputs: repository-relative fixture path, target/dependency identifiers, verifier IDs
- Outputs: normalized fixture metadata 또는 deterministic validation error
- Error model: unknown verifier, path traversal, free-form command, V1/V2 ambiguity는 validation failure
- Impacted tests: fixture validator와 registry unit tests

### Critical Surface Review

- Review requirement: manual full implementation review — command allowlist와 path containment은 security boundary다.

### Data Integrity Hardening

- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata

### Ownership

- `.codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/fixture_validator.py`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/verifier_registry.py`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_inventory_gate.py`

### Shared Surfaces

- Evaluator fixture JSON schema
- Verifier registry API consumed by runner
- `codex/skills/**` discovery boundary

### Conflicts With

- `000064-020-domain-isolated-runner-adapter` — runner must not independently define manifest or verifier semantics.

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `python3 -m unittest discover -s .codex/skills/ywc-codex-toolkit-eval/scripts -p 'test_*.py'`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json --skip-gate`

## Out of Scope

- Codex CLI invocation, credential handoff, result persistence, CI workflow edits, and distributable `codex/skills/**` content changes.
