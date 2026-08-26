# 000061-010-domain-auth-implement-skill

## Purpose

Codex-native `ywc-auth-implement` skill의 source contract를 만든다. application auth를 구현하지 않고 정책·보안·E2E gate를 갖춘 orchestration 경로를 제공한다.

## Scope

- `SKILL.md`, `agents/openai.yaml`, 6개 locale README, focused reference를 작성한다.
- read-only preflight, 9개 정책 인터뷰, dynamic recommendation, 구현·보안·E2E·PR gate 및 status contract를 문서화한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex_auth_implement_skill.md#functional-requirements` — FR-1~FR-8 source of truth
- `docs/ywc-plans/codex_auth_implement_skill.md#acceptance-criteria` — package, routing, safety acceptance criteria
- `codex/skills/ywc-skill-author/SKILL.md` — Codex skill artifact convention

### Summary

새 skill은 application auth code가 아닌 Codex orchestration 문서 묶음이다. established library/service 우선, secret 비노출, existing-auth 선택 gate, audit 뒤 E2E gate, `$ywc-task-generator`의 출력 전용 handoff를 강제해야 한다. 상세 static policy는 reference로 분리하되 workflow와 validation은 `SKILL.md`에 남긴다.

### Out of Scope (from spec)

- routing eval fixture — `000061-020-test-auth-implement-routing-evals`
- catalog/root README/plugin validation — `000061-030-docs-auth-implement-catalogs`, `000062-010-infra-auth-implement-distribution-validation`
- consumer application auth, migration, UI, secret, legal approval — feature 전체 범위 밖

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000061-020-test-auth-implement-routing-evals` — final routing contract를 fixture로 검증한다.
- `000061-030-docs-auth-implement-catalogs` — source skill directory를 catalog에 등록한다.
- `000062-010-infra-auth-implement-distribution-validation` — complete source tree를 plugin으로 동기화한다.

## Key Files

- `codex/skills/ywc-auth-implement/SKILL.md` — activation, workflow, gate, output contract
- `codex/skills/ywc-auth-implement/agents/openai.yaml` — final skill 기반 UI metadata
- `codex/skills/ywc-auth-implement/README*.md` — 6개 locale usage guide
- `codex/skills/ywc-auth-implement/references/*.md` — policy, fallback, security, legal, evidence, workflow detail

## Notes

- `SKILL.md` frontmatter에는 `name`, `description`만 두고 description은 500 Unicode character 이하로 유지한다.
- preflight는 branch와 `.env.example`을 검사·보고만 한다.
- `references/rationalization-evidence.md`는 이 task가 소유하며 eval task는 read-only로 사용한다.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `codex/skills/ywc-auth-implement/evals/evals.json` (후속 `000061-020`)
- Existing coverage: `bash scripts/check-codex-skill-descriptions.sh --paths a-m`

### Interface Contract

- Contract: `ywc-auth-implement` workflow/status output
- Inputs: auth intent, project evidence, approved policy
- Outputs: preflight, policy record, recommendation, gate evidence, one terminal status
- Error model: `DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` transitions
- Impacted tests: `scripts/run-codex-skill-contract-evals.sh`

### Critical Surface Review

- Review requirement: manual full implementation review — auth/security orchestration prompt text

### Data Integrity Hardening

- Trigger surface: N/A — documentation-only skill artifact
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A — preflight is read-only and rerunnable
- Required tests: N/A

## Parallel Execution Metadata

### Ownership

`codex/skills/ywc-auth-implement/SKILL.md`, `agents/openai.yaml`, `README*.md`, `references/**` only; excludes `evals/**`.

### Shared Surfaces

Codex skill description conventions, shared `../references/subagent-status-actions.md` delegation contract, source skill directory count.

### Conflicts With

`000061-020-test-auth-implement-routing-evals` until this task merges.

### Parallelizable After

Immediately; it is the batch root.

### Task Verify

- `test -f codex/skills/ywc-auth-implement/SKILL.md`
- `test -f codex/skills/ywc-auth-implement/agents/openai.yaml`
- `test "$(wc -l < codex/skills/ywc-auth-implement/SKILL.md)" -lt 500`
- `bash scripts/check-codex-skill-descriptions.sh --paths a-m`

## Out of Scope

Plugin synchronization, repository catalogs, eval JSON authoring, and consumer application changes.
