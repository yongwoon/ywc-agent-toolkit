# Task: 000038-020-docs-wire-doc-generator-consumers

## Prerequisites
- [ ] `000037-010-docs-language-resolution-reference` 완료(`references/language-resolution.md` 존재).

## Allowed Edit Scope
- `claude-code/skills/ywc-task-generator/SKILL.md`
- `claude-code/skills/ywc-spec-writer/SKILL.md`
- `claude-code/skills/ywc-plan/SKILL.md`
- 그 외 파일 편집 금지.

## Stop Conditions
- 기존 fallback(task-generator `en`, spec-writer `ko`) 을 유지하며 pointer 를 넣을 수 없는 구조면 중단하고 보고 — AC10 회귀 금지가 우선.
- resolution 을 subagent 안에서 수행해야 하는 skill 인데 payload 전달 경로가 불분명하면 중단하고 보고(EC8).

## Implementation Steps
- [ ] `ywc-task-generator/SKILL.md`(:43, :129) — "Language Policy section or Documentation Writing Guidelines" 추론 prose 를 `> **Action required**: Read [../references/language-resolution.md]` pointer 로 교체. user-global CLAUDE.md 확인 + project-over-user precedence 반영. 부재 시 `en`+infer-then-ask fallback 보존(A5). subagent fan-out 시 main-context 해석 후 payload 전달 명시(EC8).
- [ ] `ywc-spec-writer/SKILL.md`(:90) — "declared primary documentation language" cue 를 canonical pointer 로 교체. user-global CLAUDE.md 확인. 부재 시 `ko` fallback 보존.
- [ ] `ywc-spec-writer/SKILL.md`(:108) — resolved language code 를 `init-spec-structure.sh <lang>` 첫 위치 인자로 전달함을 명시(A4).
- [ ] `ywc-plan/SKILL.md`(:98) — Step 2 always-read "language policy" 를 canonical `## Language Policy` 섹션 + resolution 규칙에 정렬해 plan 출력 언어가 resolved 언어와 일치하도록.
- [ ] 세 skill 모두 기존 `references/language-policy.md`(locale writing 규칙) 참조는 유지.

## Task Verify
- [ ] `grep -q "language-resolution.md" claude-code/skills/ywc-task-generator/SKILL.md`
- [ ] `grep -q "language-resolution.md" claude-code/skills/ywc-spec-writer/SKILL.md`
- [ ] `grep -q "language-resolution.md" claude-code/skills/ywc-plan/SKILL.md`
- [ ] `grep -qi "en\b" claude-code/skills/ywc-task-generator/SKILL.md` (fallback 문구 잔존 확인 — 수동 리뷰)

## Verification
- [ ] `bash scripts/validate.sh` 통과.
- [ ] 수동: 세 skill 의 fallback(정책 부재 시 현행 동작)이 문서상 보존됐는지 확인(AC10).
