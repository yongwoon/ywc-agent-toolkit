# Task: 스킬 SKILL.md 결함 수정 + Codex 미러 동기화

## Prerequisites
- [ ] OQ2 방침 확인: FR5(product-review) 실편집 vs 비결함 기록. (비차단 — 미결이면 "비결함 기록"으로 진행)

## Allowed Edit Scope
- `claude-code/skills/{ywc-project-docs,ywc-project-scaffold,ywc-merge-dependabot,ywc-product-review,ywc-tdd-ritual}/SKILL.md`
- 대응 `codex/skills/<동일>/SKILL.md` (diff 존재 시). 그 외 파일 편집 금지.

## Stop Conditions
- project-docs 설명 편집 후 재평가에서 project-docs 또는 spec-writer의 S1(활성화) 회귀가 의심되면 보고(EC1).
- Codex 미러가 이미 다른 문구여서 결함이 없으면 해당 미러는 건드리지 말고 기록(EC3).
- 생성 패키지(`plugins/ywc-agent-toolkit`)를 수기 편집해야 할 상황이면 중단하고 보고(EC4).

## Implementation Steps
- [ ] **FR2** `ywc-project-docs/SKILL.md:4` 설명 끝에 anti-trigger append: "Do not use for ... Specification
      문서(use ywc-spec-writer)". 기존 트리거 문구는 보존. 본문 :70-75에서 `references/project-docs-structure.md`
      로드를 "문서 생성 전 필수" Step으로 승격(또는 최소 디렉토리/명명 결정을 본문에 인라인).
- [ ] **FR3** `ywc-project-scaffold/SKILL.md:80` 부근에 fallback 1문장: "매칭 language reference가 없으면 일반
      구조 원칙으로 진행하고 스택 가정을 사용자에게 확인".
- [ ] **FR4** `ywc-merge-dependabot/SKILL.md:150-162` 수동 충돌 절차 앞에 선행조건 명시: "먼저 `@dependabot rebase`
      코멘트; rebase가 충돌을 해소하지 못할 때만 수동 checkout/resolve". :30 defense와 정합.
- [ ] **FR5** `ywc-product-review/SKILL.md:26` — excuse 문자열의 P0/P1/P2를 High/Medium/Low로 통일. (또는 편집
      대신 본 태스크 Notes에 "비결함: P0/P1/P2는 excuse 예시일 뿐, 워크플로우는 이미 일관" 기록 — OQ2)
- [ ] **FR6** `ywc-tdd-ritual/SKILL.md:74` `<run the test, scoped to just the new test>`를 러너 추론 규칙으로
      대체: "package.json/pyproject의 test 스크립트로 신규 테스트만 실행; 러너 불명이면 사용자에게 확인".
- [ ] **FR11** 각 편집한 스킬의 `codex/skills/<skill>/SKILL.md`를 열어 동일 결함 존재 여부 확인 후, 존재할 때만
      동일하게 반영. Codex frontmatter 제약(name/description만) 준수.

## Task Verify
- [ ] `bash scripts/validate.sh` exit 0 (frontmatter/locale/shellcheck/Codex sync 게이트 통과).
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json`에서
      5개 스킬의 S2/S4/S5 mechanical 회귀 없음(모두 5 유지).

## Verification
- [ ] `bash scripts/validate.sh` exit 0.
- [ ] `git diff --stat` 이 의도한 파일(최대 10개: 5 skill + 5 codex mirror)만 포함.
