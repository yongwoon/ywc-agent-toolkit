# 000069-010-infra-eval-ci-two-tier-docs

## Purpose

평가 체계를 CI **2계층**으로 확정하고, `scripts/validate.sh` 에 claude evaluator 존재 검사를 **신설**하며, 운영 문서를 정리한다.

## Scope

- PR CI: 스키마·lint·mock verifier 만 (**모델 호출 0**)
- `validate.sh` 에 claude evaluator 검사 신설 (§AC20′ — 확장이 아니라 신설)
- live 평가와 ablation 은 **local manual** 로 문서화
- 운영 절차 문서 정리

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-skill-eval-runner.md` — §Phase 5″ (CI 2계층), §AC20′ (validate.sh 신설), AC14 (계층 분리)
- `scripts/validate.sh:598` — 기존 블록이 Codex 전용임을 확인한 지점

### Summary

**live 평가를 CI 에서 돌릴 수 없다.** 구독 인증은 개발자 머신 세션에 있고 GitHub Actions 러너에 없으며, API key 는 프로젝트 방침상 배제되었다. 따라서 원본이 전제한 3계층(PR fast / scheduled live / manual expensive)이 2계층으로 줄어든다. 평가는 릴리스 주기마다 사람이 로컬에서 돌리는 활동이 된다.

### Out of Scope (from spec)

- scheduled live CI job — 구조적으로 불가
- `.github/workflows/` 에 live 평가 job 추가

## Criticality

`normal` — CI 에 자격증명을 추가하지 않는다(추가할 것이 없다). 보안 민감 표면 없음.

## Dependencies

### Depends On

- `000068-010-domain-s3-reliability-wiring` — 밴드표·표기 규약이 문서 대상
- `000068-020-domain-ablation-paired-trials` — ablation 절차가 문서 대상

### Depended By

- (없음) — 배치의 종단

## Key Files

- `scripts/validate.sh` (claude evaluator 검사 신설)
- `.github/workflows/validate.yml` (mock verifier job 추가)
- `.claude/skills/ywc-toolkit-eval/README.md` (운영 절차)

## Notes

- **`validate.sh` 에는 claude evaluator 검사가 존재하지 않는다.** `:598` 블록은 `local skill_dir=".codex/skills/ywc-codex-toolkit-eval"` 로 Codex 전용이며, `grep "\.claude/skills/ywc-toolkit-eval" scripts/validate.sh` 는 결과가 없다. 지금은 claude `score.py` 를 지워도 `validate.sh` 가 통과한다.
- Codex 블록과 **대칭 구조**로 작성하되 `inventory_gate.py` 처럼 claude 측에 없는 파일을 요구하지 않는다.

## Hardening Evidence

### Test Feedback Path

- RED-first target: 수동 — claude `score.py` 를 임시 삭제하고 `validate.sh` 가 실패하는지 확인

### Interface Contract

- Contract: 저장소 검증 게이트
- Inputs: 저장소 트리
- Outputs: exit 0 / non-zero
- Error model: evaluator 필수 파일 부재
- Impacted tests: 파일 삭제 시 실패, 정상 시 통과

### Critical Surface Review

- Review requirement: 표준 리뷰. CI 에 시크릿을 추가하지 않음을 확인한다.

### Data Integrity Hardening

- Trigger surface: 해당 없음 (검증 전용, 상태 변경 없음)
- Atomic / locking strategy: 해당 없음
- Transaction boundary: 해당 없음
- Idempotency guard: 검증은 순수 — 반복 실행이 상태를 바꾸지 않는다
- Required tests: 반복 실행 시 동일 결과

## Parallel Execution Metadata

### Ownership

- `scripts/validate.sh` (claude evaluator 검사 블록만)
- `.github/workflows/validate.yml` (신규 job 만)
- `.claude/skills/ywc-toolkit-eval/README.md`

### Shared Surfaces

- `scripts/validate.sh` — 저장소 전역 게이트, Codex 블록과 공존
- `.github/workflows/validate.yml` — 저장소 전역 CI

### Conflicts With

- `000068-010-domain-s3-reliability-wiring` — `SKILL.md`/`references/` 문서를 함께 건드릴 수 있어 병렬 실행하지 않는다

### Parallelizable After

- `000068-010-domain-s3-reliability-wiring`
- `000068-020-domain-ablation-paired-trials`

### Task Verify

- `bash scripts/validate.sh` exit 0
- claude `score.py` 임시 삭제 후 `bash scripts/validate.sh` exit != 0

## Out of Scope

- live 평가 CI job, 시크릿 구성, 아티팩트 업로드 파이프라인
