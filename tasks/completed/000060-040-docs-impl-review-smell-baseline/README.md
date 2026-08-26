# 000060-040-docs-impl-review-smell-baseline

## Purpose
`ywc-impl-review`에 신규 공유 참조 파일 `references/code-smell-baseline.md`(Fowler 12-smell)를 생성하고, `architecture-agent.md`와 `design-agent.md`에서 각각 1줄 pointer로 참조하도록 한다(FR-5/AC5). `recurring-defects.md`와 동일한 "공유 catalog, 여러 agent 파일이 참조" 패턴을 따른다.

## Scope
- 신규 `claude-code/skills/ywc-impl-review/references/code-smell-baseline.md` 생성.
- 12개 Fowler smell(Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest)을 "정의 → 발견 신호 → 수정 방향" 표로 정리.
- 상단 3원칙 명시: (1) repo 문서 표준이 baseline override, (2) 모든 항목은 judgement call, (3) tooling 강제 항목 skip.
- `architecture-agent.md`(구조적 smell 다수) 파일 말미에 pointer 1줄, `design-agent.md` Naming Consistency 절에 pointer 1줄 추가. Duplicated Code pointer는 architecture-agent.md 우선.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` FR-5(line 110), AC5(line 60) — code-smell-baseline.md 요구사항과 observable
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` Edge Cases(line 152) — recurring-defects.md와 중복 시 위임 규칙
- `claude-code/skills/ywc-impl-review/references/recurring-defects.md` — 미러링할 공유-catalog 패턴 정본
- `claude-code/skills/ywc-skill-author/SKILL.md` 및 `references/` — A14(≥30줄 static content는 references/ 분리) 준수

### Summary
Fowler 12-smell을 구조적 리팩터링 catalog로 문서화한다. 이는 A14상 정적 콘텐츠(≥30줄)이므로 `references/`로 분리하는 것이 규칙에 부합한다. `recurring-defects.md`(bot-reviewer 데이터 기반: 데이터 계층·NULL 처리·concurrency 등)와는 성격이 다르나, 항목이 겹치면(예: Shotgun Surgery vs error-swallowing) code-smell-baseline.md 쪽에서 "recurring-defects.md §N 참조"로 위임한다. 3원칙은 기존 `--profile chill` 기본값·nitpick 억제 철학과 합치한다.

### Out of Scope (from spec)
- `recurring-defects.md` 내용 변경 — 위임 pointer만 추가하고 원 catalog는 건드리지 않는다.
- `ywc-impl-review/SKILL.md`의 Output Format 변경 — 030 task 소관.

## Criticality
`normal` — skill 참조 텍스트 신규 작성. 보안·데이터 surface 없음.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- (None — no downstream dependency)

## Key Files
- `claude-code/skills/ywc-impl-review/references/code-smell-baseline.md` — 신규 생성(12-smell 표 + 3원칙)
- `claude-code/skills/ywc-impl-review/references/architecture-agent.md` — 말미 pointer 1줄 추가
- `claude-code/skills/ywc-impl-review/references/design-agent.md` — Naming Consistency 절 pointer 1줄 추가

## Notes
- **ywc-skill-author 선행 실행 필수**: 신규 참조 파일 생성 + agent 파일 수정은 structural edit(typo/link fix 예외 아님).
- **중복 대조**: 12개 smell을 recurring-defects.md 항목과 대조해 겹치면 code-smell-baseline.md에서 위임 pointer로 처리(Edge Cases line 152).
- 030(spec-traceability)과 동일 skill이나 disjoint 파일이라 병렬 실행 가능.
- pointer 참조는 skill 이름/파일 경로만 사용하고 `@`-force-load는 금지(context 과소비 방지).

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-impl-review/references/code-smell-baseline.md`
- `claude-code/skills/ywc-impl-review/references/architecture-agent.md`
- `claude-code/skills/ywc-impl-review/references/design-agent.md`

### Shared Surfaces
- `공유 catalog 참조 관계: architecture-agent.md·design-agent.md → code-smell-baseline.md`(신규 참조 링크)
- `Skill 디렉터리 공유: ywc-impl-review/`(030과 같은 skill이나 파일은 disjoint)

### Conflicts With
- `(None identified)` — 030과 disjoint 파일이므로 병렬 안전.

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `ls claude-code/skills/ywc-impl-review/references/code-smell-baseline.md` — 파일 존재
- `grep -n "code-smell-baseline" claude-code/skills/ywc-impl-review/references/architecture-agent.md` — pointer 1건 이상
- `grep -n "code-smell-baseline" claude-code/skills/ywc-impl-review/references/design-agent.md` — pointer 1건 이상
- `bash scripts/validate.sh` — exit 0

## Out of Scope
- `SKILL.md` 본문 변경(030 소관).
- linter로 이미 강제되는 smell을 baseline에 재수록(3원칙 (3)에 따라 skip).
- README locale 파일 변경.
