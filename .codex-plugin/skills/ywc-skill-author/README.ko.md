# ywc-skill-author

새로운 ywc-* skill을 작성하거나 기존 skill의 구조를 개선할 때 사용하는 **메타 skill**입니다. Production ywc-* skill에서 도출된 표준 규칙(Frontmatter format, Rationalization Defense, multilingual triggers, progressive disclosure 등)을 LLM이 자동으로 따르도록 강제합니다.

## 사용 시나리오

- 새 ywc-* skill을 처음부터 작성할 때
- 기존 ywc-* skill의 frontmatter, body section, references 구조를 개선할 때
- ywc-* skill을 표준 rule set 기준으로 audit할 때

## 사용 방법

```bash
/ywc-skill-author
```

또는 자연어로 호출:

> "ywc skill 만들어줘"
> "ywc skill 개선해줘"
> "ywc skill 룰 점검해줘"

## 입력

- 새 skill의 경우: skill 목적, 주요 trigger 시나리오
- 기존 skill audit의 경우: 대상 skill 경로

## 출력

- 표준 구조 (Frontmatter + Rationalization Defense + Workflow + Validation Checklist)를 갖춘 SKILL.md
- 필요 시 `references/` 하위 보조 문서
- 다국어 README 세트 (`README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`)

## 핵심 규칙

이 skill이 강제하는 표준은 다음과 같이 구성됩니다:

- **Mandatory Rules**: Frontmatter / Body / Filesystem 영역의 강제 규칙 (A1–A13)
- **Recommended Rules**: 상황별 권장 규칙 (B1–B7)
- **Format Conventions**: Korean prose + English Technical 용어 정책 등
- **Anti-patterns**: Description workflow summary, stub code, `@` syntax 등 금지 패턴

상세한 내용은 `SKILL.md` 본문과 `references/` 하위 4개 문서를 참조합니다.

## 관련 Skill

- `ywc-task-generator` — Task 생성 시 동일한 multilingual policy + reference 분리 패턴 적용
- 모든 ywc-* skill — 본 skill의 규칙을 따름

## 참고 문서

- `references/skill-template.md` — 새 skill 시작 template
- `references/rationalization-defense-cookbook.md` — Rationalization Defense table 작성 가이드
- `references/description-anti-patterns.md` — Description field 작성 시 금지 패턴
- `references/cross-skill-graph.md` — ywc-* skill 간 prerequisite + cross-reference 그래프
