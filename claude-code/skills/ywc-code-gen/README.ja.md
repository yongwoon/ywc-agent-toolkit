# ywc-code-gen

複数の Layer にわたるコードを同時に生成する Skill です。Backend + Frontend + QA Agent を並列で実行します。

## Test-first・Deep Module・Critical Module Review

default path は headlights を gate します：QA lane が Backend/Frontend 実装確定の前に失敗する(RED) test を先に作成します。`--tdd` はより強い full RED → GREEN → REFACTOR ritual を opt-in し、default minimal gate を置き換えます。Public interface を body より先に設計します(deep module)。生成ファイルが critical path(auth, payment, crypto, PII, external input)に触れる場合は internal review を要求し、`/ywc-security-audit` を required next step として明示します。Verification Gate は `git diff --stat` で spec 明示ファイルのみ変更されたか(diff scope)を確認し、Confidence Gate は Minimalism 次元で過剰に複雑な code(working ≠ minimal)を fail にします。詳細は `references/tdd-deep-module-gray-box.md` を参照してください。

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
