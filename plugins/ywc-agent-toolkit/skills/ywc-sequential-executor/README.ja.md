# ywc-sequential-executor

この文書は Codex の `ywc-sequential-executor` workflow を紹介します。正確な trigger、anti-trigger、実行手順、output format は [SKILL.md](./SKILL.md) を基準にします。

## Localized Versions

- [한국어](./README.md)
- [English](./README.en.md)
- [한국어 full](./README.ko.md)

## 使用シナリオ

- User がこの Skill の trigger phrase または同等の自然言語 request を入力したとき
- Codex が作業前に Skill 固有の workflow と validation criteria を揃える必要があるとき
- 他の `ywc-*` Skill が upstream または downstream step としてこの Skill を参照するとき

## 使用方法

```bash
$ywc-sequential-executor
```

対応する option と mode は [SKILL.md](./SKILL.md) の Arguments または Workflow section に従います。

### 主要 Mode

- `--aggregate-pr`: 各 task を個別 feature branch で実行し、結果を 1 つの work branch に local merge で累積して、最後に work -> base PR 1 件で delivery します。
- `--group-name <name>`: aggregate の work branch を `work/<name>` に固定します。`--aggregate-pr` と一緒に使う場合のみ有効です。
- `--worktree`: sequential invocation 全体を main checkout の外にある単一 run worktree で実行します。Delivery mode ではないため、他の mode flag と組み合わせられます。
- Stale `.ywc-run-state.json` guard: 保存済み run-state が今回の明示 range と一致しない場合、自動 resume せず、保存済み run-state を続けるか削除して新しい run を開始するかの選択を求めます。

## Contract / TDD baseline

振る舞いを変更する task では、実装前に changed public contracts と critical internals を記録し、failing test または contract assertion を先に確認します。docs-only、config-only、mechanical、no-harness の場合は明示的な TDD exception として報告します。Completion report には changed contracts、contract tests、critical internals、exceptions を含めます。

```bash
$ywc-sequential-executor 001010..003020 --aggregate-pr --group-name billing-rollout
```

```bash
$ywc-sequential-executor 001010..003020 --worktree --pr-lang ko
```

## 出力

この Skill は [SKILL.md](./SKILL.md) に定義された report、artifact、status format に従います。Completion Status を出力する場合、`DONE`、`DONE_WITH_CONCERNS`、`BLOCKED`、`NEEDS_CONTEXT` の意味を維持します。
