# 000063-010-infra-codex-release-evidence

## Purpose

Codex SDLC v1.1 skill 개선분을 release 가능한 상태로 묶고 validation, smell review, install/sync evidence를 한 번에 정리한다.

## Scope

- validation evidence, smell review evidence, release metadata를 Codex 기준으로 정리한다.
- source skills와 generated plugin 간 sync 절차를 명시하고 검증한다.
- 임시 `CODEX_HOME` 설치 검증으로 배포 전 install contract를 확인한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-m--deterministic-task-input-and-auditable-release-evidence`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-o--codex-release-validation-must-cover-source-and-plugin-parity`

### Summary

최종 release task는 모든 source-side contract가 닫힌 뒤에만 실행된다. 이 단계에서 validator, install, sync, smell review evidence를 남기고 source/plugin parity를 확인해야 한다.

### Out of Scope (from spec)

- 개별 skill 본문 계약 설계와 locale 문서 작성 — Phase 000061/000062 소유.

## Dependencies

### Depends On

- `000062-010-docs-wayfinder-core`
- `000062-020-docs-wayfinder-routing-catalog`
- `000062-030-refactor-task-generator-preview-core`
- `000062-040-docs-task-generator-preview-assets`
- `000062-050-docs-agentic-preview-flow`
- `000062-060-docs-tech-research-persistence`

### Depended By

- None.

## Key Files

- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.release-validation.md`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.smell-review-evidence.md`
- `CHANGELOG.md`
- `VERSION`
- `scripts/validate.sh`
- `scripts/install.sh`
- `scripts/sync-codex-plugin.sh`

## Notes

Generated plugin files under `plugins/ywc-agent-toolkit/skills/` are synchronized outputs only. Manual edits there are forbidden; parity is established by source update plus sync.

## Parallel Execution Metadata

### Ownership

- release evidence docs, install/sync verification, and release metadata touchpoints

### Shared Surfaces

- global validation scripts, changelog/version, plugin sync outputs.

### Conflicts With

- every Phase 000062 task, because release evidence assumes their contracts are settled.

### Parallelizable After

- all Phase 000062 tasks complete

### Task Verify

- `bash scripts/validate.sh`
- `bash scripts/install.sh --list`
- `bash scripts/install.sh --codex ywc-plan`
- `bash scripts/sync-codex-plugin.sh`

## Out of Scope

- further contract redesign after release evidence starts; reopen earlier tasks instead.
