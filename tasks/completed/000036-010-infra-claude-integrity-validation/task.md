# Task: 000036-010-infra-claude-integrity-validation

## Prerequisites

- [ ] `000035-010-docs-impl-review-integrity-catalog` 병합 완료
- [ ] `000035-020-docs-spec-task-integrity-guidance` 병합 완료
- [ ] `000035-030-docs-executor-integrity-gates` 병합 완료

## Allowed Edit Scope

- validation 실행 및 보고. source 파일은 Phase `000035`가 유발한 validation 실패를 직접 고칠 때만 접근. `codex/**`·`plugins/**`는 편집 금지.

## Stop Conditions

- `git diff --name-only`에 `codex/**` 또는 `plugins/**` 경로가 나타나면 즉시 멈추고 경계 위반으로 보고한다.
- validation 실패 원인이 이번 batch 변경인지 pre-existing cache/stale인지 구분되지 않으면 추정하지 말고 두 가능성을 함께 보고한다.

## Implementation Steps

- [ ] FR-6 README consistency 확인: 다섯 대상 스킬 중 SKILL.md의 user-facing 요약이 바뀐 스킬에 대해 6 locale README가 일관되게 mirror됐는지 확인.
- [ ] targeted evidence: `rg -n "concurrent write|read . modify . write|partial write|transaction boundary|durable idempotency|concurrency-safe" claude-code/skills/ywc-impl-review claude-code/skills/ywc-spec-validate claude-code/skills/ywc-task-generator claude-code/skills/ywc-sequential-executor claude-code/skills/ywc-parallel-executor` 실행 — 각 FR surface에 최소 1 hit 확인.
- [ ] `rg -n "QA High" claude-code/skills/ywc-impl-review` — hit 없음 확인.
- [ ] `git diff --name-only origin/main...HEAD`(또는 batch 범위)로 변경이 `claude-code/skills/**` + `tasks/**` + `docs/ywc-plans/**`에 국한됐는지 확인 (no `codex/**`, no `plugins/**`).
- [ ] `bash scripts/validate.sh` 실행; 실패 시 원인을 batch-변경 vs cache/stale로 분류해 보고.
- [ ] 변경된 README에 대해 `npx --yes markdownlint-cli2 "claude-code/skills/ywc-impl-review/README*.md" "claude-code/skills/ywc-spec-validate/README*.md" "claude-code/skills/ywc-task-generator/README*.md"` 실행.

## Task Verify

- [ ] `bash scripts/validate.sh` exit 0
- [ ] 위 targeted `rg`가 다섯 스킬 전반에서 hit (FR-1~FR-5 반영 증거)
- [ ] `git diff --name-only`에 `codex/**`·`plugins/**` 없음 (claude-code-only 경계)
- [ ] 변경 README markdownlint 0 error

## Verification

- [ ] `bash scripts/validate.sh` 통과 (AC8)
- [ ] `bash scripts/install.sh --list --cc` — 다섯 스킬 정상 나열
