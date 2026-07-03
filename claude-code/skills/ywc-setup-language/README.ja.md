# Setup Language Skill (ywc-setup-language)

Project または user 単位の **output language** を保存し、すべての language-aware な `ywc-*`
skill が per-call の `--lang` flag や prompt なしにその言語で document、PR text、commit message
を生成できるようにする Claude Code Skill。

## Overview

この Skill は適切な `CLAUDE.md` に canonical な `## Language Policy` セクションを書き込む:

- ywc-generated document(plan / spec / task)、PR title & body、commit message description の
  output language を設定
- Idempotent — 再実行時はセクションを append せず in-place で replace
- Read-only の `--show` mode で現在 resolve される言語とその source を報告
- Additive かつ non-blocking — policy のない project は従来どおり動作

この Skill は policy を **write** するのみ。Consuming skill がそれを resolve する方法(precedence
chain、code list、section format)は shared reference `references/language-resolution.md` にある。

## Usage

```text
/ywc-setup-language ko
```

```text
/ywc-setup-language ja --user
```

```text
/ywc-setup-language --show
```

Full language name も受け付けて正規化する: `korean` → `ko`、`japanese` → `ja`、
`english` → `en`、`spanish` → `es`、`chinese` → `zh`。

## Arguments

| Argument | Description |
| --- | --- |
| `<language>` | Output language code(`ko\|ja\|en\|es\|zh`)または full name。`--show` でなければ必須。 |
| `--user` | Project `CLAUDE.md` の代わりに user-global の `~/.claude/CLAUDE.md` に write。 |
| `--show` | Resolve される言語と source rung(project / user / none)を報告。Write なし。 |

## What it writes

```markdown
## Language Policy

- **Output language**: ko
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms.
```

## Precedence

設定された policy は consuming skill が読む resolution chain の 1 つの rung である:
`--lang` flag → project `## Language Policy` → user `## Language Policy` → 各 skill の
既存 fallback。Project policy が user policy に勝つ。全ルールは
`references/language-resolution.md` を参照。

## Consuming skills

`ywc-task-generator`、`ywc-spec-writer`、`ywc-plan`、`ywc-create-pr`、`ywc-commit`。
