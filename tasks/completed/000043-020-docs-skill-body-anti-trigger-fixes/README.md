# 000043-020-docs-skill-body-anti-trigger-fixes

## Purpose

2026-07-06 평가의 S3(행동 효능) 및 설명 anti-trigger 결함 5건을 5개 스킬 SKILL.md에 반영하고, 각 결함이
Codex 미러에도 존재하는 경우 동기화한다. (FR2~FR6 + FR11)

## Scope

- `claude-code/skills/` 5개 SKILL.md 편집: project-docs, project-scaffold, merge-dependabot, product-review, tdd-ritual.
- `codex/skills/` 동일 5개 미러 — 해당 결함이 미러에 존재할 때만 동기화(EC3).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/toolkit-eval-backlog-2026-07-06.md` — FR2~FR6, FR11, EC1, EC3, EC4, §AC5(=OQ2), Existing Constraints Touched 표

### Summary
문서·메타데이터 편집만 수행하며 워크플로우 로직은 재설계하지 않는다. 각 결함은 file:line으로 확정되어 있다.
product-review(FR5)는 근거상 결함이 아닐 수 있어 편집 대신 "비결함 기록"이 허용된다(§AC5, OQ2).

### Out of Scope (from spec)
- 스킬 런타임 로직 재설계, score.py, 에이전트 파일, setup-language 케이스.

## Criticality
`normal` — 스킬 문서/frontmatter 편집. 보안 표면 아님.

## Dependencies
- **Depends On**: (없음).
- **Depended By**: (없음).

## Key Files
- `claude-code/skills/ywc-project-docs/SKILL.md`, `.../ywc-project-scaffold/SKILL.md`,
  `.../ywc-merge-dependabot/SKILL.md`, `.../ywc-product-review/SKILL.md`, `.../ywc-tdd-ritual/SKILL.md`
- 대응 `codex/skills/<동일>/SKILL.md` (diff 있을 때만)

## Notes
- **FR2 (project-docs)**: 설명(:4)에 "Specification 문서는 ywc-spec-writer" 취지 anti-trigger append(EC1: 기존
  트리거 보존, S1 회귀 주의) + 본문(:70-75) reference 로드를 문서 생성 전 필수 Step으로 승격.
- **FR3 (project-scaffold)**: :80 부근 매칭 reference 부재 시 fallback 문장 추가.
- **FR4 (merge-dependabot)**: :30(`@dependabot rebase`)와 :150-162(수동 해결)의 적용 조건 명시("rebase 우선,
  실패 시에만 수동").
- **FR5 (product-review)**: :26 excerpt의 P0/P1/P2가 excuse 문자열 내부에만 존재 → 어휘를 High/Medium/Low로
  통일하거나 "비결함" 기록. (OQ2)
- **FR6 (tdd-ritual)**: :74 `<run the test...>` placeholder를 러너 추론 규칙으로 대체.
- **EC4**: Codex 미러 편집 시 `.githooks/pre-commit`이 `plugins/ywc-agent-toolkit` 동기화를 트리거 — 생성 패키지
  수기 편집 금지, 훅/sync에 위임.

## Out of Scope
- 에이전트 경계 수정(000043-030), setup-language 케이스(000043-010).

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/{ywc-project-docs,ywc-project-scaffold,ywc-merge-dependabot,ywc-product-review,ywc-tdd-ritual}/SKILL.md` + `codex/skills/{동일 5개}/SKILL.md`
- **Shared Surfaces**: Codex 미러 sync gate(`.githooks/pre-commit`, `scripts/validate.sh`)
- **Conflicts With**: (None identified) — 010/030과 파일 미중복
- **Parallelizable After**: (즉시)
- **Task Verify**:
  `bash scripts/validate.sh` exit 0; 각 스킬 `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item <skill> --format json`로 구조 회귀 없음 확인.
