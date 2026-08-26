# 000011-010-infra-rebaseline-rescore — 구현 체크리스트

## Prerequisites
- [ ] `000010-010-docs-reviewer-anti-triggers` 완료(머지)
- [ ] `000010-020-docs-agent-dispatch-boundaries` 완료(머지)
- [ ] `000010-030-docs-skill-anti-triggers` 완료(머지)
- [ ] `000010-040-refactor-parallel-executor-extraction` 완료(머지)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (재생성)
- `.claude/skills/ywc-toolkit-eval/evals/scorecard.md` (재생성)
- `.claude/skills/ywc-toolkit-eval/evals/history.json` (행 추가)
- 소스/스킬/에이전트 편집 금지(검증·기준선 전용)

## Stop Conditions
- `--ci` 가 회귀(하락)를 보고하면 중단·조사(Phase 000010 편집이 의도치 않게 어떤 축을 떨어뜨림 — 상향만 기대)
- 어떤 편집 항목의 `unresolved_anti_trigger_pointers` 가 비어있지 않으면 중단(신규 `use ywc-*` 포인터가 실존하지 않는 형제를 가리킴 → S5 감점)
- 무관(비대상) 항목의 총점이 하락하면 중단·보고

## Implementation Steps
- [ ] S5 포인터 검증: 각 편집 항목에 대해 `score.py --item <name> --format json | jq '..|.unresolved_anti_trigger_pointers? // empty'` 가 빈 리스트
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 실행 → PASS(무회귀) 및 `history.mechanical.json` 재생성
- [ ] 기준선 diff 검토: A2(리뷰어 4→5 캡 해제분) 및 parallel-executor S4(3→5) 등 **상향만** 포함되는지 확인
- [ ] `ywc-toolkit-eval --mode full --target all` 전체 재채점 → `evals/scorecard.md` 재생성, `evals/history.json` 에 신규 실행 1행 추가(기존 행 불변)
- [ ] 8개 대상 항목(리뷰어 3, qa, doc, release-pr-list, agentic, refactor-clean, project-docs, parallel-executor) 상승, 무관 항목 무하락 확인

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 종료코드 0(PASS)
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --format json` → go/python/typescript-reviewer `a2_collision_cap == null`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-parallel-executor --format json` → `axes.S4 == 5`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 재실행 시 무변경(안정)

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `python3 -c "import json;json.load(open('.claude/skills/ywc-toolkit-eval/evals/history.json'))"` 유효, 신규 1행만 추가
