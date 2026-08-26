# 000010-030-docs-skill-anti-triggers

## Purpose
스킬 4종(`ywc-release-pr-list`, `ywc-agentic`, `ywc-refactor-clean`, `ywc-project-docs`)의 frontmatter `description` 안티트리거에 형제 스킬/에이전트명을 명시하여 S1/S6 활성화 정밀도를 높인다(FR4–FR7).

## Scope
- FR4: `ywc-release-pr-list` — `Do not use for` 절에 `ywc-changelog-release-notes` 명시, "릴리스 노트" 트리거를 changelog 스킬에 양보
- FR5: `ywc-agentic` — `ywc-sequential-executor` / `ywc-parallel-executor` 명시(tasks/ 디렉터리가 이미 있으면 executor 가 승리)
- FR6: `ywc-refactor-clean` — `ywc-refactor-cleaner` 에이전트명을 description 안티트리거에 표면화(현재 본문 :94 에만 존재)
- FR7: `ywc-project-docs` — `ywc-doc-writer` 명시(FR3 의 반대편; 두 항목이 깔끔히 분할)

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-activation-fixes.md` — FR4, FR5, FR6, FR7, Amendment A3(A4 보존), A7/A8
### Summary
네 스킬 모두 형제명을 `Do not use for` 절 내부에 추가한다. 스킬 description 은 A2(`(ywc) Use when` 접두), A3(`Do not use for`), A4(한국어+일본어 문자), S4(<900자 lean) 구조 점검을 **유지해야 한다**. 특히 FR4 의 "릴리스 노트" 제거는 해당 description 의 유일한 한글 스팬이면 A4 가 깨지므로, 제거 전 다른 한글 스팬 잔존을 확인하고 없으면 비충돌 한국어 트리거로 치환한다(A3).
### Out of Scope (from spec)
- 본문(body) 편집 — 활성화는 frontmatter description 만으로 결정(refactor-clean 본문 :94 의 에이전트명은 그대로; FR6 는 description 표면화만)
- Codex 미러 — 후속 plan

## Dependencies
### Depends On
- (없음) — Phase 000010 독립 편집 태스크
### Depended By
- `000011-010-infra-rebaseline-rescore` — 재채점으로 S1/S6 개선 확인

## Key Files
- `claude-code/skills/ywc-release-pr-list/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-agentic/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-refactor-clean/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-project-docs/SKILL.md` (frontmatter description)

## Notes
- 스킬 description 4종 모두 A2/A3/A4/S4 구조 보존 필수.
- A4 보존: 트리거 문구 제거 시 `grep -oE '[가-힣]+'` 로 다른 한글 스팬 잔존 확인(A3 amendment).
- `--ci` 금지(→ 000011). 읽기 전용 `--format json` 검증.

## Out of Scope
- 에이전트 description(→ 000010-010/020), parallel-executor(→ 000010-040)
- history.mechanical.json 재기준선화(→ 000011-010)

## Parallel Execution Metadata
- **Ownership:** `claude-code/skills/ywc-release-pr-list/SKILL.md`, `claude-code/skills/ywc-agentic/SKILL.md`, `claude-code/skills/ywc-refactor-clean/SKILL.md`, `claude-code/skills/ywc-project-docs/SKILL.md`
- **Shared Surfaces:** project-docs↔doc-writer 경계(FR7↔FR3, 000010-020)는 의미적 짝 — 파일 비중첩
- **Conflicts With:** (None identified)
- **Parallelizable After:** (없음 — 즉시 실행 가능)
- **Task Verify:**
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json` → 4개 스킬 S2 하락 없음(A2/A3/A4 유지), description 에 형제명 존재
  - `grep -c 'ywc-changelog-release-notes' claude-code/skills/ywc-release-pr-list/SKILL.md` ≥ 1 등 각 형제명 ≥ 1
