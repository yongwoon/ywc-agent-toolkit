<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# Merge Dependabot Skill

一个 Codex Skill，用于安全地批量合并 Dependabot 创建的 Pull Request。

## 概述

此 Skill 检测 Dependabot PR，应用合并前安全检查，并按 PR 编号升序处理。

### 主要特性

- 批量检测并合并 Dependabot PR
- 支持仅安全合并模式
- 合并前检查 Dockerfile 基础镜像更改、主版本升级和 CI 状态
- 在可能时尝试解决冲突
- 最后生成汇总报告

## 使用方法

```text
/merge-dependabot
/merge-dependabot security
```

自然语言触发词在 [SKILL.md](./SKILL.md) 中定义。

## 前提条件

- `gh` CLI 已安装并完成身份验证
- 用户对仓库拥有合并权限
- 仓库中已存在 Dependabot PR

## 本地化版本

- [韩语（主要）](./README.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
