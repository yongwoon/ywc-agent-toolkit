# 000053-010-refactor-skill-author-audit-workflow

## Purpose

Claude Code와 Codex의 `ywc-skill-author`를 단일, read-only audit/deletion-test 진입점으로 강화한다. 중복 `ywc-skill-audit`를 추가하지 않고 Skill Hell 위험을 줄인다.

## Scope

- 두 `ywc-skill-author/SKILL.md`에 report-only audit workflow와 deletion-test 절차를 추가한다.
- 두 bundle에 audit rubric, 동일한 `scripts/audit-skills.sh`, role/parity graph 규칙을 추가한다.
- README, Codex `agents/openai.yaml`, Codex eval fixture를 동기화한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-engineering-hardening.md#functional-requirements`
- `docs/ywc-plans/skill-engineering-hardening.md#iteration-1-amendments`
- `claude-code/skills/CLAUDE.md`
- `codex/AGENTS.md`

### Summary

기존 `ywc-skill-author`는 이미 audit trigger를 가진다. 이 task는 mechanical evidence와 model judgment를 분리한 `--audit` workflow를 추가하며, valid audit은 finding 유무와 관계없이 exit 0이다. 두 script copy는 byte-for-byte identical이어야 한다.

### Out of Scope (from spec)

- `ywc-agentic` activation 경계 — `000053-020-refactor-agentic-autonomy-trigger`
- audit 결과 검증과 pruning pilot 추천 — `000054-010-test-skill-audit-validation`
- 다른 long skill의 실제 pruning, agents/hooks/plugins/root validator 변경

## Dependencies

### Depends On

- (None — root)

### Depended By

- `000054-010-test-skill-audit-validation` — audit contract와 graph를 검증한다.

## Key Files

- `claude-code/skills/ywc-skill-author/{SKILL.md,README*.md,references/**,scripts/audit-skills.sh}`
- `codex/skills/ywc-skill-author/{SKILL.md,README*.md,references/**,scripts/audit-skills.sh,evals/**,agents/openai.yaml}`

## Notes

- Fixed CLI: `audit-skills.sh --root <dir> --counterpart-root <dir> [--near-line-cap <1..500>]`.
- Fixed sections: Inventory, Near Line Cap, Unpointed Local References, Force-load References, Declared Sibling Calls, Counterpart Coverage.
- Script finding은 semantic duplicate나 deletion authorization이 아니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: Skill-definition maintenance; runtime code 없음.
- Targeted evidence: script fixture, paired `validate-skill.sh`, `bash scripts/validate.sh`.

### Interface Contract

- Inputs: two existing skill roots and optional threshold.
- Outputs: stable six-section advisory report.
- Error model: invalid input → stderr + exit 2; valid audit → exit 0.
- Impacted tests: task-local script scenarios and repository validator.

### Critical Surface Review

- Review requirement: trigger scope, deletion-test safety, role-matrix exception은 manual full review.

### Data Integrity Hardening

- Trigger surface: N/A — audit is read-only.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-skill-author/**`
- `codex/skills/ywc-skill-author/**`

### Shared Surfaces

- Skill authoring convention, cross-skill graph, repository validator

### Conflicts With

- (None identified; `000053-020` owns `ywc-agentic/**` only.)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `bash claude-code/skills/ywc-skill-author/scripts/audit-skills.sh --root claude-code/skills --counterpart-root codex/skills`
- `bash codex/skills/ywc-skill-author/scripts/audit-skills.sh --root codex/skills --counterpart-root claude-code/skills`
- `cmp -s claude-code/skills/ywc-skill-author/scripts/audit-skills.sh codex/skills/ywc-skill-author/scripts/audit-skills.sh`
- both `validate-skill.sh` commands for `ywc-skill-author`

## Out of Scope

- `ywc-agentic/**`, generated `plugins/**`, automatic deletion, CI failure gates
