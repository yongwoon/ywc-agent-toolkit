# ywc-agent-toolkit

A collection of skills for **Claude Code** and **Codex** that automates the full development workflow — from planning and spec writing to code generation, review, and release.

[日本語](README.ja.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [Español](README.es.md)

## Supported Tools

| Tool | Skills | Install path |
|------|--------|-------------|
| Claude Code | 26 | `~/.claude/skills/` |
| Codex | 27 | `~/.codex/skills/` |

## Installation

### Via Claude Code plugin marketplace (recommended)

```bash
# Add as a marketplace source (one-time setup)
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

After running the command, open the Plugin UI (**Marketplaces** tab) and install **ywc-agent-toolkit** from there.
Skills are installed to `~/.claude/skills/` automatically — no cloning or bash required.

### Via bash script

```bash
git clone https://github.com/yongwoon/ywc-agent-toolkit.git
cd ywc-agent-toolkit

# Claude Code
bash scripts/install.sh --cc

# Codex
bash scripts/install.sh --codex

# Both
bash scripts/install.sh --all
```

### Install specific skills only

```bash
bash scripts/install.sh --cc ywc-plan ywc-commit ywc-create-pr
bash scripts/install.sh --codex ywc-plan ywc-commit ywc-ui-ux-review
```

### List available skills

```bash
bash scripts/install.sh --list
bash scripts/install.sh --list --cc
bash scripts/install.sh --list --codex
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_SKILLS_DIR` | `~/.claude/skills` | Override Claude Code install path |
| `CODEX_HOME` | `~/.codex` | Override Codex home path |

Restart Claude Code or Codex after installation for skills to take effect.

---

## Skills

Most `ywc-*` skills are available for both Claude Code and Codex. The Codex
versions include Codex-compatible frontmatter and tool guidance.

### Planning & Spec

| Skill | Description |
|-------|-------------|
| `ywc-plan` | Convert a rough idea into `plan.md` (Small) or a Spec document (Medium/Large) |
| `ywc-spec-writer` | Write and update spec documents (`docs/specification/`) |
| `ywc-spec-validate` | Validate spec quality (Completeness / Consistency / Feasibility) |
| `ywc-tech-research` | Research libraries and compare technical approaches |
| `ywc-ubiquitous-language` | Create and maintain a domain ubiquitous language dictionary |

### Task & Execution

| Skill | Description |
|-------|-------------|
| `ywc-task-generator` | Decompose a spec into dependency-safe tasks |
| `ywc-sequential-executor` | Execute tasks sequentially (Branch → Implement → Commit → PR → Merge) |
| `ywc-parallel-executor` | Execute tasks in parallel using Git worktree isolation |
| `ywc-code-gen` | Generate Backend + Frontend + QA code in parallel |
| `ywc-agentic` | Autonomously orchestrate the ywc-* pipeline from a goal (Plan → Execute → Evaluate → Repeat, max 3 iterations) |

### Review & Verification

| Skill | Description |
|-------|-------------|
| `ywc-impl-review` | Verify implementation across Spec / Security / QA axes |
| `ywc-security-audit` | Security audit based on OWASP Top 10 |
| `ywc-ui-ux-review` | UI/UX review (IA + Visual design + WCAG 2.2 AA) |
| `ywc-product-review` | Product feedback across 5 business dimensions |
| `ywc-gen-testcase` | Generate test sheets from PRs or tasks |
| `ywc-e2e-test-strategy` | Design Playwright E2E test strategy |

### Git & Release

| Skill | Description |
|-------|-------------|
| `ywc-commit` | Stage and commit session work |
| `ywc-create-pr` | Commit and create a Draft PR |
| `ywc-handle-pr-reviews` | Automate PR review responses |
| `ywc-finish-branch` | Full branch delivery (CI → merge → cleanup) |
| `ywc-merge-dependabot` | Auto-merge Dependabot PRs |
| `ywc-release-pr-list` | Summarize PRs included in a release |
| `ywc-changelog-release-notes` | Generate CHANGELOG entries and user-facing release notes |

### Documentation & Other

| Skill | Description |
|-------|-------------|
| `ywc-project-scaffold` | Generate directory structure for any language/framework |
| `ywc-project-docs` | Generate project documentation in Korean or Japanese |
| `ywc-incident-postmortem` | Write a structured postmortem after a production incident |
| `ywc-skill-author` | (Meta) Rules for authoring new `ywc-*` skills |

### Codex-only

| Skill | Description |
|-------|-------------|
| `ywc-team-assemble` | Split explicitly authorized work across specialist Codex subagents |

---

## Recommended Development Pipeline

```
ywc-tech-research        # (optional) research before starting
  ↓
ywc-plan                 # rough idea → plan.md or spec
  ↓
ywc-spec-writer          # write or update the spec
  ↓
ywc-spec-validate        # validate spec quality
  ↓
ywc-task-generator       # decompose spec into tasks
  ↓
ywc-sequential-executor  # or ywc-parallel-executor
  ↓
ywc-impl-review          # verify implementation
  ↓
ywc-gen-testcase         # generate test sheet
  ↓
ywc-commit → ywc-create-pr → ywc-handle-pr-reviews
```

---

## Claude Code Hooks

Automation hooks that run before/after Claude Code tool calls. Hooks are installed
to `~/.claude/hooks/` (global) or `./.claude/hooks/` (project-local) and registered
in `settings.json` automatically.

### Install hooks

```bash
# Install all hooks globally (default)
bash scripts/install.sh --hooks

# Install all hooks into the current project
bash scripts/install.sh --hooks --local

# Install specific hooks only
bash scripts/install.sh --hooks block-dangerous-commands cost-tracker
bash scripts/install.sh --hooks --local session-start
```

### List available hooks

```bash
bash scripts/install.sh --list --hooks
```

### Available hooks

| Hook | Event | Description |
|------|-------|-------------|
| `block-dangerous-commands` | `PreToolUse` | Block dangerous shell commands (critical/high/strict levels) |
| `check-claude-md-freshness` | `PreToolUse` | Verify CLAUDE.md is up to date before `git push` |
| `cost-tracker` | `PostToolUse` + `Stop` | Log tool call stats and print session summary on exit |
| `notify-permission` | `Notification` | Send a Slack alert when Claude is waiting for permission (`CCH_SLA_WEBHOOK` required) |
| `permission-request` | `PermissionRequest` | Auto-approve safe tools (Read, Write, Edit) |
| `protect-secrets` | `PreToolUse` | Block access to `.env`, SSH keys, and other secret files |
| `session-start` | `SessionStart` | Inject git status, `CONTEXT.md`, TODOs, and GitHub Issues at session start |

### Dependencies

| Dependency | Required | Install |
|-----------|----------|---------|
| `jq` | Yes — JSON merge | `brew install jq` / `apt-get install jq` |
| `uv` | Yes — run Python hooks | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

For per-hook usage details see [`claude-code/hooks/README.md`](claude-code/hooks/README.md).

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a PR.

- **Bug reports & skill improvements**: open an issue or PR
- **New skills**: follow the [ywc-skill-author](claude-code/skills/ywc-skill-author/SKILL.md) guidelines
- **Translations**: see the [translation guide](CONTRIBUTING.md#translations)

## License

MIT
