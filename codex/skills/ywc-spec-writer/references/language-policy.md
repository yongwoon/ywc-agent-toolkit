# Language Policy

## Default

Korean (`ko`) unless overridden by `--lang` or project guidance files (`AGENTS.md`, `CODEX.md`, `CLAUDE.md`).

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

## Shared Rules (All Languages)

- Zero program code in spec output
- Entity names in plain language (not schema field names)
- Flow steps written as actor + verb + object: "User submits the form"
- Acceptance criteria as observable outcomes, not technical implementation checks
