# ywc-agent-toolkit

> 本文档正在翻译中。完整文档请参阅 [English](README.md)。
>
> 欢迎帮助翻译，请创建 [Translation Issue](../../issues/new?template=translation.md)。

---

面向 Claude Code 和 Codex 的开发工作流自动化技能集合。
涵盖计划制定、规格书撰写、任务分解、代码生成、审查和发布的完整开发流程。

目前包含 38 个 Claude Code skill、37 个 Codex skill、12 个 Claude Code agent 和 7 个 Codex custom agent。

## 前提条件

插件市场和 Codex 插件安装**无需前提条件** — 工具会自动处理一切。

使用 **bash 脚本 fallback** 时，运行 `install.sh` 前需安装以下工具：

| 工具 | 用途 | 安装方式 |
| ---- | ---- | -------- |
| `git` | 克隆仓库 | 大多数系统已预装 |
| `bash ≥ 3.2` | 运行 `install.sh` | macOS / Linux 已预装 |
| `jq` | Hook 注册 | `brew install jq` / `apt-get install jq` |

**Skill 运行时**（安装时不需要）：

| 工具 | 使用的 Skill | 安装方式 |
| ---- | ------------ | -------- |
| `python3 ≥ 3.9` | Skill 运行时辅助功能：`ywc-parallel-executor`、`ywc-finish-branch`、`ywc-merge-dependabot`；Claude Code hooks 需要 Python ≥ 3.11 | macOS 12.3+ 已预装；`brew install python3` |
| `gh` CLI | 基于 PR 和 GitHub release 的 Skill/模式：`ywc-handle-pr-reviews`、`ywc-spec-writer --from-pr/--from-prs`、`ywc-release-pr-list`、`ywc-create-pr`、`ywc-finish-branch` PR 模式、`ywc-merge-dependabot`、`ywc-sequential-executor`/`ywc-parallel-executor`、`ywc-gen-testcase` | `brew install gh` / [cli.github.com](https://cli.github.com) |

---

## 安装

### Claude Code 插件市场（推荐）

```bash
# 添加市场源（仅需一次）
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

运行命令后，在 Plugin UI 的 **Marketplaces** 标签页中安装 **ywc-agent-toolkit**。
无需克隆或运行 bash，自动安装到 `~/.claude/skills/`。

### Codex CLI 插件目录

本仓库采用与 Superpowers 相同的 multi-harness packaging pattern：Claude Code 元数据位于 [`.claude-plugin/`](.claude-plugin/)，Codex 元数据位于 [`.codex-plugin/`](.codex-plugin/)。Codex 的 source of truth 是 [codex/skills](codex/skills)。仓库范围的 Codex marketplace catalog [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) 暴露 generated plugin package `plugins/ywc-agent-toolkit`，其中的 `skills/` 目录由 `bash scripts/sync-codex-plugin.sh` 从 `codex/skills` 生成，并由 `bash scripts/validate.sh` 检查是否保持最新。

将本仓库添加为 Codex plugin marketplace source 后，可以在 Codex 中安装 `ywc-agent-toolkit`，但这不表示它已经上架到官方 OpenAI-curated marketplace。

将本仓库添加为 Codex plugin marketplace source：

```bash
codex plugin marketplace add yongwoon/ywc-agent-toolkit
```

如果之前已经添加过 marketplace，请先刷新 Git snapshot：

```bash
codex plugin marketplace upgrade ywc-agent-toolkit
```

然后从已配置的 marketplace 直接安装：

```bash
codex plugin add ywc-agent-toolkit@ywc-agent-toolkit
```

或打开插件目录：

```text
codex
/plugins
```

在交互式 Codex 会话中选择 **YWC Agent Toolkit** marketplace 标签页，搜索 **ywc-agent-toolkit**，然后选择 **Install plugin**。

### Codex App Plugins 侧边栏

在 Codex App 中，从侧边栏打开 **Plugins**，选择 **YWC Agent Toolkit** source，然后搜索或浏览 **ywc-agent-toolkit**。确认插件来源是 `yongwoon/ywc-agent-toolkit`，然后在插件详情页安装。

如果你的环境无法使用 marketplace source installation，请使用下面的 bash fallback。

### Codex skill 维护 workflow

Codex skill 请在 [codex/skills](codex/skills) 中修改。`plugins/ywc-agent-toolkit/skills` 是 `codex plugin add` 使用的 generated marketplace package，不要把它作为 primary source 直接编辑。

请先安装一次 repository Git hooks，让 Codex marketplace package 自动保持同步：

```bash
bash scripts/install-git-hooks.sh
```

安装 hooks 后，当 commit 中 staged 了 `codex/skills` 变更时，会运行 `bash scripts/sync-codex-plugin.sh`，自动 stage generated package `plugins/ywc-agent-toolkit`，然后运行 `bash scripts/validate.sh`。包含 Codex skill/package 变更的 push 也会运行 stale package check 和 validation。

如果当前环境没有安装 hooks，请在 commit 前手动运行同样的命令：

```bash
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
```

bash fallback（`bash scripts/install.sh --codex`）会直接从 `codex/skills` 安装。marketplace flow（`codex plugin add ywc-agent-toolkit@ywc-agent-toolkit`）会从 generated package `plugins/ywc-agent-toolkit` 安装。

### bash 脚本 fallback

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

# 两者都安装
bash scripts/install.sh --all
```

详细说明请参阅 [README.md](README.md)。

---

## Review Skill HTML 输出模式

9 个 Review / Report skill 支持可选的 `--format html` flag，生成可直接在浏览器中打开的 self-contained HTML 报告，而非 Markdown。

**支持的 Skill：** `ywc-impl-review`、`ywc-security-audit`、`ywc-spec-validate`、`ywc-tech-research`、`ywc-incident-postmortem`、`ywc-product-review`、`ywc-ui-ux-review`、`ywc-gen-testcase`、`ywc-design-renew`

**背景：** AI 生成的超过 100 行的 Markdown 文档往往无法被完整阅读，而未被阅读的报告无法推动决策。HTML 通过颜色、severity 标记、标签页和交互控件（复选框、`Copy as Markdown`）让接收方真正阅读并采取行动。

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-gen-testcase 250 --format html   # 通过 localStorage 保存签收状态的交互式测试表
```

> **⚠️ Token 成本** — HTML 输出比 Markdown 消耗 2-4 倍的 output token，生成时间也更长。默认值为 `markdown`，仅在需要人工在浏览器中阅读报告时才启用 HTML。

---

## Custom Agent

Claude Code 包含 **12 个**用于 worker、reviewer、specialist dispatch 的 custom agent，安装到 `~/.claude/agents/`，详细信息请参阅 [`claude-code/agents/README.md`](claude-code/agents/README.md)。

Codex 包含 **7 个**补充 `ywc-*` skill 的 read-only specialist agent，安装到 `~/.codex/agents/`。

| Agent | 用途 | Sandbox |
|-------|------|---------|
| `ywc-architect` | 架构决策与权衡 advisor | `read-only` |
| `ywc-security-engineer` | 静态安全审查与威胁模型分类 | `read-only` |
| `ywc-root-cause-analyst` | 根因与故障原因分析 | `read-only` |
| `ywc-performance-engineer` | 性能审查与性能分析建议 | `read-only` |
| `ywc-typescript-reviewer` | TypeScript / JavaScript 语言专项审查 | `read-only` |
| `ywc-python-reviewer` | Python 语言专项审查 | `read-only` |
| `ywc-go-reviewer` | Go 语言专项审查 | `read-only` |

详细信息请参阅 [README.md](README.md)。
