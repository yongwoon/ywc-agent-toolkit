# ywc-security-audit

認証・決済・個人情報に関連するコード変更時、または定期的なセキュリティ点検を実施するための Security Agent Skill です。

## 使用方法

```text
/ywc-security-audit --code api/src/middleware/
```

## 点検項目 (OWASP Top 10)

1. Injection (SQL, Command, LDAP)
2. Broken Authentication (Token, Session)
3. Sensitive Data Exposure
4. XSS (Reflected, Stored, DOM)
5. Broken Access Control
6. Security Misconfiguration
7. SSRF
8. Input Validation
9. Rate Limiting
10. Timing Attacks

## 実行 Agent

- **Security Agent** (claude-opus-4-20250514)

## 特に実行を推奨する状況

- middleware/ 変更時（認証・認可ロジック）
- 外部入力を受け付ける API Endpoint の追加・変更時
- 定期セキュリティ点検（月1回など）

## 出力形式

Critical / High / Medium / Low の重大度別に分類されます。各発見事項には file:line、リスク説明、推奨修正が含まれます。

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` フィールドに定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
