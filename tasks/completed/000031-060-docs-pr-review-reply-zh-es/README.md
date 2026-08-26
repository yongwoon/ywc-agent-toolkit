# 000031-060-docs-pr-review-reply-zh-es

## Purpose

Codex `ywc-handle-pr-reviews`가 reviewer comment language matching rule에서 Chinese와 Spanish 예시를 명시하도록 갱신합니다. 기본 원칙은 그대로 유지합니다: reply는 original comment language를 따르고, code suggestions나 command output은 번역하지 않습니다.

## Scope

- `codex/skills/ywc-handle-pr-reviews/SKILL.md`의 Reply language rule을 Korean/English 예시에서 Korean/English/Japanese/Chinese/Spanish 예시로 확장합니다.
- README locale set, `agents/openai.yaml`, `evals/evals.json`을 갱신합니다.
- Reply language eval fixture를 추가합니다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ywc-handle-pr-reviews` — review reply language 요구사항.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ac6---review-replies-support-zhes-examples` — Acceptance Criteria.

### Summary

이 task는 PR review handler의 reply language guidance만 다룹니다. Original reviewer comment가 Chinese면 Chinese로, Spanish면 Spanish로 답합니다. Quoted reviewer text, code, file path, API name, command output은 원문 또는 English machine syntax를 유지합니다.

### Out of Scope (from spec)

- PR health artifact retrieval, CI status checks, merge-readiness logic 변경.
- PR title/body language — `000031-040`, `000031-050`.
- Plugin mirror 직접 수정 — `000032-010`.

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000032-010-infra-codex-plugin-sync-validation` — final sync/validation.

## Key Files

- `codex/skills/ywc-handle-pr-reviews/SKILL.md`
- `codex/skills/ywc-handle-pr-reviews/README.md`
- `codex/skills/ywc-handle-pr-reviews/README.en.md`
- `codex/skills/ywc-handle-pr-reviews/README.ja.md`
- `codex/skills/ywc-handle-pr-reviews/README.ko.md`
- `codex/skills/ywc-handle-pr-reviews/README.zh.md`
- `codex/skills/ywc-handle-pr-reviews/README.es.md`
- `codex/skills/ywc-handle-pr-reviews/agents/openai.yaml`
- `codex/skills/ywc-handle-pr-reviews/evals/evals.json`

## Notes

- Reply language matching은 finite language enum이 아니라 original comment matching rule입니다. zh/es는 examples로 first-class coverage를 추가합니다.
- Review artifact scripts는 변경하지 않습니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only / skill-definition maintenance. Eval JSON validation과 targeted grep으로 대체합니다.

### Interface Contract

- Contract: Reply language matches original reviewer comment language.
- Inputs: reviewer comment/review artifact.
- Outputs: reply body in same natural language, with code/machine text unchanged.
- Error model: mixed-language comment는 dominant/comment language를 따르고 quoted code는 번역하지 않습니다.
- Impacted tests: `codex/skills/ywc-handle-pr-reviews/evals/evals.json`

### Critical Surface Review

- Review requirement: N/A.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-handle-pr-reviews/**`

### Shared Surfaces

- PR review reply language guidance
- `codex/skills/ywc-handle-pr-reviews/evals/evals.json`

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `python3 -m json.tool codex/skills/ywc-handle-pr-reviews/evals/evals.json >/dev/null`
- `rg -n "Reply language|Chinese|Spanish|中文|Español" codex/skills/ywc-handle-pr-reviews`
- `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Out of Scope

- `scripts/fetch-pr-review-artifacts.sh` behavior.
- CI/merge-readiness handling.
- PR title/body language.
