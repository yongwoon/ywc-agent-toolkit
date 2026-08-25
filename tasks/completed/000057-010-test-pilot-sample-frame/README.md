# 000057-010-test-pilot-sample-frame

## Purpose

파일럿의 **표본 우주를 확정하고 고정한다.** 층화 추출된 80개 후보 목록, 후보별 시나리오, 부모 audit SHA를 report에 기록해 dispatch가 시작되기 전에 되돌릴 수 없게 만든다. 이것이 별도 task인 이유: dispatch 루프가 중간에 죽었을 때 표본이 조용히 다시 뽑히면 AC7의 keyed resume가 전제하는 "안정된 표본 우주"가 무너진다.

## Scope

- `docs/ywc-plans/prune-report-rationalization-defense.md` 생성 (report의 header + 후보 목록 부분).
- 부모 audit이 착지한 커밋의 **git SHA**를 header에 기록한다. SHA 없이는 run이 시작을 거부한다 (AC8).
- 층화 추출 실행 (AC6): Stratum A 40개, Stratum B 40개.
- 후보별 시나리오 결속 및 기록 (FR-1 3단계).
- 80개 후보 각각에 대해 `build-variant.sh`가 성공하는지 사전 검증한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-3-run-the-pilot`
- `docs/ywc-plans/skill-pruning-pilot.md` AC6 (층화 추출), AC7 (keyed resume), AC8 (부모 audit SHA)
- `docs/ywc-plans/skill-pruning-pilot.md#fr-1-...` 2단계·3단계

### Summary

**추출된 후보 목록은 어떤 dispatch보다 먼저 report에 쓰이고, 재개된 run은 다시 뽑지 않고 그것을 읽는다.** 그렇지 않으면 crash 하나가 표본 우주를 조용히 바꿔버릴 수 있는데, AC7의 keyed resume는 그 우주가 고정되어 있다고 가정한다.

**AC8의 SHA 요구는 형식적 절차가 아니다.** 부모의 audit 출력은 terminal-only여서 다른 어떤 artifact도 남기지 않는다. 따라서 "부모가 먼저 돌았어야 한다"는 서술은 검증 불가능한 이야기이고, 유일하게 검증 가능한 증거가 그 커밋의 SHA다.

층화 추출은 실현 가능함이 검증되어 있다: 46개 skill 전부가 각 stratum에 ≥1행을 가지며, Stratum A pool = 184행, Stratum B pool = 235행이다.

### Out of Scope (from spec)

- subagent dispatch, 비교, floor 계산, labeling (`000057-020` 소유)
- 어떤 skill 파일의 편집 (AC2). variant는 temp path에만 쓰인다.

## Criticality

`normal`

## Dependencies

### Depends On

- `000056-010-refactor-skill-author-deletion-test` — 층화 추출 규칙, report 스키마, 시나리오 결속 규칙을 제공한다.
- `000055-020-infra-rd-row-scripts` — enumerator와 variant builder.
- `000054-010-test-skill-audit-validation` — 부모 audit이 착지한 커밋(AC8의 SHA 출처).

### Depended By

- `000057-020-test-pilot-dispatch-report` — 고정된 후보 목록과 시나리오를 읽어 dispatch한다.

## Key Files

- `docs/ywc-plans/prune-report-rationalization-defense.md` (신규 — header + 후보 목록)

## Notes

- report의 writer는 **하나뿐**이다 (orchestrator). subagent는 경로만 반환한다.
- 후보 key 형식은 `<file>:<start>-<end>` 이며 이것이 resume의 유일한 키다 (AC7).
- 80개 후보 각각에 대해 `build-variant.sh`를 미리 한 번 돌려 exit 0을 확인하라. 마지막 남은 data row를 뽑았다면 build가 exit 1로 거부하는데(header orphan), 그 사실을 dispatch 도중에 발견하는 것보다 지금 발견하는 편이 훨씬 싸다. 거부된 후보는 같은 stratum·같은 제약 하에서 다시 뽑는다.
- **표본이 확정된 뒤에는 바꾸지 않는다.** 라벨이 마음에 들지 않아 표본을 조정하는 것은 테스트를 무효화한다.

## Out of Scope

- 480 dispatch
- 통계 계산

## Parallel Execution Metadata

### Ownership

- `docs/ywc-plans/prune-report-rationalization-defense.md` (신규, 단독 소유 — 단일 writer)

### Shared Surfaces

- `docs/ywc-plans/prune-report-rationalization-defense.md` — `000057-020`이 같은 파일에 append한다. 단일 writer 규약으로 보호된다.
- `claude-code/skills/**` — read-only.

### Conflicts With

- `000057-020-test-pilot-dispatch-report` — 같은 report 파일. 순차 실행 (010이 header/후보를 쓰고, 020이 라벨 행을 append).

### Parallelizable After

- `000056-010-refactor-skill-author-deletion-test`

### Task Verify

- report header에 부모 audit의 git SHA가 있고, 그 SHA가 실제 커밋으로 resolve된다
- 후보가 정확히 **80개**: Stratum A 40 + Stratum B 40
- 어떤 skill도 한 stratum에 2행을 기여하지 않는다
- 각 stratum이 ≥40개 서로 다른 skill에 걸친다
- 80개 후보 전부 `build-variant.sh` exit 0
- `git diff -- claude-code/`가 비어 있다 (skill 파일 무변경)
