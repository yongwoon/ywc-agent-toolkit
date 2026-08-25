# 000058-010-infra-retire-a7-quota

> **조건부 task.** `000057-020`의 증거 게이트(AC9)가 **통과한 경우에만** 실행한다. 게이트가 실패했거나 run이 `INCONCLUSIVE`면 이 task는 실행하지 않고 `000058-020` (NO-GO 종결)로 간다.

## Purpose

A7의 "≥5 Excuse/Reality 행" 수치 하한을 **다섯 사본 전부에서 함께** 제거한다. `## Rationalization Defense` **섹션 자체는 모든 곳에서 의무로 남는다** — 사라지는 것은 숫자 하한뿐이며, "관측된 실패 모드만, 하한 없음"으로 대체된다.

## Scope

다섯 사본이 **한 변경으로 함께 떨어지거나, 아무것도 떨어지지 않는다** (AC10):

1. `claude-code/skills/ywc-skill-author/SKILL.md:54` — canonical prose 사본 (rule A7)
2. `claude-code/skills/CLAUDE.md:84-85` — 두 번째 prose 사본
3. `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md:42` — 세 번째 prose 사본
4. `.claude/skills/ywc-toolkit-eval/scripts/score.py:290` — **실제로 무는 사본** (CI 게이트)
5. `.claude/skills/ywc-toolkit-eval/scripts/test_score.py:112, 123-130` — 게이트를 단언하는 단위 테스트

추가로: `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` baseline 재생성 + 커밋, 그리고 AC16에 따라 `ywc-skill-author`의 6개 locale README를 **같은 커밋에서** 갱신.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-4-conditionally-retire-the-a7-quota`
- `docs/ywc-plans/skill-pruning-pilot.md` AC9 (증거 게이트), AC10 (다섯 사본), AC13 (양쪽 게이트), AC16 (README 동일 커밋)
- `docs/ywc-plans/skill-pruning-pilot.md#critical-surfaces`
- `docs/ywc-plans/prune-report-rationalization-defense.md` (`000057-020` 산출물 — GO 판정의 근거)

### Summary

**이것이 실제로 무는 사본이다.** `score.py:290`의 `"A7_rationalization": _rationalization_data_rows(body) >= 5`가 quota를 기계적으로 강제한다. `.github/workflows/validate.yml:37`이 `score.py --ci`를 돌려 모든 axis를 커밋된 baseline `evals/history.mechanical.json`과 대조하고 **어떤 점수 하락에도 build를 실패시킨다**. 행 하나가 5 아래로 떨어지면 이 검사가 `False`로 뒤집혀 그 skill의 `s2` 점수가 떨어지고 CI가 regression으로 실패한다.

**`score.py:290`만 고치면 테스트 스위트가 깨진다.** `test_score.py:112, 123-130`이 4행에서 `assertFalse(rows >= 5)`, 5행에서 `assertTrue`를 단언한다.

**`bash scripts/validate.sh`는 이 scorer를 절대 실행하지 않는다.** `scripts/validate.sh:579-590, 691-694`는 codex-local eval tool만 다루며, `.claude/skills/ywc-toolkit-eval`을 아예 참조하지 않는다(grep 0건). 따라서 이 변경의 유일한 로컬 검증은 `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`이며, 그것을 빠뜨린 것이 이 spec의 이전 초안이 스스로에게 거짓 확신을 준 방식이다.

**`_rationalization_data_rows()`는 남긴다.** 사라지는 것은 `:290`의 `>= 5` 판정이지 행을 세는 canonical counter가 아니다. `enumerate-rd-rows.sh`의 parity 계약이 그 함수에 걸려 있다.

### Out of Scope (from spec)

- **어떤 RD 행도 삭제하지 않는다** (AC2). 이 task는 규칙을 바꿀 뿐, 행을 지우지 않는다. 실제 pruning은 이 spec 하류의 별개 human-reviewed 변경이다.
- `## Rationalization Defense` 섹션의 **의무화** 자체를 없애는 것 (섹션은 남는다)
- `codex/skills/ywc-skill-author/SKILL.md:58`, `plugins/ywc-agent-toolkit/skills/ywc-skill-author/SKILL.md:58` — 두 out-of-scope prose 사본. `plugins/`는 `codex/skills/`에서만 생성되므로(`scripts/sync-codex-plugin.sh:5`) claude-code 전용 변경은 parity 검사를 깨뜨릴 수 없음이 증명되어 있다.

## Criticality

**`critical`** — 사양이 `.claude/skills/ywc-toolkit-eval/**`를 Critical Surface로 명시적으로 선언한다. `score.py:290`, `test_score.py`, `history.mechanical.json` baseline을 수정하는 것은 **번들 내 46개 skill 전체의 CI 게이트**를 바꾼다. 여기서 잘못된 편집은 저장소 전체의 품질 강제를 조용히 약화시키거나 깨뜨리며, `bash scripts/validate.sh`는 그것을 잡지 못한다(이 scorer를 실행하지 않는다).

- 이 task는 **gray-box 위임 금지**다.
- AC13의 `score.py --ci` 실행이 **필수 증거**다.

## Dependencies

### Depends On

- `000057-020-test-pilot-dispatch-report` — **증거 게이트(AC9) 통과가 이 task의 존재 조건이다.** GO 판정 없이는 실행하지 않는다.
- `000055-030-docs-skill-author-readme-drift-sync` — 깨끗한 README baseline 위에서 A7 변경만 반영한다.

### Depended By

- (없음 — 하류 pruning은 이 spec 밖의 별개 변경이다.)

## Key Files

- `claude-code/skills/ywc-skill-author/SKILL.md` (A7)
- `claude-code/skills/CLAUDE.md`
- `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md`
- `.claude/skills/ywc-toolkit-eval/scripts/score.py`
- `.claude/skills/ywc-toolkit-eval/scripts/test_score.py`
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (재생성)
- `claude-code/skills/ywc-skill-author/README{,.en,.ja,.ko,.es,.zh}.md` (AC16 — 같은 커밋)

## Notes

- **다섯 사본은 원자적이다.** 하나만 바꾸고 나머지를 미루면 CI가 깨지거나(score.py만) 문서가 거짓말을 하거나(prose만) 테스트가 깨진다(score.py + prose, test 누락).
- baseline 재생성은 `validate.yml:33-34`의 절차를 따른다. 재생성된 `history.mechanical.json`은 **같은 커밋에** 포함한다.
- 관찰식(AC10): 다섯 파일에 대해 `grep -rn "at least 5\|≥5 data rows\|>= 5"`가 **A7 문맥에서** 매칭 0건. 동시에 `## Rationalization Defense`는 다섯 곳 모두에서 여전히 **의무 섹션**이다.

## Out of Scope

- RD 행 삭제
- `invocation:` tier (000059)
- codex / plugins 번들

## Parallel Execution Metadata

### Ownership

- `.claude/skills/ywc-toolkit-eval/scripts/score.py` (A7 판정 줄만)
- `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` (A7 단언만)
- `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md`
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- `claude-code/skills/CLAUDE.md` (A7 prose 사본)
- `claude-code/skills/ywc-skill-author/SKILL.md` (A7 규칙)
- `claude-code/skills/ywc-skill-author/README{,.en,.ja,.ko,.es,.zh}.md`

### Shared Surfaces

- **`.claude/skills/ywc-toolkit-eval/**` — 46개 skill 전체의 CI 게이트** (Critical Surface).
- `claude-code/skills/CLAUDE.md` — `000055-020`이 script registry를 편집했다 (다른 섹션, 이전 phase).
- `ywc-skill-author/SKILL.md` / README — `000059-040`이 A15/A16으로 다시 편집한다 (다음 phase).
- `_rationalization_data_rows()` — `enumerate-rd-rows.sh`의 parity 계약이 걸려 있다. **이 함수는 건드리지 않는다.**

### Conflicts With

- `000058-020-docs-a7-nogo-closure` — **상호 배타적.** 정확히 하나만 실행된다.
- `000059-040-infra-invocation-tier-validator` — 같은 `SKILL.md`/README. 다른 phase이므로 순차.

### Parallelizable After

- `000057-020-test-pilot-dispatch-report` (GO 판정 포함)

### Task Verify

- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` → 통과
- `python3 -m pytest .claude/skills/ywc-toolkit-eval/scripts/test_score.py` (또는 프로젝트의 실제 테스트 실행 방식) → 통과
- 다섯 파일에서 A7 문맥의 `>= 5` / "at least 5" / "≥5 data rows" 매칭 0건
- 다섯 파일 모두에서 `## Rationalization Defense`가 여전히 의무 섹션이다
- `_rationalization_data_rows()`가 그대로 존재하고 `enumerate-rd-rows.sh --self-check`가 여전히 `PARITY OK: 46/46`
- 6개 README가 **같은 커밋**에 포함되어 있다 (AC16)
- `git diff`에 RD 섹션 삭제 줄 0건 (AC2)
