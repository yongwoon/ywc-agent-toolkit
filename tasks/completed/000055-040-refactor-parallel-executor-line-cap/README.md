# 000055-040-refactor-parallel-executor-line-cap

## Purpose

`ywc-parallel-executor/SKILL.md`가 502줄로 A8의 500줄 상한을 위반한다. 정적 콘텐츠 한 블록을 `references/`로 추출해 상한 아래로 되돌린다.

## Scope

- `claude-code/skills/ywc-parallel-executor/SKILL.md`에서 **정적**(lookup table 또는 decision tree) 블록 ≥30줄을 `references/`로 추출하고, 본문에는 한 줄 pointer만 남긴다.
- 부모 spec의 audit report가 이 skill에 대해 낸 findings를 인용한다 (부모 FR-6 요구).

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-6-clear-the-a8-violation-ywc-parallel-executor-ac15`
- `docs/ywc-plans/skill-pruning-pilot.md` AC15
- `docs/ywc-plans/skill-engineering-hardening.md` FR-6 (pilot 선정은 audit findings를 인용해야 한다)
- `claude-code/skills/ywc-skill-author/SKILL.md:93` — Tier-2 pinning 규칙

### Summary

**무엇을 추출하면 안 되는지가 무엇을 추출할지보다 먼저다.** `ywc-skill-author/SKILL.md:93`에 따르면 Workflow / Rationalization Defense / Validation Checklist는 **정의상 Tier 2이며 Tier 3으로 절대 추출하지 않는다**. 따라서 workflow prose와 RD table은 추출 대상이 될 수 없다. 남는 것은 정적 lookup table이나 decision tree다.

이 제약이 바로 이 spec 전체의 논리적 근거이기도 하다 — RD corpus는 규칙에 의해 activation-time context에 고정되어 있어서 **추출이 아니라 삭제만이 비용 절감 수단**이다. 그래서 pilot이 필요하다.

`references/`에 새로 만드는 파일은 `validate-skill.sh:60-69`의 두 조건을 만족해야 한다: **≥30줄**이고, skill `.md`에서 pointer가 있어야 한다.

### Out of Scope (from spec)

- Workflow prose, Rationalization Defense table, Validation Checklist 추출 (Tier-2 pinning 위반)
- RD row 삭제 (AC2 global invariant)
- 다른 skill의 줄 수 정리

## Criticality

`normal` — 단일 skill의 문서 구조 변경. CI 게이트나 공유 계약을 건드리지 않는다.

## Dependencies

### Depends On

- `000054-010-test-skill-audit-validation` — 부모 spec의 audit report가 이 skill에 대한 findings를 낸다. AC15의 "cite the parent's audit findings" 요구를 만족하려면 그 report가 존재해야 한다.

### Depended By

- (없음 — 독립적인 정리 작업이다.)

## Key Files

- `claude-code/skills/ywc-parallel-executor/SKILL.md` (축소)
- `claude-code/skills/ywc-parallel-executor/references/<new>.md` (신규, ≥30줄)

## Notes

- 502 → 500 이하로 내리는 데는 3줄만 있으면 되지만, `references/` 파일은 **≥30줄**이어야 한다. 즉 추출 블록은 30줄 이상이어야 하고, 결과적으로 `SKILL.md`는 500보다 여유 있게 내려간다. 여유를 만드는 것이 목적에 부합한다.
- 추출한 블록을 `SKILL.md`에서 잘라낸 뒤 pointer 한 줄을 남긴다 — 요약을 남기지 마라. 요약은 중복이고, 중복은 다시 drift한다.

## Out of Scope

- `ywc-parallel-executor`의 동작 변경
- 다른 near-500-line skill 처리

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/references/**`

### Shared Surfaces

- (없음 — 이 task는 `ywc-parallel-executor` 디렉토리 밖으로 나가지 않는다.)

### Conflicts With

- (None identified.)

### Parallelizable After

- `000054-010-test-skill-audit-validation`

### Task Verify

- `wc -l claude-code/skills/ywc-parallel-executor/SKILL.md` ≤ 500
- `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/ywc-parallel-executor/` exit 0
- 새 `references/*.md`가 ≥30줄이고 `SKILL.md`에서 pointer가 있다
- `git diff`에 RD 섹션 내부의 `^-` 삭제 줄이 없다 (AC2)
