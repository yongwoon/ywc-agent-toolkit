# 000018-050-docs-execution-discipline — Implementation Checklist

## Prerequisites

- [ ] `000018-010-docs-principles-foundation` 완료(merged)

## Allowed Edit Scope

- [ ] `ywc-parallel-executor/**`, `ywc-sequential-executor/**`, `ywc-debug-rootcause/**`, `ywc-root-cause-analyst.md`만 편집
- [ ] Ownership 밖 편집 필요 시 중단·보고

## Stop Conditions

- [ ] sequential :265/:315 절을 재작성해야 하면 중단(게이트만 추가)
- [ ] agent model/tool/출력 상태를 바꿔야 하면 중단
- [ ] worktree에서 전체 스위트가 비현실적이면 영향범위 한정 + 근거 문서화(생략 금지)

## Implementation Steps

- [ ] **FR-6 parallel 회귀 레이어** — Step 4c(:272)에 "Task Verify 통과 후 4e 이전 전체/영향범위 스위트 실행(공유 상태/타입/스키마 회귀)" 추가; 영향범위 한정 시 근거 문서화
- [ ] **FR-8 Ownership 게이트** — sequential(Completeness Gate :290 인근) + parallel(4c 인근)에 첫 커밋/델리버리 전 `git diff --name-only`로 선언 Ownership 밖 파일 열거·플래그; 범위 외 시 BLOCKED 또는 명시 정당화
- [ ] **FR-9 debug-rootcause RED 순서** — Phase 3 §2에 "버그가 자동화 가능하면 Phase 4 §1 실패 테스트가 이 변경 이전 RED" 1절
- [ ] **FR-10 analyst 재현 요구** — NEEDS_CONTEXT 트리거(:131)에 "재현(실패 테스트/결정적 repro/캡처 출력) 부재 시 필요 누락 컨텍스트로 명시"
- [ ] **(§A2 대칭)** sequential evals가 게이트를 객관 검증 어려우면 'no objective eval — 사유' 노트
- [ ] **README 동기화(§A7)** — parallel-executor README.md/ko/en/ja만

## Task Verify

- [ ] `rg -n "전체|full suite|회귀|impacted" claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] `rg -n "git diff --name-only" claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-sequential-executor/SKILL.md`
- [ ] `rg -n "RED" claude-code/skills/ywc-debug-rootcause/SKILL.md` (Phase 3 순서)
- [ ] `rg -n "reproduction|재현|repro" claude-code/agents/ywc-root-cause-analyst.md`
- [ ] parallel-executor README 4종 반영

## Verification

- [ ] `bash scripts/validate.sh` exit 0
- [ ] `bash scripts/install.sh --list --cc-agents` exit 0
- [ ] markdownlint 통과
