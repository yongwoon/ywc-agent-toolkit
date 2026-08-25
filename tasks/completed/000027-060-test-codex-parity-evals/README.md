# 000027-060-test-codex-parity-evals

## Purpose
Codex eval fixtures에 PR #140 parity coverage를 추가한다.

## Scope
- `ywc-project-docs/evals/evals.json`에 product routing / cross-reference fixture를 추가한다.
- `ywc-project-scaffold/evals/evals.json`에 Rust + Axum + REST API + Layered Architecture fixture를 추가한다.
- Touched JSON fixture files가 `python3 -m json.tool`로 valid한지 검증한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-7-port-pr-140-codex-active-parity-fixes`
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#ac14---eval-coverage-added`
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#ac15---json-fixtures-remain-valid`

### Summary
이 repository의 Codex evals는 simple `prompt` / `expected_output` schema를 사용한다. 새 fixture는 schema를 바꾸지 않고, expected output이 routing/cross-reference와 Rust Axum scaffold intent를 잡도록 추가해야 한다. Eval harness 자체 migration은 scope 밖이다.

### Out of Scope (from spec)
- Eval harness redesign 또는 schema migration은 scope 밖이다.
- Generated plugin sync는 `000028-010-infra-plugin-sync-validation`에서 처리한다.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000028-010-infra-plugin-sync-validation` — JSON validity와 전체 validation을 최종 확인한다.

## Key Files
- `codex/skills/ywc-project-docs/evals/evals.json`
- `codex/skills/ywc-project-scaffold/evals/evals.json`

## Notes
Keep existing fixture style and indentation. Do not add non-Codex fixture format or external evaluator configuration.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-project-docs/evals/evals.json`
- `codex/skills/ywc-project-scaffold/evals/evals.json`

### Shared Surfaces
- Codex eval fixture schema

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `python3 -m json.tool codex/skills/ywc-project-docs/evals/evals.json >/dev/null`
- `python3 -m json.tool codex/skills/ywc-project-scaffold/evals/evals.json >/dev/null`
- `rg -n "docs/product|cross-reference|Axum|Layered Architecture|Rust" codex/skills/ywc-project-docs/evals/evals.json codex/skills/ywc-project-scaffold/evals/evals.json`

## Out of Scope
- Modifying skill instructions for project docs or scaffold beyond fixture needs
- Changing root CI
