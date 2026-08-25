# 000014-020-docs-code-gen-red-gate-deep-module

## Purpose

`ywc-code-gen` (Claude Code)에 함정 3/4/5 처방을 반영한다: 기본 경로에 최소 RED 선후 게이트(QA가 실패 테스트를 먼저 성립 → Backend/Frontend 구현), `--tdd`는 opt-in 유지하되 trade-off 명문화, `SKILL.md:30`의 "Gray Box" 라벨을 "Deep Module"로 교정, critical-path 감지 시 Confidence Gate 내부 리뷰 강화 + `ywc-security-audit` REQUIRED routing (FR-2, FR-5(code-gen), AC2, AC3, AC4, AC6).

## Scope

- `SKILL.md` 본문 편집(Phase 1 RED-first 게이트, TDD modes 절, 라벨 교정, Confidence Gate critical 강화, output report 필드)
- `prompts/implementer-base.md` 편집(worker가 사전 작성된 RED 테스트 대상 구현, 테스트 약화/삭제 금지)
- role references 경미 편집(`backend-agent.md`, `frontend-agent.md`, `qa-agent.md`)
- README locale set 갱신(md/en/ja/ko/es/zh)
- 모든 구조 편집은 `ywc-skill-author` 경유

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md` — FR-2, FR-5, AC2, AC3, AC4, AC6
- `claude-code/skills/references/tdd-deep-module-gray-box.md` — 000014-010 산출물

### Summary
기본값을 바꾸지 않고(`--tdd`는 opt-in 유지) 기본 경로에 한 번의 RED-before-implement 게이트만 추가한다. `--tdd`는 strict full RED→GREEN→REFACTOR(`ywc-tdd-ritual`)로 의미를 좁혀 trade-off를 명문화한다. critical module은 gray-box 불충분 → 내부 리뷰 + `ywc-security-audit` 라우팅을 Next Steps에 REQUIRED로 표기한다.

### Out of Scope (from spec)
- `--tdd`를 default-on으로 전환하지 않는다(명시적 결정).
- executor 2종(seq/parallel) 편집은 후속 task 소관.
- `codex/skills/**`, `plugins/**` 미수정.

## Dependencies

### Depends On
- `000014-010-docs-shared-tdd-boundary-contract` — 공유 reference 링크 대상

### Depended By
- `000015-010-infra-claude-executor-contract-validation` — validation/boundary 검증

## Key Files
- `claude-code/skills/ywc-code-gen/SKILL.md`
- `claude-code/skills/ywc-code-gen/prompts/implementer-base.md`
- `claude-code/skills/ywc-code-gen/references/backend-agent.md`
- `claude-code/skills/ywc-code-gen/references/frontend-agent.md`
- `claude-code/skills/ywc-code-gen/references/qa-agent.md`
- `claude-code/skills/ywc-code-gen/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` / `README.es.md` / `README.zh.md`

## Notes
- claude-code `ywc-code-gen`에는 `evals/` 디렉터리와 `agents/openai.yaml`이 없다(codex 전용). codex task와 달리 evals 갱신 단계 없음.
- RED 게이트는 Verification Gate가 이미 테스트를 실행하므로 표현상 자연스럽다. pure config/scaffold lane은 예외 기록 후 진행(빈 테스트 날조 금지 — Banned Output Patterns 유지).
- spec-validate Warning: `--tdd`는 기본 게이트를 대체(중복 실행 아님)함을 한 줄로 명시.

## Out of Scope
- executor skill 편집, codex/plugins 편집, default 플래그 전환.

## Parallel Execution Metadata
- **Ownership:** `claude-code/skills/ywc-code-gen/**`
- **Shared Surfaces:** 공유 reference(read-only link); subagent worker prompt contract; README localization
- **Conflicts With:** (None identified) — 030/040과 disjoint 디렉터리
- **Parallelizable After:** `000014-010`
- **Task Verify:**
  - `rg -n "Deep Module|RED|TDD mode|ywc-security-audit|tdd-deep-module-gray-box" claude-code/skills/ywc-code-gen/SKILL.md`
  - `! rg -n "Gray Box: design the public interface" claude-code/skills/ywc-code-gen/SKILL.md` (라벨 교정 확인)
