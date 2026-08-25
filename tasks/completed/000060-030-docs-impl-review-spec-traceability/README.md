# 000060-030-docs-impl-review-spec-traceability

## Purpose
`ywc-impl-review`의 `## Output Format`에 `### Spec Traceability` 섹션을 추가한다(FR-4/AC4). 각 Acceptance Criterion을 `Criterion`/`Status`/`Evidence`/`Scope-creep note` 4열 matrix로 제시하고, `--spec`을 optional로 변경하며, 상태 분기(생략=No spec/valid, 공급됐으나 missing=BLOCKED)를 정밀화한다. 기존 5-subagent Phase1/Phase2 산출물을 aggregation만 하며 신규 워커는 추가하지 않는다.

## Scope
- `## Output Format`의 `### Testing (QA)`와 `### Fix Priority` 사이에 `### Spec Traceability` 섹션 추가(~20줄).
- Matrix 4열 + Status 4단계(Implemented/Partial/Missing/Not Verifiable) 정의.
- Evidence 규칙(file:line·named test/output·command output 필수, task 이름·commit 메시지 추론 금지) 명시.
- `Not Verifiable`("AC는 있으나 evidence 없음") vs "No spec available"(spec 부재) 구분 명시.
- `--spec` argument를 required → optional로 변경하고 상태 분기 기술.
- HTML parity(`--format html`)와 `## Confidence Gate`의 Evidence quality 차원 pointer 교차 참조.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` FR-4(line 97), AC4(line 59) — Spec Traceability 요구사항과 observable
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` Edge Cases(line 151) — codex sibling Amendment C와의 6개 계약 정렬 목록
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md` Amendment C — 4단계 Status 용어·anti-inference·`--spec` 분기의 정본(용어 drift 재확인 대상)
- `claude-code/skills/ywc-impl-review/SKILL.md` line 36(`--spec` required), line 44/174(`--format html`), line 169(BLOCKED semantics) — 변경 지점

### Summary
Spec 적합성 리포트를 Output Format에 통합한다. Evidence는 Architecture 서브에이전트의 "Structural Spec Conformance"와 Design 서브에이전트의 "Contract Spec Conformance" 파인딩에서 추출한다(기존 산출물 aggregation, 신규 워커 없음). 핵심 정밀화는 `--spec` 두 분기 구분: **생략**=valid로 간주해 "No spec available"만 출력, **공급됐으나 파일 없음/읽기불가**=BLOCKED(현행 line 169 유지). 두 경우를 혼동하지 않는 것이 codex Amendment C의 요체다. 구현 시 sibling Amendment C 문구가 이후 변경됐는지 한 번 재확인한다.

### Out of Scope (from spec)
- 신규 6번째 impl-review subagent 도입 — FR-4는 aggregate-only(spec Out of Scope line 31).
- 기존 `[P1]`/`[P2]` 마커·severity 기호·5-subagent 구조 변경 — 그대로 유지(FR-4 line 108).
- codex-특유 요소(worker 용어 등) 포팅 — claude-code 체계 유지(Edge Cases line 151).

## Criticality
`normal` — skill prompt 텍스트 변경. 보안·데이터 surface 없음.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- (None — no downstream dependency)

## Key Files
- `claude-code/skills/ywc-impl-review/SKILL.md` — `### Spec Traceability` 섹션 추가, `--spec` argument optional화, 상태 분기 서술

## Notes
- **ywc-skill-author 선행 실행 필수**: body section 추가는 structural edit(typo/link fix 예외 아님).
- **codex sibling 용어 재확인**: 구현 직전 `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md` Amendment C의 6개 계약 문구를 대조해 drift 없음을 확인한다(현재 이미 일치).
- 040(smell-baseline)과 동일 skill이지만 disjoint 파일(이 task는 SKILL.md, 040은 references+agent 파일)이라 병렬 실행 가능.
- Open Question(spec line 165): Spec Traceability가 리포트 길이를 얼마나 늘리는지는 미실측 — 초기 구현 후 관찰, 과도하면 opt-in화 검토(이 task 범위 밖).

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-impl-review/SKILL.md`

### Shared Surfaces
- `Skill 디렉터리 공유: ywc-impl-review/`(040과 같은 skill이나 파일은 disjoint — SKILL.md ↔ references/*.md·agent 파일)

### Conflicts With
- `(None identified)` — 040과 disjoint 파일이므로 병렬 안전.

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `grep -n "Spec Traceability" claude-code/skills/ywc-impl-review/SKILL.md` — Testing (QA)와 Fix Priority 사이 line 반환
- `grep -n "spec" claude-code/skills/ywc-impl-review/SKILL.md | grep -i optional` — `--spec` optional 갱신 확인
- `wc -l claude-code/skills/ywc-impl-review/SKILL.md` — ≤ 500
- `bash scripts/validate.sh` — exit 0

## Out of Scope
- `references/architecture-agent.md`·`design-agent.md`·`code-smell-baseline.md` 편집 — 040 task 소관.
- README locale 파일 변경.
