<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# Setup Language Skill（ywc-setup-language）

一个 Claude Code Skill，用于持久化 project 或 user 级别的 **output language**，使每个
language-aware 的 `ywc-*` skill 无需在每次调用时传入 `--lang` flag 或弹出 prompt，即可以该语言
生成 document、PR text 和 commit message。

## 概述

此 Skill 会在适当的 `CLAUDE.md` 中写入一个 canonical 的 `## Language Policy` 段落：

- 为 ywc-generated document(plan / spec / task)、PR title & body 和 commit message
  description 设置 output language
- Idempotent — 重新运行时在原位 replace 该段落，而不是 append 一个重复段落
- Read-only 的 `--show` mode 报告当前 resolve 出的语言及其来源
- Additive 且 non-blocking — 没有 policy 的 project 行为与之前完全一致

它只**写入** policy。Consuming skill 如何 resolve 它(precedence chain、code list、section
format)定义在 shared reference `references/language-resolution.md` 中。

## 用法

```text
/ywc-setup-language ko
```

```text
/ywc-setup-language ja --user
```

```text
/ywc-setup-language --show
```

也接受完整语言名称并进行归一化：`korean` → `ko`、`japanese` → `ja`、
`english` → `en`、`spanish` → `es`、`chinese` → `zh`。

## Arguments

| Argument | Description |
| --- | --- |
| `<language>` | Output language code(`ko\|ja\|en\|es\|zh`)或完整名称。非 `--show` 时必填。 |
| `--user` | 写入 user-global 的 `~/.claude/CLAUDE.md`，而非 project `CLAUDE.md`。 |
| `--show` | 报告 resolve 出的语言及其来源 rung(project / user / none)。不写入。 |

## 写入内容

```markdown
## Language Policy

- **Output language**: ko
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms.
```

## 优先级

配置的 policy 是 consuming skill 读取的 resolution chain 中的一个 rung：
`--lang` flag → project `## Language Policy` → user `## Language Policy` → 每个 skill 的
既有 fallback。Project policy 优先于 user policy。完整规则见
`references/language-resolution.md`。

## Consuming skills

`ywc-task-generator`、`ywc-spec-writer`、`ywc-plan`、`ywc-create-pr`、`ywc-commit`。
