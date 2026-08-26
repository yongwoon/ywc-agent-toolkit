# 000055-020-infra-rd-row-scripts

## Purpose

Deletion Test가 필요로 하는 두 개의 bundled script를 만든다. 현재 저장소에는 Rationalization Defense row의 **위치**를 아는 도구가 하나도 없다 — canonical counter는 `int` 하나만 반환하고 줄 번호를 버린다. 표본 추출과 variant 생성 둘 다 `[(start,end), …]`를 요구하는데 그것이 존재하지 않는다.

## Scope

- `claude-code/skills/ywc-skill-author/scripts/enumerate-rd-rows.sh` (신규) — RD data row 당 `<start>-<end>` 줄 범위 하나씩 출력. `--self-check` 모드가 46개 skill 전체에 대해 canonical counter와 count parity를 단언한다.
- `claude-code/skills/ywc-skill-author/scripts/build-variant.sh` (신규) — 지정한 inclusive 범위를 삭제한 variant를 temp path에 쓰고 그 경로를 출력. 범위가 부적법하면 **쓰지 않고** exit 1.
- `claude-code/skills/CLAUDE.md`의 script registry table에 두 행 추가.
- 두 script를 가리키는 pointer를 `ywc-skill-author/SKILL.md`에 추가.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-2-two-bundled-scripts`
- `docs/ywc-plans/skill-pruning-pilot.md` AC3 (enumerator parity), AC4 (variant 결정성/무손실)
- `docs/ywc-plans/skill-pruning-pilot.md#edge-cases` — 마지막 data row 삭제 시 header orphan

### Summary

`_rationalization_data_rows()` (`score.py:379-395`)는 `section.splitlines()`를 필터링하고 길이 차를 취한다 — 줄 번호를 보존하지 않고 row 내용도 버린다. `enumerate-rd-rows.sh`는 **그 줄-필터링 로직을 그대로 확장하되 위치를 버리는 대신 보존**해서 만든다.

**canonical의 의미를 정확히 지켜라**: `_rationalization_data_rows()`가 canonical인 이유는 그것이 CI 게이트를 결정하는 함수이기 때문이다. 따라서 불일치는 **언제나 enumerator의 결함**이지 counter의 결함이 아니다.

**counter와 quota를 분리하라.** parity 계약은 `_rationalization_data_rows()`(행 세기)에 대한 것이지 `score.py:290`의 `>= 5` quota 판정에 대한 것이 아니다. `000058-010`이 quota를 제거해도 이 script의 self-check는 그대로 통과해야 한다. self-check가 quota 판정을 읽지 않도록 설계하라 — 이것이 다음 phase에서 계약이 깨지지 않게 하는 유일한 방어다.

### Out of Scope (from spec)

- 어떤 row도 실제로 삭제/커밋하지 않는다 (AC2 global invariant). `build-variant.sh`는 temp path에만 쓴다.
- 비-table 형태의 RD 섹션 처리 — RD corpus는 100 % single-table로 검증되었으므로 structural check는 table 전용이며, 비-table 분기는 이 pilot의 scope 밖이다.
- `codex/skills/**`, `plugins/**`

## Criticality

`normal` — 두 script는 read-only 분석 도구이며 CI 게이트를 바꾸지 않는다. `score.py`는 읽기 전용 reference다.

## Dependencies

### Depends On

- `000053-010-refactor-skill-author-audit-workflow` — audit mode와 `scripts/` 규약, script registry 관례를 제공한다.

### Depended By

- `000056-010-refactor-skill-author-deletion-test` — FR-1의 1단계(enumerate)와 4단계(build variant)가 이 두 script를 호출한다.
- `000057-010-test-pilot-sample-frame` — 표본 추출 프레임이 enumerator 출력으로만 만들어진다.

## Key Files

- `claude-code/skills/ywc-skill-author/scripts/enumerate-rd-rows.sh` (신규, mode `100755`)
- `claude-code/skills/ywc-skill-author/scripts/build-variant.sh` (신규, mode `100755`)
- `claude-code/skills/CLAUDE.md` (script registry table 2행 추가)
- `claude-code/skills/ywc-skill-author/SKILL.md` (script pointer)

## Notes

- 두 script 모두 `set -euo pipefail`, mode `100755`, registry에는 **`bash` prefix 없이** 등록한다 (`claude-code/skills/CLAUDE.md:282-309`의 모든 sibling과 동일).
- `build-variant.sh`의 exit 1 조건은 세 가지다: out-of-bounds, inverted range, 그리고 **table header에 data row가 0개로 남게 되는 경우**. 세 번째가 사양의 Edge Case다.
- 결정성이 계약이다 — 동일 입력에 대한 재실행은 byte-identical이어야 한다(`cmp` exit 0). variant는 LLM이 손으로 편집하지 않는다; 우발적 편집 하나가 대조를 무효화한다.
- 측정된 corpus: **46 skills, 419 data rows**, min 5, max 21, mean 9.11.

## Out of Scope

- 삭제 실행, label 부여, 통계 계산 (각각 `000056-010` / `000057-020` 소유)
- `score.py` 수정

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-skill-author/scripts/enumerate-rd-rows.sh` (신규, 단독)
- `claude-code/skills/ywc-skill-author/scripts/build-variant.sh` (신규, 단독)
- `claude-code/skills/CLAUDE.md` — script registry table 행만
- `claude-code/skills/ywc-skill-author/SKILL.md` — script pointer 줄만

### Shared Surfaces

- `claude-code/skills/CLAUDE.md` — `000058-010`이 같은 파일의 A7 prose 사본(`:84-85`)을 편집한다. 다른 섹션이지만 같은 파일이다.
- `claude-code/skills/ywc-skill-author/SKILL.md` — `000053-010`, `000056-010`, `000058-010`, `000059-040`이 모두 이 파일을 편집한다.
- `.claude/skills/ywc-toolkit-eval/scripts/score.py` — read-only reference (parity 대상).

### Conflicts With

- `000056-010-refactor-skill-author-deletion-test` — 같은 `SKILL.md`를 편집한다. 순차 실행.
- `000053-010-refactor-skill-author-audit-workflow` (부모 spec) — 같은 `SKILL.md` / `scripts/`. merge 후에만 시작.

### Parallelizable After

- `000053-010-refactor-skill-author-audit-workflow`

### Task Verify

- `bash claude-code/skills/ywc-skill-author/scripts/enumerate-rd-rows.sh --self-check` → exit 0, `PARITY OK: 46/46`
- `bash claude-code/skills/ywc-skill-author/scripts/build-variant.sh <skill-dir> <start> <end>` → variant 줄 수 == `original − (end − start + 1)`, 재실행 시 `cmp` exit 0
- out-of-bounds / inverted / header-orphan 3종 입력 각각 exit 1이며 **아무 파일도 쓰지 않는다**
