# Language Policy for Task Documents

This skill allows the user to choose the output language for task documents. If the user does not specify a language, ask for confirmation.

**Supported languages:** `ko` | `ja` | `en` | `es` | `zh` (default: `en`). Full language names (`korean`, `japanese`, `english`, `spanish`, `chinese`) are also accepted and map to these codes.

## How the User Specifies a Language

| User input example | Resolved to |
|---|---|
| "한국어로 task 생성해줘" | `ko` |
| "日本語でタスクを生成して" | `ja` |
| "Generate tasks in English" | `en` |
| "用中文生成 task" | `zh` |
| "Genera las tareas en español" | `es` |
| (not specified) | ask the user |

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

### Chinese (Simplified) (`zh`)

**Register**: 书面语 (formal written register) — appropriate for technical documentation.

**Technical terms**: Keep in English. Do not translate core terms into Chinese.

| Correct | Incorrect |
|---------|-----------|
| Database 连接配置 | 数据库连接配置 |
| API Endpoint 说明 | 接口端点说明 |
| User Flow | 用户流程 |
| Backend Service | 后端服务 |

**User story format**:
> "作为[用户类型]，我希望[操作]，以便[目的]。"

### Spanish (`es`)

**Register**: Plain business Spanish, formal *usted* register.

**Technical terms**: Keep in English. Do not translate core terms into Spanish.

| Correct | Incorrect |
|---------|-----------|
| Configuración de Database | Configuración de base de datos |
| Descripción de API Endpoint | Descripción de punto final |
| User Flow | Flujo de usuario |
| Backend Service | Servicio de backend |

**User story format**:
> "Como [tipo de usuario], quiero [acción] para [beneficio]."

## Technical Terms to Keep in English (Shared Across Locales)

API, Backend, Frontend, Database, Cache, Service, Repository, Application, Component, Module, Framework, Library, Request, Response, Schema, Model, Controller, Test, Debug, Deploy, Build, Configuration, Docker, Container, Server, Client, Router, Middleware
