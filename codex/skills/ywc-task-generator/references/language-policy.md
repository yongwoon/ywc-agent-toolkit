# Language Policy for Task Documents

This skill allows the user to choose the output language for task documents.
Language resolution is defined by the shared Codex YWC policy:
[`../../references/language-resolution.md`](../../references/language-resolution.md).
The order is explicit `--lang` > project `.codex/ywc.json` > project guidance
(`AGENTS.md`, `CODEX.md`, `CLAUDE.md`) > user `~/.codex/ywc.json` > ask user.

**Supported languages:** `ko` | `ja` | `en` | `es` | `zh`

**Aliases:** `korean` / `한국어` → `ko`, `japanese` / `日本語` → `ja`, `english` → `en`, `spanish` / `espanol` / `español` → `es`, `chinese` / `中文` / `Chinese (Simplified)` → `zh`

## How the User Specifies a Language

| User input example | Resolved to |
|---|---|
| "한국어로 task 생성해줘" | `ko` |
| "日本語でタスクを生成して" | `ja` |
| "Generate tasks in English" | `en` |
| "中文 task docs" | `zh` |
| "PR Spanish로 작성" | `es` |
| "--lang zh" | `zh` |
| "--lang es" | `es` |
| (not specified) | resolve through the shared policy; ask the user if all tiers are unresolved |

## Language-Specific Writing Rules

### English

- Write all content in English.

### Korean (한국어) / Japanese (日本語) / Chinese (Simplified, 中文) / Spanish (Español) — Common Rules

- Write in the base language but **keep technical terms in English** (avoid transliterating foreign terms).
- Use consistent terminology throughout the document.
- Keep machine-facing surfaces in English: command names, file paths, YAML keys, JSON keys, task IDs, code blocks, and frontmatter keys.
- For `zh` / `chinese`, use Simplified Chinese unless the user explicitly asks for another Chinese locale.

#### Korean examples

| Correct | Incorrect |
|---|---|
| Database 연결 설정 | 데이터베이스 연결 설정 |
| API Endpoint 구현 | API 엔드포인트 구현 |
| Backend Service Logic | 백엔드 서비스 로직 |

#### Japanese examples

| Correct | Incorrect |
|---|---|
| Database connection 設定 | データベースコネクション設定 |
| API Endpoint 実装 | API エンドポイント実装 |
| Backend Service Logic | バックエンドサービスロジック |

#### Chinese examples

| Correct | Incorrect |
|---|---|
| Database 连接设置 | 数据库连接设置 |
| API Endpoint 实现 | API 端点实现 |
| Backend Service Logic | 后端服务逻辑 |

#### Spanish examples

| Correct | Incorrect |
|---|---|
| Configuración de Database connection | Configuración de base de datos |
| Implementar API Endpoint | Implementar punto final de API |
| Backend Service Logic | Lógica de servicio backend |

## Technical Terms to Keep in English (Shared Across Locales)

API, Backend, Frontend, Database, Cache, Service, Repository, Application, Component, Module, Framework, Library, Request, Response, Schema, Model, Controller, Test, Debug, Deploy, Build, Configuration, Docker, Container, Server, Client, Router, Middleware
