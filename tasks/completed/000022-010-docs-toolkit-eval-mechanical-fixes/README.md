# 000022-010-docs-toolkit-eval-mechanical-fixes

## Purpose

`ywc-toolkit-eval` mechanical tier가 확정한 3건의 배포 스킬 결함(ywc-commit A4, ywc-spec-validate A2, ywc-gen-testcase A8)을 수정하고, 수정 결과를 반영하도록 eval mechanical baseline(`history.mechanical.json`)을 재생성한다. 결과적으로 배포 스킬 40개 전체가 deterministic structure check를 통과하게 만든다.

## Scope

- **FR1** — `ywc-commit` 설명에 일본어 트리거(`コミット` / `コミットして` / `プッシュ`)를 추가하여 A4_multilingual을 통과시킨다.
- **FR2** — `ywc-spec-validate` 설명 도입부를 `(ywc) Use after …` → `(ywc) Use when …` 표준형으로 교정하여 A2_use_when을 통과시킨다.
- **FR3** — `ywc-gen-testcase`의 본문 임베드 테스트시트 템플릿(SKILL.md:244–373)을 `references/testsheet-template.md`로 분리하여 본문을 500줄 이하로 줄이고 A8_body_cap을 통과시킨다.
- **FR4** — FR1–FR3 적용 후 `score.py --ci`를 실행하여 `history.mechanical.json` baseline을 교정된 A2/A4/A8 sub-score로 재생성한다.

## Spec Reference

### Primary Sources
- `plan.md` — 특히 `## Iteration 1 Amendments`(FR1–FR4 + AC1–AC4, 정확한 명령/트리거, FR4 순서 의존성)가 권위 있는 출처다. 상단 **Operative Sections** 포인터가 원본 Implementation Steps의 느슨한 표현보다 Amendment를 우선함을 명시한다.

### Summary
plan.md는 `ywc-toolkit-eval --mode full --target all`의 mechanical tier가 찾은 확정 결함만 다룬다. score.py / test_score.py의 스코어러 버그 수정(false positive 6건 교정 + 테스트 5건)은 이미 커밋(`cfe9670`)된 선행 작업이며 본 태스크 범위가 아니다.

### Out of Scope (from spec)
- judgment tier(S1/S3/S6, A1/A2/A6) 결과 — 세션 한도로 차단되어 데이터 없음(2:20pm Asia/Tokyo 재설정). 별도 사이클에서 재평가.
- mechanical tier가 지적하지 않은 스킬 ("while I'm here" 편집 금지).
- ywc-commit / ywc-spec-validate의 README 산문 수정 — SKILL.md frontmatter `description:`만 변경.

## Dependencies

### Depends On
- (없음) — 선행 스코어러 수정은 이미 커밋됨(`cfe9670`). 본 태스크는 현재 base branch에서 즉시 구현 가능.

### Depended By
- (없음 현재) — judgment tier 재평가 후 추가 백로그가 생기면 별도 배치로 생성.

## Key Files
- `claude-code/skills/ywc-commit/SKILL.md` (frontmatter `description:`)
- `claude-code/skills/ywc-spec-validate/SKILL.md` (frontmatter `description:`)
- `claude-code/skills/ywc-gen-testcase/SKILL.md` (템플릿 블록 → 포인터로 치환)
- `claude-code/skills/ywc-gen-testcase/references/testsheet-template.md` (신규)
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (재생성)

## Notes
- FR4는 반드시 FR1–FR3 적용 **이후** 마지막 단계로 실행한다. 먼저 실행하면 옛 실패 sub-score가 baseline에 고착된다.
- FR3 추출 블록은 inbound anchor가 없는 leaf 템플릿이다 — 치환 후 `grep -n "Single-file template\|testsheet-template" SKILL.md`로 잔여 참조를 확인한다.
- 일본어 트리거는 globally-installed ywc-commit 사본과 동일하게 맞춘다.

## Out of Scope
- 스코어러 코드(score.py / test_score.py) 변경 — 이미 커밋됨.
- es/zh 등 비필수 로케일 README 추가.

## Parallel Execution Metadata
- **Ownership**:
  - `claude-code/skills/ywc-commit/SKILL.md`
  - `claude-code/skills/ywc-spec-validate/SKILL.md`
  - `claude-code/skills/ywc-gen-testcase/SKILL.md`
  - `claude-code/skills/ywc-gen-testcase/references/testsheet-template.md`
  - `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- **Shared Surfaces**: `history.mechanical.json` — CI `--ci` regression gate의 기준 baseline. 동일 파일을 건드리는 다른 배치(예: Codex eval batch 000020–000021)와 동시 실행 시 충돌 가능하나, 그 배치는 `.claude/**`/`claude-code/**`를 hard boundary로 제외하므로 실제 겹침 없음.
- **Conflicts With**: (None identified)
- **Parallelizable After**: 현재 base branch (선행 의존 없음)
- **Task Verify**:
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json` → `ywc-commit.A4_multilingual == true`, `ywc-spec-validate.A2_use_when == true`, `ywc-gen-testcase.A8_body_cap == true`
  - `awk '/^---$/{c++;next} c>=2{n++} END{print n}' claude-code/skills/ywc-gen-testcase/SKILL.md` → ≤ 500
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` → exit 0
  - `cd .claude/skills/ywc-toolkit-eval/scripts && python3 -m unittest test_score` → 20 passed
  - `bash scripts/validate.sh` → pass
