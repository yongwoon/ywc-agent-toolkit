# 000043-010-test-setup-language-trigger-cases

## Purpose

`ywc-setup-language`의 활성화 커버리지 공백을 해소한다. `trigger-cases.json`에 positive ≥3, collision ≥2를
추가하여 `score.py`의 coverage 신호가 `sufficient=true`가 되게 하고, 후속 `ywc-toolkit-eval` 판단-tier
활성화 판정관이 이 스킬의 S1을 산출할 수 있게 한다.

## Scope

- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`에 `ywc-setup-language` 케이스 세트 추가.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/toolkit-eval-backlog-2026-07-06.md` — §AC1′, §FR1′, §OQ1′, EC2 (Iteration 1 Amendments가 권위본)

### Summary
score.py는 coverage를 signals-only로만 다루고 `axes.S1`은 null로 유지한다(설계상, `score.py:340`). 따라서 본
태스크는 S1을 직접 산출하지 않으며, coverage 신호를 sufficient로 만드는 것이 목표다. 실제 S1은 판단-tier
활성화 판정관이 신규 케이스로 산출한다.

### Out of Scope (from spec)
- S1 점수 자체의 산출(판단-tier 소관), `scorecard.md`/`history.json` 재생성, score.py 로직 변경.

## Criticality
`normal` — 평가 픽스처(JSON) 추가. 보안/결제 표면 아님.

## Dependencies
- **Depends On**: (없음) — 독립 실행 가능.
- **Depended By**: (없음). 후속 `ywc-toolkit-eval` 재평가가 소비하나 태스크 의존은 아님.

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` (수정)

## Notes
- **⚠️ 착수 전 결정 필요(§OQ1′, blocking)**: collision이 지목할 실재 경합 형제를 먼저 확정해야 한다. 권장 후보
  `ywc-project-mission`("프로젝트 설정" 표면 경합). 진짜 경합 형제가 없다고 판단되면 eval 소유자가 커버리지
  규칙(collision≥2) 예외를 승인하고 `COVERAGE_MIN_COLLISIONS` 예외를 문서화한다.
- collision을 negative로 대체하지 말 것(EC2). 케이스 shape: `{id, prompt, expected, kind, impostor?, note?}`.

## Out of Scope
- 다른 스킬/에이전트 문서 편집. Codex 대응(setup-language는 Codex 미러 없음).

## Parallel Execution Metadata
- **Ownership**: `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`
- **Shared Surfaces**: `trigger-cases.json` (다른 태스크는 이 파일을 만지지 않음)
- **Conflicts With**: (None identified)
- **Parallelizable After**: (즉시 — OQ1 결정 후)
- **Task Verify**:
  `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-setup-language --format json` →
  `signals.coverage.sufficient == true` 이고 stderr "below minimum" 경고에 ywc-setup-language 미포함.
