# 000018-020-docs-planning-discipline — Implementation Checklist

## Prerequisites

- [ ] `000018-010-docs-principles-foundation` 완료(merged)

## Allowed Edit Scope

- [ ] `ywc-spec-validate/`, `ywc-plan/`, `ywc-spec-writer/` 내부만 편집(SKILL.md + README locale set)
- [ ] Ownership 밖 편집 필요 시 중단·보고

## Stop Conditions

- [ ] spec-validate 4-subagent fan-out 구조를 바꿔야 하면 중단(차원에 접어야 함)
- [ ] default-Medium(규모) 규칙을 건드려야 하면 중단

## Implementation Steps

- [ ] **FR-2 spec-validate Simplicity 차원**
  - Review Focus 표에 "Simplicity — 명시 scope가 필요로 하지 않는 추상화/구성가능성/일반성을 규정하는가? speculative scope를 Warning으로" 1줄
  - Rationalization 행 1줄(모범사례라 복잡해도 OK → 과설계는 Warning)
- [ ] **FR-3 ywc-plan 복수 해석**
  - Rationalization 행(두 해석이 scope/data model을 바꾸면 둘 제시; default-Medium은 규모 전용)
  - Step 1에 "anchor 답변이 서로/코드 증거와 모순되면 STOP·명시·질문" 1줄
- [ ] **FR-3 ywc-spec-writer Open Questions**
  - non-negotiable rules(:146)에 "출처가 두 해석 허용 시 Open Questions에 둘 다 기록, 조용히 결정 금지" 1줄
- [ ] **README 동기화(§A7)** — 3개 skill의 README.md/ko/en/ja에 해당 동작 변경 반영

## Task Verify

- [ ] `rg -n "Simplicity" claude-code/skills/ywc-spec-validate/SKILL.md`
- [ ] `rg -n "interpretation|두 해석|복수 해석" claude-code/skills/ywc-plan/SKILL.md`
- [ ] `rg -n "Open Questions" claude-code/skills/ywc-spec-writer/SKILL.md`
- [ ] 3개 skill의 README 4종이 새 동작을 반영

## Verification

- [ ] `bash scripts/validate.sh` exit 0 (README locale set 완비 확인)
- [ ] markdownlint 통과(변경 README)
- [ ] (typecheck/build 해당 없음)
