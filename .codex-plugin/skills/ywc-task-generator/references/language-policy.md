# Language Policy for Task Documents

This skill allows the user to choose the output language for task documents. If the user does not specify a language, first infer it from the project's instruction files (`AGENTS.md`, `CODEX.md`, `CLAUDE.md`, or equivalent), then ask for confirmation only when no clear language policy is present.

**Supported languages:** `korean` | `japanese` | `english` (default: `english`)

## How the User Specifies a Language

| User input example | Resolved to |
|---|---|
| "한국어로 task 생성해줘" | korean |
| "日本語でタスクを生成して" | japanese |
| "Generate tasks in English" | english |
| (not specified) | infer from project instruction files; ask the user if inference fails |

## Language-Specific Writing Rules

### English

- Write all content in English.

### Korean (한국어) / Japanese (日本語) — Common Rules

- Write in the base language but **keep technical terms in English** (avoid transliterating foreign terms).
- Use consistent terminology throughout the document.

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

## Technical Terms to Keep in English (Shared Across Locales)

API, Backend, Frontend, Database, Cache, Service, Repository, Application, Component, Module, Framework, Library, Request, Response, Schema, Model, Controller, Test, Debug, Deploy, Build, Configuration, Docker, Container, Server, Client, Router, Middleware
