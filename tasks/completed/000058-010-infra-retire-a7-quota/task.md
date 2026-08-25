# 000058-010-infra-retire-a7-quota — Implementation Checklist

> **실행 조건**: `000057-020`의 report가 **GO** (AC9 게이트 통과: `p < 0.05` AND Stratum B inert 비율 > Stratum A)를 기록한 경우에만. NO-GO 또는 `INCONCLUSIVE`면 이 task를 실행하지 말고 `000058-020`으로 간다.

## Prerequisites

- [ ] `000057-020-test-pilot-dispatch-report`가 완료·merge되었고, report의 ceiling 판정이 `VALID`다.
- [ ] report가 증거 게이트 **GO**를 명시적으로 기록한다.
- [ ] `000055-030-docs-skill-author-readme-drift-sync`가 merge되어 README baseline이 깨끗하다.
- [ ] **Criticality: critical** — 이 task는 gray-box 위임하지 않는다. 다섯 사본 각각을 직접 읽고 편집한다.

## Allowed Edit Scope

- [ ] AC10의 다섯 파일 + `history.mechanical.json` + `ywc-skill-author`의 6개 README.
- [ ] `_rationalization_data_rows()` (`score.py:379-395`)는 **건드리지 않는다** — `enumerate-rd-rows.sh`의 parity 계약이 걸려 있다.
- [ ] `codex/skills/**`, `plugins/**`는 건드리지 않는다.
- [ ] 어떤 RD 행도 삭제하지 않는다.

## Stop Conditions

- [ ] report가 GO를 기록하지 않았으면 **시작하지 않는다**.
- [ ] `## Rationalization Defense` 섹션의 **의무화 자체**를 없애야 할 것 같으면 멈춘다 — 사라지는 것은 숫자 하한뿐이다.
- [ ] `score.py --ci`가 실패하면 멈춘다. `bash scripts/validate.sh`가 통과했다는 사실은 **아무 증거도 되지 않는다** (이 scorer를 실행하지 않는다).
- [ ] 다섯 사본 중 일부만 바꾼 상태로 커밋하려 하면 멈춘다 — AC10은 원자적이다.

## Implementation Steps

- [ ] report에서 GO 판정과 그 근거(per-stratum inert 비율, Fisher p-value)를 확인하고 커밋 메시지에 인용할 수 있게 기록한다.
- [ ] **사본 1** `claude-code/skills/ywc-skill-author/SKILL.md:54` (A7): "at least 5 domain-specific Excuse / Reality pairs"를 "관측된 실패 모드만, 하한 없음"으로 바꾼다. 섹션은 의무로 남긴다.
- [ ] **사본 2** `claude-code/skills/CLAUDE.md:84-85`: 같은 취지로 수정.
- [ ] **사본 3** `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md:42`: `≥5 data rows` 요구를 제거하되 섹션 존재 요구는 남긴다.
- [ ] **사본 4** `.claude/skills/ywc-toolkit-eval/scripts/score.py:290`: `"A7_rationalization": _rationalization_data_rows(body) >= 5` 를 섹션 **존재** 검사로 바꾼다. `_rationalization_data_rows()` 함수 자체는 그대로 둔다.
- [ ] **사본 5** `.claude/skills/ywc-toolkit-eval/scripts/test_score.py:112, 123-130`: 4행 `assertFalse` / 5행 `assertTrue` 단언을 새 계약에 맞게 고친다.
- [ ] `validate.yml:33-34`의 절차대로 `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` baseline을 재생성한다.
- [ ] `ywc-skill-author`의 6개 locale README에서 A7 서술을 갱신한다 (AC16 — **같은 커밋**).
- [ ] 위 전부를 **하나의 커밋**으로 만든다.

## Task Verify

- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` → 통과 **(필수 증거)**
- [ ] `test_score.py` 스위트 통과
- [ ] `grep -rn "at least 5\|≥5 data rows\|>= 5" claude-code/skills/ywc-skill-author/SKILL.md claude-code/skills/CLAUDE.md .claude/skills/ywc-toolkit-eval/references/skill-rubric.md .claude/skills/ywc-toolkit-eval/scripts/score.py .claude/skills/ywc-toolkit-eval/scripts/test_score.py` → A7 문맥 매칭 0건
- [ ] `grep -rn '## Rationalization Defense' <같은 다섯 파일>` → 섹션이 여전히 의무로 기술되어 있다
- [ ] `bash claude-code/skills/ywc-skill-author/scripts/enumerate-rd-rows.sh --self-check` → `PARITY OK: 46/46` (counter 불변 확인)
- [ ] `git show --stat HEAD`에 6개 README가 모두 포함되어 있다 (AC16)

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (AC13).
- [ ] `for d in claude-code/skills/ywc-*/; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh "$d" || echo "FAILED: $d"; done` → `FAILED:` 없음.
- [ ] `git diff <base>..HEAD -- 'claude-code/skills/ywc-*/SKILL.md'`의 `^-` 삭제 줄 중 Rationalization Defense 섹션 안쪽에 떨어지는 것이 **0개** (AC2).
- [ ] `codex/` 와 `plugins/` 아래 변경 0건.
