# ywc-code-gen

複数の Layer にわたるコードを同時に生成する Skill です。Backend + Frontend + QA Agent を並列で実行します。

## 使用方法

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
```

## 実行 Agent

| Agent                   | 生成物                                    |
| ----------------------- | ----------------------------------------- |
| Backend Agent (sonnet)  | API Route, Service, DB Migration          |
| Frontend Agent (sonnet) | UI Component, Query Hook, State 管理      |
| QA Agent (sonnet)       | Unit Test, Integration Test, E2E Scenario |

## sequential-executor との関係

- **sequential-executor**: 順次実行（依存関係のあるタスクに適しています）
- **/ywc-code-gen**: 独立 Layer の並列生成（SDK/API/Web が同時に必要な場合）
- 補完的に使用します

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` フィールドに定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
