<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# Release PR List

一个 Codex Skill，用于提取发布 PR 中包含的 PR 列表，按作者分组并更新 PR 描述。

## 概述

创建如 `develop` → `main` 的发布 PR 时，此 Skill 从提交标题中提取 PR 编号，查找其作者，并重写 `## PR LIST` 部分。

### 主要特性

- 从提交标题中的 `#<编号>` 模式提取 PR 编号
- 按作者登录名分组 PR 并按字母顺序排序
- 每次运行时，询问用户是否为每个 PR 追加单行摘要；仅在确认后才从 PR 标题派生简洁摘要
- 保留现有描述，仅替换 `## PR LIST` 部分
- 多次运行时保持幂等性

## 使用方法

```text
/release-pr-list 301
```

自然语言触发条件在 [SKILL.md](./SKILL.md) 中定义。

## 前提条件

- `gh` CLI 已安装并完成身份验证
- 发布 PR 已创建

## 本地化版本

- [韩语（主要）](./README.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
