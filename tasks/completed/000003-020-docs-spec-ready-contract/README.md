# 000003-020-docs-spec-ready-contract

## Purpose

PR #120의 Codex spec-readiness workflow를 추가한다. 이 task는 `ywc-spec-ready` 신규 package, `ywc-spec-validate --advisor-budget` contract, 그리고 `ywc-agentic`의 Codex-native wording/status-routing 보강을 한 vertical slice로 처리한다.

## Scope

- `codex/skills/ywc-spec-ready/` 신규 생성
- `codex/skills/ywc-spec-validate/SKILL.md` 및 README locale set에 advisor budget contract 추가
- `codex/skills/ywc-agentic/SKILL.md`에 source PR #120의 compatible wording/status-routing delta 반영
- `ywc-agentic`이 `ywc-spec-ready`를 현재 routing으로 자동 호출하지 않도록 유지

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-pr110-120-129-port.md#fr-3-add-ywc-spec-ready` - 신규 `ywc-spec-ready` behavior
- `docs/ywc-plans/codex-pr110-120-129-port.md#fr-4-update-ywc-spec-validate-advisor-budget-contract` - advisor budget contract
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac5---spec-ready-package-exists` - package acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac7---spec-validate-budget-contract-is-documented` - validate contract acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac8---agentic-is-not-silently-rerouted` - agentic routing guardrail

### Summary

`ywc-spec-ready`는 spec을 task generation 전에 수렴시키는 user-facing skill이다. `ywc-spec-validate`는 반복 loop를 직접 소유하지 않고 advisor budget과 machine-readable budget status를 제공한다. `ywc-agentic`은 Codex wording/status routing 개선만 반영하고 `ywc-spec-ready` 자동 routing은 별도 Phase 2 spec 전까지 적용하지 않는다.

### Out of Scope (from spec)

- Docker isolation - handled by `000003-010-infra-docker-isolate-package` and `000004-010-infra-parallel-docker-hooks`
- Worktree rollout - handled by `000004-020-infra-worktree-rollout`
- Catalog update와 `.codex-plugin` sync - handled by `000005-010-infra-codex-package-validation`

## Dependencies

### Depends On

- (None - root task)

### Depended By

- `000005-010-infra-codex-package-validation` - final catalog, install smoke, and package sync validate this new skill and changed contract

## Key Files

- `codex/skills/ywc-spec-ready/SKILL.md` - readiness loop skill
- `codex/skills/ywc-spec-ready/README.md` - Korean usage guide
- `codex/skills/ywc-spec-ready/README.en.md` - English source usage guide
- `codex/skills/ywc-spec-ready/README.ja.md` - Japanese usage guide
- `codex/skills/ywc-spec-ready/README.ko.md` - Korean locale usage guide
- `codex/skills/ywc-spec-ready/agents/openai.yaml` - Codex UI metadata
- `codex/skills/ywc-spec-ready/references/convergence.md` - convergence guard reference
- `codex/skills/ywc-spec-ready/references/loop-log.md` - append-only loop log schema
- `codex/skills/ywc-spec-validate/SKILL.md` - advisor budget argument and report contract
- `codex/skills/ywc-spec-validate/README*.md` - user-facing budget documentation
- `codex/skills/ywc-agentic/SKILL.md` - compatible wording/status-routing deltas only

## Notes

- `ywc-spec-ready` must stop by printing `ywc-task-generator <spec-path>`; it must not invoke task generation.
- Generic orchestrators keep max-1 retry behavior in `ywc-spec-validate`; multi-iteration ownership belongs to `ywc-spec-ready`.
- Any `ywc-spec-ready` reference inside `ywc-agentic` must be absent or explicitly marked deferred/follow-up.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-spec-ready/**`
- `codex/skills/ywc-spec-validate/SKILL.md`
- `codex/skills/ywc-spec-validate/README*.md`
- `codex/skills/ywc-agentic/SKILL.md`

### Shared Surfaces

- Codex skill routing and Programmatic Consumer Policy text
- Advisor budget report contract consumed by future orchestrators

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task - no predecessor required)

### Task Verify

- `find codex/skills/ywc-spec-ready -maxdepth 3 -type f | sort`
- `rg -n -- "--advisor-budget|Phase 2 advisor calls used: X of N|Advisor budget status|advisor_budget_status" codex/skills/ywc-spec-validate/SKILL.md`
- `rg -n "ywc-task-generator <spec-path>|DONE_WITH_CONCERNS|convergence" codex/skills/ywc-spec-ready/SKILL.md`
- `rg -n "ywc-spec-ready" codex/skills/ywc-agentic/SKILL.md || true`

## Out of Scope

- Implementing task generation
- Changing `ywc-agentic` execution loop to call `ywc-spec-ready`
- Updating root `CHANGELOG.md`, `VERSION`, or root `plugin.json`
