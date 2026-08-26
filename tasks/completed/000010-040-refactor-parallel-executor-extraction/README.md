# 000010-040-refactor-parallel-executor-extraction

## Purpose
`ywc-parallel-executor/SKILL.md` 본문이 500줄(현재 567줄)을 초과하여 S4 가 3 으로 떨어진다. 대형 정적 섹션을 `references/` 로 추출하여 본문을 500줄 이하로 낮추고 S4 를 5 로 회복한다. 더불어 description 안티트리거에 `ywc-worktrees` 를 명시한다(S1)(FR8).

## Scope
- 본문의 대형 정적 블록(모드별 참조 표, 워크드 예시, 장문 결정 표)을 `references/<topic>.md` 로 추출(각 ≥30줄, A14 인바운드 포인터 유지)
- `SKILL.md` description 안티트리거에 `ywc-worktrees` 추가

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-activation-fixes.md` — FR8, Amendment A5(추출 서브스텝, 567줄/≥30줄/A14)
### Summary
본문 ≥67줄을 추출하여 ≤500(A8) 달성. 추출 파일은 각 ≥30줄(미만이면 `_over_extracted_refs` 가 S4 를 도리어 1 깎음). 각 신규 참조는 `SKILL.md` 본문에 인바운드 포인터로 링크(A14 `_refs_have_pointers`). description 의 `ywc-worktrees` 안티트리거로 worktrees 와의 S1 경계 확립.
### Out of Scope (from spec)
- 다른 스킬/에이전트 description
- 동작 변경(behavior change) — 순수 구조 추출(refactor), 본문 내용 의미 동일 유지

## Dependencies
### Depends On
- (없음) — Phase 000010 독립 편집 태스크
### Depended By
- `000011-010-infra-rebaseline-rescore` — 재채점으로 S4 3→5 확인

## Key Files
- `claude-code/skills/ywc-parallel-executor/SKILL.md` (본문 추출 + description)
- `claude-code/skills/ywc-parallel-executor/references/*.md` (신규)

## Notes
- 본 태스크만 구조(refactor) 변경 — description-only 편집 태스크들과 분리하여 큰 diff 가 섞이지 않게 함.
- 추출은 의미를 보존(순수 이동). 본문 워크플로 단계 자체는 변경 금지.
- `--ci` 금지(→ 000011). 읽기 전용 `--format json` 검증.

## Out of Scope
- 워크플로 로직 변경, 다른 파일
- history.mechanical.json 재기준선화(→ 000011-010)

## Parallel Execution Metadata
- **Ownership:** `claude-code/skills/ywc-parallel-executor/SKILL.md`, `claude-code/skills/ywc-parallel-executor/references/`
- **Shared Surfaces:** (없음) — 단일 스킬 디렉터리
- **Conflicts With:** (None identified)
- **Parallelizable After:** (없음 — 즉시 실행 가능)
- **Task Verify:**
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-parallel-executor --format json` → `signals.body_lines` ≤ 500, `axes.S4 == 5`, `over_extracted_refs == []`
  - `grep -c 'ywc-worktrees' claude-code/skills/ywc-parallel-executor/SKILL.md` ≥ 1
  - 각 신규 `references/*.md` 줄 수 ≥ 30, 본문에서 참조됨
