# 000055-030-docs-skill-author-readme-drift-sync — Implementation Checklist

## Prerequisites

- [ ] `000053-010-refactor-skill-author-audit-workflow` is completed and merged.

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-skill-author/README{,.en,.ja,.ko,.es,.zh}.md` 6개 파일만 편집한다.
- [ ] `SKILL.md`는 읽기 전용이다.

## Stop Conditions

- [ ] README를 맞추려면 `SKILL.md`의 규칙을 바꿔야 할 것 같으면 멈춘다 — 방향이 반대다. README가 `SKILL.md`를 따라간다.
- [ ] A7 quota에 대한 서술을 바꾸고 싶어지면 멈춘다. 증거 게이트(AC9)는 아직 실행되지 않았다.

## Implementation Steps

- [ ] `grep -n '^- \*\*A[0-9]' claude-code/skills/ywc-skill-author/SKILL.md` 로 실제 최고 rule ID를 확인한다(사양은 A14라 하지만 `000053-010`이 규칙을 추가했을 수 있다).
- [ ] `ls claude-code/skills/ | grep -c '^ywc-'` 로 실제 skill 수를 확인한다.
- [ ] 6개 README 각각에서 rule 범위 표기("A1–A13" 등)를 실제 최고 ID에 맞춘다.
- [ ] 6개 README 각각에서 skill 수 표기("18개 production ywc-* skill" 등)를 실제 수에 맞춘다.
- [ ] rule 열거가 있는 README의 경우, 누락된 규칙 항목을 `SKILL.md`의 본문에 맞춰 추가한다.
- [ ] 6개 locale이 서로 같은 사실을 말하는지 대조한다 (번역만 다르고 수치는 동일).

## Task Verify

- [ ] `grep -rn 'A1[–-]A1[0-3]' claude-code/skills/ywc-skill-author/README*.md` → 결과 없음 (최고 ID보다 낮게 끝나는 범위가 없다)
- [ ] `grep -rn '18개\|18 production\|18 skills' claude-code/skills/ywc-skill-author/README*.md` → 결과 없음
- [ ] 6개 README 모두 동일한 skill 수를 적는다

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (AC13).
- [ ] `for d in claude-code/skills/ywc-*/; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh "$d" || echo "FAILED: $d"; done` → `FAILED:` 없음.
- [ ] `git diff --name-only`가 6개 README 외의 파일을 보이지 않는다.
