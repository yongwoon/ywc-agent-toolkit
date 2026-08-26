# 000053-020-refactor-agentic-autonomy-trigger

## Purpose

`ywc-agentic` activation을 명시적인 autonomous end-to-end lifecycle 요청으로 좁혀 일반 plan·단일 변경 요청의 오선택 위험을 낮춘다.

## Scope

- 양 bundle `ywc-agentic/SKILL.md`의 description trigger/anti-trigger를 수정한다.
- activation 설명이 있는 locale README를 동기화한다.
- Codex `agents/openai.yaml`이 넓은 activation promise를 반복하면 갱신한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-engineering-hardening.md#fr-5-reduce-ywc-agentic-activation-breadth`
- `docs/ywc-plans/skill-engineering-hardening.md#acceptance-criteria`
- `claude-code/skills/CLAUDE.md`
- `codex/AGENTS.md`

### Summary

workflow, arguments, downstream routing은 바꾸지 않는다. explicit autonomous lifecycle 요청만 `ywc-agentic`으로, generic planning은 `ywc-plan`으로, ordinary direct change는 implementation workflow로 route한다.

### Out of Scope (from spec)

- `ywc-skill-author` audit workflow — `000053-010-refactor-skill-author-audit-workflow`
- audit/pilot validation — `000054-010-test-skill-audit-validation`
- `ywc-agentic` body workflow/argument 변경

## Dependencies

### Depends On

- (None — root)

### Depended By

- `000054-010-test-skill-audit-validation` — trigger precision을 검증한다.

## Key Files

- `claude-code/skills/ywc-agentic/{SKILL.md,README*.md}`
- `codex/skills/ywc-agentic/{SKILL.md,README*.md,agents/openai.yaml}`

## Notes

- multilingual explicit-autonomy phrases를 유지한다.
- Claude documentation uses `/ywc-*`; Codex documentation uses `$ywc-*`.

## Hardening Evidence

### Test Feedback Path

- Named exception: metadata/documentation behavior change; runtime code 없음.
- Targeted evidence: representative routing prompts, wording grep, structure validator.

### Interface Contract

- Inputs: explicit autonomous lifecycle request.
- Outputs: existing full orchestration only for that input class.
- Error model: generic plan/direct change routes to a sibling skill.
- Impacted tests: prompt-routing review and repository validator.

### Critical Surface Review

- Review requirement: auto-trigger description affects every session; review false positive/negative examples.

### Data Integrity Hardening

- Trigger surface: N/A.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-agentic/**`
- `codex/skills/ywc-agentic/**`

### Shared Surfaces

- discovery descriptions, sibling routing vocabulary, Codex UI metadata

### Conflicts With

- (None identified; `000053-010` owns `ywc-skill-author/**` only.)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `rg -n 'autonomous|end-to-end|Do not use for|ywc-plan' claude-code/skills/ywc-agentic/SKILL.md codex/skills/ywc-agentic/SKILL.md`
- both `validate-skill.sh` commands for `ywc-agentic`

## Out of Scope

- any workflow/body behavior outside activation wording; other skills; plugins/root scripts
