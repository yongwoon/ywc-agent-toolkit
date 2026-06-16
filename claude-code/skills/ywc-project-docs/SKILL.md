---
name: ywc-project-docs
version: 2.2.0
description: "(ywc) Use when the user wants to generate or add project docs/ documentation in Korean or Japanese (Task, Architecture, Specification, Product, operational guides). Triggers: '문서 작성', '문서 만들어', '문서 추가해', 'document this', 'write a doc', 'add to docs/', 'ドキュメント作成', 'ドキュメントを書いて', '文書作成'. Do not use for code comments, README at repo root, English-only documentation, skill authoring (use ywc-skill-author), domain glossary entries (use ywc-ubiquitous-language), changelog or release notes (use ywc-changelog-release-notes), writing implementation tasks (use ywc-task-generator), or for README-locale entries / in-code WHY comments / hand-authored CHANGELOG entries (use ywc-doc-writer)."
category: spec
phase: planning
requires: []
advisor_budget: 0
allowed tools: Bash, Read, Write, Edit, Glob, Grep
---

# Project Documentation Generator (KR / JA)

**Announce at start:** "I'm using the ywc-project-docs skill to generate Korean/Japanese documentation aligned with the project's docs/ structure."

Generate documentation following the project's `docs/` directory structure,
naming conventions, and format patterns. Supports Korean and Japanese.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Language not specified, default to Korean" | Always ask. Default-language assumption produces wrong-language docs that get rewritten. |
| "Existing docs/ uses different naming, follow my own pattern" | Match the project's existing naming and structure exactly. Drift creates inconsistent docs over time. |
| "Translate Technical terms into Hangul/Katakana for readability" | Keep API, Backend, Database, etc. in English per the language policy. Transliteration breaks searchability. |
| "Doc target unclear, write a generic README" | If target type (Task, Architecture, Spec, Product, Operations) is ambiguous, ask. Generic docs are noise. |
| "Reuse content from another doc verbatim" | Cross-reference by relative path. Duplicated content drifts and becomes contradictory. |
| "Skip the spec/source link section, content is self-contained" | Always include source/spec references. Docs without source tracing become orphaned over time. |

**Violating the letter of these rules is violating the spirit.** Documentation that does not match repo conventions becomes documentation debt.

## Language Selection

Resolve the target language before doing anything else:

1. **`--lang` option present** — use it directly, no question needed.
   - `--lang kr` → Korean
   - `--lang ja` → Japanese
2. **No option** — ask:
   ```
   어떤 언어로 작성할까요? / Which language would you like?

     1. 한국어 (Korean)
     2. 日本語 (Japanese)
   ```
   Accept any of: `1` / `2`, `Korean` / `Japanese`, `한국어` / `日本語`,
   `kr` / `ja`, or a sentence containing a language name.

Then apply the corresponding policy from the Language Policy section below.

## Context

- Current docs structure: !`find docs/ -type f -name "*.md" ! -path "docs/imgs/*" | sort`
- Current tasks: !`ls docs/plans/ 2>/dev/null; ls docs/todo/ 2>/dev/null`

## Common Conventions

Directory structure, routing rules, naming conventions, document templates,
anti-patterns, folder-specific conventions (Architecture/Specification/Product),
and the pre-creation checklist follow the **shared reference**:

→ [`../references/project-docs-structure.md`](../references/project-docs-structure.md)

This skill's sole responsibility is generating documentation in the correct
language. Structure decisions are delegated to the reference above.

## Language Policy

### Korean

- **Body**: Korean prose
- **Technical terms**: English only — do not transliterate into Hangul
- **CLAUDE.md**: English only (exception)
- **Code blocks**: English (variable names and comments)
- Examples:
  - ✅ "Database 연결 설정" / ❌ "데이터베이스 연결 설정"
  - ✅ "API Endpoint 구현" / ❌ "API 엔드포인트 구현"

### Japanese

- **Body**: Japanese prose
- **Technical terms**: English only — do not transliterate into Katakana
- **CLAUDE.md**: English only (exception)
- **Code blocks**: English (variable names and comments)
- Examples:
  - ✅ "Database の接続設定" / ❌ "データベースの接続設定"
  - ✅ "API Endpoint の実装" / ❌ "API エンドポイントの実装"

## Document Structure Template

Follow the shared template structure; localize only the section labels.

**Korean labels:**

```markdown
# 제목

설명 (1-2문장)

> **관련 문서**
>
> - [문서 제목](../relative/path.md) — 한 줄 설명

---

## 목차

1. [섹션 1](#1-섹션-1)

---

## 1. 섹션 1

### 1.1 하위 섹션

내용...
```

**Japanese labels:**

```markdown
# タイトル

説明（1-2文）

> **関連ドキュメント**
>
> - [ドキュメントタイトル](../relative/path.md) — 一行説明

---

## 目次

1. [セクション1](#1-セクション1)

---

## 1. セクション1

### 1.1 サブセクション

内容...
```

Section structure, table-of-contents insertion conditions, and separator usage
follow the shared reference.

## Pre-creation Checklist

Before creating any document, confirm:

1. **Check for existing documents** — If a document on the same topic already exists, **update it** (do not create a new one).
2. **Select directory** — Confirm the appropriate directory from the routing rules in the shared reference.
3. **Cross-references** — If related documents exist, add bidirectional links (new → existing, existing → new).
4. **Official vs draft** — Place pre-finalized content in `todo/`; place finalized content in the official folder.
5. **CLAUDE.md rule** — Create documentation only when the user explicitly requests it.
