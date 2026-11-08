<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# Merge Dependabot 技能（Codex）

## 概述

此技能安全地批量合并由 Dependabot 创建的拉取请求。
可从 Claude Code 和 Codex CLI 使用。

## 功能

- 合并所有 Dependabot PR 或仅安全相关的 PR
- 为 Dockerfile `FROM` 更改、主要版本升级和 CI 状态运行合并前安全检查
- 仅通过 `@dependabot rebase` 解决合并冲突（永不手动解决），等待变基后的 head 的 CI，并固定合并到已验证的 head（`--match-head-commit`）
- 默认按升序 PR 号顺序处理 PR
- **并行自动模式**：将 PR 分组到锁文件生态系统车道，每条车道保持一个活跃的自动合并 PR，以减少大批次的实际时间；每次自动合并启动首先确认 PR 的基础分支具有必需的状态检查，未确认的 PR 进入最终顺序传递
- 输出最终摘要报告

## 使用

### Claude Code

```text
/ywc-merge-dependabot                          # 所有 PR，顺序
/ywc-merge-dependabot security                 # 仅安全 PR，顺序
/ywc-merge-dependabot parallel-auto            # 所有 PR，生态系统车道自动合并
/ywc-merge-dependabot security parallel-auto   # 仅安全 PR，生态系统车道自动合并
```

### Codex CLI

```text
使用 $ywc-merge-dependabot 来合并所有开放的 Dependabot 拉取请求。
使用 $ywc-merge-dependabot security 仅合并安全相关的 Dependabot PR。
使用 $ywc-merge-dependabot parallel-auto 通过生态系统车道自动合并调度来合并大批次。
使用 $ywc-merge-dependabot security parallel-auto 将安全作用域与并行自动执行标志结合。
```

## 先决条件

- 已安装并认证 GitHub CLI（`gh`）
- 对目标仓库有合并权限
- 对于 `parallel-auto`：仓库已启用"允许自动合并"。如果禁用，该技能将回退到顺序模式。

## 模式

此技能支持两个正交标志。

**作用域标志** — 目标 PR：

| 令牌 | 作用域 |
| --- | --- |
| `security` | 仅安全相关的 Dependabot PR |
| _（无）_ | 所有 Dependabot PR |

**执行标志** — 处理策略：

| 令牌 | 执行 | 何时使用 |
| --- | --- | --- |
| `parallel-auto` | 生态系统车道 + 每条车道一个活跃自动合并 PR | 五个或以上 PR 分散在多个生态系统中 |
| _（无）_ | 按升序 PR 号顺序 | 小批次或严格的分支保护环境 |

## 跳过条件

| 条件 | 原因 |
| --- | --- |
| Dockerfile `FROM` 更改 | 容器基础镜像更改需要手动审查 |
| 主要版本升级 | 破坏性更改风险 |
| CI 未通过 | 防止合并失败的构建/测试 |

## 结果格式

```text
模式: parallel-auto (security)
处理的生态系统组: npm (3), github-actions (2), python (2)

- 已合并    (npm)            : #123 Bump axios from 1.6.0 to 1.7.2
- 已跳过   (Dockerfile)     : #127 Bump node from 18 to 20
- 已跳过   (主要版本升级) : #130 Bump webpack from 4.x to 5.x
- 失败    (车道停滞)   : #132 Bump express from 4.18.0 to 4.19.2 - 30 分钟后冲突
```

顺序模式仍然打印 `Mode` 行，但省略 `Ecosystem groups` 标题和每个 PR 的生态系统注释。

## 文件结构

```text
ywc-merge-dependabot/
├── README.md
├── README.en.md / README.ja.md / README.ko.md
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    ├── group-by-ecosystem.py
    ├── check-base-required-checks.sh
    └── test_merge_dependabot_scripts.py
```

## 相关技能

- [ywc-create-pr](../ywc-create-pr/SKILL.md) — 创建 PR
- [ywc-handle-pr-reviews](../ywc-handle-pr-reviews/SKILL.md) — 处理 PR 审查评论
- [ywc-release-pr-list](../ywc-release-pr-list/SKILL.md) — 生成发布 PR 列表

## 操作安全性

仅在 Dockerfile diff 块中检测更改的 FROM 指令；查询/解析器故障保持未解决。变基/CI 轮询保留一个运行范围内的 1800 秒期限和块间的完整状态；超时是故障。显式调用是首选元数据，而不是运行时强制实施。
