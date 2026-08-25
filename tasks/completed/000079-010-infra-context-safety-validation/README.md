# 000079-010-infra-context-safety-validation

## Purpose

Phase `000078`의 5개 task가 모두 merge된 뒤, spec의 17개 Acceptance Criteria 중 구조적 항목을 grep으로 기계 확인하고 CI 3종 gate를 통과시킨다. 필요 시 mechanical score baseline을 재생성한다. 이 batch의 hard gate다.

## Scope

- AC7: call-site-scoped grep으로 impl-review 자동 호출 지점 **정확히 7건** 확인 + `ywc-plan --non-interactive` guard 확인.
- AC12 / AC14 / AC17: refactor-cleaner `DONE_WITH_CONCERNS`, parallel compaction, codex 경로 0건 확인.
- AC2 / AC15: impl-review directive 인용 2종, 12개 README locale 정합 확인.
- AC16: `bash scripts/validate.sh`, markdownlint, `score.py --ci` 통과. 하락 시 diff archive 후 baseline 재생성해 같은 PR에 commit.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#verification-plan`
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#traceability` — AC ↔ FR ↔ Phase 매핑
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#iteration-1-amendments` — AC7 관측 방법과 markdownlint 호출 형태 수정본이 **authoritative**

### Summary

이 change set은 prompt 문서 수정이므로 자동 테스트 harness가 없다. 구조적 항목(AC1/AC2/AC7/AC12/AC14/AC17)은 grep으로 기계 확인하고, 행위적 항목(AC4/AC9)은 각 task의 `test.md` 수동 transcript 확인으로 이미 다뤄졌다. Iteration 1 Amendments의 Critical fix에 따라 AC7의 관측 방법은 **call-site-scoped grep + 명시적 기대 건수**다 — 단순 flag 카운트는 최소 3개 모집단(기존 `ywc-plan` 호출 3건, FR-4가 추가하는 sequential Arguments 행과 External URL 분기, FR-3의 impl-review 호출 7건)을 뒤섞으므로 FR-3의 부재를 탐지할 수 없다. markdownlint도 로컬에서 임의 버전을 pin하지 말고 `.github/workflows/markdownlint.yml:19`의 실제 invocation(unpinned + 생성된 config)을 재현해야 한다 — 다른 config는 false pass와 false failure를 동시에 만든다.

### Out of Scope (from spec)

- 어떤 skill / agent 소스 파일의 수정 — Phase `000078`이 전부 담당한다. 이 task는 검증과 baseline 재생성만 한다.
- 기존 36건의 `§3.5` citation drift 정정.
- `codex/**` 및 `plugins/**` — claude-code 전용 batch이므로 generated plugin sync가 없다.
- `ywc-spec-validate` / `ywc-task-generator` 의 동일 class gap — 범위 밖으로 기록만 되어 있다.

## Criticality

`normal` — 검증 전용 task이며 소스 동작을 바꾸지 않는다. baseline 재생성은 평가 데이터 갱신이다.

## Dependencies

### Depends On

- `000078-010-docs-impl-review-bounded-payload-noninteractive` — AC1/AC2/AC3/AC4/AC5/AC6/AC8/AC15 대상
- `000078-020-docs-sequential-executor-noninteractive` — AC7(2건)/AC9/AC10/AC15 대상
- `000078-030-docs-parallel-executor-flag-compaction` — AC7(2건)/AC14 대상
- `000078-040-docs-code-gen-agentic-propagation` — AC7(3건)/AC11 대상
- `000078-050-docs-refactor-cleaner-write-scope` — AC12/AC13 대상

### Depended By

- (None — final gate)

## Key Files

- `.claude/skills/ywc-toolkit-eval/scripts/history.mechanical.json` — **score 하락 시에만** 재생성. 그 외에는 무변경
- (검증 전용 — 그 외 소스 파일은 수정하지 않는다)

## Notes

- **AC7의 기대 건수는 정확히 7이다.** `[^|]*` bound가 Markdown 표에서 한 열의 `ywc-impl-review` 언급과 다른 열의 `--non-interactive` 언급이 잘못 이어지는 것을 막는다. 7보다 크면 오탐 또는 중복 부착, 작으면 누락이다.
- **guard grep**: `grep -c "ywc-plan --non-interactive" claude-code/skills/ywc-agentic/SKILL.md` 는 **변경 전과 동일**해야 한다. 기존 3건(`:95`, `:97`, `:262`)을 건드리지 않았음을 보증한다.
- **markdownlint는 workflow가 authority다.** 로컬에서 `npx markdownlint-cli2@0.22.1 "claude-code/skills/*/README*.md"` 처럼 버전을 pin하고 다른 glob/config를 쓰면 CI와 다른 규칙이 적용된다. `.github/workflows/markdownlint.yml:19`의 config-and-glob invocation을 재현한다.
- **baseline 재생성 절차**: `score.py --ci` 실패 시 (a) diff를 archive하고 (b) 정당한 변경임을 확인한 뒤 (c) baseline을 재생성해 **같은 PR에 commit**한다.
- `translation-check.yml`은 informational이며 merge를 막지 않는다. 그럼에도 12개 README가 동일한 flag semantics를 서술하는지 육안 대조한다 (AC15).
- 이 batch에는 generated plugin sync가 없다 — `claude-code/`는 plugin package를 갖지 않는다.
- AC4 / AC9의 수동 transcript 확인은 `000078-010/test.md` 와 `000078-020/test.md` 가 담당하며, 이 task는 그 결과가 기록되었는지 확인만 한다.

## Parallel Execution Metadata

### Ownership

- `.claude/skills/ywc-toolkit-eval/scripts/history.mechanical.json` (score 하락 시에만)

### Shared Surfaces

- CI gates: `scripts/validate.sh`, `.github/workflows/markdownlint.yml`, `.github/workflows/validate.yml:32-37` (`score.py --ci`)
- mechanical score baseline — 이 batch에서 이 파일을 쓰는 유일한 task

### Conflicts With

- `000078-010-docs-impl-review-bounded-payload-noninteractive`
- `000078-020-docs-sequential-executor-noninteractive`
- `000078-030-docs-parallel-executor-flag-compaction`
- `000078-040-docs-code-gen-agentic-propagation`
- `000078-050-docs-refactor-cleaner-write-scope`

(전원 — 모든 편집이 merge된 뒤에만 baseline이 유효하다. 미완 상태에서 재생성하면 불완전한 baseline이 남는다.)

### Parallelizable After

- Phase `000078`의 5개 task 전부

### Task Verify

- `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-code-gen/SKILL.md claude-code/skills/ywc-agentic/SKILL.md | wc -l` — **정확히 7**
- `grep -c "ywc-plan --non-interactive" claude-code/skills/ywc-agentic/SKILL.md` — 변경 전과 동일
- `grep -c "Return-payload contract" claude-code/skills/ywc-impl-review/SKILL.md` — ≥ 1
- `grep -c "subagent-status-actions" claude-code/skills/ywc-impl-review/SKILL.md` — ≥ 2
- `grep -ci "compaction" claude-code/skills/ywc-parallel-executor/SKILL.md` — ≥ 1
- `grep -c "DONE_WITH_CONCERNS" claude-code/agents/ywc-refactor-cleaner.md` — 증가 확인
- `git diff --name-only main...HEAD | grep -c '^codex/'` — **0**
- `bash scripts/validate.sh` — exit 0
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` — exit 0

## Out of Scope

- 어떤 skill / agent 소스 파일의 수정. 검증 실패 시 해당 task로 되돌려 보고한다.
- 새 CI workflow 추가 또는 기존 workflow 수정.
- `codex/**` / `plugins/**` — 이 batch에 generated package sync가 없다.
- 기존 `§3.5` citation drift 정정.
