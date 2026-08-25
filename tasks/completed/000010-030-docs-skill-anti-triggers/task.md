# 000010-030-docs-skill-anti-triggers — 구현 체크리스트

## Prerequisites
- [ ] (없음) — Phase 000010 독립 편집 태스크

## Allowed Edit Scope
- `claude-code/skills/ywc-release-pr-list/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-agentic/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-refactor-clean/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-project-docs/SKILL.md` (frontmatter description)
- 그 외 파일/본문 수정 금지

## Stop Conditions
- `--ci` 실행 금지(→ 000011 소관). 읽기 전용 `--format json` 검증만.
- 편집 후 어느 스킬이든 S2 가 하락하면 중단·보고(A2/A3/A4 구조 점검 깨짐 — 특히 A4 한글/일본어 스팬 손실)
- description 이 900자를 초과하면 중단(S4 leanness — 언어 나열을 토큰 형태로 압축)

## Implementation Steps
- [ ] FR4: `ywc-release-pr-list/SKILL.md` description `Do not use for` 절에 "CHANGELOG / release-note generation (use ywc-changelog-release-notes)" 추가. "릴리스 노트" 제거 전 `grep -oE '[가-힣]+'` 로 다른 한글 스팬 확인 — 유일하면 "릴리스 PR 목록" 등 비충돌 한국어로 치환
- [ ] FR5: `ywc-agentic/SKILL.md` description 안티트리거를 `ywc-sequential-executor` / `ywc-parallel-executor` 명시형으로 교체(tasks/ 존재 시 executor 승리). A2/A3/A4 유지
- [ ] FR6: `ywc-refactor-clean/SKILL.md` description `Do not use for` 절에 `ywc-refactor-cleaner` 추가(직접 삭제 요청을 분류 단계로 라우팅)
- [ ] FR7: `ywc-project-docs/SKILL.md` description `Do not use for` 절에 `ywc-doc-writer` 명시(FR3 의 반대편 — 깔끔한 분할)
- [ ] 각 편집 후 `(ywc) Use when` 접두, `Do not use for` 절, 한글+일본어 문자 잔존 확인

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json` → 4개 스킬 S2 불하락(기준선 대비), A2/A3/A4 구조 점검 통과
- [ ] `grep -c 'ywc-changelog-release-notes' .../ywc-release-pr-list/SKILL.md` ≥ 1; `grep -cE 'ywc-(sequential|parallel)-executor' .../ywc-agentic/SKILL.md` ≥ 2; `grep -c 'ywc-refactor-cleaner' .../ywc-refactor-clean/SKILL.md` ≥ 1; `grep -c 'ywc-doc-writer' .../ywc-project-docs/SKILL.md` ≥ 1
- [ ] 각 스킬 description 의 한글 스팬 ≥ 1 및 일본어 스팬 ≥ 1 유지

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] markdownlint(프로젝트 config) 통과(README*.md 글롭이지만 SKILL.md 편집이 다른 게이트를 깨지 않음 확인)
- [ ] 기준선 불변: `git diff --quiet .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
