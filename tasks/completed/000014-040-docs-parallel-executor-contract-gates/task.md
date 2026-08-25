# 000014-040-docs-parallel-executor-contract-gates — 구현 체크리스트

## Prerequisites
- [ ] `000014-010-docs-shared-tdd-boundary-contract` 완료 및 reference 존재 확인
- [ ] `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md`의 FR-4, FR-5, AC4/AC5 확인
- [ ] `ywc-skill-author` 규칙 확인(구조 편집 경유)

## Allowed Edit Scope
- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` / `README.es.md` / `README.zh.md`

## Stop Conditions
- wave/worktree/Docker/merge lifecycle 자체를 재설계해야 할 것 같으면 중단
- code-gen/sequential-executor, `codex/skills/**`, `plugins/**` 수정 필요성이 보이면 중단
- 구조 변경이 `ywc-skill-author` 규칙과 충돌하면 중단

## Implementation Steps
- [ ] Rationalization Defense에 rows 추가:
  - [ ] TDD/headlights — 테스트가 구현을 게이트; "wave 전체 구현 후 wave 끝에서 검증"은 headlights 안티패턴
  - [ ] deep-module — 공유 public surface는 worker dispatch 전 contract 정의
- [ ] Step 4b worker payload에 directive 2개 추가(기존 verbatim directive 형식 준수):
  - [ ] interface-first directive — body 전에 public surface 설계
  - [ ] test-first-where-feasible directive — behavior-changing task는 구현 전 failing test 작성·확인; docs/config/mechanical은 예외(사유 명시)
- [ ] Step 4d/4e critical 자동 에스컬레이션: task가 critical path를 건드리면 4d `/ywc-impl-review` 강제 + 4e wave delivery 전 `/ywc-security-audit` 라우팅; 일반 task는 gray-box 유지
- [ ] Completion Report에 per-wave changed contracts + critical-module review 노트 필드 추가
- [ ] README 6종에 interface-first, test-first, critical 자동 에스컬레이션 간결 반영(technical term English 유지)
- [ ] 모든 구조 편집을 `ywc-skill-author` 경유

## Task Verify
- [ ] `rg -n "interface-first|test-first|headlights|ywc-security-audit|critical path" claude-code/skills/ywc-parallel-executor/SKILL.md`

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `README*.md` markdownlint 통과
- [ ] `git diff --name-only`에 `codex/` 및 `plugins/` 경로가 없음
