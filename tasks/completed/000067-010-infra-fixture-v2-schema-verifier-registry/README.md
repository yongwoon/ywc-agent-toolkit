# 000067-010-infra-fixture-v2-schema-verifier-registry

## Purpose

평가 fixture 의 v2 스키마 검증기와 evaluator 소유 verifier registry 를 도입한다. 이후 모든 task 가 이 두 계약 위에서 동작한다.

## Scope

- v2 case shape 검증기 (stdlib only, `score.py` 무의존 관례 준수)
- verifier registry — `argv`, cwd, timeout, 허용 env, 기대 exit code 를 evaluator 가 소유
- workspace manifest 정의 (`fixture_root`, `fixture_files`, `output_paths`, `target_skill`, `verifier_ids`)
- v1 fixture 는 읽기 전용 호환으로 통과

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-skill-eval-runner.md` — `## Iteration 4 Amendments` 가 최종 권위
- 같은 문서 AC3 (v2 필수 필드), AC4 (check type 화이트리스트), AC5 (경계 봉쇄)

### Summary

fixture 는 `schema: 2` 와 `id`/`prompt`/`language`/`category`/`should_trigger`/`expected_checks` 를 갖는다. `category` 는 `happy_path` | `negative` | `boundary` 중 정확히 하나다. `expected_checks` 는 화이트리스트된 check type 만 허용하며 **fixture 가 임의 shell 명령이나 실행 파일 경로를 지정할 수 없다** — 이것이 평가를 임의 코드 실행 경로로 만들지 않는 유일한 방어선이다.

### Out of Scope (from spec)

- runner 구현 (`000067-020`)
- 전 항목 fixture 작성 — 대표 소수만 migrate

## Criticality

`critical` — spec `## Critical Surfaces` 가 "verifier 실행" 을 명시적으로 지목한다. fixture 가 임의 shell 을 지정할 수 있으면 평가가 곧 임의 코드 실행이 된다.

## Dependencies

### Depends On

- (없음) — 이 배치의 루트

### Depended By

- `000067-020-domain-eval-runner-workspace-boundary` — manifest 와 registry 계약을 소비한다
- `000068-020-domain-ablation-paired-trials` — v2 fixture 를 입력으로 쓴다

## Key Files

- `.claude/skills/ywc-toolkit-eval/scripts/fixture_schema.py` (신규)
- `.claude/skills/ywc-toolkit-eval/scripts/verifier_registry.py` (신규)
- `.claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py` (신규)
- `.claude/skills/ywc-toolkit-eval/evals/fixtures/**` (신규)

## Notes

- `score.py` 는 stdlib 전용이다. 신규 모듈도 외부 의존을 도입하지 않는다 (신규 library task 가 불필요한 이유).
- v1 호환을 깨지 않는다 — 기존 `evals.json` 들이 그대로 통과해야 한다.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `.claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py`

### Interface Contract

- Contract: v2 fixture 검증 + verifier 조회
- Inputs: fixture JSON, registry 정의
- Outputs: 정규화된 manifest 또는 구조화된 검증 오류
- Error model: 미지원 category, v1/v2 혼동, 경로 traversal, 자유형 command 지정, 미등록 verifier id
- Impacted tests: valid/invalid fixture, symlink escape, shell 유사 값 거부

### Critical Surface Review

- Review requirement: 수동 전량 리뷰 — verifier argv 구성과 fixture→실행 경계를 다룬다.

### Data Integrity Hardening

- Trigger surface: fixture 로부터의 경로 해석
- Atomic / locking strategy: 해당 없음 (읽기 전용 검증)
- Transaction boundary: 해당 없음
- Idempotency guard: 검증은 순수 함수 — 동일 입력에 동일 출력
- Required tests: `fixture_root` realpath 봉쇄, `..` 상향 거부, symlink escape 거부

## Parallel Execution Metadata

### Ownership

- `.claude/skills/ywc-toolkit-eval/scripts/fixture_schema.py`
- `.claude/skills/ywc-toolkit-eval/scripts/verifier_registry.py`
- `.claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py`
- `.claude/skills/ywc-toolkit-eval/evals/fixtures/**`

### Shared Surfaces

- v2 fixture 스키마 — 이후 모든 task 가 소비
- verifier registry 계약

### Conflicts With

- (None identified)

### Parallelizable After

- (없음) — 배치의 시작점

### Task Verify

- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py`

## Out of Scope

- runner, S3 배선, ablation, CI 변경
