# 000027-040-refactor-agent-context-compaction

## Purpose
Repository onboarding and long-running autonomous workflows가 existing agent-context files와 compaction에 강하게 동작하도록 Codex skill guidance를 보강한다.

## Scope
- `ywc-onboard-repo` Phase 1에 agent-context pre-check를 추가한다.
- `AGENTS.md`, `.cursorrules`, `.cursor/rules/`, `.github/copilot-instructions.md`를 기존 rule source로 읽고 reconcile하도록 한다.
- `ywc-agentic`에 long-run compaction guidance를 추가한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-6-port-pr-134-agent-context-and-long-run-compaction-guidance`

### Summary
Onboarding skill은 새 `AGENTS.md`를 쓰기 전에 이미 존재하는 agent context rules를 읽고 충돌 없이 합쳐야 한다. Agentic long run은 iteration이 쌓이면 전체 transcript를 계속 들고 가기보다 `agentic-log.md`를 durable source로 사용해야 한다. Sequential executor compaction은 `000027-030-refactor-executor-health-sweeps`에서 별도로 처리한다.

### Out of Scope (from spec)
- `ywc-sequential-executor` compaction guidance는 `000027-030-refactor-executor-health-sweeps`에서 처리한다.
- Project docs naming parity와 gen-testcase URL cleanup은 `000027-050-refactor-parity-doc-hygiene`에서 처리한다.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000028-010-infra-plugin-sync-validation` — generated plugin package sync와 validation을 수행한다.

## Key Files
- `codex/skills/ywc-onboard-repo/SKILL.md`
- `codex/skills/ywc-agentic/SKILL.md`

## Notes
Existing agent-context rules must not be contradicted by generated `AGENTS.md`. Compaction guidance should be operational and brief.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-onboard-repo/**`
- `codex/skills/ywc-agentic/**`

### Shared Surfaces
- Repository agent-context file contract
- Long-run autonomous workflow state contract

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `rg -n "AGENTS.md|\\.cursorrules|\\.cursor/rules|copilot-instructions" codex/skills/ywc-onboard-repo/SKILL.md`
- `rg -n "iteration 6|5\\+ iterations|agentic-log.md|one-line iteration" codex/skills/ywc-agentic/SKILL.md`

## Out of Scope
- Editing executor PR lifecycle files
- Writing new generated agent-context files in the target repository
- Generated plugin sync
