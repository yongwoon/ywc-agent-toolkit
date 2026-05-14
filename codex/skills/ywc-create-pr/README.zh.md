<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# 创建 PR

一个 Codex Skill，用于提交更改并基于仓库的 PR 模板创建草稿 PR。

## 概述

在 feature 分支上的工作完成后，此 Skill 自动化从创建提交到创建草稿 PR 的完整流程。

### 主要特性

- 按 `develop` → `main` → `master` 顺序自动检测基础分支
- 对 `.env`、`*.key`、`*.pem` 等敏感文件执行安全检查
- 支持推送前的 CI 检查，如 lint、format、typecheck 和 test
- 在可用时应用 `.github/pull_request_template.md`
- 将每个 PR 创建为草稿

## 使用方法

```text
/create-pr
/create-pr main
/create-pr --skip-ci-check
/create-pr main --skip-ci-check
```

自然语言触发词在 [SKILL.md](./SKILL.md) 中定义。

## 前提条件

- `gh` CLI 已安装并完成身份验证
- 在 Git 仓库的 feature 分支上工作

## 本地化版本

- [韩语（主要）](./README.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
