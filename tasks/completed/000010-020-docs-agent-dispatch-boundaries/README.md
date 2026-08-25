# 000010-020-docs-agent-dispatch-boundaries

## Purpose
`ywc-qa-engineer`(FR2)와 `ywc-doc-writer`(FR3)의 dispatch 경계를 명확히 하여 A2 정밀도를 높인다. 각 에이전트의 `Do not use for` 절에 형제명을 명시하고, 충돌을 유발하는 광범위 트리거를 좁힌다.

## Scope
- FR2: `ywc-qa-engineer` 에 `ywc-tdd-ritual` + `ywc-e2e-test-strategy` 를 `Do not use for` 절에 명시, in-scope 문구에서 "E2E suites" 제거
- FR3: `ywc-doc-writer` 의 `Do not use for` 절(라인 10)에 `ywc-project-docs` + `ywc-skill-author` + `ywc-changelog-release-notes` 명시(절 내부), 범용 문서 트리거를 구체 문구로 교체

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-activation-fixes.md` — FR2, FR3, Amendment A2, A8
### Summary
qa-engineer 는 "테스트 작성" 표면을 tdd-ritual/e2e-test-strategy 와 공유하고, doc-writer 는 "문서 작성" 표면을 project-docs 와 공유한다. 형제명을 `Do not use for` 절 **내부**에 두어야 FR6 가 인식한다. doc-writer 의 라인 8(디스패처-컨텍스트 문장)에 일부 형제가 이미 언급되나 절 외부라 무효이며, `ywc-skill-author` 는 description 전체에 부재하므로 신규 추가다(A8).
### Out of Scope (from spec)
- 기계 A3(tool-grant) 점수 변경 — Bash 권한은 테스트 실행에 정당, 산문 노트는 A6 명료성만 개선(점수 불변)
- Codex 미러 — 후속 plan

## Dependencies
### Depends On
- (없음) — Phase 000010 독립 편집 태스크
### Depended By
- `000011-010-infra-rebaseline-rescore` — 재채점으로 A2 개선 확인

## Key Files
- `claude-code/agents/ywc-qa-engineer.md` (frontmatter description)
- `claude-code/agents/ywc-doc-writer.md` (frontmatter description, `Do not use for` 절 :10)

## Notes
- 토큰은 `Do not use for` 절 **내부**(첫 `Do not use for` 이후)에 위치(A2/A8).
- 에이전트 description 에는 A4(다국어) 요구가 없으므로 영문 토큰 추가/문구 제거가 구조 점검을 깨지 않음.
- 스킬 description 의 A4 와 달리 에이전트는 자유로움.

## Out of Scope
- 리뷰어 3종(→ 000010-010), 스킬 description(→ 000010-030)
- history.mechanical.json 재기준선화(→ 000011-010)

## Parallel Execution Metadata
- **Ownership:** `claude-code/agents/ywc-qa-engineer.md`, `claude-code/agents/ywc-doc-writer.md`
- **Shared Surfaces:** project-docs 와 doc-writer 의 경계는 000010-030(FR7, project-docs 쪽)과 의미적으로 짝 — 파일은 비중첩
- **Conflicts With:** (None identified)
- **Parallelizable After:** (없음 — 즉시 실행 가능)
- **Task Verify:**
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --format json` 무오류
  - `grep -c 'ywc-tdd-ritual\|ywc-e2e-test-strategy' claude-code/agents/ywc-qa-engineer.md` ≥ 2, "E2E suites" 부재
  - doc-writer 의 `ywc-skill-author` 가 `Do not use for` 절 이후 구간에 존재
