# 000064-020-domain-isolated-runner-adapter

## Purpose

V2 live case를 fresh temporary workspace와 temporary `CODEX_HOME`에서 안전하게 실행하는 evaluator runner를 만든다. 이는 host filesystem 보안 경계가 아닌 best-effort isolation임을 명시하고, 지원된 Codex CLI adapter의 unavailable/timeout/final-output 동작을 testable contract로 만든다.

## Scope

- workspace manifest에 선언된 fixture root/files, target skill/dependencies, output paths, evidence packet, verifier IDs만 허용한다.
- temporary `CODEX_HOME`에는 선택 skill과 명시된 dependency만 설치하고 persistent user configuration을 복사하지 않는다.
- CLI metadata/final output parsing, timeout/cancel, credential-provider handoff, no-provider `SKIPPED_UNAVAILABLE`를 구현한다.
- workspace snapshot과 realpath 검증으로 undeclared write, delete, symlink redirect를 `FAIL`로 만든다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-1-amendments` — temporary workspace/`CODEX_HOME`, status, artifact preconditions
- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-2-amendments` — credential-provider, workspace manifest, verifier modes
- `docs/ywc-plans/codex-skill-eval-upgrade.md#iteration-3-amendments` — fixture root and snapshot write boundary

### Summary

Runner는 evaluator validator가 확정한 manifest/registry만 소비한다. Persistent `CODEX_HOME` 또는 developer configuration으로 fallback할 수 없고, provider가 없으면 quality pass가 아닌 `SKIPPED_UNAVAILABLE`을 반환한다. Live model API egress는 CI/job policy의 명시적 exception이며 CLI isolation만으로 network boundary를 주장하지 않는다.

### Out of Scope (from spec)

- V2 manifest/registry schema 정의 — `000064-010-infra-evaluator-discovery-schema-registry`
- Artifact redaction, retention, aggregation, ablation policy — `000065-010-domain-results-artifacts-ablation`
- 실제 skill/agent fixture migration — `000065-020-test-v2-fixture-migration`

## Dependencies

### Depends On

- `000064-010-infra-evaluator-discovery-schema-registry` — validated workspace manifest와 verifier registry 계약

### Depended By

- `000065-010-domain-results-artifacts-ablation` — normalized run result와 status를 집계한다.
- `000065-020-test-v2-fixture-migration` — migrated fixture를 fake/live runner로 검증한다.
- `000066-010-infra-eval-ci-workflow-docs` — runner command, exit contract, artifact controls를 호출한다.

## Key Files

- `.codex/skills/ywc-codex-toolkit-eval/scripts/runner.py` — workspace lifecycle와 deterministic execution
- `.codex/skills/ywc-codex-toolkit-eval/scripts/codex_adapter.py` — supported CLI adapter
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py` — fake adapter, isolation, containment tests

## Notes

- 하나의 minimal production adapter만 지원한다. 여러 runtime adapter를 이 task에 추가하지 않는다.
- Verifier 실행은 registry-owned argv만 허용하며 shell interpreter, inherited credentials, network는 default-deny다.
- `source_checkout_readonly` verifier는 allowlisted readonly roots의 before/after snapshot을 비교해야 한다.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `.codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py`

### Interface Contract

- Contract: runner request/result protocol
- Inputs: normalized V2 manifest, evaluator-owned registry, credential provider handoff, adapter configuration
- Outputs: one status (`PASS`, `FAIL`, `SKIPPED_UNAVAILABLE`, `ERROR`, `INCONCLUSIVE`) and redaction-ready run metadata
- Error model: missing dependency, invalid output boundary, unavailable CLI/provider, timeout, parser failure
- Impacted tests: fake adapter, no-provider, output snapshot, readonly verifier tests

### Critical Surface Review

- Review requirement: manual full implementation review — temporary credentials, filesystem containment, subprocess invocation을 다룬다.

### Data Integrity Hardening

- Trigger surface: retryable command/API
- Atomic / locking strategy: per-run unique temporary directory; no shared writable state
- Transaction boundary: create/run/snapshot/cleanup lifecycle; failure does not reuse a workspace
- Idempotency guard: unique run ID and fresh workspace per attempt
- Required tests: consecutive-run isolation, timeout cleanup, duplicate attempt workspace separation

## Parallel Execution Metadata

### Ownership

- `.codex/skills/ywc-codex-toolkit-eval/scripts/runner.py`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/codex_adapter.py`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py`
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/runner/**`

### Shared Surfaces

- V2 workspace manifest and verifier registry
- Run result schema consumed by aggregation and CI
- `CODEX_HOME` credential isolation policy

### Conflicts With

- `000064-010-infra-evaluator-discovery-schema-registry` — must merge first; do not redefine its schema or registry.

### Parallelizable After

- `000064-010-infra-evaluator-discovery-schema-registry`

### Task Verify

- `python3 -m unittest .codex.skills.ywc-codex-toolkit-eval.scripts.test_runner`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --fixture <runner-fixture>`

## Out of Scope

- Production credential provisioning, workflow secrets configuration, broad network sandboxing, and result retention/report publication.
