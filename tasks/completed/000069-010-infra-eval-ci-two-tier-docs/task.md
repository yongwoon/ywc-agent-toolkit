# 000069-010-infra-eval-ci-two-tier-docs — Implementation Checklist

## Prerequisites

- [ ] `000068-010`, `000068-020` 머지 완료 — 문서화할 대상이 존재한다
- [ ] `scripts/validate.sh:598` 이 Codex 전용임을 직접 확인했다

## Allowed Edit Scope

`scripts/validate.sh` 의 **신규 블록만**(Codex 블록 수정 금지), `.github/workflows/validate.yml` 의 신규 job, evaluator `README.md`.

## Stop Conditions

- CI 에 모델 호출이나 Anthropic 자격증명을 추가해야 한다고 판단되면 **중단하고 보고** — 방침 위반이며 §Phase 5″ 가 금지한다
- Codex 블록을 수정해야 한다고 판단되면 중단 — 별도 소유다

## Hardening Gate

- [ ] 신규 job 이 **모델을 호출하지 않음**을 확인 (mock verifier / 스키마 검증만)
- [ ] claude `score.py` 임시 삭제 → `validate.sh` 실패 → 원복 순으로 실제 확인

## Implementation Steps

- [ ] `scripts/validate.sh` 에 claude evaluator 검사 블록 **신설** — `local skill_dir=".claude/skills/ywc-toolkit-eval"` 로 시작, `scripts/score.py`·`scripts/test_score.py`·`scripts/runner.py`·`scripts/test_runner.py`·`scripts/fixture_schema.py` 존재 확인
- [ ] 같은 블록에서 `inventory_gate.py` 를 요구하지 않는다 (claude 측에 없는 파일)
- [ ] `.github/workflows/validate.yml` 에 `skill-eval-schema` job 추가 — v2 fixture 검증 + mock verifier 테스트만 실행, **모델 호출 없음**
- [ ] `.claude/skills/ywc-toolkit-eval/README.md` 에 운영 절차 기술: PR CI 가 무엇을 보장하는가, live 평가는 왜 로컬 수동인가, ablation 실행 방법과 예상 비용
- [ ] 같은 문서에 **CI 에서 live 평가를 하지 않는 이유**를 명시 — 구독 인증이 러너에 없고 API key 는 방침상 배제

## Task Verify

- [ ] `bash scripts/validate.sh` exit 0
- [ ] claude `score.py` 를 임시로 옮긴 뒤 `bash scripts/validate.sh` 가 exit != 0 (확인 후 즉시 원복)
- [ ] 신규 CI job 이 `pull_request` 에서 실행되며 모델을 호출하지 않음

## Verification

- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py` 회귀 없음
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exit 0, baseline git diff 없음
