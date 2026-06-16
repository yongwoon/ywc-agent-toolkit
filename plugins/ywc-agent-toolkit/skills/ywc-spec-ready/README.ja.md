# ywc-spec-ready

この文書は Codex の `ywc-spec-ready` workflow を紹介します。正確な trigger、anti-trigger、実行手順、output format は [SKILL.md](./SKILL.md) を基準にします。

## Localized Versions

- [한국어](./README.md)
- [English](./README.en.md)
- [한국어 full](./README.ko.md)

## 使用シナリオ

- 自然言語 goal を task generation 前の validated spec にする必要があるとき
- 既存 spec を `ywc-task-generator` 前に `ywc-spec-validate` の `DONE` 状態まで確認するとき
- `DONE_WITH_CONCERNS` を `ywc-plan --update-spec` loop で収束させる必要があるとき

## 使用方法

```bash
$ywc-spec-ready "支払い失敗時の復旧 UX を設計して"
$ywc-spec-ready --spec docs/ywc-plans/example.md --max-iterations 4
$ywc-spec-ready --spec docs/ywc-plans/example.md --dry-run
```

成功時、この Skill は `ywc-task-generator <spec-path>` を出力して停止します。task generation や implementation は直接実行しません。

## 出力

この Skill は [SKILL.md](./SKILL.md) に定義された report、loop log、status format に従います。
