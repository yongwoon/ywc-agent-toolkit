# Language Policy

## Default

Korean (`ko`) unless overridden by `--lang` or the project's CLAUDE.md.

---

## Korean (`ko`)

**Formality**: 해요체 (polite, non-formal) — appropriate for internal project documentation.

**Technical terms**: Keep in English. Do not transliterate into Hangul.

| Correct | Incorrect |
|---------|-----------|
| Database 연결 설정 | 데이터베이스 연결 설정 |
| API Endpoint 설명 | API 엔드포인트 설명 |
| User Flow | 유저 플로우 |
| Backend Service | 백엔드 서비스 |

**User story format**:
> "[사용자 유형]로서, [행동]을 할 수 있어야 한다. 그래야 [목적]을 달성할 수 있기 때문이다."

---

## Japanese (`ja`)

**Formality**: です・ます体 (polite form) — appropriate for business documentation.

**Technical terms**: Keep in English. Do not convert to Katakana.

| Correct | Incorrect |
|---------|-----------|
| Database connection 設定 | データベースコネクション設定 |
| API Endpoint 説明 | API エンドポイント説明 |
| User Flow | ユーザーフロー |

**User story format**:
> "[ユーザータイプ]として、[アクション]を行いたい。なぜなら[目的]を達成するためだ。"

---

## English (`en`)

**Register**: Plain business English. Avoid jargon where plain language works.

**User story format**:
> "As a [user type], I want to [action] so that [benefit]."

---

## Chinese (Simplified) (`zh`)

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

---

## Spanish (`es`)

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

---

## Shared Rules (All Languages)

- Zero program code in spec output
- Entity names in plain language (not schema field names)
- Flow steps written as actor + verb + object: "User submits the form"
- Acceptance criteria as observable outcomes, not technical implementation checks
