# 000014-020-docs-code-gen-red-gate-deep-module — 구현 체크리스트

## Prerequisites
- [ ] `000014-010-docs-shared-tdd-boundary-contract` 완료 및 reference 존재 확인
- [ ] `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md`의 FR-2, FR-5, AC2/AC3/AC4/AC6 확인
- [ ] `ywc-skill-author` 규칙 확인(구조 편집 경유)

## Allowed Edit Scope
- `claude-code/skills/ywc-code-gen/SKILL.md`
- `claude-code/skills/ywc-code-gen/prompts/implementer-base.md`
- `claude-code/skills/ywc-code-gen/references/backend-agent.md`
- `claude-code/skills/ywc-code-gen/references/frontend-agent.md`
- `claude-code/skills/ywc-code-gen/references/qa-agent.md`
- `claude-code/skills/ywc-code-gen/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` / `README.es.md` / `README.zh.md`

## Stop Conditions
- `--tdd`를 default-on으로 바꾸거나 삭제해야 할 것 같으면 중단(spec에서 명시적으로 배제)
- executor skill, `codex/skills/**`, `plugins/**` 수정 필요성이 보이면 중단
- 구조 변경이 `ywc-skill-author` 규칙과 충돌하면 중단

## Implementation Steps
- [ ] `SKILL.md` Phase 1 재구성: QA subagent가 AC 기반 테스트를 먼저 작성 → orchestrator가 RED(미구현으로 인한 실패) 확인 → Backend/Frontend 병렬 구현 → Step 7에서 GREEN 확인
- [ ] pure config/scaffold lane fallback 명시: 의미있는 테스트 불가 시 예외 기록 후 진행, 빈 테스트 날조 금지
- [ ] `SKILL.md`에 "TDD modes" 절 추가: default minimal gate(RED 1회) vs `--tdd` full ritual(`ywc-tdd-ritual`); `--tdd`는 기본 게이트를 대체(중복 아님)
- [ ] `SKILL.md:30` "Gray Box" 라벨 → "Deep Module"로 교정, 내용 유지, 공유 reference §Deep Module 링크
- [ ] `SKILL.md:31` headlights row를 새 기본 RED 게이트 기준으로 갱신(--tdd 외 기본 경로도 포함)
- [ ] Confidence Gate: critical-path 매칭 시 내부 리뷰 필수 + Next Steps에 `/ywc-security-audit` REQUIRED + report에 critical 파일 표기
- [ ] output report에 `TDD mode`, `Tests RED→GREEN`, `Critical modules` 필드 추가
- [ ] `prompts/implementer-base.md`: Backend/Frontend는 사전 RED 테스트 대상 구현, 테스트 약화/삭제 금지; QA는 AC 기반 테스트를 RED로 확인 후 반환
- [ ] role refs(`backend/frontend/qa-agent.md`)에 interface-first + RED-first 기대치 경미 추가
- [ ] README 6종에 RED 기본 게이트, `--tdd` trade-off, deep-module, critical 자동 에스컬레이션을 간결히 반영(technical term은 English 유지)
- [ ] 모든 구조 편집을 `ywc-skill-author` 경유로 수행

## Task Verify
- [ ] `rg -n "Deep Module|RED|TDD mode|ywc-security-audit|tdd-deep-module-gray-box" claude-code/skills/ywc-code-gen/SKILL.md`
- [ ] `rg -n "RED|security-audit|deep module|--tdd" claude-code/skills/ywc-code-gen/prompts/implementer-base.md`

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `README*.md` markdownlint 통과
- [ ] `git diff --name-only`에 `codex/` 및 `plugins/` 경로가 없음
