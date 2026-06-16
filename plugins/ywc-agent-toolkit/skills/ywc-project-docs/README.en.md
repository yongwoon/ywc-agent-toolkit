# project-docs

A Codex Skill for generating Korean or Japanese documentation that follows
the project's `docs/` directory structure and conventions.

The target language is selected automatically from conversation context. Defaults
to **Korean**; switches to Japanese when the conversation is in Japanese or when
Japanese is explicitly requested.

## Usage

### Auto-trigger

The skill activates on natural-language phrases such as:

```
"문서 작성해줘"       (Korean: write a doc)
"문서 만들어줘"       (Korean: create a doc)
"document this"
"write a doc"
"add to docs/"
"ドキュメント作成して" (Japanese: create a document)
"ドキュメントを書いて" (Japanese: write a document)
```

### Manual invocation

```
/project-docs
```

## What This Skill Does

1. **Language selection** — detects conversation language and generates in Korean or Japanese
2. **Directory routing** — places documents in the correct `docs/` subdirectory based on intent
3. **Naming conventions** — applies lowercase kebab-case, minimal suffixes
4. **Document structure** — generates related-doc blocks, table of contents, and numbered sections
5. **Cross-references** — adds bidirectional links between related documents
6. **Language policy** — body text in the selected language; technical terms kept in English (no transliteration)
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

```
"제품 개요 문서 작성해줘"
→ docs/product/product-overview.md (Korean)

"인증 시스템 아키텍처 문서 작성해줘"
→ docs/architecture/authentication.md (Korean)

"認証システムのアーキテクチャドキュメントを書いて"
→ docs/architecture/authentication.md (Japanese)
```

## Localized Versions

- [Korean (Primary)](./README.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
