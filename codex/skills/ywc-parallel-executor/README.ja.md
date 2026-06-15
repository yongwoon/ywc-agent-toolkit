# ywc-parallel-executor

この文書は Codex の `ywc-parallel-executor` workflow を紹介します。正確な trigger、anti-trigger、実行手順、output format は [SKILL.md](./SKILL.md) を基準にします。

## Localized Versions

- [한국어](./README.md)
- [English](./README.en.md)
- [한국어 full](./README.ko.md)
- [Español](./README.es.md)
- [中文](./README.zh.md)

## 使用シナリオ

- User がこの Skill の trigger phrase または同等の自然言語 request を入力したとき
- Codex が作業前に Skill 固有の workflow と validation criteria を揃える必要があるとき
- 他の `ywc-*` Skill が upstream または downstream step としてこの Skill を参照するとき

## 使用方法

```bash
$ywc-parallel-executor
```

対応する option と mode は [SKILL.md](./SKILL.md) の Arguments または Workflow section に従います。

## Docker Isolation

Docker Compose を使う task worktree では、executor が port isolation を `ywc-docker-isolate` に委譲します。Worktree 作成前に selected task stack を audit し、各 worktree の検証後に task ごとの deterministic port を setup し、成功した task は worktree prune の前に stack を teardown します。`BLOCKED` または preserved worktree は復旧用に Docker state を保持します。

## Delivery Modes

| Mode | 動作 |
|---|---|
| `--local-merge` | 各 task を base branch に local merge して即時 push します。PR は作成しません。 |
| `--draft` | 各 task の変更を local merge で蓄積し、最後に aggregate draft PR を作成します。 |
| `--per-task-pr` | 各 task ごとに PR 作成、CI 待機、bot review 対応、最新 base refresh、PR merge、base sync、Mark Complete まで実行します。 |
| `--aggregate-pr` | invocation 全体を 1 つの aggregate branch と PR にまとめ、ready → CI → bot review → merge まで完了します。 |

`--per-task-pr` では、同じ wave の先行 task が base branch を進める場合があります。そのため merge 直前に PR branch が最新 base を含むか確認し、遅れている場合は worktree branch に base を merge して push し、CI を再確認します。Base refresh conflict は `BLOCKED` として報告し、古い head SHA の CI 結果だけで PR を merge しません。

## Group 実行

`--aggregate-pr --group-name <name>` は、多数の task を group 単位の単一 PR として delivery する場合に使います。複数 group を同時実行する場合は、worktree ではなく group ごとに独立した clone を使うのが安全です。詳細な手順と並行性ルールは [references/aggregate-pr.md](./references/aggregate-pr.md) を基準にします。

## 出力

この Skill は [SKILL.md](./SKILL.md) に定義された report、artifact、status format に従います。Completion Status を出力する場合、`DONE`、`DONE_WITH_CONCERNS`、`BLOCKED`、`NEEDS_CONTEXT` の意味を維持します。
