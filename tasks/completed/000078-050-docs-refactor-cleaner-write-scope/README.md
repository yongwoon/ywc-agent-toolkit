# 000078-050-docs-refactor-cleaner-write-scope

## Purpose

`ywc-refactor-cleaner` agent의 `Write` tool 사용 범위를 Mission / Boundaries / Anti-patterns 세 곳에 명문화한다. grant 자체는 제거하지 않고 **사용 범위만 좁힌다** — 삭제는 `Edit` 전용이고 `Write`의 유일한 정당 용도는 parent artifact directory 아래의 evidence 파일이다.

## Scope

- FR-5: Mission 1문장 추가, Boundaries "Will NOT" 항목 1개 추가(`DONE_WITH_CONCERNS` 포함), Anti-patterns 표 1행 추가.
- frontmatter `tools:` 행(`:19`)은 **무변경**. `permissionMode` 는 추가하지 않는다.
- 6개 필수 section(Mission / Triggers / Boundaries / Success Criteria / Return Contract / Anti-patterns)의 존재와 순서를 유지한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#fr-5-ywc-refactor-cleaner-의-write-사용-범위-명문화`
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md` — AC12 (문구 요구사항), AC13 (6 section 유지)
- `claude-code/agents/ywc-refactor-cleaner.md` — `:19` tools, `:29` Mission, `:45` Boundaries, `:118-128` Anti-patterns

### Summary

`ywc-refactor-cleaner`는 `tools: [Read, Write, Edit, Bash, Grep, Glob]` grant를 갖는데, Mission(`:29`)은 삭제를 "surgical removal via the `Edit` tool with no adjacent re-formatting"으로 규정하므로 `Write`가 삭제 경로에 쓰일 이유가 없다. 그럼에도 Boundaries의 "Will NOT" 8개 항목 중 `Write` 관련 항목만 **부재**하다. grant 제거는 불가능하다 — Anti-patterns(`:128`)가 "Write the commit list + per-item evidence to a file under the parent's artifact directory"를 계약 요구사항으로 두기 때문이며, spec은 grant 제거안을 검토 후 기각했다. 따라서 grant는 유지하고 사용 범위만 세 곳에 명문화한다.

### Out of Scope (from spec)

- frontmatter `tools:` 행(`:19`) 수정 — AC12에 의해 무변경.
- `permissionMode` 추가 — Coder tier에 부적합.
- `Write` grant 제거 — Anti-patterns(`:128`)의 파일 산출 계약 요구사항과 충돌하므로 기각됨.
- Return Contract의 inline 재정의 — AC13에 의해 참조만 유지한다.
- 다른 agent 파일 수정.

## Criticality

`normal` — agent의 prompt 문서만 수정하며, 변경 방향은 `Write` 사용 범위를 **좁히는** 쪽이다 (spec §Critical Surfaces).

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000079-010-infra-context-safety-validation` — AC12, AC13 검증 대상

## Key Files

- `claude-code/agents/ywc-refactor-cleaner.md` — Mission 1문장, Boundaries "Will NOT" 1항목, Anti-patterns 1행 추가

## Notes

- **AC12의 문구에 `DONE_WITH_CONCERNS` 단어가 필수다.** Boundaries 항목의 취지: "does NOT use `Write` for production source or any file outside the parent's artifact directory; if such a need arises, return `DONE_WITH_CONCERNS` to the parent instead."
- Mission 추가 문장은 두 가지를 동시에 말해야 한다 — (a) 삭제는 `Edit` 전용, (b) `Write` 의 유일한 정당 용도는 parent artifact directory 아래의 per-item evidence 파일.
- Anti-patterns 추가 행의 내용: "삭제 대신 `Write` 로 파일을 통째로 재작성" → 사유는 bisect 대상 오염 + Mission의 Edit-only 규정 위반, 대체 행동은 `Edit` 기반 surgical 삭제.
- **Edge case**: parent가 evidence 파일을 쓸 artifact directory를 지정하지 않으면 기존 `NEEDS_CONTEXT` 경로로 반환한다. `Write` 범위 제한 때문에 임의 경로를 고르지 않는다.
- `scripts/validate.sh:524,529`가 agent frontmatter의 `name:` / `description:` 을 강제하므로 frontmatter 구조를 깨지 않도록 주의한다.
- 이 task는 다른 4개 task와 완전히 독립적이며 root에서 바로 실행 가능하다.
- 본문 편집은 **영문**이다.

## Parallel Execution Metadata

### Ownership

- `claude-code/agents/ywc-refactor-cleaner.md`

### Shared Surfaces

- agent frontmatter validator (`scripts/validate.sh:524,529`) — `name:` / `description:` 필수
- `claude-code/skills/references/subagent-status-actions.md` — Return Contract가 참조하는 status set. **읽기 전용**이며 inline 재정의하지 않는다
- CI gates: `scripts/validate.sh`, `markdownlint.yml`, `score.py --ci`

### Conflicts With

- (None identified) — 유일하게 `claude-code/agents/**` 를 소유하는 task

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `grep -c "DONE_WITH_CONCERNS" claude-code/agents/ywc-refactor-cleaner.md` — 변경 전보다 증가
- `git diff -- claude-code/agents/ywc-refactor-cleaner.md | grep -c "^[+-]tools:"` — **0** (`:19` 무변경, AC12)
- `grep -nE "^## (Mission|Triggers|Boundaries|Success Criteria|Return Contract|Anti-patterns)" claude-code/agents/ywc-refactor-cleaner.md` — 6개가 원래 순서대로 존재 (AC13)
- `grep -c "permissionMode" claude-code/agents/ywc-refactor-cleaner.md` — **0**

## Out of Scope

- 어떤 skill 파일 수정도 포함하지 않는다.
- 다른 agent(`claude-code/agents/ywc-*.md`) 수정.
- `Write` grant 제거 또는 `tools:` 행 변경.
- `codex/**` 하위 모든 파일 (AC17).
- mechanical score baseline 재생성 — `000079-010`이 담당.
