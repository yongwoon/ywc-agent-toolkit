# 000019-010-infra-karpathy-validation — Implementation Checklist

## Prerequisites

- [ ] `000018-010` 완료(merged)
- [ ] `000018-020` 완료(merged)
- [ ] `000018-030` 완료(merged)
- [ ] `000018-040` 완료(merged)
- [ ] `000018-050` 완료(merged)

## Allowed Edit Scope

- [ ] 검증 전용 — 소스 편집 없음(구현 노트/검증 로그만)
- [ ] 누락 발견 시 해당 Phase 000018 태스크로 되돌려 수정(이 태스크에서 직접 고치지 않음)

## Stop Conditions

- [ ] Phase 000018 태스크 중 미완료가 있으면 중단
- [ ] rg가 어떤 FR 토큰도 반환하지 못하면 해당 태스크로 회송

## Implementation Steps

- [ ] **확장 rg(§A5)** — 12개 파일에서 토큰 반환 확인(README의 Task Verify 블록 사용)
- [ ] **저장소 검증** — `bash scripts/validate.sh`, `install.sh --list --cc`, `install.sh --list --cc-agents` 모두 exit 0
- [ ] **범위 경계(AC15)** — `git diff --name-only`가 codex/·제품 코드·무관 locale 미포함
- [ ] **AC2** — 새 karpathy-* skill/agent 부재 확인
- [ ] **AC12** — impl-review 5-aspect + Step 3 주입 블록 온전(§A4 rg)
- [ ] **AC13** — §A7 README-sync 필요 목록의 skill만 README 4종 동기화, 불필요 목록은 미변경
- [ ] **AC16** — task-generator eval 케이스 또는 불가 사유 존재

## Task Verify

- [ ] 위 모든 명령 exit 0 / 기대 출력 확인
- [ ] 검증 결과를 구현 노트에 기록

## Verification

- [ ] `bash scripts/validate.sh` exit 0
- [ ] `bash scripts/install.sh --list --cc` exit 0
- [ ] `bash scripts/install.sh --list --cc-agents` exit 0
- [ ] markdownlint 통과(전체 변경 README)
