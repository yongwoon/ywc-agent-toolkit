# 000040-010-docs-codex-language-resolution-reference

## Purpose

Codex `ywc-*` skill 이 공통으로 읽을 language resolution reference 를 만든다. 이후 task 들은 이 reference 를 source of truth 로 삼아 `--lang`, project config, project guidance, user config, ask-user 순서를 동일하게 적용한다.

## Scope

- `codex/skills/references/language-resolution.md` 신규 작성.
- precedence, config shape, supported code, alias normalization, invalid config fallback, machine-facing English policy를 문서화.
- session default 제외 정책을 명시.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-ywc-language-setup.md` — Purpose, Scope, FR-4, Data Model, Edge Cases.

### Summary

이번 feature 의 핵심은 language resolution 을 각 skill 내부 prose 에 중복하지 않고 하나의 shared reference 로 모으는 것이다. Reference 는 `explicit --lang > .codex/ywc.json > AGENTS.md/CODEX.md/CLAUDE.md > ~/.codex/ywc.json > ask user` 순서를 정의하고, skill-level default 가 없음을 분명히 해야 한다. Malformed JSON 또는 unsupported `lang` 은 hard failure 가 아니라 다음 tier 로 fallback 된다.

### Out of Scope (from spec)

- `ywc-setup` skill 작성 — `000041-010-docs-codex-ywc-setup-skill`.
- 기존 consumer skill wiring — `000041-020-docs-wire-artifact-language-consumers`, `000041-030-docs-wire-pr-orchestration-consumers`.
- Catalog/root 문서 갱신 — `000041-040-docs-catalog-language-setup`.

## Dependencies

### Depends On

- (None — root foundation task)

### Depended By

- `000041-010-docs-codex-ywc-setup-skill` — 새 skill 이 reference 를 link.
- `000041-020-docs-wire-artifact-language-consumers` — artifact 생성 skill 들이 reference 를 link.
- `000041-030-docs-wire-pr-orchestration-consumers` — PR/orchestration skill 들이 reference 를 link.
- `000041-040-docs-catalog-language-setup` — catalog 문서가 resolution order 를 요약.
- `000042-010-infra-codex-language-setup-validation` — 최종 validation 대상.

## Key Files

- `codex/skills/references/language-resolution.md` — 신규 shared reference.

## Notes

- Config file 에는 canonical code 만 저장한다: `ko`, `ja`, `en`, `zh`, `es`.
- `kr`은 기존 `ywc-project-docs` 호환 alias 로만 허용할 수 있고, config 저장값은 `ko`로 normalize 한다.
- `zh`는 사용자가 별도 locale 을 명시하지 않는 한 Simplified Chinese 로 취급한다.
- Session default 저장 파일은 만들지 않는다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only shared reference; verification is targeted grep plus full repository validation in `000042-010`.

### Interface Contract

- Contract: `codex/skills/references/language-resolution.md`
- Inputs: explicit language flags, `.codex/ywc.json`, project guidance, `~/.codex/ywc.json`
- Outputs: resolved canonical language code or ask-user requirement
- Error model: malformed config tier is ignored with optional warning, then next tier is checked
- Impacted tests: `bash scripts/validate.sh`, targeted `rg`

### Critical Surface Review

- Review requirement: N/A — docs-only skill contract.

### Data Integrity Hardening

- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata

### Ownership

- `codex/skills/references/language-resolution.md`

### Shared Surfaces

- Shared Codex reference contract: language resolution.

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `test -f codex/skills/references/language-resolution.md`
- `grep -q ".codex/ywc.json" codex/skills/references/language-resolution.md`
- `grep -q "~/.codex/ywc.json" codex/skills/references/language-resolution.md`
- `grep -q "no skill-level" codex/skills/references/language-resolution.md || grep -q "skill-level default" codex/skills/references/language-resolution.md`

## Out of Scope

- Editing any `codex/skills/ywc-*/SKILL.md`.
- Adding `ywc-setup`.
- Running generated plugin sync.
