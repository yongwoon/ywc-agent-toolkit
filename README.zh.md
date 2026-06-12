# ywc-agent-toolkit

> 本文档正在翻译中。完整文档请参阅 [English](README.md)。
>
> 欢迎帮助翻译，请创建 [Translation Issue](../../issues/new?template=translation.md)。

---

面向 Claude Code 和 Codex 的开发工作流自动化技能集合。
涵盖计划制定、规格书撰写、任务分解、代码生成、审查和发布的完整开发流程。

目前包含 36 个 Claude Code skill、37 个 Codex skill、12 个 Claude Code agent 和 7 个 Codex custom agent。

## 安装

### Claude Code 插件市场（推荐）

```bash
# 添加市场源（仅需一次）
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

运行命令后，在 Plugin UI 的 **Marketplaces** 标签页中安装 **ywc-agent-toolkit**。
无需克隆或运行 bash，自动安装到 `~/.claude/skills/`。

### Codex CLI 插件目录

本仓库在 [`.codex-plugin/`](.codex-plugin/) 下包含 Codex 插件分发所需的打包元数据，插件本地 skill 会镜像到 `.codex-plugin/skills/`，并由 `bash scripts/validate.sh` 检查是否保持最新。这表示 `ywc-agent-toolkit` 已为 Codex CLI/App 插件安装做好准备，但不表示它已经在官方 Codex 市场上架。

当包含本仓库的 Codex 插件市场或来源可用时：

```text
# Shell
codex

# 在交互式 Codex 会话中
/plugins
```

在交互式 Codex 会话中打开插件目录，搜索 `yongwoon/ywc-agent-toolkit` 的 **ywc-agent-toolkit**，然后选择 **Install plugin**。

### Codex App Plugins 侧边栏

在 Codex App 中，从侧边栏打开 **Plugins**，搜索或浏览 **ywc-agent-toolkit**，确认插件来源是 `yongwoon/ywc-agent-toolkit`，然后在插件详情页安装。

在本仓库出现在你可用的 Codex 插件来源之前，请使用下面的 bash fallback。

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

8 个 Review / Report skill 支持可选的 `--format html` flag，生成可直接在浏览器中打开的 self-contained HTML 报告，而非 Markdown。

**支持的 Skill：** `ywc-impl-review`、`ywc-security-audit`、`ywc-spec-validate`、`ywc-tech-research`、`ywc-incident-postmortem`、`ywc-product-review`、`ywc-ui-ux-review`、`ywc-gen-testcase`

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
