# ywc-agent-toolkit

> 本文档正在翻译中。完整内容请参阅 [English](README.md)。
>
> 如果您想参与翻译，请创建 [Translation Issue](../../issues/new?template=translation.md)。

---

面向 Claude Code 与 Codex 的开发工作流自动化技能集，覆盖从规划、规格编写、任务拆解到代码生成、评审与发布的完整流程。

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [Español](README.es.md)

> 📖 **[文档 & 指南](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/)** — 本 README 是简要导览。前提条件、安装、完整 skill 参考以及分步工作流指南都在指南中。

| 您想了解 | 指南页面 |
| -------- | -------- |
| 5 分钟交付第一个功能 | [03. 快速开始](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/03-quickstart/) |
| 该运行哪个 skill、按什么顺序 | [17. 完整 Skill 参考](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/14-skill-reference/) |
| 前提条件、安装路径、环境变量 | [18. 前提条件与安装](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/15-prerequisites-installation/) |
| 小改动 / 多任务 / 自主循环 | [04](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/04-general-cycle-small/) · [05](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/05-general-cycle-medium-large/) · [06](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/06-agentic-autonomous-loop/) |

## 支持的工具

| 工具        | Skills | Custom Agents | 安装路径                                  |
| ----------- | ------ | ------------- | ---------------------------------------- |
| Claude Code | 42     | 12            | `~/.claude/skills/`, `~/.claude/agents/` |
| Codex       | 52     | 8             | `~/.codex/skills/`, `~/.codex/agents/`   |

---

## 快速开始

### Claude Code

通过插件市场安装 — 无需 clone，也没有前提条件:

```bash
/plugin marketplace add yongwoon/ywc-agent-toolkit    # 1. 注册市场源
/plugin install ywc-agent-toolkit@ywc-agent-toolkit   # 2. 安装插件
```

`marketplace add` 仅注册来源，之后还需执行 `/plugin install`，或在 Plugin UI 的 **Marketplaces** 标签页中安装。安装后重启 Claude Code，skill 才会出现。

### Codex

```bash
codex plugin marketplace add yongwoon/ywc-agent-toolkit   # 1. 注册市场源
codex plugin add ywc-agent-toolkit@ywc-agent-toolkit      # 2. 安装插件
```

若此前已添加过该市场，请先用 `codex plugin marketplace upgrade ywc-agent-toolkit` 刷新其 Git 快照。您也可以运行 `codex` 后打开 `/plugins`，在 **YWC Agent Toolkit** 标签页中安装。

若使用 **Codex App**，请在侧边栏打开 **Plugins**，选择 **YWC Agent Toolkit** 源，确认来源为 `yongwoon/ywc-agent-toolkit`，然后在插件详情页安装。

### 然后运行 skill

两种工具提供相同的命令:

```bash
/ywc-onboard-repo           # 数分钟内理解陌生代码库
/ywc-plan                   # 把粗略想法变成 plan 或 spec
/ywc-debug-rootcause        # 追踪缺陷的根本原因
/ywc-impl-review            # 从 spec / 安全 / 质量角度评审代码
/ywc-agentic                # 由一个 goal 自主运行完整 pipeline
```

→ 前提条件、bash 脚本 fallback、安装路径以及 `CLAUDE_SKILLS_DIR` / `CLAUDE_AGENTS_DIR` / `CODEX_HOME` 覆盖方式，请参阅 [前提条件与安装](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/15-prerequisites-installation/)。

### 指南中未涵盖的安装选项

```bash
# 仅安装指定 skill
bash scripts/install.sh --cc ywc-plan ywc-commit ywc-create-pr
bash scripts/install.sh --codex ywc-plan ywc-commit ywc-ui-ux-review

# 仅安装选定 agent，或只装 skill 不装 agent
bash scripts/install.sh --cc-agents ywc-backend-coder ywc-qa-engineer
bash scripts/install.sh --cc --skip-agents
```

### Codex 输出语言默认值

Codex 专用的 `ywc-setup` 用于设置 Codex `ywc-*` skill 的 artifact 语言默认值:

```bash
ywc-setup --scope project --lang ko
ywc-setup --scope user --lang ja
```

解析顺序为 explicit `--lang` > project `.codex/ywc.json` > project guidance（`AGENTS.md` / `CODEX.md` / `CLAUDE.md`）> user `~/.codex/ywc.json` > 询问用户。不支持 session 级默认值。

---

## Skills

大多数 `ywc-*` skill 在 Claude Code 与 Codex 上均可使用。按目的整理的完整目录位于 [完整 Skill 参考](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/14-skill-reference/)。从这里开始:

| 目标 | Skills |
| ---- | ------ |
| 把想法变成 plan 或 spec | [`ywc-plan`](claude-code/skills/ywc-plan/README.md) → [`ywc-spec-writer`](claude-code/skills/ywc-spec-writer/README.md) |
| 理解陌生的代码库 | [`ywc-onboard-repo`](claude-code/skills/ywc-onboard-repo/README.md) |
| 拆解为依赖安全的任务 | [`ywc-task-generator`](claude-code/skills/ywc-task-generator/README.md) |
| 端到端实现任务 | [`ywc-sequential-executor`](claude-code/skills/ywc-sequential-executor/README.md) / [`ywc-parallel-executor`](claude-code/skills/ywc-parallel-executor/README.md) |
| 由 goal 运行完整 pipeline | [`ywc-agentic`](claude-code/skills/ywc-agentic/README.md) |
| 定位缺陷的根本原因 | [`ywc-debug-rootcause`](claude-code/skills/ywc-debug-rootcause/README.md) |
| 评审代码质量与安全 | [`ywc-impl-review`](claude-code/skills/ywc-impl-review/README.md), [`ywc-security-audit`](claude-code/skills/ywc-security-audit/README.md) |
| 创建 PR 并处理评审意见 | [`ywc-create-pr`](claude-code/skills/ywc-create-pr/README.md) → [`ywc-handle-pr-reviews`](claude-code/skills/ywc-handle-pr-reviews/README.md) |
| 生成 QA 测试单 | [`ywc-gen-testcase`](claude-code/skills/ywc-gen-testcase/README.md) |
| 撰写发布说明 | [`ywc-release-pr-list`](claude-code/skills/ywc-release-pr-list/README.md) + [`ywc-changelog-release-notes`](claude-code/skills/ywc-changelog-release-notes/README.md) |
| 编写新的 `ywc-*` skill | [`ywc-skill-author`](claude-code/skills/ywc-skill-author/README.md) |

所有 skill 目录位于 [`claude-code/skills/`](claude-code/skills) 与 [`codex/skills/`](codex/skills)，每个都有各自的 README。

**它们如何衔接:** `ywc-plan` → （Medium/Large）`ywc-spec-writer` → `ywc-spec-ready` → `ywc-task-generator` → `ywc-sequential-executor` / `ywc-parallel-executor`，由 executor 端到端交付每个任务。临时性改动不经过 executor: `ywc-create-pr` → `ywc-handle-pr-reviews`。各路径的命令与标志详见 [核心 pipeline 指南](https://yongwoon.github.io/ywc-agent-toolkit-lp/zh/guidebook/02-core-concepts/)。

### HTML 输出模式

九个 Review / Report skill 支持 `--format html` 标志，生成可直接在浏览器打开的自包含 HTML 报告，而非 Markdown。配色、severity coding、标签页与交互控件让接收方真正愿意阅读并采取行动。

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-gen-testcase 250 --format html   # 带 localStorage 签核的交互式测试单
```

> **⚠️ Token 成本** — HTML 输出消耗的 output token 约为 Markdown 的 2～4 倍。默认值为 `markdown`，请仅在人会用浏览器阅读的报告上启用。

支持的 skill 与详情: [`references/html-output.md`](claude-code/skills/references/html-output.md)。

---

## Custom Agent

Claude Code 提供 12 个用于 worker、reviewer 与 specialist dispatch 的 custom agent，安装至 `~/.claude/agents/`，详见 [`claude-code/agents/README.md`](claude-code/agents/README.md)。

Codex 提供与之对应的 7 个只读 specialist agent，安装至 `~/.codex/agents/`（可用 `CODEX_HOME` 覆盖），每个 agent 一个 TOML 文件:

| Agent | 用途 |
| ----- | ---- |
| [`ywc-architect`](claude-code/agents/ywc-architect.md) | 架构决策与权衡顾问 |
| [`ywc-security-engineer`](claude-code/agents/ywc-security-engineer.md) | 静态安全评审与 threat model 分级 |
| [`ywc-root-cause-analyst`](claude-code/agents/ywc-root-cause-analyst.md) | 根因与故障原因分析 |
| [`ywc-performance-engineer`](claude-code/agents/ywc-performance-engineer.md) | 性能评审与性能分析建议 |
| [`ywc-typescript-reviewer`](claude-code/agents/ywc-typescript-reviewer.md) | TypeScript / JavaScript 语言专项评审 |
| [`ywc-python-reviewer`](claude-code/agents/ywc-python-reviewer.md) | Python 语言专项评审 |
| [`ywc-go-reviewer`](claude-code/agents/ywc-go-reviewer.md) | Go 语言专项评审 |

所有 Codex agent 均为只读，绝不修改文件。它们返回标准化的 `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`、精简的 finding 集合，以及当调用方需要应用或查看时的 `Next action:`。源 TOML 位于 [`codex/agents/`](codex/agents/)。

---

## Claude Code Hooks

在 Claude Code tool 调用前后运行的自动化 hook。安装至 `~/.claude/hooks/`（全局）或 `./.claude/hooks/`（项目本地），并自动注册到 `settings.json`。需要 `jq` 与 `uv`。

```bash
bash scripts/install.sh --hooks                    # 全局安装全部 hook
bash scripts/install.sh --hooks --local            # 安装到当前项目
bash scripts/install.sh --hooks cost-tracker       # 仅安装指定 hook
bash scripts/install.sh --list --hooks             # 列出可用 hook
```

| Hook                        | Event                  | 说明                                                                    |
| --------------------------- | ---------------------- | ----------------------------------------------------------------------- |
| `block-dangerous-commands`  | `PreToolUse`           | 拦截危险的 shell 命令（critical/high/strict 级别）                       |
| `check-claude-md-freshness` | `PreToolUse`           | 在 `git push` 前校验 CLAUDE.md 是否最新                                  |
| `cost-tracker`              | `PostToolUse` + `Stop` | 记录 tool 调用统计，并在退出时输出会话摘要                                |
| `notify-permission`         | `Notification`         | 等待授权时发送 Slack 提醒（需要 `CCH_SLA_WEBHOOK`）                      |
| `permission-request`        | `PermissionRequest`    | 自动批准安全的 tool（Read、Write、Edit）                                 |
| `protect-secrets`           | `PreToolUse`           | 拦截对 `.env`、SSH 密钥等机密文件的访问                                  |
| `session-start`             | `SessionStart`         | 会话开始时注入 git status、`CONTEXT.md`、TODO 与 GitHub Issue            |

各 hook 的用法详情: [`claude-code/hooks/README.md`](claude-code/hooks/README.md)。

---

## 参与贡献

欢迎贡献！提交 PR 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

- **缺陷报告与 skill 改进**: 提交 issue 或 PR
- **新增 skill**: 遵循 [ywc-skill-author](claude-code/skills/ywc-skill-author/SKILL.md) 指南
- **翻译**: 参阅 [翻译指南](CONTRIBUTING.md#translations)
- **Codex 包同步**: 参阅 [Codex skill 维护 workflow](CONTRIBUTING.md#maintainer-workflow-for-codex-skills)

## License

MIT
