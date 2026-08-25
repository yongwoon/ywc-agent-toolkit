# Task: 000022-010-docs-toolkit-eval-mechanical-fixes

## Prerequisites
- [ ] 선행 스코어러 수정 커밋(`cfe9670`)이 base branch에 존재하는지 확인 (`git log --oneline | grep cfe9670`).
- [ ] `plan.md`의 `## Iteration 1 Amendments`(FR1–FR4 + AC1–AC4)를 읽었다.

## Allowed Edit Scope
- `claude-code/skills/ywc-commit/SKILL.md`
- `claude-code/skills/ywc-spec-validate/SKILL.md`
- `claude-code/skills/ywc-gen-testcase/SKILL.md`
- `claude-code/skills/ywc-gen-testcase/references/testsheet-template.md` (신규)
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (FR4 단계에서만)
- 그 외 파일 편집 금지. mechanical tier가 지적하지 않은 스킬은 건드리지 않는다.

## Stop Conditions
- score.py가 위 3개 외 스킬에서 신규 structure 실패를 보고하면 멈추고 보고 (범위 밖일 수 있음).
- FR3 추출 후 본문이 여전히 500줄을 초과하면 멈추고 어떤 블록을 추가 분리할지 보고.
- `score.py --ci`가 regression(비-0 exit)을 보고하면 멈추고 어떤 axis가 떨어졌는지 보고.

## Implementation Steps

### FR1 — ywc-commit 일본어 트리거 (A4)
- [ ] `claude-code/skills/ywc-commit/SKILL.md`의 frontmatter `description:`에 일본어 트리거 `コミット`, `コミットして`, `プッシュ`를 기존 한국어/영어 트리거와 나란히 추가한다.
- [ ] `(ywc) Use when` 도입부와 기존 "Do not use for…" 절을 그대로 유지한다.

### FR2 — ywc-spec-validate 표준 도입부 (A2)
- [ ] `claude-code/skills/ywc-spec-validate/SKILL.md`의 `description:` 도입부를 `(ywc) Use after writing a specification …`에서 `(ywc) Use when a specification has been written and before task decomposition, and …`로 교정한다. 의미·트리거·anti-trigger 절은 보존한다.

### FR3 — ywc-gen-testcase 템플릿 추출 (A8)
- [ ] `claude-code/skills/ywc-gen-testcase/references/testsheet-template.md`를 생성하고, SKILL.md:244–373("Single-file template" ~ "Length Management Guidelines") 블록을 그대로 옮긴다.
- [ ] SKILL.md의 해당 블록을 한 줄 Tier-3 포인터로 치환: `See [references/testsheet-template.md](references/testsheet-template.md) for the full single-file/split testsheet template and length-management rules.`
- [ ] `grep -n "Single-file template\|testsheet-template" claude-code/skills/ywc-gen-testcase/SKILL.md`로 잔여 참조가 포인터 한 줄뿐인지 확인한다.

### FR4 — mechanical baseline 재생성 (FR1–FR3 이후)
- [ ] FR1–FR3가 모두 적용된 상태에서 `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`를 실행한다.
- [ ] 재생성된 `history.mechanical.json`에서 ywc-commit/ywc-spec-validate/ywc-gen-testcase의 A4/A2/A8 sub-score가 통과값인지 확인한다.

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json` 결과에서 `ywc-commit.signals.structure_checks.A4_multilingual == true`
- [ ] 같은 결과에서 `ywc-spec-validate.signals.structure_checks.A2_use_when == true`
- [ ] 같은 결과에서 `ywc-gen-testcase.signals.structure_checks.A8_body_cap == true`, 그리고 40개 스킬 전체에 structure 실패 0건
- [ ] `awk '/^---$/{c++;next} c>=2{n++} END{print n}' claude-code/skills/ywc-gen-testcase/SKILL.md` → 500 이하
- [ ] `claude-code/skills/ywc-gen-testcase/references/testsheet-template.md` 존재
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` → exit 0

## Verification
- [ ] `cd .claude/skills/ywc-toolkit-eval/scripts && python3 -m unittest test_score` → 20 passed (스코어러 회귀 없음)
- [ ] `bash scripts/validate.sh` → pass (frontmatter / locale set / shellcheck / --list dry run)
- [ ] (lint/build) 본 레포는 bash/markdown 토킷이라 별도 컴파일 없음 — validate.sh가 CI 미러 역할.
