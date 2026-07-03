# project-docs

A Codex Skill for generating Korean, Japanese, English, Chinese, or Spanish
documentation that follows the project's `docs/` directory structure and
conventions.

If `--lang ko|ja|en|zh|es` is provided, it is used directly. Otherwise the skill resolves language through shared YWC language policy: `--lang` > `.codex/ywc.json` > `AGENTS.md` / `CODEX.md` / `CLAUDE.md` > `~/.codex/ywc.json` > ask user.

## Usage

### Auto-trigger

The skill activates on natural-language phrases such as:

```text
"문서 작성해줘"       (Korean: write a doc)
"문서 만들어줘"       (Korean: create a doc)
"document this"
"write a doc"
"add to docs/"
"English docs"
"Chinese docs"
"Spanish docs"
"中文文档"                (Chinese: Chinese documentation)
"documentación del proyecto" (Spanish: project documentation)
"ドキュメント作成して" (Japanese: create a document)
"ドキュメントを書いて" (Japanese: write a document)
```

### Manual invocation

```text
$ywc-project-docs              # resolves language through shared policy
$ywc-project-docs --lang ko    # write in Korean directly
$ywc-project-docs --lang ja    # write in Japanese directly
$ywc-project-docs --lang en    # write in English directly
$ywc-project-docs --lang zh    # write in Simplified Chinese directly
$ywc-project-docs --lang es    # write in Spanish directly
```

## What This Skill Does

1. **Language selection** — uses `--lang` if present, otherwise resolves through shared YWC language policy
2. **Directory routing** — places documents in the correct `docs/` subdirectory based on intent
3. **Naming conventions** — applies lowercase kebab-case, minimal suffixes
4. **Document structure** — generates related-doc blocks, table of contents, and numbered sections
5. **Cross-references** — adds bidirectional links between related documents
6. **Language policy** — body text in the selected language; technical terms kept in English (no transliteration or over-translation)
7. **Reading order** — preserves `product → architecture → specification → plans` for LLM consumption
8. **Anti-patterns** — prevents folder boundary mixing, duplicate storage, and draft/official confusion

## Directory Mapping

### Primary axis (core documents)

| Request Type | Target Directory |
|---|---|
| Product goals, scope, PRD | `docs/product/` |
| System design, technical decisions | `docs/architecture/` |
| Feature rules, implementation criteria | `docs/specification/` |
| Implementation order, milestones | `docs/plans/` |

### Secondary axis (operations, assets, drafts)

| Request Type | Target Directory |
|---|---|
| Operational procedures, setup guides | `docs/manuals/` |
| Incident handling, known issues | `docs/troubleshooting/` |
| UI mockups, design assets | `docs/design/` |
| Supporting images | `docs/imgs/` |
| Unconfirmed ideas, temporary notes | `docs/todo/` |

## Examples

```text
"제품 개요 문서 작성해줘"
→ docs/product/product-overview.md (Korean)

"인증 시스템 아키텍처 문서 작성해줘"
→ docs/architecture/authentication.md (Korean)

"認証システムのアーキテクチャドキュメントを書いて"
→ docs/architecture/authentication.md (Japanese)

"Write English documentation for the billing workflow"
→ docs/specification/billing.md (English)

"创建中文项目文档"
→ docs/product/product-overview.md (Chinese)

"Escribe documentación del proyecto para OAuth"
→ docs/manuals/oauth-setup.md (Spanish)
```

## Localized Versions

- [Korean (Primary)](./README.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
- [Chinese](./README.zh.md)
- [Spanish](./README.es.md)
