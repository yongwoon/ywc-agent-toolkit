<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# 处理 PR 审查

一个 Codex Skill，用于检查 PR 审查评论、在适当时应用修复，并回复每个讨论线程。

## 概述

此 Skill 自动化 PR 审查到达后的重复性工作。明确的变更请求会直接修复，而含糊或有争议的评论则会提交给用户判断。

### 主要特性

- 将评论分类为修复请求、有争议的反馈、问题和已处理项目
- 按文件分组评论，并将相关修复一起处理
- 将回复语言与审查者的语言匹配
- 跳过已处理或已回复的评论

## 使用方法

```text
/handle-pr-reviews
/handle-pr-reviews 123
```

自然语言触发词在 [SKILL.md](./SKILL.md) 中定义。

## 前提条件

- `gh` CLI 已安装并完成身份验证
- 命令在已有 PR 的分支上运行

## 本地化版本

- [韩语（主要）](./README.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
