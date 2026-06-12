# ywc-agent-toolkit

A collection of skills for **Claude Code** and **Codex** that automates the full development workflow — from planning and spec writing to code generation, review, and release.

[한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Español](README.es.md)

## Supported Tools

| Tool        | Skills | Custom Agents | Install path                             |
| ----------- | ------ | ------------- | ---------------------------------------- |
| Claude Code | 36     | 12            | `~/.claude/skills/`, `~/.claude/agents/` |
| Codex       | 37     | 7             | `~/.codex/skills/`, `~/.codex/agents/`   |

## Installation

### Via Claude Code plugin marketplace (recommended)

```bash
# Add as a marketplace source (one-time setup)
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

After running the command, open the Plugin UI (**Marketplaces** tab) and install **ywc-agent-toolkit** from there.
Skills and Claude Code agents are installed automatically — no cloning or bash required.

### Via Codex CLI plugin directory

This repository includes Codex plugin packaging metadata under [`.codex-plugin/`](.codex-plugin/), with plugin-local skills mirrored in `.codex-plugin/skills/` and checked by `bash scripts/validate.sh`. This prepares `ywc-agent-toolkit` for Codex CLI/App plugin installation, but does not mean it is already listed in an official Codex marketplace.

When a Codex plugin marketplace or source that contains this repository is available:

```text
# Shell
codex

# Inside the interactive Codex session
/plugins
```

Inside the interactive Codex session, open the plugin directory, search for **ywc-agent-toolkit** from `yongwoon/ywc-agent-toolkit`, then choose **Install plugin**.

### Via Codex App Plugins sidebar

In the Codex App, open **Plugins** from the sidebar, search or browse for **ywc-agent-toolkit**, confirm the plugin source is `yongwoon/ywc-agent-toolkit`, then install it from the plugin details view.

Until this repository appears in a Codex plugin source available to you, use the bash fallback below.

### Via bash script fallback

```bash
YWC_REF=<release-tag-or-reviewed-commit>
git clone --branch "$YWC_REF" --depth 1 https://github.com/yongwoon/ywc-agent-toolkit.git
cd ywc-agent-toolkit
git remote get-url origin
git rev-parse --verify HEAD

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

### Install only custom agents

```bash
# All 12 Claude Code worker/reviewer/specialist agents
bash scripts/install.sh --cc-agents

# All 7 read-only specialist agents
bash scripts/install.sh --codex-agents

# Selected agents
bash scripts/install.sh --cc-agents ywc-backend-coder ywc-qa-engineer
bash scripts/install.sh --codex-agents ywc-security-engineer ywc-architect

# Skills only, leaving agents untouched
bash scripts/install.sh --cc --skip-agents
bash scripts/install.sh --codex --skip-agents
```

### List available items

```bash
bash scripts/install.sh --list
bash scripts/install.sh --list --cc
bash scripts/install.sh --list --codex
bash scripts/install.sh --list --cc-agents
bash scripts/install.sh --list --codex-agents
```

### Environment variables

| Variable            | Default            | Description                             |
| ------------------- | ------------------ | --------------------------------------- |
| `CLAUDE_SKILLS_DIR` | `~/.claude/skills` | Override Claude Code install path       |
| `CLAUDE_AGENTS_DIR` | `~/.claude/agents` | Override Claude Code agent install path |
| `CODEX_HOME`        | `~/.codex`         | Override Codex home path                |

Restart Claude Code or Codex after installation for skills to take effect.

---

## Skills

Most `ywc-*` skills are available for both Claude Code and Codex. The Codex
versions include Codex-compatible frontmatter and tool guidance.

### Planning & Spec

| Skill                     | Description                                                                   |
| ------------------------- | ----------------------------------------------------------------------------- |
| `ywc-plan`                | Convert a rough idea into `plan.md` (Small) or a Spec document (Medium/Large) |
| `ywc-spec-writer`         | Write and update spec documents (`docs/specification/`)                       |
| `ywc-spec-validate`       | Validate spec quality (Completeness / Consistency / Feasibility)              |
| `ywc-tech-research`       | Research libraries and compare technical approaches                           |
| `ywc-ubiquitous-language` | Create and maintain a domain ubiquitous language dictionary                   |
| `ywc-brainstorm`          | Shape rough ideas before writing a formal plan or spec                        |
| `ywc-confidence-gate`     | Check readiness and risk before starting substantial implementation           |
| `ywc-onboard-repo`        | Generate repository onboarding context for unfamiliar projects                |

### Task & Execution

| Skill                     | Description                                                                                                     |
| ------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `ywc-task-generator`      | Decompose a spec into dependency-safe tasks                                                                     |
| `ywc-sequential-executor` | Execute tasks sequentially (Branch → Implement → Commit → PR → Merge)                                           |
| `ywc-parallel-executor`   | Execute tasks in parallel using Git worktree isolation                                                          |
| `ywc-code-gen`            | Generate Backend + Frontend + QA code in parallel                                                               |
| `ywc-agentic`             | Autonomously orchestrate the ywc-\* pipeline from a goal (Plan → Execute → Evaluate → Repeat, max 3 iterations) |
| `ywc-tdd-ritual`          | Drive feature and bugfix work through a red-green-refactor loop                                                 |
| `ywc-worktrees`           | Create, audit, prune, and resolve worktree-based task isolation                                                 |

### Review & Verification

| Skill                   | Description                                                              |
| ----------------------- | ------------------------------------------------------------------------ |
| `ywc-impl-review`       | Verify implementation across Spec / Security / QA axes                   |
| `ywc-security-audit`    | Security audit based on OWASP Top 10                                     |
| `ywc-ui-ux-review`      | UI/UX review (IA + Visual design + WCAG 2.2 AA)                          |
| `ywc-product-review`    | Product feedback across 5 business dimensions                            |
| `ywc-gen-testcase`      | Generate test sheets from PRs or tasks                                   |
| `ywc-e2e-test-strategy` | Design Playwright E2E test strategy                                      |
| `ywc-debug-rootcause`   | Investigate bugs, failed tests, and build failures to the root cause     |
| `ywc-receive-review`    | Triage and apply human or automated review feedback                      |
| `ywc-refactor-clean`    | Remove dead code, unused exports, stale files, and unused dependencies   |
| `ywc-verify-done`       | Verify tests, builds, and completion evidence before declaring work done |

### Git & Release

| Skill                         | Description                                              |
| ----------------------------- | -------------------------------------------------------- |
| `ywc-commit`                  | Stage and commit session work                            |
| `ywc-create-pr`               | Commit and create a Draft PR                             |
| `ywc-handle-pr-reviews`       | Automate PR review responses                             |
| `ywc-finish-branch`           | Full branch delivery (CI → merge → cleanup)              |
| `ywc-merge-dependabot`        | Auto-merge Dependabot PRs                                |
| `ywc-release-pr-list`         | Summarize PRs included in a release                      |
| `ywc-changelog-release-notes` | Generate CHANGELOG entries and user-facing release notes |

### Documentation & Other

| Skill                     | Description                                               |
| ------------------------- | --------------------------------------------------------- |
| `ywc-project-scaffold`    | Generate directory structure for any language/framework   |
| `ywc-project-docs`        | Generate project documentation in Korean or Japanese      |
| `ywc-incident-postmortem` | Write a structured postmortem after a production incident |
| `ywc-skill-author`        | (Meta) Rules for authoring new `ywc-*` skills             |

### Codex-only

| Skill               | Description                                                        |
| ------------------- | ------------------------------------------------------------------ |
| `ywc-team-assemble` | Split explicitly authorized work across specialist Codex subagents |

---

## Custom Agents

Claude Code also ships 12 custom agents for worker, reviewer, and specialist dispatch. They install to `~/.claude/agents/` and are documented in [`claude-code/agents/README.md`](claude-code/agents/README.md).

Seven read-only specialist agents complement the `ywc-*` skills. They are installed to `~/.codex/agents/` (override with `CODEX_HOME`) as individual TOML files, and Codex loads one custom agent per file.

| Agent                      | Purpose                                          | Sandbox     |
| -------------------------- | ------------------------------------------------ | ----------- |
| `ywc-architect`            | Architectural decision and trade-off advisor     | `read-only` |
| `ywc-security-engineer`    | Static security review and threat-model triage   | `read-only` |
| `ywc-root-cause-analyst`   | Root-cause and incident-cause analysis           | `read-only` |
| `ywc-performance-engineer` | Performance review and profiling recommendations | `read-only` |
| `ywc-typescript-reviewer`  | TypeScript / JavaScript language-specific review | `read-only` |
| `ywc-python-reviewer`      | Python language-specific review                  | `read-only` |
| `ywc-go-reviewer`          | Go language-specific review                      | `read-only` |

All Codex agents are read-only; they return a standardized `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`, a compact verdict or finding set, and a `Next action:` when the caller should apply or inspect something. They never edit files. Source TOML lives under [`codex/agents/`](codex/agents/).

---

## HTML Output Mode for Review Skills

Eight review and report skills support an opt-in `--format html` flag that produces a self-contained, browser-ready HTML report instead of Markdown.

**Supported skills:** `ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`, `ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`

**Why HTML?** AI-generated Markdown documents longer than ~100 lines are rarely read end to end — an unread report cannot drive a decision. HTML adds color, severity coding, tabs, and interactive controls (checkboxes, `Copy as Markdown`), so the human on the other end actually reads and acts on the output.

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-security-audit --code api/src/ --format html
/ywc-gen-testcase 250 --format html   # interactive testsheet with localStorage sign-off
```

> **⚠️ Token cost** — HTML output uses 2–4× the output tokens of Markdown and takes longer to generate. The default is `markdown`; enable HTML only for reports a human will read in a browser.

Details: [`references/html-output.md`](claude-code/skills/references/html-output.md).

---

## Recommended Development Pipeline

This spine mirrors how the skills are actually invoked day to day, not the full
catalog. One planning pass, a spec gate, task decomposition, then the executor as
the workhorse — for each task it delivers end to end via `ywc-finish-branch`,
folding conformance review (`--review`), PR creation, bot-review handling, and
merge in as sub-steps, so those rarely run standalone in the task-driven flow.

```
1. ywc-plan                    # rough idea → plan.md (Small) or Spec routing (Medium/Large)
     ↓
2. ywc-spec-writer             # write / update the spec          ┐ Medium / Large
     ↓                                                            │ (Small skips
   ywc-spec-validate           # gate spec quality before tasks   ┘  straight to 4)
     ↓
3. ywc-task-generator          # decompose spec into dependency-safe tasks
     ↓
4. ywc-sequential-executor 000020-010..000025-010 --review --base-branch <feature>
     #  the workhorse — runs a task range. Each task gets its own branch and PR,
     #  delivered end to end via ywc-finish-branch:
     #    branch → implement → verify → impl-review (--review)
     #    → open PR → CI → handle bot review → merge → cleanup
     #  common flags: --base-branch · --draft · --local-merge · --review · --per-task-pr
     #  (ywc-parallel-executor is the worktree-isolated alternative)
     ↓
5. ywc-gen-testcase pr <N>     # generate a QA test sheet against a task's PR
```

**Ad-hoc / non-task changes** skip the executor and deliver manually: `ywc-create-pr` opens a
draft PR, then `ywc-handle-pr-reviews` drives bot / human review to green. `ywc-handle-pr-reviews`
is also what you re-run whenever new review comments land on an open PR — task-driven or not.

Also reached for in real work: `ywc-ubiquitous-language` (domain glossary, before or during
spec), and at release time `ywc-release-pr-list` + `ywc-changelog-release-notes`.

The remaining skills are situational, not part of every run — `ywc-debug-rootcause` (a test
or build fails and the cause is unclear), `ywc-tdd-ritual` (strict red-green-refactor),
`ywc-tech-research` (compare approaches before deciding), `ywc-impl-review` (standalone
conformance review outside the executor), `ywc-agentic` (autonomously orchestrate the whole
pipeline from a goal), and others in the [Skills](#skills) table above.

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

| Hook                        | Event                  | Description                                                                           |
| --------------------------- | ---------------------- | ------------------------------------------------------------------------------------- |
| `block-dangerous-commands`  | `PreToolUse`           | Block dangerous shell commands (critical/high/strict levels)                          |
| `check-claude-md-freshness` | `PreToolUse`           | Verify CLAUDE.md is up to date before `git push`                                      |
| `cost-tracker`              | `PostToolUse` + `Stop` | Log tool call stats and print session summary on exit                                 |
| `notify-permission`         | `Notification`         | Send a Slack alert when Claude is waiting for permission (`CCH_SLA_WEBHOOK` required) |
| `permission-request`        | `PermissionRequest`    | Auto-approve safe tools (Read, Write, Edit)                                           |
| `protect-secrets`           | `PreToolUse`           | Block access to `.env`, SSH keys, and other secret files                              |
| `session-start`             | `SessionStart`         | Inject git status, `CONTEXT.md`, TODOs, and GitHub Issues at session start            |

### Dependencies

| Dependency | Required               | Install                                            |
| ---------- | ---------------------- | -------------------------------------------------- |
| `jq`       | Yes — JSON merge       | `brew install jq` / `apt-get install jq`           |
| `uv`       | Yes — run Python hooks | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

For per-hook usage details see [`claude-code/hooks/README.md`](claude-code/hooks/README.md).

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a PR.

- **Bug reports & skill improvements**: open an issue or PR
- **New skills**: follow the [ywc-skill-author](claude-code/skills/ywc-skill-author/SKILL.md) guidelines
- **Translations**: see the [translation guide](CONTRIBUTING.md#translations)

## License

MIT
