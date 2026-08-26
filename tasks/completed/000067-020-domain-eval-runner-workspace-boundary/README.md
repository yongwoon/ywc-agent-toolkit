# 000067-020-domain-eval-runner-workspace-boundary

## Purpose

skill 을 실제 실행하고 산출물을 결정적으로 채점하는 runner 를 만든다. **catalog 격리는 하지 않되(노선 N1), workspace 격리는 필수**다.

## Scope

- case 마다 새 임시 workspace 생성·회수
- 실행 전후 workspace 스냅샷 비교 — 미선언 변경은 `FAIL`
- 상태 enum `PASS` | `FAIL` | `SKIPPED_UNAVAILABLE` | `ERROR` | `INCONCLUSIVE`
- 결과 레코드 리댁션·보존 정책 (gitignore 루트, 10MB 상한, 7일 정리)
- 결정적 check 우선 실행, 미해결 항목만 judge 로

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-skill-eval-runner.md` — `## Iteration 4 Amendments` (최종 권위), 특히 "격리의 두 층위"
- 같은 문서 AC5 (경계 봉쇄), AC6 (상태 enum), AC13/§AC13′ (아티팩트 위생), §Phase 2 확정 사항
- `docs/skill-agent-eval/claude/spike-2026-07-22.md` — 발동 방식과 판정 근거의 실측 출처

### Summary

발동은 `claude -p "/<skill> <prompt>" --output-format json` 이다. json 페이로드에 활성화 신호 필드가 **없음이 실측 확인**되었으므로 판정은 `result` 에 대한 outcome 검사 단독이며 `activation_observability: unavailable` 로 기록한다. catalog 격리는 노선 N1 에서 포기했으나 **workspace 격리는 인증과 무관하며 반드시 유지**한다 — `ywc-commit` 같은 commit·push 하는 skill 이 평가 대상이기 때문이다.

### Out of Scope (from spec)

- catalog 격리 (`CLAUDE_CONFIG_DIR` 임시화 / `--bare`) — 노선 N1 에서 배제
- S3 배선 (`000068-010`), ablation (`000068-020`)

## Criticality

`critical` — spec `## Critical Surfaces` 가 "격리 workspace" 를 지목한다. 격리 실패 시 평가가 개발자의 실제 저장소를 오염시킨다.

## Dependencies

### Depends On

- `000067-010-infra-fixture-v2-schema-verifier-registry` — manifest 정규화와 verifier 조회를 제공

### Depended By

- `000068-010-domain-s3-reliability-wiring` — 실행 결과를 S3 로 환산
- `000068-020-domain-ablation-paired-trials` — with/without 실행 기반
- `000069-010-infra-eval-ci-two-tier-docs` — mock 모드 테스트를 CI 에 연결

## Key Files

- `.claude/skills/ywc-toolkit-eval/scripts/runner.py` (신규)
- `.claude/skills/ywc-toolkit-eval/scripts/claude_adapter.py` (신규)
- `.claude/skills/ywc-toolkit-eval/scripts/test_runner.py` (신규)
- `.gitignore` (아티팩트 루트 규칙 1줄)

## Notes

- 자격증명 취급은 **더 이상 critical surface 가 아니다** — N1 은 개발자의 기존 구독 세션을 그대로 쓰므로 임시 자격증명도 CI secret 도 없다.
- adapter 는 `subprocess` + `json` 만 사용 (stdlib).
- `--disable-slash-commands` 는 ablation without-arm 전용이며 이 task 의 with-arm 경로에서는 쓰지 않는다.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `.claude/skills/ywc-toolkit-eval/scripts/test_runner.py`

### Interface Contract

- Contract: case 실행 요청 → 상태 있는 결과 레코드
- Inputs: 정규화된 v2 manifest, verifier registry, adapter 설정
- Outputs: 상태 enum 하나 + 리댁션된 run metadata (run id, case id, attempt, duration, artifact path, `activation_observability`)
- Error model: adapter 부재/타임아웃, 미선언 output 쓰기, verifier 실패, 파싱 실패
- Impacted tests: fake adapter, 미선언 쓰기 거부, symlink escape, 타임아웃 정리

### Critical Surface Review

- Review requirement: 수동 전량 리뷰 — 임시 workspace 생성·회수, subprocess 호출, 스냅샷 비교를 다룬다.

### Data Integrity Hardening

- Trigger surface: 파일을 쓰는 skill 의 실행
- Atomic / locking strategy: run id 별 고유 임시 디렉터리, 공유 쓰기 상태 없음
- Transaction boundary: create → run → snapshot → cleanup. 실패한 workspace 는 재사용하지 않는다
- Idempotency guard: 시도마다 새 run id 와 새 workspace
- Required tests: 연속 2회 실행 격리, 타임아웃 후 정리, 동시 실행 시 run id 충돌 없음 (AC19)

## Parallel Execution Metadata

### Ownership

- `.claude/skills/ywc-toolkit-eval/scripts/runner.py`
- `.claude/skills/ywc-toolkit-eval/scripts/claude_adapter.py`
- `.claude/skills/ywc-toolkit-eval/scripts/test_runner.py`
- `.gitignore` (해당 1줄만)

### Shared Surfaces

- v2 manifest / verifier registry (`000067-010` 소유 — 재정의 금지)
- run 결과 스키마 — `000068-010`·`000068-020`·`000069-010` 이 소비
- `.gitignore` — 저장소 전역 파일

### Conflicts With

- `000067-010-infra-fixture-v2-schema-verifier-registry` — 먼저 머지되어야 하며 그 스키마를 재정의하지 않는다

### Parallelizable After

- `000067-010-infra-fixture-v2-schema-verifier-registry`

### Task Verify

- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_runner.py`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/runner.py --adapter fake --case <fixture-id>`

## Out of Scope

- 실제 `claude` 호출을 CI 에서 수행하는 것 (구독 인증이 CI 에 없다)
- S3 밴드 산출, ablation 집계, 은퇴 판정
