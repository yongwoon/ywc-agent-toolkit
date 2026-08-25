# 000055-020-infra-rd-row-scripts — Implementation Checklist

## Prerequisites

- [ ] `000053-010-refactor-skill-author-audit-workflow` is completed and merged.
- [ ] `.claude/skills/ywc-toolkit-eval/scripts/score.py:379-395`의 `_rationalization_data_rows()`를 읽고 줄-필터링 규칙을 정확히 파악했다.
- [ ] `claude-code/skills/CLAUDE.md:282-309`의 script registry 관례(모드 `100755`, `bash` prefix 없음)를 확인했다.

## Allowed Edit Scope

- [ ] 신규: `ywc-skill-author/scripts/enumerate-rd-rows.sh`, `ywc-skill-author/scripts/build-variant.sh`
- [ ] 수정: `claude-code/skills/CLAUDE.md` (registry table 행), `ywc-skill-author/SKILL.md` (script pointer)
- [ ] `score.py`는 읽기 전용. 어떤 skill의 RD table도 편집하지 않는다.

## Stop Conditions

- [ ] `--self-check`가 46/46 parity에 도달하지 못하면 멈춘다. **counter를 고치지 말고 enumerator를 고쳐라** — counter가 canonical이다.
- [ ] `build-variant.sh`가 거부해야 할 입력에서 파일을 쓴다면 멈춘다.
- [ ] parity self-check가 `score.py:290`의 `>= 5` quota 판정에 의존하게 되면 멈추고 재설계한다 — `000058-010`이 그 quota를 제거하면 계약이 깨진다.

## Implementation Steps

- [ ] `enumerate-rd-rows.sh <skill-dir>` 작성: `## Rationalization Defense` 섹션을 찾고, `_rationalization_data_rows()`와 **동일한 줄-필터링 규칙**(header/separator/빈 줄 제외)을 적용하되 위치를 보존해 `<start>-<end>`를 row 당 한 줄씩 출력한다.
- [ ] `--self-check` 모드 추가: 46개 skill 각각에 대해 출력 줄 수를 세고 `_rationalization_data_rows()` 반환값과 비교, `PARITY OK: 46/46`을 찍고 exit 0. 불일치는 파일명과 두 수를 찍고 exit 1.
- [ ] self-check가 canonical counter의 **행 세기 함수만** 호출하고 `score.py:290`의 quota boolean은 읽지 않도록 한다.
- [ ] `build-variant.sh <skill-dir> <start> <end>` 작성: inclusive 범위를 잘라낸 사본을 temp path에 쓰고 경로를 stdout에 출력한다.
- [ ] `build-variant.sh`의 3종 거부 조건 구현 — out-of-bounds, inverted(`start > end`), 그리고 삭제 시 table header에 data row가 0개로 남는 경우. 각각 **쓰기 전에** exit 1.
- [ ] 두 script를 `chmod 755`하고 `set -euo pipefail`을 넣는다.
- [ ] `claude-code/skills/CLAUDE.md`의 script registry table에 두 행을 sibling과 동일한 형식으로 추가한다 (`bash` prefix 없이).
- [ ] `ywc-skill-author/SKILL.md`에 두 script pointer를 추가한다.

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/enumerate-rd-rows.sh --self-check` → exit 0, `PARITY OK: 46/46`
- [ ] 임의 skill에 대해: `orig=$(wc -l < SKILL.md)`; variant 줄 수 == `orig − (end − start + 1)` 정확히 일치
- [ ] 동일 입력 두 번 실행 → `cmp -s` exit 0 (byte-identical)
- [ ] out-of-bounds / inverted / 마지막 남은 data row 3종 → 각각 exit 1, 새 파일 없음
- [ ] `test -x claude-code/skills/ywc-skill-author/scripts/enumerate-rd-rows.sh && test -x claude-code/skills/ywc-skill-author/scripts/build-variant.sh`

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (AC13).
- [ ] `for d in claude-code/skills/ywc-*/; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh "$d" || echo "FAILED: $d"; done` → `FAILED:` 없음.
- [ ] `git diff`에 RD 섹션 내부의 `^-` 삭제 줄이 하나도 없다 (AC2).
