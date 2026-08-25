# 000014-030-docs-sequential-executor-test-first — 구현 체크리스트

## Prerequisites
- [ ] `000014-010-docs-shared-tdd-boundary-contract` 완료 및 reference 존재 확인
- [ ] `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md`의 FR-3, FR-5, AC4/AC5 확인
- [ ] `ywc-skill-author` 규칙 확인(구조 편집 경유)

## Allowed Edit Scope
- `claude-code/skills/ywc-sequential-executor/SKILL.md`
- `claude-code/skills/ywc-sequential-executor/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` / `README.es.md` / `README.zh.md`

## Stop Conditions
- branch/PR/CI/merge lifecycle 자체를 재설계해야 할 것 같으면 중단
- code-gen/parallel-executor, `codex/skills/**`, `plugins/**` 수정 필요성이 보이면 중단
- 구조 변경이 `ywc-skill-author` 규칙과 충돌하면 중단

## Implementation Steps
- [ ] Rationalization Defense에 도메인 특화 rows ≥3 추가:
  - [ ] "테스트는 구현 후 추가" → behavior change는 failing test(또는 bugfix 실패 regression test) 먼저 — headlights 추월 시 런타임 크래시
  - [ ] "이 task는 internal만 변경" → public contract 변경 시 interface 먼저 작성·보고(deep module)
  - [ ] "구현 전체를 리뷰함" → 일반은 contract 중심 gray-box; critical path는 internal review + `ywc-security-audit`
- [ ] Step 3.4 "TDD is preferred"를 강화: bugfix는 fix 전 실패 regression test; new behavior는 구현 전 failing unit/integration test; docs/config/mechanical은 예외(사유 기록); 실패 테스트 선실행 불가 시 사유 기록 + `DONE_WITH_CONCERNS`; headlights + trade-off framing은 공유 reference 링크
- [ ] interface-first subsection 추가: 변경되는 exported function/endpoint/event/DTO/schema contract/props/CLI flag는 body 전에 명문화; cohesive behavior를 shallow wrapper로 쪼개지 않기
- [ ] Step 4.5/Step 5 critical 자동 에스컬레이션: task가 critical path를 건드리면 `--review` 미지정이어도 `/ywc-impl-review` 강제 + Step 5 delivery 전 `/ywc-security-audit` 라우팅; 일반 task는 변경 없음
- [ ] Completion Report에 changed contracts / 처음 실패한 tests / critical-module review 노트 필드 추가
- [ ] README 6종에 test-first 강화, deep-module, critical 자동 에스컬레이션 간결 반영(technical term English 유지)
- [ ] 모든 구조 편집을 `ywc-skill-author` 경유

## Task Verify
- [ ] `rg -n "headlights|regression test|interface-first|ywc-security-audit|critical path" claude-code/skills/ywc-sequential-executor/SKILL.md`

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `README*.md` markdownlint 통과
- [ ] `git diff --name-only`에 `codex/` 및 `plugins/` 경로가 없음
