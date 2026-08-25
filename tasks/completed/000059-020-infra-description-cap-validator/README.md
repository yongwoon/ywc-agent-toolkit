# 000059-020-infra-description-cap-validator

## Purpose

80단어 상한을 **기계적으로 강제**하고, 동시에 `validate-skill.sh`와 `score.py`의 **A2/A3 판정 불일치를 제거**한다. 상한은 검사가 없으면 다음 저자가 다시 120단어를 쓰는 순간 조용히 사라진다.

## Scope

- `validate-skill.sh`에 **80단어 상한 검사** 추가 (수리된 추출기 사용, 경계 포함: 80 PASS / 81 FAIL).
- `validate-skill.sh`의 **A2/A3를 `score.py`와 일치**시킨다 (로컬 validator를 CI 쪽으로 조인다).
- `ywc-skill-author/SKILL.md`에 새 규칙 A15(description ≤80단어) 추가 + AC16에 따라 6개 locale README **같은 커밋** 갱신.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-5-a-flat-80-word-description-cap-ac11-ac12-ac14`
- `docs/ywc-plans/skill-pruning-pilot.md` AC11 (A2/A3 통합), AC12 (상한), AC16
- `docs/ywc-plans/skill-pruning-pilot.md#existing-constraints-touched` — `score.py:286-287` vs `validate-skill.sh:37-42` 행
- `docs/ywc-plans/prune-report-rationalization-defense.md` — **enforcement 모드가 이 report의 증거 게이트 결과에 달려 있다**

### Summary

**두 validator가 A2/A3에서 실제로 다르게 판정한다:**

| | `validate-skill.sh:37-42` (로컬, 느슨) | `score.py:286-287` (CI, **canonical**) |
|---|---|---|
| A2 | substring `"(ywc) Use "` | `desc.startswith("(ywc) Use when")` |
| A3 | `"Do not use "` **또는 `"Do not invoke "`** | `Do not use (for\|during\|when\|in)` — **`invoke` 불허** |

오늘은 46/46이 양쪽을 다 통과해서 잠복 상태다. 그러나 `000059-010`이 29개 description을 다시 쓰므로, **느슨한 쪽의 사각지대에 착지한 재작성은 모든 로컬 검사를 통과하고 build를 깨뜨린다.** 그래서 통합이 재작성과 같은 FR에 있는 것이지, 후속 작업이 아니다.

**방향은 로컬 → CI 다.** `score.py`가 canonical이고 **Critical Surface**이므로 건드리지 않는다. `validate-skill.sh`를 `score.py`의 술어에 정확히 맞춘다. 이렇게 하면 FR-5 전체가 Critical Surface 밖에 머문다.

**enforcement 모드는 증거에 달려 있다** (부모 spec `:45-47`): `000057-020`의 증거 게이트가 통과했으면 hard-fail, 실패했거나 `INCONCLUSIVE`면 advisory.

### Out of Scope (from spec)

- `score.py` 수정 — Critical Surface. FR-4만이 건드린다.
- `invocation:` tier, frontmatter key 추가 — 이 spec에서 잘려나갔다.
- description 내용 수정 (`000059-010`이 이미 완료)

## Criticality

`normal` — `score.py`를 읽기만 한다. 다만 `validate-skill.sh`는 저장소 전역 게이트이므로, hard-fail로 켜기 전에 46개가 **이미 전부 통과 상태**여야 한다.

## Dependencies

### Depends On

- `000059-010-refactor-description-word-cap` — **모든 description이 이미 80단어 안에 있어야 한다.** 그렇지 않으면 상한 검사를 켜는 순간 29개가 즉시 FAIL한다.
- `000055-010-refactor-validate-skill-extractor-repair` — 상한 검사는 수리된 추출기 위에서만 의미가 있다.
- `000055-030-docs-skill-author-readme-drift-sync` — 깨끗한 README baseline 위에서 A15 추가만 반영한다.
- `000057-020-test-pilot-dispatch-report` — enforcement 모드(hard-fail vs advisory)를 결정하는 증거 게이트 결과.

### Depended By

- (없음 — 이 batch의 종결 task다.)

## Key Files

- `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh` (상한 검사 + A2/A3 통합)
- `claude-code/skills/ywc-skill-author/SKILL.md` (A15 규칙)
- `claude-code/skills/ywc-skill-author/README{,.en,.ja,.ko,.es,.zh}.md` (AC16 — 같은 커밋)

## Notes

- **순서가 안전장치다**: 재작성(`-010`) → validator(`-020`). 반대로 하면 켜는 순간 29개가 FAIL한다.
- `validate-skill.sh:9`는 `set -uo pipefail`(`-e` 없음)이다 — `fail()` accumulator가 실패하는 `grep -q`에서 살아남아야 하기 때문이다. **새 검사도 이 패턴을 따른다.**
- 상한 경계는 **포함**이다. `> 80` 일 때만 FAIL. 메시지: `FAIL: description is <N> words (> 80 word cap)`.
- **A4는 건드리지 않는다.** `validate-skill.sh`는 오늘 A4를 검사하지 않으며, 이 task도 추가하지 않는다 — `score.py`가 이미 CI에서 강제한다.

## Out of Scope

- `.claude/skills/ywc-toolkit-eval/**` 수정
- codex 번들

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh`
- `claude-code/skills/ywc-skill-author/SKILL.md` — A15
- `claude-code/skills/ywc-skill-author/README{,.en,.ja,.ko,.es,.zh}.md`

### Shared Surfaces

- `validate-skill.sh` — `000055-010`이 같은 파일의 추출기를 수리했다 (이전 phase).
- `ywc-skill-author/SKILL.md` / README — `000058-010`(GO 경로)이 A7을 편집했을 수 있다 (이전 phase).
- `.claude/skills/ywc-toolkit-eval/scripts/score.py` — **read-only.** A2/A3 술어의 원본.

### Conflicts With

- `000059-010-refactor-description-word-cap` — 이 task가 켜는 검사의 대상이다. 반드시 `-010` 완료 후.
- `000055-010-refactor-validate-skill-extractor-repair` — 같은 `validate-skill.sh`. 이전 phase이므로 순차.

### Parallelizable After

- `000059-010-refactor-description-word-cap`

### Task Verify

- 81단어 fixture → `FAIL: description is 81 words (> 80 word cap)`, exit 1
- 80단어 fixture → PASS (경계 포함)
- `(ywc) Use before ...` fixture → **FAIL** (통합 전에는 통과했다)
- `Do not invoke ...` fixture → **FAIL** (통합 전에는 통과했다)
- 46개 실제 skill 전부 여전히 PASS
- enforcement 모드가 report의 증거 게이트 결과와 일치한다
- 6개 README가 **같은 커밋**에 포함 (AC16)
