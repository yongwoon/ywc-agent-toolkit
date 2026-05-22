# Agents Directory — Authoring Rules

Canonical authoring rules for Claude Code agent files under
`claude-code/agents/`. Read this file before creating, renaming, or
restructuring any agent in this catalog.

> **Scope**: this directory is **claude-code only** — Codex CLI and pi-skills
> do not carry an equivalent agent catalog at this time
> (per Iteration 3 §M2 / §S2 of the ywc-agent-toolkit design spec).

## Authoring Overview

An **agent** is an independent worker dispatched via the Claude Code `Task` tool
(or the SDK `ClaudeAgentOptions(agents=...)` map). Each agent file is a
self-contained system-prompt that defines a named role, a bounded tool set,
and a single-responsibility mission.

Agents differ from skills:

| Surface | Trigger | Execution context | Output |
|---------|---------|-------------------|--------|
| **Skill** | `/name` slash command or auto-trigger from frontmatter `description` | Loaded into the main thread, instructions followed in-place | Whatever the main thread produces |
| **Agent** | `Task(subagent_type=name)` dispatch | Spawned as an isolated subprocess with its own context window | Return payload returned to the main thread, files written to disk |

Use an agent when work is independent, sandboxable, and the orchestrator
must remain free to plan or fan-out. Use a skill when work belongs in the
main thread's reasoning flow.

For the decision framework, see
[`docs/llm-study/SKILL_VS_AGENT.md`](../../../docs/llm-study/SKILL_VS_AGENT.md).

## Frontmatter Schema

Every agent file starts with YAML frontmatter delimited by `---` lines.
Canonical example (Iteration 3 §M3 of the design spec):

```yaml
---
name: ywc-backend-coder
description: >-
  Server-side code generation worker. Triggers: explicit `Task(subagent_type=ywc-backend-coder)`
  dispatch by ywc-code-gen / ywc-parallel-executor / ywc-sequential-executor /
  ywc-agentic Step 5. Do not invoke for client-side UI, test-only work, or
  documentation prose.
model: sonnet
tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

### Required keys

- **`name`** (lowercase string) — must match the filename (without `.md`).
  Validator rule: `filename == name`.
- **`description`** (folded block scalar `>-`) — must follow the
  `Triggers: "..." . Do not use for: "..."` pattern. The `Triggers:` field
  carries `:` characters, which would break a plain scalar — always use the
  folded form.
- **`model`** (string) — either alias (`sonnet`, `haiku`, `opus`) or pinned ID
  (`claude-sonnet-4-6`, `claude-haiku-4-5-20251001`, etc.). Both forms are
  accepted by the Claude Code runtime (empirically verified by the Phase 0
  prototype; see
  [`agents/_prototype/prototype-result.md`](_prototype/prototype-result.md)).
- **`tools`** (YAML list) — minimal tool grant. The canonical form is the
  bracketed YAML list. The comma-separated form may also parse but the YAML
  list form is the documented contract.

### Optional keys (15-field allowlist per Iteration 4 §P2)

| Key | Type | Purpose |
|-----|------|---------|
| `permissionMode` | string | `dontAsk` to suppress write-tool prompts; defaults to user/session policy. **camelCase.** |
| `maxTurns` | integer | Hard cap on conversation turns within the agent. **camelCase.** |
| `initialPrompt` | string | Override the system-prompt body (rare). **camelCase.** |
| `mcpServers` | list | Per-agent MCP server restriction. **camelCase.** |
| `disallowedTools` | list | Explicit deny list (intersected with `tools`). **lowercase.** |
| `category` | string | Logical grouping for catalog UI. **lowercase.** |
| `version` | string | Semver-style content version. **lowercase.** |
| `license` | string | License hint for catalog publishing. **lowercase.** |
| `metadata` | object | Free-form labels. **lowercase.** |
| `compatibility` | object | Tool / runtime constraints. **lowercase.** |
| `tags` | list | Search tags. **lowercase.** |
| `author` | string | Authorship attribution. **lowercase.** |
| `homepage` | string | Catalog homepage / docs URL. **lowercase.** |
| `repository` | string | Source repo URL. **lowercase.** |
| `examples` | list | Example dispatches for catalog UI. **lowercase.** |

Unrecognized keys are rejected by the validator; see
[`tools/scripts/validate_ywc_agents.py`](../../../tools/scripts/validate_ywc_agents.py)
(introduced by task `000004-030`).

### camelCase Warning (Iteration 5 §Q1, Iteration 6 §R2)

A small number of keys use camelCase while the majority use lowercase. The
asymmetry is a runtime quirk, **not** a stylistic preference. Mixing the two
forms silently fails — the runtime accepts the file but ignores the
misnamed key.

| Lowercase (mandatory) | camelCase (mandatory) |
|-----------------------|-----------------------|
| `name` | `permissionMode` |
| `description` | `maxTurns` |
| `model` | `initialPrompt` |
| `tools` | `mcpServers` |
| `disallowedTools` | |
| `category` `version` `license` `metadata` `compatibility` `tags` `author` `homepage` `repository` `examples` | |

**Authoring trap**: writing `permission_mode: dontAsk` or `maxturns: 5` produces
an agent that silently lacks the intended setting. Always reference this table
when adding a new key.

## Body Schema (6 Mandatory Sections)

Per `SKILL_AGENT_AUTHORING_PRINCIPLES.md` §4.2, every agent body contains six
sections in this order:

1. **Mission** — single-sentence purpose. What this agent is for; what it owns.
2. **Triggers** — exhaustive list of dispatch entry points (caller skill name +
   step number). Triggers in the frontmatter `description` are the auto-detect
   signal; this section is the verbose form.
3. **Boundaries** — explicit "Will NOT" enumeration. Scope creep is the
   number-one failure mode of agent fan-out; this section is where you draw
   the line.
4. **Success Criteria** — observable outcomes that mean "done." Used by
   downstream verification.
5. **Return Contract** — one-line reference:
   `> Status payload format: see claude-code/skills/references/subagent-status-actions.md §3.5`.
   **Do not invent a return format inline** (Iteration 6 §R1). The canonical
   reference defines the 4-state payload (`DONE` / `DONE_WITH_CONCERNS` /
   `BLOCKED` / `NEEDS_CONTEXT`); inventing a parallel format breaks downstream
   routing.
6. **Anti-patterns** — common authoring or invocation mistakes that violate
   the contract. Examples: "Do not invoke another agent from within this
   agent" / "Do not edit files outside the path scope listed in Mission."

## Tool Permission Tiers (§4.3)

Grant the **minimum** tool set required by the agent's Mission. The four
canonical tiers:

| Tier | Tools | Use case |
|------|-------|----------|
| Read-only researcher | `[Read, Grep, Glob]` | Survey, audit, fact-finding |
| Read-only reviewer | `[Read, Grep, Glob, WebFetch]` | Code review with online doc lookup |
| Coder | `[Read, Write, Edit, Bash, Grep, Glob]` | Implementation work |
| Doc writer | `[Read, Write, Edit, Grep, Glob]` | Documentation (no Bash) |

If your agent doesn't match a tier, justify the divergence in the agent body
under Boundaries. Avoid `[*]` — explicit lists are auditable, the wildcard is
not.

## Built-in vs Custom Justification (Iteration 4 §P3)

Claude Code ships built-in agent types (`general-purpose`, plus the
`document-skills:*` and `oh-my-claudecode:*` plugin agents). Before creating a
custom agent, justify why a built-in won't do:

- **Reusable role across multiple skills?** → custom agent (catalog entry)
- **One-off dispatch with project-specific instructions?** → `general-purpose`
  with a focused prompt
- **Specialized review (security / TS / Python / etc.)?** → use the
  `ecc:*-reviewer` family from the ECC plugin

Adding a custom agent is justified when the agent will be named-dispatched by
two or more skills, OR when it carries a stable persona that benefits from
versioning and validation.

## Read-only Safety Pattern (Iteration 5 §Q2)

For agents whose Mission is strictly read-only (researcher, reviewer), combine:

```yaml
tools: [Read, Grep, Glob]      # No Write/Edit/Bash
permissionMode: dontAsk        # Suppress redundant prompts since no writes possible
```

**Do not** apply `permissionMode: dontAsk` to coder or doc-writer tiers — those
tiers legitimately need write tools, and a stray write should still surface a
prompt. The setting is for tiers where writes are structurally excluded.

## Return Contract Reference

All agents return their payload using the canonical 4-state format defined in
[`claude-code/skills/references/subagent-status-actions.md`](../skills/references/subagent-status-actions.md) §3.5:

```
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary: <1-line>
Artifacts: <file:line list>
Concerns | Blocker | Missing-context: <bounded per format>
```

The agent body's **Return Contract** section must reference this file by path
and section — **do not redefine the format inline**.

## File Layout

```
claude-code/agents/
├── CLAUDE.md                 # This file
├── README.md                 # Korean primary catalog guide
├── README.en.md              # English locale (full content)
├── README.ja.md              # Japanese locale (full content)
├── README.ko.md              # Korean summary
├── scripts/
│   └── install.sh            # ~/.claude/agents/ bulk installer
├── <agent-name>.md           # Agent body files (created by 000005-010)
└── _prototype/               # Phase 0 throwaway (deleted before Phase 5)
```

`evals/` and other ancillary directories may appear once `000007-010` lands T2
evaluation infrastructure.

## Installation

```bash
bash claude-code/agents/scripts/install.sh           # install all agents
bash claude-code/agents/scripts/install.sh --list    # list available
bash claude-code/agents/scripts/install.sh --help    # usage
bash claude-code/agents/scripts/install.sh --dry-run # preview without writes
CLAUDE_AGENTS_DIR=/tmp/test bash claude-code/agents/scripts/install.sh
```

Installed agents land in `~/.claude/agents/` (or `$CLAUDE_AGENTS_DIR`) and
become available to every Claude Code session on the machine. Be aware that
this is a **global namespace** — if two projects install agents with the same
name, the last installer wins. Prefer the `ywc-` prefix for project-specific
agents to reduce collision risk.

## Validator

Agent files are validated by
[`tools/scripts/validate_ywc_agents.py`](../../../tools/scripts/validate_ywc_agents.py)
on every CI run. See task `000004-030-infra-agent-validator` for the rule set.
Authoring failures surface as merge-blocking errors with hints pointing back to
the relevant section of this file.

## Quick Reference

- New agent → start from an existing entry in the same tier, copy the body
  skeleton, change the Mission first.
- Return format → reference, do not invent.
- camelCase keys → only `permissionMode`, `maxTurns`, `initialPrompt`,
  `mcpServers`. Everything else is lowercase.
- `permissionMode: dontAsk` → only on read-only tiers.
- Tool grants → minimum required. Audit removes unused grants.
- Codex / pi-skills → not in scope here. This catalog is claude-code only.
