# 000016-050-docs-custom-agent-bounded-evidence

## Purpose
모든 Codex custom agent에 bounded evidence, no-invention, no-adjacent-nit, `NEEDS_CONTEXT` discipline을 일관되게 반영한다. 이 task는 각 agent specialization은 유지하면서 공통 evidence behavior만 정렬한다.

## Scope
- `codex/agents/*.toml` 7개 파일에 짧은 bounded-evidence wording 추가 또는 normalize
- 각 agent의 specialization과 read-only boundary 유지
- `codex/agents/README.md`는 필요할 때만 업데이트

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#fr-5-update-custom-agents` — custom agent 요구사항
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#acceptance-criteria` — AC7, AC8 검증 기준
- `codex/agents/*.toml` — 수정 대상 custom agent prompts

### Summary
이 task는 custom agent들이 evidence packet 밖의 facts, files, APIs, metrics, exploit paths, code owner intent를 invent하지 않도록 일관된 instruction을 추가한다. Agent별 role은 그대로 유지되어야 한다. 큰 rewrite보다 짧은 common sentence 추가가 우선이다.

### Out of Scope (from spec)
- Skill prompt/template 변경 — handled by tasks `000016-020`, `000016-030`, `000016-040`
- Agent model, sandbox, MCP/tooling behavior 변경 — out of scope
- generated plugin sync — not applicable to `codex/agents`, final validation handled by `000017-010-infra-codex-karpathy-validation`

## Dependencies

### Depends On
- `000016-010-docs-principles-guideline-gap` — shared evidence/scope vocabulary

### Depended By
- `000017-010-infra-codex-karpathy-validation` — agent list validation and final diff check

## Key Files
- `codex/agents/ywc-architect.toml`
- `codex/agents/ywc-go-reviewer.toml`
- `codex/agents/ywc-performance-engineer.toml`
- `codex/agents/ywc-python-reviewer.toml`
- `codex/agents/ywc-root-cause-analyst.toml`
- `codex/agents/ywc-security-engineer.toml`
- `codex/agents/ywc-typescript-reviewer.toml`
- `codex/agents/README.md` — only if needed

## Notes
- Preserve output contract: `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`.
- Do not homogenize role-specific expertise.
- Prefer minimal prompt edits to avoid unnecessary TOML churn.

## Parallel Execution Metadata

### Ownership
- `codex/agents/*.toml`
- `codex/agents/README.md` if needed

### Shared Surfaces
- Codex custom agent prompt contract
- Agent install/list metadata

### Conflicts With
- `(None identified)`

### Parallelizable After
- `000016-010-docs-principles-guideline-gap`

### Task Verify
- `rg -n "bounded evidence|NEEDS_CONTEXT|invent|adjacent|evidence packet" codex/agents/*.toml`
- `bash scripts/install.sh --list --codex-agents`

## Out of Scope
- Changing agent `model`, `approval_policy`, or tool access.
- Adding new agents.
- Editing Claude Code agents.
