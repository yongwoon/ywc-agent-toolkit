# 000010-040-refactor-parallel-executor-extraction — 구현 체크리스트

## Prerequisites
- [ ] (없음) — Phase 000010 독립 편집 태스크

## Allowed Edit Scope
- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/references/` (신규 파일)
- 그 외 파일 수정 금지

## Stop Conditions
- 워크플로 단계의 의미가 바뀌면 중단(순수 이동만 허용 — behavior change 금지)
- 추출 후 어느 `references/*.md` 가 30줄 미만이면 중단(`_over_extracted_refs` 가 S4 를 깎음 — 더 큰 블록으로 묶어 재추출)
- `--ci` 실행 금지(→ 000011). 읽기 전용 `--format json` 검증.

## Implementation Steps
- [ ] 현재 본문 줄 수 확인: `awk 'END{print NR}' claude-code/skills/ywc-parallel-executor/SKILL.md` (≈567)
- [ ] 추출 후보 식별: 가장 큰 자기완결 정적 블록(모드별 참조 표 / 워크드 예시 / 장문 결정 표) — 본문 ≤500 달성에 필요한 ≥67줄 분량
- [ ] 각 블록을 `references/<topic>.md` 로 이동(각 ≥30줄 내용)
- [ ] `SKILL.md` 본문에 각 신규 참조로의 인바운드 포인터(링크) 추가(A14)
- [ ] description `Do not use for` 절에 `ywc-worktrees` 명시(S1) — A2/A3/A4 유지
- [ ] 본문 ≤500줄 재확인

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-parallel-executor --format json` → `signals.body_lines` ≤ 500, `axes.S4 == 5`, `signals.over_extracted_refs == []`
- [ ] `awk 'END{exit (NR>500)}' claude-code/skills/ywc-parallel-executor/SKILL.md` (종료코드 0)
- [ ] 각 신규 `references/*.md`: `awk 'END{exit (NR<30)}' <file>` 통과, 본문에서 파일명 참조됨
- [ ] `grep -c 'ywc-worktrees' claude-code/skills/ywc-parallel-executor/SKILL.md` ≥ 1

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] 기준선 불변: `git diff --quiet .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
