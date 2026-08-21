# ywc-agent-toolkit

A collection of skills for **Claude Code** and **Codex** that automates the full development workflow — from planning and spec writing to code generation, review, and release.

[한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Español](README.es.md)

> 📖 **[Documentation & Guidebook](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/)** — this README is the short tour. The guidebook is the manual: prerequisites, installation, the full skill reference, and step-by-step workflow guides.

| Where to go | Guidebook page |
| ----------- | -------------- |
| Ship your first feature in 5 minutes | [03. Quickstart](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/03-quickstart/) |
| Which skill do I run, in what order? | [17. Full Skill Reference](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/14-skill-reference/) |
| Prerequisites, install paths, env vars | [18. Prerequisites and installation](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/15-prerequisites-installation/) |
| Small change / multi-task / autonomous loop | [04](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/04-general-cycle-small/) · [05](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/05-general-cycle-medium-large/) · [06](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/06-agentic-autonomous-loop/) |

## Supported Tools

| Tool        | Skills | Custom Agents | Install path                             |
| ----------- | ------ | ------------- | ---------------------------------------- |
| Claude Code | 42     | 12            | `~/.claude/skills/`, `~/.claude/agents/` |
| Codex       | 52     | 8             | `~/.codex/skills/`, `~/.codex/agents/`   |

---

## Quick Start

### Claude Code

Install from the plugin marketplace — no cloning, no prerequisites:

```bash
/plugin marketplace add yongwoon/ywc-agent-toolkit    # 1. register the source
/plugin install ywc-agent-toolkit@ywc-agent-toolkit   # 2. install the plugin
```

`marketplace add` only registers the source — you must then run `/plugin install`, or use the Plugin UI **Marketplaces** tab. Restart Claude Code afterward for the skills to appear.

### Codex

```bash
codex plugin marketplace add yongwoon/ywc-agent-toolkit   # 1. register the source
codex plugin add ywc-agent-toolkit@ywc-agent-toolkit      # 2. install the plugin
```

If the marketplace was added before, refresh its Git snapshot first with `codex plugin marketplace upgrade ywc-agent-toolkit`. You can also run `codex`, open `/plugins`, and install from the **YWC Agent Toolkit** tab.

In the **Codex App**, open **Plugins** in the sidebar, choose the **YWC Agent Toolkit** source, confirm it is `yongwoon/ywc-agent-toolkit`, then install from the plugin details view.

### Then run a skill

Both tools expose the same commands:

```bash
/ywc-onboard-repo           # understand an unfamiliar codebase in minutes
/ywc-plan                   # turn a rough idea into a plan or spec
/ywc-debug-rootcause        # trace a bug to its root cause
/ywc-impl-review            # review code for spec / security / quality
/ywc-agentic                # run the full pipeline autonomously from a goal
```

→ Prerequisites, the bash-script fallback, install paths, and `CLAUDE_SKILLS_DIR` / `CLAUDE_AGENTS_DIR` / `CODEX_HOME` overrides are documented in [Prerequisites and installation](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/15-prerequisites-installation/).

### Install options not covered in the guidebook

```bash
# Specific skills only
bash scripts/install.sh --cc ywc-plan ywc-commit ywc-create-pr
bash scripts/install.sh --codex ywc-plan ywc-commit ywc-ui-ux-review

# Selected agents only, or skills without agents
bash scripts/install.sh --cc-agents ywc-backend-coder ywc-qa-engineer
bash scripts/install.sh --cc --skip-agents
```

### Codex output language defaults

Codex-only `ywc-setup` configures durable artifact language for Codex `ywc-*` skills:

```bash
ywc-setup --scope project --lang ko
ywc-setup --scope user --lang ja
```

Resolution order: explicit `--lang` > project `.codex/ywc.json` > project guidance (`AGENTS.md` / `CODEX.md` / `CLAUDE.md`) > user `~/.codex/ywc.json` > ask user. Session defaults are unsupported.

---

## Skills

Most `ywc-*` skills are available for both Claude Code and Codex. The full catalog — every skill, grouped by what you want to do — lives in the [Full Skill Reference](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/14-skill-reference/). Start here:

| Goal | Skills |
| ---- | ------ |
| Turn an idea into a plan or spec | [`ywc-plan`](claude-code/skills/ywc-plan/README.md) → [`ywc-spec-writer`](claude-code/skills/ywc-spec-writer/README.md) |
| Understand an unfamiliar codebase | [`ywc-onboard-repo`](claude-code/skills/ywc-onboard-repo/README.md) |
| Break work into dependency-safe tasks | [`ywc-task-generator`](claude-code/skills/ywc-task-generator/README.md) |
| Implement tasks end-to-end | [`ywc-sequential-executor`](claude-code/skills/ywc-sequential-executor/README.md) / [`ywc-parallel-executor`](claude-code/skills/ywc-parallel-executor/README.md) |
| Run the full pipeline from a goal | [`ywc-agentic`](claude-code/skills/ywc-agentic/README.md) |
| Find the root cause of a bug | [`ywc-debug-rootcause`](claude-code/skills/ywc-debug-rootcause/README.md) |
| Review code quality and security | [`ywc-impl-review`](claude-code/skills/ywc-impl-review/README.md), [`ywc-security-audit`](claude-code/skills/ywc-security-audit/README.md) |
| Open a PR and handle review comments | [`ywc-create-pr`](claude-code/skills/ywc-create-pr/README.md) → [`ywc-handle-pr-reviews`](claude-code/skills/ywc-handle-pr-reviews/README.md) |
| Generate a QA test sheet | [`ywc-gen-testcase`](claude-code/skills/ywc-gen-testcase/README.md) |
| Write release notes | [`ywc-release-pr-list`](claude-code/skills/ywc-release-pr-list/README.md) + [`ywc-changelog-release-notes`](claude-code/skills/ywc-changelog-release-notes/README.md) |
| Author a new `ywc-*` skill | [`ywc-skill-author`](claude-code/skills/ywc-skill-author/README.md) |

Browse every skill directory under [`claude-code/skills/`](claude-code/skills) and [`codex/skills/`](codex/skills); each has its own README.

**How they fit together:** `ywc-plan` → (Medium/Large) `ywc-spec-writer` → `ywc-spec-ready` → `ywc-task-generator` → `ywc-sequential-executor` / `ywc-parallel-executor`, which delivers each task end to end. Ad-hoc changes skip the executor: `ywc-create-pr` then `ywc-handle-pr-reviews`. The [core pipeline guides](https://yongwoon.github.io/ywc-agent-toolkit-lp/en/guidebook/02-core-concepts/) walk through each path with commands and flags.

### HTML output mode

Nine review and report skills accept `--format html`, producing a self-contained browser-ready report instead of Markdown — color, severity coding, tabs, and interactive controls, so the human on the other end actually reads it.

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-gen-testcase 250 --format html   # interactive testsheet with localStorage sign-off
```

> **⚠️ Token cost** — HTML uses 2–4× the output tokens of Markdown. The default is `markdown`; enable HTML only for reports a human will read in a browser.

Supported skills and details: [`references/html-output.md`](claude-code/skills/references/html-output.md).

---

## Custom Agents

Claude Code ships 12 custom agents for worker, reviewer, and specialist dispatch, installed to `~/.claude/agents/` and documented in [`claude-code/agents/README.md`](claude-code/agents/README.md).

Codex gets seven read-only specialist counterparts, installed to `~/.codex/agents/` (override with `CODEX_HOME`) as one TOML file per agent:

| Agent | Purpose |
| ----- | ------- |
| [`ywc-architect`](claude-code/agents/ywc-architect.md) | Architectural decision and trade-off advisor |
| [`ywc-security-engineer`](claude-code/agents/ywc-security-engineer.md) | Static security review and threat-model triage |
| [`ywc-root-cause-analyst`](claude-code/agents/ywc-root-cause-analyst.md) | Root-cause and incident-cause analysis |
| [`ywc-performance-engineer`](claude-code/agents/ywc-performance-engineer.md) | Performance review and profiling recommendations |
| [`ywc-typescript-reviewer`](claude-code/agents/ywc-typescript-reviewer.md) | TypeScript / JavaScript language-specific review |
| [`ywc-python-reviewer`](claude-code/agents/ywc-python-reviewer.md) | Python language-specific review |
| [`ywc-go-reviewer`](claude-code/agents/ywc-go-reviewer.md) | Go language-specific review |

All Codex agents are read-only and never edit files. They return a standardized `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`, a compact finding set, and a `Next action:` when the caller should apply or inspect something. Source TOML lives under [`codex/agents/`](codex/agents/).

---

## Claude Code Hooks

Automation hooks that run before/after Claude Code tool calls. Installed to `~/.claude/hooks/` (global) or `./.claude/hooks/` (project-local) and registered in `settings.json` automatically. Requires `jq` and `uv`.

```bash
bash scripts/install.sh --hooks                    # all hooks, globally
bash scripts/install.sh --hooks --local            # into the current project
bash scripts/install.sh --hooks cost-tracker       # specific hooks only
bash scripts/install.sh --list --hooks             # list what is available
```

| Hook                        | Event                  | Description                                                                           |
| --------------------------- | ---------------------- | ------------------------------------------------------------------------------------- |
| `block-dangerous-commands`  | `PreToolUse`           | Block dangerous shell commands (critical/high/strict levels)                          |
| `check-claude-md-freshness` | `PreToolUse`           | Verify CLAUDE.md is up to date before `git push`                                      |
| `cost-tracker`              | `PostToolUse` + `Stop` | Log tool call stats and print session summary on exit                                 |
| `notify-permission`         | `Notification`         | Send a Slack alert when Claude is waiting for permission (`CCH_SLA_WEBHOOK` required) |
| `permission-request`        | `PermissionRequest`    | Auto-approve safe tools (Read, Write, Edit)                                           |
| `protect-secrets`           | `PreToolUse`           | Block access to `.env`, SSH keys, and other secret files                              |
| `session-start`             | `SessionStart`         | Inject git status, `CONTEXT.md`, TODOs, and GitHub Issues at session start            |

Per-hook usage details: [`claude-code/hooks/README.md`](claude-code/hooks/README.md).

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a PR.

- **Bug reports & skill improvements**: open an issue or PR
- **New skills**: follow the [ywc-skill-author](claude-code/skills/ywc-skill-author/SKILL.md) guidelines
- **Translations**: see the [translation guide](CONTRIBUTING.md#translations)
- **Codex package sync**: see [Maintainer workflow for Codex skills](CONTRIBUTING.md#maintainer-workflow-for-codex-skills)

## License

MIT
