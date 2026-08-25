# 000067-010-infra-fixture-v2-schema-verifier-registry — Implementation Checklist

## Prerequisites

- [ ] `docs/ywc-plans/claude-skill-eval-runner.md` 의 `## Iteration 4 Amendments` 를 읽었다 (최종 권위 섹션)
- [ ] 기존 `evals.json` 3종 스키마(`output-contract` / behavioral-style / 기타)를 확인했다

## Allowed Edit Scope

`.claude/skills/ywc-toolkit-eval/scripts/` 의 신규 3파일과 `evals/fixtures/**` 만. `score.py` 와 기존 fixture 는 건드리지 않는다.

## Stop Conditions

- v1 fixture 가 하나라도 검증에 실패하면 중단하고 보고 — 호환성 파기는 이 task 의 범위가 아니다
- 외부 라이브러리가 필요하다고 판단되면 중단 — stdlib 제약은 협상 대상이 아니다

## Hardening Gate

- [ ] 실패하는 테스트를 먼저 쓴다 (RED) — 특히 경로 traversal 거부
- [ ] verifier 는 registry 항목만 실행하며 fixture 문자열이 argv 에 직접 들어가지 않음을 테스트로 증명

## Implementation Steps

- [ ] `scripts/fixture_schema.py` 에 `validate_case(case) -> list[str]` 작성 — 필수 필드, `category` 도메인, `expected_checks` 화이트리스트 검사
- [ ] 동일 파일에 `normalize_manifest(case, fixture_root) -> dict` 작성 — `fixture_files`/`output_paths` 를 realpath 로 해석하고 `fixture_root` 밖이면 거부
- [ ] `scripts/verifier_registry.py` 에 `REGISTRY: dict[str, dict]` 선언 — 각 항목은 `argv`, `cwd`, `timeout`, `env_allowlist`, `expected_exit`
- [ ] 동일 파일에 `resolve(verifier_id) -> dict` 작성 — 미등록 id 는 예외
- [ ] `scripts/test_fixture_schema.py` 작성: valid v2, 미지원 category, v1 호환 통과, `..` 상향 거부, symlink escape 거부, 자유형 command 거부
- [ ] `evals/fixtures/` 에 대표 v2 fixture 2건 배치 (happy_path 1, negative 1)

## Task Verify

- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py` 통과
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py` 회귀 없음

## Verification

- [ ] `bash scripts/validate.sh` exit 0
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exit 0 이고 `history.mechanical.json` 에 git diff 없음
