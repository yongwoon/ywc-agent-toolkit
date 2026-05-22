# Claude Code Agent Catalog

This directory is the English entry point for the `claude-code/agents/`
catalog. For agent-authoring rules, see [CLAUDE.md](./CLAUDE.md).

## Catalog Overview

This catalog holds named Worker Agents dispatchable via the Claude Code
**Task tool subagent dispatch** or the **Claude Agent SDK**. Each agent runs
in an isolated context window as a single-responsibility worker, designed
as the dispatch target for skill-level fan-out (parallel or sequential).

**Current policy**

- Tier 1 (worker) — 4 agents: Backend / Frontend / QA Engineer / Doc Writer
- Tier 2 (language reviewer) — 3 agents currently shipped: TypeScript (Sonnet) / Python (Sonnet) / Go (Sonnet); Swift / Rust — follow-up PR
- Tier 3 (specialist) — 5 agents currently shipped: Architect (Opus) / Security Engineer (Sonnet) / Refactor Cleaner (Sonnet) / Root-cause Analyst (Opus) / Performance Engineer (Sonnet); additional specialists — follow-up PR
- Catalog sync scope — `claude-code/` only (not Codex / pi-skills)

Tier definitions and dispatch flow are documented in
[`docs/superpowers/specs/2026-05-21-ywc-agent-toolkit-design.md`](../../../docs/superpowers/specs/2026-05-21-ywc-agent-toolkit-design.md):
Iteration 0 §2 (Persona Definitions) and Iteration 4 §P3 (Built-in vs Custom).

## Per-Agent Summary

> The table below shows the agents currently in this catalog (4 Tier 1 workers
> + 3 Tier 2 language reviewers + 5 Tier 3 specialists). Each agent body's
> authoritative frontmatter, Mission, Boundaries, and Return Contract live in
> the corresponding `<agent-name>.md` file.

| Name | Tier | Model | Mission |
|------|------|-------|---------|
| `ywc-backend-coder` | 1 (worker) | sonnet | Server-side code: API / Business logic / Database integration |
| `ywc-frontend-coder` | 1 (worker) | sonnet | Client-side code: UI / State / Routing / a11y |
| `ywc-qa-engineer` | 1 (worker) | sonnet | Test code: Unit / Integration / E2E, edge case authoring. Must not modify code outside tests/ |
| `ywc-doc-writer` | 1 (worker) | haiku | Documentation / Comment / Release note authoring. No Bash tool grant |
| `ywc-typescript-reviewer` | 2 (language reviewer) | sonnet | TypeScript-specific code review (read-only). Type system depth (generics, conditional types, satisfies), async correctness, framework idioms (React hooks / Vue / Svelte), tsconfig strictness, ESM/CJS interop. Dispatched from ywc-impl-review Phase 1 (TS-heavy diff) / Phase 2 (Design or type-system advisor) |
| `ywc-python-reviewer` | 2 (language reviewer) | sonnet | Python-specific code review (read-only). Type system depth (Protocol / TypedDict / TypeGuard / Self / ParamSpec, mypy strict mode), asyncio correctness (gather / create_task / cancellation), framework idioms (Django ORM / FastAPI / Pydantic v2 / Flask), GIL implications (ProcessPoolExecutor vs threadpool), lifecycle patterns (context manager / generator / `__init__.py`). Dispatched from ywc-impl-review Phase 1 (Python-heavy diff) / Phase 2 (Design or type-system advisor) |
| `ywc-go-reviewer` | 2 (language reviewer) | sonnet | Go-specific code review (read-only). Goroutine lifecycle (leak / context cancellation / errgroup), channel patterns (close ownership / select / chan struct{}), interface design (accept interfaces return concrete / small interface), error wrapping (`fmt.Errorf %w` / `errors.Is` / `errors.As`), pointer vs value semantics (method set / escape analysis), generics post 1.18, lifecycle (defer / sync primitives / race detection). Dispatched from ywc-impl-review Phase 1 (Go-heavy diff) / Phase 2 (concurrency or interface-design advisor) |
| `ywc-architect` | 3 (specialist) | opus | Architectural decision worker (read-only). Trade-off analysis, module boundary / dependency direction / abstraction judgments. Dispatched from ywc-plan / ywc-impl-review Phase 2 / ywc-confidence-gate |
| `ywc-security-engineer` | 3 (specialist) | sonnet | Static security review worker (read-only). OWASP Top 10 + threat modeling + secret/PII scan, severity-rated findings with concrete remediation. Dispatched from ywc-security-audit / ywc-impl-review Phase 1 / ywc-incident-postmortem |
| `ywc-refactor-cleaner` | 3 (specialist) | sonnet | Dead-code deletion worker (coder tier — writes). Receives the SAFE-tier worklist from ywc-refactor-clean, runs per-item grep + scoped test before/after + one-deletion-per-commit. Dispatched from ywc-refactor-clean Step 3 |
| `ywc-root-cause-analyst` | 3 (specialist) | opus | Root-cause analyst (read-only). 5 Whys + hypothesis tracking + primary cause vs contributing factor separation + "architecture wrong vs fix harder" gate. Dispatched from ywc-debug-rootcause Phase 1 / Phase 3 (3+ failed fixes), ywc-incident-postmortem Step 4 |
| `ywc-performance-engineer` | 3 (specialist) | sonnet | Performance review worker (read-only). 4 axes: Backend (N+1 / index / hot loop / sync IO / allocation / lock), Frontend (bundle / render-block / image / hydration / CSS specificity), Web Vitals (LCP / INP / CLS / FCP / TBT against project targets), Profiling recommendations (py-spy / chrome devtools / node --prof / pprof / perf / JFR / dotnet-trace — recommend invocation, do not execute). Dispatched from ywc-impl-review Phase 2 advisor pass on Performance-related Architecture / Devex candidate |

Each agent body's exact frontmatter, Mission text, Boundaries, and Return
Contract lives in the corresponding `claude-code/agents/<agent-name>.md`
file. The catalog's agents are dispatched by name (`subagent_type: ywc-<name>`)
from [`ywc-code-gen`](../skills/ywc-code-gen/),
[`ywc-parallel-executor`](../skills/ywc-parallel-executor/),
[`ywc-sequential-executor`](../skills/ywc-sequential-executor/), and
[`ywc-agentic`](../skills/ywc-agentic/) (Step 5).

## Frontmatter Rule

Agent frontmatter must be valid under a strict YAML parser. Canonical form:

```yaml
---
name: <agent-name>
description: >-
  <mission summary>. Triggers: "<dispatch entry points>". Do not use for:
  "<anti-triggers>".
model: sonnet
tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

**camelCase warning** — only four keys use camelCase: `permissionMode`,
`maxTurns`, `initialPrompt`, `mcpServers`. Every other key is lowercase.
For the full table and authoring trap notes, see the "camelCase Warning"
section in [CLAUDE.md](./CLAUDE.md).

**Return Contract** — agents return payloads in the 4-state format defined in
[`claude-code/skills/references/subagent-status-actions.md`](../skills/references/subagent-status-actions.md)
§3.5 (`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`). Do not
invent a new format inside the agent body (Iteration 6 §R1).

## Install Commands

```bash
# Install all agents under ~/.claude/agents/
bash claude-code/agents/scripts/install.sh

# List available agents
bash claude-code/agents/scripts/install.sh --list

# Show usage
bash claude-code/agents/scripts/install.sh --help

# Dry-run (no writes)
bash claude-code/agents/scripts/install.sh --dry-run

# Override destination (testing)
CLAUDE_AGENTS_DIR=/tmp/test-agents bash claude-code/agents/scripts/install.sh
```

Installed agents live at `~/.claude/agents/<agent-name>.md` and are
immediately dispatchable in any Claude Code session on the machine. **Global
namespace caveat**: if another source installs an agent with the same name,
the last installer wins. Prefer the `ywc-` prefix for project-specific
agents to reduce collision risk.

## Related Skills

Agents in this catalog are dispatched by the following skills (from Phase 6
onward):

- [`ywc-code-gen`](../skills/ywc-code-gen/) — Phase 1 parallel generation step
- [`ywc-parallel-executor`](../skills/ywc-parallel-executor/) — Wave-mode task execution
- [`ywc-sequential-executor`](../skills/ywc-sequential-executor/) — Sequential task execution
- [`ywc-agentic`](../skills/ywc-agentic/) — Step 5 Execute Phase

Each skill dispatches by name via `subagent_type: ywc-<name>` inside its
SKILL.md body.
