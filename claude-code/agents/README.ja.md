# Claude Code Agent Catalog

`claude-code/agents/` Catalog の日本語 entry point です。Agent file の
authoring rule は [CLAUDE.md](./CLAUDE.md) を参照してください。

## Catalog Overview

この Catalog は Claude Code の **Task tool subagent dispatch** または
**Claude Agent SDK** から呼び出せる named Worker Agent の集合を保管します。
各 Agent は独立した context window で実行される single-responsibility worker
で、Skill の fan-out (parallel/sequential) dispatch 対象として設計されています。

**現時点のポリシー**

- Tier 1 (worker) — Backend / Frontend / QA Engineer / Doc Writer の 4 種
- Tier 2 (language reviewer) — 現在 3 種が land 済: TypeScript (Sonnet) / Python (Sonnet) / Go (Sonnet)。Swift / Rust などは follow-up PR
- Tier 3 (specialist) — 現在 5 種が land 済: Architect (Opus) / Security Engineer (Sonnet) / Refactor Cleaner (Sonnet) / Root-cause Analyst (Opus) / Performance Engineer (Sonnet)。追加 specialist は follow-up PR
- Catalog sync 範囲 — `claude-code/` のみ (Codex / pi-skills には適用しない)

Tier 定義および dispatch flow は spec 文書
[`docs/superpowers/specs/2026-05-21-ywc-agent-toolkit-design.md`](../../../docs/superpowers/specs/2026-05-21-ywc-agent-toolkit-design.md)
の Iteration 0 §2 (Persona Definitions) および Iteration 4 §P3
(Built-in vs Custom) を参照します。

## Per-Agent Summary

> 以下の表は本 Catalog に現在 land している Agent です (Tier 1 worker 4 種 + Tier 2
> language reviewer 3 種 + Tier 3 specialist 5 種)。各 Agent body の正式な
> frontmatter / Mission / Boundaries / Return Contract は対応する
> `<agent-name>.md` ファイル内で確認できます。

| Name | Tier | Model | Mission |
|------|------|-------|---------|
| `ywc-backend-coder` | 1 (worker) | sonnet | Server-side code: API / Business logic / Database integration |
| `ywc-frontend-coder` | 1 (worker) | sonnet | Client-side code: UI / State / Routing / a11y |
| `ywc-qa-engineer` | 1 (worker) | sonnet | Test code: Unit / Integration / E2E、edge case authoring。tests/ 以外の変更禁止 |
| `ywc-doc-writer` | 1 (worker) | haiku | 文書 / Comment / Release note 作成。Bash tool 除外 |
| `ywc-typescript-reviewer` | 2 (language reviewer) | sonnet | TypeScript-specific code review (read-only)。Type system depth (generics, conditional types, satisfies)、async correctness、framework idioms (React hooks / Vue / Svelte)、tsconfig strictness、ESM/CJS interop。ywc-impl-review Phase 1 (TS-heavy diff) / Phase 2 (Design 又は type-system advisor) から dispatch |
| `ywc-python-reviewer` | 2 (language reviewer) | sonnet | Python-specific code review (read-only)。Type system depth (Protocol / TypedDict / TypeGuard / Self / ParamSpec、mypy strict mode)、asyncio correctness (gather / create_task / cancellation)、framework idioms (Django ORM / FastAPI / Pydantic v2 / Flask)、GIL implications (ProcessPoolExecutor vs threadpool)、lifecycle patterns (context manager / generator / `__init__.py`)。ywc-impl-review Phase 1 (Python-heavy diff) / Phase 2 (Design 又は type-system advisor) から dispatch |
| `ywc-go-reviewer` | 2 (language reviewer) | sonnet | Go-specific code review (read-only)。Goroutine lifecycle (leak / context cancellation / errgroup)、channel patterns (close ownership / select / chan struct{})、interface design (accept interfaces return concrete / small interface)、error wrapping (`fmt.Errorf %w` / `errors.Is` / `errors.As`)、pointer vs value semantics (method set / escape analysis)、generics post 1.18、lifecycle (defer / sync primitives / race detection)。ywc-impl-review Phase 1 (Go-heavy diff) / Phase 2 (concurrency 又は interface-design advisor) から dispatch |
| `ywc-architect` | 3 (specialist) | opus | Architectural decision worker (read-only)。Trade-off 分析 + module boundary / dependency direction / 抽象化判断 verdict 返却。ywc-plan / ywc-impl-review Phase 2 / ywc-confidence-gate から dispatch |
| `ywc-security-engineer` | 3 (specialist) | sonnet | Static security review worker (read-only)。OWASP Top 10 + threat modeling + secret/PII scan、severity-rated findings + 具体 remediation。ywc-security-audit / ywc-impl-review Phase 1 / ywc-incident-postmortem から dispatch |
| `ywc-refactor-cleaner` | 3 (specialist) | sonnet | Dead-code 削除 worker (coder tier — writes)。SAFE 分類された worklist を受けて per-item grep 検証 + 前後 test 実行 + 1-deletion-per-commit で削除。ywc-refactor-clean Step 3 から dispatch |
| `ywc-root-cause-analyst` | 3 (specialist) | opus | Root-cause analyst (read-only)。5 Whys + hypothesis tracking + primary cause vs contributing factor 分離 + "architecture wrong vs fix harder" gate。ywc-debug-rootcause Phase 1 / Phase 3 (3+ failed fixes), ywc-incident-postmortem Step 4 から dispatch |
| `ywc-performance-engineer` | 3 (specialist) | sonnet | Performance review worker (read-only)。4 axes: Backend (N+1 / index / hot loop / sync IO / allocation / lock)、Frontend (bundle / render-block / image / hydration / CSS specificity)、Web Vitals (LCP / INP / CLS / FCP / TBT vs project targets)、Profiling recommendations (py-spy / chrome devtools / node --prof / pprof / perf / JFR / dotnet-trace — recommend invocation、do not execute)。ywc-impl-review Phase 2 advisor pass の Performance-related Architecture / Devex candidate から dispatch |

各 Agent body の正確な frontmatter、Mission 文言、Boundaries、Return Contract は
`claude-code/agents/<agent-name>.md` で直接確認できます。本 Catalog の
Agent は [`ywc-code-gen`](../skills/ywc-code-gen/)、
[`ywc-parallel-executor`](../skills/ywc-parallel-executor/)、
[`ywc-sequential-executor`](../skills/ywc-sequential-executor/)、
[`ywc-agentic`](../skills/ywc-agentic/) (Step 5) から
named dispatch (`subagent_type: ywc-<name>`) されます。

## Frontmatter Rule

Agent file の frontmatter は strict YAML parser で valid である必要があり、
canonical form は次の通りです:

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

**camelCase warning** — `permissionMode`、`maxTurns`、`initialPrompt`、
`mcpServers` の 4 つの key のみ camelCase で、他はすべて lowercase です。
詳細な rule は [CLAUDE.md](./CLAUDE.md) の "camelCase Warning" section を
参照してください。

**Return Contract** — Agent の return payload format は
[`claude-code/skills/references/subagent-status-actions.md`](../skills/references/subagent-status-actions.md)
§3.5 の 4-state payload (`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` /
`NEEDS_CONTEXT`) に従い、Agent body 内で新しい format を invent しないでください
(Iteration 6 §R1)。

## Install Commands

```bash
# すべての Agent を ~/.claude/agents/ にインストール
bash claude-code/agents/scripts/install.sh

# インストール可能な Agent を一覧表示
bash claude-code/agents/scripts/install.sh --list

# Usage を表示
bash claude-code/agents/scripts/install.sh --help

# 実際には書き込まず動作のみ確認
bash claude-code/agents/scripts/install.sh --dry-run

# 宛先 override (testing 用)
CLAUDE_AGENTS_DIR=/tmp/test-agents bash claude-code/agents/scripts/install.sh
```

Installed Agent は `~/.claude/agents/<agent-name>.md` に配置され、マシン上の
すべての Claude Code session から即座に dispatch 可能です。**Global namespace
注意**: 同名 Agent が別の source から install される場合、最後の installer の
内容で上書きされます。Project specific Agent は `ywc-` prefix を維持して衝突
リスクを下げることが推奨されます。

## Related Skills

本 Catalog の Agent は Phase 6 以降、以下の Skill から dispatch されます:

- [`ywc-code-gen`](../skills/ywc-code-gen/) — Phase 1 parallel generation step
- [`ywc-parallel-executor`](../skills/ywc-parallel-executor/) — Wave-mode task execution
- [`ywc-sequential-executor`](../skills/ywc-sequential-executor/) — Sequential task execution
- [`ywc-agentic`](../skills/ywc-agentic/) — Step 5 Execute Phase

各 Skill は SKILL.md 内で `subagent_type: ywc-<name>` の named dispatch を
行います。
