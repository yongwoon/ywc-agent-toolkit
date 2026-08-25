# 000060-040-docs-impl-review-smell-baseline — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] (None — root task) 선행 task 없음
- [ ] `ywc-skill-author`를 먼저 호출해 canonical rule set(A14)을 로드했다
- [ ] `references/recurring-defects.md`를 읽어 공유-catalog 패턴과 중복 항목 후보를 파악했다

## Allowed Edit Scope
- [ ] `references/code-smell-baseline.md`(신규), `references/architecture-agent.md`, `references/design-agent.md`만 편집한다
- [ ] `SKILL.md`(030 소관)·`recurring-defects.md` 본문 편집이 필요하면 중단하고 보고

## Stop Conditions
- [ ] `ywc-skill-author` 선행 호출 없이 신규 참조 파일 생성을 시작해야 하는 상황이면 중단
- [ ] Fowler smell 항목이 recurring-defects.md와 실질 중복인데 위임 없이 복제하려는 경우 중단
- [ ] pointer가 1줄을 넘어 agent 파일에 절차/설명을 중복 서술하게 되면 중단(pointer만 유지)

## Implementation Steps
- [ ] `references/code-smell-baseline.md` 신규 생성
  - [ ] 상단 3원칙 명시: (1) repo 문서 표준이 baseline override, (2) 모든 항목은 judgement call, (3) tooling 강제 항목 skip
  - [ ] 12개 smell을 "정의 → 발견 신호 → 수정 방향" 표로 정리: Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest
  - [ ] recurring-defects.md와 겹치는 항목은 "recurring-defects.md §N 참조"로 위임(중복 서술 금지)
- [ ] `references/architecture-agent.md` 말미에 `code-smell-baseline.md` pointer 1줄 추가(구조적 smell·Duplicated Code 우선 위치)
- [ ] `references/design-agent.md`의 Naming Consistency 절에 `code-smell-baseline.md` pointer 1줄 추가(Mysterious Name)

## Task Verify
- [ ] `ls claude-code/skills/ywc-impl-review/references/code-smell-baseline.md` → 파일 존재
- [ ] `grep -c "|" claude-code/skills/ywc-impl-review/references/code-smell-baseline.md` → 12-smell 표 행 존재
- [ ] `grep -n "code-smell-baseline" claude-code/skills/ywc-impl-review/references/architecture-agent.md` → 1건 이상
- [ ] `grep -n "code-smell-baseline" claude-code/skills/ywc-impl-review/references/design-agent.md` → 1건 이상

## Verification
- [ ] `ywc-skill-author` Validation Checklist(특히 Progressive Disclosure) 전부 PASS
- [ ] `bash scripts/validate.sh` exit 0
- [ ] (해당 없음) markdownlint — references/*.md는 lint glob 대상 아님
