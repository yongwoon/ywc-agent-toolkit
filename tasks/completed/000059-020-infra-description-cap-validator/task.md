# 000059-020-infra-description-cap-validator — Implementation Checklist

## Prerequisites

- [ ] `000059-010-refactor-description-word-cap` 이 완료·merge되었고, 46개 description이 **이미 전부 80단어 이하**다 (보고된 finding 제외).
- [ ] `000055-010`의 수리된 추출기가 merge되어 있다.
- [ ] `000055-030`의 README drift 수정이 merge되어 있다.
- [ ] `score.py:286-287`의 A2/A3 술어를 직접 읽었다.
- [ ] `docs/ywc-plans/prune-report-rationalization-defense.md`의 증거 게이트 결과(GO / NO-GO / INCONCLUSIVE)를 확인했다 — **enforcement 모드를 결정한다.**

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh`
- [ ] `claude-code/skills/ywc-skill-author/SKILL.md` — A15 규칙만
- [ ] `claude-code/skills/ywc-skill-author/README{,.en,.ja,.ko,.es,.zh}.md`
- [ ] `.claude/skills/ywc-toolkit-eval/**` 는 **읽기 전용**이다 (Critical Surface).

## Stop Conditions

- [ ] 46개 중 하나라도 80단어를 초과한 상태에서 hard-fail 검사를 켜려 하면 **멈춘다** — `000059-010`으로 돌아간다.
- [ ] 증거 게이트가 통과하지 않았는데 hard-fail로 켜려 하면 멈춘다 — 부모 spec `:45-47`이 advisory를 요구한다.
- [ ] `score.py`를 수정해야 통합이 된다고 느끼면 멈춘다 — **방향이 반대다.** 로컬 validator가 `score.py`로 이동한다.
- [ ] `validate-skill.sh`에 `set -e`를 추가하고 싶어지면 멈춘다 — `fail()` accumulator가 깨진다.

## Implementation Steps

- [ ] report에서 증거 게이트 결과를 읽고 **enforcement 모드**를 확정한다:
  - GO → 검사를 **hard-fail** (exit 1)
  - NO-GO / INCONCLUSIVE → **advisory** (경고 출력, exit 0)
- [ ] **A2 통합**: `validate-skill.sh`의 opener 검사를 substring `"(ywc) Use "` 에서 **`(ywc) Use when` 으로 시작**하는지로 바꾼다 (`score.py:286`과 동일).
- [ ] **A3 통합**: anti-trigger 검사를 `Do not use (for|during|when|in)` 로 바꾼다. **`Do not invoke` 허용을 제거한다** (`score.py:287`과 동일).
- [ ] **상한 검사 추가**: 수리된 추출기(`000055-010`)를 **재사용**한다 — 두 번째 parser를 만들지 않는다. `> 80` 일 때만 `FAIL: description is <N> words (> 80 word cap)`. 단어 세기는 locale 비의존.
- [ ] 새 검사들이 `set -uo pipefail`(`-e` 없음) 환경의 `fail()` accumulator 패턴을 따르는지 확인한다.
- [ ] `ywc-skill-author/SKILL.md`에 규칙 **A15**(description ≤ 80단어)를 추가한다.
- [ ] AC16: 6개 locale README의 rule 범위를 A15까지로 **같은 커밋에서** 갱신한다.
- [ ] `wc -l claude-code/skills/ywc-skill-author/SKILL.md` ≤ 500 (A8) 확인.

## Task Verify

- [ ] `for d in claude-code/skills/ywc-*/; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh "$d" || echo "FAILED: $d"; done` → `FAILED:` 없음 (46/46 통과)
- [ ] 81단어 fixture → `FAIL: description is 81 words (> 80 word cap)`, exit 1
- [ ] 80단어 fixture → PASS
- [ ] `(ywc) Use before ...` fixture → FAIL (통합 전에는 통과했던 케이스)
- [ ] `Do not invoke ...` fixture → FAIL (통합 전에는 통과했던 케이스)
- [ ] enforcement 모드가 report의 게이트 결과와 일치한다
- [ ] `git show --stat HEAD` 에 6개 README가 모두 포함 (AC16)
- [ ] `.claude/skills/ywc-toolkit-eval/` 아래 변경 0건

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` → regression 0건 (AC13).
- [ ] `test "$(wc -l < claude-code/skills/ywc-skill-author/SKILL.md)" -le 500` (A8)
- [ ] `ls claude-code/skills/ | grep -E 'ywc-skill-(prune|audit)'` → 결과 없음 (AC1)
- [ ] `git diff`에 RD 섹션 삭제 줄 0건 (AC2).
