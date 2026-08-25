# 000027-010-refactor-plan-pr-spec-contracts

## Purpose
`ywc-plan`, `ywc-create-pr`, `ywc-spec-validate`의 핵심 workflow contract를 upstream PR #132/#134/#140 기준으로 맞춘다.

## Scope
- `ywc-plan` Medium/Large spec handoff를 `ywc-spec-ready` opt-in shortcut으로 갱신한다.
- `ywc-create-pr`에 PR 생성 전 mandatory author self-review gate를 추가한다.
- `ywc-spec-validate`에 `--tasks <dir>` cross-artifact validation과 Confidence Gate mapping correction을 추가한다.
- 관련 README locale set에서 user-facing workflow 설명을 맞춘다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-1-port-pr-132-ywc-plan-spec-ready-handoff`
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-4-port-pr-134-create-pr-self-review-gate`
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-5-port-pr-134-spec-validate-cross-artifact-pass`
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-7-port-pr-140-codex-active-parity-fixes`

### Summary
Planning, PR creation, spec validation의 user-facing contract를 먼저 정렬한다. `ywc-plan`은 사용자가 명시적으로 승인한 경우에만 `ywc-spec-ready <path>`를 실행해야 한다. `ywc-create-pr`은 PR 생성 전 작성자가 `git diff <base-branch>...HEAD`를 직접 읽도록 요구한다. `ywc-spec-validate`는 spec과 generated tasks 사이의 coverage/provenance drift를 찾고, Confidence Gate vocabulary를 수정한다.

### Out of Scope (from spec)
- PR health helper와 executor call-site 변경은 `000027-020-refactor-pr-health-handler`, `000027-030-refactor-executor-health-sweeps`에서 처리한다.
- Generated plugin sync는 `000028-010-infra-plugin-sync-validation`에서 처리한다.
- Eval fixture 추가는 `000027-060-test-codex-parity-evals`에서 처리한다.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000028-010-infra-plugin-sync-validation` — source skill 변경을 generated plugin package에 반영하고 전체 validation을 수행한다.

## Key Files
- `codex/skills/ywc-plan/SKILL.md`
- `codex/skills/ywc-plan/README*.md`
- `codex/skills/ywc-create-pr/SKILL.md`
- `codex/skills/ywc-create-pr/README*.md`
- `codex/skills/ywc-spec-validate/SKILL.md`
- `codex/skills/ywc-spec-validate/README*.md`

## Notes
`ywc-spec-validate --advisor-budget`는 이미 존재하므로 중복 port하지 않는다. Codex `SKILL.md` frontmatter는 `name`과 `description`만 유지한다.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-plan/**`
- `codex/skills/ywc-create-pr/**`
- `codex/skills/ywc-spec-validate/**`

### Shared Surfaces
- Skill workflow contract: spec planning -> spec ready -> task generation
- Skill workflow contract: PR creation gate
- Validation report vocabulary: `Critical/Warning/Suggestion`

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `rg -n "ywc-spec-ready|auto-converge|자동 수렴|Did not auto-execute" codex/skills/ywc-plan`
- `rg -n "Author Self-Review Gate|git diff <base-branch>\\.\\.\\.HEAD|does not replace independent" codex/skills/ywc-create-pr`
- `rg -n -- "--tasks <dir>|Cross-Artifact Consistency|Requirement Coverage|Task Provenance|UNCOVERED|ORPHAN" codex/skills/ywc-spec-validate`
- `rg -n "Critical/Warning/Suggestion|DONE_WITH_CONCERNS" codex/skills/ywc-spec-validate/SKILL.md`

## Out of Scope
- PR review artifact retrieval script implementation
- Executor lifecycle updates
- Plugin package sync under `plugins/ywc-agent-toolkit/skills/**`
