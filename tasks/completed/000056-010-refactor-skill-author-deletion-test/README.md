# 000056-010-refactor-skill-author-deletion-test

## Purpose

`ywc-skill-author`의 audit mode에 **판정 가능한(decidable)** Deletion Test를 넣는다. 부모 spec은 프로토콜의 *형태*(baseline → 삭제 → 재실행 → compare)만 명세하고 `compare`가 어떻게 결론에 도달하는지를 남겨두었다. 판정 규칙이 없으면 "compare"는 에이전트가 자기 산문을 스스로 심사하는 일로 붕괴한다 — Deletion Test가 제거하려던 바로 그 편향이다.

## Scope

- `ywc-skill-author/SKILL.md`의 audit mode에 8단계 Deletion Test 절차를 추가한다 (열거 → 층화 추출 → 시나리오 결속 → variant 생성 → blind 3+3 dispatch → 비교 → floor pooling + ceiling 검사 → labeling).
- `ywc-skill-author/references/deletion-test-rubric.md` (신규, ≥30줄) — 동등성 판정 rubric.
- 라벨 3종(`inert` / `load-bearing` / `indeterminate`), 꼬리-경계 문턱 `T`, 타당성 상한(ceiling) 규칙을 명문화한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-1-a-decidable-deletion-test-inside-ywc-skill-authors-audit-mode` (8단계 전체)
- `docs/ywc-plans/skill-pruning-pilot.md` AC5 (6 artifact + pooled floor + 꼬리 경계), AC5a (validity ceiling), AC6 (층화 추출), AC7 (keyed resume)
- `docs/ywc-plans/skill-pruning-pilot.md#edge-cases`
- `claude-code/skills/references/subagent-status-actions.md` §3.5 — subagent 반환 payload 계약

### Summary

**blind dispatch가 이 설계의 안전장치다.** 심사 subagent 6개 중 어느 것도 자기가 어느 variant를 들고 있는지, deletion test가 돌고 있는지, authoring rule이 존재하는지를 듣지 못한다. 이것이 "너는 X를 반드시 포함해야 한다"는 authoring 편향을 심사에서 배제하며, **audit이 두 번째 meta-skill 없이 `ywc-skill-author` 안에 안전하게 살 수 있는 이유**다 (AC1 global invariant).

**noise floor는 후보별로 추정하지 않는다.** 후보당 3쌍은 턱없이 부족하다 — 0/3 관측이 대략 [0 %, 71 %]의 95 % 신뢰구간을 허용한다. floor는 표본 전체에 pooling한다: 후보당 within-variant 비교 6개 × 80후보 = **480개 pooled 비교**, 여기서 모든 후보가 대조되는 전역 불일치율 하나가 나온다.

**문턱 `T`는 평균이 아니라 상위 꼬리 분위수다.** 귀무가설(삭제된 행이 진짜로 inert) 하에서 cross-variant 불일치 수는 `Binomial(9, floor_rate)`를 따른다. `T` = `P(X ≤ t) ≥ 0.95`를 만족하는 최소 `t`. 순진한 `T = floor(floor_rate × 9)`는 귀무의 *평균*에 앉아 있어서 진짜 inert한 행의 **37–61 %를 load-bearing으로 오분류**한다.

**경계는 단측이며, 싼 쪽만 보호한다 — 이 점을 문서에 소리 내어 적어라.** `T`는 `P(label = load-bearing | 진짜 inert) ≤ 5 %`를 통제한다. 이것은 무해한 오류(행이 보존될 뿐)다. **위험한 오류** `P(label = inert | 진짜 load-bearing)`는 통제하지 **못하며**, 대립가설 분포를 정의하지 않는 이 설계로는 통제할 수 없다.

> **`inert` 라벨은 AC9의 집계 대조를 위한 증거이지, 그 행을 지워도 된다는 허가가 아니다.**

### Out of Scope (from spec)

- 파일럿 **실행** (`000057-010`/`000057-020` 소유). 이 task는 절차와 rubric만 만든다.
- 어떤 행의 삭제·편집·커밋 (AC2)
- 별도의 `ywc-skill-prune` / `ywc-skill-audit` skill 생성 (AC1, 부모 spec이 금지)
- 후보당 시나리오를 여러 개 쓰는 것 (Open Question — 기본값은 후보당 1개)

## Criticality

`normal` — `.claude/skills/ywc-toolkit-eval/**`을 건드리지 않는다. 다만 이 task가 정의하는 판정 규칙이 틀리면 `000057`의 증거 전체가 무의미해지므로, rubric과 문턱 공식은 **사양 본문과 축자적으로** 대조해야 한다.

## Dependencies

### Depends On

- `000055-020-infra-rd-row-scripts` — 1단계(enumerate)와 4단계(build variant)가 이 두 script를 호출한다. script 없이는 절차가 실행 불가능하다.
- `000053-010-refactor-skill-author-audit-workflow` — audit mode 자체를 제공한다 (부모 spec).

### Depended By

- `000057-010-test-pilot-sample-frame` — 층화 추출 규칙(AC6)과 report 스키마를 여기서 가져간다.
- `000057-020-test-pilot-dispatch-report` — dispatch 절차, floor/ceiling 계산, labeling 규칙을 여기서 가져간다.

## Key Files

- `claude-code/skills/ywc-skill-author/SKILL.md` (audit mode 확장)
- `claude-code/skills/ywc-skill-author/references/deletion-test-rubric.md` (신규, ≥30줄)

## Notes

- **A8 상한을 주시하라.** `ywc-skill-author/SKILL.md`에 8단계 절차를 통째로 넣으면 500줄을 넘길 수 있다. 절차의 상세는 rubric reference로 밀고 `SKILL.md`에는 진입점과 판정 규칙 요약만 남긴다.
- rubric은 `validate-skill.sh:60-69`의 두 조건을 만족해야 한다: **≥30줄**, 그리고 skill `.md`에서 pointer 존재.
- **동등성 판정 기준**: 표현·동등 항목의 순서 차이 등 표면적 차이는 동등이다. 수행한 행동, 건드린 파일, 강제한 게이트, 발한 거부의 차이는 동등이 아니다. *어떤* 텍스트 차이든 behavioral로 보는 rubric은 아무것도 inert로 라벨하지 못하며, 그러면 pilot 자체가 no-op이 된다.
- **재시도 금지**: variant가 불일치했다는 이유로 후보를 다시 돌리는 것은 금지다 — 그것은 테스트를 "항상 통과하는 테스트"로 바꾼다.
- subagent는 artifact **경로만** 반환한다 (§3.5). 이것 없이는 80후보 sweep이 첫 wave에서 orchestrator를 포화시킨다.

## Out of Scope

- 통계 스크립트 작성 (floor/Fisher 계산은 `000057-020`이 수행)
- `score.py` 수정

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-skill-author/SKILL.md` — audit mode 섹션
- `claude-code/skills/ywc-skill-author/references/deletion-test-rubric.md` (신규, 단독)

### Shared Surfaces

- `claude-code/skills/ywc-skill-author/SKILL.md` — `000055-020`(script pointer), `000058-010`(A7 규칙), `000059-040`(A15/A16)이 같은 파일을 편집한다.
- `claude-code/skills/references/subagent-status-actions.md` §3.5 — read-only로 인용.

### Conflicts With

- `000055-020-infra-rd-row-scripts` — 같은 `SKILL.md`. 순차 실행 (000055가 먼저 merge).

### Parallelizable After

- `000055-020-infra-rd-row-scripts`

### Task Verify

- `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/ywc-skill-author/` exit 0
- `wc -l claude-code/skills/ywc-skill-author/references/deletion-test-rubric.md` ≥ 30
- `SKILL.md`가 rubric을 가리키는 pointer를 가진다
- `wc -l claude-code/skills/ywc-skill-author/SKILL.md` ≤ 500 (A8)
- `ls claude-code/skills/ | grep -E 'ywc-skill-(prune|audit)'` → 결과 없음 (AC1)
