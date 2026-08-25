# 000027-050-refactor-parity-doc-hygiene

## Purpose
Active Codex docs에서 stale skill names와 internal repository URL을 제거하고, `ywc-gen-testcase` Source contract를 explicit range notation으로 정리한다.

## Scope
- Shared `project-docs-structure.md`에서 split skill name인 `ywc-project-docs-ja` / `ywc-project-docs-kr`를 제거한다.
- `ywc-gen-testcase` active docs/examples에서 `legalforce/cas-marketing-on`을 synthetic public example로 교체한다.
- `ywc-gen-testcase/SKILL.md` Source line을 task range와 git range notation이 명확한 형태로 normalize한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-7-port-pr-140-codex-active-parity-fixes`

### Summary
PR #140 parity fixes는 Codex active docs가 실제 bundle structure와 public-safe examples를 반영하도록 만드는 작업이다. `ywc-project-docs`는 unified skill이므로 obsolete split names를 제거해야 한다. `ywc-gen-testcase`는 internal repo URL을 active docs에서 없애고, report Source line에 task range와 git range를 명확히 남겨야 한다.

### Out of Scope (from spec)
- `ywc-spec-validate` Confidence Gate mapping은 `000027-010-refactor-plan-pr-spec-contracts`에서 처리한다.
- Eval fixture 추가는 `000027-060-test-codex-parity-evals`에서 처리한다.
- Historical changelog entries는 active usage example이 아니면 수정하지 않는다.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000028-010-infra-plugin-sync-validation` — generated plugin package sync와 stale pattern scan을 수행한다.

## Key Files
- `codex/skills/references/project-docs-structure.md`
- `codex/skills/ywc-gen-testcase/references/examples.md`
- `codex/skills/ywc-gen-testcase/README*.md`
- `codex/skills/ywc-gen-testcase/SKILL.md`

## Notes
Required README locale set must stay semantically aligned. Existing `README.es.md` or `README.zh.md` should be updated if they contain the stale URL.

## Parallel Execution Metadata

### Ownership
- `codex/skills/references/project-docs-structure.md`
- `codex/skills/ywc-gen-testcase/**`

### Shared Surfaces
- Public example URL policy
- Project docs skill naming reference

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `rg -n "ywc-project-docs-ja|ywc-project-docs-kr" codex/skills/references/project-docs-structure.md`
- `rg -n "legalforce/cas-marketing-on" codex/skills/ywc-gen-testcase`
- `rg -n "task range|git range|Source:" codex/skills/ywc-gen-testcase/SKILL.md`

## Out of Scope
- Generated plugin package edits
- Eval fixture additions
- Historical changelog cleanup
