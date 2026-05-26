# Codex Custom Agents

This directory contains Codex custom agent definitions that complement the
portable `ywc-*` skills.

These files are installed to `${CODEX_HOME:-~/.codex}/agents` by
`scripts/install.sh --codex` (skills + agents together) or by
`scripts/install.sh --codex-agents` when installing agents only.

## Included Agents

| Agent | Purpose | Sandbox |
| --- | --- | --- |
| `ywc-architect` | Architectural decision and trade-off advisor | `read-only` |
| `ywc-security-engineer` | Static security review and threat-model triage | `read-only` |
| `ywc-root-cause-analyst` | Root-cause and incident-cause analysis | `read-only` |
| `ywc-performance-engineer` | Performance review and profiling recommendations | `read-only` |
| `ywc-typescript-reviewer` | TypeScript / JavaScript language-specific review | `read-only` |
| `ywc-python-reviewer` | Python language-specific review | `read-only` |
| `ywc-go-reviewer` | Go language-specific review | `read-only` |

## Authoring Notes

- Keep these files in TOML. Codex loads one custom agent per file.
- Required fields are `name`, `description`, and `developer_instructions`.
- Keep specialist agents read-only unless there is a deliberate implementation
  role with a bounded edit contract.
- Do not copy Claude Code-only fields such as `tools`, `permissionMode`, or
  `Task(subagent_type=...)` into Codex TOML.
