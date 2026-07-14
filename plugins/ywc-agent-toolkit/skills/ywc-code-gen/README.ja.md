# ywc-code-gen

複数の Layer にわたるコードを同時に生成する Skill です。Backend + Frontend + QA Agent を並列で実行します。

## 使用方法

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API" --review
```

## 実行 Agent

| Agent                   | 生成物                                    |
| ----------------------- | ----------------------------------------- |
| Backend Agent (sonnet)  | API Route, Service, DB Migration          |
| Frontend Agent (sonnet) | UI Component, Query Hook, State 管理      |
| QA Agent (sonnet)       | Unit Test, Integration Test, E2E Scenario |

## Contract / TDD baseline

Worker 実行前に Contract Snapshot を用意し、Backend、Frontend、QA が同じ public contract を参照するようにします。振る舞いを変更する生成は既定で test-first になり、`--tdd` はより厳密な RED/GREEN/REFACTOR checkpoint commit モードです。

## 任意の実装レビュー

`--review` を指定すると、生成結果が検証と Confidence Gate を通過した後に `ywc-impl-review` を実行します。review 専用 commit を作成せず、staged・unstaged・untracked・削除された生成変更を確認します(`--tdd` は checkpoint ごとに commit して working tree を空にするため、その場合の review 対象は `--git-range <pre-generation-sha>..HEAD` に切り替わります)。開始前の working tree はクリーンである必要があり、Critical/High の問題は一度修正して再レビューし、残る懸念は結果に保持します。

**`--review` なしでも**、生成ファイルが critical path(auth, payment, crypto, PII, external input)に該当する場合は `ywc-impl-review` と `ywc-security-audit` を強制実行します(`ywc-sequential-executor` と同じ契約)。**両方の** review の Critical/High finding が 1 回の fix cycle の対象となり、いずれかが `BLOCKED`/`NEEDS_CONTEXT` を返した場合は成功として報告せずそのまま伝播します。この Skill は merge 権限を持たないため、gate は blocking ではなく advisory です — 残った finding は状態を `DONE_WITH_CONCERNS` に下げるだけで、生成コードを破棄しません。

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
