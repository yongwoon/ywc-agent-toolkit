<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-spec-writer

项目规范编写工具。以人类可读的 Markdown 格式创建并维护 `docs/specification/` 目录。面向开发者和非开发者编写——不含程序代码，只包含目标、功能、数据、用户流程和非功能性需求。

## 使用场景

- **新项目**：在没有任何规范的情况下编写第一份完整规范
- **基于任务的更新**：将 `ywc-task-generator` 的单个任务文档反映到规范中
- **任务范围 / 多任务更新**：一次性反映多个任务（范围、glob 或多 ID）
- **基于 PR 的更新**：从一个或多个 PR diff 及其 narrative 更新规范
- **提交后同步**：代码变更后同步规范
- **完整刷新**：从当前代码库重新生成整个规范

## 使用方法

```bash
/ywc-spec-writer                          # 自动模式（基于提交的更新）
/ywc-spec-writer --full                   # 完整规范生成（需要确认）
/ywc-spec-writer --update                 # 重新生成所有章节
/ywc-spec-writer --from-task tasks/000002-010-api-user/
/ywc-spec-writer --from-tasks 000002-010..000003-020   # 任务范围（可跨阶段）
/ywc-spec-writer --from-tasks '000002-*' 000003-010    # Glob + 单个 ID 混合
/ywc-spec-writer --from-commit HEAD
/ywc-spec-writer --from-pr 42                          # 单个 PR
/ywc-spec-writer --from-prs 42 43 51                   # 多个 PR（union diff）
/ywc-spec-writer --setup-hook             # 安装 git hook
/ywc-spec-writer --lang ja                # 以日语输出
```

## 输入参数

- （可选）`--full` / `--update` — 完整生成或刷新
- （可选）`--from-task <path>` — 单个任务目录路径
- （可选）`--from-tasks <id-or-pattern> ...` — 任务范围 / glob / 多 ID（搜索 active + completed）
- （可选）`--from-commit <ref>` — 提交引用（默认：`HEAD`）
- （可选）`--from-pr <num>` — 单个 PR（需要 gh CLI）
- （可选）`--from-prs <num> ...` — 多个 PR union diff（重复文件自动去重）
- （可选）`--lang ko|ja|en` — 输出语言（默认：`ko`）
- （可选）`--setup-hook` — 安装 git pre-commit hook

> 使用 `--from-pr` / `--from-prs` 时需要安装并认证 `gh` CLI。PR title / body / `headRefOid` 将作为 narrative context 和 audit trail 记录到规范中。

## 输出

```
docs/specification/
├── README.md              # 索引 + 变更日志
├── 01-overview.md         # 项目概述
├── 02-features.md         # 功能需求（用户故事格式）
├── 03-data.md             # 数据模型
├── 04-interfaces.md       # 外部接口
├── 05-user-flows.md       # 用户流程
├── 06-requirements.md     # 非功能性需求
└── 07-glossary.md         # 术语表
```

## 相关技能

- `ywc-plan` — 生成功能规范，作为本技能的输入
- `ywc-spec-validate` — 验证已编写的规范
- `ywc-task-generator` — 将审查后的规范分解为任务
- `ywc-ubiquitous-language` — 将规范词汇与领域术语对齐
