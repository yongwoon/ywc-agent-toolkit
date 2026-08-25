# 000061-030-docs-auth-implement-catalogs

## Purpose

새 Codex skill을 source catalog에 등록하고, 다섯 root README의 Codex skill count를 live directory count와 일치시킨다.

## Scope

- `codex/skills/README.md`에 `ywc-auth-implement` row를 추가한다.
- `README.md`, `README.ko.md`, `README.ja.md`, `README.zh.md`, `README.es.md`의 Codex skill count만 live value로 갱신한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex_auth_implement_skill.md#fr-9-documentation-and-catalogs` — exact catalog/locale boundary
- `docs/ywc-plans/codex_auth_implement_skill.md#verification` — live-count verification command

### Summary

Count는 spec의 stale number가 아니라 implementation 시점의 `codex/skills/` directory listing으로 계산한다. `README.en.md`를 만들지 않고 `VERSION`과 `CHANGELOG.md`도 수정하지 않는다. Catalog entry는 source skill이 존재한 뒤에만 추가한다.

### Out of Scope (from spec)

- skill artifacts — `000061-010-domain-auth-implement-skill`
- eval fixtures — `000061-020-test-auth-implement-routing-evals`
- plugin synchronization — `000062-010-infra-auth-implement-distribution-validation`

## Dependencies

### Depends On

- `000061-010-domain-auth-implement-skill` — countable directory와 catalog description source

### Depended By

- `000062-010-infra-auth-implement-distribution-validation` — final catalog/count validation

## Key Files

- `codex/skills/README.md` — source skill catalog
- `README.md`, `README.ko.md`, `README.ja.md`, `README.zh.md`, `README.es.md` — live Codex skill count

## Notes

- exact five existing root README만 수정한다.
- count update는 post-addition live count 기록이다.

## Hardening Evidence

### Test Feedback Path

- Named exception: documentation-only change; live-count command is replacement verification.

### Interface Contract

- Contract: published Codex skill inventory count
- Inputs: `find codex/skills -mindepth 1 -maxdepth 1 -type d ! -name references ! -name scripts`
- Outputs: five consistent README count values
- Error model: count mismatch causes spec verification failure
- Impacted tests: `bash scripts/validate.sh`

### Critical Surface Review

- Review requirement: N/A — documentation catalog only

### Data Integrity Hardening

- Trigger surface: N/A — static documentation
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A — recompute count on each run
- Required tests: N/A

## Parallel Execution Metadata

### Ownership

`codex/skills/README.md`, `README.md`, `README.ko.md`, `README.ja.md`, `README.zh.md`, `README.es.md` only.

### Shared Surfaces

Codex skill directory inventory and root translated README catalog data.

### Conflicts With

(None identified) after `000061-010` merges; parallel-safe with `000061-020-test-auth-implement-routing-evals`.

### Parallelizable After

`000061-010-domain-auth-implement-skill` merged.

### Task Verify

- `live_count="$(find codex/skills -mindepth 1 -maxdepth 1 -type d ! -name references ! -name scripts | wc -l | tr -d ' ')"; rg -n "Codex.*${live_count}|Codex\\s*\\|\\s*${live_count}\\b" README.md README.ko.md README.ja.md README.zh.md README.es.md`
- `rg -n 'ywc-auth-implement' codex/skills/README.md`

## Out of Scope

New root README locales, release metadata, skill implementation, and plugin generation.
